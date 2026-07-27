"""第4段のrequirement機能境界relation契約。"""

import dataclasses
import hashlib
import json
import re


class BoundaryRelationError(Exception):
  """requirement間の所有境界を安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class BoundaryRelation:
  source: str
  relation: str
  target: str
  contract: str


@dataclasses.dataclass(frozen=True)
class BoundaryRelations:
  status: str
  records: tuple
  relation_count: int
  digest: str


_REQUIREMENT_ID = re.compile(
  r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_FIELDS = {"from", "relation", "to", "contract"}
_RELATIONS = {"depends_on", "provides_to", "returns_to"}


def _text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def validate_boundary_relations(
  *,
  records,
  defined_requirement_ids,
):
  requirement_ids = tuple(defined_requirement_ids)
  if (
    len(set(requirement_ids)) != len(requirement_ids)
    or any(
      not _text(value)
      or _REQUIREMENT_ID.fullmatch(value) is None
      for value in requirement_ids
    )
  ):
    raise BoundaryRelationError(
      "requirement definitions must be unique valid IDs"
    )
  defined = frozenset(requirement_ids)
  parsed = []
  for value in records:
    if (
      not isinstance(value, dict)
      or set(value) != _FIELDS
      or value["relation"] not in _RELATIONS
      or value["from"] not in defined
      or value["to"] not in defined
      or value["from"] == value["to"]
      or not _text(value["contract"])
    ):
      raise BoundaryRelationError(
        "boundary relations must resolve fixed fields"
      )
    parsed.append(BoundaryRelation(
      source=value["from"],
      relation=value["relation"],
      target=value["to"],
      contract=value["contract"],
    ))
  identities = tuple(
    (
      value.source,
      value.relation,
      value.target,
      value.contract,
    )
    for value in parsed
  )
  if len(set(identities)) != len(identities):
    raise BoundaryRelationError(
      "boundary relations must be unique"
    )
  relation_set = set(identities)
  for value in parsed:
    if value.relation == "provides_to":
      reciprocal = (
        value.target,
        "depends_on",
        value.source,
        value.contract,
      )
      if reciprocal not in relation_set:
        raise BoundaryRelationError(
          "provides_to requires reciprocal depends_on"
        )
  ordered = tuple(sorted(
    parsed,
    key=lambda value: (
      value.source,
      value.relation,
      value.target,
      value.contract,
    ),
  ))
  document = {
    "records": [
      {
        "contract": value.contract,
        "from": value.source,
        "relation": value.relation,
        "to": value.target,
      }
      for value in ordered
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
  return BoundaryRelations(
    status="complete",
    records=ordered,
    relation_count=len(ordered),
    digest=digest,
  )
