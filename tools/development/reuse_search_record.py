"""Work 4B最小試行：実装前の既存routine検索とnew-only記録（reuse_search_record）。

承認：DEC-WORK4B-MINIMAL-PILOT-SCOPE-001
（docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md §2〜§4）

検索はWork 4AのRoutine ProfileとComparison Discoveryを固定sourceとし、
宣言（subject、target_paths、target_symbols）から決定的に導出する。
recordは処置labelを持たず、Human判断を先取りしない。
"""

import hashlib
import json
from pathlib import Path


class ReuseSearchError(Exception):
    """検索recordの生成・検証・保存・gate判定の失敗。"""


_RECORD_FIELDS_V1 = (
    "record_kind", "schema_version", "subject", "declaration",
    "source_identity", "query", "hits", "groups", "content_digest",
)
_RECORD_FIELDS_V2 = _RECORD_FIELDS_V1 + ("freshness",)
_FRESHNESS_FIELDS = (
    "assessed", "observation_snapshot_id", "target_paths",
    "files_at_observation", "changed_files", "new_files", "missing_files", "stale",
)
_DECLARATION_FIELDS = ("subject", "target_paths", "target_symbols")
_IDENTITY_FIELDS = (
    "profile_run_id", "discovery_run_id", "source_content_id",
    "profile_schema_version", "extraction_rule_version",
    "discovery_schema_version", "grouping_rule_version",
)
_HIT_FIELDS = (
    "symbol_id", "code_reference", "match_reasons", "group_id", "basis_kind",
)
_GROUP_FIELDS = ("group_id", "basis_kind", "member_symbol_ids")
_EXPECTED_IDENTITY_FIELDS = (
    "profile_run_id", "discovery_run_id", "source_content_id",
)
_QUERY_RULES = (
    "target_path_scope",
    "target_symbol_name_match",
    "direct_neighbor",
    "group_membership_full_members",
)


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _range_matches(relative, target_paths):
    return any(
        relative == prefix or relative.startswith(prefix) for prefix in target_paths
    )


def _current_range_files(project_root, target_paths):
    """対象範囲に現存する.py fileをproject root相対で決定的に列挙する。"""

    root = Path(project_root)
    found = set()
    for prefix in target_paths:
        candidate = root / prefix
        if candidate.is_file():
            found.add(Path(prefix).as_posix())
        elif candidate.is_dir():
            for item in candidate.rglob("*.py"):
                found.add(item.relative_to(root).as_posix())
    return sorted(found)


def _assess_freshness(*, observation_document, target_paths, project_root):
    """観測時点のfile digestと現状を突き合わせ、乖離を機械計測する。"""

    files_at_observation = sorted(
        (
            {"path": item["path"], "sha256": item["file_sha256"]}
            for item in observation_document.get("files", [])
            if _range_matches(item["path"], target_paths)
        ),
        key=lambda item: item["path"],
    )
    observed_paths = {item["path"] for item in files_at_observation}
    changed = []
    missing = []
    root = Path(project_root)
    for item in files_at_observation:
        target = root / item["path"]
        if not target.is_file():
            missing.append(item["path"])
        elif file_sha256(target) != item["sha256"]:
            changed.append(item["path"])
    new_files = [
        relative
        for relative in _current_range_files(project_root, target_paths)
        if relative not in observed_paths
    ]
    return {
        "assessed": True,
        "observation_snapshot_id": observation_document.get("snapshot_id"),
        "target_paths": list(target_paths),
        "files_at_observation": files_at_observation,
        "changed_files": changed,
        "new_files": new_files,
        "missing_files": missing,
        "stale": bool(changed or new_files or missing),
    }


def _content_digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return hashlib.sha256(
        json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    ).hexdigest()


def _profile_run_id(profile_document):
    value = profile_document.get("profile_run_id", profile_document.get("run_id"))
    if not isinstance(value, str) or not value:
        raise ReuseSearchError("profile run id is missing")
    return value


def _discovery_run_id(discovery_document):
    value = discovery_document.get("discovery_run_id", discovery_document.get("run_id"))
    if not isinstance(value, str) or not value:
        raise ReuseSearchError("discovery run id is missing")
    return value


