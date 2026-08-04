"""Issue Resolution Pilotのactive stateを固定record列から導出する。"""

import dataclasses
import re


_KINDS = (
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
_SHA256 = re.compile(r"[0-9a-f]{64}")
_ALLOWED_STATUS = {
    "candidate": {"open"},
    "triage_decision": {"promote_to_issue"},
    "issue": {"open"},
    "plan": {"proposed"},
    "challenge": {"changes_required", "ready_for_human_approval"},
    "plan_approval": {"approve_plan"},
    "task_contract": {"fixed"},
    "work_start": {"accepted"},
    "implementation_verification": {"accepted"},
    "verdict": {"resolved", "unresolved"},
}


class IssueResolutionStateError(Exception):
    """固定recordからstateを一意かつ安全に導出できない。"""


@dataclasses.dataclass(frozen=True)
class IssueResolutionState:
    state: str
    evidence_ids: tuple
    indeterminate: bool = False


def _error(reason):
    raise IssueResolutionStateError(f"indeterminate: {reason}")


def _validate_record(record):
    if not isinstance(record, dict):
        _error("record is invalid")
    kind = record.get("record_kind")
    if kind not in _KINDS:
        _error("record kind is invalid")
    record_id = record.get("record_id")
    version = record.get("record_version")
    digest = record.get("content_digest")
    bindings = record.get("bindings")
    if (
        not isinstance(record_id, str)
        or not record_id
        or not isinstance(version, int)
        or isinstance(version, bool)
        or version < 1
        or not isinstance(digest, str)
        or not _SHA256.fullmatch(digest)
        or not isinstance(bindings, dict)
        or record.get("status") not in _ALLOWED_STATUS[kind]
    ):
        _error("record is invalid")
    if any(
        binding_kind not in _KINDS
        or not isinstance(binding_digest, str)
        or not _SHA256.fullmatch(binding_digest)
        for binding_kind, binding_digest in bindings.items()
    ):
        _error("record is invalid")


def _select_latest(records):
    grouped = {kind: {} for kind in _KINDS}
    for record in records:
        if not isinstance(record, dict):
            _error("record is invalid")
        kind = record.get("record_kind")
        version = record.get("record_version")
        if (
            kind not in _KINDS
            or not isinstance(version, int)
            or isinstance(version, bool)
            or version < 1
        ):
            _error("record is invalid")
        current = grouped[kind].get(version)
        if current is not None and (
            current.get("record_id") != record.get("record_id")
            or current.get("content_digest")
            != record.get("content_digest")
        ):
            _error("same-version conflict")
        grouped[kind][version] = record
    for record in records:
        _validate_record(record)
    return {
        kind: versions[max(versions)]
        for kind, versions in grouped.items()
        if versions
    }


def _selected_chain(selected):
    present_indexes = [
        index
        for index, kind in enumerate(_KINDS)
        if kind in selected
    ]
    if not present_indexes or present_indexes[0] != 0:
        _error("required record is missing")
    highest = max(present_indexes)
    if present_indexes != list(range(highest + 1)):
        _error("required record is missing")
    chain = [selected[kind] for kind in _KINDS[: highest + 1]]
    if chain[0]["bindings"]:
        _error("stale binding")
    for index, record in enumerate(chain[1:], start=1):
        upstream = chain[index - 1]
        expected = {
            upstream["record_kind"]: upstream["content_digest"]
        }
        if record["bindings"] != expected:
            _error("stale binding")
    return chain


def _derive(chain):
    highest = len(chain) - 1
    if highest == 0:
        return "triage_pending"
    if highest == 1:
        return "issue_creation_pending"
    if highest == 2:
        return "resolution_plan_pending"
    if highest == 3:
        return "plan_challenge_pending"
    challenge = chain[4]
    if challenge["status"] == "changes_required":
        if highest != 4:
            _error("record is invalid")
        return "plan_changes_required"
    if highest == 4:
        return "plan_approval_pending"
    if highest == 5:
        return "task_contract_pending"
    task_contract = chain[6]
    if (
        task_contract.get("in_working_tree") is not True
        or not isinstance(task_contract.get("in_head"), bool)
    ):
        _error("record is invalid")
    if highest == 6:
        return (
            "implementation_ready"
            if task_contract["in_head"]
            else "task_contract_commit_pending"
        )
    if task_contract["in_head"] is not True:
        _error("record is invalid")
    if highest == 7:
        return "implementation_in_progress"
    if highest == 8:
        return "verdict_pending"
    return chain[9]["status"]


def derive_issue_resolution_state(records, *, declared_state=None):
    """最新版の非stale record chainだけからactive stateを導出する。"""

    if not isinstance(records, (list, tuple)) or not records:
        _error("required record is missing")
    selected = _select_latest(records)
    chain = _selected_chain(selected)
    state = _derive(chain)
    if declared_state is not None and declared_state != state:
        _error("declared state mismatch")
    return IssueResolutionState(
        state=state,
        evidence_ids=tuple(record["record_id"] for record in chain),
    )
