"""Work 1A Layout Baselineの受入テスト。"""

import importlib
import json
from pathlib import Path
import shutil

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BASELINE_RECORD = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-03-layout-baseline-v1.json"
)
EMPTY_PROJECT = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "layout"
    / "empty-project"
)
LOGICAL_ROOTS = {
    "code_root",
    "config_root",
    "project_root",
    "data_root",
    "state_root",
    "log_root",
    "cache_root",
    "sensitive_root",
    "evaluation_root",
}


def _layout():
    return importlib.import_module("tools.layout.baseline")


def _defaults(tmp_path, role):
    base = tmp_path / "defaults" / role
    return {
        "code_root": base / "code",
        "config_root": base / "config",
        "data_root": base / "data",
        "state_root": base / "state",
        "log_root": base / "log",
        "cache_root": base / "cache",
        "sensitive_root": base / "sensitive",
        "evaluation_root": base / "evaluation",
    }


def test_baseline_record_fixes_roots_boundaries_and_migration_policy():
    layout = _layout()

    baseline = layout.load_layout_baseline(BASELINE_RECORD)

    assert set(baseline["logical_roots"]) == LOGICAL_ROOTS
    assert baseline["resolution_precedence"] == [
        "explicit_cli",
        "versioned_user_setting",
        "allowlisted_environment",
        "os_standard",
    ]
    assert baseline["git_boundary"] == {
        "managed_root": "project_root",
        "external_roots": sorted(LOGICAL_ROOTS - {"project_root"}),
    }
    assert baseline["relative_path_policy"] == {
        "allowed_for": "project_artifacts_only",
        "base_root": "project_root",
        "escape": "reject",
    }
    assert baseline["environment_isolation"]["cross_write"] == "reject"
    assert baseline["environment_isolation"]["shared_root"] == (
        "project_root_read_only_for_stable"
    )
    assert baseline["migration_policy"]["required_fields"] == [
        "from_version",
        "to_version",
        "affected_roots",
        "impact_closure",
        "link_check",
        "data_migration",
        "dry_run",
        "rollback",
    ]


def test_root_resolution_uses_fixed_precedence_and_absolute_runtime_paths(
    tmp_path,
):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_RECORD)
    project = tmp_path / "project"
    project.mkdir()

    resolution = layout.resolve_layout(
        baseline,
        environment_role="development",
        project_root=project,
        defaults=_defaults(tmp_path, "development"),
        environment={
            "REVIEWCOMPASS3_LOG_ROOT": str(tmp_path / "environment-log"),
        },
        user_settings={
            "state_root": str(tmp_path / "settings-state"),
        },
        overrides={
            "data_root": str(tmp_path / "explicit-data"),
        },
    )

    assert resolution.roots["project_root"] == project.resolve()
    assert resolution.roots["data_root"] == (
        tmp_path / "explicit-data"
    ).resolve()
    assert resolution.roots["state_root"] == (
        tmp_path / "settings-state"
    ).resolve()
    assert resolution.roots["log_root"] == (
        tmp_path / "environment-log"
    ).resolve()
    assert resolution.roots["cache_root"] == (
        tmp_path / "defaults" / "development" / "cache"
    ).resolve()

    with pytest.raises(layout.LayoutError, match="absolute"):
        layout.resolve_layout(
            baseline,
            environment_role="development",
            project_root=project,
            defaults=_defaults(tmp_path, "development"),
            overrides={"data_root": "relative/data"},
        )


def test_stable_and_development_roots_are_isolated_and_cross_write_fails(
    tmp_path,
):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_RECORD)
    project = tmp_path / "project"
    project.mkdir()
    stable = layout.resolve_layout(
        baseline,
        environment_role="stable",
        project_root=project,
        defaults=_defaults(tmp_path, "stable"),
    )
    development = layout.resolve_layout(
        baseline,
        environment_role="development",
        project_root=project,
        defaults=_defaults(tmp_path, "development"),
    )

    layout.validate_environment_isolation(stable, development)

    with pytest.raises(layout.LayoutError, match="cross-environment"):
        layout.validate_write_target(
            stable,
            development.roots["data_root"] / "runs" / "run-001.json",
        )

    overlapping = layout.resolve_layout(
        baseline,
        environment_role="development",
        project_root=project,
        defaults=_defaults(tmp_path, "development"),
        overrides={"data_root": str(stable.roots["data_root"])},
    )
    with pytest.raises(layout.LayoutError, match="overlap"):
        layout.validate_environment_isolation(stable, overlapping)


def test_empty_project_binding_survives_checkout_move(tmp_path):
    layout = _layout()
    first_checkout = tmp_path / "checkout-a"
    second_checkout = tmp_path / "moved" / "checkout-b"
    shutil.copytree(EMPTY_PROJECT, first_checkout)

    first = layout.validate_project_layout(
        first_checkout,
        binding_id="binding-a",
        checkout_id="checkout-a",
        captured_at="2026-08-03T00:00:00+09:00",
    )
    second_checkout.parent.mkdir()
    shutil.move(first_checkout, second_checkout)
    second = layout.validate_project_layout(
        second_checkout,
        binding_id="binding-b",
        checkout_id="checkout-b",
        captured_at="2026-08-03T00:01:00+09:00",
    )

    assert first.project_id == second.project_id == "rc3-fixture-empty-project"
    assert first.project_manifest_digest == second.project_manifest_digest
    assert first.binding_id != second.binding_id
    assert first.repository_root != second.repository_root
    assert second.repository_root == second_checkout.resolve()
    assert second.resolved_document_links == (
        second_checkout.resolve() / "docs" / "layout-entry.md",
    )


def test_binding_rejects_project_identity_mismatch(tmp_path):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_RECORD)
    checkout = tmp_path / "checkout"
    shutil.copytree(EMPTY_PROJECT, checkout)
    binding = layout.validate_project_layout(
        checkout,
        binding_id="binding-a",
        checkout_id="checkout-a",
        captured_at="2026-08-03T00:00:00+09:00",
    )
    mismatched = binding.to_dict()
    assert set(mismatched) == set(
        baseline["project_binding"]["required_fields"]
    )
    mismatched["project_id"] = "different-project"

    with pytest.raises(layout.LayoutError, match="project identity"):
        layout.validate_project_binding(checkout, mismatched)

    relative = binding.to_dict()
    relative["repository_root"] = "relative/checkout"
    with pytest.raises(layout.LayoutError, match="absolute"):
        layout.validate_project_binding(checkout, relative)


def test_managed_fixture_contains_no_terminal_absolute_paths():
    layout = _layout()

    assert layout.find_terminal_absolute_paths(EMPTY_PROJECT) == ()


def test_project_relative_escape_and_incomplete_migration_are_rejected(
    tmp_path,
):
    layout = _layout()
    checkout = tmp_path / "checkout"
    shutil.copytree(EMPTY_PROJECT, checkout)
    manifest_path = checkout / ".reviewcompass" / "project-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["document_links"] = ["../outside.md"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(layout.LayoutError, match="escape"):
        layout.validate_project_layout(
            checkout,
            binding_id="binding-a",
            checkout_id="checkout-a",
            captured_at="2026-08-03T00:00:00+09:00",
        )

    baseline = layout.load_layout_baseline(BASELINE_RECORD)
    with pytest.raises(layout.LayoutError, match="rollback"):
        layout.validate_layout_migration(
            baseline,
            {
                "from_version": 1,
                "to_version": 2,
                "affected_roots": ["data_root"],
                "impact_closure": ["run", "provenance"],
                "link_check": "passed",
                "data_migration": "dry-copy",
                "dry_run": "passed",
            },
        )
