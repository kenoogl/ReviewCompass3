"""Issue Resolution TODO compaction Task Contract v2のAcceptance Test。"""

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_V1_PATH = (
    "records/task-contract/"
    "issue-resolution-todo-compaction-implementation-v1.json"
)
CONTRACT_V2_PATH = (
    "records/task-contract/"
    "issue-resolution-todo-compaction-implementation-v2.json"
)
PLAN_V4_PATH = (
    ".reviewcompass/workflow/resolution-plans/"
    "plan-pilot-todo-growth-001--v4.json"
)
CHALLENGE_V4_PATH = (
    ".reviewcompass/workflow/plan-challenges/"
    "challenge-pilot-todo-growth-001--v4.json"
)
DECISION_V4_PATH = (
    "records/development/"
    "2026-08-04-issue-resolution-pilot-plan-challenge-v4-decision.json"
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_pilot"
    )


def _load(relative_path):
    return json.loads(
        (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
    )


def _sha256(relative_path):
    return hashlib.sha256(
        (PROJECT_ROOT / relative_path).read_bytes()
    ).hexdigest()


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


def _file_ref(relative_path, record=None):
    reference = {
        "path": relative_path,
        "sha256": _sha256(relative_path),
    }
    if record is not None:
        reference["content_digest"] = record["content_digest"]
    return reference


def _work_item(plan_item, *, sequence, status, boundaries):
    return {
        "sequence": sequence,
        "work_item_id": plan_item["work_item_id"],
        "depends_on": plan_item["depends_on"],
        "objective": plan_item["objective"],
        "obligation_ids": plan_item["obligation_ids"],
        "acceptance_ids": plan_item["acceptance_ids"],
        "oracle_ids": plan_item["oracle_ids"],
        "rollback_step_ids": plan_item["rollback_step_ids"],
        "status_at_creation": status,
        "tdd_boundary": boundaries[0],
        "start_condition": boundaries[1],
        "completion_condition": boundaries[2],
    }


def _contract_v2():
    previous = _load(CONTRACT_V1_PATH)
    plan = _load(PLAN_V4_PATH)
    challenge = _load(CHALLENGE_V4_PATH)
    decision = _load(DECISION_V4_PATH)
    plan_items = {
        item["work_item_id"]: item
        for item in plan["work_items"]
    }
    order = (
        "WI-001",
        "WI-002",
        "WI-006",
        "WI-007",
        "WI-003",
        "WI-004",
        "WI-005",
    )
    boundaries = {
        "WI-001": (
            "固定snapshot helper TestのRED containing commitを変更せずGREENにする",
            "Task Contract v1 containing commit確認済み",
            "固定Test 9件GREEN、実snapshot不在、completion Evidenceとcontaining commit一致",
        ),
        "WI-002": (
            "12288 bytes合格、12289 bytes拒否を含む正常・負例・境界Testを先にREDへする",
            "Task Contract v2 containing commit、WI-001繰越Evidence、clean transition確認済み",
            "既知違反fixtureだけを意図した理由で拒否し、決定的restoreが一致する",
        ),
        "WI-006": (
            "全許可遷移、欠落、競合、stale、手入力不一致を先にREDへする",
            "WI-002 completed and committed",
            "最新の非stale固定recordだけから一意stateと根拠IDsを返し、負例を推測しない",
        ),
        "WI-007": (
            "source一致、source変更、既存出力衝突、versioned再作成境界を実行前に固定する",
            "WI-002とWI-006 completed and committed、clean worktree、最新TODO source identity確認",
            "snapshot／manifest再読込一致、containing commitはTODOを変更せず、WI-003用source identityを固定",
        ),
        "WI-003": (
            "生成器とprojection validatorの期待出力を固定し、source再照合後だけTODOへ書く",
            "WI-007 containing commit確認、TODO source identity再読込一致、clean worktree",
            "TODOは12288 bytes以下、active Issue一件、過去Claim・詳細履歴0、全参照解決済み",
        ),
        "WI-004": (
            "共通prompt一件、各入口参照一件、CLAUDE.md第二authority拒否Testを先にREDへする",
            "WI-002 completed and committed",
            "重複TODO意味規則0で、CodexとClaude入口が同じpromptだけを参照する",
        ),
        "WI-005": (
            "post-write、restore rehearsal、stale閉包、Verdict入力の受入条件を実施前に固定する",
            "WI-003 and WI-004 completed and committed",
            "公式全Test、再読込、参照、restoreが合格し、Verdict候補が残余riskを記録する",
        ),
    }
    record = copy.deepcopy(previous)
    record["task_contract_id"] = (
        "TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V2"
    )
    record["task_contract_version"] = 2
    record["created_at"] = "2026-08-04T12:20:00+09:00"
    record["goal"] = (
        "承認済みPlan v4をtest-firstで実施し、TODO_NEXT_SESSION.mdを"
        "復元可能性とauthorityを保った短いactive Issue入口へ一回だけ圧縮する。"
    )
    record["supersedes_contract_ref"] = {
        "task_contract_id": previous["task_contract_id"],
        "task_contract_version": previous["task_contract_version"],
        **_file_ref(CONTRACT_V1_PATH, previous),
    }
    record["plan_ref"] = {
        "plan_id": plan["plan_id"],
        "plan_version": plan["plan_version"],
        **_file_ref(PLAN_V4_PATH, plan),
    }
    record["challenge_ref"] = {
        "challenge_id": challenge["challenge_id"],
        "challenge_version": challenge["challenge_version"],
        **_file_ref(CHALLENGE_V4_PATH, challenge),
    }
    record["approval_decision_ref"] = {
        "decision_id": decision["decision_id"],
        "decision_version": decision["decision_version"],
        **_file_ref(DECISION_V4_PATH, decision),
    }
    record["fixed_sources"] = [
        {
            **_file_ref(
                "records/development/"
                "2026-08-04-issue-resolution-pilot-wi-001-"
                "snapshot-boundary-decision.json",
                _load(
                    "records/development/"
                    "2026-08-04-issue-resolution-pilot-wi-001-"
                    "snapshot-boundary-decision.json"
                ),
            )
        },
        {
            **_file_ref(
                "records/development/"
                "2026-08-04-issue-resolution-pilot-plan-v4-"
                "green-test-receipt-v1.json"
            )
        },
        previous["fixed_sources"][-1],
    ]
    record["carried_forward_work"] = {
        "work_item_id": "WI-001",
        "status": "completed_carried_forward",
        "containing_commit": (
            "64782ec4e94422462e093f7492d9f87197b37a6d"
        ),
        "source_contract_ref": {
            "task_contract_id": previous["task_contract_id"],
            "task_contract_version": previous["task_contract_version"],
            **_file_ref(CONTRACT_V1_PATH, previous),
        },
        "test_ref": _file_ref("tests/test_todo_snapshot.py"),
        "implementation_ref": _file_ref(
            "tools/development/todo_snapshot.py"
        ),
        "evidence_ref": _file_ref(
            "records/development/"
            "2026-08-04-issue-resolution-pilot-wi-001-"
            "snapshot-boundary-triage-completion-evidence-v1.md"
        ),
        "actual_snapshot_created": False,
    }
    record["state_projection"]["rules"][0]["condition"] = (
        "this exact Task Contract v2 exists in the working tree but is not byte-identical at its path in HEAD"
    )
    record["state_projection"]["rules"][1]["condition"] = (
        "this exact Task Contract v2 is byte-identical at its path in HEAD and no accepted WI-001 completion Evidence exists"
    )
    record["state_projection"]["rules"][2]["condition"] = (
        "the Task Contract v2 containing commit is verified and accepted carried-forward WI-001 completion Evidence exists"
    )
    record["work_items"] = [
        _work_item(
            plan_items[work_item_id],
            sequence=index,
            status=(
                "completed_carried_forward"
                if work_item_id == "WI-001"
                else "not_started"
            ),
            boundaries=boundaries[work_item_id],
        )
        for index, work_item_id in enumerate(order, start=1)
    ]
    record["prohibitions"] = [
        "Task Contract v2のcontaining commit確認前にWI-002を開始しない",
        "完了済みWork Itemを未コミットのまま次Work Itemへ進めない",
        "WI-002とWI-006のcommit前にWI-007の実snapshotを作成しない",
        "WI-007 containing commitでTODO sourceを変更しない",
        "WI-007後にsource identityが変わった場合はWI-003を開始せず新しいversioned snapshotを作る",
        "active state、Digest、bytes、lines、Claim数をLLMの手入力で正本化しない",
        "Plan v4、Challenge v4、Approval Decision、Task Contract v1、固定WI-001 Testをin-place変更しない",
        "green TestまたはcommitだけでIssueをresolvedにしない",
        "外部送信、hook、watcher、scheduler、background serviceを有効化しない",
    ]
    record["next_action"] = (
        "Commit and verify this exact Task Contract v2, derive implementation_in_progress from carried-forward WI-001 Evidence, then begin WI-002 RED as a separate work unit."
    )
    record["content_digest"] = _canonical_digest(record)
    return record


def _validate(record):
    return _module().validate_implementation_task_contract_v2(
        record,
        project_root=PROJECT_ROOT,
    )


def test_accepts_task_contract_v2_with_carried_forward_wi001():
    result = _validate(_contract_v2())

    assert result.record_id == (
        "TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V2"
    )


def test_repository_task_contract_v2_matches_fixed_candidate():
    actual = _load(CONTRACT_V2_PATH)

    assert actual == _contract_v2()
    assert _validate(actual).content_digest == actual["content_digest"]


def test_rejects_task_contract_v2_with_stale_plan_binding():
    record = _contract_v2()
    record["plan_ref"]["sha256"] = "0" * 64
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        _module().PilotValidationError,
        match="Task Contract v2 reference",
    ):
        _validate(record)


