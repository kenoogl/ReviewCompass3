"""レビュー中断再開と成功成果温存の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib


def test_resumes_only_unsuccessful_assignment_and_preserves_history(tmp_path):
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  raw_review_store = importlib.import_module(
    "tools.bootstrap.raw_review_store"
  )
  review_resume = importlib.import_module(
    "tools.bootstrap.review_resume"
  )
  content = '{"contract":"fixed"}'
  payload = review_contract.ContractedReviewPayload(
    content=content,
    digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    closed_payload_digest="c" * 64,
    prompt_version="bootstrap-review-v1",
    output_schema_version=1,
    output_schema_digest="s" * 64,
  )
  assignments = (
    review_execution.ReviewAssignment(
      "main",
      "provider",
      "model-main",
      "main",
    ),
    review_execution.ReviewAssignment(
      "independent",
      "provider",
      "model-independent",
      "independent",
    ),
  )
  initial = (
    review_execution.ReviewExecution(
      assignments[0],
      "succeeded",
      '{"result":"main"}',
      None,
      payload.digest,
    ),
    review_execution.ReviewExecution(
      assignments[1],
      "failed",
      None,
      "temporary failure",
      payload.digest,
    ),
  )
  records = raw_review_store.store_raw_executions(
    tmp_path,
    "attempt-001",
    initial,
  )
  original = {
    record.relative_path: (
      tmp_path / record.relative_path
    ).read_bytes()
    for record in records
  }
  called = []

  resumed = review_resume.resume_review_assignments(
    payload,
    assignments,
    records,
    runner=lambda assignment, _content: (
      called.append(assignment.name)
      or '{"result":"independent"}'
    ),
  )

  assert called == ["independent"]
  assert tuple(
    record.assignment_name
    for record in resumed.completed_records
  ) == ("main",)
  assert tuple(
    record.assignment_name
    for record in resumed.failed_history
  ) == ("independent",)
  assert tuple(
    execution.assignment.name
    for execution in resumed.new_executions
  ) == ("independent",)
  assert resumed.new_executions[0].status == "succeeded"
  assert original == {
    record.relative_path: (
      tmp_path / record.relative_path
    ).read_bytes()
    for record in records
  }
