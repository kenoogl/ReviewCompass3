"""独立抽出候補の決定的統合。"""

import dataclasses
import hashlib
import json

from .seven_axes import AXIS_ORDER


class CandidateIntegrationError(Exception):
  """候補の統合判断が完全・一意でない。"""


@dataclasses.dataclass(frozen=True)
class CandidateIntegration:
  status: str
  added: tuple
  merged: tuple
  deferred: tuple
  digest: str


def _text(value):
  return isinstance(value, str) and bool(value) and "\n" not in value


def integrate_candidates(
  *,
  existing_items,
  candidates,
  resolutions,
):
  existing = tuple(existing_items)
  candidate_values = tuple(candidates)
  resolution_values = tuple(resolutions)
  if any(
    not isinstance(item, dict)
    or set(item) != {"identifier", "evidence"}
    or not _text(item["identifier"])
    or not item["evidence"]
    for item in existing
  ) or any(
    not isinstance(item, dict)
    or set(item) != {
      "candidate_id", "statement", "axis", "evidence",
    }
    or not _text(item["candidate_id"])
    or not _text(item["statement"])
    or item["axis"] not in AXIS_ORDER
    or not item["evidence"]
    for item in candidate_values
  ):
    raise CandidateIntegrationError("invalid candidate input")
  existing_ids = tuple(item["identifier"] for item in existing)
  candidate_ids = tuple(item["candidate_id"] for item in candidate_values)
  if (
    len(set(existing_ids)) != len(existing_ids)
    or len(set(candidate_ids)) != len(candidate_ids)
  ):
    raise CandidateIntegrationError("candidate identifiers must be unique")
  if any(
    not isinstance(value, dict)
    or set(value) != {
      "candidate_id", "action", "target", "rationale",
    }
    or value["action"] not in {"add", "merge", "defer"}
    or not _text(value["rationale"])
    for value in resolution_values
  ):
    raise CandidateIntegrationError("invalid candidate resolution")
  resolved_ids = tuple(value["candidate_id"] for value in resolution_values)
  if (
    len(set(resolved_ids)) != len(resolved_ids)
    or set(resolved_ids) != set(candidate_ids)
  ):
    raise CandidateIntegrationError("every candidate requires one resolution")
  added = []
  merged = []
  deferred = []
  added_targets = set()
  existing_set = set(existing_ids)
  for value in sorted(
    resolution_values,
    key=lambda item: item["candidate_id"],
  ):
    action = value["action"]
    target = value["target"]
    if action == "merge":
      if target not in existing_set:
        raise CandidateIntegrationError("merge target does not exist")
      merged.append((value["candidate_id"], target))
    elif action == "add":
      if (
        not _text(target)
        or target in existing_set
        or target in added_targets
      ):
        raise CandidateIntegrationError("add target must be new")
      added_targets.add(target)
      added.append((value["candidate_id"], target))
    else:
      if target is not None:
        raise CandidateIntegrationError("defer cannot have a target")
      deferred.append((value["candidate_id"], value["rationale"]))
  document = {
    "added": added,
    "deferred": deferred,
    "merged": merged,
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return CandidateIntegration(
    status="complete",
    added=tuple(added),
    merged=tuple(merged),
    deferred=tuple(deferred),
    digest=digest,
  )
