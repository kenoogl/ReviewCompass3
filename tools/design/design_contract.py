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
_ORACLE_TYPES = {"machine", "human", "hybrid"}


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
