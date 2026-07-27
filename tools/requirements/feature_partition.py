"""第4段の機能分割とエッセンス被覆契約。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re


class FeaturePartitionError(Exception):
  """機能分割を安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class Feature:
  feature_id: str
  name: str
  responsibility: str
  intent_refs: tuple
  essence_ids: tuple
  non_goals: tuple


@dataclasses.dataclass(frozen=True)
class FeaturePartition:
  status: str
  features: tuple
  feature_count: int
  covered_essence_count: int
  uncovered_essence_ids: tuple
  duplicate_essence_ids: tuple
  digest: str


_FIELDS = {
  "feature_id",
  "name",
  "responsibility",
  "intent_refs",
  "essence_ids",
  "non_goals",
}
_FEATURE_ID = re.compile(
  r"FEAT-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_INTENT_ID = re.compile(
  r"INT-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_ESSENCE_ID = re.compile(r"ESS-[0-9]{4,}")


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
    not result
    or len(set(result)) != len(result)
    or any(
      not _text(value)
      or pattern.fullmatch(value) is None
      for value in result
    )
  ):
    raise FeaturePartitionError(
      f"{label} definitions must be unique valid IDs"
    )
  return frozenset(result)


def _references(value, *, defined, pattern, label):
  if not isinstance(value, (list, tuple)):
    raise FeaturePartitionError(
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
    raise FeaturePartitionError(
      f"{label} references must be unique and resolve"
    )
  return tuple(sorted(result))


def _texts(value, label):
  if not isinstance(value, (list, tuple)):
    raise FeaturePartitionError(
      f"{label} must be a sequence"
    )
  result = tuple(value)
  if (
    not result
    or len(set(result)) != len(result)
    or any(not _text(item) for item in result)
  ):
    raise FeaturePartitionError(
      f"{label} must contain unique non-empty text"
    )
  return tuple(sorted(result))


def _feature(value, *, intent_ids, essence_ids):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or not _text(value["feature_id"])
    or _FEATURE_ID.fullmatch(value["feature_id"]) is None
    or not _text(value["name"])
    or not _text(value["responsibility"])
  ):
    raise FeaturePartitionError(
      "features require fixed non-empty fields"
    )
  return Feature(
    feature_id=value["feature_id"],
    name=value["name"],
    responsibility=value["responsibility"],
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
    non_goals=_texts(value["non_goals"], "non-goals"),
  )


def validate_feature_partition(
  *,
  features,
  defined_intent_ids,
  defined_essence_ids,
):
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
  parsed = tuple(
    _feature(
      value,
      intent_ids=intent_ids,
      essence_ids=essence_ids,
    )
    for value in features
  )
  if not parsed:
    raise FeaturePartitionError(
      "feature partition must not be empty"
    )
  feature_ids = tuple(
    feature.feature_id for feature in parsed
  )
  if len(set(feature_ids)) != len(feature_ids):
    raise FeaturePartitionError(
      "feature IDs must be unique"
    )
  allocations = [
    essence_id
    for feature in parsed
    for essence_id in feature.essence_ids
  ]
  allocation_set = set(allocations)
  duplicates = tuple(sorted({
    essence_id for essence_id in allocations
    if allocations.count(essence_id) > 1
  }))
  uncovered = tuple(sorted(
    essence_ids - allocation_set
  ))
  if duplicates or uncovered or allocation_set != essence_ids:
    raise FeaturePartitionError(
      "every essence requires exactly one feature destination"
    )
  ordered = tuple(sorted(
    parsed,
    key=lambda feature: feature.feature_id,
  ))
  document = {
    "features": [
      {
        "essence_ids": list(feature.essence_ids),
        "feature_id": feature.feature_id,
        "intent_refs": list(feature.intent_refs),
        "name": feature.name,
        "non_goals": list(feature.non_goals),
        "responsibility": feature.responsibility,
      }
      for feature in ordered
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
  return FeaturePartition(
    status="complete",
    features=ordered,
    feature_count=len(ordered),
    covered_essence_count=len(allocation_set),
    uncovered_essence_ids=(),
    duplicate_essence_ids=(),
    digest=digest,
  )
