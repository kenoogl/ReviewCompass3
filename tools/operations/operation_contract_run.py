"""承認済み運用契約一件で受入済み部品一件を実行し、実行記録を着地させる。"""

import hashlib
import io
import json
import os
import re
import stat

from tools.design.one_design_acceptance_entry import main as design_acceptance_main
from tools.requirements.one_requirement_feature_source_entry import (
    main as requirement_candidate_main,
)
from tools.session_logs.redaction import default_pattern_rules
from tools.session_logs.redaction import find_high_entropy


_GENERAL_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256_VALUE = re.compile(r"[0-9a-f]{64}\Z")
_INPUT_SIZE_LIMIT = 262144
_CONTRACT_MEMBERS = frozenset(
    (
        "schema_version",
        "contract_identifier",
        "human_approved",
        "operation",
        "input_root",
        "inputs",
        "expected_bindings",
        "output_root",
    )
)
_OPERATIONS = {
    "design_acceptance_check": {
        "entry": design_acceptance_main,
        "input_names": ("design", "acceptance"),
        "argument_names": {"design": "--design", "acceptance": "--acceptance"},
        "binding_positions": {
            "design": ("design", "sha256"),
            "acceptance": ("acceptance", "sha256"),
        },
    },
    "requirement_candidate_check": {
        "entry": requirement_candidate_main,
        "input_names": ("catalog", "candidate"),
        "argument_names": {"catalog": "--catalog", "candidate": "--candidate"},
        "binding_positions": {
            "catalog": ("catalog", "sha256"),
            "candidate": ("candidate", "sha256"),
        },
    },
}


class OperationContractStop(Exception):
    """運用契約を安全に実行できないため処理を停止する。"""

    def __init__(self, reason, source, extra=None):
        super().__init__(reason)
        self.reason = reason
        self.source = source
        self.extra = extra


class _DuplicateMember(ValueError):
    """復号後のJSON項目名が重複している。"""


def canonical_json_bytes(value):
    """値を内容識別値用の正準JSON bytesへ変換する。"""

    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _absolute_path_parts(value, reason, source):
    if not isinstance(value, str) or not value.startswith("/"):
        raise OperationContractStop(reason, source)
    if value == "/":
        return ()
    parts = value.split("/")[1:]
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise OperationContractStop(reason, source)
    return tuple(parts)


def _required_open_flags():
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    directory = getattr(os, "O_DIRECTORY", 0)
    nonblock = getattr(os, "O_NONBLOCK", 0)
    if not no_follow or not directory or not nonblock:
        raise OperationContractStop("unreadable_input", "contract")
    return no_follow, directory, nonblock


def read_contract_file(contract_path):
    """契約fileを非追跡で安全に読む。"""

    parts = _absolute_path_parts(contract_path, "invalid_path", "arguments")
    if not parts:
        raise OperationContractStop("invalid_path", "arguments")
    no_follow, directory, nonblock = _required_open_flags()
    directory_flags = os.O_RDONLY | no_follow | directory
    current = None
    file_descriptor = None
    open_failed = False
    try:
        current = os.open("/", directory_flags)
        for component in parts[:-1]:
            next_descriptor = os.open(component, directory_flags, dir_fd=current)
            os.close(current)
            current = next_descriptor
        file_descriptor = os.open(
            parts[-1],
            os.O_RDONLY | no_follow | nonblock,
            dir_fd=current,
        )
        os.close(current)
        current = None
    except OSError:
        open_failed = True
    if open_failed:
        if current is not None:
            try:
                os.close(current)
            except OSError:
                pass
        raise OperationContractStop("unreadable_input", "contract")

    read_failed = False
    try:
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise OperationContractStop("unreadable_input", "contract")
        if before.st_size > _INPUT_SIZE_LIMIT:
            raise OperationContractStop("size_limit_exceeded", "contract")
        chunks = []
        remaining = _INPUT_SIZE_LIMIT + 1
        while remaining:
            chunk = os.read(file_descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > _INPUT_SIZE_LIMIT:
            raise OperationContractStop("size_limit_exceeded", "contract")
        after = os.fstat(file_descriptor)
    except OperationContractStop:
        os.close(file_descriptor)
        raise
    except OSError:
        read_failed = True
    if read_failed:
        os.close(file_descriptor)
        raise OperationContractStop("unreadable_input", "contract")
    os.close(file_descriptor)

    before_identity = (before.st_mode, before.st_size, before.st_dev, before.st_ino)
    after_identity = (after.st_mode, after.st_size, after.st_dev, after.st_ino)
    if (
        not stat.S_ISREG(after.st_mode)
        or before_identity != after_identity
        or len(data) != before.st_size
    ):
        raise OperationContractStop("unreadable_input", "contract")
    return data


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateMember
        value[key] = item
    return value


def _decode_contract(raw):
    source = "contract"
    if not isinstance(raw, bytes):
        raise OperationContractStop("invalid_schema", source)
    decode_failed = False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        decode_failed = True
    if decode_failed:
        raise OperationContractStop("invalid_utf8", source)
    schema_failed = False
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError, RecursionError):
        schema_failed = True
    if schema_failed:
        raise OperationContractStop("invalid_schema", source)
    return value


