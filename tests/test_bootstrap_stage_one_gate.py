"""第1段完了関門監査の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def _passing_evidence():
  return {
    "source_universe": True,
    "known_candidates": True,
    "material_insufficiency": True,
    "selection_routes": True,
    "stale_rejection": True,
    "digest_chain": True,
    "approval_binding": True,
    "immutable_resume": True,
  }


def test_reports_candidate_before_explicit_user_approval():
  stage_one_gate = importlib.import_module(
    "tools.bootstrap.stage_one_gate"
  )

  audit = stage_one_gate.audit_stage_one(
    _passing_evidence(),
    user_approved=False,
  )

  assert audit.status == "candidate"
  assert audit.passed_gate_count == 8
  assert audit.unresolved_gates == ()
  assert audit.user_approved is False
  assert {
    gate.status
    for gate in audit.gates
  } == {"passed"}


def test_fails_closed_with_unresolved_gate():
  stage_one_gate = importlib.import_module(
    "tools.bootstrap.stage_one_gate"
  )
  evidence = _passing_evidence()
  evidence["digest_chain"] = False

  audit = stage_one_gate.audit_stage_one(
    evidence,
    user_approved=False,
  )

  assert audit.status == "blocked"
  assert audit.passed_gate_count == 7
  assert audit.unresolved_gates == ("digest_chain",)


def test_reports_ready_only_after_explicit_user_approval():
  stage_one_gate = importlib.import_module(
    "tools.bootstrap.stage_one_gate"
  )

  assert stage_one_gate.audit_stage_one(
    _passing_evidence(),
    user_approved=True,
  ).status == "ready"
