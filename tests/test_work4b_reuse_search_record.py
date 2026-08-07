"""Work 4B最小試行：再利用検索record（reuse_search_record）の宣言R1〜R7を固定するTest。

承認済み範囲提案：docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md §4
承認Decision：DEC-WORK4B-MINIMAL-PILOT-SCOPE-001
"""

import json
from pathlib import Path

import pytest

from tools.development import reuse_search_record as rsr


PROFILE_RUN_ID = "a" * 64
DISCOVERY_RUN_ID = "b" * 64
SOURCE_CONTENT_ID = "c" * 64


def _fixture_profile():
    return {
        "run_id": PROFILE_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [
            {
                "symbol_id": "tools/development/example_a.py:build_record",
                "code_reference": {
                    "relative_path": "tools/development/example_a.py",
                    "start_line": 10,
                    "end_line": 30,
                },
                "signature": "(subject, source)",
                "structure_digest": "d" * 64,
                "direct_callee_symbol_ids": [
                    "tools/development/example_b.py:canonical_digest"
                ],
                "direct_caller_symbol_ids": [],
            },
            {
                "symbol_id": "tools/development/example_b.py:canonical_digest",
                "code_reference": {
                    "relative_path": "tools/development/example_b.py",
                    "start_line": 5,
                    "end_line": 12,
                },
                "signature": "(document)",
                "structure_digest": "e" * 64,
                "direct_callee_symbol_ids": [],
                "direct_caller_symbol_ids": [
                    "tools/development/example_a.py:build_record"
                ],
            },
            {
                "symbol_id": "tools/session_logs/unrelated.py:far_away",
                "code_reference": {
                    "relative_path": "tools/session_logs/unrelated.py",
                    "start_line": 1,
                    "end_line": 4,
                },
                "signature": "()",
                "structure_digest": "f" * 64,
                "direct_callee_symbol_ids": [],
                "direct_caller_symbol_ids": [],
            },
        ],
    }


def _fixture_discovery():
    return {
        "run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [
            {
                "group_id": "group-0001",
                "basis_kind": "shared_direct_callee",
                "member_symbol_ids": [
                    "tools/development/example_a.py:build_record",
                    "tools/development/example_b.py:canonical_digest",
                    "tools/session_logs/unrelated.py:far_away",
                ],
            }
        ],
    }


def _declaration():
    return {
        "subject": "work4b-minimal-pilot/reuse-search-record-helper",
        "target_paths": ["tools/development/"],
        "target_symbols": ["reuse_search_record"],
    }


def _expected_identity():
    return {
        "profile_run_id": PROFILE_RUN_ID,
        "discovery_run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
    }


def _search():
    return rsr.search_existing_routines(
        profile_document=_fixture_profile(),
        discovery_document=_fixture_discovery(),
        declaration=_declaration(),
    )


def test_r1_record_binds_work4a_identity():
    record = _search()
    identity = record["source_identity"]
    assert identity["profile_run_id"] == PROFILE_RUN_ID
    assert identity["discovery_run_id"] == DISCOVERY_RUN_ID
    assert identity["source_content_id"] == SOURCE_CONTENT_ID
    assert rsr.validate_reuse_search_record(
        record, expected_identity=_expected_identity()
    )


def test_r1_validator_rejects_missing_or_mismatched_identity():
    record = _search()
    tampered = json.loads(json.dumps(record))
    tampered["source_identity"]["profile_run_id"] = "9" * 64
    with pytest.raises(rsr.ReuseSearchError):
        rsr.validate_reuse_search_record(
            tampered, expected_identity=_expected_identity()
        )
    incomplete = json.loads(json.dumps(record))
    del incomplete["source_identity"]["discovery_run_id"]
    with pytest.raises(rsr.ReuseSearchError):
        rsr.validate_reuse_search_record(
            incomplete, expected_identity=_expected_identity()
        )


