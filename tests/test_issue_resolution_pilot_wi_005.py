"""WI-005 post-write、restore rehearsal、Verdict候補のAcceptance Test。"""

import hashlib
import importlib
import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = (
    ROOT
    / "records/development/2026-08-04-issue-resolution-pilot-resolution-verdict-candidate-v1.json"
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_post_write"
    )


def test_actual_post_write_and_isolated_restore_rehearsal():
    before = (ROOT / "TODO_NEXT_SESSION.md").read_bytes()

    result = _module().verify_post_write(
        project_root=ROOT,
        todo_path="TODO_NEXT_SESSION.md",
        snapshot_path="records/session-handoffs/2026-08-04-todo-before-compaction-001.md",
        manifest_path="records/session-handoffs/2026-08-04-todo-before-compaction-001.manifest.json",
        known_active_ids={"ISSUE-PILOT-TODO-GROWTH-001"},
    )

    assert result.todo_sha256 == hashlib.sha256(before).hexdigest()
    assert result.todo_bytes <= 12288
    assert result.active_ids == ("ISSUE-PILOT-TODO-GROWTH-001",)
    assert result.reference_count == 4
    assert result.snapshot_sha256 == (
        "16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1"
    )
    assert result.restore_action == "restored"
    assert result.current_todo_preserved is True
    assert (ROOT / "TODO_NEXT_SESSION.md").read_bytes() == before


def test_rejects_stale_todo_reference_digest():
    document = re.sub(
        rb"(?<=SHA-256 `)[0-9a-f]{64}",
        b"0" * 64,
        (ROOT / "TODO_NEXT_SESSION.md").read_bytes(),
        count=1,
    )

    with pytest.raises(
        _module().PostWriteVerificationError,
        match="TODO reference digest mismatch",
    ):
        _module().validate_todo_reference_digests(
            document,
            project_root=ROOT,
        )


def test_actual_verdict_candidate_is_valid_and_pending_human_decision():
    candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))

    result = _module().validate_resolution_verdict_candidate(
        candidate,
        project_root=ROOT,
    )

    assert result.verdict_candidate_id == (
        "RVC-PILOT-TODO-GROWTH-001-V1"
    )
    assert result.recommended_outcome == "resolved"
    assert result.effective_outcome == "pending_human_decision"
    assert result.derived_state == "verdict_pending"


def test_rejects_candidate_without_residual_risk():
    candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
    candidate["residual_risks"] = []
    candidate["content_digest"] = _module().canonical_digest(candidate)

    with pytest.raises(
        _module().PostWriteVerificationError,
        match="residual risk is required",
    ):
        _module().validate_resolution_verdict_candidate(
            candidate,
            project_root=ROOT,
        )


def test_rejects_candidate_that_preempts_human_verdict():
    candidate = json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))
    candidate["effective_outcome"] = "resolved"
    candidate["content_digest"] = _module().canonical_digest(candidate)

    with pytest.raises(
        _module().PostWriteVerificationError,
        match="Human decision is required",
    ):
        _module().validate_resolution_verdict_candidate(
            candidate,
            project_root=ROOT,
        )
