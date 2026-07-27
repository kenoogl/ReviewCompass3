"""利用者決定の再確認材料に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_separates_approval_targets_from_information_only_items():
  material = importlib.import_module(
    "tools.extraction.decision_review_material"
  )
  result = material.build_decision_review_material((
    {
      "identifier": "ESS-0001",
      "statement": "閉じた辺語彙とID参照を採用する",
      "review_kind": "approval",
      "rationale": "現設計へ移すには現利用者の再確認が必要",
      "current_disposition": "follow_up",
      "sources": (
        {
          "layer": "inventory",
          "role": "secondary_index",
          "limitation": "一次記録を集約した一覧",
        },
        {
          "layer": "issue",
          "role": "primary_decision",
          "limitation": "旧リポジトリ時点の決定",
        },
        {
          "layer": "session",
          "role": "contemporaneous_summary",
          "limitation": "逐語記録ではない",
        },
      ),
    },
    {
      "identifier": "ESS-0008",
      "statement": "利用者指示でセッション取込を起動する",
      "review_kind": "information",
      "rationale": "第0段で広い起動経路を承認済み",
      "current_disposition": "follow_up",
      "sources": ({
        "layer": "session",
        "role": "primary_instruction",
        "limitation": "旧実装時点の指示",
      },),
    },
  ))

  assert result.status == "awaiting_user_review"
  assert result.approval_targets == ("ESS-0001",)
  assert result.information_targets == ("ESS-0008",)
  assert result.approval_candidate == {
    "approved": False,
    "target_ids": ["ESS-0001"],
    "material_digest": result.digest,
  }
  assert tuple(
    entry.current_disposition for entry in result.entries
  ) == ("follow_up", "follow_up")
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "candidate",
  (
    {
      "identifier": "ESS-0001",
      "statement": "判断",
      "review_kind": "approval",
      "rationale": "",
      "current_disposition": "follow_up",
      "sources": (),
    },
    {
      "identifier": "ESS-0001",
      "statement": "判断",
      "review_kind": "approval",
      "rationale": "理由",
      "current_disposition": "transfer",
      "sources": ({
        "layer": "issue",
        "role": "primary_decision",
        "limitation": "旧決定",
      },),
    },
  ),
)
def test_rejects_unreasoned_or_prematurely_transferred_candidates(candidate):
  material = importlib.import_module(
    "tools.extraction.decision_review_material"
  )

  with pytest.raises(material.DecisionReviewMaterialError):
    material.build_decision_review_material((candidate,))
