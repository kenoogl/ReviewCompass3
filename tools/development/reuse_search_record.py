"""Work 4B最小試行：実装前の既存routine検索とnew-only記録（reuse_search_record）。

承認：DEC-WORK4B-MINIMAL-PILOT-SCOPE-001
（docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md §2〜§4）

検索はWork 4AのRoutine ProfileとComparison Discoveryを固定sourceとし、
宣言（subject、target_paths、target_symbols）から決定的に導出する。
recordは処置labelを持たず、Human判断を先取りしない。
"""

import ast
import hashlib
import json
import re
from pathlib import Path


class ReuseSearchError(Exception):
    """検索recordの生成・検証・保存・gate判定の失敗。"""


_RECORD_FIELDS_V1 = (
    "record_kind", "schema_version", "subject", "declaration",
    "source_identity", "query", "hits", "groups", "content_digest",
)
_RECORD_FIELDS_V2 = _RECORD_FIELDS_V1 + ("freshness",)
_RECORD_FIELDS_V3 = (
    "record_kind", "schema_version", "subject", "declaration",
    "source_identity", "query", "hits", "groups", "capability_results",
    "uncovered_capability_ids", "human_adjudication_required", "freshness",
    "content_digest",
)
_RECORD_FIELDS_V4 = (
    "record_kind", "schema_version", "subject", "declaration",
    "source_identity", "query", "capability_results",
    "no_search_material_capability_ids", "human_adjudication_required",
    "freshness", "content_digest",
)
_FRESHNESS_FIELDS = (
    "assessed", "observation_snapshot_id", "target_paths",
    "files_at_observation", "changed_files", "new_files", "missing_files", "stale",
)
_DECLARATION_FIELDS = ("subject", "target_paths", "target_symbols")
_CAPABILITY_DECLARATION_FIELDS = ("subject", "source_scope_paths", "capabilities")
_CAPABILITY_FIELDS = (
    "capability_id", "responsibility", "inputs", "outputs", "failure_behavior",
    "required_properties", "reference_paths", "reference_symbols", "symbol_terms",
    "required_effect_markers", "forbidden_effect_markers",
)
_CAPABILITY_RESULT_FIELDS = (
    "capability_id", "coverage_status", "anchor_symbol_ids",
    "missing_reference_paths", "missing_reference_symbols", "candidates",
)
_CAPABILITY_CANDIDATE_FIELDS = (
    "symbol_id", "code_reference", "match_reasons", "related_group_ids",
    "conflicting_effect_markers", "declared_lifecycle",
)
_GROUPED_CAPABILITY_RESULT_FIELDS = (
    "capability_id", "search_status", "direct_matches", "hint_matches",
    "comparison_groups", "missing_reference_paths", "missing_reference_symbols",
)
_GROUPED_MATCH_FIELDS = (
    "symbol_id", "code_reference", "match_reasons",
    "conflicting_effect_markers", "declared_lifecycle",
)
_COMPARISON_GROUP_SUMMARY_FIELDS = (
    "group_id", "basis_kind", "basis_evidence", "basis_limitation",
    "member_count", "presentation_class", "representative_symbol_ids",
    "member_record_reference", "matched_symbol_ids",
)
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
_CAPABILITY_QUERY_RULES = (
    "work_specific_capability_declaration",
    "reference_path_and_exact_symbol_anchor",
    "symbol_term_hint",
    "required_effect_marker_match",
    "direct_neighbor",
    "focused_structural_or_neighborhood_group_members",
    "forbidden_effect_marker_annotation",
    "declared_source_lifecycle_observation",
)
_GROUPED_CAPABILITY_QUERY_RULES = (
    "work_specific_capability_declaration",
    "exact_reference_symbol_and_direct_neighbor",
    "reference_path_symbol_term_and_required_effect_as_hints",
    "existing_work4a_comparison_group_summary",
    "comparison_group_members_not_flattened",
    "forbidden_effect_marker_annotation",
    "declared_source_lifecycle_observation",
)
_CAPABILITY_EXPANSION_BASIS_KINDS = {
    "structural_exact_match",
    "call_neighborhood",
}
_EFFECT_MARKERS = {
    "file_read", "file_write", "process_spawn", "network", "environment",
    "global_mutation",
}
_DECLARED_LIFECYCLES = {"stable", "provisional", "stopped"}


