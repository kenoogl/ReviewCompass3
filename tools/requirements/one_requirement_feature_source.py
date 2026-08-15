"""構造化済み要求候補一件の整合を決定的に検査する。"""

import hashlib
import json
import re

from tools.session_logs.redaction import default_pattern_rules
from tools.session_logs.redaction import find_high_entropy


_GENERAL_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_FEATURE_IDENTIFIER = re.compile(r"FEAT-[A-Z0-9]+(?:-[A-Z0-9]+)*\Z")
_REQUIREMENT_IDENTIFIER = re.compile(
    r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}\Z"
)
_SHA256_VALUE = re.compile(r"[0-9a-f]{64}\Z")
_DECLARED_STATUSES = frozenset(
    ("effective", "approved_context", "candidate", "historical")
)
_DISPOSITIONS = frozenset(("selected", "not_selected"))
_SEVEN_LISTS = (
    "inputs",
    "outputs",
    "stop_conditions",
    "recovery_conditions",
    "preserved_artifacts",
    "acceptance_criteria",
    "non_goals",
)
_LIMITATIONS = (
    "source_status_not_verified",
    "semantic_correctness_not_verified",
    "multi_requirement_partition_not_verified",
    "authority_not_changed",
    "sensitive_detection_not_exhaustive",
)


class RequirementCandidateStop(Exception):
    """入力を安全に検査できないため処理を停止する。"""

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
        raise RequirementCandidateStop("invalid_schema", source)
    decode_failed = False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        decode_failed = True
    if decode_failed:
        raise RequirementCandidateStop("invalid_utf8", source)
    schema_failed = False
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError, RecursionError):
        schema_failed = True
    if schema_failed:
        raise RequirementCandidateStop("invalid_schema", source)
    return value


def _is_excluded_catalog_digest(path, text):
    return (
        len(path) == 3
        and path[0] == "sources"
        and isinstance(path[1], int)
        and path[2] == "sha256"
        and _SHA256_VALUE.fullmatch(text) is not None
    )


