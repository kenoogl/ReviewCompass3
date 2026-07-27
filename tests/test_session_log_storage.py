"""セッションログ成果物保存の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def _record(event_id, role, text):
  return {
    "uuid": event_id,
    "type": role,
    "sessionId": "session-1",
    "message": {
      "role": role,
      "content": text,
    },
  }


def _write_records(path, records):
  path.write_text(
    "".join(json.dumps(record) + "\n" for record in records),
    encoding="utf-8",
  )


def test_stores_idempotently_appends_and_preserves_on_change(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  transcript_root = tmp_path / "transcripts"
  provenance_root = tmp_path / "provenance"

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  storage = importlib.import_module("tools.session_logs.storage")

  first_records = (
    _record("user-1", "user", "First."),
  )
  _write_records(raw_log, first_records)
  first_artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )

  created = storage.store_artifact(
    first_artifact,
    transcript_root=transcript_root,
    provenance_root=provenance_root,
  )
  repeated = storage.store_artifact(
    first_artifact,
    transcript_root=transcript_root,
    provenance_root=provenance_root,
  )

  assert created.action == "created"
  assert repeated.action == "unchanged"
  assert created.transcript_path == (
    transcript_root / "nested" / "session.md"
  )
  assert created.provenance_path == (
    provenance_root / "nested" / "session.json"
  )
  assert created.transcript_path.read_text(encoding="utf-8") == (
    first_artifact.text
  )
  state = json.loads(created.provenance_path.read_text(encoding="utf-8"))
  assert state["provenance"]["source_path"] == "nested/session.jsonl"
  assert len(state["event_fingerprints"]) == 1

  appended_records = first_records + (
    _record("assistant-1", "assistant", "Second."),
  )
  _write_records(raw_log, appended_records)
  appended_artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  updated = storage.store_artifact(
    appended_artifact,
    transcript_root=transcript_root,
    provenance_root=provenance_root,
  )

  assert updated.action == "updated"
  assert updated.transcript_path.read_text(encoding="utf-8") == (
    appended_artifact.text
  )
  assert appended_artifact.text.startswith(first_artifact.text)

  changed_records = (
    _record("user-1", "user", "Changed first event."),
    appended_records[1],
  )
  _write_records(raw_log, changed_records)
  changed_artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  preserved = storage.store_artifact(
    changed_artifact,
    transcript_root=transcript_root,
    provenance_root=provenance_root,
  )

  assert preserved.action == "preserved"
  assert preserved.transcript_path.read_text(encoding="utf-8") == (
    appended_artifact.text
  )
