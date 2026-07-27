"""実測follow_upの根拠付き再検証。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


class EmpiricalRevalidationError(Exception):
  """実測follow_upを根拠付きで再分類できない。"""


@dataclasses.dataclass(frozen=True, order=True)
class EmpiricalObservation:
  name: str
  status: str
  evidence: str
  rationale: str


@dataclasses.dataclass(frozen=True)
class EmpiricalRevalidationItem:
  identifier: str
  status: str
  observations: tuple


@dataclasses.dataclass(frozen=True)
class EmpiricalRevalidation:
  status: str
  resolved: tuple
  follow_up: tuple
  information: tuple
  items: tuple
  digest: str


_STATUSES = frozenset({"resolved", "follow_up", "information"})


def _text(value):
  return isinstance(value, str) and bool(value.strip())


def _parse_observation(value):
  if (
    not isinstance(value, dict)
    or set(value)
    != {"name", "status", "evidence", "rationale"}
    or not _text(value["name"])
    or value["status"] not in _STATUSES
    or not _text(value["evidence"])
    or not _text(value["rationale"])
  ):
    raise EmpiricalRevalidationError(
      "observations require known status and explicit evidence"
    )
  return EmpiricalObservation(
    name=value["name"],
    status=value["status"],
    evidence=value["evidence"],
    rationale=value["rationale"],
  )


def _parse_item(value):
  if (
    not isinstance(value, dict)
    or set(value) != {"identifier", "observations"}
    or not _text(value["identifier"])
    or not isinstance(value["observations"], (list, tuple))
    or not value["observations"]
  ):
    raise EmpiricalRevalidationError(
      "empirical item requires observations"
    )
  observations = tuple(sorted(
    _parse_observation(observation)
    for observation in value["observations"]
  ))
  names = tuple(observation.name for observation in observations)
  if len(set(names)) != len(names):
    raise EmpiricalRevalidationError(
      "observation names must be unique"
    )
  statuses = {observation.status for observation in observations}
  if "follow_up" in statuses:
    status = "follow_up"
  elif "resolved" in statuses:
    status = "resolved"
  else:
    status = "information"
  return EmpiricalRevalidationItem(
    identifier=value["identifier"],
    status=status,
    observations=observations,
  )


def revalidate_empirical_followups(records):
  values = tuple(records)
  if not values:
    raise EmpiricalRevalidationError(
      "empirical follow-up records are required"
    )
  items = tuple(sorted(
    (_parse_item(value) for value in values),
    key=lambda item: item.identifier,
  ))
  identifiers = tuple(item.identifier for item in items)
  if len(set(identifiers)) != len(identifiers):
    raise EmpiricalRevalidationError(
      "empirical item identifiers must be unique"
    )
  partitions = {
    status: tuple(
      item.identifier
      for item in items
      if item.status == status
    )
    for status in _STATUSES
  }
  document = {
    "items": [
      {
        "identifier": item.identifier,
        "observations": [
          dataclasses.asdict(observation)
          for observation in item.observations
        ],
        "status": item.status,
      }
      for item in items
    ],
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return EmpiricalRevalidation(
    status=(
      "follow_up"
      if partitions["follow_up"]
      else "complete"
    ),
    resolved=partitions["resolved"],
    follow_up=partitions["follow_up"],
    information=partitions["information"],
    items=items,
    digest=digest,
  )
