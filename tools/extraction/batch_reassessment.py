"""構造化batch判断の独立再判定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re


_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")
_PATHS = frozenset({"main", "independent"})
_ACTIONS = frozenset({"extract", "merge", "not_selected"})


class BatchReassessmentError(Exception):
  """同一batch材料に基づく独立再判定を確定できない。"""


@dataclasses.dataclass(frozen=True)
class BatchReassessmentConflict:
  candidate: str
  main_action: str
  main_essence_id: object
  independent_action: str
  independent_essence_id: object


@dataclasses.dataclass(frozen=True)
class BatchReassessmentResult:
  status: str
  agreed: tuple
  conflicts: tuple
  digest: str


def _parse_decision(value):
  if (
    not isinstance(value, dict)
    or set(value)
    != {"candidate", "action", "essence_id", "rationale"}
    or not isinstance(value["candidate"], str)
    or not value["candidate"]
    or value["action"] not in _ACTIONS
    or not isinstance(value["rationale"], str)
    or not value["rationale"].strip()
  ):
    raise BatchReassessmentError(
      "batch decision requires fixed reasoned fields"
    )
  if value["action"] in {"extract", "merge"}:
    if (
      not isinstance(value["essence_id"], str)
      or not value["essence_id"]
    ):
      raise BatchReassessmentError(
        "extract and merge require essence target"
      )
  elif value["essence_id"] is not None:
    raise BatchReassessmentError(
      "not-selected decision cannot have essence target"
    )
  return dict(value)


def _parse_assessment(value, material_digest, candidates):
  if (
    not isinstance(value, dict)
    or set(value) != {
      "path",
      "material_digest",
      "raw_evidence",
      "decisions",
    }
    or value["path"] not in _PATHS
    or value["material_digest"] != material_digest
    or not isinstance(value["raw_evidence"], (list, tuple))
    or len(set(value["raw_evidence"]))
    != len(value["raw_evidence"])
    or set(value["raw_evidence"]) != set(candidates)
    or not isinstance(value["decisions"], (list, tuple))
  ):
    raise BatchReassessmentError(
      "assessment must bind all fixed batch materials"
    )
  decisions = tuple(
    _parse_decision(decision)
    for decision in value["decisions"]
  )
  identifiers = tuple(
    decision["candidate"] for decision in decisions
  )
  if (
    len(set(identifiers)) != len(identifiers)
    or set(identifiers) != set(candidates)
  ):
    raise BatchReassessmentError(
      "assessment decisions must cover every candidate"
    )
  return {
    "decisions": tuple(sorted(
      decisions,
      key=lambda decision: decision["candidate"],
    )),
    "material_digest": value["material_digest"],
    "path": value["path"],
    "raw_evidence": tuple(sorted(value["raw_evidence"])),
  }


def reconcile_batch_reassessments(
  material_digest,
  candidates,
  assessments,
):
  candidate_values = tuple(candidates)
  if (
    not isinstance(material_digest, str)
    or _DIGEST_PATTERN.fullmatch(material_digest) is None
    or not candidate_values
    or len(set(candidate_values)) != len(candidate_values)
    or any(
      not isinstance(candidate, str) or not candidate
      for candidate in candidate_values
    )
  ):
    raise BatchReassessmentError(
      "material digest and candidates must be fixed"
    )
  values = tuple(
    _parse_assessment(
      value,
      material_digest,
      candidate_values,
    )
    for value in assessments
  )
  if (
    len(values) != 2
    or {value["path"] for value in values} != _PATHS
  ):
    raise BatchReassessmentError(
      "exactly one main and independent assessment are required"
    )
  by_path = {value["path"]: value for value in values}
  main = {
    value["candidate"]: value
    for value in by_path["main"]["decisions"]
  }
  independent = {
    value["candidate"]: value
    for value in by_path["independent"]["decisions"]
  }
  agreed = []
  conflicts = []
  for candidate in sorted(candidate_values):
    main_value = main[candidate]
    independent_value = independent[candidate]
    main_pair = (
      main_value["action"],
      main_value["essence_id"],
    )
    independent_pair = (
      independent_value["action"],
      independent_value["essence_id"],
    )
    if main_pair == independent_pair:
      agreed.append((
        candidate,
        main_pair[0],
        main_pair[1],
      ))
    else:
      conflicts.append(BatchReassessmentConflict(
        candidate=candidate,
        main_action=main_pair[0],
        main_essence_id=main_pair[1],
        independent_action=independent_pair[0],
        independent_essence_id=independent_pair[1],
      ))
  document = {
    "agreed": [
      {
        "action": action,
        "candidate": candidate,
        "essence_id": essence_id,
      }
      for candidate, action, essence_id in agreed
    ],
    "assessments": [
      {
        **value,
        "decisions": list(value["decisions"]),
        "raw_evidence": list(value["raw_evidence"]),
      }
      for value in sorted(values, key=lambda item: item["path"])
    ],
    "conflicts": [
      dataclasses.asdict(conflict)
      for conflict in conflicts
    ],
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return BatchReassessmentResult(
    status="blocked" if conflicts else "complete",
    agreed=tuple(agreed),
    conflicts=tuple(conflicts),
    digest=digest,
  )
