"""Issue Resolution TODO compaction実装Task Contractの機械検証。"""

import hashlib
import importlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    PROJECT_ROOT
    / "records/task-contract"
    / "issue-resolution-todo-compaction-implementation-v1.json"
)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def _contract():
    return _load(CONTRACT_PATH)


def test_contract_digest_and_fixed_references_are_current():
    contract = _contract()
    references = [
        contract["parent_contract_ref"],
        contract["issue_ref"],
        contract["plan_ref"],
        contract["challenge_ref"],
        contract["approval_decision_ref"],
    ]

    assert contract["content_digest"] == _canonical_digest(contract)
    assert all(
        _sha256(PROJECT_ROOT / reference["path"])
        == reference["sha256"]
        for reference in references
    )
    for reference in references:
        if "content_digest" not in reference:
            continue
        record = _load(PROJECT_ROOT / reference["path"])
        assert record["content_digest"] == reference["content_digest"]

    # 固定sourceは、lifecycle statusとsource pinを解決する共通resolverで検証する。
    # 歴史状態の契約では、受理時点のGit blobまたは明示された`verify_working_tree`で
    # 照合する。stale判定を緩めるものではなく、pinの無い変更済みsourceは停止する。
    pilot = importlib.import_module("tools.development.issue_resolution_pilot")
    count, resolved = pilot.validate_fixed_sources_for_contract(
        CONTRACT_PATH, project_root=PROJECT_ROOT
    )
    assert count == len(contract["fixed_sources"])
    assert resolved >= 1


def test_contract_is_bound_to_approved_plan_v3():
    contract = _contract()
    plan = _load(PROJECT_ROOT / contract["plan_ref"]["path"])
    challenge = _load(PROJECT_ROOT / contract["challenge_ref"]["path"])
    decision = _load(
        PROJECT_ROOT / contract["approval_decision_ref"]["path"]
    )

    assert contract["plan_ref"]["plan_version"] == 3
    assert contract["challenge_ref"]["challenge_version"] == 3
    assert challenge["overall_verdict"] == "ready_for_human_approval"
    assert challenge["blocking_finding_ids"] == []
    assert decision["decision"] == "approve_plan"
    assert decision["plan_ref"]["content_digest"] == plan["content_digest"]
    assert decision["challenge_ref"]["content_digest"] == (
        challenge["content_digest"]
    )


def test_contract_preserves_plan_work_item_order_and_coverage():
    contract = _contract()
    plan = _load(PROJECT_ROOT / contract["plan_ref"]["path"])
    contract_items = contract["work_items"]
    plan_items = {
        item["work_item_id"]: item
        for item in plan["work_items"]
    }
    expected_order = [
        "WI-001",
        "WI-002",
        "WI-006",
        "WI-003",
        "WI-004",
        "WI-005",
    ]

    assert [item["sequence"] for item in contract_items] == list(
        range(1, 7)
    )
    assert [item["work_item_id"] for item in contract_items] == (
        expected_order
    )
    for item in contract_items:
        plan_item = plan_items[item["work_item_id"]]
        for field in (
            "depends_on",
            "obligation_ids",
            "acceptance_ids",
            "oracle_ids",
            "rollback_step_ids",
        ):
            assert item[field] == plan_item[field]
        assert item["objective"] == plan_item["objective"]
        assert item["tdd_boundary"]
        assert item["start_condition"]
        assert item["completion_condition"]


def test_contract_fixes_commit_stable_three_state_projection():
    contract = _contract()
    projection = contract["state_projection"]
    rules = projection["rules"]

    assert contract["current_state_at_creation"] == (
        "task_contract_commit_pending"
    )
    assert [rule["state"] for rule in rules] == [
        "task_contract_commit_pending",
        "implementation_ready",
        "implementation_in_progress",
    ]
    assert "not byte-identical" in rules[0]["condition"]
    assert "byte-identical" in rules[1]["condition"]
    assert "no accepted WI-001 RED" in rules[1]["condition"]
    assert "WI-001 RED start Evidence" in rules[2]["condition"]
    assert "without modifying" in projection["commit_stability"]
    assert "never hand-entered" in projection["authority"]


def test_contract_stops_premature_implementation_and_compaction():
    contract = _contract()
    prohibitions = "\n".join(contract["prohibitions"])
    human_gates = "\n".join(contract["human_gates"])

    assert "containing commit確認前にWI-001を開始しない" in prohibitions
    assert "未コミットのまま次Work Itemへ進めない" in prohibitions
    assert "Digest一致前にTODOを書き換えない" in prohibitions
    assert "Issueをresolvedにしない" in prohibitions
    assert "Resolution VerdictによるIssue解決" in human_gates
    assert contract["next_action"].startswith(
        "Commit and verify this exact Task Contract"
    )
