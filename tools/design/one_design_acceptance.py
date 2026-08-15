"""一件の設計と受入条件を決定的に照合する。"""

import hashlib
import json
import os
import re
import stat


_SAFE_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_OPERATORS = frozenset(("equals", "not_equals", "contains_all", "contains_none"))
_QUEUE_ORDER = ("contradicted", "missing", "satisfied", "unreferenced_fact")
_INTEGER_LIMIT = 9007199254740991
_INPUT_SIZE_LIMIT = 262144


class DesignAcceptanceStop(Exception):
    """入力を安全に照合できないため処理を停止する。"""

    def __init__(self, reason, source):
        super().__init__(reason)
        self.reason = reason
        self.source = source


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


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateMember
        value[key] = item
    return value


def _decode_input(raw, source):
    if not isinstance(raw, bytes):
        raise DesignAcceptanceStop("invalid_schema", source)
    decode_failed = False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        decode_failed = True
    if decode_failed:
        raise DesignAcceptanceStop("invalid_utf8", source)
    schema_failed = False
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, _DuplicateMember, RecursionError):
        schema_failed = True
    if schema_failed:
        raise DesignAcceptanceStop("invalid_schema", source)
    return value


def _is_safe_identifier(value):
    return isinstance(value, str) and _SAFE_IDENTIFIER.fullmatch(value) is not None


