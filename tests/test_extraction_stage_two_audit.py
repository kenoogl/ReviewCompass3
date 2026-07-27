"""第2段被覆監査に関する暫定テスト。"""

import importlib


def test_blocks_incomplete_coverage_and_unresolved_items():
  audit = importlib.import_module(
    "tools.extraction.stage_two_audit"
  )
  result = audit.audit_stage_two(
    population=("a", "b", "c"),
    extracted=("a",),
    not_selected=("b",),
    unresolved_dependencies=1,
    reassessment_conflicts=0,
    unclassified_items=0,
    missing_destinations=0,
    unreasoned_rejections=0,
    follow_up_items=2,
    user_approved=False,
  )

  assert result.status == "blocked"
  assert result.uncovered == ("c",)
  assert result.approval_candidate is None


def test_generates_candidate_only_after_all_machine_gates_pass():
  audit = importlib.import_module(
    "tools.extraction.stage_two_audit"
  )
  result = audit.audit_stage_two(
    population=("a", "b"),
    extracted=("a",),
    not_selected=("b",),
    unresolved_dependencies=0,
    reassessment_conflicts=0,
    unclassified_items=0,
    missing_destinations=0,
    unreasoned_rejections=0,
    follow_up_items=0,
    user_approved=False,
  )

  assert result.status == "awaiting_user_approval"
  assert result.uncovered == ()
  assert result.approval_candidate == {
    "approved": False,
    "audit_digest": result.digest,
  }
