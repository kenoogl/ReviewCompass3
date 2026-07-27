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


@dataclasses.dataclass(frozen=True)
class ObligationSourceRecord:
  obligation_id: str
  requirement_id: str
  intent_refs: tuple
  essence_ids: tuple
  rationale: str


@dataclasses.dataclass(frozen=True)
class ObligationSourceTrace:
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
_OBLIGATION_ID = re.compile(
  r"(REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,})"
  r"#(statement|inputs|outputs|stop_conditions|"
  r"recovery_conditions|preserved_artifacts|"
  r"acceptance_criteria|non_goals)"
)
_ATOMIC_OBLIGATION_ID = re.compile(
  r"(REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,})"
  r"#(?:statement|(?:inputs|outputs|stop_conditions|"
  r"recovery_conditions|preserved_artifacts|"
  r"acceptance_criteria|non_goals)\.[0-9]{3})"
)
_DISPOSITIONS = {"selected", "not_selected"}
_OBLIGATION_FIELDS = {
  "obligation_id",
  "requirement_id",
  "intent_refs",
  "essence_ids",
  "rationale",
}
_ATOMIC_RELATION_FIELDS = {
  "obligation_id",
  "source_requirement_id",
}
_ATOMIC_LIST_FIELDS = (
  "inputs",
  "outputs",
  "stop_conditions",
  "recovery_conditions",
  "preserved_artifacts",
  "acceptance_criteria",
  "non_goals",
)


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


def validate_obligation_sources(
  *,
  records,
  required_obligation_ids,
  defined_requirement_ids,
  defined_intent_ids,
  defined_essence_ids,
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
  obligations = tuple(required_obligation_ids)
  if (
    len(set(obligations)) != len(obligations)
    or any(
      not _text(value)
      or _OBLIGATION_ID.fullmatch(value) is None
      or value.split("#", 1)[0] not in requirement_ids
      for value in obligations
    )
  ):
    raise RequirementSourceTraceError(
      "obligation definitions must be unique and resolve"
    )
  required = frozenset(obligations)
  parsed = []
  for value in records:
    if (
      not isinstance(value, dict)
      or set(value) != _OBLIGATION_FIELDS
      or not _text(value["rationale"])
    ):
      raise RequirementSourceTraceError(
        "obligation records require fixed non-empty fields"
      )
    obligation_id = value["obligation_id"]
    requirement_id = value["requirement_id"]
    match = (
      _OBLIGATION_ID.fullmatch(obligation_id)
      if _text(obligation_id)
      else None
    )
    if (
      match is None
      or obligation_id not in required
      or requirement_id not in requirement_ids
      or match.group(1) != requirement_id
    ):
      raise RequirementSourceTraceError(
        "obligation relation must resolve to its requirement"
      )
    parsed.append(ObligationSourceRecord(
      obligation_id=obligation_id,
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
      rationale=value["rationale"],
    ))
  relation_ids = tuple(
    record.obligation_id for record in parsed
  )
  if (
    len(set(relation_ids)) != len(relation_ids)
    or set(relation_ids) != required
  ):
    raise RequirementSourceTraceError(
      "every obligation requires one source relation"
    )
  ordered = tuple(sorted(
    parsed,
    key=lambda record: record.obligation_id,
  ))
  document = {
    "records": [
      dataclasses.asdict(record)
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
  return ObligationSourceTrace(
    status="complete",
    records=ordered,
    digest=digest,
  )


def _atomic_obligations(requirement):
  if (
    not isinstance(requirement, dict)
    or not _text(requirement.get("requirement_id"))
    or _REQUIREMENT_ID.fullmatch(
      requirement["requirement_id"]
    ) is None
    or not _text(requirement.get("statement"))
  ):
    raise RequirementSourceTraceError(
      "atomic obligations require a valid requirement"
    )
  requirement_id = requirement["requirement_id"]
  result = [(
    f"{requirement_id}#statement",
    requirement["statement"],
  )]
  for field in _ATOMIC_LIST_FIELDS:
    values = requirement.get(field)
    if (
      not isinstance(values, (list, tuple))
      or not values
      or any(not _text(value) for value in values)
    ):
      raise RequirementSourceTraceError(
        "atomic obligation fields must be non-empty"
      )
    result.extend(
      (
        f"{requirement_id}#{field}.{index:03d}",
        value,
      )
      for index, value in enumerate(values, start=1)
    )
  return tuple(result)


def validate_atomic_obligation_sources(
  *,
  requirements,
  relations,
  source_records,
  defined_intent_ids,
  defined_essence_ids,
):
  requirement_values = tuple(requirements)
  requirement_ids = _defined(
    (
      value.get("requirement_id")
      if isinstance(value, dict)
      else None
      for value in requirement_values
    ),
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
  sources = tuple(
    _record(
      value,
      requirement_ids=requirement_ids,
      intent_ids=intent_ids,
      essence_ids=essence_ids,
    )
    for value in source_records
  )
  source_by_requirement = {
    value.requirement_id: value
    for value in sources
    if value.requirement_id is not None
  }
  if set(source_by_requirement) != requirement_ids:
    raise RequirementSourceTraceError(
      "every requirement requires a source record"
    )
  atomic_values = dict(
    item
    for requirement in requirement_values
    for item in _atomic_obligations(requirement)
  )
  parsed = []
  relation_ids = []
  for value in relations:
    if (
      not isinstance(value, dict)
      or set(value) != _ATOMIC_RELATION_FIELDS
    ):
      raise RequirementSourceTraceError(
        "atomic relations require fixed fields"
      )
    obligation_id = value["obligation_id"]
    source_requirement_id = value[
      "source_requirement_id"
    ]
    match = (
      _ATOMIC_OBLIGATION_ID.fullmatch(obligation_id)
      if _text(obligation_id)
      else None
    )
    if (
      match is None
      or obligation_id not in atomic_values
      or source_requirement_id not in source_by_requirement
      or match.group(1) != source_requirement_id
    ):
      raise RequirementSourceTraceError(
        "atomic obligation relation must resolve"
      )
    source = source_by_requirement[source_requirement_id]
    relation_ids.append(obligation_id)
    parsed.append(ObligationSourceRecord(
      obligation_id=obligation_id,
      requirement_id=source_requirement_id,
      intent_refs=source.intent_refs,
      essence_ids=source.essence_ids,
      rationale=source.rationale,
    ))
  if (
    len(set(relation_ids)) != len(relation_ids)
    or set(relation_ids) != set(atomic_values)
  ):
    raise RequirementSourceTraceError(
      "every atomic obligation requires one source relation"
    )
  ordered = tuple(sorted(
    parsed,
    key=lambda record: record.obligation_id,
  ))
  document = {
    "records": [
      {
        **dataclasses.asdict(record),
        "text": atomic_values[record.obligation_id],
      }
      for record in ordered
    ],
    "schema_version": 2,
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return ObligationSourceTrace(
    status="complete",
    records=ordered,
    digest=digest,
  )
