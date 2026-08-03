"""統一50 Requirement候補の機械Evidence生成Test。"""

import importlib
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def migration():
    return importlib.import_module(
        "tools.requirements.unified_migration"
    )


def _receipt(status="passed", fallback_used=False):
    return {
        "receipt_kind": "policy_test_verification_run",
        "runner_id": "RC3-DEVELOPMENT-TEST-RUNNER",
        "runner_version": 1,
        "command": "python3 -m pytest -q",
        "python_version": "3.9.6",
        "pytest_version": "8.4.2",
        "fallback_used": fallback_used,
        "config_digest": "1" * 64,
        "source_state_digest": "2" * 64,
        "status": status,
        "exit_code": 0 if status == "passed" else 1,
    }


def test_builds_schema_valid_evidence_for_candidate_and_all_50_definitions(
    migration,
):
    plan = migration.build_migration_plan(PROJECT_ROOT)

    evidence = migration.build_evidence_record(
        plan,
        receipt=_receipt(),
        receipt_ref={
            "logical_id": "RC3-POLICY-TEST-RECEIPT-WORK3-V1",
            "version": 1,
            "path": "records/development/test-receipt.json",
            "sha256": "3" * 64,
        },
        recorded_at="2026-08-03T21:30:00+09:00",
    )

    assert evidence["result"] == "passed"
    assert len(evidence["subject_refs"]) == 51
    assert {
        reference["logical_id"]
        for reference in plan.candidate["definition_refs"]
    } <= {
        reference["logical_id"]
        for reference in evidence["subject_refs"]
    }
    assert evidence["source_refs"][-1]["logical_id"] == (
        "RC3-POLICY-TEST-RECEIPT-WORK3-V1"
    )
    migration.validate_evidence_record(PROJECT_ROOT, evidence)


@pytest.mark.parametrize(
    "receipt",
    (
        _receipt(status="failed"),
        _receipt(fallback_used=True),
    ),
)
def test_rejects_failed_or_fallback_test_receipt(migration, receipt):
    plan = migration.build_migration_plan(PROJECT_ROOT)

    with pytest.raises(
        migration.RequirementMigrationError,
        match="verification_receipt_rejected",
    ):
        migration.build_evidence_record(
            plan,
            receipt=receipt,
            receipt_ref={
                "logical_id": "RC3-POLICY-TEST-RECEIPT-WORK3-V1",
                "version": 1,
                "path": "records/development/test-receipt.json",
                "sha256": "3" * 64,
            },
            recorded_at="2026-08-03T21:30:00+09:00",
        )
