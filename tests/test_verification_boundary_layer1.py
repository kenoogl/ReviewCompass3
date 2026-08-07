"""層1の残り3件：対応表のscope欄、gate時の再検索、空文字拒否と決定日時の単調性。

承認：DEC-VERIFICATION-BOUNDARY-001（層1）
所見：反証C-1（対象範囲の宣言）、R-3（検索したふり）、C-2（空summary）、I-2（decided_at）
"""

import hashlib
import json
from pathlib import Path

import pytest

from tools.development import declaration_red_map_check as drmc
from tools.development import issue_intake_v4 as intake
from tools.development import reuse_search_record as rsr


P, D, S = "a" * 64, "b" * 64, "c" * 64
EXPECTED = {"profile_run_id": P, "discovery_run_id": D, "source_content_id": S}


# ---------------------------------------------------------------- C-1：scope欄


def _tests_file(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_sample.py").write_text(
        "def test_a():\n    pass\n\n\ndef test_orphan():\n    pass\n", encoding="utf-8"
    )
    return "tests/test_sample.py"


def _map(tmp_path, *, scope, listed, declared, reason=None):
    relative = _tests_file(tmp_path)
    document = {
        "record_kind": "declaration_red_map",
        "map_id": "M", "map_version": 1,
        "scope": {"kind": scope},
        "test_files": {relative: sorted(listed)},
        "declarations": {
            "P1": {
                "summary": "s",
                "tests": [{"test": "%s::%s" % (relative, name), "red_now": True}
                          for name in declared],
                "red_now": True,
            }
        },
    }
    if reason is not None:
        document["scope"]["reason"] = reason
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return path


def test_l1_complete_scope_detects_a_test_missing_from_both_sides(tmp_path):
    """反証C-1の完全解消：欄からも宣言からも漏れた実在testを検出する。"""

    path = _map(tmp_path, scope="complete", listed=["test_a"], declared=["test_a"])
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert any("test_unmapped_to_declarations" in finding and "test_orphan" in finding
               for finding in result["findings"])


def test_l2_partial_scope_limits_the_check_to_the_listing(tmp_path):
    """部分列挙は、理由を添えれば範囲外のtestを対象にしない。"""

    path = _map(tmp_path, scope="partial", listed=["test_a"], declared=["test_a"],
                reason="変更したtestだけを扱う対応表である")
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "passed"


def test_l3_partial_scope_without_a_reason_is_rejected(tmp_path):
    """範囲を狭めるなら理由を残さなければならない。"""

    path = _map(tmp_path, scope="partial", listed=["test_a"], declared=["test_a"])
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert any("scope_reason_missing" in finding for finding in result["findings"])


def test_l4_missing_scope_defaults_to_complete(tmp_path):
    """scope欄の無い対応表は完全列挙として扱う（黙って緩めない）。"""

    relative = _tests_file(tmp_path)
    document = {
        "record_kind": "declaration_red_map", "map_id": "M", "map_version": 1,
        "test_files": {relative: ["test_a"]},
        "declarations": {"P1": {"summary": "s", "tests": [
            {"test": "%s::test_a" % relative, "red_now": True}], "red_now": True}},
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert any("test_orphan" in finding for finding in result["findings"])


# ---------------------------------------------------------------- C-2：空summary


def test_l5_empty_declaration_summary_is_rejected(tmp_path):
    relative = _tests_file(tmp_path)
    document = {
        "record_kind": "declaration_red_map", "map_id": "M", "map_version": 1,
        "scope": {"kind": "partial", "reason": "fixture"},
        "test_files": {relative: ["test_a"]},
        "declarations": {"P1": {"summary": "   ", "tests": [
            {"test": "%s::test_a" % relative, "red_now": True}], "red_now": True}},
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert any("declaration_summary_empty" in finding for finding in result["findings"])


# ---------------------------------------------------------------- R-3：gate再検索


def _search_env(tmp_path):
    source = tmp_path / "tools/pkg/existing.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("def helper():\n    pass\n", encoding="utf-8")
    profile = {
        "run_id": P, "source_content_id": S, "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [{
            "symbol_id": "tools/pkg/existing.py:helper",
            "code_reference": {"relative_path": "tools/pkg/existing.py",
                               "start_line": 1, "end_line": 2},
            "signature": "()", "structure_digest": "d" * 64,
            "direct_callee_symbol_ids": [], "direct_caller_symbol_ids": [],
        }],
    }
    discovery = {"run_id": D, "source_content_id": S, "schema_version": 1,
                 "grouping_rule_version": 1, "groups": []}
    declaration = {"subject": "r3", "target_paths": ["tools/pkg/"],
                   "target_symbols": ["helper"]}
    observation = {"snapshot_id": "9" * 64, "source_content_id": S,
                   "files": [{"path": "tools/pkg/existing.py",
                              "file_sha256": rsr.file_sha256(source)}]}
    record = rsr.search_existing_routines(
        profile_document=profile, discovery_document=discovery,
        declaration=declaration, observation_document=observation,
        project_root=tmp_path,
    )
    return record, profile, discovery


def test_l6_emptied_hits_are_rejected_by_re_running_the_search(tmp_path):
    """反証R-3：検索したふりのrecordは、gateが再検索して拒否する。"""

    record, profile, discovery = _search_env(tmp_path)
    record["hits"] = []
    record["groups"] = []
    record["content_digest"] = rsr._content_digest(record)
    path = tmp_path / "search.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    gate = rsr.gate_check(
        record_path=path, expected_identity=EXPECTED, project_root=tmp_path,
        profile_document=profile, discovery_document=discovery,
    )
    assert gate["start_allowed"] is False
    assert gate["reason"] == "search_result_mismatch"


def test_l7_intact_record_passes_the_re_run(tmp_path):
    record, profile, discovery = _search_env(tmp_path)
    path = tmp_path / "search.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    gate = rsr.gate_check(
        record_path=path, expected_identity=EXPECTED, project_root=tmp_path,
        profile_document=profile, discovery_document=discovery,
    )
    assert gate["start_allowed"] is True


# ---------------------------------------------------------------- I-2：単調性


def _decision(tmp_path, *, version, decided_at, supersedes=None):
    document = {
        "decision_id": "DEC-IC-SAMPLE-001",
        "decision_version": version,
        "decided_at": decided_at,
        "supersedes": supersedes,
    }
    return document


def test_l8_successor_decision_may_not_move_backwards_in_time():
    """反証I-2の部分処置：後継decisionの決定時刻は前版より前へ戻れない。"""

    previous = {"decision_id": "DEC-IC-SAMPLE-001", "decision_version": 1,
                "decided_at": "2026-08-07T10:00:00+09:00"}
    successor = {"decision_id": "DEC-IC-SAMPLE-001", "decision_version": 2,
                 "decided_at": "2026-08-06T10:00:00+09:00"}
    with pytest.raises(intake.IntakeError):
        intake.check_decision_time_monotonicity(
            successor=successor, previous=previous
        )


def test_l9_forward_moving_successor_is_accepted():
    previous = {"decision_id": "DEC-IC-SAMPLE-001", "decision_version": 1,
                "decided_at": "2026-08-07T10:00:00+09:00"}
    successor = {"decision_id": "DEC-IC-SAMPLE-001", "decision_version": 2,
                 "decided_at": "2026-08-07T11:00:00+09:00"}
    assert intake.check_decision_time_monotonicity(
        successor=successor, previous=previous
    ) is True
