"""第4段の機能分割とエッセンス受け先に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _feature(**overrides):
  value = {
    "feature_id": "FEAT-REVIEW-CONTEXT",
    "name": "レビュー入力構成",
    "responsibility": "Task固有の入力を固定して検証する",
    "intent_refs": ("INT-PRODUCT", "INT-CONSTRAINTS"),
    "essence_ids": ("ESS-0005", "ESS-0006"),
    "non_goals": ("LLMによる暗黙の材料選択",),
  }
  value.update(overrides)
  return value


def test_validates_complete_non_overlapping_feature_partition():
  partition = importlib.import_module(
    "tools.requirements.feature_partition"
  )

  result = partition.validate_feature_partition(
    features=(
      _feature(),
      _feature(
        feature_id="FEAT-REVIEW-EXECUTION",
        name="レビュー実行",
        responsibility="固定条件でreviewを実行する",
        intent_refs=("INT-PRODUCT", "INT-SUCCESS"),
        essence_ids=("ESS-0003",),
        non_goals=("最終判断の自動化",),
      ),
    ),
    defined_intent_ids=(
      "INT-CONSTRAINTS",
      "INT-PRODUCT",
      "INT-SUCCESS",
    ),
    defined_essence_ids=(
      "ESS-0003",
      "ESS-0005",
      "ESS-0006",
    ),
  )

  assert result.status == "complete"
  assert result.feature_count == 2
  assert result.covered_essence_count == 3
  assert result.uncovered_essence_ids == ()
  assert result.duplicate_essence_ids == ()
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "features",
  (
    (
      _feature(essence_ids=("ESS-0005",)),
    ),
    (
      _feature(),
      _feature(
        feature_id="FEAT-OTHER",
        essence_ids=("ESS-0006",),
      ),
    ),
    (
      _feature(essence_ids=("ESS-9999",)),
    ),
  ),
)
def test_rejects_uncovered_duplicate_or_unknown_essence(
  features,
):
  partition = importlib.import_module(
    "tools.requirements.feature_partition"
  )

  with pytest.raises(partition.FeaturePartitionError):
    partition.validate_feature_partition(
      features=features,
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0005", "ESS-0006"),
    )


@pytest.mark.parametrize(
  "feature",
  (
    _feature(feature_id="invalid"),
    _feature(name=""),
    _feature(responsibility=""),
    _feature(intent_refs=()),
    _feature(intent_refs=("INT-UNKNOWN",)),
    _feature(non_goals=()),
    _feature(non_goals=("same", "same")),
  ),
)
def test_rejects_incomplete_feature_boundary(feature):
  partition = importlib.import_module(
    "tools.requirements.feature_partition"
  )

  with pytest.raises(partition.FeaturePartitionError):
    partition.validate_feature_partition(
      features=(feature,),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0005", "ESS-0006"),
    )


def test_rejects_duplicate_feature_ids():
  partition = importlib.import_module(
    "tools.requirements.feature_partition"
  )

  with pytest.raises(partition.FeaturePartitionError):
    partition.validate_feature_partition(
      features=(_feature(), _feature()),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0005", "ESS-0006"),
    )
