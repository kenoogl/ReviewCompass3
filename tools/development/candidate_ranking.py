"""絞り込み順位表（構成A-2）：LLM意味判断へ渡す候補groupの機械的な順位付け。

承認：DEC-WORK4B-MAIN-DESIGN-BUNDLE-001 §2 A-2

順位は承認済みの辞書式順——(1)basis_kindの強さ、(2)守り役moduleの含有、(3)member数、
(4)変更範囲との交差——で決定的に計算する。統合除外宣言に該当するgroupは候補から落とし、
落とした件数・group・該当entryを順位表自身が表示する（silent capの禁止）。
staleなProfileからの生成はfail-closedで拒否する（構成Bの締め）。
"""

import hashlib
import json
from pathlib import Path

from tools.development.integration_exclusions import (
    IntegrationExclusionError,
    excluded_entry_ids,
    validate_integration_exclusions,
)
from tools.development.reuse_search_record import _assess_freshness


class CandidateRankingError(Exception):
    """順位表の生成・保存の失敗。"""


_BASIS_ORDER = (
    "structural_exact_match",
    "interface_shape_match",
    "shared_direct_callee",
    "shared_test_reference",
    "shared_exception_contract",
    "call_neighborhood",
)
_FRESHNESS_TARGET_PATHS = ("tools/",)


from tools.common.digests import file_sha256 as file_sha256


from tools.common.digests import canonical_content_digest as _content_digest


def _matches_any(relative, prefixes):
    return any(
        relative == prefix or relative.startswith(prefix) for prefix in prefixes
    )


def build_candidate_ranking(
    *,
    profile_document,
    discovery_document,
    exclusions_record,
    observation_document,
    project_root,
    guard_module_paths,
    changed_paths,
    created_at,
):
    """除外・鮮度・順位規則を適用した順位表recordを決定的に生成する。"""

    if profile_document.get("source_content_id") != discovery_document.get(
        "source_content_id"
    ):
        raise CandidateRankingError("profile and discovery source content ids differ")

    # 除外宣言は候補の脱落を決める。検証せずに受け取ると、壊れた宣言のまま
    # groupを落とせてしまう。
    try:
        validate_integration_exclusions(
            exclusions_record, project_root=project_root
        )
    except IntegrationExclusionError as error:
        raise CandidateRankingError(
            f"exclusions record is invalid: {error}"
        ) from error

    freshness = _assess_freshness(
        observation_document=observation_document,
        target_paths=_FRESHNESS_TARGET_PATHS,
        project_root=project_root,
    )
    if freshness["stale"]:
        raise CandidateRankingError(
            "profile_stale: "
            + ",".join(
                freshness["changed_files"]
                + freshness["new_files"]
                + freshness["missing_files"]
            )
        )

    module_by_symbol = {
        routine["symbol_id"]: routine["code_reference"]["relative_path"]
        for routine in profile_document.get("routines", [])
    }

    ranked_source = []
    dropped = []
    for group in discovery_document.get("groups", []):
        members = list(group.get("member_symbol_ids", []))
        entry_ids = sorted(
            {
                entry_id
                for symbol_id in members
                for entry_id in excluded_entry_ids(
                    symbol_id, record=exclusions_record
                )
            }
        )
        if entry_ids:
            dropped.append({"group_id": group["group_id"], "entry_ids": entry_ids})
            continue

        basis_kind = group.get("basis_kind")
        if basis_kind not in _BASIS_ORDER:
            raise CandidateRankingError(f"unknown basis kind: {basis_kind}")
        member_paths = [
            module_by_symbol.get(symbol_id, symbol_id.split(":", 1)[0])
            for symbol_id in members
        ]
        guard = any(_matches_any(path, guard_module_paths) for path in member_paths)
        change_overlap = any(
            _matches_any(path, changed_paths) for path in member_paths
        )
        ranked_source.append(
            {
                "group_id": group["group_id"],
                "basis_kind": basis_kind,
                "member_count": len(members),
                "contains_guard_module": guard,
                "overlaps_changed_paths": change_overlap,
            }
        )

    ranked_source.sort(
        key=lambda entry: (
            _BASIS_ORDER.index(entry["basis_kind"]),
            0 if entry["contains_guard_module"] else 1,
            -entry["member_count"],
            0 if entry["overlaps_changed_paths"] else 1,
            entry["group_id"],
        )
    )
    ranking = [
        dict(entry, rank=index + 1) for index, entry in enumerate(ranked_source)
    ]
    dropped.sort(key=lambda item: item["group_id"])

    record = {
        "record_kind": "candidate_ranking",
        "schema_version": 1,
        "created_at": created_at,
        "source_identity": {
            "profile_run_id": profile_document.get(
                "profile_run_id", profile_document.get("run_id")
            ),
            "discovery_run_id": discovery_document.get(
                "discovery_run_id", discovery_document.get("run_id")
            ),
            "source_content_id": profile_document.get("source_content_id"),
            "exclusion_id": exclusions_record["exclusion_id"],
            "exclusion_content_digest": exclusions_record["content_digest"],
        },
        "freshness": freshness,
        "rule": {
            "basis_order": list(_BASIS_ORDER),
            "criteria_order": [
                "basis_kind_strength",
                "contains_guard_module",
                "member_count",
                "overlaps_changed_paths",
                "group_id",
            ],
        },
        "guard_module_paths": sorted(guard_module_paths),
        "changed_paths": sorted(changed_paths),
        "excluded": {
            "dropped_group_count": len(dropped),
            "dropped_groups": dropped,
        },
        "ranking": ranking,
    }
    record["content_digest"] = _content_digest(record)
    return record


def write_candidate_ranking(*, path, record):
    """new-onlyで保存する。既存fileの上書きを拒否する。"""

    target = Path(path)
    if target.exists():
        raise CandidateRankingError("candidate ranking record already exists")
    target.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
