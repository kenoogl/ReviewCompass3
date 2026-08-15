"""正式コード再利用検索の一操作入口を固定する試験。"""

import hashlib
import importlib
import json
import subprocess
from pathlib import Path

import pytest

from tools.development import work4a_rebuild_v3 as rebuild
from tools.development import reuse_search_record as reuse


PROJECT_ID = "reviewcompass3"
UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
CAPTURED_AT = "2026-08-15T13:00:00+09:00"


def _digest(document):
    return hashlib.sha256(
        json.dumps(
            document,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _git(root, *arguments):
    result = subprocess.run(
        ("git", *arguments),
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _write_plan(root, *, empty_paths=False):
    searches = [
        {
            "subject": "formal_code",
            "target_paths": [] if empty_paths else ["tools/core/engine.py"],
            "target_symbols": ["store"],
            "attestation_path": "records/formal-code-attestation.json",
        },
        {
            "subject": "provisional_code",
            "target_paths": ["tools/core/engine.py"],
            "target_symbols": [],
            "attestation_path": "records/provisional-code-attestation.json",
        },
    ]
    document = {
        "record_kind": "formal_code_reuse_search_plan",
        "schema_version": 1,
        "plan_id": "FCRS-TEST-V1",
        "searches": searches,
    }
    document["content_digest"] = _digest(document)
    path = root / "records" / "search-plan.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _write_capability_plan(root):
    capability = {
        "capability_id": "store_value",
        "responsibility": "値を保存する",
        "inputs": ["値"],
        "outputs": ["保存結果"],
        "failure_behavior": ["失敗を成功として扱わない"],
        "required_properties": ["決定的に処理する"],
        "reference_paths": ["tools/core/engine.py"],
        "reference_symbols": [],
        "symbol_terms": ["store"],
        "required_effect_markers": [],
        "forbidden_effect_markers": ["network"],
    }
    document = {
        "record_kind": "formal_code_reuse_search_plan",
        "schema_version": 2,
        "plan_id": "FCRS-TEST-V2",
        "searches": [
            {
                "subject": "capability_search",
                "capabilities": [capability],
                "attestation_path": "records/capability-attestation.json",
            }
        ],
    }
    document["content_digest"] = _digest(document)
    path = root / "records" / "capability-plan.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _project(tmp_path, *, initialize_git=True, empty_paths=False):
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
        "def store(value):\n    return value\n",
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
    plan = _write_plan(root, empty_paths=empty_paths)
    if initialize_git:
        _git(root, "init", "-q")
        _git(root, "config", "user.name", "Test User")
        _git(root, "config", "user.email", "test@example.invalid")
        _git(root, "add", ".")
        _git(root, "commit", "-q", "-m", "fixture")
    return root, universe.path, policy.path, plan


def _execute(entry, root, universe, policy, plan, tmp_path, **options):
    return entry.execute_formal_search(
        project_root=root,
        runtime_root=tmp_path / "runtime",
        profile="development",
        universe_path=universe,
        policy_path=policy,
        plan_path=plan,
        captured_at=CAPTURED_AT,
        **options,
    )


def test_one_operation_processes_two_searches_from_one_commit(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, plan = _project(tmp_path)

    result = _execute(entry, root, universe, policy, plan, tmp_path)

    assert result["status"] == "completed"
    assert result["head"] == _git(root, "rev-parse", "HEAD")
    assert result["source_file_count"] == 1
    assert len(result["searches"]) == 2
    assert all(item["start_allowed"] for item in result["searches"])
    assert all(Path(item["attestation_path"]).is_file() for item in result["searches"])
    assert result["lifecycle_adjudication_required"] is True
    assert result["reuse_disposition_adjudication_required"] is True


def test_one_operation_accepts_capability_plan_without_fixed_global_list(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, _ = _project(tmp_path)
    plan = _write_capability_plan(root)
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "capability plan")

    result = _execute(entry, root, universe, policy, plan, tmp_path)

    assert result["status"] == "completed"
    assert result["searches"][0]["capability_count"] == 1
    assert result["searches"][0]["uncovered_capability_ids"] == []
    assert result["searches"][0]["candidate_count"] >= 1


def test_capability_attestation_becomes_stale_when_new_code_enters_git_scope(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, _ = _project(tmp_path)
    plan = _write_capability_plan(root)
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "capability plan")
    result = _execute(entry, root, universe, policy, plan, tmp_path)
    search = result["searches"][0]
    (root / "tools" / "core" / "new_helper.py").write_text(
        "def new_helper():\n    return None\n",
        encoding="utf-8",
    )

    verdict = reuse.gate_check_attested(
        attestation_path=search["attestation_path"],
        data_root=(
            tmp_path
            / "runtime"
            / "projects"
            / PROJECT_ID
            / "development"
            / "data"
        ),
        expected_identity={
            "profile_run_id": result["routine_profile_run_id"],
            "discovery_run_id": result["comparison_discovery_run_id"],
            "source_content_id": result["source_content_id"],
        },
        project_root=root,
    )

    assert verdict["start_allowed"] is False
    assert verdict["reason"] == "profile_stale"
    assert "tools/core/new_helper.py" in verdict["stale_files"]


def test_one_operation_reports_elapsed_time_without_changing_search_identity(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, _ = _project(tmp_path)
    plan = _write_capability_plan(root)
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "capability plan")
    ticks = iter((0.0, 1.0, 3.0, 6.0, 7.0, 11.0))

    result = _execute(
        entry,
        root,
        universe,
        policy,
        plan,
        tmp_path,
        clock=lambda: next(ticks),
    )

    assert result["timing"] == {
        "measurement": "monotonic_elapsed_time",
        "unit": "seconds",
        "observation": 1.0,
        "routine_profile": 2.0,
        "comparison_discovery": 3.0,
        "searches": 4.0,
        "total": 11.0,
    }
    assert result["searches"][0]["elapsed_seconds"] == 4.0
    attestation = json.loads(
        Path(result["searches"][0]["attestation_path"]).read_text(encoding="utf-8")
    )
    assert "timing" not in attestation


def test_one_operation_rejects_uncommitted_state(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, plan = _project(tmp_path)
    (root / "tools" / "core" / "engine.py").write_text(
        "def store(value):\n    return None\n",
        encoding="utf-8",
    )

    with pytest.raises(entry.FormalCodeReuseSearchError) as error:
        _execute(entry, root, universe, policy, plan, tmp_path)

    assert error.value.code == "uncommitted_repository_state"


def test_one_operation_rejects_empty_target_paths(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, plan = _project(tmp_path, empty_paths=True)

    with pytest.raises(entry.FormalCodeReuseSearchError) as error:
        _execute(entry, root, universe, policy, plan, tmp_path)

    assert error.value.code == "invalid_search_plan"


def test_one_operation_rejects_existing_attestation(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, plan = _project(tmp_path)
    target = root / "records" / "formal-code-attestation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("existing\n", encoding="utf-8")
    _git(root, "add", target.relative_to(root).as_posix())
    _git(root, "commit", "-q", "-m", "existing output")

    with pytest.raises(entry.FormalCodeReuseSearchError) as error:
        _execute(entry, root, universe, policy, plan, tmp_path)

    assert error.value.code == "output_already_exists"


def test_one_operation_rejects_non_repository(tmp_path):
    entry = importlib.import_module("tools.development.formal_code_reuse_search")
    root, universe, policy, plan = _project(tmp_path, initialize_git=False)

    with pytest.raises(entry.FormalCodeReuseSearchError) as error:
        _execute(entry, root, universe, policy, plan, tmp_path)

    assert error.value.code == "committed_source_unavailable"
