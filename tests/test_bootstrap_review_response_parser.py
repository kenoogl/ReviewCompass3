"""レビュー応答の厳格解析に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _store_response(tmp_path, response):
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  raw_review_store = importlib.import_module(
    "tools.bootstrap.raw_review_store"
  )
  assignment = review_execution.ReviewAssignment(
    name="main",
    provider="provider",
    model="model",
    route="main",
  )
  execution = review_execution.ReviewExecution(
    assignment=assignment,
    status="succeeded",
    raw_response=json.dumps(response),
    error=None,
    contracted_payload_digest="p" * 64,
  )
  record = raw_review_store.store_raw_executions(
    tmp_path,
    "attempt-001",
    (execution,),
  )[0]
  return record


def _valid_response():
  return {
    "schema_version": 1,
    "findings": [
      {
        "id": "F-001",
        "severity": "warning",
        "title": "Missing guard",
        "description": "The boundary is not checked.",
        "material_identifiers": ["target.md"],
      },
    ],
    "summary": "One finding.",
  }


def test_strictly_parses_and_digest_links_valid_raw_response(tmp_path):
  record = _store_response(tmp_path, _valid_response())
  response_parser = importlib.import_module(
    "tools.bootstrap.review_response_parser"
  )

  parsed = response_parser.parse_raw_review_record(
    tmp_path,
    record,
  )

  assert parsed.assignment_name == "main"
  assert parsed.route == "main"
  assert parsed.raw_digest == record.raw_digest
  assert parsed.contracted_payload_digest == "p" * 64
  assert parsed.findings == (
    response_parser.ParsedFinding(
      identifier="F-001",
      severity="warning",
      title="Missing guard",
      description="The boundary is not checked.",
      material_identifiers=("target.md",),
    ),
  )
  assert parsed.summary == "One finding."
  assert len(parsed.digest) == 64


@pytest.mark.parametrize(
  "mutation",
  (
    "missing",
    "unknown",
    "wrong_type",
    "unknown_severity",
    "duplicate_id",
  ),
)
def test_rejects_response_outside_fixed_schema(tmp_path, mutation):
  response = _valid_response()
  if mutation == "missing":
    del response["summary"]
  elif mutation == "unknown":
    response["extra"] = True
  elif mutation == "wrong_type":
    response["findings"][0]["material_identifiers"] = "target.md"
  elif mutation == "unknown_severity":
    response["findings"][0]["severity"] = "critical"
  else:
    response["findings"].append(dict(response["findings"][0]))
  record = _store_response(tmp_path, response)
  response_parser = importlib.import_module(
    "tools.bootstrap.review_response_parser"
  )

  with pytest.raises(response_parser.ReviewResponseParseError):
    response_parser.parse_raw_review_record(tmp_path, record)


def test_rejects_modified_raw_record(tmp_path):
  record = _store_response(tmp_path, _valid_response())
  path = tmp_path / record.relative_path
  document = json.loads(path.read_text(encoding="utf-8"))
  document["raw_response"] = "{}"
  path.write_text(json.dumps(document), encoding="utf-8")
  response_parser = importlib.import_module(
    "tools.bootstrap.review_response_parser"
  )

  with pytest.raises(response_parser.ReviewResponseParseError):
    response_parser.parse_raw_review_record(tmp_path, record)
