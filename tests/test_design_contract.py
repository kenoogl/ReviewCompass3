"""第5段のdesign契約に関する暫定テスト。"""

import importlib

import pytest


def _design(**overrides):
  value = {
    "design_id": "DES-CONTEXT",
    "feature_id": "FEAT-CONTEXT",
    "title": "Context design",
    "decisions": ("固定材料からContextを構成する",),
    "alternatives": ("会話履歴全体を暗黙利用する",),
    "rationale": "再現可能性を保つため",
    "components": ("context_builder",),
    "machine_responsibilities": ("Digest検証",),
    "llm_responsibilities": ("材料の意味的関連性を提案",),
    "human_responsibilities": ("採用材料を決定",),
    "failure_strategy": ("不一致時は確定しない",),
    "requirement_ids": ("REQ-CONTEXT-001",),
    "acceptance_test_ids": ("AT-CONTEXT-001",),
    "boundary_ids": ("BOUNDARY-001",),
  }
  value.update(overrides)
  return value


def _acceptance(**overrides):
  value = {
    "test_id": "AT-CONTEXT-001",
    "requirement_id": "REQ-CONTEXT-001",
    "oracle_type": "machine",
    "setup": "固定Taskを用意する",
    "stimulus": "Contextを構成する",
    "expected": "同一Digestを返す",
    "negative_case": "材料欠落時は拒否する",
  }
  value.update(overrides)
  return value


def test_validates_complete_design_and_acceptance_coverage():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )

  result = contract.validate_design_contract(
    designs=(_design(),),
    acceptance_tests=(_acceptance(),),
    defined_feature_ids=("FEAT-CONTEXT",),
    defined_requirement_ids=("REQ-CONTEXT-001",),
    defined_boundary_ids=("BOUNDARY-001",),
  )

  assert result.status == "complete"
  assert result.feature_count == 1
  assert result.requirement_count == 1
  assert result.acceptance_test_count == 1
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  ("designs", "acceptance_tests", "boundary_ids"),
  (
    ((), (_acceptance(),), ("BOUNDARY-001",)),
    ((_design(requirement_ids=("REQ-UNKNOWN-001",)),),
     (_acceptance(),), ("BOUNDARY-001",)),
    ((_design(acceptance_test_ids=("AT-UNKNOWN-001",)),),
     (_acceptance(),), ("BOUNDARY-001",)),
    ((_design(boundary_ids=()),),
     (_acceptance(),), ("BOUNDARY-001",)),
    ((_design(),),
     (_acceptance(oracle_type="unknown"),), ("BOUNDARY-001",)),
  ),
)
def test_rejects_incomplete_design_contract(
  designs,
  acceptance_tests,
  boundary_ids,
):
  contract = importlib.import_module(
    "tools.design.design_contract"
  )

  with pytest.raises(contract.DesignContractError):
    contract.validate_design_contract(
      designs=designs,
      acceptance_tests=acceptance_tests,
      defined_feature_ids=("FEAT-CONTEXT",),
      defined_requirement_ids=("REQ-CONTEXT-001",),
      defined_boundary_ids=boundary_ids,
    )


def test_validates_boundary_content_interfaces_and_state_machines():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  result = contract.validate_design_architecture(
    designs=(_design(),),
    boundary_catalog=(
      {
        "boundary_id": "BOUNDARY-001",
        "from": "REQ-CONTEXT-001",
        "relation": "provides_to",
        "to": "REQ-CONTEXT-001",
        "contract": "self test boundary",
      },
    ),
    approved_boundary_relations=(
      {
        "from": "REQ-CONTEXT-001",
        "relation": "provides_to",
        "to": "REQ-CONTEXT-001",
        "contract": "self test boundary",
      },
    ),
    requirement_feature_map={
      "REQ-CONTEXT-001": "FEAT-CONTEXT",
    },
    interfaces=(
      {
        "interface_id": "IF-CONTEXT-EXEC",
        "provider_design_id": "DES-CONTEXT",
        "consumer_design_id": "DES-CONTEXT",
        "identity_fields": ("context_digest",),
        "payload_fields": ("task",),
        "failure_verdict": "blocked",
        "owner_design_id": "DES-CONTEXT",
      },
    ),
    state_machines=(
      {
        "machine_id": "SM-WORKFLOW",
        "owner_design_id": "DES-CONTEXT",
        "states": ("ready", "blocked"),
        "events": ("fail",),
        "transitions": (
          {
            "from": "ready",
            "event": "fail",
            "to": "blocked",
            "guard": "validation failed",
            "persistence": "before visibility",
          },
        ),
      },
    ),
    defined_interface_ids=("IF-CONTEXT-EXEC",),
    defined_state_machine_ids=("SM-WORKFLOW",),
  )

  assert result.status == "complete"
  assert result.boundary_count == 1
  assert result.interface_count == 1
  assert result.state_machine_count == 1


def test_rejects_boundary_content_not_approved():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )

  with pytest.raises(contract.DesignContractError):
    contract.validate_design_architecture(
      designs=(_design(),),
      boundary_catalog=(
        {
          "boundary_id": "BOUNDARY-001",
          "from": "REQ-CONTEXT-001",
          "relation": "provides_to",
          "to": "REQ-CONTEXT-001",
          "contract": "changed",
        },
      ),
      approved_boundary_relations=(
        {
          "from": "REQ-CONTEXT-001",
          "relation": "provides_to",
          "to": "REQ-CONTEXT-001",
          "contract": "approved",
        },
      ),
      requirement_feature_map={
        "REQ-CONTEXT-001": "FEAT-CONTEXT",
      },
      interfaces=(),
      state_machines=(),
      defined_interface_ids=(),
      defined_state_machine_ids=(),
    )
