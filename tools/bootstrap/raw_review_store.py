"""レビューraw応答と失敗診断の不変保存。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path
import re

from tools.bootstrap.review_execution import ReviewExecution


_IDENTIFIER_PATTERN = re.compile(r"[a-z0-9][a-z0-9._-]*")


class RawReviewStoreError(Exception):
  """rawレビュー記録を安全に不変保存できない。"""


@dataclasses.dataclass(frozen=True)
class RawReviewRecord:
  attempt_id: str
  assignment_name: str
  route: str
  status: str
  contracted_payload_digest: str
  raw_digest: str
  relative_path: str


def _raw_value(execution):
  if (
    execution.status == "succeeded"
    and isinstance(execution.raw_response, str)
    and execution.error is None
  ):
    return execution.raw_response
  if (
    execution.status == "failed"
    and execution.raw_response is None
    and isinstance(execution.error, str)
  ):
    return execution.error
  raise RawReviewStoreError(
    "Invalid review execution result"
  )


def _validate_executions(executions):
  values = tuple(executions)
  for execution in values:
    if (
      not isinstance(execution, ReviewExecution)
      or _IDENTIFIER_PATTERN.fullmatch(
        execution.assignment.name or ""
      ) is None
      or execution.assignment.route not in ("main", "independent")
      or not isinstance(
        execution.contracted_payload_digest,
        str,
      )
      or len(execution.contracted_payload_digest) != 64
    ):
      raise RawReviewStoreError(
        "Invalid review execution metadata"
      )
    _raw_value(execution)
  names = tuple(
    execution.assignment.name
    for execution in values
  )
  if len(set(names)) != len(names):
    raise RawReviewStoreError(
      "Execution assignment names must be unique"
    )
  return tuple(sorted(
    values,
    key=lambda execution: execution.assignment.name,
  ))


def store_raw_executions(
  storage_root,
  attempt_id,
  executions,
) -> tuple:
  if (
    not isinstance(attempt_id, str)
    or _IDENTIFIER_PATTERN.fullmatch(attempt_id) is None
  ):
    raise RawReviewStoreError(
      "Unsafe raw review attempt identifier"
    )
  execution_values = _validate_executions(executions)
  root = Path(storage_root).resolve()
  attempt_root = root / attempt_id
  try:
    root.mkdir(parents=True, exist_ok=True)
    attempt_root.mkdir(exist_ok=False)
  except OSError as error:
    raise RawReviewStoreError(
      "Raw review attempt already exists or cannot be created"
    ) from error

  records = []
  try:
    for execution in execution_values:
      raw_value = _raw_value(execution)
      raw_digest = hashlib.sha256(
        raw_value.encode("utf-8")
      ).hexdigest()
      relative_path = (
        "%s/%s.raw.json"
        % (attempt_id, execution.assignment.name)
      )
      document = {
        "assignment": {
          "model": execution.assignment.model,
          "name": execution.assignment.name,
          "provider": execution.assignment.provider,
          "route": execution.assignment.route,
        },
        "attempt_id": attempt_id,
        "contracted_payload_digest": (
          execution.contracted_payload_digest
        ),
        "error": execution.error,
        "raw_digest": raw_digest,
        "raw_response": execution.raw_response,
        "status": execution.status,
      }
      encoded = (
        json.dumps(
          document,
          ensure_ascii=False,
          separators=(",", ":"),
          sort_keys=True,
        )
        + "\n"
      )
      with (root / relative_path).open(
        "x",
        encoding="utf-8",
      ) as output:
        output.write(encoded)
      records.append(RawReviewRecord(
        attempt_id=attempt_id,
        assignment_name=execution.assignment.name,
        route=execution.assignment.route,
        status=execution.status,
        contracted_payload_digest=(
          execution.contracted_payload_digest
        ),
        raw_digest=raw_digest,
        relative_path=relative_path,
      ))
  except OSError as error:
    raise RawReviewStoreError(
      "Cannot preserve immutable raw review evidence"
    ) from error
  return tuple(records)
