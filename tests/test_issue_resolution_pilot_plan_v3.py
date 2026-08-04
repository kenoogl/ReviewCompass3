"""Issue Resolution早期PilotのPlan v3 state境界Acceptance Test。"""

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
PLAN_V2_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v2.json"
)
PLAN_V3_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v3.json"
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


def _plan_v2():
    return json.loads(
        (PROJECT_ROOT / PLAN_V2_PATH).read_text(encoding="utf-8")
    )


def _item(records, id_field, identifier):
    return next(
        record
        for record in records
        if record[id_field] == identifier
    )


def _plan_v3():
    record = copy.deepcopy(_plan_v2())
    record["plan_version"] = 3
    record["created_at"] = "2026-08-04T10:00:00+09:00"
    record["prohibitions"].append(
        "Task Contractのcontaining commit確認前にWI-001を開始しない"
    )
    _item(record["work_items"], "work_item_id", "WI-006")[
        "expected_outcome"
    ] = (
        "Task Contractのcommit境界とWI-001開始境界を含む最新の非stale "
        "recordだけからstateが一意に決まり、推測を拒否できる。"
    )
    _item(record["acceptance"], "acceptance_id", "ACC-007")[
        "criterion"
    ] = (
        "Task Contractがworking treeにだけ存在すれば"
        "task_contract_commit_pending、containing commit確認済みかつ"
        "WI-001未開始ならimplementation_ready、WI-001のRED開始後だけ"
        "implementation_in_progressとする。"
    )
    oracle = _item(record["oracles"], "oracle_id", "ORACLE-007")
    oracle["method"] = (
        "task_contract_commit_pending、implementation_ready、"
        "implementation_in_progressの正常・負例・境界fixtureを入力する。"
    )
    oracle["expected"] = (
        "未commit、containing commit確認済み、WI-001 RED開始済みが"
        "それぞれ一意の三状態へ写像される。"
    )
    record["task_contract_route_candidates"] = [
        (
            "Task Contractを作成・検証し、containing commit確認後に"
            "WI-001のREDを開始する"
        ),
        "WI-001、WI-002、WI-006、WI-003、WI-004、WI-005を順にrouteする",
    ]
    record["content_digest"] = _canonical_digest(record)
    return record


def _validate(record):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    return pilot.validate_resolution_plan(
        record,
        path=PLAN_V3_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )


def test_accepts_plan_v3_with_preimplementation_state_closure():
    result = _validate(_plan_v3())

    assert result.record_id == "PLAN-PILOT-TODO-GROWTH-001"


def test_rejects_plan_v3_without_preimplementation_state_closure():
    pilot = _module()
    record = _plan_v2()
    record["plan_version"] = 3
    record["created_at"] = "2026-08-04T10:00:00+09:00"
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="pre-implementation state closure",
    ):
        _validate(record)


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("acceptance", "pre-implementation state closure"),
        ("oracle", "pre-implementation state oracle"),
        ("commit_gate", "Task Contract commit gate"),
    ),
)
def test_rejects_incomplete_plan_v3_boundary(mutation, message):
    pilot = _module()
    record = _plan_v3()
    if mutation == "acceptance":
        acceptance = _item(
            record["acceptance"],
            "acceptance_id",
            "ACC-007",
        )
        acceptance["criterion"] = (
            "Task Contract作成後はimplementation_in_progressとする。"
        )
    elif mutation == "oracle":
        oracle = _item(record["oracles"], "oracle_id", "ORACLE-007")
        oracle["method"] = "active stateの正常例だけを検査する。"
        oracle["expected"] = "stateを一件返す。"
    else:
        record["prohibitions"].remove(
            "Task Contractのcontaining commit確認前にWI-001を開始しない"
        )
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(pilot.PilotValidationError, match=message):
        _validate(record)
