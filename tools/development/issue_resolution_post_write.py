"""WI-005のpost-write検証、隔離restore rehearsal、Verdict候補検証。"""

import dataclasses
import hashlib
import json
import re
import tempfile
from pathlib import Path

from tools.development.issue_resolution_state import (
    IssueResolutionStateError,
    derive_issue_resolution_state,
)
from tools.development.todo_compaction import (
    restore_todo_from_snapshot,
    validate_compacted_todo,
)
from tools.development.todo_handoff import (
    validate_commit_stable_git_section,
)


_REFERENCE = re.compile(
    r"^- \[[^\]\n]+\]\((?P<path>[^)\n]+)\)"
    r" — SHA-256 `(?P<digest>[0-9a-f]{64})`$",
    re.MULTILINE,
)
_CANDIDATE_FIELDS = {
    "record_kind",
    "schema_version",
    "verdict_candidate_id",
    "candidate_version",
    "created_at",
    "issue_ref",
    "plan_ref",
    "task_contract_ref",
    "verification_refs",
    "acceptance_results",
    "unresolved_items",
    "residual_risks",
    "recommendation",
    "recommendation_rationale",
    "human_decision_required",
    "effective_outcome",
    "state_chain",
    "derived_state",
    "content_digest",
}
_VERDICT_FIELDS = {
    "record_kind",
    "schema_version",
    "verdict_id",
    "verdict_version",
    "decided_at",
    "decision_maker",
    "candidate_ref",
    "issue_ref",
    "outcome",
    "rationale",
    "accepted_residual_risks",
    "unresolved_item_dispositions",
    "evidence_refs",
    "content_digest",
}


class PostWriteVerificationError(Exception):
    """WI-005の固定検証境界を満たさない。"""


@dataclasses.dataclass(frozen=True)
class PostWriteVerification:
    todo_sha256: str
    todo_bytes: int
    active_ids: tuple
    reference_count: int
    snapshot_sha256: str
    restore_action: str
    current_todo_preserved: bool


@dataclasses.dataclass(frozen=True)
class VerdictCandidateValidation:
    verdict_candidate_id: str
    recommended_outcome: str
    effective_outcome: str
    derived_state: str


@dataclasses.dataclass(frozen=True)
class ResolutionVerdictValidation:
    verdict_id: str
    outcome: str
    derived_state: str


from tools.common.digests import sha256_hex as _sha256


from tools.common.digests import canonical_content_digest as canonical_digest


def _project_path(project_root, relative_path):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute() or not path.parts:
        raise PostWriteVerificationError("project reference is invalid")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise PostWriteVerificationError(
            "project reference is invalid"
        ) from error
    return resolved


def _validate_ref(reference, project_root):
    if not isinstance(reference, dict) or set(reference) != {
        "path",
        "sha256",
    }:
        raise PostWriteVerificationError("record reference is invalid")
    path = _project_path(project_root, reference["path"])
    try:
        content = path.read_bytes()
    except OSError as error:
        raise PostWriteVerificationError(
            "record reference is invalid"
        ) from error
    if _sha256(content) != reference["sha256"]:
        raise PostWriteVerificationError("record reference is stale")


def validate_todo_reference_digests(document, *, project_root):
    """TODOに表示したpathとDigestを実fileへ照合する。"""

    if not isinstance(document, bytes):
        raise PostWriteVerificationError("TODO must be bytes")
    try:
        text = document.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PostWriteVerificationError("TODO is not UTF-8") from error
    matches = tuple(_REFERENCE.finditer(text))
    if not matches:
        raise PostWriteVerificationError("TODO reference digest is missing")
    for match in matches:
        relative_path = match.group("path")
        expected = match.group("digest")
        path = _project_path(project_root, relative_path)
        try:
            actual = _sha256(path.read_bytes())
        except OSError as error:
            raise PostWriteVerificationError(
                "TODO reference digest mismatch"
            ) from error
        if actual != expected:
            raise PostWriteVerificationError(
                "TODO reference digest mismatch"
            )
    return len(matches)


