"""レビュー中断再開と成功成果の温存。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib

from tools.bootstrap.raw_review_store import RawReviewRecord
from tools.bootstrap.review_contract import ContractedReviewPayload
from tools.bootstrap.review_execution import (
  ReviewAssignment,
  ReviewExecution,
)


class ReviewResumeError(Exception):
  """レビュー履歴から安全に再開できない。"""


@dataclasses.dataclass(frozen=True)
class ReviewResume:
  completed_records: tuple
  failed_history: tuple
  new_executions: tuple


def resume_review_assignments(
  contracted_payload,
  assignments,
  records,
  *,
  runner,
) -> ReviewResume:
  if (
    not isinstance(contracted_payload, ContractedReviewPayload)
    or hashlib.sha256(
      contracted_payload.content.encode("utf-8")
    ).hexdigest() != contracted_payload.digest
  ):
    raise ReviewResumeError(
      "Resume requires an intact contracted payload"
    )
  assignment_values = tuple(assignments)
  if (
    any(
      not isinstance(assignment, ReviewAssignment)
      for assignment in assignment_values
    )
    or len({
      assignment.name
      for assignment in assignment_values
    }) != len(assignment_values)
    or {
      assignment.route
      for assignment in assignment_values
    } != {"main", "independent"}
  ):
    raise ReviewResumeError(
      "Resume requires unique assignments on both routes"
    )
  record_values = tuple(records)
  if any(
    not isinstance(record, RawReviewRecord)
    or record.contracted_payload_digest
    != contracted_payload.digest
    for record in record_values
  ):
    raise ReviewResumeError(
      "Resume history must belong to one contracted payload"
    )
  known_names = {
    assignment.name
    for assignment in assignment_values
  }
  if any(
    record.assignment_name not in known_names
    for record in record_values
  ):
    raise ReviewResumeError(
      "Resume history contains an unknown assignment"
    )

  completed_records = tuple(sorted(
    (
      record
      for record in record_values
      if record.status == "succeeded"
    ),
    key=lambda record: (
      record.assignment_name,
      record.relative_path,
    ),
  ))
  completed_names = {
    record.assignment_name
    for record in completed_records
  }
  failed_history = tuple(sorted(
    (
      record
      for record in record_values
      if record.status == "failed"
    ),
    key=lambda record: (
      record.assignment_name,
      record.relative_path,
    ),
  ))
  new_executions = []
  for assignment in sorted(
    assignment_values,
    key=lambda value: value.name,
  ):
    if assignment.name in completed_names:
      continue
    try:
      response = runner(
        assignment,
        contracted_payload.content,
      )
      if not isinstance(response, str):
        raise TypeError("provider response must be text")
      execution = ReviewExecution(
        assignment,
        "succeeded",
        response,
        None,
        contracted_payload.digest,
      )
    except Exception as error:
      execution = ReviewExecution(
        assignment,
        "failed",
        None,
        str(error),
        contracted_payload.digest,
      )
    new_executions.append(execution)
  return ReviewResume(
    completed_records=completed_records,
    failed_history=failed_history,
    new_executions=tuple(new_executions),
  )
