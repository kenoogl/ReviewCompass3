"""第2段の優先度付き抽出batch。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


class PriorityBatchError(Exception):
  """優先抽出batchを完全かつ一意に処理できない。"""


@dataclasses.dataclass(frozen=True)
class PriorityBatch:
  identifier: str
  layer: str
  candidates: tuple


@dataclasses.dataclass(frozen=True)
class PriorityBatchPlan:
  status: str
  batches: tuple
  scheduled_count: int
  unscheduled: tuple
  digest: str


@dataclasses.dataclass(frozen=True)
class PriorityBatchResolution:
  status: str
  extracted: tuple
  not_selected: tuple
  digest: str


LAYER_ORDER = (
  "dependency_materials",
  "structured_materials",
  "implementation",
  "tests",
  "specifications",
  "issues",
  "sessions",
  "empirical_records",
  "other",
)


def _path(identifier):
  if not isinstance(identifier, str) or identifier.count(":") != 1:
    raise PriorityBatchError("candidate must use source:path")
  source, path = identifier.split(":", 1)
  if not source or not path:
    raise PriorityBatchError("candidate must use source:path")
  return path


def _layer(identifier, dependencies):
  path = _path(identifier)
  if identifier in dependencies:
    return "dependency_materials"
  if (
    path.endswith((".yaml", ".yml", ".json"))
    and (
      "/specs/" in path
      or path.startswith("specs/")
    )
  ):
    return "structured_materials"
  if (
    path.startswith("docs/sessions/")
    or "/evidence/sessions/" in path
  ):
    return "sessions"
  if "/evidence/" in path:
    return "empirical_records"
  if (
    (path.startswith("tools/") or "/tools/" in path)
    and path.endswith(".py")
    and "/tests/" not in path
  ):
    return "implementation"
  if (
    path.startswith("tests/")
    or "/tests/" in path
    or path.rsplit("/", 1)[-1].startswith("test_")
  ):
    return "tests"
  if (
    path.startswith("specs/")
    or "/specs/" in path
    or path.startswith("docs/design/")
  ):
    return "specifications"
  if "/backlog/issues/" in path:
    return "issues"
  return "other"


def build_priority_batches(
  population,
  *,
  covered,
  dependency_materials,
  batch_size,
):
  values = tuple(population)
  covered_values = tuple(covered)
  dependency_values = tuple(dependency_materials)
  if (
    not values
    or len(set(values)) != len(values)
    or len(set(covered_values)) != len(covered_values)
    or len(set(dependency_values)) != len(dependency_values)
    or not set(covered_values) <= set(values)
    or not set(dependency_values) <= set(values)
    or not isinstance(batch_size, int)
    or batch_size <= 0
  ):
    raise PriorityBatchError("invalid priority batch inputs")
  for identifier in values:
    _path(identifier)
  remaining = set(values) - set(covered_values)
  dependencies = set(dependency_values) & remaining
  grouped = {layer: [] for layer in LAYER_ORDER}
  for identifier in sorted(remaining):
    grouped[_layer(identifier, dependencies)].append(identifier)
  batches = []
  for layer in LAYER_ORDER:
    candidates = grouped[layer]
    for offset in range(0, len(candidates), batch_size):
      batches.append(PriorityBatch(
        identifier=f"{layer}-{offset // batch_size + 1:04d}",
        layer=layer,
        candidates=tuple(candidates[offset:offset + batch_size]),
      ))
  scheduled = {
    candidate
    for batch in batches
    for candidate in batch.candidates
  }
  unscheduled = tuple(sorted(remaining - scheduled))
  document = {
    "batch_size": batch_size,
    "batches": [
      dataclasses.asdict(batch) for batch in batches
    ],
    "covered": sorted(covered_values),
    "schema_version": 1,
    "unscheduled": list(unscheduled),
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return PriorityBatchPlan(
    status="blocked" if unscheduled else "complete",
    batches=tuple(batches),
    scheduled_count=len(scheduled),
    unscheduled=unscheduled,
    digest=digest,
  )


def resolve_priority_batch(batch, resolutions):
  if (
    not isinstance(batch, PriorityBatch)
    or not batch.identifier
    or batch.layer not in LAYER_ORDER
    or not batch.candidates
    or len(set(batch.candidates)) != len(batch.candidates)
  ):
    raise PriorityBatchError("invalid priority batch")
  values = tuple(resolutions)
  candidates = [
    value.get("candidate")
    for value in values
    if isinstance(value, dict)
  ]
  if (
    len(candidates) != len(values)
    or len(set(candidates)) != len(candidates)
    or set(candidates) != set(batch.candidates)
  ):
    raise PriorityBatchError("batch resolutions must cover candidates")
  extracted = []
  not_selected = []
  normalized = []
  for value in values:
    if (
      set(value)
      != {"candidate", "action", "essence_id", "rationale"}
      or value["action"] not in {"extract", "not_selected"}
      or not isinstance(value["rationale"], str)
      or not value["rationale"].strip()
    ):
      raise PriorityBatchError("invalid batch resolution")
    if value["action"] == "extract":
      if not isinstance(value["essence_id"], str) or not value["essence_id"]:
        raise PriorityBatchError("extracted candidate requires essence ID")
      extracted.append((value["candidate"], value["essence_id"]))
    else:
      if value["essence_id"] is not None:
        raise PriorityBatchError(
          "not-selected candidate cannot have essence ID"
        )
      not_selected.append(value["candidate"])
    normalized.append(dict(value))
  document = {
    "batch": dataclasses.asdict(batch),
    "resolutions": sorted(
      normalized,
      key=lambda value: value["candidate"],
    ),
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return PriorityBatchResolution(
    status="complete",
    extracted=tuple(sorted(extracted)),
    not_selected=tuple(sorted(not_selected)),
    digest=digest,
  )
