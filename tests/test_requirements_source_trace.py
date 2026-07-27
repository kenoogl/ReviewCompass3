"""第4段のrequirement由来記録に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _record(**overrides):
  value = {
    "requirement_id": "REQ-RUNTIME-001",
    "intent_refs": ("INT-PRODUCT", "INT-CONSTRAINTS"),
    "essence_ids": ("ESS-0003", "ESS-0005"),
    "disposition": "selected",
    "rationale": "Task固有の入力と実行条件を固定するため",
  }
  value.update(overrides)
  return value


def test_builds_deterministic_requirement_source_trace():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  result = source_trace.validate_requirement_sources(
    records=(
      _record(),
      _record(
        requirement_id="REQ-RUNTIME-002",
        intent_refs=("INT-SUCCESS",),
        essence_ids=("ESS-0006",),
        rationale="staleな入力で確定しないため",
      ),
    ),
    defined_requirement_ids=(
      "REQ-RUNTIME-002",
      "REQ-RUNTIME-001",
    ),
    defined_intent_ids=(
      "INT-CONSTRAINTS",
      "INT-PRODUCT",
      "INT-SUCCESS",
    ),
    defined_essence_ids=(
      "ESS-0006",
      "ESS-0005",
      "ESS-0003",
    ),
  )

  assert result.status == "complete"
  assert tuple(
    record.requirement_id for record in result.records
  ) == ("REQ-RUNTIME-001", "REQ-RUNTIME-002")
  assert result.records[0].intent_refs == (
    "INT-CONSTRAINTS",
    "INT-PRODUCT",
  )
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "record",
  (
    _record(intent_refs=()),
    _record(essence_ids=()),
    _record(intent_refs=("INT-UNKNOWN",)),
    _record(essence_ids=("ESS-9999",)),
    _record(requirement_id="REQ-UNKNOWN-001"),
    _record(rationale=""),
    _record(intent_refs=("INT-PRODUCT", "INT-PRODUCT")),
    _record(disposition="unknown"),
  ),
)
def test_rejects_incomplete_or_unresolved_requirement_sources(
  record,
):
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(record,),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0003", "ESS-0005"),
    )


def test_requires_reason_for_not_selected_essence():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(
        _record(
          requirement_id=None,
          disposition="not_selected",
          rationale="",
        ),
      ),
      defined_requirement_ids=(),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0003", "ESS-0005"),
    )


def test_rejects_duplicate_requirement_relations():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(_record(), _record()),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0003", "ESS-0005"),
    )


def test_rejects_requirement_without_source_relation():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(_record(),),
      defined_requirement_ids=(
        "REQ-RUNTIME-001",
        "REQ-RUNTIME-002",
      ),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=("ESS-0003", "ESS-0005"),
    )


def test_rejects_out_of_feature_or_uncovered_essence():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(_record(essence_ids=("ESS-0003",)),),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=(
        "ESS-0003",
        "ESS-0005",
        "ESS-0006",
      ),
      allowed_essence_ids=("ESS-0003", "ESS-0005"),
      required_essence_ids=("ESS-0003", "ESS-0005"),
    )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_requirement_sources(
      records=(_record(essence_ids=("ESS-0006",)),),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=(
        "INT-PRODUCT",
        "INT-CONSTRAINTS",
      ),
      defined_essence_ids=(
        "ESS-0003",
        "ESS-0005",
        "ESS-0006",
      ),
      allowed_essence_ids=("ESS-0003", "ESS-0005"),
      required_essence_ids=("ESS-0003",),
    )


def _obligation_record(**overrides):
  value = {
    "obligation_id": "REQ-RUNTIME-001#statement",
    "requirement_id": "REQ-RUNTIME-001",
    "intent_refs": ("INT-PRODUCT",),
    "essence_ids": ("ESS-0003",),
    "rationale": "要件本文をTask Runtimeの目的へ結ぶため",
  }
  value.update(overrides)
  return value


def test_builds_deterministic_obligation_source_trace():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  result = source_trace.validate_obligation_sources(
    records=(
      _obligation_record(
        obligation_id="REQ-RUNTIME-001#inputs",
      ),
      _obligation_record(),
    ),
    required_obligation_ids=(
      "REQ-RUNTIME-001#statement",
      "REQ-RUNTIME-001#inputs",
    ),
    defined_requirement_ids=("REQ-RUNTIME-001",),
    defined_intent_ids=("INT-PRODUCT",),
    defined_essence_ids=("ESS-0003",),
  )

  assert result.status == "complete"
  assert tuple(
    record.obligation_id for record in result.records
  ) == (
    "REQ-RUNTIME-001#inputs",
    "REQ-RUNTIME-001#statement",
  )
  assert len(result.digest) == 64


def test_requires_source_relation_for_every_obligation_scope():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_obligation_sources(
      records=(_obligation_record(),),
      required_obligation_ids=(
        "REQ-RUNTIME-001#statement",
        "REQ-RUNTIME-001#inputs",
      ),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=("INT-PRODUCT",),
      defined_essence_ids=("ESS-0003",),
    )


@pytest.mark.parametrize(
  "record",
  (
    _obligation_record(
      obligation_id="REQ-RUNTIME-001#unknown",
    ),
    _obligation_record(requirement_id="REQ-UNKNOWN-001"),
    _obligation_record(intent_refs=("INT-UNKNOWN",)),
    _obligation_record(essence_ids=("ESS-9999",)),
    _obligation_record(rationale=""),
  ),
)
def test_rejects_unresolved_obligation_source(record):
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_obligation_sources(
      records=(record,),
      required_obligation_ids=(
        "REQ-RUNTIME-001#statement",
      ),
      defined_requirement_ids=("REQ-RUNTIME-001",),
      defined_intent_ids=("INT-PRODUCT",),
      defined_essence_ids=("ESS-0003",),
    )


def test_expands_and_validates_every_atomic_obligation():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )
  requirement = {
    "requirement_id": "REQ-RUNTIME-001",
    "statement": "実行条件を固定する",
    "inputs": ["Task", "Context"],
    "outputs": ["Run"],
    "stop_conditions": ["Context不一致"],
    "recovery_conditions": ["Contextを再固定する"],
    "preserved_artifacts": ["拒否診断"],
    "acceptance_criteria": ["同一入力で同一identity"],
    "non_goals": ["Human判断の代替"],
  }
  expected_ids = (
    "REQ-RUNTIME-001#acceptance_criteria.001",
    "REQ-RUNTIME-001#inputs.001",
    "REQ-RUNTIME-001#inputs.002",
    "REQ-RUNTIME-001#non_goals.001",
    "REQ-RUNTIME-001#outputs.001",
    "REQ-RUNTIME-001#preserved_artifacts.001",
    "REQ-RUNTIME-001#recovery_conditions.001",
    "REQ-RUNTIME-001#statement",
    "REQ-RUNTIME-001#stop_conditions.001",
  )

  result = source_trace.validate_atomic_obligation_sources(
    requirements=(requirement,),
    relations=tuple(
      {
        "obligation_id": obligation_id,
        "source_requirement_id": "REQ-RUNTIME-001",
      }
      for obligation_id in expected_ids
    ),
    source_records=(_record(
      essence_ids=("ESS-0003",),
      intent_refs=("INT-PRODUCT",),
    ),),
    defined_intent_ids=("INT-PRODUCT",),
    defined_essence_ids=("ESS-0003",),
  )

  assert result.status == "complete"
  assert tuple(
    record.obligation_id for record in result.records
  ) == expected_ids
  assert len(result.digest) == 64


def test_rejects_missing_atomic_list_entry_relation():
  source_trace = importlib.import_module(
    "tools.requirements.source_trace"
  )
  requirement = {
    "requirement_id": "REQ-RUNTIME-001",
    "statement": "実行条件を固定する",
    "inputs": ["Task", "Context"],
    "outputs": ["Run"],
    "stop_conditions": ["Context不一致"],
    "recovery_conditions": ["Contextを再固定する"],
    "preserved_artifacts": ["拒否診断"],
    "acceptance_criteria": ["同一入力で同一identity"],
    "non_goals": ["Human判断の代替"],
  }

  with pytest.raises(source_trace.RequirementSourceTraceError):
    source_trace.validate_atomic_obligation_sources(
      requirements=(requirement,),
      relations=(
        {
          "obligation_id": "REQ-RUNTIME-001#statement",
          "source_requirement_id": "REQ-RUNTIME-001",
        },
      ),
      source_records=(_record(
        essence_ids=("ESS-0003",),
        intent_refs=("INT-PRODUCT",),
      ),),
      defined_intent_ids=("INT-PRODUCT",),
      defined_essence_ids=("ESS-0003",),
    )
