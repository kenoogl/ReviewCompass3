"""第2段の独立生材料再判定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re


ALLOWED_PATHS = frozenset({"main", "independent"})
ALLOWED_DECISIONS = frozenset({
  "transfer",
  "redesign",
  "reject",
  "follow_up",
})
_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")


class ReassessmentError(Exception):
  """同一生材料に基づく独立再判定を確定できない。"""


@dataclasses.dataclass(frozen=True)
class Reassessment:
  path: str
  material_digest: str
  raw_evidence: tuple
  decisions: tuple


@dataclasses.dataclass(frozen=True)
class ReassessmentConflict:
  identifier: str
  main_decision: str
  independent_decision: str


@dataclasses.dataclass(frozen=True)
class ReassessmentResult:
  status: str
  agreed: tuple
  conflicts: tuple
  digest: str


def _valid_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _parse_assessment(value, material_digest, item_ids):
  if (
    not isinstance(value, dict)
    or set(value) != {
      "path",
      "material_digest",
      "raw_evidence",
      "decisions",
    }
    or value["path"] not in ALLOWED_PATHS
    or value["material_digest"] != material_digest
    or not isinstance(value["raw_evidence"], (list, tuple))
    or not value["raw_evidence"]
    or len(set(value["raw_evidence"]))
    != len(value["raw_evidence"])
    or any(
      not _valid_text(reference)
      for reference in value["raw_evidence"]
    )
    or not isinstance(value["decisions"], dict)
    or set(value["decisions"]) != set(item_ids)
    or any(
      decision not in ALLOWED_DECISIONS
      for decision in value["decisions"].values()
    )
  ):
    raise ReassessmentError(
      "Reassessment must cover fixed raw material and every item"
    )
  return Reassessment(
    path=value["path"],
    material_digest=value["material_digest"],
    raw_evidence=tuple(sorted(value["raw_evidence"])),
    decisions=tuple(sorted(value["decisions"].items())),
  )


def reconcile_reassessments(
  material_digest,
  item_ids,
  assessments,
) -> ReassessmentResult:
  identifiers = tuple(item_ids)
  if (
    not isinstance(material_digest, str)
    or _DIGEST_PATTERN.fullmatch(material_digest) is None
    or not identifiers
    or len(set(identifiers)) != len(identifiers)
    or any(not _valid_text(item) for item in identifiers)
  ):
    raise ReassessmentError(
      "Material digest and item identifiers must be fixed"
    )
  values = tuple(
    _parse_assessment(
      assessment,
      material_digest,
      identifiers,
    )
    for assessment in assessments
  )
  if (
    len(values) != 2
    or {value.path for value in values} != ALLOWED_PATHS
  ):
    raise ReassessmentError(
      "Exactly one main and one independent assessment are required"
    )
  by_path = {value.path: value for value in values}
  main = dict(by_path["main"].decisions)
  independent = dict(by_path["independent"].decisions)
  agreed = []
  conflicts = []
  for identifier in sorted(identifiers):
    if main[identifier] == independent[identifier]:
      agreed.append((identifier, main[identifier]))
    else:
      conflicts.append(ReassessmentConflict(
        identifier=identifier,
        main_decision=main[identifier],
        independent_decision=independent[identifier],
      ))

  document = {
    "agreed": [
      {"decision": decision, "identifier": identifier}
      for identifier, decision in agreed
    ],
    "assessments": [
      {
        "decisions": dict(value.decisions),
        "material_digest": value.material_digest,
        "path": value.path,
        "raw_evidence": list(value.raw_evidence),
      }
      for value in sorted(values, key=lambda value: value.path)
    ],
    "conflicts": [
      dataclasses.asdict(conflict)
      for conflict in conflicts
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
  return ReassessmentResult(
    status="blocked" if conflicts else "complete",
    agreed=tuple(agreed),
    conflicts=tuple(conflicts),
    digest=digest,
  )
