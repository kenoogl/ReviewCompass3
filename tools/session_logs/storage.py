"""セッションログ成果物の配置と追記専用保存。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path

from tools.session_logs.updates import merge_append_only


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


def _write_state(path, artifact, fingerprints):
  path.write_text(
    json.dumps(
      _state(artifact, fingerprints),
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ) + "\n",
    encoding="utf-8",
  )


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
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    if summary_path is not None:
      summary_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(artifact.text, encoding="utf-8")
    if summary_path is not None:
      summary_path.write_text(artifact.summary_text, encoding="utf-8")
    _write_state(provenance_path, artifact, fingerprints)
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
    with transcript_path.open("a", encoding="utf-8") as transcript_file:
      transcript_file.write(artifact.text[len(existing_text):])
    if summary_path is not None:
      summary_path.write_text(artifact.summary_text, encoding="utf-8")
    _write_state(provenance_path, artifact, fingerprints)
    action = "updated"
  else:
    action = "preserved"

  return StorageResult(
    action=action,
    transcript_path=transcript_path,
    provenance_path=provenance_path,
    summary_path=summary_path,
  )
