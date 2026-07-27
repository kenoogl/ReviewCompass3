"""第5段のdesign契約に関する暫定テスト。"""

import copy
import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]


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


def test_validates_protocol_boundary_map_and_event_routes():
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
        "identity_fields": (
          "context_id",
          "freshness_verdict",
        ),
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
    protocols=(
      {
        "protocol_id": "PROTOCOL-RUN-START",
        "initial_interfaces": (
          "IF-CONTEXT-EXEC",
        ),
        "initial_states": {
          "SM-WORKFLOW": "ready",
        },
        "expected_states": {
          "SM-WORKFLOW": "blocked",
        },
        "steps": (
          {
            "step_id": "RUN-START-001",
            "actor_design_id": "DES-CONTEXT",
            "interface_id": "IF-CONTEXT-EXEC",
            "interface_role": "input",
            "state_machine_id": "SM-WORKFLOW",
            "from_state": "ready",
            "event": "fail",
            "to_state": "blocked",
            "on_failure": (
              {
                "machine_id": "SM-WORKFLOW",
                "from_state": "ready",
                "event": "fail",
                "to_state": "blocked",
                "persistence": "before visibility",
              },
            ),
            "failure_expected_states": {
              "SM-WORKFLOW": "blocked",
            },
          },
        ),
      },
    ),
    boundary_interface_map={
      "BOUNDARY-001": ("IF-CONTEXT-EXEC",),
    },
    event_routes=(
      {
        "route_id": "ROUTE-RUN-FAIL",
        "source_interface_id": "IF-CONTEXT-EXEC",
        "target_state_machine_id": "SM-WORKFLOW",
        "event": "fail",
      },
    ),
    required_interface_fields={
      "IF-CONTEXT-EXEC": (
        "context_id",
        "freshness_verdict",
      ),
    },
    required_protocol_machine_ids=("SM-WORKFLOW",),
  )

  assert result.protocol_count == 1
  assert result.event_route_count == 1


def test_rejects_protocol_state_sequence_mismatch():
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
          "identity_fields": ("context_id",),
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
      protocols=(
        {
          "protocol_id": "PROTOCOL-RUN-START",
          "initial_interfaces": (),
          "initial_states": {
            "SM-WORKFLOW": "ready",
          },
          "expected_states": {
            "SM-WORKFLOW": "ready",
          },
          "steps": (
            {
              "step_id": "RUN-START-001",
              "actor_design_id": "DES-CONTEXT",
              "interface_id": "IF-CONTEXT-EXEC",
              "interface_role": "input",
              "state_machine_id": "SM-WORKFLOW",
              "from_state": "ready",
              "event": "fail",
              "to_state": "ready",
              "on_failure": (
                {
                  "machine_id": "SM-WORKFLOW",
                  "from_state": "ready",
                  "event": "fail",
                  "to_state": "blocked",
                  "persistence": "before visibility",
                },
              ),
              "failure_expected_states": {
                "SM-WORKFLOW": "blocked",
              },
            },
          ),
        },
      ),
    )


