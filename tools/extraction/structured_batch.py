"""構造化材料batchの完全解決。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


class StructuredBatchError(Exception):
  """構造化材料batchを完全かつ一意に解決できない。"""


@dataclasses.dataclass(frozen=True)
class StructuredBatchResolution:
  status: str
  extracted: tuple
  merged: tuple
  not_selected: tuple
  digest: str


ALLOWED_KINDS = frozenset({
  "schema",
  "canonical_spec",
  "state",
  "approval",
  "raw_response",
  "generated_evidence",
})


def resolve_structured_batch(
  candidates,
  classifications,
  resolutions,
):
  candidate_values = tuple(candidates)
  if (
    not candidate_values
    or len(set(candidate_values)) != len(candidate_values)
    or not isinstance(classifications, dict)
    or set(classifications) != set(candidate_values)
    or any(
      kind not in ALLOWED_KINDS
      for kind in classifications.values()
    )
  ):
    raise StructuredBatchError(
      "batch candidates require complete semantic classifications"
    )
  values = tuple(resolutions)
  resolution_candidates = [
    value.get("candidate")
    for value in values
    if isinstance(value, dict)
  ]
  if (
    len(resolution_candidates) != len(values)
    or len(set(resolution_candidates))
    != len(resolution_candidates)
    or set(resolution_candidates) != set(candidate_values)
  ):
    raise StructuredBatchError(
      "resolutions must cover every batch candidate"
    )
  extracted = []
  merged = []
  not_selected = []
  normalized = []
  for value in values:
    if (
      set(value)
      != {"candidate", "action", "essence_id", "rationale"}
      or value["action"]
      not in {"extract", "merge", "not_selected"}
      or not isinstance(value["rationale"], str)
      or not value["rationale"].strip()
    ):
      raise StructuredBatchError(
        "resolution requires fixed reasoned fields"
      )
    target = value["essence_id"]
    if value["action"] in {"extract", "merge"}:
      if not isinstance(target, str) or not target:
        raise StructuredBatchError(
          "extract and merge require essence target"
        )
      pair = (value["candidate"], target)
      if value["action"] == "extract":
        extracted.append(pair)
      else:
        merged.append(pair)
    else:
      if target is not None:
        raise StructuredBatchError(
          "not-selected candidate cannot have essence target"
        )
      not_selected.append(value["candidate"])
    normalized.append({
      **value,
      "semantic_kind": classifications[value["candidate"]],
    })
  extracted_ids = [target for _, target in extracted]
  if len(set(extracted_ids)) != len(extracted_ids):
    raise StructuredBatchError(
      "new essence identifiers must be unique"
    )
  document = {
    "classifications": dict(sorted(classifications.items())),
    "resolutions": sorted(
      normalized,
      key=lambda value: value["candidate"],
    ),
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return StructuredBatchResolution(
    status="complete",
    extracted=tuple(sorted(extracted)),
    merged=tuple(sorted(merged)),
    not_selected=tuple(sorted(not_selected)),
    digest=digest,
  )
