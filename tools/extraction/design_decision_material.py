"""設計評価競合の未選択判断材料。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


class DesignDecisionMaterialError(Exception):
  """設計判断材料を安全かつ中立に構成できない。"""


@dataclasses.dataclass(frozen=True, order=True)
class DesignDecisionOption:
  disposition: str
  statement: str
  rationale: str
  destination: object
  evidence: tuple


@dataclasses.dataclass(frozen=True)
class DesignDecisionMaterial:
  status: str
  identifier: str
  question: str
  options: tuple
  selected_disposition: object
  approval_candidate: dict
  digest: str


_DISPOSITIONS = frozenset({"transfer", "redesign", "reject"})
_FIELDS = {
  "disposition",
  "statement",
  "rationale",
  "destination",
  "evidence",
}


def _text(value):
  return (
    isinstance(value, str)
    and bool(value.strip())
    and "\n" not in value
  )


def _parse_option(value):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or value["disposition"] not in _DISPOSITIONS
    or not _text(value["statement"])
    or not _text(value["rationale"])
    or not isinstance(value["evidence"], (list, tuple))
    or not value["evidence"]
    or len(set(value["evidence"])) != len(value["evidence"])
    or any(not _text(item) for item in value["evidence"])
  ):
    raise DesignDecisionMaterialError(
      "design options require fixed reasoned evidence"
    )
  destination = value["destination"]
  if (
    value["disposition"] == "reject"
    and destination is not None
  ) or (
    value["disposition"] != "reject"
    and not _text(destination)
  ):
    raise DesignDecisionMaterialError(
      "option disposition and destination are inconsistent"
    )
  return DesignDecisionOption(
    disposition=value["disposition"],
    statement=value["statement"],
    rationale=value["rationale"],
    destination=destination,
    evidence=tuple(sorted(value["evidence"])),
  )


def build_design_decision_material(
  *,
  identifier,
  question,
  current_disposition,
  options,
):
  if (
    not _text(identifier)
    or not _text(question)
    or current_disposition != "follow_up"
  ):
    raise DesignDecisionMaterialError(
      "design decision must remain an identified follow-up"
    )
  parsed = tuple(sorted(
    (_parse_option(value) for value in tuple(options)),
    key=lambda option: option.disposition,
  ))
  if (
    len(parsed) != len(_DISPOSITIONS)
    or {option.disposition for option in parsed}
    != _DISPOSITIONS
  ):
    raise DesignDecisionMaterialError(
      "transfer, redesign, and reject options are required"
    )
  document = {
    "current_disposition": current_disposition,
    "identifier": identifier,
    "options": [
      dataclasses.asdict(option) for option in parsed
    ],
    "question": question,
    "schema_version": 1,
    "selected_disposition": None,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return DesignDecisionMaterial(
    status="awaiting_user_review",
    identifier=identifier,
    question=question,
    options=parsed,
    selected_disposition=None,
    approval_candidate={
      "approved": False,
      "material_digest": digest,
      "selected_disposition": None,
      "target_id": identifier,
    },
    digest=digest,
  )
