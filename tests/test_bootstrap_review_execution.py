"""複数担当レビュー実行境界の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib

import pytest


def _contracted_payload(review_contract):
  content = '{"contract":"fixed"}'
  return review_contract.ContractedReviewPayload(
    content=content,
    digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    closed_payload_digest="c" * 64,
    prompt_version="bootstrap-review-v1",
    output_schema_version=1,
    output_schema_digest="s" * 64,
  )


def test_runs_distinct_roles_against_same_payload_and_preserves_successes():
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  payload = _contracted_payload(review_contract)
  assignments = (
    review_execution.ReviewAssignment(
      name="independent-b",
      provider="provider-b",
      model="model-b",
      route="independent",
    ),
    review_execution.ReviewAssignment(
      name="main",
      provider="provider-a",
      model="model-a",
      route="main",
    ),
    review_execution.ReviewAssignment(
      name="independent-a",
      provider="provider-c",
      model="model-c",
      route="independent",
    ),
  )
  received = []

  def runner(assignment, content):
    received.append((assignment.name, content))
    if assignment.name == "independent-a":
      raise RuntimeError("provider unavailable")
    return '{"schema_version":1,"findings":[],"summary":"ok"}'

  executions = review_execution.execute_review_assignments(
    payload,
    assignments,
    runner=runner,
  )

  assert tuple(execution.assignment.name for execution in executions) == (
    "independent-a",
    "independent-b",
    "main",
  )
  assert tuple(execution.status for execution in executions) == (
    "failed",
    "succeeded",
    "succeeded",
  )
  assert executions[1].raw_response is not None
  assert executions[0].error == "provider unavailable"
  assert {
    execution.contracted_payload_digest
    for execution in executions
  } == {payload.digest}
  assert {
    content
    for _name, content in received
  } == {payload.content}


@pytest.mark.parametrize("route", ("main", "independent"))
def test_rejects_assignment_set_missing_required_route(route):
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  assignment = review_execution.ReviewAssignment(
    name=route,
    provider="provider",
    model="model",
    route=route,
  )

  with pytest.raises(review_execution.ReviewExecutionError):
    review_execution.execute_review_assignments(
      _contracted_payload(review_contract),
      (assignment,),
      runner=lambda _assignment, _content: "{}",
    )
