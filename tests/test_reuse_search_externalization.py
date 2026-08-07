"""構成C：検索recordの外部化（証明書方式）の宣言H1〜H4を固定するTest。

承認：DEC-WORK4B-MAIN-DESIGN-BUNDLE-001 §4（外部DATA_ROOT＋証明書、fail-closed、
byte一致移行、旧位置保持）
"""

import json
from pathlib import Path

import pytest

from tools.development import reuse_search_record as rsr


PROFILE_RUN_ID = "a" * 64
DISCOVERY_RUN_ID = "b" * 64
SOURCE_CONTENT_ID = "c" * 64


def _fixture_record():
    profile = {
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
    discovery = {
        "run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
        "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [],
    }
    declaration = {
        "subject": "work4b-c/fixture-subject",
        "target_paths": ["tools/pkg/"],
        "target_symbols": ["helper"],
    }
    return rsr.search_existing_routines(
        profile_document=profile,
        discovery_document=discovery,
        declaration=declaration,
    )


def _expected_identity():
    return {
        "profile_run_id": PROFILE_RUN_ID,
        "discovery_run_id": DISCOVERY_RUN_ID,
        "source_content_id": SOURCE_CONTENT_ID,
    }


def test_h1_externalize_writes_body_and_attestation_new_only(tmp_path):
    record = _fixture_record()
    data_root = tmp_path / "data"
    attestation_path = tmp_path / "attestation-v1.json"
    attestation = rsr.externalize_reuse_search_record(
        record=record, data_root=data_root, attestation_path=attestation_path
    )
    external = data_root / "work4b" / "reuse-searches" / (
        record["content_digest"] + ".json"
    )
    assert external.is_file()
    assert json.loads(external.read_text(encoding="utf-8")) == record
    stored = json.loads(attestation_path.read_text(encoding="utf-8"))
    assert stored == attestation
    assert stored["record_kind"] == "reuse_search_attestation"
    assert stored["external"]["relative_path"] == (
        f"work4b/reuse-searches/{record['content_digest']}.json"
    )
    assert stored["external"]["content_digest"] == record["content_digest"]
    assert stored["external"]["byte_sha256"] == rsr.file_sha256(external)
    assert stored["source_identity"] == record["source_identity"]
    with pytest.raises(rsr.ReuseSearchError):
        rsr.externalize_reuse_search_record(
            record=record, data_root=data_root, attestation_path=attestation_path
        )


def test_h2_attested_gate_allows_valid_external_record(tmp_path):
    record = _fixture_record()
    data_root = tmp_path / "data"
    attestation_path = tmp_path / "attestation-v1.json"
    rsr.externalize_reuse_search_record(
        record=record, data_root=data_root, attestation_path=attestation_path
    )
    gate = rsr.gate_check_attested(
        attestation_path=attestation_path,
        data_root=data_root,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert gate["start_allowed"] is True


def test_h3_attested_gate_fails_closed_on_missing_or_tampered_body(tmp_path):
    record = _fixture_record()
    data_root = tmp_path / "data"
    attestation_path = tmp_path / "attestation-v1.json"
    rsr.externalize_reuse_search_record(
        record=record, data_root=data_root, attestation_path=attestation_path
    )
    external = data_root / "work4b" / "reuse-searches" / (
        record["content_digest"] + ".json"
    )
    original_bytes = external.read_bytes()

    external.unlink()
    missing = rsr.gate_check_attested(
        attestation_path=attestation_path,
        data_root=data_root,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert missing["start_allowed"] is False
    assert missing["reason"] == "record_unavailable"

    external.write_bytes(original_bytes.replace(b"helper", b"hacked"))
    tampered = rsr.gate_check_attested(
        attestation_path=attestation_path,
        data_root=data_root,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert tampered["start_allowed"] is False
    assert tampered["reason"] == "record_unavailable"


def test_h4_migration_is_byte_identical_and_keeps_the_original(tmp_path):
    record = _fixture_record()
    original_path = tmp_path / "records" / "legacy-reuse-search-v1.json"
    original_path.parent.mkdir(parents=True, exist_ok=True)
    rsr.write_reuse_search_record(path=original_path, record=record)
    original_bytes = original_path.read_bytes()

    data_root = tmp_path / "data"
    attestation_path = tmp_path / "attestation-v1.json"
    result = rsr.migrate_reuse_search_record(
        record_path=original_path,
        data_root=data_root,
        attestation_path=attestation_path,
    )
    external = data_root / "work4b" / "reuse-searches" / (
        record["content_digest"] + ".json"
    )
    assert external.read_bytes() == original_bytes
    assert original_path.read_bytes() == original_bytes
    assert result["byte_identical"] is True
    gate = rsr.gate_check_attested(
        attestation_path=attestation_path,
        data_root=data_root,
        expected_identity=_expected_identity(),
        project_root=tmp_path,
    )
    assert gate["start_allowed"] is True