def verify_post_write(
    *,
    project_root,
    todo_path,
    snapshot_path,
    manifest_path,
    known_active_ids,
):
    """現行TODOを再読込し、checkout外の一時rootで復元をrehearseする。"""

    root = Path(project_root).resolve()
    todo = _project_path(root, todo_path)
    before = todo.read_bytes()
    compact = validate_compacted_todo(
        before,
        project_root=root,
        known_active_ids=known_active_ids,
    )
    stable = validate_commit_stable_git_section(before.decode("utf-8"))
    if stable.status != "passed":
        raise PostWriteVerificationError("TODO commit stability failed")
    reference_count = validate_todo_reference_digests(
        before,
        project_root=root,
    )
    snapshot = _project_path(root, snapshot_path)
    manifest = _project_path(root, manifest_path)

    with tempfile.TemporaryDirectory() as temporary:
        rehearsal_root = Path(temporary)
        rehearsal_todo = rehearsal_root / todo_path
        rehearsal_snapshot = rehearsal_root / snapshot_path
        rehearsal_manifest = rehearsal_root / manifest_path
        rehearsal_todo.parent.mkdir(parents=True, exist_ok=True)
        rehearsal_snapshot.parent.mkdir(parents=True, exist_ok=True)
        rehearsal_manifest.parent.mkdir(parents=True, exist_ok=True)
        rehearsal_todo.write_bytes(before)
        rehearsal_snapshot.write_bytes(snapshot.read_bytes())
        rehearsal_manifest.write_bytes(manifest.read_bytes())
        restored = restore_todo_from_snapshot(
            project_root=rehearsal_root,
            source_path=todo_path,
            snapshot_path=snapshot_path,
            manifest_path=manifest_path,
        )
        rehearsal_todo.write_bytes(before)
        if rehearsal_todo.read_bytes() != before:
            raise PostWriteVerificationError(
                "current TODO recovery mismatch"
            )

    preserved = todo.read_bytes() == before
    if not preserved:
        raise PostWriteVerificationError("current TODO was modified")
    return PostWriteVerification(
        todo_sha256=_sha256(before),
        todo_bytes=compact.bytes_count,
        active_ids=compact.active_ids,
        reference_count=reference_count,
        snapshot_sha256=restored.source_sha256,
        restore_action=restored.action,
        current_todo_preserved=preserved,
    )


def validate_resolution_verdict_candidate(record, *, project_root):
    """Human判断前のVerdict候補とEvidence／state bindingを検証する。"""

    if not isinstance(record, dict) or set(record) != _CANDIDATE_FIELDS:
        raise PostWriteVerificationError("Verdict candidate fields are invalid")
    if (
        record["record_kind"] != "resolution_verdict_candidate"
        or record["schema_version"] != 1
        or record["candidate_version"] != 1
        or record["content_digest"] != canonical_digest(record)
    ):
        raise PostWriteVerificationError("Verdict candidate identity is invalid")
    for reference in (
        record["issue_ref"],
        record["plan_ref"],
        record["task_contract_ref"],
        *record["verification_refs"],
    ):
        _validate_ref(reference, project_root)
    if (
        not isinstance(record["acceptance_results"], list)
        or not record["acceptance_results"]
        or any(
            result.get("status") != "passed"
            for result in record["acceptance_results"]
        )
    ):
        raise PostWriteVerificationError("Acceptance result is invalid")
    if not isinstance(record["unresolved_items"], list) or not record["unresolved_items"]:
        raise PostWriteVerificationError("unresolved item record is required")
    if not isinstance(record["residual_risks"], list) or not record["residual_risks"]:
        raise PostWriteVerificationError("residual risk is required")
    if (
        record["human_decision_required"] is not True
        or record["effective_outcome"] != "pending_human_decision"
    ):
        raise PostWriteVerificationError("Human decision is required")
    if record["recommendation"] not in {"resolved", "unresolved"}:
        raise PostWriteVerificationError("recommendation is invalid")

    state_records = []
    for item in record["state_chain"]:
        if not isinstance(item, dict) or set(item) != {"source_ref", "record"}:
            raise PostWriteVerificationError("state chain is invalid")
        _validate_ref(item["source_ref"], project_root)
        state_records.append(item["record"])
    try:
        state = derive_issue_resolution_state(state_records)
    except IssueResolutionStateError as error:
        raise PostWriteVerificationError("state chain is invalid") from error
    if state.state != "verdict_pending" or record["derived_state"] != state.state:
        raise PostWriteVerificationError("state chain is invalid")
    return VerdictCandidateValidation(
        verdict_candidate_id=record["verdict_candidate_id"],
        recommended_outcome=record["recommendation"],
        effective_outcome=record["effective_outcome"],
        derived_state=state.state,
    )