def search_existing_routines(
    *,
    profile_document,
    discovery_document,
    declaration,
    observation_document=None,
    project_root=".",
):
    """宣言された対象範囲から既存routineを決定的に検索し、recordを返す。

    observation_documentを渡すとschema 2となり、観測時点のfile digestとの乖離を
    機械計測したfreshness欄を持つ。渡さない場合はschema 1（既存recordと同形式）。
    """

    for field in _DECLARATION_FIELDS:
        if field not in declaration:
            raise ReuseSearchError(f"declaration field is missing: {field}")
    source_content_id = profile_document.get("source_content_id")
    if discovery_document.get("source_content_id") != source_content_id:
        raise ReuseSearchError("profile and discovery source content ids differ")

    routines = profile_document.get("routines", [])
    by_id = {item["symbol_id"]: item for item in routines}
    target_paths = tuple(declaration["target_paths"])
    target_symbols = tuple(declaration["target_symbols"])

    matched = {}
    for routine in routines:
        reasons = []
        relative = routine["code_reference"]["relative_path"]
        if any(relative == prefix or relative.startswith(prefix) for prefix in target_paths):
            reasons.append("target_path_scope")
        symbol_name = routine["symbol_id"].rsplit(":", 1)[-1]
        if any(token and token in symbol_name for token in target_symbols):
            reasons.append("target_symbol_name_match")
        if reasons:
            matched[routine["symbol_id"]] = reasons

    neighbor_ids = {}
    for symbol_id in tuple(matched):
        routine = by_id[symbol_id]
        for neighbor in tuple(routine.get("direct_callee_symbol_ids", ())) + tuple(
            routine.get("direct_caller_symbol_ids", ())
        ):
            if neighbor in by_id and neighbor not in matched:
                neighbor_ids.setdefault(neighbor, ["direct_neighbor"])
    matched.update(neighbor_ids)

    groups_by_member = {}
    for group in discovery_document.get("groups", []):
        for member in group.get("member_symbol_ids", []):
            groups_by_member.setdefault(member, []).append(group)

    hits = []
    referenced_groups = {}
    for symbol_id in sorted(matched):
        routine = by_id[symbol_id]
        base = {
            "symbol_id": symbol_id,
            "code_reference": dict(routine["code_reference"]),
            "match_reasons": sorted(matched[symbol_id]),
        }
        member_groups = sorted(
            groups_by_member.get(symbol_id, []), key=lambda item: item["group_id"]
        )
        if member_groups:
            for group in member_groups:
                referenced_groups[group["group_id"]] = group
                hits.append(
                    dict(
                        base,
                        group_id=group["group_id"],
                        basis_kind=group.get("basis_kind"),
                    )
                )
        else:
            hits.append(dict(base, group_id=None, basis_kind=None))
    hits.sort(key=lambda hit: (hit["symbol_id"], hit["group_id"] or ""))
    groups_section = [
        {
            "group_id": group["group_id"],
            "basis_kind": group.get("basis_kind"),
            "member_symbol_ids": list(group["member_symbol_ids"]),
        }
        for group in sorted(referenced_groups.values(), key=lambda item: item["group_id"])
    ]

    record = {
        "record_kind": "reuse_search_record",
        "schema_version": 1 if observation_document is None else 2,
        "subject": declaration["subject"],
        "declaration": {
            "subject": declaration["subject"],
            "target_paths": list(target_paths),
            "target_symbols": list(target_symbols),
        },
        "source_identity": {
            "profile_run_id": _profile_run_id(profile_document),
            "discovery_run_id": _discovery_run_id(discovery_document),
            "source_content_id": source_content_id,
            "profile_schema_version": profile_document.get("schema_version"),
            "extraction_rule_version": profile_document.get("extraction_rule_version"),
            "discovery_schema_version": discovery_document.get("schema_version"),
            "grouping_rule_version": discovery_document.get("grouping_rule_version"),
        },
        "query": {"rules_applied": list(_QUERY_RULES)},
        "hits": hits,
        "groups": groups_section,
    }
    if observation_document is not None:
        record["freshness"] = _assess_freshness(
            observation_document=observation_document,
            target_paths=target_paths,
            project_root=project_root,
        )
    record["content_digest"] = _content_digest(record)
    return record


