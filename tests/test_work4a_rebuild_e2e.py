"""Work 4A再設計の一貫した受入境界。実装より先に固定する。"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _project(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    manifest = {
        "schema_version": 2,
        "project_id": "work4a-e2e",
        "artifact_roots": {
            "contracts": ".reviewcompass/contracts",
            "design_decisions": ".reviewcompass/design-decisions",
            "policies": ".reviewcompass/policies",
            "requirement_maps": ".reviewcompass/requirement-maps",
            "reuse": ".reviewcompass/reuse",
            "verified_artifacts": ".reviewcompass/verified-artifacts",
            "workflow": ".reviewcompass/workflow",
        },
        "document_links": [],
    }
    (project_root / ".reviewcompass").mkdir()
    (project_root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    source_root = project_root / "src"
    source_root.mkdir()
    (source_root / "routine.py").write_text(
        "def existing(value):\n    return value\n", encoding="utf-8"
    )
    return project_root, source_root


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild")


def test_observation_separates_source_content_identity_from_head(rebuild, tmp_path):
    """Acceptance 1: 同じsource内容ならHEAD差でbaselineをstaleにしない。"""
    project_root, source_root = _project(tmp_path)
    data_root = tmp_path / "data"

    first = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="a" * 40,
        tool_version="v1",
    )
    second = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="b" * 40,
        tool_version="v1",
    )

    assert first.source_content_id == second.source_content_id
    assert first.snapshot_id != second.snapshot_id
    assert first.observation_path.is_relative_to(data_root)
    assert second.observation_path.is_relative_to(data_root)


def test_new_entry_reuses_unchanged_record_refs_and_baseline_is_fresh(rebuild, tmp_path):
    """Acceptance 2--5: Decisionからnew-only台帳を作り、再観測でfreshを確認する。"""
    project_root, source_root = _project(tmp_path)
    data_root = tmp_path / "data"
    observation = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="a" * 40,
        tool_version="v1",
    )
    candidates = rebuild.build_candidate_run(
        observation=observation,
        data_root=data_root,
        tool_version="v1",
    )
    decision = rebuild.write_human_decision(
        project_root=project_root,
        decision_id="DEC-WORK4A-E2E-001",
        candidate_run=candidates,
        disposition="reuse",
    )
    first = rebuild.append_reusable_routine_baseline(
        project_root=project_root,
        observation=observation,
        candidate_run=candidates,
        decision=decision,
        new_entries=(
            {
                "entry_id": "RRL-EXISTING",
                "symbol": "routine.existing",
                "responsibility": "identity value",
                "side_effects": [],
                "disposition": "reuse",
            },
        ),
        new_relations=(),
        prior=None,
    )
    original_entry = first.entry_paths[0].read_bytes()

    (source_root / "routine.py").write_text(
        "def existing(value):\n    return value\n\ndef added(value):\n    return value + 1\n",
        encoding="utf-8",
    )
    changed_observation = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="c" * 40,
        tool_version="v1",
    )
    changed_candidates = rebuild.build_candidate_run(
        observation=changed_observation,
        data_root=data_root,
        tool_version="v1",
    )
    second_decision = rebuild.write_human_decision(
        project_root=project_root,
        decision_id="DEC-WORK4A-E2E-002",
        candidate_run=changed_candidates,
        disposition="extend",
    )
    second = rebuild.append_reusable_routine_baseline(
        project_root=project_root,
        observation=changed_observation,
        candidate_run=changed_candidates,
        decision=second_decision,
        new_entries=(
            {
                "entry_id": "RRL-ADDED",
                "symbol": "routine.added",
                "responsibility": "increment value",
                "side_effects": [],
                "disposition": "extend",
            },
        ),
        new_relations=(
            {
                "relation_id": "REL-ADDED-EXISTING",
                "left_entry_id": "RRL-ADDED",
                "right_entry_id": "RRL-EXISTING",
                "relation_kind": "extends",
                "rationale": "adds one behavior",
            },
        ),
        prior=first,
    )

    assert first.entry_paths[0].read_bytes() == original_entry
    assert len(second.new_entry_paths) == 1
    assert len(second.entry_refs) == 2
    after_artifact_commit = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="d" * 40,
        tool_version="v1",
    )
    assert rebuild.validate_baseline(
        baseline=second,
        observation=after_artifact_commit,
        policy_change="ordinary",
    ).status == "fresh"


def test_rebuild_rejects_content_change_tampering_unsafe_root_and_high_risk_policy(
    rebuild, tmp_path
):
    """Acceptance 6: 正常経路以外は台帳をcurrentとして使わせない。"""
    project_root, source_root = _project(tmp_path)
    data_root = tmp_path / "data"
    observation = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="a" * 40,
        tool_version="v1",
    )
    candidates = rebuild.build_candidate_run(
        observation=observation, data_root=data_root, tool_version="v1"
    )
    decision = rebuild.write_human_decision(
        project_root=project_root,
        decision_id="DEC-WORK4A-E2E-003",
        candidate_run=candidates,
        disposition="reuse",
    )
    baseline = rebuild.append_reusable_routine_baseline(
        project_root=project_root,
        observation=observation,
        candidate_run=candidates,
        decision=decision,
        new_entries=(
            {
                "entry_id": "RRL-EXISTING",
                "symbol": "routine.existing",
                "responsibility": "identity value",
                "side_effects": [],
                "disposition": "reuse",
            },
        ),
        new_relations=(),
        prior=None,
    )
    (source_root / "routine.py").write_text("def changed():\n    return 0\n", encoding="utf-8")
    changed = rebuild.capture_source_observation(
        project_root=project_root,
        source_root=source_root,
        data_root=data_root,
        source_paths=("routine.py",),
        head="b" * 40,
        tool_version="v1",
    )
    assert rebuild.validate_baseline(
        baseline=baseline, observation=changed, policy_change="ordinary"
    ).status == "stale"
    baseline.entry_paths[0].write_text("tampered", encoding="utf-8")
    with pytest.raises(rebuild.RebuildValidationError, match="entry digest"):
        rebuild.validate_baseline(
            baseline=baseline, observation=observation, policy_change="ordinary"
        )
    with pytest.raises(rebuild.RebuildValidationError, match="reuse root"):
        rebuild.resolve_reuse_root(
            project_root=project_root,
            manifest_override={"artifact_roots": {"reuse": "../escape"}},
        )
    assert rebuild.validate_baseline(
        baseline=baseline,
        observation=observation,
        policy_change="authority",
    ).status == "revalidation_required"


def test_historical_contract_status_requires_human_approval_and_provenance(
    rebuild, tmp_path
):
    """Acceptance 7: legacy Contractを推測だけでhistoricalへ変換しない。"""
    contract = tmp_path / "legacy-contract.json"
    contract.write_text('{"contract_status":"fixed_pending_containing_commit"}', encoding="utf-8")

    with pytest.raises(rebuild.RebuildValidationError, match="human approval"):
        rebuild.record_historical_contract_status(
            contract_path=contract,
            creation_commit="a" * 40,
            creation_policy_digest="b" * 64,
            human_decision=None,
            status_root=tmp_path / "statuses",
        )
    status = rebuild.record_historical_contract_status(
        contract_path=contract,
        creation_commit="a" * 40,
        creation_policy_digest="b" * 64,
        human_decision={"decision_id": "DEC-HIST-001", "outcome": "completed_historical"},
        status_root=tmp_path / "statuses",
    )

    assert status.contract_sha256 == _sha256(contract)
    assert status.outcome == "completed_historical"
    assert status.permits_current_start is False
