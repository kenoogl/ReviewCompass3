"""第2段のエッセンス台帳schema。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import enum
import hashlib
import json
import re


class EssenceLedgerError(Exception):
  """エッセンス台帳を安全に確定できない。"""


class EssenceKind(enum.Enum):
  USER_DECISION = "user_decision"
  CAPABILITY = "capability"
  PROCEDURE = "procedure"
  INVARIANT = "invariant"
  CONTRACT = "contract"
  RECOVERY = "recovery"
  EMPIRICAL_FINDING = "empirical_finding"


class EssenceDisposition(enum.Enum):
  TRANSFER = "transfer"
  REDESIGN = "redesign"
  REJECT = "reject"
  FOLLOW_UP = "follow_up"


@dataclasses.dataclass(frozen=True)
class EssenceItem:
  identifier: str
  statement: str
  kind: EssenceKind
  evidence: tuple
  related_tests: tuple
  dependencies: tuple
  disposition: EssenceDisposition
  rationale: str
  destination: object


@dataclasses.dataclass(frozen=True)
class EssenceLedger:
  status: str
  items: tuple
  digest: str


_IDENTIFIER_PATTERN = re.compile(r"ESS-[0-9]{4,}")
_FIELDS = {
  "identifier",
  "statement",
  "kind",
  "evidence",
  "related_tests",
  "dependencies",
  "disposition",
  "rationale",
  "destination",
}


def _valid_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _parse_text_tuple(value, *, required):
  if (
    not isinstance(value, (list, tuple))
    or (required and not value)
    or len(set(value)) != len(value)
    or any(not _valid_text(item) for item in value)
  ):
    raise EssenceLedgerError(
      "Ledger references must be unique text values"
    )
  return tuple(sorted(value))


def _parse_item(value):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or not _valid_text(value["identifier"])
    or _IDENTIFIER_PATTERN.fullmatch(
      value["identifier"]
    ) is None
    or not _valid_text(value["statement"])
    or not _valid_text(value["rationale"])
  ):
    raise EssenceLedgerError(
      "Ledger items require fixed non-empty fields"
    )
  try:
    kind = EssenceKind(value["kind"])
    disposition = EssenceDisposition(
      value["disposition"]
    )
  except (TypeError, ValueError) as error:
    raise EssenceLedgerError(
      "Ledger item uses an unknown enum value"
    ) from error

  destination = value["destination"]
  if (
    disposition == EssenceDisposition.REJECT
    and destination is not None
  ) or (
    disposition != EssenceDisposition.REJECT
    and not _valid_text(destination)
  ):
    raise EssenceLedgerError(
      "Disposition and destination are inconsistent"
    )

  return EssenceItem(
    identifier=value["identifier"],
    statement=value["statement"],
    kind=kind,
    evidence=_parse_text_tuple(
      value["evidence"],
      required=True,
    ),
    related_tests=_parse_text_tuple(
      value["related_tests"],
      required=False,
    ),
    dependencies=_parse_text_tuple(
      value["dependencies"],
      required=False,
    ),
    disposition=disposition,
    rationale=value["rationale"],
    destination=destination,
  )


def build_essence_ledger(records) -> EssenceLedger:
  items = tuple(_parse_item(record) for record in records)
  identifiers = tuple(item.identifier for item in items)
  if (
    not items
    or len(set(identifiers)) != len(identifiers)
  ):
    raise EssenceLedgerError(
      "Ledger identifiers must be unique"
    )
  identifier_set = set(identifiers)
  if any(
    item.identifier in item.dependencies
    or not set(item.dependencies) <= identifier_set
    for item in items
  ):
    raise EssenceLedgerError(
      "Ledger dependencies must resolve without self-reference"
    )

  ordered = tuple(sorted(
    items,
    key=lambda item: item.identifier,
  ))
  document = {
    "items": [
      {
        "dependencies": list(item.dependencies),
        "destination": item.destination,
        "disposition": item.disposition.value,
        "evidence": list(item.evidence),
        "identifier": item.identifier,
        "kind": item.kind.value,
        "rationale": item.rationale,
        "related_tests": list(item.related_tests),
        "statement": item.statement,
      }
      for item in ordered
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
  return EssenceLedger(
    status="complete",
    items=ordered,
    digest=digest,
  )
