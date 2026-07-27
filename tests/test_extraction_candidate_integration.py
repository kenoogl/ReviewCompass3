"""独立候補統合に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_integrates_every_candidate_as_add_merge_or_defer():
  integration = importlib.import_module(
    "tools.extraction.candidate_integration"
  )
  result = integration.integrate_candidates(
    existing_items=(
      {
        "identifier": "ESS-0001",
        "evidence": ("source:a.py#L1",),
      },
    ),
    candidates=(
      {
        "candidate_id": "ALT-001",
        "statement": "既存候補",
        "axis": "capability",
        "evidence": ("source:a.py#L1-L5",),
      },
      {
        "candidate_id": "ALT-002",
        "statement": "新規候補",
        "axis": "recovery",
        "evidence": ("source:b.py#L2",),
      },
      {
        "candidate_id": "ALT-003",
        "statement": "保留候補",
        "axis": "procedure",
        "evidence": ("source:c.py#L3",),
      },
    ),
    resolutions=(
      {
        "candidate_id": "ALT-001",
        "action": "merge",
        "target": "ESS-0001",
        "rationale": "同じ責務",
      },
      {
        "candidate_id": "ALT-002",
        "action": "add",
        "target": "ESS-0002",
        "rationale": "独立した復旧責務",
      },
      {
        "candidate_id": "ALT-003",
        "action": "defer",
        "target": None,
        "rationale": "追加材料が必要",
      },
    ),
  )

  assert result.status == "complete"
  assert result.added == (("ALT-002", "ESS-0002"),)
  assert result.merged == (("ALT-001", "ESS-0001"),)
  assert result.deferred == (("ALT-003", "追加材料が必要"),)
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "resolutions",
  (
    (),
    (
      {
        "candidate_id": "ALT-001",
        "action": "merge",
        "target": "ESS-9999",
        "rationale": "存在しない",
      },
    ),
    (
      {
        "candidate_id": "ALT-001",
        "action": "defer",
        "target": "ESS-0001",
        "rationale": "対象付き保留",
      },
    ),
  ),
)
def test_rejects_unresolved_or_invalid_candidate_resolutions(
  resolutions,
):
  integration = importlib.import_module(
    "tools.extraction.candidate_integration"
  )

  with pytest.raises(integration.CandidateIntegrationError):
    integration.integrate_candidates(
      existing_items=({
        "identifier": "ESS-0001",
        "evidence": ("source:a.py#L1",),
      },),
      candidates=({
        "candidate_id": "ALT-001",
        "statement": "候補",
        "axis": "capability",
        "evidence": ("source:b.py#L2",),
      },),
      resolutions=resolutions,
    )
