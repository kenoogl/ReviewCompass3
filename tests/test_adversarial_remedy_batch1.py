"""反証レビュー第1束の処置：型1・型2の8件を拒否テストとして固定する。

承認：DEC-ADVERSARIAL-REMEDY-BATCH1-001
所見：records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md
"""

import json
from pathlib import Path

import pytest

from tools.development import candidate_ranking as cr
from tools.development import declaration_red_map_check as drmc
from tools.development import integration_exclusions as ix
from tools.development import reuse_search_record as rsr


P, D, S = "a" * 64, "b" * 64, "c" * 64
EXPECTED = {"profile_run_id": P, "discovery_run_id": D, "source_content_id": S}


def _env(tmp_path):
    src = tmp_path / "tools/pkg/existing.py"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text("def helper():\n    pass\n", encoding="utf-8")
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
    declaration = {"subject": "remedy", "target_paths": ["tools/pkg/"],
                   "target_symbols": ["helper"]}
    observation = {"snapshot_id": "9" * 64, "source_content_id": S,
                   "files": [{"path": "tools/pkg/existing.py",
                              "file_sha256": rsr.file_sha256(src)}]}
    record = rsr.search_existing_routines(
        profile_document=profile, discovery_document=discovery,
        declaration=declaration, observation_document=observation,
        project_root=tmp_path,
    )
    return record


def _rewrite(tmp_path, record):
    path = tmp_path / "search.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_r2_narrowed_freshness_scope_is_rejected(tmp_path):
    record = _env(tmp_path)
    record["freshness"]["target_paths"] = ["tools/nonexistent/"]
    record["content_digest"] = rsr._content_digest(record)
    path = _rewrite(tmp_path, record)
    gate = rsr.gate_check(
        record_path=path, expected_identity=EXPECTED, project_root=tmp_path
    )
    assert gate["start_allowed"] is False
    assert "scope" in gate["reason"]


def test_r4_scope_disagreement_between_declaration_and_freshness_is_rejected(tmp_path):
    record = _env(tmp_path)
    record["freshness"]["target_paths"] = ["tools/pkg/existing.py"]
    record["content_digest"] = rsr._content_digest(record)
    path = _rewrite(tmp_path, record)
    gate = rsr.gate_check(
        record_path=path, expected_identity=EXPECTED, project_root=tmp_path
    )
    assert gate["start_allowed"] is False
    assert "scope" in gate["reason"]


def _externalize(tmp_path, record):
    data_root = tmp_path / "data"
    attestation_path = tmp_path / "attestation.json"
    rsr.externalize_reuse_search_record(
        record=record, data_root=data_root, attestation_path=attestation_path
    )
    return data_root, attestation_path


def test_r5_tampered_attestation_field_is_rejected(tmp_path):
    record = _env(tmp_path)
    data_root, attestation_path = _externalize(tmp_path, record)
    document = json.loads(attestation_path.read_text(encoding="utf-8"))
    document["hit_count"] = 9999
    document["content_digest"] = rsr._content_digest(document)
    attestation_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    gate = rsr.gate_check_attested(
        attestation_path=attestation_path, data_root=data_root,
        expected_identity=EXPECTED, project_root=tmp_path,
    )
    assert gate["start_allowed"] is False
    assert gate["reason"] == "attestation_mismatch"


def test_r6_attestation_identity_swap_is_rejected(tmp_path):
    record = _env(tmp_path)
    data_root, attestation_path = _externalize(tmp_path, record)
    document = json.loads(attestation_path.read_text(encoding="utf-8"))
    document["source_identity"]["profile_run_id"] = "e" * 64
    document["content_digest"] = rsr._content_digest(document)
    attestation_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    gate = rsr.gate_check_attested(
        attestation_path=attestation_path, data_root=data_root,
        expected_identity=EXPECTED, project_root=tmp_path,
    )
    assert gate["start_allowed"] is False
    assert gate["reason"] == "attestation_mismatch"


def _map_env(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_sample.py").write_text(
        "def test_a():\n    pass\n\n\ndef test_orphan():\n    pass\n", encoding="utf-8"
    )


