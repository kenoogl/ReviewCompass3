"""第2段の増分被覆を合成する再監査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.extraction.stage_two_audit import audit_stage_two


@dataclasses.dataclass(frozen=True)
class StageTwoReaudit:
  status: str
  prior_covered_count: int
  newly_covered_count: int
  covered_count: int
  uncovered_count: int
  unresolved_count: int
  approval_candidate: object
  digest: str


def reaudit_stage_two(
  *,
  population,
  prior_extracted,
  prior_not_selected,
  batch_resolutions,
  unresolved_dependencies,
  reassessment_conflicts,
  unclassified_items,
  missing_destinations,
  unreasoned_rejections,
  follow_up_items,
  user_approved,
):
  population_values = tuple(population)
  prior_extracted_values = tuple(prior_extracted)
  prior_not_selected_values = tuple(prior_not_selected)
  prior = set(prior_extracted_values) | set(
    prior_not_selected_values
  )
  new_extracted = []
  new_not_selected = []
  for resolution in tuple(batch_resolutions):
    if (
      not isinstance(resolution, dict)
      or set(resolution) != {"extracted", "not_selected"}
    ):
      raise ValueError("batch resolution requires fixed fields")
    new_extracted.extend(resolution["extracted"])
    new_not_selected.extend(resolution["not_selected"])
  new_values = tuple(new_extracted + new_not_selected)
  if (
    len(set(new_values)) != len(new_values)
    or prior & set(new_values)
    or not set(new_values) <= set(population_values)
  ):
    raise ValueError(
      "new batch coverage must be unique, known, and incremental"
    )
  extracted = prior_extracted_values + tuple(new_extracted)
  not_selected = prior_not_selected_values + tuple(new_not_selected)
  audit = audit_stage_two(
    population=population_values,
    extracted=extracted,
    not_selected=not_selected,
    unresolved_dependencies=unresolved_dependencies,
    reassessment_conflicts=reassessment_conflicts,
    unclassified_items=unclassified_items,
    missing_destinations=missing_destinations,
    unreasoned_rejections=unreasoned_rejections,
    follow_up_items=follow_up_items,
    user_approved=user_approved,
  )
  return StageTwoReaudit(
    status=audit.status,
    prior_covered_count=len(prior),
    newly_covered_count=len(new_values),
    covered_count=len(extracted) + len(not_selected),
    uncovered_count=len(audit.uncovered),
    unresolved_count=audit.unresolved_count,
    approval_candidate=audit.approval_candidate,
    digest=audit.digest,
  )
