"""第2段の抽出項目判断・受け先分類。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import enum
import hashlib
import json


class DestinationClassificationError(Exception):
  """抽出項目の判断と受け先を安全に分類できない。"""


class DestinationDisposition(enum.Enum):
  TRANSFER = "transfer"
  REDESIGN = "redesign"
  REJECT = "reject"
  FOLLOW_UP = "follow_up"


@dataclasses.dataclass(frozen=True)
class DestinationDecision:
  identifier: str
  disposition: DestinationDisposition
  rationale: str
  destination: object


@dataclasses.dataclass(frozen=True)
class DestinationClassification:
  status: str
  transferred: tuple
  redesigned: tuple
  rejected: tuple
  follow_up: tuple
  unclassified: tuple
  decisions: tuple
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
      "destination",
    }
    or not _valid_text(value["identifier"])
    or not _valid_text(value["rationale"])
  ):
    raise DestinationClassificationError(
      "Destination decisions require fixed reasoned fields"
    )
  try:
    disposition = DestinationDisposition(
      value["disposition"]
    )
  except (TypeError, ValueError) as error:
    raise DestinationClassificationError(
      "Unknown destination disposition"
    ) from error
  destination = value["destination"]
  if (
    disposition == DestinationDisposition.REJECT
    and destination is not None
  ) or (
    disposition != DestinationDisposition.REJECT
    and not _valid_text(destination)
  ):
    raise DestinationClassificationError(
      "Destination is inconsistent with disposition"
    )
  return DestinationDecision(
    identifier=value["identifier"],
    disposition=disposition,
    rationale=value["rationale"],
    destination=destination,
  )


def classify_destinations(
  item_ids,
  decisions,
) -> DestinationClassification:
  identifiers = tuple(item_ids)
  if (
    not identifiers
    or len(set(identifiers)) != len(identifiers)
    or any(not _valid_text(identifier) for identifier in identifiers)
  ):
    raise DestinationClassificationError(
      "Extracted item identifiers must be unique"
    )
  decision_values = tuple(
    _parse_decision(value)
    for value in decisions
  )
  decision_ids = tuple(
    decision.identifier
    for decision in decision_values
  )
  if (
    len(set(decision_ids)) != len(decision_ids)
    or not set(decision_ids) <= set(identifiers)
  ):
    raise DestinationClassificationError(
      "Decisions must be unique and inside extracted items"
    )

  ordered = tuple(sorted(
    decision_values,
    key=lambda decision: decision.identifier,
  ))
  partitions = {
    disposition: tuple(
      decision.identifier
      for decision in ordered
      if decision.disposition == disposition
    )
    for disposition in DestinationDisposition
  }
  unclassified = tuple(sorted(
    set(identifiers) - set(decision_ids)
  ))
  document = {
    "decisions": [
      {
        "destination": decision.destination,
        "disposition": decision.disposition.value,
        "identifier": decision.identifier,
        "rationale": decision.rationale,
      }
      for decision in ordered
    ],
    "schema_version": 1,
    "unclassified": list(unclassified),
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return DestinationClassification(
    status="blocked" if unclassified else "complete",
    transferred=partitions[
      DestinationDisposition.TRANSFER
    ],
    redesigned=partitions[
      DestinationDisposition.REDESIGN
    ],
    rejected=partitions[
      DestinationDisposition.REJECT
    ],
    follow_up=partitions[
      DestinationDisposition.FOLLOW_UP
    ],
    unclassified=unclassified,
    decisions=ordered,
    digest=digest,
  )