def _require_exact_fields(document, fields, label):
    if not isinstance(document, dict):
        raise ReuseSearchError(f"{label} is not a mapping")
    unknown = sorted(set(document) - set(fields))
    if unknown:
        raise ReuseSearchError(f"{label} has unknown fields: {','.join(unknown)}")
    missing = sorted(set(fields) - set(document))
    if missing:
        raise ReuseSearchError(f"{label} misses fields: {','.join(missing)}")


def validate_reuse_search_record(record, *, expected_identity):
    """結線・new-only形式・label禁止・digestをfail-closedで検証する。"""

    if not isinstance(record, dict):
        raise ReuseSearchError("reuse search record is not a mapping")
    if record.get("record_kind") != "reuse_search_record":
        raise ReuseSearchError("record kind is invalid")
    schema_version = record.get("schema_version")
    if schema_version == 1:
        _require_exact_fields(record, _RECORD_FIELDS_V1, "reuse search record")
    elif schema_version == 2:
        _require_exact_fields(record, _RECORD_FIELDS_V2, "reuse search record")
        _require_exact_fields(record["freshness"], _FRESHNESS_FIELDS, "freshness")
    else:
        raise ReuseSearchError("schema version is invalid")
    _require_exact_fields(record["declaration"], _DECLARATION_FIELDS, "declaration")
    if record["subject"] != record["declaration"]["subject"]:
        raise ReuseSearchError("subject differs from declaration")

    _require_exact_fields(record["source_identity"], _IDENTITY_FIELDS, "source identity")
    _require_exact_fields(
        dict(expected_identity), _EXPECTED_IDENTITY_FIELDS, "expected identity"
    )
    for field in _EXPECTED_IDENTITY_FIELDS:
        if record["source_identity"][field] != expected_identity[field]:
            raise ReuseSearchError(f"source identity is stale: {field}")

    if not isinstance(record["hits"], list):
        raise ReuseSearchError("hits is not a list")
    group_ids = set()
    for group in record["groups"]:
        _require_exact_fields(group, _GROUP_FIELDS, "group reference")
        group_ids.add(group["group_id"])
    for hit in record["hits"]:
        _require_exact_fields(hit, _HIT_FIELDS, "hit")
        if hit["group_id"] is not None and hit["group_id"] not in group_ids:
            raise ReuseSearchError("hit references a group missing from groups")

    if record["content_digest"] != _content_digest(record):
        raise ReuseSearchError("content digest mismatch")
    return True


def write_reuse_search_record(*, path, record):
    """new-onlyで保存する。既存fileの上書きを拒否する。"""

    target = Path(path)
    if target.exists():
        raise ReuseSearchError("reuse search record already exists")
    target.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def gate_check(*, record_path, expected_identity, project_root="."):
    """実装開始のgate判定。record不存在・結線不一致・鮮度乖離はfail-closedで開始不可。"""

    target = Path(record_path)
    if not target.is_file():
        return {
            "start_allowed": False,
            "reason": "reuse_search_record_missing",
        }
    try:
        record = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {
            "start_allowed": False,
            "reason": "reuse_search_record_unreadable",
        }
    try:
        validate_reuse_search_record(record, expected_identity=expected_identity)
    except ReuseSearchError as error:
        return {
            "start_allowed": False,
            "reason": f"reuse_search_record_invalid: {error}",
        }
    if record["schema_version"] == 1:
        return {
            "start_allowed": True,
            "reason": "reuse_search_record_verified",
            "freshness": "not_assessed",
        }

    freshness = record["freshness"]
    observed = {
        item["path"]: item["sha256"] for item in freshness["files_at_observation"]
    }
    stale_files = []
    root = Path(project_root)
    for relative, recorded_sha in sorted(observed.items()):
        current = root / relative
        if not current.is_file() or file_sha256(current) != recorded_sha:
            stale_files.append(relative)
    for relative in _current_range_files(project_root, freshness["target_paths"]):
        if relative not in observed:
            stale_files.append(relative)
    if stale_files:
        return {
            "start_allowed": False,
            "reason": "profile_stale",
            "stale_files": sorted(stale_files),
        }
    return {
        "start_allowed": True,
        "reason": "reuse_search_record_verified",
        "freshness": "assessed_fresh",
    }