def _normalize_value(value, source):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if -_INTEGER_LIMIT <= value <= _INTEGER_LIMIT:
            return value
        raise DesignAcceptanceStop("invalid_schema", source)
    if isinstance(value, str):
        if 1 <= len(value) <= 2000 and "\x00" not in value:
            return value
        raise DesignAcceptanceStop("invalid_schema", source)
    if isinstance(value, list):
        if not 1 <= len(value) <= 32:
            raise DesignAcceptanceStop("invalid_schema", source)
        if any(
            not isinstance(item, str)
            or not 1 <= len(item) <= 256
            or "\x00" in item
            for item in value
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        if len(set(value)) != len(value):
            raise DesignAcceptanceStop("invalid_schema", source)
        return sorted(value)
    raise DesignAcceptanceStop("invalid_schema", source)


def _normalize_design(value):
    source = "design"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "design_identifier",
        "facts",
    }:
        raise DesignAcceptanceStop("invalid_schema", source)
    if value["schema_version"] != 1 or not _is_safe_identifier(
        value["design_identifier"]
    ):
        raise DesignAcceptanceStop("invalid_schema", source)
    facts = value["facts"]
    if not isinstance(facts, list) or not 1 <= len(facts) <= 256:
        raise DesignAcceptanceStop("invalid_schema", source)

    normalized_facts = []
    fact_ids = set()
    subjects = set()
    for fact in facts:
        if not isinstance(fact, dict) or set(fact) != {
            "fact_id",
            "subject",
            "value",
        }:
            raise DesignAcceptanceStop("invalid_schema", source)
        fact_id = fact["fact_id"]
        subject = fact["subject"]
        if (
            not _is_safe_identifier(fact_id)
            or not _is_safe_identifier(subject)
            or fact_id in fact_ids
            or subject in subjects
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        fact_ids.add(fact_id)
        subjects.add(subject)
        normalized_facts.append(
            {
                "fact_id": fact_id,
                "subject": subject,
                "value": _normalize_value(fact["value"], source),
            }
        )

    normalized_facts.sort(key=lambda fact: (fact["subject"], fact["fact_id"]))
    return {
        "schema_version": 1,
        "design_identifier": value["design_identifier"],
        "facts": normalized_facts,
    }


def _normalize_acceptance(value):
    source = "acceptance"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "acceptance_identifier",
        "conditions",
    }:
        raise DesignAcceptanceStop("invalid_schema", source)
    if value["schema_version"] != 1 or not _is_safe_identifier(
        value["acceptance_identifier"]
    ):
        raise DesignAcceptanceStop("invalid_schema", source)
    conditions = value["conditions"]
    if not isinstance(conditions, list) or not 1 <= len(conditions) <= 256:
        raise DesignAcceptanceStop("invalid_schema", source)

    normalized_conditions = []
    condition_ids = set()
    subjects = set()
    for condition in conditions:
        if not isinstance(condition, dict) or set(condition) != {
            "condition_id",
            "subject",
            "operator",
            "expected",
        }:
            raise DesignAcceptanceStop("invalid_schema", source)
        condition_id = condition["condition_id"]
        subject = condition["subject"]
        operator = condition["operator"]
        if (
            not _is_safe_identifier(condition_id)
            or not _is_safe_identifier(subject)
            or condition_id in condition_ids
            or subject in subjects
            or operator not in _OPERATORS
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        expected = _normalize_value(condition["expected"], source)
        if operator in ("contains_all", "contains_none") and not isinstance(
            expected,
            list,
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        condition_ids.add(condition_id)
        subjects.add(subject)
        normalized_conditions.append(
            {
                "condition_id": condition_id,
                "subject": subject,
                "operator": operator,
                "expected": expected,
            }
        )

    normalized_conditions.sort(key=lambda condition: condition["condition_id"])
    return {
        "schema_version": 1,
        "acceptance_identifier": value["acceptance_identifier"],
        "conditions": normalized_conditions,
    }


def _typed_equal(actual, expected):
    return type(actual) is type(expected) and actual == expected


def _is_satisfied(operator, actual, expected):
    if operator == "equals":
        return _typed_equal(actual, expected)
    if operator == "not_equals":
        return not _typed_equal(actual, expected)
    if not isinstance(actual, list):
        return False
    actual_values = set(actual)
    expected_values = set(expected)
    if operator == "contains_all":
        return expected_values.issubset(actual_values)
    return actual_values.isdisjoint(expected_values)


def _build_result(design, acceptance):
    facts_by_subject = {fact["subject"]: fact for fact in design["facts"]}
    used_fact_ids = set()
    results = []
    identifiers_by_kind = {kind: [] for kind in _QUEUE_ORDER}

    for condition in acceptance["conditions"]:
        fact = facts_by_subject.get(condition["subject"])
        if fact is None:
            disposition = "missing"
            fact_id = None
            actual_sha256 = None
        else:
            fact_id = fact["fact_id"]
            used_fact_ids.add(fact_id)
            actual_sha256 = _sha256(fact["value"])
            disposition = (
                "satisfied"
                if _is_satisfied(
                    condition["operator"],
                    fact["value"],
                    condition["expected"],
                )
                else "contradicted"
            )
        identifiers_by_kind[disposition].append(condition["condition_id"])
        results.append(
            {
                "condition_id": condition["condition_id"],
                "subject": condition["subject"],
                "disposition": disposition,
                "fact_id": fact_id,
                "operator": condition["operator"],
                "expected_value_sha256": _sha256(condition["expected"]),
                "actual_value_sha256": actual_sha256,
            }
        )

    unreferenced = sorted(
        fact["fact_id"]
        for fact in design["facts"]
        if fact["fact_id"] not in used_fact_ids
    )
    identifiers_by_kind["unreferenced_fact"] = unreferenced
    counts = {
        "contradicted": len(identifiers_by_kind["contradicted"]),
        "missing": len(identifiers_by_kind["missing"]),
        "satisfied": len(identifiers_by_kind["satisfied"]),
        "unreferenced_fact": len(unreferenced),
    }
    queue = [
        {"identifiers": sorted(identifiers_by_kind[kind]), "kind": kind}
        for kind in _QUEUE_ORDER
        if identifiers_by_kind[kind]
    ]
    result = {
        "acceptance": {
            "condition_count": len(acceptance["conditions"]),
            "identifier": acceptance["acceptance_identifier"],
            "sha256": _sha256(acceptance),
        },
        "counts": counts,
        "decision_status": "pending_human_decision",
        "design": {
            "fact_count": len(design["facts"]),
            "identifier": design["design_identifier"],
            "sha256": _sha256(design),
        },
        "external_send_approved": False,
        "human_decision_queue": queue,
        "results": results,
        "schema_version": 1,
        "status": "comparison_completed",
        "unreferenced_fact_ids": unreferenced,
        "verdict": (
            "review_required"
            if counts["missing"] or counts["contradicted"]
            else "conditions_met_pending_human_decision"
        ),
    }
    result["comparison_sha256"] = _sha256(result)
    return result


def _absolute_path_parts(value):
    if not isinstance(value, str) or not value.startswith("/"):
        raise DesignAcceptanceStop("invalid_path", "arguments")
    if value == "/":
        return ()
    parts = value.split("/")[1:]
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise DesignAcceptanceStop("invalid_path", "arguments")
    return tuple(parts)


def _required_open_flags():
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    directory = getattr(os, "O_DIRECTORY", 0)
    nonblock = getattr(os, "O_NONBLOCK", 0)
    if not no_follow or not directory or not nonblock:
        raise DesignAcceptanceStop("unreadable_input", "none")
    return no_follow, directory, nonblock


def _open_root(root_parts, no_follow, directory):
    flags = os.O_RDONLY | no_follow | directory
    current = None
    open_failed = False
    try:
        current = os.open("/", flags)
        for component in root_parts:
            next_descriptor = os.open(component, flags, dir_fd=current)
            os.close(current)
            current = next_descriptor
    except OSError:
        open_failed = True
    if open_failed:
        if current is not None:
            try:
                os.close(current)
            except OSError:
                pass
        raise DesignAcceptanceStop("unreadable_input", "none")
    return current


def _open_file_from_root(
    root_descriptor,
    relative_parts,
    source,
    no_follow,
    directory,
    nonblock,
):
    current = None
    file_descriptor = None
    open_failed = False
    try:
        current = os.dup(root_descriptor)
        directory_flags = os.O_RDONLY | no_follow | directory
        for component in relative_parts[:-1]:
            next_descriptor = os.open(
                component,
                directory_flags,
                dir_fd=current,
            )
            os.close(current)
            current = next_descriptor
        file_descriptor = os.open(
            relative_parts[-1],
            os.O_RDONLY | no_follow | nonblock,
            dir_fd=current,
        )
        os.close(current)
    except OSError:
        open_failed = True
    if open_failed:
        if current is not None:
            try:
                os.close(current)
            except OSError:
                pass
        if file_descriptor is not None:
            try:
                os.close(file_descriptor)
            except OSError:
                pass
        raise DesignAcceptanceStop("unreadable_input", source)
    return file_descriptor


def _read_regular_file(file_descriptor, source):
    read_failed = False
    try:
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise DesignAcceptanceStop("unreadable_input", source)
        if before.st_size > _INPUT_SIZE_LIMIT:
            raise DesignAcceptanceStop("size_limit_exceeded", source)
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
            raise DesignAcceptanceStop("size_limit_exceeded", source)
        after = os.fstat(file_descriptor)
    except DesignAcceptanceStop:
        raise
    except OSError:
        read_failed = True
    if read_failed:
        raise DesignAcceptanceStop("unreadable_input", source)

    before_identity = (before.st_mode, before.st_size, before.st_dev, before.st_ino)
    after_identity = (after.st_mode, after.st_size, after.st_dev, after.st_ino)
    if (
        not stat.S_ISREG(after.st_mode)
        or before_identity != after_identity
        or len(data) != before.st_size
    ):
        raise DesignAcceptanceStop("unreadable_input", source)
    return data, (before.st_dev, before.st_ino)


def _read_one_input(
    root_descriptor,
    relative_parts,
    source,
    no_follow,
    directory,
    nonblock,
):
    file_descriptor = _open_file_from_root(
        root_descriptor,
        relative_parts,
        source,
        no_follow,
        directory,
        nonblock,
    )
    try:
        return _read_regular_file(file_descriptor, source)
    finally:
        os.close(file_descriptor)


def read_input_pair(input_root, design_path, acceptance_path):
    """明示root内の異なる通常file二件を非追跡で安全に読む。"""

    root_parts = _absolute_path_parts(input_root)
    design_parts = _absolute_path_parts(design_path)
    acceptance_parts = _absolute_path_parts(acceptance_path)
    root_size = len(root_parts)
    if (
        design_parts[:root_size] != root_parts
        or acceptance_parts[:root_size] != root_parts
        or len(design_parts) <= root_size
        or len(acceptance_parts) <= root_size
        or design_parts == acceptance_parts
    ):
        raise DesignAcceptanceStop("invalid_path", "arguments")

    no_follow, directory, nonblock = _required_open_flags()
    root_descriptor = _open_root(root_parts, no_follow, directory)
    try:
        design_data, design_identity = _read_one_input(
            root_descriptor,
            design_parts[root_size:],
            "design",
            no_follow,
            directory,
            nonblock,
        )
        acceptance_data, acceptance_identity = _read_one_input(
            root_descriptor,
            acceptance_parts[root_size:],
            "acceptance",
            no_follow,
            directory,
            nonblock,
        )
    finally:
        os.close(root_descriptor)
    if design_identity == acceptance_identity:
        raise DesignAcceptanceStop("invalid_path", "arguments")
    return design_data, acceptance_data


def compare_inputs(design_bytes, acceptance_bytes):
    """検査・正規化した設計と受入条件を照合する。"""

    design = _normalize_design(_decode_input(design_bytes, "design"))
    acceptance = _normalize_acceptance(
        _decode_input(acceptance_bytes, "acceptance")
    )
    return _build_result(design, acceptance)