def _iter_input_strings(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key, None
            yield from _iter_input_strings(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_input_strings(item, path + (index,))
    elif isinstance(value, str):
        yield value, path


def _scan_sensitive(value, source, *, allow_catalog_digest):
    rules = default_pattern_rules()
    for text, path in _iter_input_strings(value):
        if (
            allow_catalog_digest
            and path is not None
            and _is_excluded_catalog_digest(path, text)
        ):
            continue
        if any(re.search(rule.pattern, text) for rule in rules):
            raise RequirementCandidateStop("sensitive_data_remaining", source)
        if find_high_entropy(text):
            raise RequirementCandidateStop("sensitive_data_remaining", source)


def _has_only_unicode_scalar_values(value):
    return not any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _is_general_identifier(value):
    return (
        isinstance(value, str)
        and _GENERAL_IDENTIFIER.fullmatch(value) is not None
    )


def _is_free_text(value, maximum_length=2000):
    return (
        isinstance(value, str)
        and 1 <= len(value) <= maximum_length
        and "\x00" not in value
        and _has_only_unicode_scalar_values(value)
    )


def _validate_free_text_list(value, source):
    if not isinstance(value, list) or not 1 <= len(value) <= 32:
        raise RequirementCandidateStop("invalid_schema", source)
    for item in value:
        if not _is_free_text(item, maximum_length=500):
            raise RequirementCandidateStop("invalid_schema", source)
    if len(set(value)) != len(value):
        raise RequirementCandidateStop("invalid_schema", source)
    return list(value)


def _require_schema_version(value, source):
    if type(value) is not int or value != 1:
        raise RequirementCandidateStop("invalid_schema", source)


def _validate_catalog(value):
    source = "catalog"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "catalog_identifier",
        "sources",
    }:
        raise RequirementCandidateStop("invalid_schema", source)
    _require_schema_version(value["schema_version"], source)
    if not _is_general_identifier(value["catalog_identifier"]):
        raise RequirementCandidateStop("invalid_schema", source)
    sources = value["sources"]
    if not isinstance(sources, list) or not 1 <= len(sources) <= 256:
        raise RequirementCandidateStop("invalid_schema", source)

    normalized_sources = []
    source_ids = set()
    for item in sources:
        if not isinstance(item, dict) or set(item) != {
            "source_id",
            "sha256",
            "declared_status",
        }:
            raise RequirementCandidateStop("invalid_schema", source)
        source_id = item["source_id"]
        digest = item["sha256"]
        declared_status = item["declared_status"]
        if (
            not _is_general_identifier(source_id)
            or not isinstance(digest, str)
            or _SHA256_VALUE.fullmatch(digest) is None
            or declared_status not in _DECLARED_STATUSES
            or source_id in source_ids
        ):
            raise RequirementCandidateStop("invalid_schema", source)
        source_ids.add(source_id)
        normalized_sources.append(
            {
                "source_id": source_id,
                "sha256": digest,
                "declared_status": declared_status,
            }
        )

    normalized_sources.sort(key=lambda item: item["source_id"])
    return {
        "schema_version": 1,
        "catalog_identifier": value["catalog_identifier"],
        "sources": normalized_sources,
    }


def _validate_feature(value, source):
    if not isinstance(value, dict) or set(value) != {
        "feature_id",
        "name",
        "responsibility",
        "non_goals",
    }:
        raise RequirementCandidateStop("invalid_schema", source)
    feature_id = value["feature_id"]
    if (
        not isinstance(feature_id, str)
        or _FEATURE_IDENTIFIER.fullmatch(feature_id) is None
        or not _is_free_text(value["name"])
        or not _is_free_text(value["responsibility"])
    ):
        raise RequirementCandidateStop("invalid_schema", source)
    return {
        "feature_id": feature_id,
        "name": value["name"],
        "responsibility": value["responsibility"],
        "non_goals": _validate_free_text_list(value["non_goals"], source),
    }


def _validate_requirement(value, source):
    expected_members = {
        "requirement_id",
        "feature_id",
        "statement",
    } | set(_SEVEN_LISTS)
    if not isinstance(value, dict) or set(value) != expected_members:
        raise RequirementCandidateStop("invalid_schema", source)
    requirement_id = value["requirement_id"]
    feature_id = value["feature_id"]
    if (
        not isinstance(requirement_id, str)
        or _REQUIREMENT_IDENTIFIER.fullmatch(requirement_id) is None
        or not isinstance(feature_id, str)
        or _FEATURE_IDENTIFIER.fullmatch(feature_id) is None
        or not _is_free_text(value["statement"])
    ):
        raise RequirementCandidateStop("invalid_schema", source)
    normalized = {
        "requirement_id": requirement_id,
        "feature_id": feature_id,
        "statement": value["statement"],
    }
    for field in _SEVEN_LISTS:
        normalized[field] = _validate_free_text_list(value[field], source)
    return normalized


def _validate_dispositions(value, source):
    if not isinstance(value, list) or not 1 <= len(value) <= 256:
        raise RequirementCandidateStop("invalid_schema", source)
    normalized = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {
            "source_id",
            "disposition",
            "rationale",
        }:
            raise RequirementCandidateStop("invalid_schema", source)
        if (
            not _is_general_identifier(item["source_id"])
            or item["disposition"] not in _DISPOSITIONS
            or not _is_free_text(item["rationale"])
        ):
            raise RequirementCandidateStop("invalid_schema", source)
        normalized.append(
            {
                "source_id": item["source_id"],
                "disposition": item["disposition"],
                "rationale": item["rationale"],
            }
        )
    return normalized


def _validate_obligation_sources(value, source):
    if not isinstance(value, list) or not 1 <= len(value) <= 256:
        raise RequirementCandidateStop("invalid_schema", source)
    normalized = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {
            "obligation_id",
            "source_ids",
        }:
            raise RequirementCandidateStop("invalid_schema", source)
        obligation_id = item["obligation_id"]
        source_ids = item["source_ids"]
        if (
            not isinstance(obligation_id, str)
            or not 1 <= len(obligation_id) <= 256
            or "\x00" in obligation_id
            or not _has_only_unicode_scalar_values(obligation_id)
        ):
            raise RequirementCandidateStop("invalid_schema", source)
        if not isinstance(source_ids, list) or not 1 <= len(source_ids) <= 256:
            raise RequirementCandidateStop("invalid_schema", source)
        if any(
            not _is_general_identifier(source_id) for source_id in source_ids
        ):
            raise RequirementCandidateStop("invalid_schema", source)
        if len(set(source_ids)) != len(source_ids):
            raise RequirementCandidateStop("invalid_schema", source)
        normalized.append(
            {
                "obligation_id": obligation_id,
                "source_ids": sorted(source_ids),
            }
        )
    return normalized


def _validate_candidate(value):
    source = "candidate"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "candidate_identifier",
        "feature",
        "requirement",
        "source_dispositions",
        "obligation_sources",
    }:
        raise RequirementCandidateStop("invalid_schema", source)
    _require_schema_version(value["schema_version"], source)
    if not _is_general_identifier(value["candidate_identifier"]):
        raise RequirementCandidateStop("invalid_schema", source)
    return {
        "schema_version": 1,
        "candidate_identifier": value["candidate_identifier"],
        "feature": _validate_feature(value["feature"], source),
        "requirement": _validate_requirement(value["requirement"], source),
        "source_dispositions": _validate_dispositions(
            value["source_dispositions"],
            source,
        ),
        "obligation_sources": _validate_obligation_sources(
            value["obligation_sources"],
            source,
        ),
    }


