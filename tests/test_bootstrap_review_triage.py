"""複数担当所見の統合・triageに関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import importlib
import json

import pytest


def _finding(identifier, severity, description):
  return {
    "id": identifier,
    "severity": severity,
    "title": "Finding " + identifier,
    "description": description,
    "material_identifiers": ["target.md"],
  }


def _parsed_reviews(tmp_path):
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  raw_review_store = importlib.import_module(
    "tools.bootstrap.raw_review_store"
  )
  response_parser = importlib.import_module(
    "tools.bootstrap.review_response_parser"
  )
  responses = {
    "main": {
      "schema_version": 1,
      "findings": [
        _finding("F-001", "warning", "same"),
        _finding("F-002", "error", "unsafe"),
      ],
      "summary": "main",
    },
    "independent": {
      "schema_version": 1,
      "findings": [
        _finding("F-001", "warning", "same"),
        _finding("F-002", "warning", "uncertain"),
        _finding("F-003", "info", "additional"),
      ],
      "summary": "independent",
    },
  }
  executions = tuple(
    review_execution.ReviewExecution(
      assignment=review_execution.ReviewAssignment(
        name=name,
        provider="provider-" + name,
        model="model-" + name,
        route=name,
      ),
      status="succeeded",
      raw_response=json.dumps(response),
      error=None,
      contracted_payload_digest="p" * 64,
    )
    for name, response in responses.items()
  )
  records = raw_review_store.store_raw_executions(
    tmp_path,
    "attempt-001",
    executions,
  )
  return tuple(
    response_parser.parse_raw_review_record(tmp_path, record)
    for record in records
  )


def test_deterministically_triages_duplicates_conflicts_and_singletons(
  tmp_path,
):
  reviews = _parsed_reviews(tmp_path)
  review_triage = importlib.import_module(
    "tools.bootstrap.review_triage"
  )

  triage = review_triage.triage_parsed_reviews(
    tuple(reversed(reviews))
  )

  assert tuple(finding.identifier for finding in triage.findings) == (
    "F-001",
    "F-002",
    "F-003",
  )
  assert tuple(finding.disposition for finding in triage.findings) == (
    "corroborated",
    "conflict",
    "single",
  )
  assert triage.findings[0].reporters == ("independent", "main")
  assert triage.findings[1].severities == ("error", "warning")
  assert triage.findings[1].descriptions == ("uncertain", "unsafe")
  assert {
    review.raw_digest
    for review in reviews
  } == set(triage.raw_digests)
  assert {
    review.digest
    for review in reviews
  } == set(triage.parsed_digests)
  assert len(triage.digest) == 64
  assert triage == review_triage.triage_parsed_reviews(reviews)


@pytest.mark.parametrize("invalid_kind", ("missing_route", "mixed_payload"))
def test_rejects_incomplete_or_mixed_review_sets(tmp_path, invalid_kind):
  reviews = _parsed_reviews(tmp_path)
  if invalid_kind == "missing_route":
    reviews = (reviews[0],)
  else:
    reviews = (
      reviews[0],
      dataclasses.replace(
        reviews[1],
        contracted_payload_digest="x" * 64,
      ),
    )
  review_triage = importlib.import_module(
    "tools.bootstrap.review_triage"
  )

  with pytest.raises(review_triage.ReviewTriageError):
    review_triage.triage_parsed_reviews(reviews)
