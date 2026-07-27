"""follow_up解消検査に関する暫定テスト。"""

import importlib


def test_decision_source_chain_stays_follow_up_until_user_reconfirms():
  resolution = importlib.import_module(
    "tools.extraction.followup_resolution"
  )
  result = resolution.verify_decision_source_chain(
    inventory_reference="inventory.md#L1",
    primary_references=("issue.yaml#L10", "session.md#L20"),
    user_reconfirmed=False,
  )

  assert result.status == "follow_up"
  assert result.primary_reference_count == 2
  assert result.required_action == "user_reconfirmation"


def test_rule_recount_reports_source_and_arithmetic_discrepancies():
  resolution = importlib.import_module(
    "tools.extraction.followup_resolution"
  )
  result = resolution.verify_rule_recount(
    (
      {"raw": 10, "kept": 6, "frag": 2, "sub": 1},
      {"raw": 4, "kept": 3, "frag": 1, "sub": 0},
    ),
    claimed_source_count=1,
    claimed_raw=14,
    claimed_kept=9,
    claimed_frag=3,
    claimed_sub=1,
  )

  assert result.status == "follow_up"
  assert result.actual_source_count == 2
  assert result.uncategorized_count == 1
  assert result.discrepancies == (
    "source_count",
    "raw_partition",
  )
