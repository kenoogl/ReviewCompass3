"""構成A-2：絞り込み順位表の宣言G1〜G5を固定するTest。

承認：DEC-WORK4B-MAIN-DESIGN-BUNDLE-001 §2 A-2（辞書式順1→3→4→2、除外の件数表示、
silent capの禁止）
"""

import json
from pathlib import Path

import pytest

from tools.development import candidate_ranking as cr
from tools.development import integration_exclusions as ix


PROFILE_RUN_ID = "a" * 64
DISCOVERY_RUN_ID = "b" * 64
SOURCE_CONTENT_ID = "c" * 64
SNAPSHOT_ID = "9" * 64


def _routine(symbol_id, path):
    return {
        "symbol_id": symbol_id,
        "code_reference": {"relative_path": path, "start_line": 1, "end_line": 2},
        "signature": "()",
        "structure_digest": "d" * 64,
        "direct_callee_symbol_ids": [],
        "direct_caller_symbol_ids": [],
    }


def _fixture_profile():
    return {
        "run_id": PROFILE_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [
            _routine("tools/pkg/guard.py:check", "tools/pkg/guard.py"),
            _routine("tools/pkg/plain.py:render", "tools/pkg/plain.py"),
            _routine("tools/pkg/frozen.py:legacy", "tools/pkg/frozen.py"),
            _routine("tools/pkg/other.py:helper", "tools/pkg/other.py"),
        ],
    }


def _group(group_id, basis_kind, members):
    return {
        "group_id": group_id,
        "basis_kind": basis_kind,
        "member_symbol_ids": members,
    }


def _fixture_discovery():
    return {
        "run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [
            _group(
                "group-weak-guard",
                "call_neighborhood",
                ["tools/pkg/guard.py:check", "tools/pkg/other.py:helper"],
            ),
            _group(
                "group-strong-plain",
                "structural_exact_match",
                ["tools/pkg/plain.py:render", "tools/pkg/other.py:helper"],
            ),
            _group(
                "group-strong-guard",
                "structural_exact_match",
                ["tools/pkg/guard.py:check", "tools/pkg/plain.py:render"],
            ),
            _group(
                "group-frozen",
                "structural_exact_match",
                ["tools/pkg/frozen.py:legacy", "tools/pkg/plain.py:render"],
            ),
        ],
    }


def _exclusions(tmp_path):
    approval = tmp_path / "records" / "approval.md"
    approval.parent.mkdir(parents=True, exist_ok=True)
    approval.write_text("# approval\n", encoding="utf-8")
    record = {
        "record_kind": "integration_exclusions",
        "schema_version": 1,
        "exclusion_id": "RC3-FIXTURE-EXCLUSIONS-001",
        "exclusion_version": 1,
        "created_at": "2026-08-07T13:34:52+09:00",
        "approval": {
            "decision_id": "DEC-FIXTURE-001",
            "path": "records/approval.md",
            "sha256": ix.file_sha256(approval),
        },
        "entries": [
            {
                "entry_id": "E1",
                "reason_kind": "frozen_lane",
                "targets": [
                    {"kind": "module_path", "value": "tools/pkg/frozen.py"}
                ],
                "rationale": "凍結対象",
                "authority_refs": [
                    {"decision_id": "DEC-FIXTURE-001", "path": "records/approval.md"}
                ],
            }
        ],
    }
    record["content_digest"] = ix.content_digest(record)
    return record


def _observation(tmp_path, paths):
    for relative in paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text("def x():\n    pass\n", encoding="utf-8")
    return {
        "snapshot_id": SNAPSHOT_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "files": [
            {
                "path": relative,
                "file_sha256": cr.file_sha256(tmp_path / relative),
            }
            for relative in paths
        ],
    }


_PATHS = (
    "tools/pkg/guard.py",
    "tools/pkg/plain.py",
    "tools/pkg/frozen.py",
    "tools/pkg/other.py",
)


def _build(tmp_path, **overrides):
    observation = overrides.pop("observation", None) or _observation(tmp_path, _PATHS)
    arguments = {
        "profile_document": _fixture_profile(),
        "discovery_document": _fixture_discovery(),
        "exclusions_record": _exclusions(tmp_path),
        "observation_document": observation,
        "project_root": tmp_path,
        "guard_module_paths": ["tools/pkg/guard.py"],
        "changed_paths": [],
        "created_at": "2026-08-07T13:34:52+09:00",
    }
    arguments.update(overrides)
    return cr.build_candidate_ranking(**arguments)


def test_g1_ranking_is_deterministic(tmp_path):
    first = _build(tmp_path)
    second = _build(tmp_path)
    assert first == second
    assert first["content_digest"] == second["content_digest"]


def test_g2_order_follows_the_approved_lexicographic_rule(tmp_path):
    record = _build(tmp_path)
    ordered = [entry["group_id"] for entry in record["ranking"]]
    assert ordered == ["group-strong-guard", "group-strong-plain", "group-weak-guard"]
    assert [entry["rank"] for entry in record["ranking"]] == [1, 2, 3]


def test_g3_excluded_groups_are_dropped_with_visible_counts(tmp_path):
    record = _build(tmp_path)
    excluded = record["excluded"]
    assert excluded["dropped_group_count"] == 1
    assert excluded["dropped_groups"] == [
        {"group_id": "group-frozen", "entry_ids": ["E1"]}
    ]
    ranked_ids = {entry["group_id"] for entry in record["ranking"]}
    assert "group-frozen" not in ranked_ids


def test_g4_stale_profile_is_rejected_fail_closed(tmp_path):
    observation = _observation(tmp_path, _PATHS)
    (tmp_path / "tools/pkg/guard.py").write_text(
        "def x():\n    return 1\n", encoding="utf-8"
    )
    with pytest.raises(cr.CandidateRankingError):
        _build(tmp_path, observation=observation)


def test_g5_write_is_new_only(tmp_path):
    record = _build(tmp_path)
    target = tmp_path / "ranking-v1.json"
    cr.write_candidate_ranking(path=target, record=record)
    with pytest.raises(cr.CandidateRankingError):
        cr.write_candidate_ranking(path=target, record=record)
    assert json.loads(target.read_text(encoding="utf-8")) == record
