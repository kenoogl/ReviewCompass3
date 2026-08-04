"""Work 4A v2の設計前提を含むE2E受入境界。"""

import importlib
import json
from pathlib import Path

import pytest


def _project(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    (root / ".reviewcompass").mkdir()
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "project_id": "work4a-v2-e2e",
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
        ),
        encoding="utf-8",
    )
    (root / "tools").mkdir()
    (root / "tools" / "routine.py").write_text(
        "def existing(value):\n    return value\n", encoding="utf-8"
    )
    (root / "tests").mkdir()
    (root / "tests" / "ignored.py").write_text(
        "def ignored():\n    return 0\n", encoding="utf-8"
    )
    (root / "docs").mkdir()
    (root / "docs" / "ignored.py").write_text(
        "def ignored_document():\n    return 0\n", encoding="utf-8"
    )
    development_policy = root / "development-policy.md"
    development_policy.write_text("policy v1\n", encoding="utf-8")
    return root, development_policy


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild_v2")


def _inputs(rebuild, root, development_policy):
    universe = rebuild.write_source_universe(
        project_root=root,
        universe_id="SRCU-WORK4A-TOOLS-PY-V1",
        development_policy_path=development_policy,
    )
    policy = rebuild.write_freshness_policy(
        project_root=root,
        policy_id="POL-WORK4A-FRESHNESS-001",
        development_policy_path=development_policy,
    )
    return universe, policy


def test_v2_observation_uses_only_approved_universe_and_head_is_provenance(
    rebuild, tmp_path
):
    """v2 acceptance 1, 5: callerのpath列ではなくuniverse recordを使う。"""
    root, development_policy = _project(tmp_path)
    universe, policy = _inputs(rebuild, root, development_policy)
    data_root = tmp_path / "data"

    first = rebuild.capture_observation(
        project_root=root,
        data_root=data_root,
        universe=universe,
        policy=policy,
        head="a" * 40,
        tool_version="v2",
    )
    second = rebuild.capture_observation(
        project_root=root,
        data_root=data_root,
        universe=universe,
        policy=policy,
        head="b" * 40,
        tool_version="v2",
    )

    assert first.source_content_id == second.source_content_id
    assert first.snapshot_id != second.snapshot_id
    assert first.paths == ("tools/routine.py",)
    assert rebuild.validate_universe_change(
        baseline_universe=universe,
        observed_universe_id="SRCU-WORK4A-TOOLS-PY-V2",
    ).status == "stale"


def test_v2_requires_policy_and_operational_decision_for_new_only_entry_and_relation(
    rebuild, tmp_path
):
    """v2 acceptance 2, 3: EntryとRelationの双方を複製しない。"""
    root, development_policy = _project(tmp_path)
    universe, policy = _inputs(rebuild, root, development_policy)
    observation = rebuild.capture_observation(
        project_root=root, data_root=tmp_path / "data", universe=universe,
        policy=policy, head="a" * 40, tool_version="v2",
    )
    candidates = rebuild.build_candidate_run(observation=observation)
    with pytest.raises(rebuild.V2ValidationError, match="operational decision"):
        rebuild.append_baseline(
            project_root=root, observation=observation, candidates=candidates,
            policy=policy, decision=None, entries=(), relations=(), prior=None,
        )
    decision = rebuild.write_operational_decision(
        project_root=root, decision_id="DEC-OP-001", candidates=candidates,
        disposition="reuse", human_id="human-1",
    )
    first = rebuild.append_baseline(
        project_root=root, observation=observation, candidates=candidates,
        policy=policy, decision=decision,
        entries=({"entry_id": "ENTRY-1", "symbol": "tools.routine.existing"},),
        relations=({"relation_id": "REL-1", "left": "ENTRY-1", "right": "ENTRY-1", "kind": "self"},),
        prior=None,
    )
    entry_bytes = first.entry_paths[0].read_bytes()
    relation_bytes = first.relation_paths[0].read_bytes()
    second_decision = rebuild.write_operational_decision(
        project_root=root, decision_id="DEC-OP-002", candidates=candidates,
        disposition="extend", human_id="human-1",
    )
    second = rebuild.append_baseline(
        project_root=root, observation=observation, candidates=candidates,
        policy=policy, decision=second_decision,
        entries=({"entry_id": "ENTRY-2", "symbol": "tools.routine.new"},),
        relations=({"relation_id": "REL-2", "left": "ENTRY-2", "right": "ENTRY-1", "kind": "extends"},),
        prior=first,
    )

    assert first.entry_paths[0].read_bytes() == entry_bytes
    assert first.relation_paths[0].read_bytes() == relation_bytes
    assert second.current_version == 2
    assert len(second.entry_paths) == 2
    assert len(second.relation_paths) == 2


def test_v2_rejects_tampering_missing_baseline_version_and_policy_change(rebuild, tmp_path):
    """v2 acceptance 4, 6: currentを推測せず、重要Policy変更で止める。"""
    root, development_policy = _project(tmp_path)
    universe, policy = _inputs(rebuild, root, development_policy)
    observation = rebuild.capture_observation(
        project_root=root, data_root=tmp_path / "data", universe=universe,
        policy=policy, head="a" * 40, tool_version="v2",
    )
    candidates = rebuild.build_candidate_run(observation=observation)
    decision = rebuild.write_operational_decision(
        project_root=root, decision_id="DEC-OP-003", candidates=candidates,
        disposition="reuse", human_id="human-1",
    )
    baseline = rebuild.append_baseline(
        project_root=root, observation=observation, candidates=candidates,
        policy=policy, decision=decision,
        entries=({"entry_id": "ENTRY-1", "symbol": "tools.routine.existing"},),
        relations=(), prior=None,
    )
    baseline.entry_paths[0].write_text("tampered", encoding="utf-8")
    with pytest.raises(rebuild.V2ValidationError, match="digest"):
        rebuild.validate_current(project_root=root, observation=observation, policy=policy)
    assert rebuild.classify_policy_change(
        policy=policy, change_class="authority"
    ).status == "revalidation_required"
    with pytest.raises(rebuild.V2ValidationError, match="baseline series"):
        rebuild.validate_baseline_series(versions=(1, 3))


def test_v2_legacy_contract_without_creation_evidence_is_only_evidence_insufficient(
    rebuild, tmp_path
):
    """v2 acceptance 7: 欠落した過去根拠を推測で補わない。"""
    root, _ = _project(tmp_path)
    contract = root / "legacy.json"
    contract.write_text('{"status":"active"}', encoding="utf-8")

    with pytest.raises(rebuild.V2ValidationError, match="creation evidence"):
        rebuild.record_historical_status(
            project_root=root, contract_path=contract, creation_commit=None,
            creation_policy_ref=None, human_decision={"outcome": "completed_historical"},
        )
    status = rebuild.record_historical_status(
        project_root=root, contract_path=contract, creation_commit=None,
        creation_policy_ref=None, human_decision=None,
    )
    assert status.outcome == "evidence_insufficient"
    assert status.permits_current_start is False
