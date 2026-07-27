"""第5段のbootstrap実装適合性監査契約。"""

import dataclasses
import hashlib
import json
import re


class BootstrapConformanceError(Exception):
  """bootstrap適合性を安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class BootstrapConformance:
  status: str
  counts: dict
  digest: str


_FIELDS = {
  "requirement_id",
  "classification",
  "target_design_id",
  "implementation_evidence",
  "test_evidence",
  "rationale",
  "gaps",
}
_REQUIREMENT_ID = re.compile(
  r"REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}"
)
_DESIGN_ID = re.compile(
  r"DES-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)
_COMMIT = re.compile(r"[0-9a-f]{40}")
_CLASSIFICATIONS = {
  "conformant",
  "adapt",
  "replace",
  "defer",
}


def _text(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _defined(values, pattern, label):
  result = tuple(values)
  if (
    not result
    or len(set(result)) != len(result)
    or any(
      not _text(value)
      or pattern.fullmatch(value) is None
      for value in result
    )
  ):
    raise BootstrapConformanceError(
      f"{label} definitions must be unique valid IDs"
    )
  return frozenset(result)


def _paths(value, *, defined, label):
  if not isinstance(value, (list, tuple)):
    raise BootstrapConformanceError(
      f"{label} must be a sequence"
    )
  result = tuple(value)
  if (
    len(set(result)) != len(result)
    or any(not _text(item) for item in result)
    or not set(result) <= defined
  ):
    raise BootstrapConformanceError(
      f"{label} must resolve"
    )
  return result


def validate_bootstrap_conformance(
  *,
  records,
  defined_requirement_ids,
  defined_design_ids,
  defined_evidence_paths,
  bootstrap_commit,
):
  requirement_ids = _defined(
    defined_requirement_ids,
    _REQUIREMENT_ID,
    "requirement",
  )
  design_ids = _defined(
    defined_design_ids,
    _DESIGN_ID,
    "design",
  )
  evidence_paths = frozenset(defined_evidence_paths)
  if (
    not evidence_paths
    or any(not _text(value) for value in evidence_paths)
    or not _text(bootstrap_commit)
    or _COMMIT.fullmatch(bootstrap_commit) is None
  ):
    raise BootstrapConformanceError(
      "fixed bootstrap evidence is required"
    )
  parsed = []
  for value in records:
    if (
      not isinstance(value, dict)
      or set(value) != _FIELDS
      or value["requirement_id"] not in requirement_ids
      or value["classification"] not in _CLASSIFICATIONS
      or value["target_design_id"] not in design_ids
      or not _text(value["rationale"])
      or not isinstance(value["gaps"], (list, tuple))
      or any(not _text(item) for item in value["gaps"])
    ):
      raise BootstrapConformanceError(
        "conformance records require fixed fields"
      )
    parsed_value = dict(value)
    parsed_value["implementation_evidence"] = _paths(
      value["implementation_evidence"],
      defined=evidence_paths,
      label="implementation evidence",
    )
    parsed_value["test_evidence"] = _paths(
      value["test_evidence"],
      defined=evidence_paths,
      label="test evidence",
    )
    parsed_value["gaps"] = tuple(value["gaps"])
    if value["classification"] == "conformant":
      if (
        not parsed_value["implementation_evidence"]
        or not parsed_value["test_evidence"]
        or parsed_value["gaps"]
      ):
        raise BootstrapConformanceError(
          "conformant requires implementation and tests without gaps"
        )
    elif not parsed_value["gaps"]:
      raise BootstrapConformanceError(
        "nonconformant classifications require gaps"
      )
    parsed.append(parsed_value)
  record_ids = [
    value["requirement_id"] for value in parsed
  ]
  if (
    len(set(record_ids)) != len(record_ids)
    or set(record_ids) != requirement_ids
  ):
    raise BootstrapConformanceError(
      "every requirement requires one classification"
    )
  counts = {
    classification: sum(
      value["classification"] == classification
      for value in parsed
    )
    for classification in sorted(_CLASSIFICATIONS)
  }
  document = {
    "bootstrap_commit": bootstrap_commit,
    "records": sorted(
      parsed,
      key=lambda value: value["requirement_id"],
    ),
    "schema_version": 1,
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return BootstrapConformance(
    status="complete",
    counts=counts,
    digest=digest,
  )