def test_r2_write_is_new_only_and_refuses_overwrite(tmp_path):
    record = _search()
    target = tmp_path / "reuse-search-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)
    assert target.is_file()
    with pytest.raises(rsr.ReuseSearchError):
        rsr.write_reuse_search_record(path=target, record=record)
    assert json.loads(target.read_text(encoding="utf-8")) == record


def test_r3_same_inputs_yield_identical_content_digest():
    first = _search()
    second = _search()
    assert first["content_digest"] == second["content_digest"]
    assert first == second


def test_r4_zero_hit_record_is_valid_and_distinct_from_absence(tmp_path):
    declaration = {
        "subject": "work4b-minimal-pilot/no-match-subject",
        "target_paths": ["tools/nonexistent_package/"],
        "target_symbols": ["nothing_matches_this_name"],
    }
    record = rsr.search_existing_routines(
        profile_document=_fixture_profile(),
        discovery_document=_fixture_discovery(),
        declaration=declaration,
    )
    assert record["hits"] == []
    assert rsr.validate_reuse_search_record(
        record, expected_identity=_expected_identity()
    )
    target = tmp_path / "zero-hit-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)
    present = rsr.gate_check(
        record_path=target, expected_identity=_expected_identity()
    )
    assert present["start_allowed"] is True
    absent = rsr.gate_check(
        record_path=tmp_path / "never-written.json",
        expected_identity=_expected_identity(),
    )
    assert absent["start_allowed"] is False


def test_r5_validator_rejects_disposition_labels():
    record = _search()
    for label in ("reuse", "extend", "merge", "split", "as_is"):
        labeled = json.loads(json.dumps(record))
        labeled["disposition"] = label
        with pytest.raises(rsr.ReuseSearchError):
            rsr.validate_reuse_search_record(
                labeled, expected_identity=_expected_identity()
            )
    hit_labeled = json.loads(json.dumps(record))
    assert hit_labeled["hits"], "fixture must produce at least one hit"
    hit_labeled["hits"][0]["disposition"] = "merge"
    with pytest.raises(rsr.ReuseSearchError):
        rsr.validate_reuse_search_record(
            hit_labeled, expected_identity=_expected_identity()
        )


def test_r6_group_references_keep_all_members():
    # 設計変更（2026-08-07）：memberの全列は各hitへ複製せず、recordの`groups`欄へ
    # group一件につき一度だけ保持する。実データ測定でhitごとの複製がmember項目を
    # 62,113件（正規化後3,493件の約18倍）へ膨張させたため。R6の趣旨（memberを
    # 上限で切り捨てない）は`groups`欄の全member保持で満たす。
    record = _search()
    group_hits = [
        hit for hit in record["hits"] if hit.get("group_id") == "group-0001"
    ]
    assert group_hits, "target routines belong to group-0001"
    groups_by_id = {group["group_id"]: group for group in record["groups"]}
    for hit in group_hits:
        assert hit["group_id"] in groups_by_id
    assert sorted(groups_by_id["group-0001"]["member_symbol_ids"]) == sorted(
        [
            "tools/development/example_a.py:build_record",
            "tools/development/example_b.py:canonical_digest",
            "tools/session_logs/unrelated.py:far_away",
        ]
    )
    referenced = {
        hit["group_id"] for hit in record["hits"] if hit["group_id"] is not None
    }
    assert referenced <= set(groups_by_id), "every referenced group is present once"


def test_r7_gate_fails_closed_on_missing_record_and_stale_identity(tmp_path):
    record = _search()
    target = tmp_path / "reuse-search-v1.json"
    rsr.write_reuse_search_record(path=target, record=record)

    matching = rsr.gate_check(
        record_path=target, expected_identity=_expected_identity()
    )
    assert matching["start_allowed"] is True

    missing = rsr.gate_check(
        record_path=tmp_path / "absent.json",
        expected_identity=_expected_identity(),
    )
    assert missing["start_allowed"] is False

    stale_identity = dict(_expected_identity(), profile_run_id="1" * 64)
    stale = rsr.gate_check(record_path=target, expected_identity=stale_identity)
    assert stale["start_allowed"] is False
