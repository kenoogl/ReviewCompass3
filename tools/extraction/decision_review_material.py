"""旧利用者決定候補の再確認材料。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


class DecisionReviewMaterialError(Exception):
  """再確認材料を安全かつ一意に構成できない。"""


@dataclasses.dataclass(frozen=True, order=True)
class DecisionEvidenceLayer:
  layer: str
  role: str
  limitation: str


@dataclasses.dataclass(frozen=True)
class DecisionReviewEntry:
  identifier: str
  statement: str
  review_kind: str
  rationale: str
  current_disposition: str
  sources: tuple


@dataclasses.dataclass(frozen=True)
class DecisionReviewMaterial:
  status: str
  entries: tuple
  approval_targets: tuple
  information_targets: tuple
  approval_candidate: object
  digest: str


def _text(value):
  return isinstance(value, str) and bool(value.strip())


def _parse_source(value):
  if (
    not isinstance(value, dict)
    or set(value) != {"layer", "role", "limitation"}
    or any(not _text(value[key]) for key in value)
  ):
    raise DecisionReviewMaterialError(
      "decision evidence layers require fixed non-empty fields"
    )
  return DecisionEvidenceLayer(
    layer=value["layer"],
    role=value["role"],
    limitation=value["limitation"],
  )


def _parse_candidate(value):
  if (
    not isinstance(value, dict)
    or set(value) != {
      "identifier",
      "statement",
      "review_kind",
      "rationale",
      "current_disposition",
      "sources",
    }
    or not _text(value["identifier"])
    or not _text(value["statement"])
    or value["review_kind"] not in {"approval", "information"}
    or not _text(value["rationale"])
    or value["current_disposition"] != "follow_up"
    or not isinstance(value["sources"], (list, tuple))
    or not value["sources"]
  ):
    raise DecisionReviewMaterialError(
      "decision candidates must remain reasoned follow-ups"
    )
  sources = tuple(sorted(
    _parse_source(source) for source in value["sources"]
  ))
  if value["review_kind"] == "approval" and not any(
    source.role.startswith("primary_") for source in sources
  ):
    raise DecisionReviewMaterialError(
      "approval target requires primary decision evidence"
    )
  return DecisionReviewEntry(
    identifier=value["identifier"],
    statement=value["statement"],
    review_kind=value["review_kind"],
    rationale=value["rationale"],
    current_disposition=value["current_disposition"],
    sources=sources,
  )


def build_decision_review_material(candidates):
  values = tuple(candidates)
  if not values:
    raise DecisionReviewMaterialError(
      "decision review candidates are required"
    )
  entries = tuple(sorted(
    (_parse_candidate(value) for value in values),
    key=lambda entry: entry.identifier,
  ))
  identifiers = tuple(entry.identifier for entry in entries)
  if len(set(identifiers)) != len(identifiers):
    raise DecisionReviewMaterialError(
      "decision candidate identifiers must be unique"
    )
  approval_targets = tuple(
    entry.identifier
    for entry in entries
    if entry.review_kind == "approval"
  )
  information_targets = tuple(
    entry.identifier
    for entry in entries
    if entry.review_kind == "information"
  )
  document = {
    "approval_targets": list(approval_targets),
    "entries": [
      {
        **{
          key: value
          for key, value in dataclasses.asdict(entry).items()
          if key != "sources"
        },
        "sources": [
          dataclasses.asdict(source)
          for source in entry.sources
        ],
      }
      for entry in entries
    ],
    "information_targets": list(information_targets),
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  candidate = None
  if approval_targets:
    candidate = {
      "approved": False,
      "target_ids": list(approval_targets),
      "material_digest": digest,
    }
  return DecisionReviewMaterial(
    status=(
      "awaiting_user_review"
      if approval_targets
      else "complete"
    ),
    entries=entries,
    approval_targets=approval_targets,
    information_targets=information_targets,
    approval_candidate=candidate,
    digest=digest,
  )
