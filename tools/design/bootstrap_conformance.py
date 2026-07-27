"""第5段のbootstrap実装適合性監査契約。"""

import dataclasses
import hashlib
import json
import re
import subprocess
from pathlib import Path


class BootstrapConformanceError(Exception):
  """bootstrap適合性を安全に確定できない。"""


@dataclasses.dataclass(frozen=True)
class BootstrapConformance:
  status: str
  counts: dict
  digest: str


@dataclasses.dataclass(frozen=True)
class EvidenceBackedBootstrapConformance:
  status: str
  counts: dict
  gap_count: int
  evidence_count: int
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
_DIGEST = re.compile(r"[0-9a-f]{64}")
_CLASSIFICATIONS = {
  "conformant",
  "adapt",
  "replace",
  "defer",
}
_GAP_CATEGORY_BY_CLASSIFICATION = {
  "adapt": {
    "adaptation",
    "missing_boundary",
    "missing_gate",
  },
  "replace": {
    "incompatible_boundary",
    "replacement",
  },
  "defer": {"deferred"},
}
_EVIDENCE_FIELDS = {
  "path",
  "blob_sha256",
  "role",
  "requirement_ids",
}
_EVIDENCE_ROLES = {"implementation", "test"}
_TEST_RUN_FIELDS = {
  "bootstrap_commit",
  "command",
  "status",
  "passed_count",
  "output_digest",
}
_GAP_FIELDS = {
  "gap_id",
  "requirement_id",
  "category",
  "component",
  "atomic_obligation_ids",
  "depends_on_gap_ids",
  "acceptance_test_ids",
  "stop_condition",
}
_DEPENDENCY_FIELDS = {
  "provider_requirement_id",
  "consumer_requirement_id",
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


def _unique_texts(value, label, *, empty=False):
  if not isinstance(value, (list, tuple)):
    raise BootstrapConformanceError(
      f"{label} must be a sequence"
    )
  result = tuple(value)
  if (
    (not empty and not result)
    or len(set(result)) != len(result)
    or any(not _text(item) for item in result)
  ):
    raise BootstrapConformanceError(
      f"{label} must contain unique text"
    )
  return result


def validate_evidence_backed_bootstrap_conformance(
  *,
  records,
  requirement_design_map,
  evidence_manifest,
  commit_blob_map,
  test_run,
  gaps,
  requirement_dependencies,
  bootstrap_commit,
  approved_obligation_map=None,
  design_component_map=None,
  requirement_acceptance_test_map=None,
  approved_requirement_dependencies=None,
  normalized_test_output=None,
  expected_passed_count=None,
  repository_root=None,
):
  if (
    not isinstance(requirement_design_map, dict)
    or not requirement_design_map
  ):
    raise BootstrapConformanceError(
      "requirement design map is required"
    )
  requirement_ids = frozenset(requirement_design_map)
  if any(
    _REQUIREMENT_ID.fullmatch(requirement_id) is None
    or _DESIGN_ID.fullmatch(design_id) is None
    for requirement_id, design_id
    in requirement_design_map.items()
  ):
    raise BootstrapConformanceError(
      "requirement design map is invalid"
    )

  parsed_evidence = []
  evidence_by_path = {}
  for value in evidence_manifest:
    if (
      not isinstance(value, dict)
      or set(value) != _EVIDENCE_FIELDS
      or not _text(value["path"])
      or _DIGEST.fullmatch(value["blob_sha256"]) is None
      or value["role"] not in _EVIDENCE_ROLES
    ):
      raise BootstrapConformanceError(
        "evidence manifest entries are invalid"
      )
    evidence_requirements = _unique_texts(
      value["requirement_ids"],
      "evidence requirements",
    )
    if (
      not set(evidence_requirements) <= requirement_ids
      or value["path"] in evidence_by_path
      or commit_blob_map.get(value["path"])
      != value["blob_sha256"]
    ):
      raise BootstrapConformanceError(
        "evidence must resolve to fixed commit blobs"
      )
    parsed = dict(value)
    parsed["requirement_ids"] = evidence_requirements
    parsed_evidence.append(parsed)
    evidence_by_path[value["path"]] = parsed
  if (
    not parsed_evidence
    or set(commit_blob_map) != set(evidence_by_path)
  ):
    raise BootstrapConformanceError(
      "evidence manifest coverage must be exact"
    )
  if repository_root is not None:
    validate_commit_blob_claims(
      repository_root=repository_root,
      bootstrap_commit=bootstrap_commit,
      commit_blob_map=commit_blob_map,
    )

  if (
    not isinstance(test_run, dict)
    or set(test_run) != _TEST_RUN_FIELDS
    or test_run["bootstrap_commit"] != bootstrap_commit
    or _COMMIT.fullmatch(bootstrap_commit) is None
    or test_run["command"] != "python3 -m pytest -q"
    or test_run["status"] != "passed"
    or not isinstance(test_run["passed_count"], int)
    or isinstance(test_run["passed_count"], bool)
    or test_run["passed_count"] < 1
    or _DIGEST.fullmatch(
      test_run["output_digest"]
    ) is None
  ):
    raise BootstrapConformanceError(
      "fixed bootstrap test run must pass"
    )
  if normalized_test_output is not None:
    if (
      not isinstance(normalized_test_output, str)
      or hashlib.sha256(
        normalized_test_output.encode("utf-8")
      ).hexdigest() != test_run["output_digest"]
      or test_run["passed_count"]
      != expected_passed_count
    ):
      raise BootstrapConformanceError(
        "test output and count must match observation"
      )

  parsed_gaps = []
  gap_by_id = {}
  for value in gaps:
    if (
      not isinstance(value, dict)
      or set(value) != _GAP_FIELDS
      or not _text(value["gap_id"])
      or value["requirement_id"] not in requirement_ids
      or not _text(value["category"])
      or not _text(value["component"])
      or not _text(value["stop_condition"])
      or value["gap_id"] in gap_by_id
    ):
      raise BootstrapConformanceError(
        "gap entries are invalid"
      )
    parsed = dict(value)
    for field in (
      "atomic_obligation_ids",
      "depends_on_gap_ids",
      "acceptance_test_ids",
    ):
      parsed[field] = _unique_texts(
        value[field],
        field,
        empty=field == "depends_on_gap_ids",
      )
    if approved_obligation_map is not None and any(
      approved_obligation_map.get(obligation_id)
      != value["requirement_id"]
      for obligation_id
      in parsed["atomic_obligation_ids"]
    ):
      raise BootstrapConformanceError(
        "gap obligations must resolve to approved IDs"
      )
    if (
      design_component_map is not None
      and value["component"] not in design_component_map.get(
        requirement_design_map[value["requirement_id"]],
        (),
      )
    ):
      raise BootstrapConformanceError(
        "gap component must belong to target design"
      )
    if (
      requirement_acceptance_test_map is not None
      and parsed["acceptance_test_ids"] != (
        requirement_acceptance_test_map[
          value["requirement_id"]
        ],
      )
    ):
      raise BootstrapConformanceError(
        "gap acceptance test must match requirement"
      )
    parsed_gaps.append(parsed)
    gap_by_id[value["gap_id"]] = parsed
  for gap in parsed_gaps:
    if any(
      dependency_id not in gap_by_id
      for dependency_id in gap["depends_on_gap_ids"]
    ):
      raise BootstrapConformanceError(
        "gap dependencies must resolve"
      )

  result = validate_bootstrap_conformance(
    records=records,
    defined_requirement_ids=requirement_ids,
    defined_design_ids=set(
      requirement_design_map.values()
    ),
    defined_evidence_paths=set(evidence_by_path),
    bootstrap_commit=bootstrap_commit,
  )
  parsed_records = tuple(records)
  record_by_requirement = {
    value["requirement_id"]: value
    for value in parsed_records
  }
  for record in parsed_records:
    requirement_id = record["requirement_id"]
    if (
      record["target_design_id"]
      != requirement_design_map[requirement_id]
    ):
      raise BootstrapConformanceError(
        "record design must match approved map"
      )
    for role, field in (
      ("implementation", "implementation_evidence"),
      ("test", "test_evidence"),
    ):
      for path in record[field]:
        evidence = evidence_by_path[path]
        if (
          evidence["role"] != role
          or requirement_id
          not in evidence["requirement_ids"]
        ):
          raise BootstrapConformanceError(
            "record evidence role and requirement must match"
          )
    record_gap_ids = tuple(record["gaps"])
    if any(
      gap_id not in gap_by_id
      or gap_by_id[gap_id]["requirement_id"]
      != requirement_id
      for gap_id in record_gap_ids
    ):
      raise BootstrapConformanceError(
        "record gaps must resolve to requirement"
      )
    classification = record["classification"]
    if classification in ("adapt", "replace") and (
      not record["implementation_evidence"]
      or not record["test_evidence"]
    ):
      raise BootstrapConformanceError(
        "adapt and replace require comparison evidence"
      )
    if classification == "defer" and (
      record["implementation_evidence"]
      or record["test_evidence"]
    ):
      raise BootstrapConformanceError(
        "defer cannot claim bootstrap evidence"
      )
    expected_category = (
      _GAP_CATEGORY_BY_CLASSIFICATION.get(
        classification
      )
    )
    for gap_id in record_gap_ids:
      gap = gap_by_id[gap_id]
      if (
        gap["category"] not in expected_category
        or any(
          not obligation_id.startswith(
            f"{requirement_id}#"
          )
          for obligation_id
          in gap["atomic_obligation_ids"]
        )
      ):
        raise BootstrapConformanceError(
          "gap semantics must match classification"
        )
  used_gap_ids = {
    gap_id
    for record in parsed_records
    for gap_id in record["gaps"]
  }
  if used_gap_ids != set(gap_by_id):
    raise BootstrapConformanceError(
      "gap coverage must be exact"
    )

  parsed_dependencies = []
  for value in requirement_dependencies:
    if (
      not isinstance(value, dict)
      or set(value) != _DEPENDENCY_FIELDS
      or value["provider_requirement_id"]
      not in requirement_ids
      or value["consumer_requirement_id"]
      not in requirement_ids
    ):
      raise BootstrapConformanceError(
        "requirement dependencies are invalid"
      )
    provider = record_by_requirement[
      value["provider_requirement_id"]
    ]
    consumer = record_by_requirement[
      value["consumer_requirement_id"]
    ]
    if (
      consumer["classification"] == "conformant"
      and provider["classification"] != "conformant"
    ):
      raise BootstrapConformanceError(
        "conformant record requires conformant dependencies"
      )
    if (
      provider["classification"] != "conformant"
      and consumer["classification"] != "conformant"
    ):
      provider_gap_ids = set(provider["gaps"])
      consumer_gap_dependencies = {
        gap_id
        for consumer_gap_id in consumer["gaps"]
        for gap_id in gap_by_id[
          consumer_gap_id
        ]["depends_on_gap_ids"]
      }
      if not (
        provider_gap_ids
        <= consumer_gap_dependencies
      ):
        raise BootstrapConformanceError(
          "nonconformant dependency gaps must be linked"
        )
    parsed_dependencies.append(dict(value))
  if approved_requirement_dependencies is not None:
    actual_dependencies = {
      (
        value["provider_requirement_id"],
        value["consumer_requirement_id"],
      )
      for value in parsed_dependencies
    }
    approved_dependencies = {
      (
        value["provider_requirement_id"],
        value["consumer_requirement_id"],
      )
      for value in approved_requirement_dependencies
    }
    if actual_dependencies != approved_dependencies:
      raise BootstrapConformanceError(
        "requirement dependency coverage must be exact"
      )

  document = {
    "bootstrap_commit": bootstrap_commit,
    "evidence_manifest": sorted(
      parsed_evidence,
      key=lambda value: value["path"],
    ),
    "gaps": sorted(
      parsed_gaps,
      key=lambda value: value["gap_id"],
    ),
    "records": sorted(
      parsed_records,
      key=lambda value: value["requirement_id"],
    ),
    "requirement_dependencies": sorted(
      parsed_dependencies,
      key=lambda value: (
        value["provider_requirement_id"],
        value["consumer_requirement_id"],
      ),
    ),
    "requirement_design_map": dict(sorted(
      requirement_design_map.items()
    )),
    "schema_version": 1,
    "test_run": dict(test_run),
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return EvidenceBackedBootstrapConformance(
    status="complete",
    counts=result.counts,
    gap_count=len(parsed_gaps),
    evidence_count=len(parsed_evidence),
    digest=digest,
  )


def validate_commit_blob_claims(
  *,
  repository_root,
  bootstrap_commit,
  commit_blob_map,
):
  root = Path(repository_root)
  if (
    not root.is_dir()
    or _COMMIT.fullmatch(bootstrap_commit) is None
    or not isinstance(commit_blob_map, dict)
    or not commit_blob_map
  ):
    raise BootstrapConformanceError(
      "commit blob verification inputs are invalid"
    )
  for path, declared_digest in commit_blob_map.items():
    if (
      not _text(path)
      or _DIGEST.fullmatch(declared_digest) is None
    ):
      raise BootstrapConformanceError(
        "commit blob claims are invalid"
      )
    try:
      content = subprocess.run(
        (
          "git",
          "show",
          f"{bootstrap_commit}:{path}",
        ),
        cwd=root,
        check=True,
        capture_output=True,
      ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
      raise BootstrapConformanceError(
        "commit blob cannot be resolved"
      ) from error
    if hashlib.sha256(content).hexdigest() != declared_digest:
      raise BootstrapConformanceError(
        "commit blob digest does not match"
      )
  return {
    "bootstrap_commit": bootstrap_commit,
    "evidence_count": len(commit_blob_map),
    "status": "complete",
  }
