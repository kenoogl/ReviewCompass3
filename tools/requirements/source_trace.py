"""第4段のrequirement由来記録契約。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re


class RequirementSourceTraceError(Exception):
  """requirementの由来を安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class RequirementSourceRecord:
  requirement_id: object
  intent_refs: tuple
  essence_ids: tuple
  disposition: str
  rationale: str


@dataclasses.dataclass(frozen=True)
class RequirementSourceTrace:
  status: str
  records: tuple
  digest: str


_FIELDS = {
  "requirement_id",
  "intent_refs",
  "essence_ids",
  "disposition",
  "rationale",
}
_REQUIREMENT_ID = re.compile(
  r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_INTENT_ID = re.compile(r"INT-[A-Z0-9]+(?:-[A-Z0-9]+)*")
_ESSENCE_ID = re.compile(r"ESS-[0-9]{4,}")
_DISPOSITIONS = {"selected", "not_selected"}


def _text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _defined(values, pattern, label):
  result = tuple(values)
  if (
    len(set(result)) != len(result)
    or any(
      not _text(value)
      or pattern.fullmatch(value) is None
      for value in result
    )
  ):
    raise RequirementSourceTraceError(
      f"{label} definitions must be unique valid IDs"
    )
  return frozenset(result)


def _references(value, *, defined, pattern, label):
  if not isinstance(value, (list, tuple)):
    raise RequirementSourceTraceError(
      f"{label} references must be a sequence"
    )
  result = tuple(value)
  if (
    not result
    or len(set(result)) != len(result)
    or any(
      not _text(item)
      or pattern.fullmatch(item) is None
      for item in result
    )
    or not set(result) <= defined
  ):
    raise RequirementSourceTraceError(
      f"{label} references must be unique and resolve"
    )
  return tuple(sorted(result))


def _record(
  value,
  *,
  requirement_ids,
  intent_ids,
  essence_ids,
):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or value["disposition"] not in _DISPOSITIONS
    or not _text(value["rationale"])
  ):
    raise RequirementSourceTraceError(
      "source records require fixed non-empty fields"
    )
  requirement_id = value["requirement_id"]
  if value["disposition"] == "selected":
    if (
      not _text(requirement_id)
      or _REQUIREMENT_ID.fullmatch(requirement_id) is None
      or requirement_id not in requirement_ids
    ):
      raise RequirementSourceTraceError(
        "selected records require a defined requirement ID"
      )
  elif requirement_id is not None:
    raise RequirementSourceTraceError(
      "not-selected records must not define a requirement ID"
    )
  return RequirementSourceRecord(
    requirement_id=requirement_id,
    intent_refs=_references(
      value["intent_refs"],
      defined=intent_ids,
      pattern=_INTENT_ID,
      label="intent",
    ),
    essence_ids=_references(
      value["essence_ids"],
      defined=essence_ids,
      pattern=_ESSENCE_ID,
      label="essence",
    ),
    disposition=value["disposition"],
    rationale=value["rationale"],
  )


def validate_requirement_sources(
  *,
  records,
  defined_requirement_ids,
  defined_intent_ids,
  defined_essence_ids,
  allowed_essence_ids=None,
  required_essence_ids=None,
):
  requirement_ids = _defined(
    defined_requirement_ids,
    _REQUIREMENT_ID,
    "requirement",
  )
  intent_ids = _defined(
    defined_intent_ids,
    _INTENT_ID,
    "intent",
  )
  essence_ids = _defined(
    defined_essence_ids,
    _ESSENCE_ID,
    "essence",
  )
  allowed_essences = (
    essence_ids
    if allowed_essence_ids is None
    else _defined(
      allowed_essence_ids,
      _ESSENCE_ID,
      "allowed essence",
    )
  )
  required_essences = (
    frozenset()
    if required_essence_ids is None
    else _defined(
      required_essence_ids,
      _ESSENCE_ID,
      "required essence",
    )
  )
  if (
    not allowed_essences <= essence_ids
    or not required_essences <= allowed_essences
  ):
    raise RequirementSourceTraceError(
      "feature essence definitions must resolve"
    )
  parsed = tuple(
    _record(
      value,
      requirement_ids=requirement_ids,
      intent_ids=intent_ids,
      essence_ids=essence_ids,
    )
    for value in records
  )
  selected_ids = tuple(
    record.requirement_id
    for record in parsed
    if record.requirement_id is not None
  )
  if len(set(selected_ids)) != len(selected_ids):
    raise RequirementSourceTraceError(
      "requirement relations must be unique"
    )
  if set(selected_ids) != requirement_ids:
    raise RequirementSourceTraceError(
      "every defined requirement requires one source relation"
    )
  traced_essences = {
    essence_id
    for record in parsed
    for essence_id in record.essence_ids
  }
  if (
    not traced_essences <= allowed_essences
    or not required_essences <= traced_essences
  ):
    raise RequirementSourceTraceError(
      "feature essence trace is incomplete or out of scope"
    )
  ordered = tuple(sorted(
    parsed,
    key=lambda record: (
      record.requirement_id is None,
      record.requirement_id or "",
      record.essence_ids,
    ),
  ))
  document = {
    "records": [
      {
        "disposition": record.disposition,
        "essence_ids": list(record.essence_ids),
        "intent_refs": list(record.intent_refs),
        "rationale": record.rationale,
        "requirement_id": record.requirement_id,
      }
      for record in ordered
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
  return RequirementSourceTrace(
    status="complete",
    records=ordered,
    digest=digest,
  )
