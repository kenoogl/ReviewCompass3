"""複数担当のレビュー実行境界。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import re

from tools.bootstrap.review_contract import ContractedReviewPayload


_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9._-]*")
_ROUTES = {"main", "independent"}


class ReviewExecutionError(Exception):
  """レビュー担当を安全に実行できない。"""


@dataclasses.dataclass(frozen=True)
class ReviewAssignment:
  name: str
  provider: str
  model: str
  route: str


@dataclasses.dataclass(frozen=True)
class ReviewExecution:
  assignment: ReviewAssignment
  status: str
  raw_response: object
  error: object
  contracted_payload_digest: str


def _valid_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _validate_assignment(assignment):
  if (
    not isinstance(assignment, ReviewAssignment)
    or _NAME_PATTERN.fullmatch(assignment.name or "") is None
    or not _valid_text(assignment.provider)
    or not _valid_text(assignment.model)
    or assignment.route not in _ROUTES
  ):
    raise ReviewExecutionError(
      "Invalid review assignment"
    )


def execute_review_assignments(
  contracted_payload,
  assignments,
  *,
  runner,
) -> tuple:
  if (
    not isinstance(contracted_payload, ContractedReviewPayload)
    or hashlib.sha256(
      contracted_payload.content.encode("utf-8")
    ).hexdigest() != contracted_payload.digest
  ):
    raise ReviewExecutionError(
      "Executions require an intact contracted payload"
    )
  assignment_values = tuple(assignments)
  for assignment in assignment_values:
    _validate_assignment(assignment)
  names = tuple(
    assignment.name
    for assignment in assignment_values
  )
  if (
    len(set(names)) != len(names)
    or {
      assignment.route
      for assignment in assignment_values
    } != _ROUTES
  ):
    raise ReviewExecutionError(
      "Assignments require unique names and both routes"
    )

  executions = []
  for assignment in sorted(
    assignment_values,
    key=lambda value: value.name,
  ):
    try:
      response = runner(
        assignment,
        contracted_payload.content,
      )
      if not isinstance(response, str):
        raise TypeError("provider response must be text")
      execution = ReviewExecution(
        assignment=assignment,
        status="succeeded",
        raw_response=response,
        error=None,
        contracted_payload_digest=contracted_payload.digest,
      )
    except Exception as error:
      execution = ReviewExecution(
        assignment=assignment,
        status="failed",
        raw_response=None,
        error=str(error),
        contracted_payload_digest=contracted_payload.digest,
      )
    executions.append(execution)
  return tuple(executions)
