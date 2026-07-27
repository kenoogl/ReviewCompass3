"""実測follow_upの再検証に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_resolves_closed_holes_but_keeps_current_dispute():
  revalidation = importlib.import_module(
    "tools.extraction.empirical_revalidation"
  )
  result = revalidation.revalidate_empirical_followups((
    {
      "identifier": "ESS-0011",
      "observations": (
        {
          "name": "marker_spoof",
          "status": "information",
          "evidence": "current transcript is not parsed as structure",
          "rationale": "旧marker方式限定",
        },
        {
          "name": "lf_split",
          "status": "resolved",
          "evidence": "claude and codex LF mutation tests",
          "rationale": "U+2028を同一event本文として保持",
        },
        {
          "name": "exact_count",
          "status": "resolved",
          "evidence": "raw range digest regeneration tests",
          "rationale": "件数語でなく固定範囲全体を照合",
        },
      ),
    },
    {
      "identifier": "ESS-0012",
      "observations": (
        {
          "name": "source_count_correction",
          "status": "resolved",
          "evidence": "group A primary detail",
          "rationale": "本数と判定者数を分離",
        },
        {
          "name": "classification_correction",
          "status": "information",
          "evidence": "user decision inventory",
          "rationale": "優位点ではなく利用者決定",
        },
        {
          "name": "side_track_dispute",
          "status": "follow_up",
          "evidence": "group G2 conflicting judgments",
          "rationale": "現設計判断が未確定",
        },
      ),
    },
  ))

  assert result.status == "follow_up"
  assert result.resolved == ("ESS-0011",)
  assert result.follow_up == ("ESS-0012",)
  assert result.information == ()
  assert tuple(
    (item.identifier, item.status)
    for item in result.items
  ) == (
    ("ESS-0011", "resolved"),
    ("ESS-0012", "follow_up"),
  )
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "observation",
  (
    {
      "name": "missing_evidence",
      "status": "resolved",
      "evidence": "",
      "rationale": "理由",
    },
    {
      "name": "unknown",
      "status": "unknown",
      "evidence": "evidence",
      "rationale": "理由",
    },
  ),
)
def test_rejects_unproven_or_unknown_observations(observation):
  revalidation = importlib.import_module(
    "tools.extraction.empirical_revalidation"
  )

  with pytest.raises(revalidation.EmpiricalRevalidationError):
    revalidation.revalidate_empirical_followups(({
      "identifier": "ESS-0011",
      "observations": (observation,),
    },))
