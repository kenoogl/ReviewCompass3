"""構成B：再利用検索の鮮度判定（宣言F1〜F4）を固定するTest。

承認：DEC-WORK4B-MAIN-DESIGN-BUNDLE-001 §3（閾値：対象範囲のfileに観測後の変更が
1件でもあれば停止）
"""

import json
from pathlib import Path

from tools.development import reuse_search_record as rsr


PROFILE_RUN_ID = "a" * 64
DISCOVERY_RUN_ID = "b" * 64
SOURCE_CONTENT_ID = "c" * 64
SNAPSHOT_ID = "9" * 64


def _write_source(tmp_path, relative, body):
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    return target


def _fixture_profile():
    return {
        "run_id": PROFILE_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [
            {
                "symbol_id": "tools/pkg/existing.py:helper",
                "code_reference": {
                    "relative_path": "tools/pkg/existing.py",
                    "start_line": 1,
                    "end_line": 2,
                },
                "signature": "()",
                "structure_digest": "d" * 64,
                "direct_callee_symbol_ids": [],
                "direct_caller_symbol_ids": [],
            }
        ],
    }


def _fixture_discovery():
    return {
        "run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [],
    }


def _observation(tmp_path, files):
    return {
        "snapshot_id": SNAPSHOT_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "files": [
            {"path": relative, "file_sha256": rsr.file_sha256(tmp_path / relative)}
            for relative in files
        ],
    }


def _declaration():
    return {
        "subject": "work4b-b/fixture-subject",
        "target_paths": ["tools/pkg/"],
        "target_symbols": ["helper"],
    }


def _expected_identity():
    return {
        "profile_run_id": PROFILE_RUN_ID,
        "discovery_run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
    }


def _search(tmp_path, observation):
    return rsr.search_existing_routines(
        profile_document=_fixture_profile(),
        discovery_document=_fixture_discovery(),
        declaration=_declaration(),
        observation_document=observation,
        project_root=tmp_path,
    )


def test_f1_record_carries_machine_assessed_freshness(tmp_path):
    _write_source(tmp_path, "tools/pkg/existing.py", "def helper():\n    pass\n")
    observation = _observation(tmp_path, ["tools/pkg/existing.py"])
    record = _search(tmp_path, observation)
    freshness = record["freshness"]
    assert record["schema_version"] == 2
    assert freshness["assessed"] is True
    assert freshness["observation_snapshot_id"] == SNAPSHOT_ID
    assert freshness["stale"] is False
    assert freshness["changed_files"] == []
    assert freshness["new_files"] == []
    assert rsr.validate_reuse_search_record(
        record, expected_identity=_expected_identity()
    )


def test_f2_gate_stops_when_an_observed_file_changed(tmp_path):
    source = _write_source(
        tmp_path, "tools/pkg/existing.py", "def helper():\n    pass\n"
    )
    observation = _observation(tmp_path, ["tools/pkg/existing.py"])
    record = _search(tmp_path, observation)
    target = tmp_path / "search-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)

    source.write_text("def helper():\n    return 1\n", encoding="utf-8")
    gate = rsr.gate_check(
        record_path=target,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert gate["start_allowed"] is False
    assert gate["reason"] == "profile_stale"
    assert "tools/pkg/existing.py" in gate["stale_files"]


def test_f3_gate_stops_when_a_new_file_appears_in_range(tmp_path):
    _write_source(tmp_path, "tools/pkg/existing.py", "def helper():\n    pass\n")
    observation = _observation(tmp_path, ["tools/pkg/existing.py"])
    record = _search(tmp_path, observation)
    target = tmp_path / "search-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)

    _write_source(tmp_path, "tools/pkg/brand_new.py", "def unseen():\n    pass\n")
    gate = rsr.gate_check(
        record_path=target,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert gate["start_allowed"] is False
    assert gate["reason"] == "profile_stale"
    assert "tools/pkg/brand_new.py" in gate["stale_files"]


def test_f4_gate_allows_when_range_is_unchanged_and_v1_records_keep_validating(tmp_path):
    _write_source(tmp_path, "tools/pkg/existing.py", "def helper():\n    pass\n")
    observation = _observation(tmp_path, ["tools/pkg/existing.py"])
    record = _search(tmp_path, observation)
    target = tmp_path / "search-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)
    gate = rsr.gate_check(
        record_path=target,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert gate["start_allowed"] is True

    legacy = rsr.search_existing_routines(
        profile_document=_fixture_profile(),
        discovery_document=_fixture_discovery(),
        declaration=_declaration(),
    )
    assert legacy["schema_version"] == 1
    assert "freshness" not in legacy
    assert rsr.validate_reuse_search_record(
        legacy, expected_identity=_expected_identity()
    )
    legacy_path = tmp_path / "legacy-v1.json"
    rsr.write_reuse_search_record(path=legacy_path, record=legacy)
    legacy_gate = rsr.gate_check(
        record_path=legacy_path,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert legacy_gate["start_allowed"] is True
    assert legacy_gate["freshness"] == "not_assessed"
