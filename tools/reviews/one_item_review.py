"""一件レビュー材料と結果集合を扱う読取り専用の製品核。"""

import errno
import json
import os
import re
import stat
from pathlib import Path

from tools.common.digests import canonical_json_bytes, sha256_hex
from tools.session_logs.redaction import default_pattern_rules, find_high_entropy


MATERIAL_MAX_BYTES = 262_144
REVIEW_SPEC_MAX_BYTES = 65_536
RESULTS_MAX_BYTES = 1_048_576

_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
_FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9._~/-])/(?:[^/\s\"'<>]+/)*[^/\s\"'<>]+"),
    re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|\\\\)[^\s\"'<>]+"),
    re.compile(r"(?<![A-Za-z0-9:])//[^/\\\s\"'<>]+[/\\][^\s\"'<>]+"),
    re.compile(r"\bfile://[^\s\"'<>]+", re.IGNORECASE),
)


class ReviewStop(Exception):
    """契約境界を安全に満たせない。"""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


def _absolute_path(value):
    try:
        path = Path(value)
    except TypeError as error:
        raise ReviewStop("invalid_path") from error
    if not path.is_absolute() or ".." in path.parts:
        raise ReviewStop("invalid_path")
    return Path(os.path.normpath(path))


def _open_directory(parent_fd, name):
    try:
        entry = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except OSError as error:
        raise ReviewStop("unreadable_input") from error
    if stat.S_ISLNK(entry.st_mode) or not stat.S_ISDIR(entry.st_mode):
        raise ReviewStop("invalid_path")
    try:
        return os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise ReviewStop("invalid_path") from error
        raise ReviewStop("unreadable_input") from error


def _open_root(root):
    current_fd = os.open("/", _DIRECTORY_FLAGS)
    try:
        for part in root.parts[1:]:
            next_fd = _open_directory(current_fd, part)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _relative_parts(root, input_path):
    try:
        relative = input_path.relative_to(root)
    except ValueError as error:
        raise ReviewStop("invalid_path") from error
    if not relative.parts:
        raise ReviewStop("invalid_path")
    return relative.parts


def _open_input(root_fd, relative_parts):
    current_fd = os.dup(root_fd)
    try:
        for part in relative_parts[:-1]:
            next_fd = _open_directory(current_fd, part)
            os.close(current_fd)
            current_fd = next_fd
        try:
            file_descriptor = os.open(
                relative_parts[-1],
                _FILE_FLAGS,
                dir_fd=current_fd,
            )
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                raise ReviewStop("invalid_path") from error
            raise ReviewStop("unreadable_input") from error
        return file_descriptor
    finally:
        os.close(current_fd)


