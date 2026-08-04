"""Issue Resolution早期PilotのIssue／Plan Acceptance Test。"""

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    PROJECT_ROOT / "config/development-issue-resolution-pilot-v2.json"
)
ISSUE_PATH = (
    PROJECT_ROOT
    / ".reviewcompass/workflow/issues"
    / "issue-pilot-todo-growth-001--v1.json"
)
PLAN_PATH = (
    PROJECT_ROOT
    / ".reviewcompass/workflow/resolution-plans"
    / "plan-pilot-todo-growth-001--v1.json"
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_pilot"
    )


def _canonical_digest(record):
    payload = {
        key: value
        for key, value in record.items()
        if key != "content_digest"
    }
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_ref(project_root, relative_path):
    return {
        "path": relative_path,
        "sha256": _sha256(project_root / relative_path),
    }


def _candidate_and_decision(project_root):
    source_path = "records/development/observation-v1.json"
    _write_json(
        project_root / source_path,
        {
            "observation_id": "OBS-PILOT-TODO-GROWTH-001",
            "status": "fixed_pilot_source",
        },
    )
    candidate_path = (
        ".reviewcompass/workflow/improvement-candidates/"
        "ic-pilot-todo-growth-001--v1.json"
    )
    candidate = {
        "record_kind": "improvement_candidate",
        "schema_version": 1,
        "candidate_id": "IC-PILOT-TODO-GROWTH-001",
        "candidate_version": 1,
        "created_at": "2026-08-04T08:30:00+09:00",
        "source_work": "inter-work/issue-resolution-early-pilot",
        "source_identity": {
            "kind": "observation",
            "source_id": "OBS-PILOT-TODO-GROWTH-001",
            "source_version": 1,
            **_file_ref(project_root, source_path),
        },
        "problem": "TODO contains accumulated historical claims.",
        "impact": ["current handoff is difficult to scan"],
        "scope": ["one development-only Pilot subject"],
        "non_scope": ["formal product Issue schema"],
        "classification_candidates": ["process_improvement"],
        "route_candidates": ["issue_resolution"],
        "consumer_candidates": ["reviewcompass3-development"],
        "evidence_refs": [_file_ref(project_root, source_path)],
        "proposed_action": "Obtain a Human Triage Decision.",
        "content_digest": "",
    }
    candidate["content_digest"] = _canonical_digest(candidate)
    _write_json(project_root / candidate_path, candidate)
    decision_path = (
        ".reviewcompass/workflow/triage-decisions/"
        "dec-pilot-todo-growth-001--v1.json"
    )
    decision = {
        "record_kind": "human_triage_decision",
        "schema_version": 1,
        "decision_id": "DEC-PILOT-TODO-GROWTH-001",
        "decision_version": 1,
        "decided_at": "2026-08-04T08:35:00+09:00",
        "decision_maker": "human",
        "candidate_ref": {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["candidate_version"],
            **_file_ref(project_root, candidate_path),
            "content_digest": candidate["content_digest"],
        },
        "disposition": "issue_resolution",
        "blocking": False,
        "rationale": "Human approved one durable Issue subject.",
        "selected_consumer": "reviewcompass3-development",
        "next_action": "Create the approved Issue Record.",
        "issue_promotion": {
            "approved": True,
            "issue_id": "ISSUE-PILOT-TODO-GROWTH-001",
        },
        "content_digest": "",
    }
    decision["content_digest"] = _canonical_digest(decision)
    _write_json(project_root / decision_path, decision)
    return source_path, candidate, candidate_path, decision, decision_path


