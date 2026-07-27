"""第2段一括完了関門に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _decision(candidate, action, essence_id):
  return {
    "candidate": candidate,
    "action": action,
    "essence_id": essence_id,
    "rationale": "固定材料を意味族へ完全解決",
  }


def _assessment(path, digest, candidates, decisions):
  return {
    "path": path,
    "material_digest": digest,
    "raw_evidence": candidates,
    "decisions": decisions,
  }


def test_completes_full_remaining_population_before_approval():
  completion = importlib.import_module(
    "tools.extraction.stage_two_completion"
  )
  candidates = ("source:new.py", "source:related.md")
  decisions = (
    _decision("source:new.py", "extract", "ESS-0034"),
    _decision("source:related.md", "merge", "ESS-0001"),
  )
  digest = "a" * 64

  result = completion.complete_stage_two(
    population=("source:prior.py",) + candidates,
    prior_covered=("source:prior.py",),
    material_digest=digest,
    assessments=(
      _assessment("main", digest, candidates, decisions),
      _assessment("independent", digest, candidates, decisions),
    ),
    existing_essence_ids=("ESS-0001",),
    new_essence_ids=("ESS-0034",),
    follow_up_ids=(),
    user_approved=False,
  )

  assert result.status == "awaiting_user_approval"
  assert result.covered_count == 3
  assert result.uncovered_count == 0
  assert result.extracted_count == 1
  assert result.merged_count == 1
  assert result.not_selected_count == 0
  assert result.conflict_count == 0
  assert result.approval_candidate == {
    "approved": False,
    "audit_digest": result.audit_digest,
  }


def test_keeps_complete_coverage_blocked_while_follow_up_remains():
  completion = importlib.import_module(
    "tools.extraction.stage_two_completion"
  )
  candidates = ("source:history.md",)
  decisions = (
    _decision(
      "source:history.md",
      "not_selected",
      None,
    ),
  )
  digest = "b" * 64

  result = completion.complete_stage_two(
    population=candidates,
    prior_covered=(),
    material_digest=digest,
    assessments=(
      _assessment("main", digest, candidates, decisions),
      _assessment("independent", digest, candidates, decisions),
    ),
    existing_essence_ids=("ESS-0001",),
    new_essence_ids=(),
    follow_up_ids=("ESS-0001",),
    user_approved=False,
  )

  assert result.status == "blocked"
  assert result.covered_count == 1
  assert result.uncovered_count == 0
  assert result.unresolved_count == 1
  assert result.approval_candidate is None


def test_rejects_missing_new_essence_extraction():
  completion = importlib.import_module(
    "tools.extraction.stage_two_completion"
  )
  candidates = ("source:related.md",)
  decisions = (
    _decision("source:related.md", "merge", "ESS-0001"),
  )

  with pytest.raises(completion.StageTwoCompletionError):
    completion.complete_stage_two(
      population=candidates,
      prior_covered=(),
      material_digest="c" * 64,
      assessments=(
        _assessment("main", "c" * 64, candidates, decisions),
        _assessment(
          "independent",
          "c" * 64,
          candidates,
          decisions,
        ),
      ),
      existing_essence_ids=("ESS-0001",),
      new_essence_ids=("ESS-0034",),
      follow_up_ids=(),
      user_approved=False,
    )