from tools.common.digests import file_sha256 as file_sha256
from tools.development import work4a_rebuild_v3 as work4a


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


from tools.common.digests import canonical_content_digest as _content_digest


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


def _require_string_list(value, field, *, allow_empty=True):
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(value))
    ):
        raise ReuseSearchError(f"capability field is invalid: {field}")


def _validate_capability(capability):
    _require_exact_fields(capability, _CAPABILITY_FIELDS, "capability")
    for field in ("capability_id", "responsibility"):
        if not isinstance(capability[field], str) or not capability[field]:
            raise ReuseSearchError(f"capability field is invalid: {field}")
    for field in (
        "inputs", "outputs", "failure_behavior", "required_properties",
        "reference_paths", "reference_symbols", "symbol_terms",
        "required_effect_markers", "forbidden_effect_markers",
    ):
        _require_string_list(
            capability[field],
            field,
            allow_empty=field not in (
                "inputs", "outputs", "failure_behavior", "required_properties"
            ),
        )
    if not any(
        capability[field]
        for field in (
            "reference_paths", "reference_symbols", "symbol_terms",
            "required_effect_markers",
        )
    ):
        raise ReuseSearchError("capability has no machine search input")
    marker_fields = set(capability["required_effect_markers"]) | set(
        capability["forbidden_effect_markers"]
    )
    if marker_fields - _EFFECT_MARKERS:
        raise ReuseSearchError("capability effect marker is invalid")
    if set(capability["required_effect_markers"]) & set(
        capability["forbidden_effect_markers"]
    ):
        raise ReuseSearchError("required and forbidden effect markers overlap")
    for relative in capability["reference_paths"]:
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ReuseSearchError("capability reference path is invalid")


def _source_lifecycle(project_root, relative_path, cache):
    if relative_path in cache:
        return cache[relative_path]
    try:
        source = (Path(project_root) / relative_path).read_text(encoding="utf-8")
        document = ast.parse(source)
        docstring = ast.get_docstring(document) or ""
    except (OSError, UnicodeDecodeError, SyntaxError):
        cache[relative_path] = "undeclared"
        return cache[relative_path]
    match = re.search(r"(?m)^lifecycle:\s*([a-z_-]+)\s*$", docstring)
    value = match.group(1) if match else "undeclared"
    cache[relative_path] = value if value in _DECLARED_LIFECYCLES else "undeclared"
    return cache[relative_path]


