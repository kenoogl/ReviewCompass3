"""第2段の抽出項目判断・受け先分類に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _decision(identifier, disposition, destination):
  return {
    "identifier": identifier,
    "disposition": disposition,
    "rationale": f"{disposition}とする根拠",
    "destination": destination,
  }


def test_classifies_every_item_into_one_judgment_partition():
  classification = importlib.import_module(
    "tools.extraction.destination_classification"
  )

  result = classification.classify_destinations(
    ("ESS-0001", "ESS-0002", "ESS-0003", "ESS-0004"),
    (
      _decision("ESS-0001", "transfer", "review.bundle"),
      _decision("ESS-0002", "redesign", "governance.approval"),
      _decision("ESS-0003", "reject", None),
      _decision("ESS-0004", "follow_up", "backlog.recovery"),
    ),
  )

  assert result.status == "complete"
  assert result.transferred == ("ESS-0001",)
  assert result.redesigned == ("ESS-0002",)
  assert result.rejected == ("ESS-0003",)
  assert result.follow_up == ("ESS-0004",)
  assert result.unclassified == ()
  assert len(result.digest) == 64


def test_keeps_items_without_judgment_unclassified_and_blocked():
  classification = importlib.import_module(
    "tools.extraction.destination_classification"
  )

  result = classification.classify_destinations(
    ("ESS-0001", "ESS-0002"),
    (_decision("ESS-0001", "transfer", "review.bundle"),),
  )

  assert result.status == "blocked"
  assert result.unclassified == ("ESS-0002",)


@pytest.mark.parametrize(
  "decisions",
  (
    (
      _decision("ESS-0001", "transfer", "review.bundle"),
      _decision("ESS-0001", "redesign", "review.bundle"),
    ),
    (_decision("ESS-9999", "transfer", "review.bundle"),),
    (_decision("ESS-0001", "unknown", "review.bundle"),),
    (_decision("ESS-0001", "transfer", None),),
    (_decision("ESS-0001", "reject", "review.bundle"),),
    ({
      "identifier": "ESS-0001",
      "disposition": "reject",
      "rationale": "",
      "destination": None,
    },),
  ),
)
def test_rejects_ambiguous_invalid_or_unreasoned_judgments(decisions):
  classification = importlib.import_module(
    "tools.extraction.destination_classification"
  )

  with pytest.raises(
    classification.DestinationClassificationError
  ):
    classification.classify_destinations(
      ("ESS-0001",),
      decisions,
    )
