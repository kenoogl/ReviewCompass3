"""第2段の独立生材料再判定に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


MATERIAL_DIGEST = "a" * 64


def _assessment(path, decisions, **overrides):
  value = {
    "path": path,
    "material_digest": MATERIAL_DIGEST,
    "raw_evidence": (
      "ReviewCompass:tools/api_providers/source_bundle.py:1-40",
    ),
    "decisions": decisions,
  }
  value.update(overrides)
  return value


def test_completes_when_main_and_independent_raw_reassessments_agree():
  reassessment = importlib.import_module(
    "tools.extraction.reassessment"
  )
  decisions = {
    "ESS-0001": "transfer",
    "ESS-0002": "redesign",
  }

  result = reassessment.reconcile_reassessments(
    MATERIAL_DIGEST,
    ("ESS-0001", "ESS-0002"),
    (
      _assessment("main", decisions),
      _assessment("independent", decisions),
    ),
  )

  assert result.status == "complete"
  assert result.agreed == (
    ("ESS-0001", "transfer"),
    ("ESS-0002", "redesign"),
  )
  assert result.conflicts == ()
  assert len(result.digest) == 64


def test_blocks_conflicts_without_treating_them_as_final():
  reassessment = importlib.import_module(
    "tools.extraction.reassessment"
  )

  result = reassessment.reconcile_reassessments(
    MATERIAL_DIGEST,
    ("ESS-0001",),
    (
      _assessment("main", {"ESS-0001": "transfer"}),
      _assessment(
        "independent",
        {"ESS-0001": "redesign"},
      ),
    ),
  )

  assert result.status == "blocked"
  assert result.agreed == ()
  assert result.conflicts == (
    reassessment.ReassessmentConflict(
      identifier="ESS-0001",
      main_decision="transfer",
      independent_decision="redesign",
    ),
  )


@pytest.mark.parametrize(
  "assessments",
  (
    (
      _assessment("main", {"ESS-0001": "transfer"}),
    ),
    (
      _assessment("main", {"ESS-0001": "transfer"}),
      _assessment("main", {"ESS-0001": "transfer"}),
    ),
    (
      _assessment("main", {"ESS-0001": "transfer"}),
      _assessment(
        "independent",
        {"ESS-0001": "transfer"},
        raw_evidence=(),
      ),
    ),
    (
      _assessment("main", {"ESS-0001": "transfer"}),
      _assessment(
        "independent",
        {"ESS-0001": "transfer"},
        material_digest="b" * 64,
      ),
    ),
    (
      _assessment("main", {"ESS-0001": "transfer"}),
      _assessment("independent", {}),
    ),
  ),
)
def test_rejects_missing_paths_summary_only_or_wrong_material(
  assessments,
):
  reassessment = importlib.import_module(
    "tools.extraction.reassessment"
  )

  with pytest.raises(reassessment.ReassessmentError):
    reassessment.reconcile_reassessments(
      MATERIAL_DIGEST,
      ("ESS-0001",),
      assessments,
    )
