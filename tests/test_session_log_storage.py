"""セッションログ成果物保存の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


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
  summary_root = tmp_path / "summaries"
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
    summary_root=summary_root,
    provenance_root=provenance_root,
  )
  repeated = storage.store_artifact(
    first_artifact,
    transcript_root=transcript_root,
    summary_root=summary_root,
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
  assert created.summary_path == (
    summary_root / "nested" / "session.md"
  )
  assert created.transcript_path.read_text(encoding="utf-8") == (
    first_artifact.text
  )
  assert created.summary_path.read_text(encoding="utf-8") == (
    first_artifact.summary_text
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
    summary_root=summary_root,
    provenance_root=provenance_root,
  )

  assert updated.action == "updated"
  assert updated.transcript_path.read_text(encoding="utf-8") == (
    appended_artifact.text
  )
  assert updated.summary_path.read_text(encoding="utf-8") == (
    appended_artifact.summary_text
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
    summary_root=summary_root,
    provenance_root=provenance_root,
  )

  assert preserved.action == "preserved"
  assert preserved.transcript_path.read_text(encoding="utf-8") == (
    appended_artifact.text
  )
  assert preserved.summary_path.read_text(encoding="utf-8") == (
    appended_artifact.summary_text
  )


def test_restores_all_artifacts_when_atomic_replace_fails(tmp_path, monkeypatch):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  transcript_root = tmp_path / "transcripts"
  summary_root = tmp_path / "summaries"
  provenance_root = tmp_path / "provenance"

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  storage = importlib.import_module("tools.session_logs.storage")

  _write_records(raw_log, (_record("user-1", "user", "First."),))
  first_artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  stored = storage.store_artifact(
    first_artifact,
    transcript_root=transcript_root,
    summary_root=summary_root,
    provenance_root=provenance_root,
  )
  before = {
    path: path.read_bytes()
    for path in (
      stored.transcript_path,
      stored.summary_path,
      stored.provenance_path,
    )
  }

  _write_records(raw_log, (
    _record("user-1", "user", "First."),
    _record("assistant-1", "assistant", "Second."),
  ))
  appended_artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )

  original_replace = storage._replace_file
  calls = {"count": 0}

  def fail_second_replace(source, target):
    calls["count"] += 1
    if calls["count"] == 2:
      raise OSError("injected replace failure")
    original_replace(source, target)

  monkeypatch.setattr(storage, "_replace_file", fail_second_replace)

  with pytest.raises(storage.StorageError):
    storage.store_artifact(
      appended_artifact,
      transcript_root=transcript_root,
      summary_root=summary_root,
      provenance_root=provenance_root,
    )

  assert {path: path.read_bytes() for path in before} == before
  assert tuple(tmp_path.rglob("*.tmp")) == ()
