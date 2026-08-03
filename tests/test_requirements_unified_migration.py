"""Legacy 37 Requirementの単一definition形式への機械移行Test。"""

import copy
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_IDS = {
    requirement_id
    for binding in json.loads(
        (
            PROJECT_ROOT
            / "records/requirements/authority/rc3-legacy-requirements-37--v1.json"
        ).read_text()
    )["legacy_authority_bindings"]
    for requirement_id in binding["requirement_ids"]
}


@pytest.fixture
def migration():
    return importlib.import_module(
        "tools.requirements.unified_migration"
    )


def test_builds_deterministic_37_definitions_and_unified_50_candidate(
    migration,
):
    first = migration.build_migration_plan(PROJECT_ROOT)
    second = migration.build_migration_plan(PROJECT_ROOT)

    assert first == second
    assert len(first.definitions) == 37
    assert {item["requirement_id"] for item in first.definitions} == LEGACY_IDS
    assert all(item["acceptance_truth_changed"] is False for item in first.definitions)
    assert all(len(item["source_refs"]) == 4 for item in first.definitions)
    assert len(first.candidate["definition_refs"]) == 50
    assert len({
        ref["logical_id"]
        for ref in first.candidate["definition_refs"]
    }) == 50
    assert first.candidate["candidate_id"] == (
        "RC3-REQUIREMENTS-UNIFIED-50-2026-08-03-V1"
    )


def test_migration_preserves_every_legacy_semantic_field(migration):
    plan = migration.build_migration_plan(PROJECT_ROOT)
    original = migration.load_legacy_requirements(PROJECT_ROOT)
    migrated = {
        item["requirement_id"]: item
        for item in plan.definitions
    }

    for requirement_id, source in original.items():
        target = migrated[requirement_id]
        for field in (
            "feature_id",
            "statement",
            "inputs",
            "outputs",
            "stop_conditions",
            "recovery_conditions",
            "preserved_artifacts",
            "acceptance_criteria",
            "non_goals",
        ):
            assert target[field] == source[field]


def test_migration_rejects_missing_semantic_field(migration):
    requirement = copy.deepcopy(
        next(iter(migration.load_legacy_requirements(PROJECT_ROOT).values()))
    )
    requirement.pop("acceptance_criteria")

    with pytest.raises(
        migration.RequirementMigrationError,
        match="migration_incomplete",
    ):
        migration.build_definition(
            requirement,
            source_refs=[{
                "logical_id": "SOURCE",
                "version": 1,
                "path": "source.json",
                "sha256": "0" * 64,
            }],
        )


def test_migration_writer_is_idempotent_and_rejects_conflicting_output(
    migration,
    tmp_path,
):
    plan = migration.build_migration_plan(PROJECT_ROOT)

    first = migration.write_migration_plan(plan, tmp_path)
    second = migration.write_migration_plan(plan, tmp_path)

    assert first.written_count == 38
    assert second.written_count == 0
    assert second.unchanged_count == 38

    target = (
        tmp_path
        / "records/requirements/definitions/req-context-001--v1.json"
    )
    target.write_text("{}\n")
    with pytest.raises(
        migration.RequirementMigrationError,
        match="conflicting_output",
    ):
        migration.write_migration_plan(plan, tmp_path)
