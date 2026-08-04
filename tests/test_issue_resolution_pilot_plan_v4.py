"""Issue Resolution早期PilotのPlan v4 snapshot時点Acceptance Test。"""

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
PLAN_V3_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v3.json"
)
PLAN_V4_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v4.json"
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


def _item(records, id_field, identifier):
    return next(
        record
        for record in records
        if record[id_field] == identifier
    )


def _plan_v4():
    record = copy.deepcopy(_load(PLAN_V3_PATH))
    record["plan_version"] = 4
    record["created_at"] = "2026-08-04T12:00:00+09:00"
    record["dependencies"].append(
        "Human current-Issue revision Decision approving option A"
    )
    record["prohibitions"].extend(
        (
            "WI-002とWI-006のcommit前にWI-007の実snapshotを作成しない",
            (
                "WI-007再読込合格後からWI-003の最初のTODO書換えまで"
                "source TODOを変更しない"
            ),
        )
    )

    helper = _item(record["work_items"], "work_item_id", "WI-001")
    helper["objective"] = (
        "TODO byte-exact snapshot helperを固定Testに対してGREENにする。"
    )
    helper["expected_outcome"] = (
        "実TODOを書き換えずsnapshot作成・再読込機能が利用できる。"
    )
    helper["acceptance_ids"] = ["ACC-008"]
    helper["oracle_ids"] = ["ORACLE-008"]
    helper["rollback_step_ids"] = ["RB-003"]

    record["acceptance"].append(
        {
            "acceptance_id": "ACC-008",
            "criterion": (
                "固定WI-001 Test SHA-256を変更せず全件GREENとし、"
                "実TODO snapshotは作成しない。"
            ),
        }
    )
    record["oracles"].append(
        {
            "oracle_id": "ORACLE-008",
            "kind": "fixed_test_identity",
            "method": (
                "RED containing commitのTest SHA-256を再取得して"
                "snapshot helperへ実行する。"
            ),
            "expected": "Test SHA-256不変で9件すべてGREENになる。",
        }
    )
    record["rollback"].append(
        {
            "rollback_step_id": "RB-003",
            "trigger": "snapshot helper Testまたは全Testが失敗する。",
            "action": (
                "実TODOと実snapshotを変更せずhelperを未完了へ戻す。"
            ),
            "verification": (
                "固定Test SHA-256不変、実snapshot不在、全Test合格を確認する。"
            ),
        }
    )

    actual_snapshot = {
        "work_item_id": "WI-007",
        "objective": (
            "WI-003直前のTODOをbyte-exact snapshotと別manifestへ"
            "機械作成し、再読込する。"
        ),
        "depends_on": ["WI-002", "WI-006"],
        "obligation_ids": ["OBL-001"],
        "expected_outcome": (
            "圧縮直前TODOが独立snapshotから同じSHA-256で復元できる。"
        ),
        "acceptance_ids": ["ACC-001"],
        "oracle_ids": ["ORACLE-001"],
        "rollback_step_ids": ["RB-001"],
    }
    projection_index = next(
        index
        for index, item in enumerate(record["work_items"])
        if item["work_item_id"] == "WI-003"
    )
    record["work_items"].insert(projection_index, actual_snapshot)
    projection = _item(record["work_items"], "work_item_id", "WI-003")
    projection["depends_on"].append("WI-007")

    snapshot_acceptance = _item(
        record["acceptance"],
        "acceptance_id",
        "ACC-001",
    )
    snapshot_acceptance["criterion"] = (
        "WI-002とWI-006のcontaining commit確認後かつWI-003直前に、"
        "records/session-handoffs/のbyte-exact snapshotと別manifestが"
        "source TODOのSHA-256、bytes、lines、Claim数を保持する。"
        "WI-007 commitではTODOを変更せず、WI-003開始時の再読込まで"
        "source identityが一致する。"
    )
    snapshot_oracle = _item(
        record["oracles"],
        "oracle_id",
        "ORACLE-001",
    )
    snapshot_oracle["method"] = (
        "WI-007作成時とWI-003開始時にsource、snapshot、manifestを"
        "別々に再読込し、bytes、SHA-256、lines、Claim数を再取得する。"
    )
    snapshot_oracle["expected"] = (
        "二時点でsource identityとsnapshot identityが一致し、"
        "manifest計測値と再計測値が一致する。"
    )
    record["recovery"].append(
        "WI-007後にTODOが変わった場合はWI-003を開始せず、"
        "既存snapshotを上書きせず新しいversioned snapshotを作る。"
    )
    record["task_contract_route_candidates"] = [
        (
            "WI-001 helper GREENを既存Evidenceから確認し、"
            "Plan v4承認後にTask Contract v2へ移送する"
        ),
        (
            "WI-001、WI-002、WI-006、WI-007、WI-003、WI-004、"
            "WI-005を順にrouteする"
        ),
    ]
    record["content_digest"] = _canonical_digest(record)
    return record


