"""正式なコード検索をローカルの確定コミットへ結び付ける試験。"""

import json
import subprocess
from pathlib import Path

import pytest

from tools.development import work4a_rebuild_v3 as rebuild


PROJECT_ID = "reviewcompass3"
UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
CAPTURED_AT = "2026-08-15T12:00:00+09:00"


def _git(root, *arguments):
    result = subprocess.run(
        ("git", *arguments),
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _project(tmp_path):
    root = tmp_path / "project"
    (root / "tools" / "core").mkdir(parents=True)
    (root / "docs" / "development").mkdir(parents=True)
    for name in ("contracts", "design-decisions", "policies", "reuse"):
        (root / ".reviewcompass" / name).mkdir(parents=True)
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(
            {
                "artifact_roots": {
                    "contracts": ".reviewcompass/contracts",
                    "design_decisions": ".reviewcompass/design-decisions",
                    "policies": ".reviewcompass/policies",
                    "reuse": ".reviewcompass/reuse",
                },
                "document_links": [],
                "project_id": PROJECT_ID,
                "schema_version": 2,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "tools" / "core" / "engine.py").write_text(
        "def run():\n    return 1\n",
        encoding="utf-8",
    )
    development = root / "docs" / "development" / "development-policy.md"
    development.write_text("development policy\n", encoding="utf-8")
    universe = rebuild.write_source_universe(
        project_root=root,
        universe_id=UNIVERSE_ID,
        universe_version=1,
        development_policy_path=development,
    )
    policy = rebuild.write_freshness_policy_v4(
        project_root=root,
        policy_id=POLICY_ID,
        policy_version=1,
        development_policy_path=development,
        change_class="ordinary",
    )
    return root, universe, policy


def _commit(root):
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "fixture")
    return _git(root, "rev-parse", "HEAD")


def _capture(root, universe, policy, tmp_path):
    return rebuild.capture_committed_observation(
        project_root=root,
        runtime_root=tmp_path / "runtime",
        profile="development",
        universe=universe,
        policy=policy,
        tool_version="v3-formal",
        captured_at=CAPTURED_AT,
    )


def test_formal_observation_derives_head_from_clean_local_commit(tmp_path):
    root, universe, policy = _project(tmp_path)
    head = _commit(root)

    observation = _capture(root, universe, policy, tmp_path)
    document = json.loads(observation.path.read_text(encoding="utf-8"))

    assert document["head"] == head
    assert [item["path"] for item in document["files"]] == [
        "tools/core/engine.py"
    ]


@pytest.mark.parametrize("state", ("modified", "staged", "untracked"))
def test_formal_observation_rejects_uncommitted_repository_state(tmp_path, state):
    root, universe, policy = _project(tmp_path)
    _commit(root)
    if state == "modified":
        (root / "tools" / "core" / "engine.py").write_text(
            "def run():\n    return 2\n",
            encoding="utf-8",
        )
    else:
        added = root / "tools" / "core" / "added.py"
        added.write_text("VALUE = 1\n", encoding="utf-8")
        if state == "staged":
            _git(root, "add", added.relative_to(root).as_posix())

    with pytest.raises(rebuild.V3ValidationError) as error:
        _capture(root, universe, policy, tmp_path)

    assert error.value.code == "uncommitted_repository_state"


def test_formal_observation_rejects_ignored_code_outside_commit(tmp_path):
    root, universe, policy = _project(tmp_path)
    (root / ".gitignore").write_text("tools/core/ignored.py\n", encoding="utf-8")
    _commit(root)
    (root / "tools" / "core" / "ignored.py").write_text(
        "VALUE = 1\n",
        encoding="utf-8",
    )

    with pytest.raises(rebuild.V3ValidationError) as error:
        _capture(root, universe, policy, tmp_path)

    assert error.value.code == "committed_source_set_mismatch"


def test_formal_observation_rejects_non_repository(tmp_path):
    root, universe, policy = _project(tmp_path)

    with pytest.raises(rebuild.V3ValidationError) as error:
        _capture(root, universe, policy, tmp_path)

    assert error.value.code == "committed_source_unavailable"
