"""Task Contract固定入力のlifecycle statusとsource pinのAcceptance Test。

指示：records/session-handoffs/2026-08-05-codex-to-claude-task-contract-source-pin-implementation.md
"""

import hashlib
import importlib
import json
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PILOT_CONTRACT = PROJECT_ROOT / "records/task-contract/issue-resolution-early-pilot-v1.json"
TRANSCRIPT_CONTRACT = (
    PROJECT_ROOT / "records/task-contract/session-transcript-eventual-preservation-v1.json"
)
PLAN_PATH = "docs/current/reviewcompass3-plan-current.md"
PINNED_PLAN_SHA = "0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694"
PINNED_COMMIT = "c475becb3ebf3f3cb9e362d64bab79606ed3719d"


def _module():
    return importlib.import_module("tools.development.issue_resolution_pilot")


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _canonical_digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return _sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    )


def _write_record(path, document):
    document["content_digest"] = _canonical_digest(document)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _git(root, *arguments):
    return subprocess.run(
        ("git", *arguments),
        cwd=str(root),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _fixture_repository(tmp_path, *, source_text="plan v1\n"):
    """固定sourceを一件持つ最小のTask Contract repositoryを作る。"""

    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "records" / "task-contract").mkdir(parents=True)
    (root / "records" / "development").mkdir(parents=True)
    plan = root / "docs" / "plan.md"
    plan.write_text(source_text, encoding="utf-8")
    _git(root.parent, "init", "-q", str(root))
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=test@example.com", "-c", "user.name=test", "commit", "-q", "-m", "fix plan")
    commit = _git(root, "rev-parse", "HEAD")

    contract = {
        "task_contract_id": "TC-FIXTURE-2026-08-05-V1",
        "status": "active",
        "goal": "fixture",
        "fixed_sources": [{"path": "docs/plan.md", "sha256": _sha256(source_text.encode("utf-8"))}],
        "in_scope": ["fixture scope"],
    }
    contract_path = root / "records" / "task-contract" / "fixture-v1.json"
    contract_path.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root, contract_path, commit, _sha256(source_text.encode("utf-8"))


def _status_record(root, contract_path, status):
    return _write_record(
        root / "records" / "development" / "fixture-status.json",
        {
            "record_kind": "task_contract_lifecycle_status",
            "schema_version": 1,
            "digest_algorithm": "sha256",
            "status_record_id": "TCLS-FIXTURE-V1",
            "status_record_version": 1,
            "recorded_at": "2026-08-05",
            "task_contract_id": "TC-FIXTURE-2026-08-05-V1",
            "task_contract_path": "records/task-contract/fixture-v1.json",
            "task_contract_sha256": _sha256(contract_path.read_bytes()),
            "lifecycle_status": status,
            "grounds": [],
            "effect": "fixture",
        },
    )


def _pin_record(root, contract_path, *, commit, sha256, name="fixture-pin.json", path="docs/plan.md"):
    return _write_record(
        root / "records" / "development" / name,
        {
            "record_kind": "task_contract_source_pin",
            "schema_version": 1,
            "digest_algorithm": "sha256",
            "pin_record_id": f"TCSP-FIXTURE-{name}",
            "pin_record_version": 1,
            "recorded_at": "2026-08-05",
            "task_contract_id": "TC-FIXTURE-2026-08-05-V1",
            "task_contract_path": "records/task-contract/fixture-v1.json",
            "task_contract_sha256": _sha256(contract_path.read_bytes()),
            "applicable_lifecycle_statuses": [
                "completed",
                "completed_carried_forward",
                "superseded",
                "historical",
            ],
            "unpinned_source_policy": "verify_working_tree",
            "pins": [{"path": path, "sha256": sha256, "commit": commit, "reason": "fixture"}],
            "effect": "fixture",
        },
    )


# 1. 歴史状態の実contractは、Current Planが変わってもpinのblobが一致すれば通る


