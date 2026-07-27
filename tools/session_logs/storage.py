"""セッションログ成果物の配置と追記専用保存。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import os
from pathlib import Path

from tools.session_logs.updates import merge_append_only


class StorageError(Exception):
  """成果物群の保存または復旧に失敗した。"""


@dataclasses.dataclass(frozen=True)
class StorageResult:
  action: str
  transcript_path: Path
  provenance_path: Path
  summary_path: object = None


def _event_fingerprint(event) -> str:
  payload = {
    "type": type(event).__name__,
    "value": dataclasses.asdict(event),
  }
  encoded = json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
  ).encode("utf-8")
  return hashlib.sha256(encoded).hexdigest()


def _state(artifact, fingerprints):
  return {
    "event_fingerprints": list(fingerprints),
    "provenance": dataclasses.asdict(artifact.provenance),
  }


def _state_bytes(artifact, fingerprints):
  return (
    json.dumps(
      _state(artifact, fingerprints),
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ) + "\n"
  ).encode("utf-8")


def _replace_file(source, target):
  os.replace(source, target)


def _commit_outputs(outputs):
  snapshots = {}
  temporary_paths = {}
  try:
    for path, data in outputs.items():
      path.parent.mkdir(parents=True, exist_ok=True)
      snapshots[path] = path.read_bytes() if path.exists() else None
      temporary_path = path.with_name(path.name + ".tmp")
      temporary_path.write_bytes(data)
      temporary_paths[path] = temporary_path
    for path, temporary_path in temporary_paths.items():
      _replace_file(temporary_path, path)
  except OSError as error:
    for path, snapshot in snapshots.items():
      if snapshot is None:
        path.unlink(missing_ok=True)
      else:
        path.write_bytes(snapshot)
    raise StorageError("Failed to commit session artifacts") from error
  finally:
    for temporary_path in temporary_paths.values():
      temporary_path.unlink(missing_ok=True)


def store_artifact(
  artifact,
  *,
  transcript_root,
  provenance_root,
  summary_root=None,
) -> StorageResult:
  source_path = Path(artifact.provenance.source_path)
  transcript_path = (
    Path(transcript_root) / source_path.with_suffix(".md")
  )
  provenance_path = (
    Path(provenance_root) / source_path.with_suffix(".json")
  )
  summary_path = (
    Path(summary_root) / source_path.with_suffix(".md")
    if summary_root is not None
    else None
  )
  fingerprints = tuple(
    _event_fingerprint(event)
    for event in artifact.events
  )

  transcript_exists = transcript_path.exists()
  provenance_exists = provenance_path.exists()
  summary_exists = summary_path is None or summary_path.exists()
  if (
    not transcript_exists
    and not provenance_exists
    and (summary_path is None or not summary_path.exists())
  ):
    outputs = {
      transcript_path: artifact.text.encode("utf-8"),
      provenance_path: _state_bytes(artifact, fingerprints),
    }
    if summary_path is not None:
      outputs[summary_path] = artifact.summary_text.encode("utf-8")
    _commit_outputs(outputs)
    return StorageResult(
      action="created",
      transcript_path=transcript_path,
      provenance_path=provenance_path,
      summary_path=summary_path,
    )

  if not transcript_exists or not provenance_exists or not summary_exists:
    return StorageResult(
      action="preserved",
      transcript_path=transcript_path,
      provenance_path=provenance_path,
      summary_path=summary_path,
    )

  try:
    existing_text = transcript_path.read_text(encoding="utf-8")
    existing_summary = (
      summary_path.read_text(encoding="utf-8")
      if summary_path is not None
      else None
    )
    existing_state = json.loads(
      provenance_path.read_text(encoding="utf-8")
    )
    existing_fingerprints = tuple(
      existing_state["event_fingerprints"]
    )
  except (OSError, ValueError, KeyError, TypeError):
    return StorageResult(
      action="preserved",
      transcript_path=transcript_path,
      provenance_path=provenance_path,
      summary_path=summary_path,
    )

  update = merge_append_only(existing_fingerprints, fingerprints)
  if update.action == "unchanged":
    transcript_matches = existing_text == artifact.text
    summary_matches = (
      summary_path is None
      or existing_summary == artifact.summary_text
    )
    action = (
      "unchanged"
      if transcript_matches and summary_matches
      else "preserved"
    )
  elif update.action == "updated" and artifact.text.startswith(existing_text):
    outputs = {
      transcript_path: artifact.text.encode("utf-8"),
      provenance_path: _state_bytes(artifact, fingerprints),
    }
    if summary_path is not None:
      outputs[summary_path] = artifact.summary_text.encode("utf-8")
    _commit_outputs(outputs)
    action = "updated"
  else:
    action = "preserved"

  return StorageResult(
    action=action,
    transcript_path=transcript_path,
    provenance_path=provenance_path,
    summary_path=summary_path,
  )