def test_rejects_task_contract_v2_without_wi001_completion():
    record = _contract_v2()
    record["carried_forward_work"]["status"] = "not_started"
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        _module().PilotValidationError,
        match="WI-001 carry-forward",
    ):
        _validate(record)


def test_rejects_task_contract_v2_with_stale_goal_plan_version():
    record = _contract_v2()
    record["goal"] = record["goal"].replace("Plan v4", "Plan v3")
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        _module().PilotValidationError,
        match="Task Contract v2 Plan authority",
    ):
        _validate(record)


def test_rejects_task_contract_v2_wrong_work_item_order():
    record = _contract_v2()
    record["work_items"][3], record["work_items"][4] = (
        record["work_items"][4],
        record["work_items"][3],
    )
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        _module().PilotValidationError,
        match="Task Contract v2 work item order",
    ):
        _validate(record)


@pytest.mark.parametrize(
    "mutation",
    ("wi007_todo_write", "wi003_source_check", "early_wi002"),
)
def test_rejects_task_contract_v2_incomplete_execution_boundary(mutation):
    record = _contract_v2()
    items = {
        item["work_item_id"]: item
        for item in record["work_items"]
    }
    if mutation == "wi007_todo_write":
        items["WI-007"]["completion_condition"] = (
            "snapshotをcommitしてTODOへ完了を追記する"
        )
    elif mutation == "wi003_source_check":
        items["WI-003"]["start_condition"] = (
            "WI-007 completed and committed"
        )
    else:
        record["prohibitions"] = [
            value
            for value in record["prohibitions"]
            if "containing commit確認前にWI-002" not in value
        ]
    record["content_digest"] = _canonical_digest(record)

    with pytest.raises(
        _module().PilotValidationError,
        match="Task Contract v2 execution boundary",
    ):
        _validate(record)
