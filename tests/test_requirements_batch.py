"""第4段のrequirements batchに関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _requirement(**overrides):
  value = {
    "requirement_id": "REQ-CONTEXT-001",
    "feature_id": "FEAT-REVIEW-CONTEXT",
    "statement": "利用者はReview Taskの固定入力を確認できる",
    "inputs": ("Task criteria", "Target", "source materials"),
    "outputs": ("固定済みExecution Context",),
    "stop_conditions": ("入力の欠落",),
    "recovery_conditions": ("不足入力を追加して新しい版を作る",),
    "preserved_artifacts": ("失敗した入力候補と検査結果",),
    "acceptance_criteria": ("入力ごとのDigestを確認できる",),
    "non_goals": ("材料候補の完全自律選択",),
  }
  value.update(overrides)
  return value


def test_validates_complete_requirement_batch():
  batch = importlib.import_module(
    "tools.requirements.requirement_batch"
  )

  result = batch.validate_requirement_batch(
    requirements=(
      _requirement(),
      _requirement(
        requirement_id="REQ-CONTEXT-002",
        statement="入力変更時は既存結果をstaleとして停止する",
      ),
    ),
    defined_feature_ids=("FEAT-REVIEW-CONTEXT",),
  )

  assert result.status == "complete"
  assert result.requirement_count == 2
  assert tuple(
    item.requirement_id for item in result.requirements
  ) == ("REQ-CONTEXT-001", "REQ-CONTEXT-002")
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "requirement",
  (
    _requirement(requirement_id="invalid"),
    _requirement(feature_id="FEAT-UNKNOWN"),
    _requirement(statement=""),
    _requirement(inputs=()),
    _requirement(outputs=()),
    _requirement(stop_conditions=()),
    _requirement(recovery_conditions=()),
    _requirement(preserved_artifacts=()),
    _requirement(acceptance_criteria=()),
    _requirement(non_goals=()),
    _requirement(inputs=("same", "same")),
  ),
)
def test_rejects_incomplete_or_unresolved_requirement(
  requirement,
):
  batch = importlib.import_module(
    "tools.requirements.requirement_batch"
  )

  with pytest.raises(batch.RequirementBatchError):
    batch.validate_requirement_batch(
      requirements=(requirement,),
      defined_feature_ids=("FEAT-REVIEW-CONTEXT",),
    )


def test_rejects_duplicate_requirement_ids():
  batch = importlib.import_module(
    "tools.requirements.requirement_batch"
  )

  with pytest.raises(batch.RequirementBatchError):
    batch.validate_requirement_batch(
      requirements=(_requirement(), _requirement()),
      defined_feature_ids=("FEAT-REVIEW-CONTEXT",),
    )
