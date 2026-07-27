"""第2段の増分再監査に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_combines_prior_and_new_batch_coverage_before_reaudit():
  reaudit = importlib.import_module(
    "tools.extraction.stage_two_reaudit"
  )

  result = reaudit.reaudit_stage_two(
    population=("source:a", "source:b", "source:c"),
    prior_extracted=("source:a",),
    prior_not_selected=(),
    batch_resolutions=(
      {
        "extracted": ("source:b",),
        "not_selected": (),
      },
    ),
    unresolved_dependencies=0,
    reassessment_conflicts=0,
    unclassified_items=0,
    missing_destinations=0,
    unreasoned_rejections=0,
    follow_up_items=1,
    user_approved=False,
  )

  assert result.status == "blocked"
  assert result.prior_covered_count == 1
  assert result.newly_covered_count == 1
  assert result.covered_count == 2
  assert result.uncovered_count == 1
  assert result.unresolved_count == 2
  assert result.approval_candidate is None
  assert len(result.digest) == 64


def test_generates_candidate_only_after_full_coverage_and_zero_unresolved():
  reaudit = importlib.import_module(
    "tools.extraction.stage_two_reaudit"
  )

  result = reaudit.reaudit_stage_two(
    population=("source:a", "source:b"),
    prior_extracted=("source:a",),
    prior_not_selected=(),
    batch_resolutions=(
      {
        "extracted": (),
        "not_selected": ("source:b",),
      },
    ),
    unresolved_dependencies=0,
    reassessment_conflicts=0,
    unclassified_items=0,
    missing_destinations=0,
    unreasoned_rejections=0,
    follow_up_items=0,
    user_approved=False,
  )

  assert result.status == "awaiting_user_approval"
  assert result.uncovered_count == 0
  assert result.unresolved_count == 0
  assert result.approval_candidate == {
    "approved": False,
    "audit_digest": result.digest,
  }