def _is_excluded_binding_digest(path, text):
    return (
        len(path) == 2
        and path[0] == "expected_bindings"
        and _SHA256_VALUE.fullmatch(text) is not None
    )


def _is_excluded_operation_name(path, text):
    return len(path) == 1 and path[0] == "operation" and text in _OPERATIONS


def _iter_strings(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key, None
            yield from _iter_strings(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_strings(item, path + (index,))
    elif isinstance(value, str):
        yield value, path


def _scan_sensitive(value):
    rules = default_pattern_rules()
    for text, path in _iter_strings(value):
        if path is not None and (
            _is_excluded_binding_digest(path, text)
            or _is_excluded_operation_name(path, text)
        ):
            continue
        if any(re.search(rule.pattern, text) for rule in rules):
            raise OperationContractStop("sensitive_data_remaining", "contract")
        if find_high_entropy(text):
            raise OperationContractStop("sensitive_data_remaining", "contract")


def _has_only_unicode_scalar_values(value):
    return not any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _require_lexical_absolute(value, source):
    if (
        not isinstance(value, str)
        or "\x00" in value
        or not _has_only_unicode_scalar_values(value)
    ):
        raise OperationContractStop("invalid_schema", source)
    _absolute_path_parts(value, "invalid_schema", source)
    return value


def _validate_contract(value):
    source = "contract"
    if not isinstance(value, dict) or set(value) != _CONTRACT_MEMBERS:
        raise OperationContractStop("invalid_schema", source)
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise OperationContractStop("invalid_schema", source)
    identifier = value["contract_identifier"]
    if (
        not isinstance(identifier, str)
        or _GENERAL_IDENTIFIER.fullmatch(identifier) is None
    ):
        raise OperationContractStop("invalid_schema", source)
    if value["human_approved"] is not True:
        raise OperationContractStop("invalid_schema", source)
    operation = value["operation"]
    if operation not in _OPERATIONS:
        raise OperationContractStop("invalid_schema", source)
    definition = _OPERATIONS[operation]
    input_names = definition["input_names"]
    _require_lexical_absolute(value["input_root"], source)
    inputs = value["inputs"]
    if not isinstance(inputs, dict) or set(inputs) != set(input_names):
        raise OperationContractStop("invalid_schema", source)
    for name in input_names:
        _require_lexical_absolute(inputs[name], source)
    bindings = value["expected_bindings"]
    if not isinstance(bindings, dict) or set(bindings) != set(input_names):
        raise OperationContractStop("invalid_schema", source)
    for name in input_names:
        digest = bindings[name]
        if not isinstance(digest, str) or _SHA256_VALUE.fullmatch(digest) is None:
            raise OperationContractStop("invalid_schema", source)
    _require_lexical_absolute(value["output_root"], source)
    return value


def _record_paths(value):
    final_name = f"{value['contract_identifier']}--execution-v1.json"
    output_root = value["output_root"]
    final_path = f"{output_root}/{final_name}"
    partial_path = f"{final_path}.partial"
    return final_path, partial_path


def _check_output_root(value):
    output_root = value["output_root"]
    final_path, partial_path = _record_paths(value)
    root_check_failed = False
    try:
        details = os.lstat(output_root)
        if not stat.S_ISDIR(details.st_mode):
            root_check_failed = True
    except OSError:
        root_check_failed = True
    if root_check_failed:
        raise OperationContractStop("invalid_output_root", "output")
    for existing in (final_path, partial_path):
        present = True
        try:
            os.lstat(existing)
        except OSError:
            present = False
        if present:
            raise OperationContractStop("invalid_output_root", "output")
    return final_path, partial_path


def _run_part(value):
    definition = _OPERATIONS[value["operation"]]
    arguments = ["check", "--input-root", value["input_root"]]
    for name in definition["input_names"]:
        arguments.append(definition["argument_names"][name])
        arguments.append(value["inputs"][name])
    buffer = io.BytesIO()
    exit_code = definition["entry"](arguments, output=buffer)
    payload = buffer.getvalue()
    if not payload.endswith(b"\n"):
        raise OperationContractStop("internal_failure", "none")
    parse_failed = False
    try:
        result = json.loads(payload[:-1].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        parse_failed = True
    if parse_failed or not isinstance(result, dict):
        raise OperationContractStop("internal_failure", "none")
    if exit_code != 0:
        reason = result.get("reason")
        part_source = result.get("source")
        if (
            result.get("status") != "stopped"
            or not isinstance(reason, str)
            or not isinstance(part_source, str)
        ):
            raise OperationContractStop("internal_failure", "none")
        raise OperationContractStop(
            "part_stopped",
            "part",
            extra={
                "part_reason": reason,
                "part_source": part_source,
                "part_exit_code": exit_code,
            },
        )
    return result, payload


def _check_bindings(value, part_result):
    definition = _OPERATIONS[value["operation"]]
    bindings = []
    for name in sorted(definition["input_names"]):
        expected = value["expected_bindings"][name]
        reported = part_result
        lookup_failed = False
        for key in definition["binding_positions"][name]:
            if not isinstance(reported, dict) or key not in reported:
                lookup_failed = True
                break
            reported = reported[key]
        if lookup_failed or not isinstance(reported, str):
            raise OperationContractStop("internal_failure", "none")
        if expected != reported:
            raise OperationContractStop("binding_mismatch", "contract")
        bindings.append(
            {
                "name": name,
                "expected_sha256": expected,
                "reported_sha256": reported,
            }
        )
    return bindings


def _build_record(value, bindings, part_result, part_payload):
    record = {
        "status": "operation_executed",
        "schema_version": 1,
        "contract": {
            "identifier": value["contract_identifier"],
            "sha256": _sha256(value),
        },
        "operation": value["operation"],
        "bindings": bindings,
        "part_exit_code": 0,
        "part_result": part_result,
        "part_result_sha256": hashlib.sha256(part_payload[:-1]).hexdigest(),
        "decision_status": "pending_human_decision",
        "external_send_approved": False,
    }
    record["record_sha256"] = _sha256(record)
    return record


def _read_back_bytes(partial_path, size_limit):
    descriptor = os.open(partial_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        chunks = []
        remaining = size_limit + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _recover_partial(partial_path):
    try:
        os.unlink(partial_path)
    except OSError:
        pass


def _publish_record(record, final_path, partial_path):
    record_bytes = canonical_json_bytes(record) + b"\n"
    creation_failed = False
    descriptor = None
    try:
        descriptor = os.open(
            partial_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except OSError:
        creation_failed = True
    if creation_failed:
        raise OperationContractStop("record_write_failed", "output")

    write_failed = False
    try:
        written = os.write(descriptor, record_bytes)
        if written != len(record_bytes):
            write_failed = True
    except OSError:
        write_failed = True
    finally:
        try:
            os.close(descriptor)
        except OSError:
            write_failed = True
    if write_failed:
        _recover_partial(partial_path)
        raise OperationContractStop("record_write_failed", "output")

    verify_failed = False
    try:
        if _read_back_bytes(partial_path, len(record_bytes)) != record_bytes:
            verify_failed = True
    except OSError:
        verify_failed = True
    if verify_failed:
        _recover_partial(partial_path)
        raise OperationContractStop("record_write_failed", "output")

    publish_failed = False
    try:
        os.link(partial_path, final_path)
    except OSError:
        publish_failed = True
    if publish_failed:
        _recover_partial(partial_path)
        raise OperationContractStop("record_write_failed", "output")

    cleanup_failed = False
    try:
        os.unlink(partial_path)
    except OSError:
        cleanup_failed = True
    if cleanup_failed:
        raise OperationContractStop("partial_cleanup_failed", "output")
    return record_bytes


def run_operation_contract(contract_path):
    """契約fileを検査し、部品一件を実行し、実行記録一件を着地させる。"""

    raw = read_contract_file(contract_path)
    decoded = _decode_contract(raw)
    _scan_sensitive(decoded)
    value = _validate_contract(decoded)
    final_path, partial_path = _check_output_root(value)
    part_result, part_payload = _run_part(value)
    bindings = _check_bindings(value, part_result)
    record = _build_record(value, bindings, part_result, part_payload)
    return _publish_record(record, final_path, partial_path)
