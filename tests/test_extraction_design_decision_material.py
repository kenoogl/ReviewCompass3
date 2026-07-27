"""設計評価競合の判断材料に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _options():
  return (
    {
      "disposition": "transfer",
      "statement": "side-track stackを優位点として移す",
      "rationale": "作業分離と復帰履歴を保持できる",
      "destination": "workflow.side_track_stack",
      "evidence": ("source:advantage.md#A10",),
    },
    {
      "disposition": "redesign",
      "statement": "目的だけを再設計して移す",
      "rationale": "旧実装の欠落を引き継がず作業分離を保つ",
      "destination": "workflow.interruption_recovery",
      "evidence": ("source:gap.md#CVG2-03",),
    },
    {
      "disposition": "reject",
      "statement": "独立機能としては移さない",
      "rationale": "既存の履歴管理で目的を満たせる可能性がある",
      "destination": None,
      "evidence": (
        "source:advantage.md#A10",
        "source:gap.md#CVG2-03",
      ),
    },
  )


def test_builds_unselected_three_way_design_decision_material():
  material = importlib.import_module(
    "tools.extraction.design_decision_material"
  )

  result = material.build_design_decision_material(
    identifier="ESS-0012",
    question=(
      "side-track stackを現システムへどう扱うか"
    ),
    current_disposition="follow_up",
    options=_options(),
  )

  assert result.status == "awaiting_user_review"
  assert result.identifier == "ESS-0012"
  assert result.selected_disposition is None
  assert tuple(
    option.disposition for option in result.options
  ) == ("redesign", "reject", "transfer")
  assert result.approval_candidate == {
    "approved": False,
    "material_digest": result.digest,
    "selected_disposition": None,
    "target_id": "ESS-0012",
  }
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "options",
  (
    _options()[:2],
    (
      _options()[0],
      _options()[1],
      {
        **_options()[2],
        "destination": "workflow.invalid",
      },
    ),
    (
      _options()[0],
      _options()[1],
      {
        **_options()[2],
        "evidence": (),
      },
    ),
  ),
)
def test_rejects_incomplete_inconsistent_or_unsupported_options(
  options,
):
  material = importlib.import_module(
    "tools.extraction.design_decision_material"
  )

  with pytest.raises(material.DesignDecisionMaterialError):
    material.build_design_decision_material(
      identifier="ESS-0012",
      question="判断",
      current_disposition="follow_up",
      options=options,
    )
