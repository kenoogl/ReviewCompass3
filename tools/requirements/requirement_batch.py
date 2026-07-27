"""第4段のrequirements batch契約。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re


class RequirementBatchError(Exception):
  """requirements batchを安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class Requirement:
  requirement_id: str
  feature_id: str
  statement: str
  inputs: tuple
  outputs: tuple
  stop_conditions: tuple
  recovery_conditions: tuple
  preserved_artifacts: tuple
  acceptance_criteria: tuple
  non_goals: tuple


@dataclasses.dataclass(frozen=True)
class RequirementBatch:
  status: str
  requirements: tuple
  requirement_count: int
  digest: str


_FIELDS = {
  "requirement_id",
  "feature_id",
  "statement",
  "inputs",
  "outputs",
  "stop_conditions",
  "recovery_conditions",
  "preserved_artifacts",
  "acceptance_criteria",
  "non_goals",
}
_LIST_FIELDS = (
  "inputs",
  "outputs",
  "stop_conditions",
  "recovery_conditions",
  "preserved_artifacts",
  "acceptance_criteria",
  "non_goals",
)
_REQUIREMENT_ID = re.compile(
  r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_FEATURE_ID = re.compile(
  r"FEAT-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)


def _text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _texts(value, label):
  if not isinstance(value, (list, tuple)):
    raise RequirementBatchError(
      f"{label} must be a sequence"
    )
  result = tuple(value)
  if (
    not result
    or len(set(result)) != len(result)
    or any(not _text(item) for item in result)
  ):
    raise RequirementBatchError(
      f"{label} must contain unique non-empty text"
    )
  return tuple(sorted(result))


def _defined_features(values):
  result = tuple(values)
  if (
    not result
    or len(set(result)) != len(result)
    or any(
      not _text(value)
      or _FEATURE_ID.fullmatch(value) is None
      for value in result
    )
  ):
    raise RequirementBatchError(
      "feature definitions must be unique valid IDs"
    )
  return frozenset(result)


def _requirement(value, feature_ids):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or not _text(value["requirement_id"])
    or _REQUIREMENT_ID.fullmatch(
      value["requirement_id"]
    ) is None
    or not _text(value["feature_id"])
    or value["feature_id"] not in feature_ids
    or not _text(value["statement"])
  ):
    raise RequirementBatchError(
      "requirements require fixed non-empty fields"
    )
  parsed_lists = {
    field: _texts(value[field], field)
    for field in _LIST_FIELDS
  }
  return Requirement(
    requirement_id=value["requirement_id"],
    feature_id=value["feature_id"],
    statement=value["statement"],
    inputs=parsed_lists["inputs"],
    outputs=parsed_lists["outputs"],
    stop_conditions=parsed_lists["stop_conditions"],
    recovery_conditions=parsed_lists[
      "recovery_conditions"
    ],
    preserved_artifacts=parsed_lists[
      "preserved_artifacts"
    ],
    acceptance_criteria=parsed_lists[
      "acceptance_criteria"
    ],
    non_goals=parsed_lists["non_goals"],
  )


def validate_requirement_batch(
  *,
  requirements,
  defined_feature_ids,
):
  feature_ids = _defined_features(defined_feature_ids)
  parsed = tuple(
    _requirement(value, feature_ids)
    for value in requirements
  )
  if not parsed:
    raise RequirementBatchError(
      "requirement batch must not be empty"
    )
  requirement_ids = tuple(
    requirement.requirement_id
    for requirement in parsed
  )
  if len(set(requirement_ids)) != len(requirement_ids):
    raise RequirementBatchError(
      "requirement IDs must be unique"
    )
  ordered = tuple(sorted(
    parsed,
    key=lambda requirement: requirement.requirement_id,
  ))
  document = {
    "requirements": [
      {
        "acceptance_criteria": list(
          requirement.acceptance_criteria
        ),
        "feature_id": requirement.feature_id,
        "inputs": list(requirement.inputs),
        "non_goals": list(requirement.non_goals),
        "outputs": list(requirement.outputs),
        "preserved_artifacts": list(
          requirement.preserved_artifacts
        ),
        "recovery_conditions": list(
          requirement.recovery_conditions
        ),
        "requirement_id": requirement.requirement_id,
        "statement": requirement.statement,
        "stop_conditions": list(
          requirement.stop_conditions
        ),
      }
      for requirement in ordered
    ],
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
  return RequirementBatch(
    status="complete",
    requirements=ordered,
    requirement_count=len(ordered),
    digest=digest,
  )