def test_historical_early_pilot_passes_with_source_pin():
    pilot = _module()
    working = _sha256((PROJECT_ROOT / PLAN_PATH).read_bytes())
    assert working != PINNED_PLAN_SHA, "この検証はPlanが更新済みであることを前提にする"
    assert pilot.validate_task_contract_sources(
        PILOT_CONTRACT, project_root=PROJECT_ROOT
    ) == 9


# 2. activeなcontractは固定sourceが変われば停止する


def test_active_contract_stops_when_fixed_source_changes(tmp_path):
    pilot = _module()
    root, contract_path, _commit, _sha = _fixture_repository(tmp_path)
    (root / "docs" / "plan.md").write_text("plan v2\n", encoding="utf-8")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "stale" in str(error.value)


# 3. active_staleはsource pinで通せない


def test_active_stale_cannot_be_revived_by_source_pin(tmp_path):
    pilot = _module()
    root, contract_path, commit, sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "active_stale")
    _pin_record(root, contract_path, commit=commit, sha256=sha)
    (root / "docs" / "plan.md").write_text("plan v2\n", encoding="utf-8")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "stale_fixed_source" in str(error.value)


def test_session_transcript_contract_is_recorded_as_active_stale():
    pilot = _module()
    record = pilot.load_task_contract_lifecycle_status(
        TRANSCRIPT_CONTRACT, project_root=PROJECT_ROOT
    )
    assert record["lifecycle_status"] == "active_stale"
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(
            TRANSCRIPT_CONTRACT, project_root=PROJECT_ROOT
        )
    assert "stale_fixed_source" in str(error.value)


# 4. pinのcommit不存在、blob不一致、対象contract不一致、重複pinを停止する


def test_pin_with_unknown_commit_stops(tmp_path):
    pilot = _module()
    root, contract_path, _commit, sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    _pin_record(root, contract_path, commit="0" * 40, sha256=sha)
    (root / "docs" / "plan.md").write_text("plan v2\n", encoding="utf-8")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "pin_unresolvable" in str(error.value)


def test_pin_with_mismatched_blob_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit, _sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    _pin_record(root, contract_path, commit=commit, sha256="1" * 64)
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


def test_pin_bound_to_other_contract_digest_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit, sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    pin_path = _pin_record(root, contract_path, commit=commit, sha256=sha)
    document = json.loads(pin_path.read_text(encoding="utf-8"))
    document["task_contract_sha256"] = "2" * 64
    _write_record(pin_path, document)
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


def test_conflicting_pins_for_same_source_stop(tmp_path):
    pilot = _module()
    root, contract_path, commit, sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    _pin_record(root, contract_path, commit=commit, sha256=sha)
    _pin_record(
        root, contract_path, commit=commit, sha256="3" * 64, name="fixture-pin-2.json"
    )
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


# 5. source pinの無いhistorical contractを停止する


def test_historical_contract_without_pin_stops(tmp_path):
    pilot = _module()
    root, contract_path, _commit, _sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "pin_unresolvable" in str(error.value)


def test_historical_contract_does_not_fall_back_to_working_tree(tmp_path):
    """pinが無い歴史状態のcontractは、working treeが一致していても通さない。"""

    pilot = _module()
    root, contract_path, _commit, _sha = _fixture_repository(tmp_path)
    _status_record(root, contract_path, "completed_carried_forward")
    assert (root / "docs" / "plan.md").read_text(encoding="utf-8") == "plan v1\n"
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_task_contract_sources(contract_path, project_root=root)
    assert "pin_unresolvable" in str(error.value)


# CLI出力


def test_cli_reports_pin_resolution_without_removing_existing_keys(capsys):
    pilot = _module()
    exit_code = pilot.main(
        [
            "--project-root",
            str(PROJECT_ROOT),
            "task-contract",
            str(PILOT_CONTRACT),
        ]
    )
    assert exit_code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["fixed_source_count"] == 9
    assert output["pin_resolved_count"] == 1
