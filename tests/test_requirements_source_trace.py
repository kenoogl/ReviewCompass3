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
