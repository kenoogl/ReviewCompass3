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
):
  parsed_designs = tuple(designs)
  if not parsed_designs:
    raise DesignContractError(
      "architecture requires designs"
    )
  design_ids = set()
  design_feature_map = {}
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
      transitions.append(dict(transition))
    if not transitions:
      raise DesignContractError(
        "state machines require transitions"
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

  document = {
    "boundaries": sorted(
      parsed_boundaries,
      key=lambda value: value["boundary_id"],
    ),
    "interfaces": sorted(
      parsed_interfaces,
      key=lambda value: value["interface_id"],
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
    digest=digest,
  )
