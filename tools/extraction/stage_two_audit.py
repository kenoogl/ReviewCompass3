"""第2段の被覆・未解決関門監査。"""

import dataclasses
import hashlib
import json


@dataclasses.dataclass(frozen=True)
class StageTwoAudit:
  status: str
  uncovered: tuple
  unresolved_count: int
  approval_candidate: object
  digest: str


def audit_stage_two(
  *,
  population,
  extracted,
  not_selected,
  unresolved_dependencies,
  reassessment_conflicts,
  unclassified_items,
  missing_destinations,
  unreasoned_rejections,
  follow_up_items,
  user_approved,
):
  universe = tuple(population)
  extracted_values = tuple(extracted)
  not_selected_values = tuple(not_selected)
  if (
    len(set(universe)) != len(universe)
    or set(extracted_values) & set(not_selected_values)
    or not (
      set(extracted_values) | set(not_selected_values)
    ) <= set(universe)
  ):
    raise ValueError("stage two coverage sets are inconsistent")
  counts = (
    unresolved_dependencies,
    reassessment_conflicts,
    unclassified_items,
    missing_destinations,
    unreasoned_rejections,
    follow_up_items,
  )
  if any(not isinstance(value, int) or value < 0 for value in counts):
    raise ValueError("audit counts must be non-negative")
  uncovered = tuple(sorted(
    set(universe)
    - set(extracted_values)
    - set(not_selected_values)
  ))
  unresolved_count = len(uncovered) + sum(counts)
  document = {
    "counts": {
      "follow_up_items": follow_up_items,
      "missing_destinations": missing_destinations,
      "reassessment_conflicts": reassessment_conflicts,
      "unclassified_items": unclassified_items,
      "unreasoned_rejections": unreasoned_rejections,
      "unresolved_dependencies": unresolved_dependencies,
    },
    "covered_count": (
      len(extracted_values) + len(not_selected_values)
    ),
    "population_count": len(universe),
    "schema_version": 1,
    "uncovered": list(uncovered),
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  if unresolved_count:
    status = "blocked"
    candidate = None
  elif user_approved is True:
    status = "ready"
    candidate = None
  else:
    status = "awaiting_user_approval"
    candidate = {
      "approved": False,
      "audit_digest": digest,
    }
  return StageTwoAudit(
    status=status,
    uncovered=uncovered,
    unresolved_count=unresolved_count,
    approval_candidate=candidate,
    digest=digest,
  )