def _read_file(root, root_fd, input_path, max_bytes):
    relative_parts = _relative_parts(root, input_path)
    file_descriptor = _open_input(root_fd, relative_parts)
    try:
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ReviewStop("invalid_path")
        if before.st_size > max_bytes:
            raise ReviewStop("size_limit_exceeded")

        chunks = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(file_descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        content = b"".join(chunks)

        after = os.fstat(file_descriptor)
        if not stat.S_ISREG(after.st_mode):
            raise ReviewStop("invalid_path")
        if len(content) > max_bytes or after.st_size > max_bytes:
            raise ReviewStop("size_limit_exceeded")
        if before.st_size != after.st_size or len(content) != after.st_size:
            raise ReviewStop("unreadable_input")
        if not content or b"\x00" in content:
            raise ReviewStop("invalid_schema")
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ReviewStop("invalid_utf8") from error
        return content, (after.st_dev, after.st_ino)
    finally:
        os.close(file_descriptor)


def read_input_files(*, input_root, material, review_spec, results=None):
    """明示されたroot内の二件または三件の通常fileだけを安全に読む。"""

    root = _absolute_path(input_root)
    requested = (
        ("material", _absolute_path(material), MATERIAL_MAX_BYTES),
        ("review_spec", _absolute_path(review_spec), REVIEW_SPEC_MAX_BYTES),
    )
    if results is not None:
        requested += (("results", _absolute_path(results), RESULTS_MAX_BYTES),)

    root_fd = _open_root(root)
    try:
        contents = {}
        identities = set()
        for name, input_path, max_bytes in requested:
            content, identity = _read_file(root, root_fd, input_path, max_bytes)
            if identity in identities:
                raise ReviewStop("invalid_arguments")
            identities.add(identity)
            contents[name] = content
        return contents
    finally:
        os.close(root_fd)


def _decoded_strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _decoded_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _decoded_strings(item)
    elif isinstance(value, str):
        yield value


def _check_safe_texts(texts):
    pattern_rules = default_pattern_rules()
    for text in texts:
        if any(re.search(rule.pattern, text) for rule in pattern_rules):
            raise ReviewStop("sensitive_data_remaining")
        if find_high_entropy(text):
            raise ReviewStop("sensitive_data_remaining")
        if any(pattern.search(text) for pattern in _ABSOLUTE_PATH_PATTERNS):
            raise ReviewStop("absolute_path_remaining")


def _valid_identifier(value):
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def _validate_review_spec(value):
    root_keys = {
        "schema_version",
        "material_identifier",
        "goal",
        "criteria",
        "constraints",
    }
    if not isinstance(value, dict) or set(value) != root_keys:
        raise ReviewStop("invalid_schema")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ReviewStop("invalid_schema")
    if not _valid_identifier(value["material_identifier"]):
        raise ReviewStop("invalid_schema")
    goal = value["goal"]
    if not isinstance(goal, str) or not 1 <= len(goal) <= 2_000 or "\x00" in goal:
        raise ReviewStop("invalid_schema")

    criteria = value["criteria"]
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= 16:
        raise ReviewStop("invalid_schema")
    normalized_criteria = []
    criterion_ids = set()
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != {"id", "text"}:
            raise ReviewStop("invalid_schema")
        criterion_id = criterion["id"]
        criterion_text = criterion["text"]
        if (
            not _valid_identifier(criterion_id)
            or criterion_id in criterion_ids
            or not isinstance(criterion_text, str)
            or not criterion_text
            or "\x00" in criterion_text
        ):
            raise ReviewStop("invalid_schema")
        criterion_ids.add(criterion_id)
        normalized_criteria.append({"id": criterion_id, "text": criterion_text})

    constraints = value["constraints"]
    if not isinstance(constraints, list) or len(constraints) > 16:
        raise ReviewStop("invalid_schema")
    if any(
        not isinstance(constraint, str) or not constraint or "\x00" in constraint
        for constraint in constraints
    ):
        raise ReviewStop("invalid_schema")

    normalized_criteria.sort(key=lambda item: item["id"])
    return {
        "constraints": list(constraints),
        "criteria": normalized_criteria,
        "goal": goal,
        "material_identifier": value["material_identifier"],
        "schema_version": 1,
    }


def prepare_material(material_bytes, review_spec_bytes):
    """資料と条件から決定的なレビュー材料を作る。"""

    if not isinstance(material_bytes, bytes) or not isinstance(review_spec_bytes, bytes):
        raise ReviewStop("invalid_schema")
    try:
        material_text = material_bytes.decode("utf-8")
        review_spec_text = review_spec_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReviewStop("invalid_utf8") from error
    if not material_text or "\x00" in material_text or "\x00" in review_spec_text:
        raise ReviewStop("invalid_schema")
    try:
        decoded_spec = json.loads(review_spec_text)
    except (json.JSONDecodeError, RecursionError) as error:
        raise ReviewStop("invalid_schema") from error

    _check_safe_texts((material_text, *_decoded_strings(decoded_spec)))
    normalized_spec = _validate_review_spec(decoded_spec)
    review_spec_sha256 = sha256_hex(canonical_json_bytes(normalized_spec))
    result = {
        "external_send_approved": False,
        "material": {
            "content": material_text,
            "content_sha256": sha256_hex(material_bytes),
            "identifier": normalized_spec["material_identifier"],
            "line_count": len(material_text.splitlines()),
        },
        "result_schema": {
            "grouping_basis": "supplied_issue_key",
            "schema_version": 1,
            "semantic_deduplication_performed": False,
        },
        "review_spec": {
            "constraints": normalized_spec["constraints"],
            "criteria": normalized_spec["criteria"],
            "goal": normalized_spec["goal"],
            "sha256": review_spec_sha256,
        },
        "schema_version": 1,
        "status": "material_prepared",
    }
    result["material_package_sha256"] = sha256_hex(canonical_json_bytes(result))
    return result
