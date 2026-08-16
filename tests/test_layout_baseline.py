"""Work 1A Layout Baselineの受入テスト。"""

import importlib
import hashlib
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
BASELINE_V2_CANDIDATE = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-04-layout-baseline-v2-candidate.json"
)
EMPTY_PROJECT = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "layout"
    / "empty-project"
)
EMPTY_PROJECT_V2 = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "layout"
    / "empty-project-v2"
)
LAYOUT_V2_APPROVAL = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-04-layout-baseline-v2-approval-decision.json"
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


def test_raw_response_ledger_artifact_is_exempt_from_absolute_scan(tmp_path):
    """送信台帳の未加工応答（外部データ）は絶対path混入検査の対象外である。"""

    layout = _layout()
    managed = tmp_path / "managed"
    ledger = managed / "egress-ledger"
    ledger.mkdir(parents=True)
    external = '{"signature":"/OSkiiNAW3Z/C/6/external-binary-like-data"}'
    (ledger / "ORD-X--response-v1.raw").write_text(external, encoding="utf-8")
    (ledger / "note.txt").write_text("/Users/example/leak", encoding="utf-8")

    findings = layout.find_terminal_absolute_paths(managed)

    assert all("response-v1.raw" not in finding for finding in findings)
    assert any("note.txt" in finding for finding in findings)


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


def test_v2_baseline_fixes_workflow_and_deployment_package_boundary():
    layout = _layout()

    baseline = layout.load_layout_baseline(BASELINE_V2_CANDIDATE)

    assert baseline["schema_version"] == 2
    assert baseline["layout_version"] == 2
    assert baseline["project_artifact_policy"] == {
        "canonical_root_name": "workflow",
        "canonical_project_artifact_move": "prohibited",
        "record_relation_identity": [
            "id",
            "version",
            "digest",
            "relation_kind",
        ],
        "classification_change": "rebuild_projection",
        "semantic_data_migration": "exceptional_human_approved",
    }
    assert baseline["deployment_package_policy"] == {
        "source_selection": "manifest_allowlist",
        "deployment_package_replaceable": True,
        "runtime_projection_rebuildable": True,
        "project_artifact_update_requires_runtime_reinstall": False,
        "prohibited_project_paths": [
            ".reviewcompass/project-manifest.json",
            ".reviewcompass/workflow",
        ],
    }


def test_v2_project_manifest_requires_workflow_root(tmp_path):
    layout = _layout()
    checkout = tmp_path / "checkout"
    shutil.copytree(EMPTY_PROJECT_V2, checkout)

    binding = layout.validate_project_layout(
        checkout,
        binding_id="binding-v2",
        checkout_id="checkout-v2",
        captured_at="2026-08-04T00:00:00+09:00",
    )

    assert binding.project_id == "rc3-fixture-empty-project-v2"
    manifest_path = checkout / ".reviewcompass" / "project-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    del manifest["artifact_roots"]["workflow"]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(layout.LayoutError, match="artifact roots"):
        layout.validate_project_layout(
            checkout,
            binding_id="binding-v2",
            checkout_id="checkout-v2",
            captured_at="2026-08-04T00:00:00+09:00",
        )


def test_workflow_records_are_append_only_instead_of_moved(tmp_path):
    layout = _layout()
    checkout = tmp_path / "checkout"
    shutil.copytree(EMPTY_PROJECT_V2, checkout)
    workflow = checkout / ".reviewcompass" / "workflow"
    issue = workflow / "issues" / "issue-001--v1.json"
    issue.parent.mkdir()
    issue.write_text('{"issue_id":"issue-001","version":1}\n')
    before = layout.snapshot_project_artifacts(checkout, "workflow")

    plan = workflow / "resolution-plans" / "plan-001--v1.json"
    plan.parent.mkdir()
    plan.write_text(
        '{"plan_id":"plan-001","issue_id":"issue-001","version":1}\n'
    )
    after_add = layout.snapshot_project_artifacts(checkout, "workflow")

    assert layout.validate_project_artifact_append_only(before, after_add)
    moved = workflow / "resolution-plans" / issue.name
    issue.rename(moved)
    after_move = layout.snapshot_project_artifacts(checkout, "workflow")
    with pytest.raises(layout.LayoutError, match="removed or rewritten"):
        layout.validate_project_artifact_append_only(before, after_move)


def test_deployment_package_rejects_project_workflow_records(tmp_path):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_V2_CANDIDATE)
    package = tmp_path / "package"
    (package / "tools").mkdir(parents=True)
    (package / "tools" / "runner.py").write_text("pass\n")

    assert layout.validate_deployment_package_layout(package, baseline)

    leaked_issue = (
        package
        / ".reviewcompass"
        / "workflow"
        / "issues"
        / "issue-001--v1.json"
    )
    leaked_issue.parent.mkdir(parents=True)
    leaked_issue.write_text('{"issue_id":"issue-001","version":1}\n')
    with pytest.raises(layout.LayoutError, match="Project Artifact"):
        layout.validate_deployment_package_layout(package, baseline)


def test_reviewcompass3_project_manifest_uses_approved_v2_boundary():
    layout = _layout()
    approval = json.loads(LAYOUT_V2_APPROVAL.read_text(encoding="utf-8"))
    approved_path = PROJECT_ROOT / approval["approved_target"]["path"]
    approved_digest = hashlib.sha256(approved_path.read_bytes()).hexdigest()

    assert approved_digest == approval["approved_target"]["sha256"]
    assert approval["approved_target"]["authority_status"] == "current"
    baseline = layout.load_layout_baseline(approved_path)
    binding = layout.validate_project_layout(
        PROJECT_ROOT,
        binding_id="reviewcompass3-local-binding",
        checkout_id="reviewcompass3-local-checkout",
        captured_at="2026-08-04T00:00:00+09:00",
    )

    manifest_path = PROJECT_ROOT / ".reviewcompass" / "project-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert baseline["layout_version"] == 2
    assert binding.project_id == manifest["project_id"] == "reviewcompass3"
    assert manifest["schema_version"] == 2
    assert manifest["artifact_roots"]["workflow"] == (
        ".reviewcompass/workflow"
    )
    assert set(manifest["artifact_roots"]) == {
        "contracts",
        "design_decisions",
        "policies",
        "requirement_maps",
        "reuse",
        "verified_artifacts",
        "workflow",
    }
    workflow_snapshot = layout.snapshot_project_artifacts(
        PROJECT_ROOT,
        "workflow",
    )
    expected_bootstrap_snapshot = {
        ".reviewcompass/workflow/.gitkeep": hashlib.sha256(
            b"project-artifact-root\n"
        ).hexdigest(),
        ".reviewcompass/workflow/improvement-candidates/.gitkeep": (
            hashlib.sha256(b"").hexdigest()
        ),
        ".reviewcompass/workflow/triage-decisions/.gitkeep": (
            hashlib.sha256(b"").hexdigest()
        ),
    }
    for path, digest in expected_bootstrap_snapshot.items():
        assert workflow_snapshot[path] == digest
    assert layout.find_terminal_absolute_paths(
        PROJECT_ROOT / ".reviewcompass"
    ) == ()

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
