"""ブートストラップreviewの独立変異・障害注入検査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import tempfile

from tools.bootstrap.closed_payload import ClosedPayload
from tools.bootstrap.raw_review_store import (
  RawReviewStoreError,
  store_raw_executions,
)
from tools.bootstrap.review_contract import (
  ContractedReviewPayload,
  ReviewContractError,
  materialize_review_contract,
)
from tools.bootstrap.review_execution import (
  ReviewAssignment,
  ReviewExecution,
  execute_review_assignments,
)
from tools.bootstrap.review_response_parser import (
  ParsedReview,
  ReviewResponseParseError,
  parse_raw_review_record,
)
from tools.bootstrap.review_resume import resume_review_assignments
from tools.bootstrap.review_triage import (
  ReviewTriageError,
  triage_parsed_reviews,
)


@dataclasses.dataclass(frozen=True)
class AssuranceCheck:
  name: str
  status: str


@dataclasses.dataclass(frozen=True)
class ReviewAssuranceReport:
  status: str
  checks: tuple
  passed_count: int
  failed_count: int


def _contracted_payload():
  content = '{"contract":"fixed"}'
  return ContractedReviewPayload(
    content,
    hashlib.sha256(content.encode("utf-8")).hexdigest(),
    "c" * 64,
    "bootstrap-review-v1",
    1,
    "s" * 64,
  )


def _assignments():
  return (
    ReviewAssignment("main", "fixture", "main-model", "main"),
    ReviewAssignment(
      "independent",
      "fixture",
      "independent-model",
      "independent",
    ),
  )


def _digest_mutation():
  payload = ClosedPayload("{}", "0" * 64, "b" * 64, "t" * 64, ())
  try:
    materialize_review_contract(payload)
  except ReviewContractError:
    return True
  return False


def _schema_mutation():
  execution = ReviewExecution(
    _assignments()[0],
    "succeeded",
    "{}",
    None,
    "p" * 64,
  )
  with tempfile.TemporaryDirectory() as root:
    record = store_raw_executions(
      root,
      "attempt-001",
      (execution,),
    )[0]
    try:
      parse_raw_review_record(root, record)
    except ReviewResponseParseError:
      return True
  return False


def _missing_route():
  review = ParsedReview(
    "main",
    "main",
    "p" * 64,
    "r" * 64,
    (),
    "",
    "d" * 64,
  )
  try:
    triage_parsed_reviews((review,))
  except ReviewTriageError:
    return True
  return False


def _immutable_raw_store():
  execution = ReviewExecution(
    _assignments()[0],
    "succeeded",
    "{}",
    None,
    "p" * 64,
  )
  with tempfile.TemporaryDirectory() as root:
    store_raw_executions(root, "attempt-001", (execution,))
    try:
      store_raw_executions(root, "attempt-001", (execution,))
    except RawReviewStoreError:
      return True
  return False


def _provider_partial_failure():
  executions = execute_review_assignments(
    _contracted_payload(),
    _assignments(),
    runner=lambda assignment, _content: (
      "{}"
      if assignment.route == "main"
      else (_ for _ in ()).throw(RuntimeError("failure"))
    ),
  )
  return {
    execution.status
    for execution in executions
  } == {"succeeded", "failed"}


def _resume_preserves_success():
  payload = _contracted_payload()
  assignments = _assignments()
  initial = (
    ReviewExecution(
      assignments[0],
      "succeeded",
      "{}",
      None,
      payload.digest,
    ),
    ReviewExecution(
      assignments[1],
      "failed",
      None,
      "failure",
      payload.digest,
    ),
  )
  with tempfile.TemporaryDirectory() as root:
    records = store_raw_executions(
      root,
      "attempt-001",
      initial,
    )
    resumed = resume_review_assignments(
      payload,
      assignments,
      records,
      runner=lambda _assignment, _content: "{}",
    )
  return (
    tuple(
      record.assignment_name
      for record in resumed.completed_records
    ) == ("main",)
    and tuple(
      execution.assignment.name
      for execution in resumed.new_executions
    ) == ("independent",)
  )


_CHECKS = (
  ("digest_mutation", _digest_mutation),
  ("schema_mutation", _schema_mutation),
  ("missing_route", _missing_route),
  ("immutable_raw_store", _immutable_raw_store),
  ("provider_partial_failure", _provider_partial_failure),
  ("resume_preserves_success", _resume_preserves_success),
)


def run_bootstrap_review_assurance(
  *,
  overrides=None,
) -> ReviewAssuranceReport:
  override_values = {} if overrides is None else dict(overrides)
  checks = []
  for name, default_check in _CHECKS:
    check = override_values.get(name, default_check)
    try:
      detected = check() is True
    except Exception:
      detected = False
    checks.append(AssuranceCheck(
      name,
      "detected" if detected else "missed",
    ))
  passed_count = sum(
    check.status == "detected"
    for check in checks
  )
  failed_count = len(checks) - passed_count
  return ReviewAssuranceReport(
    "passed" if failed_count == 0 else "failed",
    tuple(checks),
    passed_count,
    failed_count,
  )
