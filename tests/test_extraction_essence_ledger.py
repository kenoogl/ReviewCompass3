"""第2段のエッセンス台帳schemaに関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _record(**overrides):
  value = {
    "identifier": "ESS-0001",
    "statement": "レビュー材料は送信前に固定する",
    "kind": "invariant",
    "evidence": (
      "ReviewCompass:tools/api_providers/source_bundle.py:1",
    ),
    "related_tests": (
      "ReviewCompass:tools/api_providers/tests/test_source_bundle.py",
    ),
    "dependencies": (),
    "disposition": "transfer",
    "rationale": "固定済み材料の改変防止に必要",
    "destination": "review.material_bundle",
  }
  value.update(overrides)
  return value


def test_builds_deterministic_ledger_with_typed_fields():
  ledger = importlib.import_module(
    "tools.extraction.essence_ledger"
  )
  records = (
    _record(),
    _record(
      identifier="ESS-0002",
      statement="旧承認状態は引き継がない",
      kind="user_decision",
      evidence=(
        "ReviewCompass2:docs/design/user-decisions-inventory.md:10",
      ),
      related_tests=(),
      dependencies=("ESS-0001",),
      disposition="redesign",
      rationale="新しいintentから再承認するため",
      destination="governance.approval",
    ),
  )

  result = ledger.build_essence_ledger(records)

  assert result.status == "complete"
  assert tuple(item.identifier for item in result.items) == (
    "ESS-0001",
    "ESS-0002",
  )
  assert result.items[0].kind.value == "invariant"
  assert result.items[1].disposition.value == "redesign"
  assert result.items[1].dependencies == ("ESS-0001",)
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "record",
  (
    _record(evidence=()),
    _record(kind="unknown"),
    _record(dependencies=("ESS-9999",)),
    _record(rationale=""),
    _record(destination=None),
    _record(
      disposition="reject",
      destination="must-not-have-destination",
    ),
  ),
)
def test_rejects_missing_evidence_invalid_types_or_incomplete_judgment(
  record,
):
  ledger = importlib.import_module(
    "tools.extraction.essence_ledger"
  )

  with pytest.raises(ledger.EssenceLedgerError):
    ledger.build_essence_ledger((record,))


def test_rejected_item_requires_reason_but_no_destination():
  ledger = importlib.import_module(
    "tools.extraction.essence_ledger"
  )

  result = ledger.build_essence_ledger((
    _record(
      disposition="reject",
      rationale="旧製品固有の承認状態だから",
      destination=None,
    ),
  ))

  assert result.status == "complete"
  assert result.items[0].destination is None