def test_c1_listing_and_declarations_must_agree_in_both_directions(tmp_path):
    """C-1の部分修正：欄と宣言の双方向一致を要求する。

    欄からも宣言からも漏れた実在testの検出（反証C-1の完全な解消）は、
    部分列挙の対応表と衝突するため設計判断へ送った。限界は
    `records/development/2026-08-07-adversarial-remedy-batch1-green-evidence-v1.md`
    に記録する。
    """
    _map_env(tmp_path)
    document = {
        "record_kind": "declaration_red_map", "map_id": "M", "map_version": 1,
        "test_files": {"tests/test_sample.py": ["test_a", "test_orphan"]},
        "declarations": {"P1": {"summary": "s", "tests": [
            {"test": "tests/test_sample.py::test_a", "red_now": True}],
            "red_now": True}},
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert result["machine_count"]["tests_unmapped_to_declarations"] == 1
    assert any("test_orphan" in finding for finding in result["findings"])

    reversed_document = {
        "record_kind": "declaration_red_map", "map_id": "M", "map_version": 1,
        "test_files": {"tests/test_sample.py": ["test_a"]},
        "declarations": {"P1": {"summary": "s", "tests": [
            {"test": "tests/test_sample.py::test_a", "red_now": True},
            {"test": "tests/test_sample.py::test_orphan", "red_now": True}],
            "red_now": True}},
    }
    reversed_path = tmp_path / "map_reversed.json"
    reversed_path.write_text(
        json.dumps(reversed_document, ensure_ascii=False), encoding="utf-8"
    )
    reversed_result = drmc.check_declaration_red_map(
        map_path=reversed_path, project_root=tmp_path
    )
    assert reversed_result["status"] == "failed"
    assert any(
        "test_missing_from_listing" in finding
        for finding in reversed_result["findings"]
    )


def test_c3_sharing_one_test_across_declarations_is_rejected(tmp_path):
    _map_env(tmp_path)
    shared = [{"test": "tests/test_sample.py::test_a", "red_now": True}]
    document = {
        "record_kind": "declaration_red_map", "map_id": "M", "map_version": 1,
        "test_files": {"tests/test_sample.py": ["test_a", "test_orphan"]},
        "declarations": {
            "P1": {"summary": "s", "tests": shared, "red_now": True},
            "P2": {"summary": "s", "tests": shared, "red_now": True},
        },
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    result = drmc.check_declaration_red_map(map_path=path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert any("shared_test" in finding for finding in result["findings"])


def _approval(tmp_path):
    approval = tmp_path / "records" / "approval.md"
    approval.parent.mkdir(parents=True, exist_ok=True)
    approval.write_text("# approval\n", encoding="utf-8")
    return approval


def _exclusions(tmp_path, *, authority_refs=None, targets=None):
    approval = _approval(tmp_path)
    record = {
        "record_kind": "integration_exclusions", "schema_version": 1,
        "exclusion_id": "X", "exclusion_version": 1,
        "created_at": "2026-08-07T00:00:00+09:00",
        "approval": {"decision_id": "DEC-X", "path": "records/approval.md",
                     "sha256": ix.file_sha256(approval)},
        "entries": [{
            "entry_id": "E1", "reason_kind": "frozen_lane",
            "targets": targets or [{"kind": "module_path",
                                    "value": "tools/pkg/frozen.py"}],
            "rationale": "r",
            "authority_refs": authority_refs if authority_refs is not None else [
                {"decision_id": "DEC-X", "path": "records/approval.md"}
            ],
        }],
    }
    record["content_digest"] = ix.content_digest(record)
    return record


def test_x1_unresolvable_authority_reference_is_rejected(tmp_path):
    record = _exclusions(
        tmp_path, authority_refs=[{"decision_id": "DEC-NONEXISTENT-999",
                                   "path": "records/absent.md"}]
    )
    with pytest.raises(ix.IntegrationExclusionError):
        ix.validate_integration_exclusions(record, project_root=tmp_path)


def test_x1_authority_reference_without_a_path_is_rejected(tmp_path):
    record = _exclusions(tmp_path, authority_refs=[{"decision_id": "DEC-X"}])
    with pytest.raises(ix.IntegrationExclusionError):
        ix.validate_integration_exclusions(record, project_root=tmp_path)


def test_g1_ranking_rejects_an_invalid_exclusions_record(tmp_path):
    (tmp_path / "tools/pkg").mkdir(parents=True, exist_ok=True)
    source = tmp_path / "tools/pkg/a.py"
    source.write_text("def a():\n    pass\n", encoding="utf-8")
    record = _exclusions(tmp_path)
    record["entries"][0]["rationale"] = "tampered without digest update"
    profile = {
        "run_id": P, "source_content_id": S, "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [{
            "symbol_id": "tools/pkg/a.py:a",
            "code_reference": {"relative_path": "tools/pkg/a.py",
                               "start_line": 1, "end_line": 2},
            "signature": "()", "structure_digest": "d" * 64,
            "direct_callee_symbol_ids": [], "direct_caller_symbol_ids": [],
        }],
    }
    discovery = {
        "run_id": D, "source_content_id": S, "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [{"group_id": "G1", "basis_kind": "structural_exact_match",
                    "member_symbol_ids": ["tools/pkg/a.py:a"]}],
    }
    observation = {"snapshot_id": "9" * 64, "source_content_id": S,
                   "files": [{"path": "tools/pkg/a.py",
                              "file_sha256": cr.file_sha256(source)}]}
    with pytest.raises(cr.CandidateRankingError):
        cr.build_candidate_ranking(
            profile_document=profile, discovery_document=discovery,
            exclusions_record=record, observation_document=observation,
            project_root=tmp_path, guard_module_paths=[], changed_paths=[],
            created_at="2026-08-07T00:00:00+09:00",
        )