def search_required_capabilities(
    *,
    profile_document,
    discovery_document,
    declaration,
    observation_document,
    project_root=".",
):
    """作業ごとの必要な働きから、現在の全コードにある候補を導く。"""

    _require_exact_fields(
        declaration, _CAPABILITY_DECLARATION_FIELDS, "capability declaration"
    )
    subject = declaration["subject"]
    if not isinstance(subject, str) or not subject:
        raise ReuseSearchError("capability subject is invalid")
    source_scope_paths = declaration["source_scope_paths"]
    _require_string_list(source_scope_paths, "source_scope_paths", allow_empty=False)
    for relative in source_scope_paths:
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ReuseSearchError("source scope path is invalid")
    capabilities = declaration["capabilities"]
    if not isinstance(capabilities, list) or not capabilities:
        raise ReuseSearchError("capabilities are missing")
    identifiers = []
    for capability in capabilities:
        _validate_capability(capability)
        identifiers.append(capability["capability_id"])
    if len(identifiers) != len(set(identifiers)):
        raise ReuseSearchError("capability id is duplicated")

    source_content_id = profile_document.get("source_content_id")
    if discovery_document.get("source_content_id") != source_content_id:
        raise ReuseSearchError("profile and discovery source content ids differ")
    routines = profile_document.get("routines", [])
    by_id = {item["symbol_id"]: item for item in routines}
    groups_by_member = {}
    groups_by_id = {}
    for group in discovery_document.get("groups", []):
        groups_by_id[group["group_id"]] = group
        for member in group.get("member_symbol_ids", []):
            groups_by_member.setdefault(member, []).append(group)

    observed_paths = {item["path"] for item in observation_document.get("files", [])}
    lifecycle_cache = {}
    aggregate_reasons = {}
    referenced_group_ids = set()
    capability_results = []
    uncovered = []
    for capability in capabilities:
        reasons = {}
        anchor_ids = set()
        capability_group_ids = set()
        reference_paths = tuple(capability["reference_paths"])
        reference_symbols = set(capability["reference_symbols"])
        symbol_terms = tuple(capability["symbol_terms"])
        required_markers = set(capability["required_effect_markers"])
        forbidden_markers = set(capability["forbidden_effect_markers"])

        for routine in routines:
            symbol_id = routine["symbol_id"]
            relative = routine["code_reference"]["relative_path"]
            symbol_name = symbol_id.rsplit(":", 1)[-1]
            direct_reasons = []
            if any(
                relative == prefix or relative.startswith(f"{prefix}/")
                for prefix in reference_paths
            ):
                direct_reasons.append("reference_path_anchor")
            if symbol_id in reference_symbols:
                direct_reasons.append("reference_symbol_anchor")
            if any(term in symbol_name for term in symbol_terms):
                direct_reasons.append("symbol_term_hint")
            if direct_reasons:
                anchor_ids.add(symbol_id)
                reasons.setdefault(symbol_id, set()).update(direct_reasons)
            if required_markers and required_markers <= set(
                routine.get("syntactic_effect_markers", [])
            ):
                reasons.setdefault(symbol_id, set()).add("required_effect_marker_match")

        for symbol_id in sorted(anchor_ids):
            routine = by_id[symbol_id]
            for neighbor in tuple(routine.get("direct_callee_symbol_ids", ())) + tuple(
                routine.get("direct_caller_symbol_ids", ())
            ):
                if neighbor in by_id:
                    reasons.setdefault(neighbor, set()).add("direct_neighbor")
            for group in groups_by_member.get(symbol_id, []):
                if (
                    group.get("basis_kind") not in _CAPABILITY_EXPANSION_BASIS_KINDS
                    or group.get("presentation_class") != "focused"
                ):
                    continue
                referenced_group_ids.add(group["group_id"])
                capability_group_ids.add(group["group_id"])
                for member in group.get("member_symbol_ids", []):
                    if member in by_id:
                        reasons.setdefault(member, set()).add("comparison_group_member")

        candidates = []
        for symbol_id in sorted(reasons):
            routine = by_id[symbol_id]
            related_groups = sorted(
                group["group_id"]
                for group in groups_by_member.get(symbol_id, [])
                if group["group_id"] in capability_group_ids
            )
            markers = set(routine.get("syntactic_effect_markers", []))
            item = {
                "symbol_id": symbol_id,
                "code_reference": dict(routine["code_reference"]),
                "match_reasons": sorted(reasons[symbol_id]),
                "related_group_ids": related_groups,
                "conflicting_effect_markers": sorted(markers & forbidden_markers),
                "declared_lifecycle": _source_lifecycle(
                    project_root,
                    routine["code_reference"]["relative_path"],
                    lifecycle_cache,
                ),
            }
            candidates.append(item)
            aggregate_reasons.setdefault(symbol_id, set()).update(reasons[symbol_id])
        coverage = "candidates_found" if candidates else "no_candidates"
        if not candidates:
            uncovered.append(capability["capability_id"])
        capability_results.append(
            {
                "capability_id": capability["capability_id"],
                "coverage_status": coverage,
                "anchor_symbol_ids": sorted(anchor_ids),
                "missing_reference_paths": sorted(
                    relative
                    for relative in set(reference_paths)
                    if not any(
                        path == relative or path.startswith(f"{relative}/")
                        for path in observed_paths
                    )
                ),
                "missing_reference_symbols": sorted(reference_symbols - set(by_id)),
                "candidates": candidates,
            }
        )

    hits = [
        {
            "symbol_id": symbol_id,
            "code_reference": dict(by_id[symbol_id]["code_reference"]),
            "match_reasons": sorted(reasons),
            "group_id": None,
            "basis_kind": None,
        }
        for symbol_id, reasons in sorted(aggregate_reasons.items())
    ]
    groups = [
        {
            "group_id": group_id,
            "basis_kind": groups_by_id[group_id].get("basis_kind"),
            "member_symbol_ids": list(groups_by_id[group_id]["member_symbol_ids"]),
        }
        for group_id in sorted(referenced_group_ids)
    ]
    record = {
        "record_kind": "reuse_search_record",
        "schema_version": 3,
        "subject": subject,
        "declaration": {
            "subject": subject,
            "source_scope_paths": list(source_scope_paths),
            "capabilities": json.loads(json.dumps(capabilities)),
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
        "query": {"rules_applied": list(_CAPABILITY_QUERY_RULES)},
        "hits": hits,
        "groups": groups,
        "capability_results": capability_results,
        "uncovered_capability_ids": sorted(uncovered),
        "human_adjudication_required": True,
        "freshness": _assess_freshness(
            observation_document=observation_document,
            target_paths=source_scope_paths,
            project_root=project_root,
        ),
    }
    record["content_digest"] = _content_digest(record)
    return record


def search_required_capabilities_grouped(
    *,
    profile_document,
    discovery_document,
    declaration,
    observation_document,
    project_root=".",
):
    """既存の比較集団を崩さず、直接対象と検索上の手掛かりを分ける。"""
    legacy = search_required_capabilities(
        profile_document=profile_document,
        discovery_document=discovery_document,
        declaration=declaration,
        observation_document=observation_document,
        project_root=project_root,
    )
    if discovery_document.get("routine_profile_run_id") != _profile_run_id(
        profile_document
    ):
        raise ReuseSearchError("profile and discovery run ids differ")
    if discovery_document.get("routine_profile_content_digest") != profile_document.get(
        "content_digest"
    ):
        raise ReuseSearchError("profile and discovery content digests differ")
    source_scope_paths = declaration["source_scope_paths"]
    routines = [
        item
        for item in profile_document.get("routines", [])
        if any(
            item["code_reference"]["relative_path"] == prefix
            or item["code_reference"]["relative_path"].startswith(f"{prefix}/")
            for prefix in source_scope_paths
        )
    ]
    by_id = {item["symbol_id"]: item for item in routines}
    capability_results = []
    no_search_material = []
    legacy_by_capability = {
        item["capability_id"]: item for item in legacy["capability_results"]
    }

    def match_item(candidate, reasons):
        return {
            "symbol_id": candidate["symbol_id"],
            "code_reference": dict(candidate["code_reference"]),
            "match_reasons": sorted(reasons),
            "conflicting_effect_markers": list(
                candidate["conflicting_effect_markers"]
            ),
            "declared_lifecycle": candidate["declared_lifecycle"],
        }

    hint_reason_names = {
        "reference_path_anchor": "reference_path_hint",
        "symbol_term_hint": "symbol_term_hint",
        "required_effect_marker_match": "required_effect_marker_hint",
    }
    for capability in declaration["capabilities"]:
        legacy_result = legacy_by_capability[capability["capability_id"]]
        candidates = {
            item["symbol_id"]: item
            for item in legacy_result["candidates"]
            if item["symbol_id"] in by_id
        }
        direct_reasons = {}
        hint_reasons = {
            symbol_id: {
                hint_reason_names[reason]
                for reason in item["match_reasons"]
                if reason in hint_reason_names
            }
            for symbol_id, item in candidates.items()
            if set(item["match_reasons"]) & set(hint_reason_names)
        }
        group_seed_ids = set()
        reference_symbols = set(capability["reference_symbols"])
        for symbol_id in sorted(reference_symbols & set(by_id)):
            direct_reasons.setdefault(symbol_id, set()).add("exact_reference_symbol")
            group_seed_ids.add(symbol_id)
            routine = by_id[symbol_id]
            for neighbor in tuple(routine.get("direct_callee_symbol_ids", ())) + tuple(
                routine.get("direct_caller_symbol_ids", ())
            ):
                if neighbor in by_id:
                    direct_reasons.setdefault(neighbor, set()).add("direct_neighbor")

        for symbol_id, reasons in hint_reasons.items():
            if "symbol_term_hint" in reasons:
                group_seed_ids.add(symbol_id)

        for symbol_id in sorted(set(direct_reasons) & set(hint_reasons)):
            direct_reasons[symbol_id].update(hint_reasons.pop(symbol_id))

        grouped = {}
        for symbol_id in sorted(group_seed_ids):
            payload = work4a.build_llm_initial_input(
                routine_profile_document=profile_document,
                comparison_discovery_document=discovery_document,
                symbol_id=symbol_id,
            )
            for summary in payload["comparison_groups"]:
                group_id = summary["group_id"]
                if group_id not in grouped:
                    grouped[group_id] = {
                        **json.loads(json.dumps(summary)),
                        "matched_symbol_ids": [],
                    }
                grouped[group_id]["matched_symbol_ids"].append(symbol_id)

        direct_matches = [
            match_item(candidates[symbol_id], direct_reasons[symbol_id])
            for symbol_id in sorted(direct_reasons)
        ]
        hint_matches = [
            match_item(candidates[symbol_id], hint_reasons[symbol_id])
            for symbol_id in sorted(hint_reasons)
        ]
        comparison_groups = []
        for group_id in sorted(grouped):
            summary = grouped[group_id]
            summary["matched_symbol_ids"] = sorted(set(summary["matched_symbol_ids"]))
            comparison_groups.append(summary)

        if direct_matches:
            search_status = "direct_matches_found"
        elif hint_matches or comparison_groups:
            search_status = "search_hints_found"
        else:
            search_status = "no_search_material"
            no_search_material.append(capability["capability_id"])
        capability_results.append(
            {
                "capability_id": capability["capability_id"],
                "search_status": search_status,
                "direct_matches": direct_matches,
                "hint_matches": hint_matches,
                "comparison_groups": comparison_groups,
                "missing_reference_paths": list(
                    legacy_result["missing_reference_paths"]
                ),
                "missing_reference_symbols": list(
                    legacy_result["missing_reference_symbols"]
                ),
            }
        )

    record = {
        "record_kind": "reuse_search_record",
        "schema_version": 4,
        "subject": legacy["subject"],
        "declaration": json.loads(json.dumps(legacy["declaration"])),
        "source_identity": dict(legacy["source_identity"]),
        "query": {"rules_applied": list(_GROUPED_CAPABILITY_QUERY_RULES)},
        "capability_results": capability_results,
        "no_search_material_capability_ids": sorted(no_search_material),
        "human_adjudication_required": True,
        "freshness": json.loads(json.dumps(legacy["freshness"])),
    }
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
        # 反証R-2・R-4：宣言とfreshnessの対象範囲は一致しなければならない。
        # 片方だけ狭めると、gateが範囲外の変更・新規fileを見なくなる。
        if list(record["freshness"]["target_paths"]) != list(
            record["declaration"]["target_paths"]
        ):
            raise ReuseSearchError(
                "freshness scope disagrees with the declared scope"
            )
    elif schema_version == 3:
        _require_exact_fields(record, _RECORD_FIELDS_V3, "reuse search record")
        _require_exact_fields(record["freshness"], _FRESHNESS_FIELDS, "freshness")
        _require_exact_fields(
            record["declaration"],
            _CAPABILITY_DECLARATION_FIELDS,
            "capability declaration",
        )
        if list(record["freshness"]["target_paths"]) != list(
            record["declaration"]["source_scope_paths"]
        ):
            raise ReuseSearchError(
                "freshness scope disagrees with the declared source scope"
            )
        capability_ids = []
        for capability in record["declaration"]["capabilities"]:
            _validate_capability(capability)
            capability_ids.append(capability["capability_id"])
        if len(capability_ids) != len(set(capability_ids)):
            raise ReuseSearchError("capability id is duplicated")
        result_ids = []
        uncovered = []
        for result in record["capability_results"]:
            _require_exact_fields(
                result, _CAPABILITY_RESULT_FIELDS, "capability result"
            )
            result_ids.append(result["capability_id"])
            if result["coverage_status"] not in ("candidates_found", "no_candidates"):
                raise ReuseSearchError("capability coverage status is invalid")
            if result["coverage_status"] == "no_candidates":
                uncovered.append(result["capability_id"])
            for candidate in result["candidates"]:
                _require_exact_fields(
                    candidate, _CAPABILITY_CANDIDATE_FIELDS, "capability candidate"
                )
                if candidate["declared_lifecycle"] not in (
                    "stable", "provisional", "stopped", "undeclared"
                ):
                    raise ReuseSearchError("declared lifecycle is invalid")
        if result_ids != capability_ids:
            raise ReuseSearchError("capability result coverage is incomplete")
        if sorted(uncovered) != record["uncovered_capability_ids"]:
            raise ReuseSearchError("uncovered capability summary differs")
        if record["human_adjudication_required"] is not True:
            raise ReuseSearchError("human adjudication boundary is missing")
    elif schema_version == 4:
        _require_exact_fields(record, _RECORD_FIELDS_V4, "reuse search record")
        _require_exact_fields(record["freshness"], _FRESHNESS_FIELDS, "freshness")
        _require_exact_fields(
            record["declaration"],
            _CAPABILITY_DECLARATION_FIELDS,
            "capability declaration",
        )
        if list(record["freshness"]["target_paths"]) != list(
            record["declaration"]["source_scope_paths"]
        ):
            raise ReuseSearchError(
                "freshness scope disagrees with the declared source scope"
            )
        capability_ids = []
        for capability in record["declaration"]["capabilities"]:
            _validate_capability(capability)
            capability_ids.append(capability["capability_id"])
        if len(capability_ids) != len(set(capability_ids)):
            raise ReuseSearchError("capability id is duplicated")
        result_ids = []
        no_search_material = []
        for result in record["capability_results"]:
            _require_exact_fields(
                result,
                _GROUPED_CAPABILITY_RESULT_FIELDS,
                "grouped capability result",
            )
            result_ids.append(result["capability_id"])
            if result["search_status"] not in (
                "direct_matches_found",
                "search_hints_found",
                "no_search_material",
            ):
                raise ReuseSearchError("capability search status is invalid")
            if result["search_status"] == "no_search_material":
                no_search_material.append(result["capability_id"])
            for field in ("direct_matches", "hint_matches"):
                for match in result[field]:
                    _require_exact_fields(
                        match, _GROUPED_MATCH_FIELDS, "grouped capability match"
                    )
            for group in result["comparison_groups"]:
                _require_exact_fields(
                    group,
                    _COMPARISON_GROUP_SUMMARY_FIELDS,
                    "comparison group summary",
                )
                if "member_symbol_ids" in group:
                    raise ReuseSearchError("comparison group members were flattened")
        if result_ids != capability_ids:
            raise ReuseSearchError("capability result coverage is incomplete")
        if sorted(no_search_material) != record[
            "no_search_material_capability_ids"
        ]:
            raise ReuseSearchError("no search material summary differs")
        if record["human_adjudication_required"] is not True:
            raise ReuseSearchError("human adjudication boundary is missing")
    else:
        raise ReuseSearchError("schema version is invalid")
    if schema_version in (1, 2):
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

    if schema_version <= 3:
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


def _gate_verdict(record, *, expected_identity, project_root):
    """読み込み済みrecordに対する共通のgate判定（検証と鮮度再計測）。"""

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


def _search_matches(record, *, profile_document, discovery_document, project_root):
    """記録された検索結果を再現し、同一かどうかを返す（反証R-3）。

    記録済みの宣言と観測から検索をやり直し、content digestを突き合わせる。
    観測欄を持たないschema 1のrecordは再現の材料が無いため、照合しない。
    """

    if record["schema_version"] == 1:
        return True
    freshness = record["freshness"]
    observation = {
        "snapshot_id": freshness["observation_snapshot_id"],
        "source_content_id": record["source_identity"]["source_content_id"],
        "files": [
            {"path": item["path"], "file_sha256": item["sha256"]}
            for item in freshness["files_at_observation"]
        ],
    }
    if record["schema_version"] == 2:
        rebuilt = search_existing_routines(
            profile_document=profile_document,
            discovery_document=discovery_document,
            declaration=record["declaration"],
            observation_document=observation,
            project_root=project_root,
        )
    elif record["schema_version"] == 3:
        rebuilt = search_required_capabilities(
            profile_document=profile_document,
            discovery_document=discovery_document,
            declaration=record["declaration"],
            observation_document=observation,
            project_root=project_root,
        )
    else:
        rebuilt = search_required_capabilities_grouped(
            profile_document=profile_document,
            discovery_document=discovery_document,
            declaration=record["declaration"],
            observation_document=observation,
            project_root=project_root,
        )
    return rebuilt["content_digest"] == record["content_digest"]


def gate_check(
    *,
    record_path,
    expected_identity,
    project_root=".",
    profile_document=None,
    discovery_document=None,
):
    """実装開始のgate判定。record不存在・結線不一致・鮮度乖離はfail-closedで開始不可。

    ProfileとDiscoveryを渡した場合、検索を再実行して結果の一致まで確認する
    （反証R-3。渡さない場合は再検索を行わない）。
    """

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
    if profile_document is not None and discovery_document is not None:
        try:
            reproduced = _search_matches(
                record,
                profile_document=profile_document,
                discovery_document=discovery_document,
                project_root=project_root,
            )
        except ReuseSearchError as error:
            return {
                "start_allowed": False,
                "reason": f"search_result_unreproducible: {error}",
            }
        if not reproduced:
            return {"start_allowed": False, "reason": "search_result_mismatch"}
    return _gate_verdict(
        record, expected_identity=expected_identity, project_root=project_root
    )


_EXTERNAL_DIRECTORY = "work4b/reuse-searches"


def _external_relative_path(record):
    return f"{_EXTERNAL_DIRECTORY}/{record['content_digest']}.json"


def _build_attestation(record, *, byte_sha256):
    document = {
        "record_kind": "reuse_search_attestation",
        "schema_version": 1,
        "subject": record["subject"],
        "external": {
            "relative_path": _external_relative_path(record),
            "content_digest": record["content_digest"],
            "byte_sha256": byte_sha256,
        },
        "source_identity": dict(record["source_identity"]),
        "record_schema_version": record["schema_version"],
    }
    if record["schema_version"] <= 3:
        document["hit_count"] = len(record["hits"])
    if record["schema_version"] == 3:
        document["capability_count"] = len(record["capability_results"])
        document["uncovered_capability_count"] = len(
            record["uncovered_capability_ids"]
        )
    if record["schema_version"] == 4:
        document["capability_count"] = len(record["capability_results"])
        document["direct_match_count"] = sum(
            len(result["direct_matches"])
            for result in record["capability_results"]
        )
        document["hint_match_count"] = sum(
            len(result["hint_matches"])
            for result in record["capability_results"]
        )
        document["comparison_group_count"] = sum(
            len(result["comparison_groups"])
            for result in record["capability_results"]
        )
        document["no_search_material_capability_count"] = len(
            record["no_search_material_capability_ids"]
        )
    document["content_digest"] = _content_digest(document)
    return document


def _write_new_text(path, text):
    target = Path(path)
    if target.exists():
        raise ReuseSearchError(f"target already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def externalize_reuse_search_record(*, record, data_root, attestation_path):
    """record本体を外部rootへ、証明書をproject内へ、いずれもnew-onlyで書く。"""

    external = Path(data_root) / _external_relative_path(record)
    _write_new_text(
        external, json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    )
    attestation = _build_attestation(record, byte_sha256=file_sha256(external))
    _write_new_text(
        attestation_path,
        json.dumps(attestation, ensure_ascii=False, indent=2) + "\n",
    )
    return attestation


def migrate_reuse_search_record(*, record_path, data_root, attestation_path):
    """既存recordをbyte一致で外部化する。旧位置recordは削除せず保持する。"""

    source = Path(record_path)
    payload = source.read_bytes()
    record = json.loads(payload.decode("utf-8"))
    external = Path(data_root) / _external_relative_path(record)
    if external.exists():
        raise ReuseSearchError(f"target already exists: {external}")
    external.parent.mkdir(parents=True, exist_ok=True)
    external.write_bytes(payload)
    if external.read_bytes() != payload or not source.is_file():
        raise ReuseSearchError("migration is not byte identical")
    attestation = _build_attestation(record, byte_sha256=file_sha256(external))
    _write_new_text(
        attestation_path,
        json.dumps(attestation, ensure_ascii=False, indent=2) + "\n",
    )
    return {
        "byte_identical": True,
        "external_path": str(external),
        "attestation_path": str(attestation_path),
        "content_digest": record["content_digest"],
    }


def gate_check_attested(*, attestation_path, data_root, expected_identity, project_root="."):
    """証明書経由のgate判定。外部recordの欠落・改竄はfail-closedで開始不可。"""

    try:
        attestation = json.loads(Path(attestation_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"start_allowed": False, "reason": "attestation_unavailable"}
    external_ref = attestation.get("external", {})
    relative = external_ref.get("relative_path")
    if (
        not isinstance(relative, str)
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
    ):
        return {"start_allowed": False, "reason": "attestation_unavailable"}
    external = Path(data_root) / relative
    if not external.is_file():
        return {"start_allowed": False, "reason": "record_unavailable"}
    if file_sha256(external) != external_ref.get("byte_sha256"):
        return {"start_allowed": False, "reason": "record_unavailable"}
    try:
        record = json.loads(external.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"start_allowed": False, "reason": "record_unavailable"}
    if record.get("content_digest") != external_ref.get("content_digest"):
        return {"start_allowed": False, "reason": "record_unavailable"}
    # 反証R-5・R-6：証明書は外部本体の要約を載せる。要約が本体と食い違うなら、
    # 読み手が本体を開かずに誤った件数・由来を信じることになる。
    expected_attestation = _build_attestation(
        record, byte_sha256=external_ref.get("byte_sha256")
    )
    if attestation != expected_attestation:
        return {"start_allowed": False, "reason": "attestation_mismatch"}
    return _gate_verdict(
        record, expected_identity=expected_identity, project_root=project_root
    )
