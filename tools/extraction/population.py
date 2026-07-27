"""第2段の抽出母集団分類。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import enum
import hashlib
import json


class PopulationClassificationError(Exception):
  """抽出母集団を安全に分類できない。"""


class PopulationDisposition(enum.Enum):
  INCLUDE = "include"
  EXCLUDE = "exclude"
  DEFER = "defer"


@dataclasses.dataclass(frozen=True)
class PopulationDecision:
  identifier: str
  disposition: PopulationDisposition
  rationale: str


@dataclasses.dataclass(frozen=True)
class PopulationClassification:
  status: str
  included: tuple
  excluded: tuple
  deferred: tuple
  unknown: tuple
  digest: str


def _valid_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _parse_decision(value):
  if (
    not isinstance(value, dict)
    or set(value) != {
      "identifier",
      "disposition",
      "rationale",
    }
    or not _valid_text(value["identifier"])
    or not _valid_text(value["rationale"])
  ):
    raise PopulationClassificationError(
      "Population decisions require fixed non-empty fields"
    )
  try:
    disposition = PopulationDisposition(
      value["disposition"]
    )
  except (TypeError, ValueError) as error:
    raise PopulationClassificationError(
      "Unknown population disposition"
    ) from error
  return PopulationDecision(
    value["identifier"],
    disposition,
    value["rationale"],
  )


def classify_extraction_population(
  source_universe,
  decisions,
) -> PopulationClassification:
  universe = tuple(source_universe)
  if (
    len(set(universe)) != len(universe)
    or any(
      not _valid_text(identifier)
      for identifier in universe
    )
  ):
    raise PopulationClassificationError(
      "Source universe identifiers must be unique strings"
    )
  decision_values = tuple(
    _parse_decision(value)
    for value in decisions
  )
  decision_identifiers = tuple(
    decision.identifier
    for decision in decision_values
  )
  if (
    len(set(decision_identifiers))
    != len(decision_identifiers)
    or not set(decision_identifiers) <= set(universe)
  ):
    raise PopulationClassificationError(
      "Population decisions must be unique and inside the universe"
    )
  by_identifier = {
    decision.identifier: decision
    for decision in decision_values
  }
  partitions = {
    disposition: tuple(sorted(
      identifier
      for identifier, decision in by_identifier.items()
      if decision.disposition == disposition
    ))
    for disposition in PopulationDisposition
  }
  unknown = tuple(sorted(
    set(universe) - set(by_identifier)
  ))
  document = {
    "decisions": [
      {
        "disposition": (
          by_identifier[identifier].disposition.value
          if identifier in by_identifier
          else "unknown"
        ),
        "identifier": identifier,
        "rationale": (
          by_identifier[identifier].rationale
          if identifier in by_identifier
          else None
        ),
      }
      for identifier in sorted(universe)
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
  return PopulationClassification(
    status="blocked" if unknown else "complete",
    included=partitions[PopulationDisposition.INCLUDE],
    excluded=partitions[PopulationDisposition.EXCLUDE],
    deferred=partitions[PopulationDisposition.DEFER],
    unknown=unknown,
    digest=digest,
  )


def include_entire_population(
  source_universe,
) -> PopulationClassification:
  universe = tuple(source_universe)
  return classify_extraction_population(
    universe,
    (
      {
        "identifier": identifier,
        "disposition": "include",
        "rationale": "fixed_commit_regular_blob",
      }
      for identifier in universe
    ),
  )