def _issue(project_root):
    (
        source_path,
        candidate,
        candidate_path,
        decision,
        decision_path,
    ) = _candidate_and_decision(project_root)
    record = {
        "record_kind": "issue_record",
        "schema_version": 1,
        "issue_id": "ISSUE-PILOT-TODO-GROWTH-001",
        "issue_version": 1,
        "created_at": "2026-08-04T09:00:00+09:00",
        "source_work": "inter-work/issue-resolution-early-pilot",
        "source_identity": {
            "kind": "observation",
            "source_id": "OBS-PILOT-TODO-GROWTH-001",
            "source_version": 1,
            **_file_ref(project_root, source_path),
        },
        "candidate_ref": {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["candidate_version"],
            **_file_ref(project_root, candidate_path),
            "content_digest": candidate["content_digest"],
        },
        "triage_decision_ref": {
            "decision_id": decision["decision_id"],
            "decision_version": decision["decision_version"],
            **_file_ref(project_root, decision_path),
            "content_digest": decision["content_digest"],
        },
        "problem": "TODO contains accumulated history and keeps growing.",
        "motivation": "Restore a short and reliable current handoff.",
        "impact": ["current state is difficult to recover"],
        "scope": ["one TODO growth Issue subject"],
        "non_scope": ["bulk migration of historical findings"],
        "evidence_refs": [
            _file_ref(project_root, source_path),
            _file_ref(project_root, candidate_path),
            _file_ref(project_root, decision_path),
        ],
        "related_files": ["TODO_NEXT_SESSION.md"],
        "related_units": [
            "TC-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1"
        ],
        "owner_candidate": "reviewcompass3-development",
        "route_candidate": "issue_resolution_plan",
        "content_digest": "",
    }
    record["content_digest"] = _canonical_digest(record)
    path = (
        ".reviewcompass/workflow/issues/"
        "issue-pilot-todo-growth-001--v1.json"
    )
    return record, path


def _resolution_plan(project_root):
    issue, issue_path = _issue(project_root)
    _write_json(project_root / issue_path, issue)
    record = {
        "record_kind": "issue_resolution_plan",
        "schema_version": 1,
        "plan_id": "PLAN-PILOT-TODO-GROWTH-001",
        "plan_version": 1,
        "created_at": "2026-08-04T09:05:00+09:00",
        "issue_ref": {
            "issue_id": issue["issue_id"],
            "issue_version": issue["issue_version"],
            **_file_ref(project_root, issue_path),
            "content_digest": issue["content_digest"],
        },
        "goal": "Create a short current handoff without losing Evidence.",
        "scope": ["snapshot and compact the root TODO after challenge"],
        "non_scope": ["formal product Issue schema"],
        "prohibitions": ["do not compact TODO before Plan Challenge"],
        "dependencies": ["Human Plan Challenge approval"],
        "issue_obligations": [
            {
                "obligation_id": "OBL-001",
                "statement": "Preserve the full pre-compaction TODO.",
                "source_field": "scope",
            },
            {
                "obligation_id": "OBL-002",
                "statement": "Produce a compact active-ID handoff.",
                "source_field": "problem",
            },
        ],
        "work_items": [
            {
                "work_item_id": "WI-001",
                "objective": "Create an immutable milestone snapshot.",
                "depends_on": [],
                "obligation_ids": ["OBL-001"],
                "expected_outcome": "Pre-compaction TODO is recoverable.",
                "acceptance_ids": ["ACC-001"],
                "oracle_ids": ["ORACLE-001"],
                "rollback_step_ids": ["RB-001"],
            },
            {
                "work_item_id": "WI-002",
                "objective": "Compact TODO to current active IDs.",
                "depends_on": ["WI-001"],
                "obligation_ids": ["OBL-002"],
                "expected_outcome": "Root TODO contains no history log.",
                "acceptance_ids": ["ACC-002"],
                "oracle_ids": ["ORACLE-002"],
                "rollback_step_ids": ["RB-001"],
            },
        ],
        "acceptance": [
            {
                "acceptance_id": "ACC-001",
                "criterion": "Snapshot Digest matches pre-compaction TODO.",
            },
            {
                "acceptance_id": "ACC-002",
                "criterion": "TODO contains only the active Issue projection.",
            },
        ],
        "oracles": [
            {
                "oracle_id": "ORACLE-001",
                "kind": "digest",
                "method": "Compare snapshot and source SHA-256.",
                "expected": "Digests are identical.",
            },
            {
                "oracle_id": "ORACLE-002",
                "kind": "validator",
                "method": "Run the TODO projection validator.",
                "expected": "One known Issue ID and no detailed history.",
            },
        ],
        "risks": ["Compaction could remove the only Evidence reference."],
        "deployment": ["Repository-local documentation change only."],
        "rollback": [
            {
                "rollback_step_id": "RB-001",
                "trigger": "Any post-write validator fails.",
                "action": "Restore TODO from the milestone snapshot.",
                "verification": "Restored SHA-256 matches the snapshot.",
            }
        ],
        "recovery": ["Retain an unresolved Verdict if compaction fails."],
        "task_contract_route_candidates": [
            "TODO compaction implementation Task Contract"
        ],
        "content_digest": "",
    }
    record["content_digest"] = _canonical_digest(record)
    path = (
        ".reviewcompass/workflow/resolution-plans/"
        "plan-pilot-todo-growth-001--v1.json"
    )
    return record, path


