"""第2段の7軸による初回エッセンス抽出。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import enum
import hashlib
import json
import re


class SevenAxisExtractionError(Exception):
  """候補集合を一意に抽出できない。"""


class ExtractionAxis(enum.Enum):
  USER_DECISION = "user_decision"
  CAPABILITY = "capability"
  PROCEDURE = "procedure"
  INVARIANT = "invariant"
  CONTRACT = "contract"
  RECOVERY = "recovery"
  EMPIRICAL_FINDING = "empirical_finding"


AXIS_ORDER = tuple(axis.value for axis in ExtractionAxis)
_IDENTIFIER_PATTERN = re.compile(r"ESS-[0-9]{4,}")


@dataclasses.dataclass(frozen=True)
class ExtractedEssence:
  identifier: str
  statement: str
  axis: ExtractionAxis
  evidence: tuple
  dependencies: tuple


@dataclasses.dataclass(frozen=True)
class RejectedCandidate:
  identifier: str
  reason: str


@dataclasses.dataclass(frozen=True)
class InitialExtraction:
  status: str
  accepted: tuple
  rejected: tuple
  missing_axes: tuple
  digest: str


def _valid_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _parse_candidate(value):
  if (
    not isinstance(value, dict)
    or set(value) != {
      "identifier",
      "statement",
      "axis",
      "evidence",
      "dependencies",
    }
    or not _valid_text(value["identifier"])
    or _IDENTIFIER_PATTERN.fullmatch(
      value["identifier"]
    ) is None
    or not _valid_text(value["statement"])
    or not isinstance(value["axis"], str)
    or not isinstance(value["evidence"], (list, tuple))
    or len(set(value["evidence"])) != len(value["evidence"])
    or any(
      not _valid_text(reference)
      for reference in value["evidence"]
    )
    or not isinstance(value["dependencies"], (list, tuple))
    or len(set(value["dependencies"]))
    != len(value["dependencies"])
    or any(
      not _valid_text(dependency)
      for dependency in value["dependencies"]
    )
  ):
    raise SevenAxisExtractionError(
      "Extraction candidates require fixed valid fields"
    )
  return {
    "axis": value["axis"],
    "dependencies": tuple(sorted(value["dependencies"])),
    "evidence": tuple(sorted(value["evidence"])),
    "identifier": value["identifier"],
    "statement": value["statement"],
  }


def _evidence_resolves(references, materials):
  for reference in references:
    if reference.count("#") != 1:
      return False
    material, location = reference.split("#", 1)
    if material not in materials or not location:
      return False
  return True


def extract_initial_essences(
  candidates,
  *,
  source_materials,
) -> InitialExtraction:
  materials = tuple(source_materials)
  if (
    not materials
    or len(set(materials)) != len(materials)
    or any(not _valid_text(material) for material in materials)
  ):
    raise SevenAxisExtractionError(
      "Source materials must be unique fixed identifiers"
    )
  values = tuple(
    _parse_candidate(candidate)
    for candidate in candidates
  )
  identifiers = tuple(
    value["identifier"]
    for value in values
  )
  if (
    not values
    or len(set(identifiers)) != len(identifiers)
  ):
    raise SevenAxisExtractionError(
      "Candidate identifiers must be unique"
    )
  identifier_set = set(identifiers)
  material_set = set(materials)
  accepted = []
  rejected = []
  for value in sorted(
    values,
    key=lambda candidate: candidate["identifier"],
  ):
    reason = None
    try:
      axis = ExtractionAxis(value["axis"])
    except ValueError:
      axis = None
      reason = "unknown_axis"
    if reason is None and not value["evidence"]:
      reason = "missing_evidence"
    if (
      reason is None
      and not _evidence_resolves(
        value["evidence"],
        material_set,
      )
    ):
      reason = "unresolved_evidence"
    if (
      reason is None
      and (
        value["identifier"] in value["dependencies"]
        or not set(value["dependencies"]) <= identifier_set
      )
    ):
      reason = "unresolved_dependency"

    if reason is not None:
      rejected.append(RejectedCandidate(
        identifier=value["identifier"],
        reason=reason,
      ))
      continue
    accepted.append(ExtractedEssence(
      identifier=value["identifier"],
      statement=value["statement"],
      axis=axis,
      evidence=value["evidence"],
      dependencies=value["dependencies"],
    ))

  found_axes = {item.axis.value for item in accepted}
  missing_axes = tuple(
    axis
    for axis in AXIS_ORDER
    if axis not in found_axes
  )
  document = {
    "accepted": [
      {
        "axis": item.axis.value,
        "dependencies": list(item.dependencies),
        "evidence": list(item.evidence),
        "identifier": item.identifier,
        "statement": item.statement,
      }
      for item in accepted
    ],
    "missing_axes": list(missing_axes),
    "rejected": [
      dataclasses.asdict(item)
      for item in rejected
    ],
    "schema_version": 1,
    "source_materials": sorted(materials),
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return InitialExtraction(
    status=(
      "blocked"
      if rejected or missing_axes
      else "complete"
    ),
    accepted=tuple(accepted),
    rejected=tuple(rejected),
    missing_axes=missing_axes,
    digest=digest,
  )