def _expected_obligation_ids(requirement):
    identifiers = [f"{requirement['requirement_id']}#statement"]
    for field in _SEVEN_LISTS:
        for index in range(1, len(requirement[field]) + 1):
            identifiers.append(
                f"{requirement['requirement_id']}#{field}.{index:03d}"
            )
    return identifiers


def _check_references(catalog, candidate):
    source = "candidate"
    if (
        candidate["requirement"]["feature_id"]
        != candidate["feature"]["feature_id"]
    ):
        raise RequirementCandidateStop("unresolved_reference", source)
    catalog_ids = {item["source_id"] for item in catalog["sources"]}
    for item in candidate["source_dispositions"]:
        if item["source_id"] not in catalog_ids:
            raise RequirementCandidateStop("unresolved_reference", source)
    expected_ids = set(_expected_obligation_ids(candidate["requirement"]))
    selected_ids = {
        item["source_id"]
        for item in candidate["source_dispositions"]
        if item["disposition"] == "selected"
    }
    for item in candidate["obligation_sources"]:
        if item["obligation_id"] not in expected_ids:
            raise RequirementCandidateStop("unresolved_reference", source)
        for source_id in item["source_ids"]:
            if source_id not in catalog_ids or source_id not in selected_ids:
                raise RequirementCandidateStop("unresolved_reference", source)


def _check_coverage(catalog, candidate):
    source = "candidate"
    catalog_ids = [item["source_id"] for item in catalog["sources"]]
    disposition_ids = [
        item["source_id"] for item in candidate["source_dispositions"]
    ]
    if len(disposition_ids) != len(set(disposition_ids)) or set(
        disposition_ids
    ) != set(catalog_ids):
        raise RequirementCandidateStop("incomplete_coverage", source)
    expected_ids = _expected_obligation_ids(candidate["requirement"])
    obligation_ids = [
        item["obligation_id"] for item in candidate["obligation_sources"]
    ]
    if len(obligation_ids) != len(set(obligation_ids)) or set(
        obligation_ids
    ) != set(expected_ids):
        raise RequirementCandidateStop("incomplete_coverage", source)
    referenced = set()
    for item in candidate["obligation_sources"]:
        referenced.update(item["source_ids"])
    selected_ids = {
        item["source_id"]
        for item in candidate["source_dispositions"]
        if item["disposition"] == "selected"
    }
    if not selected_ids <= referenced:
        raise RequirementCandidateStop("incomplete_coverage", source)


