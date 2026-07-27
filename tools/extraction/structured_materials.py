"""固定構造化材料の意味分類。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re

import yaml


_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40,64}")
_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclasses.dataclass(frozen=True, order=True)
class StructuredMaterial:
  identifier: str
  kind: str
  commit: str
  sha256: str


@dataclasses.dataclass(frozen=True, order=True)
class UnresolvedStructuredMaterial:
  identifier: str
  reason: str


@dataclasses.dataclass(frozen=True)
class StructuredMaterialClassification:
  status: str
  items: tuple
  unresolved: tuple
  digest: str


def _path(identifier):
  if not isinstance(identifier, str) or identifier.count(":") != 1:
    raise ValueError("structured identifier must use source:path")
  source, path = identifier.split(":", 1)
  if not source or not path:
    raise ValueError("structured identifier must use source:path")
  return path


def _parse(path, content):
  if path.endswith(".json"):
    return json.loads(content)
  if path.endswith((".yaml", ".yml")):
    return yaml.safe_load(content)
  raise ValueError("unsupported structured extension")


def _semantic_kind(path, value):
  if not isinstance(value, dict):
    return None
  keys = set(value)
  if (
    ("schemas/" in path or path.endswith(".schema.json"))
    and "$schema" in keys
    and ("properties" in keys or "$defs" in keys)
  ):
    return "schema"
  if "approved_by" in keys and (
    "approved_action" in keys
    or "decision" in keys
    or "approval_utterance" in keys
    or any(key.startswith("approved_") for key in keys)
  ):
    return "approval"
  if (
    ("/state/" in path or path.endswith("ledger.yaml"))
    and (
      "entries" in keys
      or "current" in keys
      or "stages" in keys
    )
  ):
    return "state"
  if (
    "/evidence/exchanges/" in path
    and (
      "response" in keys
      or "raw_response" in keys
      or "events" in keys
    )
  ):
    return "raw_response"
  if (
    "/reviews/" in path
    and "/raw/" in path
    and bool(keys & {"response", "raw_response", "events"})
  ):
    return "raw_response"
  if (
    "/evidence/reviews/" in path
    and (
      "verdict" in keys
      or "findings" in keys
      or "items" in keys
      or "results" in keys
    )
  ):
    return "generated_evidence"
  if "/reviews/" in path and (
    (
      "findings" in keys
      and bool(keys & {"model", "provider", "role"})
    )
    or "model_results" in keys
    or ("models" in keys and "run_id" in keys)
    or ("triage_status" in keys and "items" in keys)
    or (
      "run_id" in keys
      and "target_files" in keys
      and "roles" not in keys
    )
  ):
    return "generated_evidence"
  if (
    "/reviews/" in path
    and "schema_version" in keys
    and "roles" in keys
    and "target_files" in keys
  ):
    return "canonical_spec"
  if "/reviews/" in path and "schema_version" in keys:
    return "generated_evidence"
  if (
    ("/specs/" in path or path.startswith("specs/"))
    and ("schema_version" in keys or "version" in keys)
    and bool(keys & {
      "coverage",
      "units",
      "requirements",
      "features",
      "decisions",
      "records",
      "items",
    })
  ):
    return "canonical_spec"
  return None


def classify_structured_materials(documents, provenance):
  if (
    not isinstance(documents, dict)
    or not documents
    or not isinstance(provenance, dict)
    or set(documents) != set(provenance)
  ):
    raise ValueError("documents and provenance must match")
  items = []
  unresolved = []
  for identifier in sorted(documents):
    path = _path(identifier)
    content = documents[identifier]
    source = provenance[identifier]
    if (
      not isinstance(content, str)
      or not isinstance(source, dict)
      or set(source) != {"commit", "sha256"}
      or not isinstance(source["commit"], str)
      or _COMMIT_PATTERN.fullmatch(source["commit"]) is None
      or not isinstance(source["sha256"], str)
      or _DIGEST_PATTERN.fullmatch(source["sha256"]) is None
    ):
      raise ValueError("structured provenance is invalid")
    actual_digest = hashlib.sha256(content.encode()).hexdigest()
    if actual_digest != source["sha256"]:
      unresolved.append(UnresolvedStructuredMaterial(
        identifier,
        "stale_provenance",
      ))
      continue
    try:
      value = _parse(path, content)
    except (ValueError, json.JSONDecodeError, yaml.YAMLError):
      unresolved.append(UnresolvedStructuredMaterial(
        identifier,
        "parse_failure",
      ))
      continue
    kind = _semantic_kind(path, value)
    if kind is None:
      unresolved.append(UnresolvedStructuredMaterial(
        identifier,
        "unknown_semantic_shape",
      ))
      continue
    items.append(StructuredMaterial(
      identifier=identifier,
      kind=kind,
      commit=source["commit"],
      sha256=source["sha256"],
    ))
  ordered_items = tuple(sorted(items))
  ordered_unresolved = tuple(sorted(unresolved))
  document = {
    "items": [
      dataclasses.asdict(item) for item in ordered_items
    ],
    "schema_version": 1,
    "unresolved": [
      dataclasses.asdict(item)
      for item in ordered_unresolved
    ],
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return StructuredMaterialClassification(
    status="blocked" if ordered_unresolved else "complete",
    items=ordered_items,
    unresolved=ordered_unresolved,
    digest=digest,
  )
