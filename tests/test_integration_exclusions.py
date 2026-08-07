"""構成A-1：統合除外宣言の宣言X1〜X4を固定するTest。

承認：DEC-INTEGRATION-EXCLUSION-ENTRIES-001（entry 3件）、
DEC-WORK4B-MAIN-DESIGN-BUNDLE-001（構成A-1）
"""

import json
from pathlib import Path

import pytest

from tools.development import integration_exclusions as ix


def _fixture_record(tmp_path):
    approval = tmp_path / "records" / "approval-decision.md"
    approval.parent.mkdir(parents=True, exist_ok=True)
    approval.write_text("# approval\n", encoding="utf-8")
    record = {
        "record_kind": "integration_exclusions",
        "schema_version": 1,
        "exclusion_id": "RC3-INTEGRATION-EXCLUSIONS-001",
        "exclusion_version": 1,
        "created_at": "2026-08-07T12:57:15+09:00",
        "approval": {
            "decision_id": "DEC-INTEGRATION-EXCLUSION-ENTRIES-001",
            "path": "records/approval-decision.md",
            "sha256": ix.file_sha256(approval),
        },
        "entries": [
            {
                "entry_id": "E1",
                "reason_kind": "frozen_lane",
                "targets": [
                    {
                        "kind": "symbol_prefix",
                        "value": "tools/development/issue_resolution_pilot.py:validate_implementation_task_contract_v2",
                    }
                ],
                "rationale": "旧Pilot記録は旧規則のまま保持し、新規則で再判定しない",
                "authority_refs": [
                    {
                        "decision_id": "DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001",
                        "path": "records/approval-decision.md",
                    }
                ],
            },
            {
                "entry_id": "E3",
                "reason_kind": "historical_retained",
                "targets": [
                    {
                        "kind": "module_path",
                        "value": "tools/requirements/unified_migration.py",
                    }
                ],
                "rationale": "一回性の移行器を歴史として保持する",
                "authority_refs": [
                    {
                        "decision_id": "DEC-INTEGRATION-EXCLUSION-ENTRIES-001",
                        "path": "records/approval-decision.md",
                    }
                ],
            },
        ],
    }
    record["content_digest"] = ix.content_digest(record)
    return record


def test_x1_valid_record_validates(tmp_path):
    record = _fixture_record(tmp_path)
    assert ix.validate_integration_exclusions(record, project_root=tmp_path)


def test_x1_rejects_unknown_reason_kind(tmp_path):
    record = _fixture_record(tmp_path)
    record["entries"][0]["reason_kind"] = "just_because"
    record["content_digest"] = ix.content_digest(record)
    with pytest.raises(ix.IntegrationExclusionError):
        ix.validate_integration_exclusions(record, project_root=tmp_path)


def test_x2_rejects_missing_approval_and_refuses_overwrite(tmp_path):
    record = _fixture_record(tmp_path)
    unapproved = json.loads(json.dumps(record))
    del unapproved["approval"]
    with pytest.raises(ix.IntegrationExclusionError):
        ix.validate_integration_exclusions(unapproved, project_root=tmp_path)

    target = tmp_path / "integration-exclusions-001--v1.json"
    ix.write_integration_exclusions(path=target, record=record)
    with pytest.raises(ix.IntegrationExclusionError):
        ix.write_integration_exclusions(path=target, record=record)
    assert json.loads(target.read_text(encoding="utf-8")) == record


def test_x3_symbol_matching_is_deterministic(tmp_path):
    record = _fixture_record(tmp_path)
    hit = ix.excluded_entry_ids(
        "tools/development/issue_resolution_pilot.py:validate_implementation_task_contract_v2",
        record=record,
    )
    assert hit == ["E1"]
    module_hit = ix.excluded_entry_ids(
        "tools/requirements/unified_migration.py:check_migration_plan",
        record=record,
    )
    assert module_hit == ["E3"]
    miss = ix.excluded_entry_ids(
        "tools/development/issue_resolution_pilot.py:validate_candidate",
        record=record,
    )
    assert miss == []
    again = ix.excluded_entry_ids(
        "tools/development/issue_resolution_pilot.py:validate_implementation_task_contract_v2",
        record=record,
    )
    assert again == hit


def test_x4_load_fails_closed_on_missing_or_invalid_file(tmp_path):
    with pytest.raises(ix.IntegrationExclusionError):
        ix.load_integration_exclusions(
            path=tmp_path / "absent.json", project_root=tmp_path
        )
    broken = tmp_path / "broken.json"
    broken.write_text("not json", encoding="utf-8")
    with pytest.raises(ix.IntegrationExclusionError):
        ix.load_integration_exclusions(path=broken, project_root=tmp_path)
