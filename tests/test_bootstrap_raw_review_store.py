"""rawレビュー応答の不変保存に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _executions(review_execution):
  main = review_execution.ReviewAssignment(
    name="main",
    provider="provider-a",
    model="model-a",
    route="main",
  )
  independent = review_execution.ReviewAssignment(
    name="independent",
    provider="provider-b",
    model="model-b",
    route="independent",
  )
  return (
    review_execution.ReviewExecution(
      assignment=independent,
      status="failed",
      raw_response=None,
      error="provider unavailable",
      contracted_payload_digest="p" * 64,
    ),
    review_execution.ReviewExecution(
      assignment=main,
      status="succeeded",
      raw_response='{"summary":"ok"}',
      error=None,
      contracted_payload_digest="p" * 64,
    ),
  )


def test_stores_success_and_failure_as_digest_linked_immutable_raw_records(
  tmp_path,
):
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  raw_review_store = importlib.import_module(
    "tools.bootstrap.raw_review_store"
  )
  storage_root = tmp_path / "raw"

  records = raw_review_store.store_raw_executions(
    storage_root,
    "attempt-001",
    _executions(review_execution),
  )

  assert tuple(record.assignment_name for record in records) == (
    "independent",
    "main",
  )
  assert tuple(record.status for record in records) == (
    "failed",
    "succeeded",
  )
  main_record = records[1]
  assert main_record.contracted_payload_digest == "p" * 64
  assert main_record.raw_digest == hashlib.sha256(
    b'{"summary":"ok"}'
  ).hexdigest()
  stored = json.loads(
    (storage_root / main_record.relative_path).read_text(
      encoding="utf-8"
    )
  )
  assert stored["raw_response"] == '{"summary":"ok"}'
  assert stored["raw_digest"] == main_record.raw_digest
  assert stored["assignment"]["route"] == "main"

  original_bytes = {
    record.relative_path: (
      storage_root / record.relative_path
    ).read_bytes()
    for record in records
  }
  with pytest.raises(raw_review_store.RawReviewStoreError):
    raw_review_store.store_raw_executions(
      storage_root,
      "attempt-001",
      _executions(review_execution),
    )
  assert original_bytes == {
    record.relative_path: (
      storage_root / record.relative_path
    ).read_bytes()
    for record in records
  }


def test_rejects_unsafe_attempt_identifier(tmp_path):
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  raw_review_store = importlib.import_module(
    "tools.bootstrap.raw_review_store"
  )

  with pytest.raises(raw_review_store.RawReviewStoreError):
    raw_review_store.store_raw_executions(
      tmp_path,
      "../attempt",
      _executions(review_execution),
    )
