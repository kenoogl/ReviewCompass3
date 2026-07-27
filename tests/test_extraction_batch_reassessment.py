"""構造化batchの独立再判定に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


DIGEST = "a" * 64
CANDIDATES = ("source:a.yaml", "source:b.yaml")


def _assessment(path, decisions, **overrides):
  value = {
    "path": path,
    "material_digest": DIGEST,
    "raw_evidence": CANDIDATES,
    "decisions": decisions,
  }
  value.update(overrides)
  return value


def test_agrees_on_candidate_action_and_essence_target():
  reassessment = importlib.import_module(
    "tools.extraction.batch_reassessment"
  )
  decisions = (
    {
      "candidate": "source:a.yaml",
      "action": "extract",
      "essence_id": "ESS-0020",
      "rationale": "新規契約",
    },
    {
      "candidate": "source:b.yaml",
      "action": "merge",
      "essence_id": "ESS-0020",
      "rationale": "同じ証拠族",
    },
  )

  result = reassessment.reconcile_batch_reassessments(
    DIGEST,
    CANDIDATES,
    (
      _assessment("main", decisions),
      _assessment("independent", decisions),
    ),
  )

  assert result.status == "complete"
  assert result.agreed == (
    ("source:a.yaml", "extract", "ESS-0020"),
    ("source:b.yaml", "merge", "ESS-0020"),
  )
  assert result.conflicts == ()
  assert len(result.digest) == 64


def test_blocks_action_or_target_conflicts():
  reassessment = importlib.import_module(
    "tools.extraction.batch_reassessment"
  )
  main = (
    {
      "candidate": "source:a.yaml",
      "action": "merge",
      "essence_id": "ESS-0020",
      "rationale": "既存へ統合",
    },
  )
  independent = (
    {
      "candidate": "source:a.yaml",
      "action": "not_selected",
      "essence_id": None,
      "rationale": "重複証拠",
    },
  )

  result = reassessment.reconcile_batch_reassessments(
    DIGEST,
    ("source:a.yaml",),
    (
      _assessment("main", main, raw_evidence=("source:a.yaml",)),
      _assessment(
        "independent",
        independent,
        raw_evidence=("source:a.yaml",),
      ),
    ),
  )

  assert result.status == "blocked"
  assert result.conflicts == (
    reassessment.BatchReassessmentConflict(
      candidate="source:a.yaml",
      main_action="merge",
      main_essence_id="ESS-0020",
      independent_action="not_selected",
      independent_essence_id=None,
    ),
  )


@pytest.mark.parametrize(
  "assessments",
  (
    (
      _assessment("main", ()),
      _assessment("independent", ()),
    ),
    (
      _assessment("main", (), material_digest="b" * 64),
      _assessment("independent", ()),
    ),
  ),
)
def test_rejects_incomplete_or_wrong_material_assessments(assessments):
  reassessment = importlib.import_module(
    "tools.extraction.batch_reassessment"
  )

  with pytest.raises(reassessment.BatchReassessmentError):
    reassessment.reconcile_batch_reassessments(
      DIGEST,
      CANDIDATES,
      assessments,
    )
