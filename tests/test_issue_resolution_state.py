"""WI-006 Issue Resolution active state resolverのAcceptance Test。"""

import hashlib
import importlib

import pytest


KINDS = (
    "candidate",
    "triage_decision",
    "issue",
    "plan",
    "challenge",
    "plan_approval",
    "task_contract",
    "work_start",
    "implementation_verification",
    "verdict",
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_state"
    )


def _digest(kind, version, suffix="current"):
    return hashlib.sha256(
        f"{kind}:{version}:{suffix}".encode("utf-8")
    ).hexdigest()


def _record(
    kind,
    *,
    version=1,
    status="accepted",
    binding=None,
    suffix="current",
    in_working_tree=None,
    in_head=None,
):
    record = {
        "record_kind": kind,
        "record_id": f"{kind.upper()}-PILOT-001-V{version}-{suffix}",
        "record_version": version,
        "content_digest": _digest(kind, version, suffix),
        "status": status,
        "bindings": {},
    }
    if binding is not None:
        record["bindings"] = {
            binding["record_kind"]: binding["content_digest"]
        }
    if in_working_tree is not None:
        record["in_working_tree"] = in_working_tree
    if in_head is not None:
        record["in_head"] = in_head
    return record


def _base_records(*, challenge_status="ready_for_human_approval"):
    records = []
    candidate = _record("candidate", status="open")
    records.append(candidate)
    triage = _record(
        "triage_decision",
        status="promote_to_issue",
        binding=candidate,
    )
    records.append(triage)
    issue = _record("issue", status="open", binding=triage)
    records.append(issue)
    plan = _record("plan", status="proposed", binding=issue)
    records.append(plan)
    challenge = _record(
        "challenge",
        status=challenge_status,
        binding=plan,
    )
    records.append(challenge)
    approval = _record(
        "plan_approval",
        status="approve_plan",
        binding=challenge,
    )
    records.append(approval)
    task = _record(
        "task_contract",
        status="fixed",
        binding=approval,
        in_working_tree=True,
        in_head=True,
    )
    records.append(task)
    work_start = _record(
        "work_start",
        status="accepted",
        binding=task,
    )
    records.append(work_start)
    verification = _record(
        "implementation_verification",
        status="accepted",
        binding=work_start,
    )
    records.append(verification)
    verdict = _record(
        "verdict",
        status="resolved",
        binding=verification,
    )
    records.append(verdict)
    return records


def _records_for(state):
    if state == "triage_pending":
        return _base_records()[:1]
    if state == "issue_creation_pending":
        return _base_records()[:2]
    if state == "resolution_plan_pending":
        return _base_records()[:3]
    if state == "plan_challenge_pending":
        return _base_records()[:4]
    if state == "plan_changes_required":
        return _base_records(challenge_status="changes_required")[:5]
    if state == "plan_approval_pending":
        return _base_records()[:5]
    if state == "task_contract_pending":
        return _base_records()[:6]
    if state == "task_contract_commit_pending":
        records = _base_records()[:7]
        records[-1]["in_head"] = False
        return records
    if state == "implementation_ready":
        return _base_records()[:7]
    if state == "implementation_in_progress":
        return _base_records()[:8]
    if state == "verdict_pending":
        return _base_records()[:9]
    if state in {"resolved", "unresolved"}:
        records = _base_records()
        records[-1]["status"] = state
        return records
    raise AssertionError(f"unknown test state: {state}")


@pytest.mark.parametrize(
    "expected_state",
    (
        "triage_pending",
        "issue_creation_pending",
        "resolution_plan_pending",
        "plan_challenge_pending",
        "plan_changes_required",
        "plan_approval_pending",
        "task_contract_pending",
        "task_contract_commit_pending",
        "implementation_ready",
        "implementation_in_progress",
        "verdict_pending",
        "resolved",
        "unresolved",
    ),
)
def test_derives_each_allowed_state_with_evidence_ids(expected_state):
    records = _records_for(expected_state)

    result = _module().derive_issue_resolution_state(records)

    assert result.state == expected_state
    assert result.evidence_ids == tuple(
        record["record_id"]
        for record in records
    )
    assert result.indeterminate is False


def test_selects_latest_nonstale_version():
    records = _base_records()[:4]
    plan = records[-1]
    old_challenge = _record(
        "challenge",
        version=1,
        status="changes_required",
        binding=plan,
        suffix="old",
    )
    current_challenge = _record(
        "challenge",
        version=2,
        status="ready_for_human_approval",
        binding=plan,
    )
    records.extend((old_challenge, current_challenge))

    result = _module().derive_issue_resolution_state(records)

    assert result.state == "plan_approval_pending"
    assert result.evidence_ids[-1] == current_challenge["record_id"]
    assert old_challenge["record_id"] not in result.evidence_ids


def test_rejects_missing_required_upstream_record():
    records = _base_records()[:3]
    records.pop(1)

    with pytest.raises(
        _module().IssueResolutionStateError,
        match="indeterminate: required record is missing",
    ):
        _module().derive_issue_resolution_state(records)


def test_rejects_same_version_conflict():
    records = _base_records()[:4]
    plan = records[-1]
    records.extend(
        (
            _record("challenge", binding=plan, suffix="a"),
            _record("challenge", binding=plan, suffix="b"),
        )
    )

    with pytest.raises(
        _module().IssueResolutionStateError,
        match="indeterminate: same-version conflict",
    ):
        _module().derive_issue_resolution_state(records)


def test_rejects_stale_binding():
    records = _base_records()[:4]
    records[-1]["bindings"]["issue"] = "0" * 64

    with pytest.raises(
        _module().IssueResolutionStateError,
        match="indeterminate: stale binding",
    ):
        _module().derive_issue_resolution_state(records)


def test_rejects_hand_entered_state_mismatch():
    records = _records_for("implementation_in_progress")

    with pytest.raises(
        _module().IssueResolutionStateError,
        match="indeterminate: declared state mismatch",
    ):
        _module().derive_issue_resolution_state(
            records,
            declared_state="implementation_ready",
        )
