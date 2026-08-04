"""Issue Resolution早期PilotのPlan Challenge Acceptance Test。"""

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    PROJECT_ROOT / "config/development-issue-resolution-pilot-v3.json"
)
ISSUE_PATH = (
    ".reviewcompass/workflow/issues/"
    "issue-pilot-todo-growth-001--v1.json"
)
PLAN_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v1.json"
)
CHALLENGE_PATH = (
    ".reviewcompass/workflow/plan-challenges/"
    "challenge-pilot-todo-growth-001--v1.json"
)
CRITERIA = (
    "obligation_coverage",
    "work_item_granularity",
    "tdd_closure",
    "prohibition_transfer",
    "feasibility_dependencies",
    "oracle_quality",
    "rollback_recovery",
    "stale_binding",
    "pilot_threshold",
    "entrypoint_authority",
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_pilot"
    )


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _challenge():
    issue = json.loads(
        (PROJECT_ROOT / ISSUE_PATH).read_text(encoding="utf-8")
    )
    plan = json.loads(
        (PROJECT_ROOT / PLAN_PATH).read_text(encoding="utf-8")
    )
    record = {
        "record_kind": "plan_challenge",
        "schema_version": 1,
        "challenge_id": "CHALLENGE-PILOT-TODO-GROWTH-001",
        "challenge_version": 1,
        "created_at": "2026-08-04T09:15:00+09:00",
        "reviewer_kind": "llm_semantic_analysis_with_human_gate",
        "independence_status": "human_independent_review_pending",
        "issue_ref": {
            "issue_id": issue["issue_id"],
            "issue_version": issue["issue_version"],
            "path": ISSUE_PATH,
            "sha256": _sha256(PROJECT_ROOT / ISSUE_PATH),
            "content_digest": issue["content_digest"],
        },
        "plan_ref": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
            "path": PLAN_PATH,
            "sha256": _sha256(PROJECT_ROOT / PLAN_PATH),
            "content_digest": plan["content_digest"],
        },
        "criteria_results": [
            {
                "criterion_id": criterion_id,
                "verdict": "pass",
                "rationale": "The fixed Plan provides reviewable material.",
            }
            for criterion_id in CRITERIA
        ],
        "findings": [],
        "blocking_finding_ids": [],
        "overall_verdict": "ready_for_human_approval",
        "stale_binding": False,
        "human_decision_required": True,
        "next_action": "Obtain the independent Human Plan decision.",
        "content_digest": "",
    }
    record["content_digest"] = _canonical_digest(record)
    return record


def test_v3_config_adds_only_plan_challenge_record():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)

    assert config["pilot_version"] == 3
    assert config["directories"]["plan_challenge"] == (
        ".reviewcompass/workflow/plan-challenges"
    )


def test_repository_contains_contiguous_valid_plan_challenge_versions():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    challenge_path = PROJECT_ROOT / CHALLENGE_PATH
    challenge_files = sorted(challenge_path.parent.glob("*.json"))

    assert challenge_path in challenge_files
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in challenge_files
    ]
    results = [
        pilot.validate_record_file(
            path,
            project_root=PROJECT_ROOT,
            config=config,
        )
        for path in challenge_files
    ]
    assert {
        record["challenge_id"]
        for record in records
    } == {"CHALLENGE-PILOT-TODO-GROWTH-001"}
    assert [
        record["challenge_version"]
        for record in records
    ] == list(range(1, len(records) + 1))
    assert {
        result.record_id
        for result in results
    } == {"CHALLENGE-PILOT-TODO-GROWTH-001"}
    assert records[0]["overall_verdict"] == "changes_required"
    assert records[0]["blocking_finding_ids"] == ["PC-BLOCK-001"]
    assert records[-1]["overall_verdict"] == "ready_for_human_approval"
    assert records[-1]["blocking_finding_ids"] == []


def test_validates_ready_plan_challenge():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()

    result = pilot.validate_plan_challenge(
        record,
        path=CHALLENGE_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )

    assert result.record_id == "CHALLENGE-PILOT-TODO-GROWTH-001"


def test_rejects_challenge_bound_to_stale_plan():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()
    record["plan_ref"]["sha256"] = "0" * 64
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match="Plan reference"):
        pilot.validate_plan_challenge(
            record,
            path=CHALLENGE_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_missing_challenge_criterion():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()
    record["criteria_results"].pop()
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match="criteria"):
        pilot.validate_plan_challenge(
            record,
            path=CHALLENGE_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_blocking_criterion_without_finding():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()
    record["criteria_results"][0]["verdict"] = "block"
    record["overall_verdict"] = "changes_required"
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match="blocking Finding"):
        pilot.validate_plan_challenge(
            record,
            path=CHALLENGE_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_ready_verdict_with_blocking_finding():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()
    record["criteria_results"][0]["verdict"] = "block"
    record["findings"] = [
        {
            "finding_id": "PC-BLOCK-001",
            "severity": "blocking",
            "criterion_id": "obligation_coverage",
            "statement": "A required obligation is missing.",
            "required_action": "Revise the Plan before approval.",
        }
    ]
    record["blocking_finding_ids"] = ["PC-BLOCK-001"]
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match="overall verdict"):
        pilot.validate_plan_challenge(
            record,
            path=CHALLENGE_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_challenge_that_bypasses_human_decision():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _challenge()
    record["human_decision_required"] = False
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match="Human decision"):
        pilot.validate_plan_challenge(
            record,
            path=CHALLENGE_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )
