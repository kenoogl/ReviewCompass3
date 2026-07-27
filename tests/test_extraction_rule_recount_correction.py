"""規則再集計差分の訂正に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_resolves_duplicate_source_and_duplicate_rule_gaps():
  correction = importlib.import_module(
    "tools.extraction.rule_recount_correction"
  )
  raw_records = (
    {
      "impl": "phase.py",
      "path": "tools/api/phase.py",
      "raise": ("required",),
      "reasons": (),
      "stderr": (),
    },
    {
      "impl": "api/phase.py",
      "path": "tools/api/phase.py",
      "raise": ("required",),
      "reasons": (),
      "stderr": (),
    },
    {
      "impl": "check.py",
      "path": "tools/check.py",
      "raise": ("invalid", "invalid", "missing"),
      "reasons": (),
      "stderr": (),
    },
  )
  recount_rows = (
    {
      "impl": "phase.py",
      "raw": 1,
      "kept": 1,
      "frag": 0,
      "sub": 0,
    },
    {
      "impl": "api/phase.py",
      "raw": 1,
      "kept": 1,
      "frag": 0,
      "sub": 0,
    },
    {
      "impl": "check.py",
      "raw": 3,
      "kept": 2,
      "frag": 0,
      "sub": 0,
    },
  )

  result = correction.correct_rule_recount(
    raw_records,
    recount_rows,
    expected_source_count=2,
  )

  assert result.status == "resolved"
  assert result.corrected_source_count == 2
  assert result.duplicate_source_paths == (
    "tools/api/phase.py",
  )
  assert result.removed_source_aliases == ("phase.py",)
  assert result.raw_count == 4
  assert result.kept_count == 3
  assert result.fragment_count == 0
  assert result.substring_count == 0
  assert result.exact_duplicate_count == 1
  assert result.unexplained_count == 0
  assert len(result.digest) == 64


def test_keeps_unexplained_partition_gap_as_follow_up():
  correction = importlib.import_module(
    "tools.extraction.rule_recount_correction"
  )

  result = correction.correct_rule_recount(
    ({
      "impl": "check.py",
      "path": "tools/check.py",
      "raise": ("invalid",),
      "reasons": (),
      "stderr": (),
    },),
    ({
      "impl": "check.py",
      "raw": 2,
      "kept": 1,
      "frag": 0,
      "sub": 0,
    },),
    expected_source_count=1,
  )

  assert result.status == "follow_up"
  assert result.exact_duplicate_count == 0
  assert result.unexplained_count == 1
  assert result.discrepancies == ("unexplained_partition",)