def test_v2_config_adds_only_issue_and_resolution_plan_records():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)

    assert config["pilot_version"] == 2
    assert config["maximum_issue_subjects"] == 1
    assert config["directories"]["issue_record"] == (
        ".reviewcompass/workflow/issues"
    )
    assert config["directories"]["issue_resolution_plan"] == (
        ".reviewcompass/workflow/resolution-plans"
    )


def test_repository_contains_one_valid_issue_and_plan():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    issue_files = sorted(ISSUE_PATH.parent.glob("*.json"))
    plan_files = sorted(PLAN_PATH.parent.glob("*.json"))

    assert issue_files == [ISSUE_PATH]
    assert plan_files == [PLAN_PATH]
    issue_result = pilot.validate_record_file(
        ISSUE_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )
    plan_result = pilot.validate_record_file(
        PLAN_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )
    assert issue_result.record_id == "ISSUE-PILOT-TODO-GROWTH-001"
    assert plan_result.record_id == "PLAN-PILOT-TODO-GROWTH-001"


def test_validates_issue_against_human_promotion(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    issue, path = _issue(tmp_path)

    result = pilot.validate_issue(
        issue,
        path=path,
        project_root=tmp_path,
        config=config,
    )

    assert result.record_id == "ISSUE-PILOT-TODO-GROWTH-001"
    assert result.content_digest == issue["content_digest"]


@pytest.mark.parametrize(
    ("mutation", "path_change", "message"),
    [
        (
            lambda record: record.update(issue_id="ISSUE-OTHER-001"),
            None,
            "Issue promotion",
        ),
        (
            lambda record: record["triage_decision_ref"].update(
                sha256="0" * 64
            ),
            None,
            "triage decision reference",
        ),
        (
            lambda record: record.update(current_status="open"),
            None,
            "fields",
        ),
        (
            lambda record: None,
            ".reviewcompass/workflow/issues/wrong.json",
            "record path",
        ),
    ],
)
def test_rejects_unapproved_stale_or_mutable_issue(
    tmp_path,
    mutation,
    path_change,
    message,
):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    issue, path = _issue(tmp_path)
    mutation(issue)
    issue["content_digest"] = _canonical_digest(issue)

    with pytest.raises(pilot.PilotValidationError, match=message):
        pilot.validate_issue(
            issue,
            path=path_change or path,
            project_root=tmp_path,
            config=config,
        )


def test_validates_resolution_plan_coverage_and_oracles(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    plan, path = _resolution_plan(tmp_path)

    result = pilot.validate_resolution_plan(
        plan,
        path=path,
        project_root=tmp_path,
        config=config,
    )

    assert result.record_id == "PLAN-PILOT-TODO-GROWTH-001"
    assert result.content_digest == plan["content_digest"]


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("scope", "scope"),
        ("prohibitions", "prohibitions"),
        ("issue_obligations", "issue obligations"),
        ("work_items", "work items"),
        ("acceptance", "Acceptance"),
        ("oracles", "oracles"),
        ("rollback", "rollback"),
    ],
)
def test_rejects_plan_missing_challenge_material(tmp_path, field, message):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    plan, path = _resolution_plan(tmp_path)
    plan[field] = []
    plan["content_digest"] = _canonical_digest(plan)

    with pytest.raises(pilot.PilotValidationError, match=message):
        pilot.validate_resolution_plan(
            plan,
            path=path,
            project_root=tmp_path,
            config=config,
        )


def test_rejects_unknown_plan_coverage_reference(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    plan, path = _resolution_plan(tmp_path)
    plan["work_items"][0]["acceptance_ids"] = ["ACC-UNKNOWN"]
    plan["content_digest"] = _canonical_digest(plan)

    with pytest.raises(pilot.PilotValidationError, match="coverage reference"):
        pilot.validate_resolution_plan(
            plan,
            path=path,
            project_root=tmp_path,
            config=config,
        )


def test_rejects_plan_bound_to_stale_issue(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    plan, path = _resolution_plan(tmp_path)
    plan["issue_ref"]["sha256"] = "0" * 64
    plan["content_digest"] = _canonical_digest(plan)

    with pytest.raises(pilot.PilotValidationError, match="Issue reference"):
        pilot.validate_resolution_plan(
            plan,
            path=path,
            project_root=tmp_path,
            config=config,
        )
