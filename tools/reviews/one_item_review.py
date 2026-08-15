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
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


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


def _check_safe_text(text, *, check_entropy=True):
    pattern_rules = default_pattern_rules()
    if any(re.search(rule.pattern, text) for rule in pattern_rules):
        raise ReviewStop("sensitive_data_remaining")
    if check_entropy and find_high_entropy(text):
        raise ReviewStop("sensitive_data_remaining")
    if any(pattern.search(text) for pattern in _ABSOLUTE_PATH_PATTERNS):
        raise ReviewStop("absolute_path_remaining")


def _check_safe_texts(texts):
    for text in texts:
        _check_safe_text(text)


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


def _check_result_strings(value, *, root=False):
    if isinstance(value, dict):
        for key, item in value.items():
            _check_safe_text(key)
            if root and key == "material_package_sha256":
                _check_safe_text(item, check_entropy=False)
            else:
                _check_result_strings(item)
    elif isinstance(value, list):
        for item in value:
            _check_result_strings(item)
    elif isinstance(value, str):
        _check_safe_text(value)


def _required_text(value):
    return isinstance(value, str) and bool(value) and "\x00" not in value


def _normalize_finding(value, criterion_ids, line_count):
    expected_keys = {
        "finding_id",
        "issue_key",
        "severity",
        "title",
        "description",
        "criterion_ids",
        "start_line",
        "end_line",
    }
    if not isinstance(value, dict) or set(value) != expected_keys:
        raise ReviewStop("invalid_schema")
    if not _valid_identifier(value["finding_id"]) or not _valid_identifier(
        value["issue_key"]
    ):
        raise ReviewStop("invalid_schema")
    if value["severity"] not in {"error", "warning", "info"}:
        raise ReviewStop("invalid_schema")
    if not _required_text(value["title"]) or not _required_text(
        value["description"]
    ):
        raise ReviewStop("invalid_schema")
    selected_criteria = value["criterion_ids"]
    if (
        not isinstance(selected_criteria, list)
        or not selected_criteria
        or any(not _valid_identifier(item) for item in selected_criteria)
        or len(set(selected_criteria)) != len(selected_criteria)
        or not set(selected_criteria).issubset(criterion_ids)
    ):
        raise ReviewStop("invalid_schema")
    start_line = value["start_line"]
    end_line = value["end_line"]
    if (
        type(start_line) is not int
        or type(end_line) is not int
        or not 1 <= start_line <= end_line <= line_count
    ):
        raise ReviewStop("invalid_schema")
    return {
        "criterion_ids": sorted(selected_criteria),
        "description": value["description"],
        "end_line": end_line,
        "finding_id": value["finding_id"],
        "issue_key": value["issue_key"],
        "severity": value["severity"],
        "start_line": start_line,
        "title": value["title"],
    }


def _normalize_review(value, criterion_ids, line_count):
    if not isinstance(value, dict) or set(value) != {
        "reviewer_id",
        "verdict",
        "summary",
        "findings",
    }:
        raise ReviewStop("invalid_schema")
    if not _valid_identifier(value["reviewer_id"]):
        raise ReviewStop("invalid_schema")
    verdict = value["verdict"]
    if verdict not in {
        "findings_present",
        "no_findings",
        "insufficient_evidence",
    }:
        raise ReviewStop("invalid_schema")
    if not _required_text(value["summary"]) or not isinstance(
        value["findings"], list
    ):
        raise ReviewStop("invalid_schema")
    findings = [
        _normalize_finding(item, criterion_ids, line_count)
        for item in value["findings"]
    ]
    if (verdict == "findings_present") != bool(findings):
        raise ReviewStop("invalid_schema")
    finding_ids = [item["finding_id"] for item in findings]
    issue_keys = [item["issue_key"] for item in findings]
    if len(set(finding_ids)) != len(finding_ids) or len(set(issue_keys)) != len(
        issue_keys
    ):
        raise ReviewStop("invalid_schema")
    findings.sort(key=lambda item: (item["issue_key"], item["finding_id"]))
    return {
        "findings": findings,
        "reviewer_id": value["reviewer_id"],
        "summary": value["summary"],
        "verdict": verdict,
    }


def validate_results(material_package, results_bytes):
    """結果集合を厳格検査し、決定的な順へ正規化する。"""

    if not isinstance(material_package, dict) or not isinstance(results_bytes, bytes):
        raise ReviewStop("invalid_schema")
    try:
        decoded = json.loads(results_bytes.decode("utf-8"))
    except UnicodeDecodeError as error:
        raise ReviewStop("invalid_utf8") from error
    except (json.JSONDecodeError, RecursionError) as error:
        raise ReviewStop("invalid_schema") from error
    if not isinstance(decoded, dict):
        raise ReviewStop("invalid_schema")
    supplied_sha256 = decoded.get("material_package_sha256")
    if not isinstance(supplied_sha256, str) or not _SHA256.fullmatch(
        supplied_sha256
    ):
        raise ReviewStop("invalid_schema")
    if supplied_sha256 != material_package.get("material_package_sha256"):
        raise ReviewStop("stale_material")

    _check_result_strings(decoded, root=True)
    if set(decoded) != {"schema_version", "material_package_sha256", "reviews"}:
        raise ReviewStop("invalid_schema")
    if type(decoded["schema_version"]) is not int or decoded["schema_version"] != 1:
        raise ReviewStop("invalid_schema")
    reviews = decoded["reviews"]
    if not isinstance(reviews, list) or not 1 <= len(reviews) <= 8:
        raise ReviewStop("invalid_schema")
    try:
        criterion_ids = {
            item["id"] for item in material_package["review_spec"]["criteria"]
        }
        line_count = material_package["material"]["line_count"]
    except (KeyError, TypeError) as error:
        raise ReviewStop("invalid_schema") from error
    normalized_reviews = [
        _normalize_review(item, criterion_ids, line_count) for item in reviews
    ]
    reviewer_ids = [item["reviewer_id"] for item in normalized_reviews]
    if len(set(reviewer_ids)) != len(reviewer_ids):
        raise ReviewStop("invalid_schema")
    if sum(len(item["findings"]) for item in normalized_reviews) > 100:
        raise ReviewStop("invalid_schema")
    normalized_reviews.sort(key=lambda item: item["reviewer_id"])
    normalized_root = {
        "material_package_sha256": supplied_sha256,
        "reviews": normalized_reviews,
        "schema_version": 1,
    }
    validated_reviews = []
    for normalized in normalized_reviews:
        content = {
            key: value for key, value in normalized.items() if key != "reviewer_id"
        }
        validated_reviews.append({
            "review": normalized,
            "review_content_sha256": sha256_hex(canonical_json_bytes(content)),
            "review_sha256": sha256_hex(canonical_json_bytes(normalized)),
        })
    return {
        "material_package_sha256": supplied_sha256,
        "result_set_sha256": sha256_hex(canonical_json_bytes(normalized_root)),
        "reviews": validated_reviews,
    }
