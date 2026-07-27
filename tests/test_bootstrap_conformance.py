"""第5段のbootstrap適合性監査契約に関する暫定テスト。"""

import importlib

import pytest


def _record(**overrides):
  value = {
    "requirement_id": "REQ-CONTEXT-001",
    "classification": "conformant",
    "target_design_id": "DES-CONTEXT",
    "implementation_evidence": (
      "tools/context.py",
    ),
    "test_evidence": (
      "tests/test_context.py",
    ),
    "rationale": "固定入力と拒否挙動を実装・試験済み",
    "gaps": (),
  }
  value.update(overrides)
  return value


def test_validates_evidence_backed_conformance():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  result = conformance.validate_bootstrap_conformance(
    records=(_record(),),
    defined_requirement_ids=("REQ-CONTEXT-001",),
    defined_design_ids=("DES-CONTEXT",),
    defined_evidence_paths=(
      "tools/context.py",
      "tests/test_context.py",
    ),
    bootstrap_commit="a" * 40,
  )

  assert result.status == "complete"
  assert result.counts["conformant"] == 1
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "record",
  (
    _record(implementation_evidence=()),
    _record(test_evidence=()),
    _record(gaps=("未解決",)),
    _record(classification="unknown"),
    _record(target_design_id="DES-UNKNOWN"),
    _record(implementation_evidence=("tools/unknown.py",)),
  ),
)
def test_rejects_unsupported_conformant_classification(record):
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  with pytest.raises(conformance.BootstrapConformanceError):
    conformance.validate_bootstrap_conformance(
      records=(record,),
      defined_requirement_ids=("REQ-CONTEXT-001",),
      defined_design_ids=("DES-CONTEXT",),
      defined_evidence_paths=(
        "tools/context.py",
        "tests/test_context.py",
      ),
      bootstrap_commit="a" * 40,
    )


def test_requires_gap_for_nonconformant_classification():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  with pytest.raises(conformance.BootstrapConformanceError):
    conformance.validate_bootstrap_conformance(
      records=(_record(
        classification="adapt",
        gaps=(),
      ),),
      defined_requirement_ids=("REQ-CONTEXT-001",),
      defined_design_ids=("DES-CONTEXT",),
      defined_evidence_paths=(
        "tools/context.py",
        "tests/test_context.py",
      ),
      bootstrap_commit="a" * 40,
    )
