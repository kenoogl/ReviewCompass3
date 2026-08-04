"""Human Resolution Verdictと早期Pilot closureのAcceptance Test。"""

import json
from pathlib import Path

import pytest

from tools.development import issue_resolution_post_write as verification


ROOT = Path(__file__).resolve().parents[1]
VERDICT_PATH = (
    ROOT
    / ".reviewcompass/workflow/resolution-verdicts/verdict-pilot-todo-growth-001--v1.json"
)


def _verdict():
    return json.loads(VERDICT_PATH.read_text(encoding="utf-8"))


def test_actual_human_verdict_closes_state_as_resolved():
    result = verification.validate_resolution_verdict(
        _verdict(),
        project_root=ROOT,
    )

    assert result.verdict_id == "VERDICT-PILOT-TODO-GROWTH-001-V1"
    assert result.outcome == "resolved"
    assert result.derived_state == "resolved"


def test_rejects_non_human_resolution_verdict():
    verdict = _verdict()
    verdict["decision_maker"] = "automation"
    verdict["content_digest"] = verification.canonical_digest(verdict)

    with pytest.raises(
        verification.PostWriteVerificationError,
        match="Human Resolution Verdict is required",
    ):
        verification.validate_resolution_verdict(
            verdict,
            project_root=ROOT,
        )


def test_rejects_stale_verdict_candidate_binding():
    verdict = _verdict()
    verdict["candidate_ref"]["sha256"] = "0" * 64
    verdict["content_digest"] = verification.canonical_digest(verdict)

    with pytest.raises(
        verification.PostWriteVerificationError,
        match="Verdict candidate binding is stale",
    ):
        verification.validate_resolution_verdict(
            verdict,
            project_root=ROOT,
        )


def test_rejects_resolved_without_accepting_all_residual_risks():
    verdict = _verdict()
    verdict["accepted_residual_risks"] = verdict[
        "accepted_residual_risks"
    ][:-1]
    verdict["content_digest"] = verification.canonical_digest(verdict)

    with pytest.raises(
        verification.PostWriteVerificationError,
        match="residual risk disposition is incomplete",
    ):
        verification.validate_resolution_verdict(
            verdict,
            project_root=ROOT,
        )
