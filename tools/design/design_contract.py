"""第5段のdesignと受け入れ試験の契約。"""

import dataclasses
import hashlib
import json
import re


class DesignContractError(Exception):
  """designを安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class DesignContract:
  status: str
  feature_count: int
  requirement_count: int
  acceptance_test_count: int
  boundary_count: int
  digest: str


@dataclasses.dataclass(frozen=True)
class DesignArchitecture:
  status: str
  boundary_count: int
  interface_count: int
  state_machine_count: int
  protocol_count: int
  event_route_count: int
  digest: str


_DESIGN_FIELDS = {
  "design_id",
  "feature_id",
  "title",
  "decisions",
  "alternatives",
  "rationale",
  "components",
  "machine_responsibilities",
  "llm_responsibilities",
  "human_responsibilities",
  "failure_strategy",
  "requirement_ids",
  "acceptance_test_ids",
  "boundary_ids",
}
_ACCEPTANCE_FIELDS = {
  "test_id",
  "requirement_id",
  "oracle_type",
  "setup",
  "stimulus",
  "expected",
  "negative_case",
}
_LIST_FIELDS = (
  "decisions",
  "alternatives",
  "components",
  "machine_responsibilities",
  "llm_responsibilities",
  "human_responsibilities",
  "failure_strategy",
  "requirement_ids",
  "acceptance_test_ids",
  "boundary_ids",
)
_DESIGN_ID = re.compile(
  r"DES-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_FEATURE_ID = re.compile(
  r"FEAT-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_REQUIREMENT_ID = re.compile(
  r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_TEST_ID = re.compile(
  r"AT-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_BOUNDARY_ID = re.compile(r"BOUNDARY-[0-9]{3,}")
_INTERFACE_ID = re.compile(
  r"IF-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_STATE_MACHINE_ID = re.compile(
  r"SM-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_ORACLE_TYPES = {"machine", "human", "hybrid"}
_BOUNDARY_FIELDS = {
  "boundary_id",
  "from",
  "relation",
  "to",
  "contract",
}
_APPROVED_BOUNDARY_FIELDS = {
  "from",
  "relation",
  "to",
  "contract",
}
_INTERFACE_FIELDS = {
  "interface_id",
  "provider_design_id",
  "consumer_design_id",
  "identity_fields",
  "payload_fields",
  "failure_verdict",
  "owner_design_id",
}
_STATE_MACHINE_FIELDS = {
  "machine_id",
  "owner_design_id",
  "states",
  "events",
  "transitions",
}
_TRANSITION_FIELDS = {
  "from",
  "event",
  "to",
  "guard",
  "persistence",
}
_PROTOCOL_FIELDS = {
  "protocol_id",
  "initial_states",
  "expected_states",
  "steps",
}
_PROTOCOL_STEP_FIELDS = {
  "step_id",
  "actor_design_id",
  "interface_id",
  "interface_role",
  "state_machine_id",
  "from_state",
  "event",
  "to_state",
  "on_failure",
}
_INTERFACE_ROLES = {
  "input",
  "output",
  "internal_evidence",
}
_FAILURE_BRANCH_FIELDS = {
  "machine_id",
  "from_state",
  "event",
  "to_state",
  "persistence",
}
_EVENT_ROUTE_FIELDS = {
  "route_id",
  "source_interface_id",
  "target_state_machine_id",
  "event",
}


def _text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _defined(values, pattern, label, *, empty=False):
  result = tuple(values)
  if (
    (not empty and not result)
    or len(set(result)) != len(result)
    or any(
      not _text(value)
      or pattern.fullmatch(value) is None
      for value in result
    )
  ):
    raise DesignContractError(
      f"{label} definitions must be unique valid IDs"
    )
  return frozenset(result)


def _texts(value, label, *, empty=False):
  if not isinstance(value, (list, tuple)):
    raise DesignContractError(
      f"{label} must be a sequence"
    )
  result = tuple(value)
  if (
    (not empty and not result)
    or len(set(result)) != len(result)
    or any(not _text(item) for item in result)
  ):
    raise DesignContractError(
      f"{label} must contain unique text"
    )
  return result


def validate_design_contract(
  *,
  designs,
  acceptance_tests,
  defined_feature_ids,
  defined_requirement_ids,
  defined_boundary_ids,
):
  feature_ids = _defined(
    defined_feature_ids,
    _FEATURE_ID,
    "feature",
  )
  requirement_ids = _defined(
    defined_requirement_ids,
    _REQUIREMENT_ID,
    "requirement",
  )
  boundary_ids = _defined(
    defined_boundary_ids,
    _BOUNDARY_ID,
    "boundary",
    empty=True,
  )
  parsed_designs = []
  for value in designs:
    if (
      not isinstance(value, dict)
      or set(value) != _DESIGN_FIELDS
      or not _text(value["design_id"])
      or _DESIGN_ID.fullmatch(value["design_id"]) is None
      or value["feature_id"] not in feature_ids
      or not _text(value["title"])
      or not _text(value["rationale"])
    ):
      raise DesignContractError(
        "designs require fixed non-empty fields"
      )
    parsed = dict(value)
    for field in _LIST_FIELDS:
      parsed[field] = _texts(
        value[field],
        field,
        empty=field == "boundary_ids",
      )
    parsed_designs.append(parsed)
  if not parsed_designs:
    raise DesignContractError(
      "design contract requires designs"
    )
  if (
    {value["feature_id"] for value in parsed_designs}
    != feature_ids
    or len({
      value["feature_id"] for value in parsed_designs
    }) != len(parsed_designs)
    or len({
      value["design_id"] for value in parsed_designs
    }) != len(parsed_designs)
  ):
    raise DesignContractError(
      "every feature requires one unique design"
    )
  traced_requirements = [
    item
    for value in parsed_designs
    for item in value["requirement_ids"]
  ]
  traced_boundaries = [
    item
    for value in parsed_designs
    for item in value["boundary_ids"]
  ]
  if (
    len(set(traced_requirements))
    != len(traced_requirements)
    or set(traced_requirements) != requirement_ids
    or len(set(traced_boundaries)) != len(traced_boundaries)
    or set(traced_boundaries) != boundary_ids
  ):
    raise DesignContractError(
      "design coverage must be exact"
    )
  parsed_tests = []
  for value in acceptance_tests:
    if (
      not isinstance(value, dict)
      or set(value) != _ACCEPTANCE_FIELDS
      or not _text(value["test_id"])
      or _TEST_ID.fullmatch(value["test_id"]) is None
      or value["requirement_id"] not in requirement_ids
      or value["oracle_type"] not in _ORACLE_TYPES
      or any(
        not _text(value[field])
        for field in (
          "setup",
          "stimulus",
          "expected",
          "negative_case",
        )
      )
    ):
      raise DesignContractError(
        "acceptance tests require fixed valid fields"
      )
    parsed_tests.append(dict(value))
  test_ids = [value["test_id"] for value in parsed_tests]
  tested_requirements = [
    value["requirement_id"] for value in parsed_tests
  ]
  if (
    len(set(test_ids)) != len(test_ids)
    or len(set(tested_requirements))
    != len(tested_requirements)
    or set(tested_requirements) != requirement_ids
  ):
    raise DesignContractError(
      "every requirement requires one acceptance test"
    )
  test_by_requirement = {
    value["requirement_id"]: value["test_id"]
    for value in parsed_tests
  }
  for design in parsed_designs:
    expected = {
      test_by_requirement[requirement_id]
      for requirement_id in design["requirement_ids"]
    }
    if set(design["acceptance_test_ids"]) != expected:
      raise DesignContractError(
        "design acceptance references must match requirements"
      )
  document = {
    "acceptance_tests": sorted(
      parsed_tests,
      key=lambda value: value["test_id"],
    ),
    "designs": sorted(
      parsed_designs,
      key=lambda value: value["design_id"],
    ),
    "schema_version": 1,
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return DesignContract(
    status="complete",
    feature_count=len(feature_ids),
    requirement_count=len(requirement_ids),
    acceptance_test_count=len(parsed_tests),
    boundary_count=len(boundary_ids),
    digest=digest,
  )


def validate_design_architecture(
  *,
  designs,
  boundary_catalog,
  approved_boundary_relations,
  requirement_feature_map,
  interfaces,
  state_machines,
  defined_interface_ids,
  defined_state_machine_ids,
  protocols=(),
  boundary_interface_map=None,
  event_routes=(),
  required_interface_fields=None,
  required_boundary_fields=None,
  required_protocol_machine_ids=None,
):
  parsed_designs = tuple(designs)
  if not parsed_designs:
    raise DesignContractError(
      "architecture requires designs"
    )
  design_ids = set()
  design_feature_map = {}
  design_by_feature = {}
  boundary_owner_map = {}
  for design in parsed_designs:
    if (
      not isinstance(design, dict)
      or not _text(design.get("design_id"))
      or not _text(design.get("feature_id"))
      or not isinstance(
        design.get("boundary_ids"),
        (list, tuple),
      )
    ):
      raise DesignContractError(
        "architecture designs must resolve"
      )
    design_id = design["design_id"]
    if design_id in design_ids:
      raise DesignContractError(
        "architecture design IDs must be unique"
      )
    design_ids.add(design_id)
    design_feature_map[design_id] = design["feature_id"]
    design_by_feature[design["feature_id"]] = design_id
    for boundary_id in design["boundary_ids"]:
      if boundary_id in boundary_owner_map:
        raise DesignContractError(
          "boundary ownership must be unique"
        )
      boundary_owner_map[boundary_id] = design_id

  approved = tuple(approved_boundary_relations)
  if any(
    not isinstance(value, dict)
    or set(value) != _APPROVED_BOUNDARY_FIELDS
    or any(not _text(value[field]) for field in value)
    for value in approved
  ):
    raise DesignContractError(
      "approved boundary relations are invalid"
    )
  approved_tuples = {
    (
      value["from"],
      value["relation"],
      value["to"],
      value["contract"],
    )
    for value in approved
  }
  if len(approved_tuples) != len(approved):
    raise DesignContractError(
      "approved boundary relations must be unique"
    )

  parsed_boundaries = []
  for value in boundary_catalog:
    if (
      not isinstance(value, dict)
      or set(value) != _BOUNDARY_FIELDS
      or not _text(value["boundary_id"])
      or _BOUNDARY_ID.fullmatch(
        value["boundary_id"]
      ) is None
      or any(
        not _text(value[field])
        for field in ("from", "relation", "to", "contract")
      )
    ):
      raise DesignContractError(
        "boundary catalog entries are invalid"
      )
    relation = (
      value["from"],
      value["relation"],
      value["to"],
      value["contract"],
    )
    owner_id = boundary_owner_map.get(
      value["boundary_id"]
    )
    if (
      relation not in approved_tuples
      or value["from"] not in requirement_feature_map
      or value["to"] not in requirement_feature_map
      or owner_id is None
      or design_feature_map[owner_id]
      != requirement_feature_map[value["from"]]
    ):
      raise DesignContractError(
        "boundary content and ownership must be approved"
      )
    parsed_boundaries.append(dict(value))
  boundary_ids = [
    value["boundary_id"] for value in parsed_boundaries
  ]
  if (
    len(set(boundary_ids)) != len(boundary_ids)
    or set(boundary_ids) != set(boundary_owner_map)
    or {
      (
        value["from"],
        value["relation"],
        value["to"],
        value["contract"],
      )
      for value in parsed_boundaries
    } != approved_tuples
  ):
    raise DesignContractError(
      "boundary catalog coverage must be exact"
    )

  interface_ids = _defined(
    defined_interface_ids,
    _INTERFACE_ID,
    "interface",
    empty=True,
  )
  parsed_interfaces = []
  for value in interfaces:
    if (
      not isinstance(value, dict)
      or set(value) != _INTERFACE_FIELDS
      or value["interface_id"] not in interface_ids
      or value["provider_design_id"] not in design_ids
      or value["consumer_design_id"] not in design_ids
      or value["owner_design_id"] not in design_ids
      or not _text(value["failure_verdict"])
    ):
      raise DesignContractError(
        "interfaces require fixed valid fields"
      )
    parsed = dict(value)
    parsed["identity_fields"] = _texts(
      value["identity_fields"],
      "interface identity fields",
    )
    parsed["payload_fields"] = _texts(
      value["payload_fields"],
      "interface payload fields",
    )
    parsed_interfaces.append(parsed)
  if (
    len({
      value["interface_id"]
      for value in parsed_interfaces
    }) != len(parsed_interfaces)
    or {
      value["interface_id"]
      for value in parsed_interfaces
    } != interface_ids
  ):
    raise DesignContractError(
      "interface coverage must be exact"
    )
  interface_by_id = {
    value["interface_id"]: value
    for value in parsed_interfaces
  }
  if required_interface_fields is not None:
    if (
      not isinstance(required_interface_fields, dict)
      or set(required_interface_fields)
      - interface_ids
    ):
      raise DesignContractError(
        "required interface fields must resolve"
      )
    for interface_id, fields in (
      required_interface_fields.items()
    ):
      required = set(_texts(
        fields,
        "required interface fields",
      ))
      if not required <= set(
        interface_by_id[interface_id][
          "identity_fields"
        ]
      ):
        raise DesignContractError(
          "required interface identity is missing"
        )

  parsed_boundary_map = {}
  if boundary_interface_map is not None:
    if (
      not isinstance(boundary_interface_map, dict)
      or set(boundary_interface_map)
      != set(boundary_ids)
    ):
      raise DesignContractError(
        "boundary interface coverage must be exact"
      )
    boundary_by_id = {
      value["boundary_id"]: value
      for value in parsed_boundaries
    }
    for boundary_id, mapped_ids in (
      boundary_interface_map.items()
    ):
      resolved_ids = _texts(
        mapped_ids,
        "boundary interface IDs",
      )
      if not set(resolved_ids) <= interface_ids:
        raise DesignContractError(
          "boundary interfaces must resolve"
        )
      boundary = boundary_by_id[boundary_id]
      if boundary["relation"] == "depends_on":
        provider_requirement = boundary["to"]
        consumer_requirement = boundary["from"]
      else:
        provider_requirement = boundary["from"]
        consumer_requirement = boundary["to"]
      provider_design = design_by_feature[
        requirement_feature_map[provider_requirement]
      ]
      consumer_design = design_by_feature[
        requirement_feature_map[consumer_requirement]
      ]
      if not any(
        interface_by_id[interface_id][
          "provider_design_id"
        ] == provider_design
        and interface_by_id[interface_id][
          "consumer_design_id"
        ] == consumer_design
        for interface_id in resolved_ids
      ):
        raise DesignContractError(
          "boundary interface endpoints must match"
        )
      parsed_boundary_map[boundary_id] = resolved_ids
  if required_boundary_fields is not None:
    if (
      boundary_interface_map is None
      or not isinstance(required_boundary_fields, dict)
      or set(required_boundary_fields)
      - set(boundary_ids)
    ):
      raise DesignContractError(
        "required boundary fields must resolve"
      )
    for boundary_id, fields in (
      required_boundary_fields.items()
    ):
      required = set(_texts(
        fields,
        "required boundary fields",
      ))
      available = {
        field
        for interface_id
        in parsed_boundary_map[boundary_id]
        for field in (
          *interface_by_id[interface_id][
            "identity_fields"
          ],
          *interface_by_id[interface_id][
            "payload_fields"
          ],
        )
      }
      if not required <= available:
        raise DesignContractError(
          "boundary contract fields are missing"
        )

  machine_ids = _defined(
    defined_state_machine_ids,
    _STATE_MACHINE_ID,
    "state machine",
    empty=True,
  )
  parsed_machines = []
  for value in state_machines:
    if (
      not isinstance(value, dict)
      or set(value) != _STATE_MACHINE_FIELDS
      or value["machine_id"] not in machine_ids
      or value["owner_design_id"] not in design_ids
    ):
      raise DesignContractError(
        "state machines require fixed valid fields"
      )
    states = _texts(
      value["states"],
      "state machine states",
    )
    events = _texts(
      value["events"],
      "state machine events",
    )
    transitions = []
    transition_keys = set()
    for transition in value["transitions"]:
      if (
        not isinstance(transition, dict)
        or set(transition) != _TRANSITION_FIELDS
        or transition["from"] not in states
        or transition["to"] not in states
        or transition["event"] not in events
        or not _text(transition["guard"])
        or not _text(transition["persistence"])
      ):
        raise DesignContractError(
          "state transitions must be closed"
        )
      transition_key = (
        transition["from"],
        transition["event"],
      )
      if transition_key in transition_keys:
        raise DesignContractError(
          "state transitions must be deterministic"
        )
      transition_keys.add(transition_key)
      transitions.append(dict(transition))
    if not transitions:
      raise DesignContractError(
        "state machines require transitions"
      )
    initial_state = states[0]
    reachable = {initial_state}
    while True:
      expanded = reachable | {
        transition["to"]
        for transition in transitions
        if transition["from"] in reachable
      }
      if expanded == reachable:
        break
      reachable = expanded
    outgoing_states = {
      transition["from"]
      for transition in transitions
    }
    terminal_states = set(states) - outgoing_states
    can_reach_terminal = set(terminal_states)
    while True:
      expanded = can_reach_terminal | {
        transition["from"]
        for transition in transitions
        if transition["to"] in can_reach_terminal
      }
      if expanded == can_reach_terminal:
        break
      can_reach_terminal = expanded
    if (
      reachable != set(states)
      or not terminal_states
      or can_reach_terminal != set(states)
    ):
      raise DesignContractError(
        "all states must reach a terminal state"
      )
    parsed = dict(value)
    parsed["states"] = states
    parsed["events"] = events
    parsed["transitions"] = tuple(transitions)
    parsed_machines.append(parsed)
  if (
    len({
      value["machine_id"]
      for value in parsed_machines
    }) != len(parsed_machines)
    or {
      value["machine_id"]
      for value in parsed_machines
    } != machine_ids
  ):
    raise DesignContractError(
      "state machine coverage must be exact"
    )
  machine_by_id = {
    value["machine_id"]: value
    for value in parsed_machines
  }

  parsed_routes = []
  route_ids = set()
  for value in event_routes:
    if (
      not isinstance(value, dict)
      or set(value) != _EVENT_ROUTE_FIELDS
      or not _text(value["route_id"])
      or value["route_id"] in route_ids
      or value["source_interface_id"]
      not in interface_ids
      or value["target_state_machine_id"]
      not in machine_ids
      or value["event"] not in machine_by_id[
        value["target_state_machine_id"]
      ]["events"]
      or machine_by_id[
        value["target_state_machine_id"]
      ]["owner_design_id"] != interface_by_id[
        value["source_interface_id"]
      ]["consumer_design_id"]
    ):
      raise DesignContractError(
        "event routes must resolve"
      )
    route_ids.add(value["route_id"])
    parsed_routes.append(dict(value))

  parsed_protocols = []
  protocol_ids = set()
  step_ids = set()
  for value in protocols:
    if (
      not isinstance(value, dict)
      or set(value) != _PROTOCOL_FIELDS
      or not _text(value["protocol_id"])
      or value["protocol_id"] in protocol_ids
      or not isinstance(value["initial_states"], dict)
      or not isinstance(value["expected_states"], dict)
      or not isinstance(value["steps"], (list, tuple))
      or not value["steps"]
    ):
      raise DesignContractError(
        "protocols require ordered steps"
      )
    protocol_ids.add(value["protocol_id"])
    initial_states = dict(value["initial_states"])
    expected_states = dict(value["expected_states"])
    if (
      not initial_states
      or set(initial_states) != set(expected_states)
      or any(
        machine_id not in machine_ids
        or state not in machine_by_id[machine_id][
          "states"
        ]
        for machine_id, state
        in initial_states.items()
      )
      or any(
        state not in machine_by_id[machine_id][
          "states"
        ]
        for machine_id, state
        in expected_states.items()
      )
    ):
      raise DesignContractError(
        "protocol state contracts must resolve"
      )
    current_states = dict(initial_states)
    steps = []
    for step in value["steps"]:
      if (
        not isinstance(step, dict)
        or set(step) != _PROTOCOL_STEP_FIELDS
        or not _text(step["step_id"])
        or step["step_id"] in step_ids
        or step["actor_design_id"] not in design_ids
        or step["interface_id"] not in interface_ids
        or step["interface_role"] not in _INTERFACE_ROLES
        or step["state_machine_id"] not in machine_ids
        or step["state_machine_id"]
        not in current_states
        or step["from_state"]
        != current_states[step["state_machine_id"]]
        or step["event"] not in machine_by_id[
          step["state_machine_id"]
        ]["events"]
        or step["to_state"] not in machine_by_id[
          step["state_machine_id"]
        ]["states"]
        or not isinstance(
          step["on_failure"],
          (list, tuple),
        )
        or not step["on_failure"]
      ):
        raise DesignContractError(
          "protocol step must resolve: "
          f"{step.get('step_id', '<unknown>')}"
        )
      interface = interface_by_id[step["interface_id"]]
      if step["actor_design_id"] not in {
        interface["provider_design_id"],
        interface["consumer_design_id"],
        interface["owner_design_id"],
      }:
        raise DesignContractError(
          "protocol actor must participate in interface"
        )
      machine_owner = machine_by_id[
        step["state_machine_id"]
      ]["owner_design_id"]
      if (
        step["interface_role"] == "input"
        and interface["consumer_design_id"]
        != machine_owner
      ) or (
        step["interface_role"] == "output"
        and interface["provider_design_id"]
        != machine_owner
      ) or (
        step["interface_role"] == "internal_evidence"
        and machine_owner not in {
          interface["provider_design_id"],
          interface["consumer_design_id"],
        }
      ):
        raise DesignContractError(
          "protocol interface role must match owner"
        )
      if not any(
        transition["from"] == step["from_state"]
        and transition["event"] == step["event"]
        and transition["to"] == step["to_state"]
        for transition in machine_by_id[
          step["state_machine_id"]
        ]["transitions"]
      ):
        raise DesignContractError(
          "protocol step must match state transition"
        )
      for failure in step["on_failure"]:
        if (
          not isinstance(failure, dict)
          or set(failure) != _FAILURE_BRANCH_FIELDS
          or failure["machine_id"] not in machine_ids
          or failure["from_state"] not in machine_by_id[
            failure["machine_id"]
          ]["states"]
          or failure["to_state"] not in machine_by_id[
            failure["machine_id"]
          ]["states"]
          or failure["event"] not in machine_by_id[
            failure["machine_id"]
          ]["events"]
          or not _text(failure["persistence"])
          or not any(
            transition["from"] == failure["from_state"]
            and transition["event"] == failure["event"]
            and transition["to"] == failure["to_state"]
            for transition in machine_by_id[
              failure["machine_id"]
            ]["transitions"]
          )
        ):
          raise DesignContractError(
            "protocol failure branch must match transition"
          )
      current_states[step["state_machine_id"]] = (
        step["to_state"]
      )
      step_ids.add(step["step_id"])
      steps.append(dict(step))
    if current_states != expected_states:
      raise DesignContractError(
      "protocol must reach expected states"
      )
    parsed_protocols.append({
      "expected_states": dict(sorted(
        expected_states.items()
      )),
      "initial_states": dict(sorted(
        initial_states.items()
      )),
      "protocol_id": value["protocol_id"],
      "steps": tuple(steps),
    })
  if required_protocol_machine_ids is not None:
    required_protocol_machines = set(_texts(
      required_protocol_machine_ids,
      "required protocol machine IDs",
    ))
    covered_protocol_machines = {
      machine_id
      for protocol in parsed_protocols
      for machine_id in protocol["initial_states"]
    }
    if (
      required_protocol_machines != machine_ids
      or covered_protocol_machines != machine_ids
    ):
      raise DesignContractError(
        "protocols must cover every state machine"
      )

  document = {
    "boundary_interface_map": dict(sorted(
      parsed_boundary_map.items()
    )),
    "required_boundary_fields": (
      {}
      if required_boundary_fields is None
      else dict(sorted(
        (
          boundary_id,
          tuple(fields),
        )
        for boundary_id, fields
        in required_boundary_fields.items()
      ))
    ),
    "boundaries": sorted(
      parsed_boundaries,
      key=lambda value: value["boundary_id"],
    ),
    "interfaces": sorted(
      parsed_interfaces,
      key=lambda value: value["interface_id"],
    ),
    "event_routes": sorted(
      parsed_routes,
      key=lambda value: value["route_id"],
    ),
    "protocols": sorted(
      parsed_protocols,
      key=lambda value: value["protocol_id"],
    ),
    "required_protocol_machine_ids": (
      ()
      if required_protocol_machine_ids is None
      else tuple(sorted(required_protocol_machine_ids))
    ),
    "schema_version": 1,
    "state_machines": sorted(
      parsed_machines,
      key=lambda value: value["machine_id"],
    ),
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return DesignArchitecture(
    status="complete",
    boundary_count=len(parsed_boundaries),
    interface_count=len(parsed_interfaces),
    state_machine_count=len(parsed_machines),
    protocol_count=len(parsed_protocols),
    event_route_count=len(parsed_routes),
    digest=digest,
  )
