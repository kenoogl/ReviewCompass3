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


@dataclasses.dataclass(frozen=True)
class DesignDecisionSelection:
  status: str
  identifier: str
  selected_disposition: str
  destination: object
  statement: str
  rationale: str
  evidence: tuple
  material_digest: str
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


def select_design_decision(material, approval):
  if (
    not isinstance(material, DesignDecisionMaterial)
    or material.status != "awaiting_user_review"
    or material.selected_disposition is not None
    or not isinstance(approval, dict)
    or set(approval) != {
      "approved",
      "material_digest",
      "selected_disposition",
      "target_id",
    }
    or approval["approved"] is not True
    or approval["material_digest"] != material.digest
    or approval["target_id"] != material.identifier
  ):
    raise DesignDecisionMaterialError(
      "selection requires matching explicit approval"
    )
  by_disposition = {
    option.disposition: option
    for option in material.options
  }
  selected = by_disposition.get(
    approval["selected_disposition"]
  )
  if selected is None:
    raise DesignDecisionMaterialError(
      "selected disposition must be a material option"
    )
  document = {
    "approval": dict(approval),
    "identifier": material.identifier,
    "material_digest": material.digest,
    "selected_option": dataclasses.asdict(selected),
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return DesignDecisionSelection(
    status="resolved",
    identifier=material.identifier,
    selected_disposition=selected.disposition,
    destination=selected.destination,
    statement=selected.statement,
    rationale=selected.rationale,
    evidence=selected.evidence,
    material_digest=material.digest,
    digest=digest,
  )