def _build_result(catalog, candidate):
    dispositions = sorted(
        candidate["source_dispositions"],
        key=lambda item: item["source_id"],
    )
    obligations = sorted(
        candidate["obligation_sources"],
        key=lambda item: item["obligation_id"],
    )
    normalized_candidate = {
        "schema_version": 1,
        "candidate_identifier": candidate["candidate_identifier"],
        "feature": candidate["feature"],
        "requirement": candidate["requirement"],
        "source_dispositions": dispositions,
        "obligation_sources": obligations,
    }
    trace = {
        "schema_version": 1,
        "source_dispositions": dispositions,
        "obligation_sources": obligations,
    }
    status_by_source = {
        item["source_id"]: item["declared_status"]
        for item in catalog["sources"]
    }
    counts = {
        "approved_context_sources": 0,
        "candidate_sources": 0,
        "effective_sources": 0,
        "historical_sources": 0,
        "not_selected_sources": 0,
        "selected_sources": 0,
        "traced_obligations": len(obligations),
    }
    for item in catalog["sources"]:
        counts[f"{item['declared_status']}_sources"] += 1
    for item in dispositions:
        counts[f"{item['disposition']}_sources"] += 1

    selected_candidates = sorted(
        item["source_id"]
        for item in dispositions
        if item["disposition"] == "selected"
        and status_by_source[item["source_id"]] == "candidate"
    )
    selected_historicals = sorted(
        item["source_id"]
        for item in dispositions
        if item["disposition"] == "selected"
        and status_by_source[item["source_id"]] == "historical"
    )
    queue = [
        {
            "identifiers": [candidate["candidate_identifier"]],
            "kind": "requirement_candidate",
        },
    ]
    if selected_candidates:
        queue.append(
            {
                "identifiers": selected_candidates,
                "kind": "candidate_source_selection",
            }
        )
    if selected_historicals:
        queue.append(
            {
                "identifiers": selected_historicals,
                "kind": "historical_source_selection",
            }
        )

    result = {
        "status": "requirement_candidate_checked",
        "schema_version": 1,
        "decision_status": "pending_human_decision",
        "promotion_status": "not_promoted",
        "verdict": (
            "review_required_pending_human_decision"
            if selected_candidates or selected_historicals
            else "trace_complete_pending_human_decision"
        ),
        "catalog": {
            "identifier": catalog["catalog_identifier"],
            "sha256": _sha256(catalog),
            "source_count": len(catalog["sources"]),
        },
        "candidate": {
            "identifier": candidate["candidate_identifier"],
            "sha256": _sha256(normalized_candidate),
        },
        "feature": {
            "identifier": candidate["feature"]["feature_id"],
            "sha256": _sha256(candidate["feature"]),
        },
        "requirement": {
            "identifier": candidate["requirement"]["requirement_id"],
            "sha256": _sha256(candidate["requirement"]),
            "obligation_count": len(obligations),
        },
        "counts": counts,
        "source_dispositions": [
            {
                "source_id": item["source_id"],
                "declared_status": status_by_source[item["source_id"]],
                "disposition": item["disposition"],
            }
            for item in dispositions
        ],
        "obligation_sources": obligations,
        "trace_sha256": _sha256(trace),
        "human_decision_queue": queue,
        "limitations": list(_LIMITATIONS),
        "external_send_approved": False,
    }
    result["result_sha256"] = _sha256(result)
    return result


def check_inputs(catalog_bytes, candidate_bytes):
    """検査・正規化した出典一覧と要求候補の整合を検査する。"""

    catalog_value = _decode_input(catalog_bytes, "catalog")
    candidate_value = _decode_input(candidate_bytes, "candidate")
    _scan_sensitive(catalog_value, "catalog", allow_catalog_digest=True)
    _scan_sensitive(candidate_value, "candidate", allow_catalog_digest=False)
    catalog = _validate_catalog(catalog_value)
    candidate = _validate_candidate(candidate_value)
    _check_references(catalog, candidate)
    _check_coverage(catalog, candidate)
    return _build_result(catalog, candidate)
