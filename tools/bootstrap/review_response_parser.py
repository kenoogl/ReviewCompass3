"""不変raw記録からの厳格レビュー応答解析。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path, PurePosixPath

from tools.bootstrap.raw_review_store import RawReviewRecord


_ROOT_KEYS = {"schema_version", "findings", "summary"}
_FINDING_KEYS = {
  "id",
  "severity",
  "title",
  "description",
  "material_identifiers",
}
_SEVERITIES = {"error", "warning", "info"}


class ReviewResponseParseError(Exception):
  """rawレビュー応答を固定schemaで解析できない。"""


@dataclasses.dataclass(frozen=True)
class ParsedFinding:
  identifier: str
  severity: str
  title: str
  description: str
  material_identifiers: tuple


@dataclasses.dataclass(frozen=True)
class ParsedReview:
  assignment_name: str
  route: str
  contracted_payload_digest: str
  raw_digest: str
  findings: tuple
  summary: str
  digest: str


def _load_raw_document(storage_root, record):
  if not isinstance(record, RawReviewRecord):
    raise ReviewResponseParseError(
      "Expected an immutable raw review record"
    )
  relative = PurePosixPath(record.relative_path)
  if (
    relative.is_absolute()
    or any(part in ("", ".", "..") for part in relative.parts)
  ):
    raise ReviewResponseParseError(
      "Unsafe raw review record path"
    )
  path = Path(storage_root).resolve()
  for part in relative.parts:
    path = path / part
    if path.is_symlink():
      raise ReviewResponseParseError(
        "Raw review record must not be a symbolic link"
      )
  try:
    document = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
    raise ReviewResponseParseError(
      "Cannot read raw review record"
    ) from error
  if (
    not isinstance(document, dict)
    or set(document) != {
      "assignment",
      "attempt_id",
      "contracted_payload_digest",
      "error",
      "raw_digest",
      "raw_response",
      "status",
    }
    or not isinstance(document["assignment"], dict)
    or set(document["assignment"]) != {
      "model",
      "name",
      "provider",
      "route",
    }
    or document["attempt_id"] != record.attempt_id
    or document["assignment"]["name"] != record.assignment_name
    or document["assignment"]["route"] != record.route
    or document["status"] != record.status
    or document["contracted_payload_digest"]
    != record.contracted_payload_digest
    or document["raw_digest"] != record.raw_digest
  ):
    raise ReviewResponseParseError(
      "Raw review record metadata does not match"
    )
  if (
    document["status"] != "succeeded"
    or not isinstance(document["raw_response"], str)
    or document["error"] is not None
    or hashlib.sha256(
      document["raw_response"].encode("utf-8")
    ).hexdigest() != record.raw_digest
  ):
    raise ReviewResponseParseError(
      "Only intact successful raw responses can be parsed"
    )
  return document


def _required_text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
  )


def _parse_finding(value):
  if (
    not isinstance(value, dict)
    or set(value) != _FINDING_KEYS
    or not _required_text(value["id"])
    or value["severity"] not in _SEVERITIES
    or not _required_text(value["title"])
    or not _required_text(value["description"])
    or not isinstance(value["material_identifiers"], list)
    or any(
      not _required_text(identifier)
      for identifier in value["material_identifiers"]
    )
    or len(set(value["material_identifiers"]))
    != len(value["material_identifiers"])
  ):
    raise ReviewResponseParseError(
      "Finding does not match the fixed schema"
    )
  return ParsedFinding(
    identifier=value["id"],
    severity=value["severity"],
    title=value["title"],
    description=value["description"],
    material_identifiers=tuple(sorted(
      value["material_identifiers"]
    )),
  )


def parse_raw_review_record(storage_root, record) -> ParsedReview:
  raw_document = _load_raw_document(storage_root, record)
  try:
    response = json.loads(raw_document["raw_response"])
  except json.JSONDecodeError as error:
    raise ReviewResponseParseError(
      "Raw response must be one JSON document"
    ) from error
  if (
    not isinstance(response, dict)
    or set(response) != _ROOT_KEYS
    or type(response["schema_version"]) is not int
    or response["schema_version"] != 1
    or not isinstance(response["findings"], list)
    or not isinstance(response["summary"], str)
  ):
    raise ReviewResponseParseError(
      "Response does not match the fixed root schema"
    )
  findings = tuple(sorted(
    (
      _parse_finding(value)
      for value in response["findings"]
    ),
    key=lambda finding: finding.identifier,
  ))
  identifiers = tuple(
    finding.identifier
    for finding in findings
  )
  if len(set(identifiers)) != len(identifiers):
    raise ReviewResponseParseError(
      "Finding identifiers must be unique"
    )
  parsed_document = {
    "assignment_name": record.assignment_name,
    "contracted_payload_digest": (
      record.contracted_payload_digest
    ),
    "findings": [
      {
        "description": finding.description,
        "id": finding.identifier,
        "material_identifiers": list(
          finding.material_identifiers
        ),
        "severity": finding.severity,
        "title": finding.title,
      }
      for finding in findings
    ],
    "raw_digest": record.raw_digest,
    "route": record.route,
    "summary": response["summary"],
  }
  digest = hashlib.sha256(
    json.dumps(
      parsed_document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return ParsedReview(
    assignment_name=record.assignment_name,
    route=record.route,
    contracted_payload_digest=record.contracted_payload_digest,
    raw_digest=record.raw_digest,
    findings=findings,
    summary=response["summary"],
    digest=digest,
  )