def test_rejects_unreachable_state():
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
      interfaces=(),
      state_machines=(
        {
          "machine_id": "SM-WORKFLOW",
          "owner_design_id": "DES-CONTEXT",
          "states": ("ready", "orphan", "blocked"),
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
      defined_interface_ids=(),
      defined_state_machine_ids=("SM-WORKFLOW",),
    )


def _stage_five_inputs():
  architecture = json.loads((
    ROOT
    / "records/design/stage-five-architecture-integrity.json"
  ).read_text())
  design = json.loads((
    ROOT / "records/design/stage-five-design.json"
  ).read_text())
  requirements = json.loads((
    ROOT
    / "records/requirements/review-context-batch-0001.json"
  ).read_text())["requirements"]
  remaining = json.loads((
    ROOT
    / "records/requirements/remaining-batches-0002-0009.json"
  ).read_text())["batches"]
  for batch in remaining:
    requirements.extend(batch["requirements"])
  relations = json.loads((
    ROOT
    / "records/requirements/requirement-boundary-relations.json"
  ).read_text())["relations"]
  return architecture, design, requirements, relations


def _validate_stage_five(contract, architecture):
  _, design, requirements, relations = _stage_five_inputs()
  return contract.validate_design_architecture(
    designs=design["designs"],
    boundary_catalog=design["boundary_catalog"],
    approved_boundary_relations=relations,
    requirement_feature_map={
      value["requirement_id"]: value["feature_id"]
      for value in requirements
    },
    interfaces=architecture["interfaces"],
    state_machines=architecture["state_machines"],
    defined_interface_ids=[
      value["interface_id"]
      for value in architecture["interfaces"]
    ],
    defined_state_machine_ids=[
      value["machine_id"]
      for value in architecture["state_machines"]
    ],
    protocols=architecture["protocols"],
    boundary_interface_map=(
      architecture["boundary_interface_map"]
    ),
    event_routes=architecture["event_routes"],
    required_interface_fields=(
      architecture["required_interface_fields"]
    ),
    required_boundary_fields=(
      architecture["required_boundary_fields"]
    ),
    required_protocol_machine_ids=(
      architecture["required_protocol_machine_ids"]
    ),
    required_generated_interface_ids=(
      "IF-HARNESS-CAPTURE-RESULT",
      "IF-HARNESS-VALIDATION-CANDIDATE",
      "IF-HARNESS-VALIDATION-RESULT",
      "IF-HARNESS-WORKFLOW-RUN-RESULT",
    ),
    required_failure_state_groups=(
      {
        "SM-RUN": (
          "failed",
          "irrecoverable",
          "blocked",
        ),
        "SM-WORKFLOW": ("blocked",),
      },
    ),
    required_failure_protocol_ids=(
      "PROTOCOL-RUN-START-FAILURE",
      "PROTOCOL-RETRY-FAILURE",
      "PROTOCOL-DISPATCH-FAILURE",
      "PROTOCOL-CAPTURE-DIAGNOSTIC-FAILURE",
      "PROTOCOL-CAPTURE-QUARANTINE",
      "PROTOCOL-CAPTURE-IRRECOVERABLE",
      "PROTOCOL-VALIDATION-FAILURE",
      "PROTOCOL-FINDING-PREFAIL",
      "PROTOCOL-FINDING-FINALFAIL",
    ),
    required_failure_correlations=(
      {
        "source_machine_id": "SM-PROVIDER-CAPTURE",
        "source_from_state": "receiving",
        "source_event": "diagnostic_failed",
        "target_machine_id": "SM-RUN",
        "target_event": "capture_diagnostic_failed",
        "target_state": "failed",
      },
      {
        "source_machine_id": "SM-PROVIDER-CAPTURE",
        "source_from_state": "receiving",
        "source_event": "quarantine",
        "target_machine_id": "SM-RUN",
        "target_event": "capture_quarantined",
        "target_state": "failed",
      },
      {
        "source_machine_id": "SM-PROVIDER-CAPTURE",
        "source_from_state": "receiving",
        "source_event": "fail",
        "target_machine_id": "SM-RUN",
        "target_event": "capture_failed",
        "target_state": "irrecoverable",
      },
    ),
  )


def test_validates_stage_five_architecture_baseline():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  architecture, _, _, _ = _stage_five_inputs()

  result = _validate_stage_five(
    contract,
    architecture,
  )

  assert result.status == "complete"
  assert result.protocol_count == 14


def test_rejects_required_generated_interface_as_initial_input():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  architecture, _, _, _ = _stage_five_inputs()
  architecture = copy.deepcopy(architecture)
  normal = next(
    value
    for value in architecture["protocols"]
    if value["protocol_id"]
    == "PROTOCOL-ATTEMPT-CAPTURE-VALIDATION"
  )
  normal["initial_interfaces"].append(
    "IF-HARNESS-CAPTURE-RESULT"
  )

  with pytest.raises(contract.DesignContractError):
    _validate_stage_five(contract, architecture)


def test_rejects_incomplete_protocol_failure_state_vector():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  architecture, _, _, _ = _stage_five_inputs()
  architecture = copy.deepcopy(architecture)
  normal = next(
    value
    for value in architecture["protocols"]
    if value["protocol_id"]
    == "PROTOCOL-ATTEMPT-CAPTURE-VALIDATION"
  )
  capture_open = next(
    value
    for value in normal["steps"]
    if value["step_id"] == "CAPTURE-001"
  )
  capture_open["on_failure"] = [
    value
    for value in capture_open["on_failure"]
    if value["machine_id"] != "SM-WORKFLOW"
  ]

  with pytest.raises(contract.DesignContractError):
    _validate_stage_five(contract, architecture)


def test_rejects_capture_and_run_failure_classification_mismatch():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  architecture, _, _, _ = _stage_five_inputs()
  architecture = copy.deepcopy(architecture)
  protocol_value = next(
    value
    for value in architecture["protocols"]
    if value["protocol_id"]
    == "PROTOCOL-CAPTURE-IRRECOVERABLE"
  )
  protocol_value["steps"][0]["event"] = "diagnostic_failed"

  with pytest.raises(contract.DesignContractError):
    _validate_stage_five(contract, architecture)


def test_rejects_nonterminal_failure_protocol_main_path():
  contract = importlib.import_module(
    "tools.design.design_contract"
  )
  architecture, _, _, _ = _stage_five_inputs()
  architecture = copy.deepcopy(architecture)
  protocol_value = next(
    value
    for value in architecture["protocols"]
    if value["protocol_id"]
    == "PROTOCOL-RUN-START-FAILURE"
  )
  protocol_value["steps"] = [
    value
    for value in protocol_value["steps"]
    if value["state_machine_id"] != "SM-WORKFLOW"
  ]
  protocol_value["expected_states"]["SM-WORKFLOW"] = (
    "running"
  )

  with pytest.raises(contract.DesignContractError):
    _validate_stage_five(contract, architecture)