def validate_resolution_verdict(record, *, project_root):
    """Human Verdictを候補、risk処置、resolver終端へ結線する。"""

    if not isinstance(record, dict) or set(record) != _VERDICT_FIELDS:
        raise PostWriteVerificationError("Resolution Verdict fields are invalid")
    if (
        record["record_kind"] != "resolution_verdict"
        or record["schema_version"] != 1
        or record["verdict_version"] != 1
        or record["content_digest"] != canonical_digest(record)
    ):
        raise PostWriteVerificationError("Resolution Verdict identity is invalid")
    if record["decision_maker"] != "Human":
        raise PostWriteVerificationError(
            "Human Resolution Verdict is required"
        )
    candidate_ref = record["candidate_ref"]
    if not isinstance(candidate_ref, dict) or set(candidate_ref) != {
        "path",
        "sha256",
        "content_digest",
    }:
        raise PostWriteVerificationError(
            "Verdict candidate binding is stale"
        )
    candidate_path = _project_path(project_root, candidate_ref["path"])
    try:
        candidate_content = candidate_path.read_bytes()
        candidate = json.loads(candidate_content.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PostWriteVerificationError(
            "Verdict candidate binding is stale"
        ) from error
    if (
        _sha256(candidate_content) != candidate_ref["sha256"]
        or candidate.get("content_digest") != candidate_ref["content_digest"]
    ):
        raise PostWriteVerificationError(
            "Verdict candidate binding is stale"
        )
    validate_resolution_verdict_candidate(
        candidate,
        project_root=project_root,
    )
    _validate_ref(record["issue_ref"], project_root)
    for reference in record["evidence_refs"]:
        _validate_ref(reference, project_root)
    if record["outcome"] not in {"resolved", "unresolved"}:
        raise PostWriteVerificationError("Resolution Verdict outcome is invalid")
    if record["outcome"] == "resolved" and record[
        "accepted_residual_risks"
    ] != candidate["residual_risks"]:
        raise PostWriteVerificationError(
            "residual risk disposition is incomplete"
        )
    expected_items = {
        item["item"] for item in candidate["unresolved_items"]
    }
    dispositions = record["unresolved_item_dispositions"]
    if (
        not isinstance(dispositions, list)
        or {item.get("item") for item in dispositions} != expected_items
        or any(
            item.get("disposition") not in {"checkpoint", "deferred"}
            for item in dispositions
        )
    ):
        raise PostWriteVerificationError(
            "unresolved item disposition is incomplete"
        )

    state_records = [item["record"] for item in candidate["state_chain"]]
    verification = state_records[-1]
    state_records.append(
        {
            "record_kind": "verdict",
            "record_id": record["verdict_id"],
            "record_version": record["verdict_version"],
            "content_digest": record["content_digest"],
            "status": record["outcome"],
            "bindings": {
                "implementation_verification": verification["content_digest"]
            },
        }
    )
    try:
        state = derive_issue_resolution_state(state_records)
    except IssueResolutionStateError as error:
        raise PostWriteVerificationError(
            "Resolution Verdict state is invalid"
        ) from error
    if state.state != record["outcome"]:
        raise PostWriteVerificationError(
            "Resolution Verdict state is invalid"
        )
    return ResolutionVerdictValidation(
        verdict_id=record["verdict_id"],
        outcome=record["outcome"],
        derived_state=state.state,
    )
