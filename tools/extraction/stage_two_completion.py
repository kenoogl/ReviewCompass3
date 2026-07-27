"""第2段の残存母集団を一括で閉じる完了関門。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import re

from tools.extraction.batch_reassessment import (
  BatchReassessmentError,
  reconcile_batch_reassessments,
)
from tools.extraction.stage_two_audit import audit_stage_two


class StageTwoCompletionError(Exception):
  """第2段の全件判断を安全に完了できない。"""


@dataclasses.dataclass(frozen=True)
class StageTwoCompletion:
  status: str
  covered_count: int
  uncovered_count: int
  unresolved_count: int
  extracted_count: int
  merged_count: int
  not_selected_count: int
  conflict_count: int
  approval_candidate: object
  reassessment_digest: str
  audit_digest: str


_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")


def _texts(values):
  result = tuple(values)
  if (
    len(set(result)) != len(result)
    or any(
      not isinstance(value, str) or not value
      for value in result
    )
  ):
    raise StageTwoCompletionError(
      "completion identifiers must be unique text"
    )
  return result


def complete_stage_two(
  *,
  population,
  prior_covered,
  material_digest,
  assessments,
  existing_essence_ids,
  new_essence_ids,
  follow_up_ids,
  user_approved,
):
  universe = _texts(population)
  prior = _texts(prior_covered)
  existing = _texts(existing_essence_ids)
  new = _texts(new_essence_ids)
  follow_ups = _texts(follow_up_ids)
  if (
    not set(prior) <= set(universe)
    or set(existing) & set(new)
    or _DIGEST_PATTERN.fullmatch(material_digest) is None
  ):
    raise StageTwoCompletionError(
      "completion inputs must bind a fixed remaining population"
    )
  remaining = tuple(sorted(set(universe) - set(prior)))
  if not remaining:
    raise StageTwoCompletionError(
      "completion requires a remaining population"
    )
  assessment_values = tuple(assessments)
  try:
    reassessment = reconcile_batch_reassessments(
      material_digest,
      remaining,
      assessment_values,
    )
  except BatchReassessmentError as error:
    raise StageTwoCompletionError(str(error)) from error
  main = next(
    value for value in assessment_values
    if value.get("path") == "main"
  )
  decisions = tuple(main["decisions"])
  allowed_targets = set(existing) | set(new)
  extracted = []
  merged = []
  not_selected = []
  for decision in decisions:
    action = decision["action"]
    target = decision["essence_id"]
    if action == "extract":
      if target not in set(new):
        raise StageTwoCompletionError(
          "extract decisions require declared new essence IDs"
        )
      extracted.append((decision["candidate"], target))
    elif action == "merge":
      if target not in allowed_targets:
        raise StageTwoCompletionError(
          "merge decisions require known essence IDs"
        )
      merged.append((decision["candidate"], target))
    else:
      not_selected.append(decision["candidate"])
  extracted_targets = tuple(
    target for _, target in extracted
  )
  if (
    len(set(extracted_targets)) != len(extracted_targets)
    or set(extracted_targets) != set(new)
  ):
    raise StageTwoCompletionError(
      "every new essence ID requires exactly one extraction"
    )
  selected = tuple(
    candidate for candidate, _ in extracted + merged
  )
  audit = audit_stage_two(
    population=universe,
    extracted=prior + selected,
    not_selected=tuple(not_selected),
    unresolved_dependencies=0,
    reassessment_conflicts=len(reassessment.conflicts),
    unclassified_items=0,
    missing_destinations=0,
    unreasoned_rejections=0,
    follow_up_items=len(follow_ups),
    user_approved=user_approved,
  )
  return StageTwoCompletion(
    status=audit.status,
    covered_count=len(universe) - len(audit.uncovered),
    uncovered_count=len(audit.uncovered),
    unresolved_count=audit.unresolved_count,
    extracted_count=len(extracted),
    merged_count=len(merged),
    not_selected_count=len(not_selected),
    conflict_count=len(reassessment.conflicts),
    approval_candidate=audit.approval_candidate,
    reassessment_digest=reassessment.digest,
    audit_digest=audit.digest,
  )
