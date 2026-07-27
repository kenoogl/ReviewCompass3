"""固定プロンプトと出力schemaを持つレビュー契約。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json

from tools.bootstrap.closed_payload import ClosedPayload


PROMPT_VERSION = "bootstrap-review-v1"
OUTPUT_SCHEMA_VERSION = 1
PROMPT = (
  "閉鎖payload内の材料だけを根拠としてレビューし、"
  "指定されたJSON schemaだけで応答してください。"
)

_OUTPUT_SCHEMA = {
  "additionalProperties": False,
  "properties": {
    "findings": {
      "items": {
        "additionalProperties": False,
        "properties": {
          "description": {"type": "string"},
          "id": {"type": "string"},
          "material_identifiers": {
            "items": {"type": "string"},
            "type": "array",
          },
          "severity": {
            "enum": ["error", "warning", "info"],
            "type": "string",
          },
          "title": {"type": "string"},
        },
        "required": [
          "id",
          "severity",
          "title",
          "description",
          "material_identifiers",
        ],
        "type": "object",
      },
      "type": "array",
    },
    "schema_version": {"const": 1, "type": "integer"},
    "summary": {"type": "string"},
  },
  "required": [
    "schema_version",
    "findings",
    "summary",
  ],
  "type": "object",
}


class ReviewContractError(Exception):
  """固定レビュー契約を安全に生成できない。"""


@dataclasses.dataclass(frozen=True)
class ContractedReviewPayload:
  content: str
  digest: str
  closed_payload_digest: str
  prompt_version: str
  output_schema_version: int
  output_schema_digest: str


def output_schema():
  return json.loads(json.dumps(_OUTPUT_SCHEMA))


def materialize_review_contract(
  closed_payload,
  *,
  prompt_version=PROMPT_VERSION,
  output_schema_version=OUTPUT_SCHEMA_VERSION,
) -> ContractedReviewPayload:
  if (
    prompt_version != PROMPT_VERSION
    or output_schema_version != OUTPUT_SCHEMA_VERSION
  ):
    raise ReviewContractError(
      "Unknown prompt or output schema version"
    )
  if (
    not isinstance(closed_payload, ClosedPayload)
    or hashlib.sha256(
      closed_payload.content.encode("utf-8")
    ).hexdigest() != closed_payload.digest
  ):
    raise ReviewContractError(
      "Review contract requires an intact closed payload"
    )
  try:
    closed_document = json.loads(closed_payload.content)
  except (TypeError, json.JSONDecodeError) as error:
    raise ReviewContractError(
      "Closed payload must contain JSON"
    ) from error

  schema = output_schema()
  schema_bytes = json.dumps(
    schema,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode("utf-8")
  schema_digest = hashlib.sha256(schema_bytes).hexdigest()
  content = json.dumps(
    {
      "closed_payload": closed_document,
      "closed_payload_digest": closed_payload.digest,
      "output_schema": schema,
      "output_schema_digest": schema_digest,
      "output_schema_version": OUTPUT_SCHEMA_VERSION,
      "prompt": PROMPT,
      "prompt_version": PROMPT_VERSION,
    },
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  )
  return ContractedReviewPayload(
    content=content,
    digest=hashlib.sha256(
      content.encode("utf-8")
    ).hexdigest(),
    closed_payload_digest=closed_payload.digest,
    prompt_version=PROMPT_VERSION,
    output_schema_version=OUTPUT_SCHEMA_VERSION,
    output_schema_digest=schema_digest,
  )