def _validate(record):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    return pilot.validate_resolution_plan(
        record,
        path=PLAN_V4_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )


def test_accepts_plan_v4_with_snapshot_timing_closure():
    result = _validate(_plan_v4())

    assert result.record_id == "PLAN-PILOT-TODO-GROWTH-001"


def test_repository_plan_v4_matches_fixed_candidate():
    actual = _load(PLAN_V4_PATH)

    assert actual == _plan_v4()
    assert _validate(actual).content_digest == actual["content_digest"]


def test_rejects_plan_v4_without_actual_snapshot_work_item():
    pilot = _module()
    record = _plan_v4()
    record["work_items"] = [
        item
        for item in record["work_items"]
        if item["work_item_id"] != "WI-007"
    ]
    projection = _item(record["work_items"], "work_item_id", "WI-003")
    projection["depends_on"].remove("WI-007")
    helper = _item(record["work_items"], "work_item_id", "WI-001")
    helper["acceptance_ids"].append("ACC-001")
    helper["oracle_ids"].append("ORACLE-001")
    helper["rollback_step_ids"].append("RB-001")
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="snapshot timing closure",
    ):
        _validate(record)


@pytest.mark.parametrize(
    "mutation",
    (
        "helper_boundary",
        "snapshot_dependencies",
        "projection_dependency",
        "source_guard",
        "acceptance",
        "route_order",
    ),
)
def test_rejects_incomplete_plan_v4_snapshot_boundary(mutation):
    pilot = _module()
    record = _plan_v4()
    helper = _item(record["work_items"], "work_item_id", "WI-001")
    snapshot = _item(record["work_items"], "work_item_id", "WI-007")
    projection = _item(record["work_items"], "work_item_id", "WI-003")
    if mutation == "helper_boundary":
        helper["objective"] = "現行TODOの実snapshotを作成する。"
    elif mutation == "snapshot_dependencies":
        snapshot["depends_on"].remove("WI-006")
    elif mutation == "projection_dependency":
        projection["depends_on"].remove("WI-007")
    elif mutation == "source_guard":
        record["prohibitions"] = [
            value
            for value in record["prohibitions"]
            if "WI-007再読込合格後" not in value
        ]
    elif mutation == "acceptance":
        acceptance = _item(
            record["acceptance"],
            "acceptance_id",
            "ACC-001",
        )
        acceptance["criterion"] = (
            "WI-001でTODO snapshotとmanifestを作成する。"
        )
    else:
        record["task_contract_route_candidates"][-1] = (
            "WI-001、WI-007、WI-002、WI-006、WI-003を順にrouteする"
        )
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="snapshot timing closure",
    ):
        _validate(record)


def test_rejects_plan_v4_without_session_boundary_recovery():
    pilot = _module()
    record = _plan_v4()
    record["recovery"] = [
        value
        for value in record["recovery"]
        if "WI-007後にTODOが変わった場合" not in value
    ]
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        pilot.PilotValidationError,
        match="snapshot timing recovery",
    ):
        _validate(record)
