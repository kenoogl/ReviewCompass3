"""Issue Resolution早期PilotのPlan修復Acceptance Test。"""

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
PLAN_V1_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v1.json"
)
PLAN_V2_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v2.json"
)
CHALLENGE_V1_PATH = (
    ".reviewcompass/workflow/plan-challenges/"
    "challenge-pilot-todo-growth-001--v1.json"
)
CHALLENGE_V2_PATH = (
    ".reviewcompass/workflow/plan-challenges/"
    "challenge-pilot-todo-growth-001--v2.json"
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


def _load(relative_path):
    return json.loads(
        (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
    )


def _plan_v2():
    record = copy.deepcopy(_load(PLAN_V1_PATH))
    record["plan_version"] = 2
    record["created_at"] = "2026-08-04T09:20:00+09:00"
    record["issue_obligations"].append(
        {
            "obligation_id": "OBL-006",
            "statement": (
                "TODOのactive stateを固定recordから機械導出し、"
                "手入力stateを正本にしない。"
            ),
            "source_field": "problem",
        }
    )
    record["work_items"].append(
        {
            "work_item_id": "WI-006",
            "objective": (
                "Candidate、Decision、Issue、Challenge、Task、Verdictから"
                "active stateを導出するresolverをtest-firstで実装する。"
            ),
            "depends_on": ["WI-002"],
            "obligation_ids": ["OBL-006"],
            "expected_outcome": (
                "欠落、競合、stale、手入力不一致を推測せず拒否できる。"
            ),
            "acceptance_ids": ["ACC-007"],
            "oracle_ids": ["ORACLE-007"],
            "rollback_step_ids": ["RB-002"],
        }
    )
    next(
        item
        for item in record["work_items"]
        if item["work_item_id"] == "WI-003"
    )["depends_on"].append("WI-006")
    next(
        acceptance
        for acceptance in record["acceptance"]
        if acceptance["acceptance_id"] == "ACC-002"
    )["criterion"] = (
        "TODOは12288 bytes以下とし、境界Testは12288 bytes合格、"
        "12289 bytes拒否を固定する。"
    )
    next(
        acceptance
        for acceptance in record["acceptance"]
        if acceptance["acceptance_id"] == "ACC-005"
    )["criterion"] = (
        "root CLAUDE.mdは共通promptへのlink-only入口とし、"
        "独立したTODO意味規則を拒否する。"
    )
    record["acceptance"].append(
        {
            "acceptance_id": "ACC-007",
            "criterion": (
                "active stateは最新の非stale固定recordから決定的に導出され、"
                "欠落、競合、手入力不一致は未確定として拒否される。"
            ),
        }
    )
    record["oracles"].append(
        {
            "oracle_id": "ORACLE-007",
            "kind": "derived_state_transition_table",
            "method": (
                "各許可遷移と欠落、競合、stale、手入力不一致fixtureを"
                "resolverへ入力する。"
            ),
            "expected": (
                "許可遷移だけが一意stateを返し、負例はstateを推測せず拒否する。"
            ),
        }
    )
    record["content_digest"] = _canonical_digest(record)
    return record


def test_accepts_versioned_plan_with_derived_state_closure():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _plan_v2()

    result = pilot.validate_resolution_plan(
        record,
        path=PLAN_V2_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )

    assert result.record_id == "PLAN-PILOT-TODO-GROWTH-001"


def test_rejects_version2_plan_without_derived_state_closure():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _load(PLAN_V1_PATH)
    record["plan_version"] = 2
    record["created_at"] = "2026-08-04T09:20:00+09:00"
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="derived state closure",
    ):
        pilot.validate_resolution_plan(
            record,
            path=PLAN_V2_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_version2_plan_without_exact_pilot_boundary():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _plan_v2()
    acceptance = next(
        item
        for item in record["acceptance"]
        if item["acceptance_id"] == "ACC-002"
    )
    acceptance["criterion"] = "TODOは概ね12 KiB以下とする。"
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="Pilot boundary",
    ):
        pilot.validate_resolution_plan(
            record,
            path=PLAN_V2_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_rejects_version2_plan_with_second_claude_authority():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _plan_v2()
    acceptance = next(
        item
        for item in record["acceptance"]
        if item["acceptance_id"] == "ACC-005"
    )
    acceptance["criterion"] = (
        "root CLAUDE.mdに独立したTODO意味規則を記載する。"
    )
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="entrypoint authority",
    ):
        pilot.validate_resolution_plan(
            record,
            path=PLAN_V2_PATH,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_accepts_versioned_plan_challenge():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record = _load(CHALLENGE_V1_PATH)
    record["challenge_version"] = 2
    record["created_at"] = "2026-08-04T09:25:00+09:00"
    record["content_digest"] = _canonical_digest(record)

    result = pilot.validate_plan_challenge(
        record,
        path=CHALLENGE_V2_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )

    assert result.record_id == "CHALLENGE-PILOT-TODO-GROWTH-001"
