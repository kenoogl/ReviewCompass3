"""リポジトリ外の明示ログを値なしで検証するハーネス。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
import os
import subprocess
from pathlib import Path

from tools.session_logs.discovery import discover_raw_logs
from tools.session_logs.pipeline import (
  UnsupportedSourceKind,
  prepare_artifact,
)


class PrivateValidationError(Exception):
  """私的ログを安全な境界で検証できない。"""


@dataclasses.dataclass(frozen=True)
class PrivateValidationResult:
  status: str
  counts: dict
  git_unchanged: bool
  evidence_path: Path


def _within(path, root):
  resolved_path = Path(path).resolve()
  resolved_root = Path(root).resolve()
  return (
    resolved_path == resolved_root
    or resolved_root in resolved_path.parents
  )


def _validate_boundaries(raw_root, repository_root, evidence_path):
  repository = Path(repository_root).resolve()
  raw = Path(raw_root).resolve()
  evidence = Path(evidence_path).resolve()
  if (
    not (repository / ".git").exists()
    or _within(raw, repository)
    or _within(evidence, repository)
  ):
    raise PrivateValidationError(
      "Unsafe private validation boundary"
    )
  return raw, repository, evidence


def _git_status(repository_root, runner):
  try:
    result = runner(
      [
        "git",
        "-C",
        str(repository_root),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
      ],
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise PrivateValidationError(
      "Cannot inspect repository state"
    ) from error
  if result.returncode != 0:
    raise PrivateValidationError(
      "Cannot inspect repository state"
    )
  return result.stdout


def _write_evidence(path, payload):
  temporary_path = path.with_name(path.name + ".tmp")
  try:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
      ) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, path)
  except OSError as error:
    raise PrivateValidationError(
      "Cannot write private validation evidence"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)


def validate_private_logs(
  raw_root,
  *,
  repository_root,
  evidence_path,
  rules,
  tool_version,
  allow_patterns=(),
  runner=subprocess.run,
) -> PrivateValidationResult:
  raw, repository, evidence = _validate_boundaries(
    raw_root,
    repository_root,
    evidence_path,
  )
  before = _git_status(repository, runner)
  try:
    relative_paths = discover_raw_logs(raw)
  except Exception as error:
    raise PrivateValidationError(
      "Cannot discover private logs"
    ) from error
  counts = {
    "claude": 0,
    "codex": 0,
    "failed": 0,
    "unsupported": 0,
  }
  for relative_path in relative_paths:
    try:
      artifact = prepare_artifact(
        raw / relative_path,
        raw_root=raw,
        rules=rules,
        tool_version=tool_version,
        allow_patterns=allow_patterns,
      )
    except UnsupportedSourceKind:
      counts["unsupported"] += 1
    except Exception:
      counts["failed"] += 1
    else:
      counts[artifact.source_kind] += 1
  after = _git_status(repository, runner)
  git_unchanged = before == after
  if not git_unchanged:
    status = "repository_changed"
  elif counts["failed"] or counts["unsupported"]:
    status = "failed"
  elif not relative_paths:
    status = "no_targets"
  else:
    status = "passed"
  payload = {
    "counts": counts,
    "git_unchanged": git_unchanged,
    "status": status,
  }
  _write_evidence(evidence, payload)
  return PrivateValidationResult(
    status=status,
    counts=counts,
    git_unchanged=git_unchanged,
    evidence_path=evidence,
  )
