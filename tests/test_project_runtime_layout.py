"""Project-first runtime root Layout Baseline v3の受入テスト。"""

import importlib
import stat
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BASELINE_V3_CANDIDATE = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-04-layout-baseline-v3-project-first-candidate.json"
)


def _layout():
    return importlib.import_module("tools.layout.baseline")


def test_v3_candidate_fixes_project_first_runtime_root_boundary():
    layout = _layout()

    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)

    assert baseline["schema_version"] == 3
    assert baseline["layout_version"] == 3
    assert baseline["project_runtime_layout"] == {
        "runtime_root": {
            "default_home_relative_path": ".reviewcompass3",
            "resolution_precedence": [
                "explicit_cli",
                "versioned_user_setting",
                "allowlisted_environment",
                "home_default",
            ],
            "environment_variable": "REVIEWCOMPASS3_RUNTIME_ROOT",
        },
        "project_id_source": "project_manifest.stable_explicit_id",
        "profiles": ["development", "runtime"],
        "project_relative_prefix": "projects",
        "root_kinds": [
            "data",
            "state",
            "cache",
            "logs",
            "evaluation",
            "sensitive",
        ],
        "creation": "explicit_requested_kinds_only",
        "binding_directory": "deferred_until_concurrent_checkout_need",
    }
    assert baseline["deployment_package_policy"]["runtime_root_included"] is False


def test_v3_resolves_project_profile_roots_without_creating_them(tmp_path):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)
    runtime_root = tmp_path / ".reviewcompass3"

    development = layout.resolve_project_runtime_layout(
        baseline,
        runtime_root=runtime_root,
        project_id="project-alpha",
        profile="development",
    )
    runtime = layout.resolve_project_runtime_layout(
        baseline,
        runtime_root=runtime_root,
        project_id="project-alpha",
        profile="runtime",
    )
    other_project = layout.resolve_project_runtime_layout(
        baseline,
        runtime_root=runtime_root,
        project_id="project-beta",
        profile="development",
    )

    assert development.config_root == runtime_root / "config"
    assert development.roots["data"] == (
        runtime_root / "projects" / "project-alpha" / "development" / "data"
    )
    assert set(development.roots) == {
        "data",
        "state",
        "cache",
        "logs",
        "evaluation",
        "sensitive",
    }
    assert development.roots["data"] != runtime.roots["data"]
    assert development.roots["data"] != other_project.roots["data"]
    assert not runtime_root.exists()


def test_v3_initializes_only_explicitly_requested_roots(tmp_path):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)
    resolution = layout.resolve_project_runtime_layout(
        baseline,
        runtime_root=tmp_path / ".reviewcompass3",
        project_id="project-alpha",
        profile="development",
    )

    created = layout.initialize_project_runtime_layout(
        resolution,
        requested_kinds=["data", "sensitive"],
    )

    assert created == {
        "data": resolution.roots["data"],
        "sensitive": resolution.roots["sensitive"],
    }
    assert not resolution.config_root.exists()
    assert resolution.roots["data"].is_dir()
    assert resolution.roots["sensitive"].is_dir()
    assert not resolution.roots["state"].exists()
    assert not resolution.roots["cache"].exists()
    if __import__("os").name != "nt":
        assert stat.S_IMODE(resolution.roots["sensitive"].stat().st_mode) == 0o700


@pytest.mark.parametrize(
    ("project_id", "profile", "requested_kinds"),
    [
        ("../escape", "development", ["data"]),
        ("project-alpha", "stable", ["data"]),
        ("project-alpha", "development", ["unknown"]),
    ],
)
def test_v3_rejects_unsafe_project_profile_and_root_kind(
    tmp_path,
    project_id,
    profile,
    requested_kinds,
):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)

    if profile != "development":
        with pytest.raises(layout.LayoutError, match="profile"):
            layout.resolve_project_runtime_layout(
                baseline,
                runtime_root=tmp_path / ".reviewcompass3",
                project_id=project_id,
                profile=profile,
            )
        return
    if project_id != "project-alpha":
        with pytest.raises(layout.LayoutError, match="project identity"):
            layout.resolve_project_runtime_layout(
                baseline,
                runtime_root=tmp_path / ".reviewcompass3",
                project_id=project_id,
                profile=profile,
            )
        return

    resolution = layout.resolve_project_runtime_layout(
        baseline,
        runtime_root=tmp_path / ".reviewcompass3",
        project_id=project_id,
        profile=profile,
    )
    with pytest.raises(layout.LayoutError, match="root kind"):
        layout.initialize_project_runtime_layout(
            resolution,
            requested_kinds=requested_kinds,
        )


def test_v3_deployment_package_rejects_embedded_runtime_root(tmp_path):
    layout = _layout()
    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)
    package = tmp_path / "package"
    package.mkdir()

    assert layout.validate_deployment_package_layout(package, baseline)

    (package / ".reviewcompass3" / "projects").mkdir(parents=True)
    with pytest.raises(layout.LayoutError, match="runtime root"):
        layout.validate_deployment_package_layout(package, baseline)
