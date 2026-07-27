"""固定プロンプト・出力schema契約の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import importlib
import json

import pytest


def _closed_payload(closed_payload):
  content = json.dumps(
    {
      "bundle_digest": "b" * 64,
      "materials": [],
      "schema_version": 1,
      "target_digest": "t" * 64,
    },
    separators=(",", ":"),
    sort_keys=True,
  )
  return closed_payload.ClosedPayload(
    content=content,
    digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    bundle_digest="b" * 64,
    target_digest="t" * 64,
    material_identifiers=(),
  )


def test_materializes_deterministic_versioned_review_contract():
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )
  payload = _closed_payload(closed_payload)

  contracted = review_contract.materialize_review_contract(payload)

  document = json.loads(contracted.content)
  assert document["prompt_version"] == "bootstrap-review-v1"
  assert document["output_schema"]["additionalProperties"] is False
  assert document["output_schema"]["required"] == [
    "schema_version",
    "findings",
    "summary",
  ]
  assert document["closed_payload_digest"] == payload.digest
  assert contracted.digest == hashlib.sha256(
    contracted.content.encode("utf-8")
  ).hexdigest()
  assert contracted == review_contract.materialize_review_contract(payload)


@pytest.mark.parametrize(
  "override",
  (
    {"prompt_version": "unknown"},
    {"output_schema_version": 999},
  ),
)
def test_rejects_unknown_contract_versions(override):
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )

  with pytest.raises(review_contract.ReviewContractError):
    review_contract.materialize_review_contract(
      _closed_payload(closed_payload),
      **override,
    )


def test_rejects_modified_closed_payload():
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  review_contract = importlib.import_module(
    "tools.bootstrap.review_contract"
  )
  payload = dataclasses.replace(
    _closed_payload(closed_payload),
    content='{"modified":true}',
  )

  with pytest.raises(review_contract.ReviewContractError):
    review_contract.materialize_review_contract(payload)
