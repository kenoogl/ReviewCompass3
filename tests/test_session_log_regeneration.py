"""セッションログ転写再生成の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import re

import pytest

def _event(event_id, text):
  return json.dumps({
    "uuid": event_id,
    "type": "user",
    "sessionId": "session-1",
    "message": {
      "role": "user",
      "content": text,
    },
  }) + "\n"


def test_regenerates_only_recorded_range_and_compares_saved_transcript(
  tmp_path,
):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  raw_log.write_text(_event("user-1", "Original."), encoding="utf-8")

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  with raw_log.open("a", encoding="utf-8") as output:
    output.write(_event("user-2", "Appended later."))

  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )
  result = regeneration.regenerate_transcript(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    rules=(),
  )

  assert result == regeneration.RegenerationResult(
    text=artifact.text,
    source_matches=True,
    provenance_matches=True,
    stored_matches=True,
  )

  changed_saved = regeneration.regenerate_transcript(
    artifact.provenance,
    raw_root=raw_root,
    stored_text="## user\n\nChanged after storage.\n",
    rules=(),
  )
  assert changed_saved.provenance_matches is True
  assert changed_saved.stored_matches is False


def test_regeneration_detects_recorded_source_change(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  raw_log.write_text(_event("user-1", "Original."), encoding="utf-8")

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  raw_log.write_text(_event("user-1", "Changed."), encoding="utf-8")

  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )
  result = regeneration.regenerate_transcript(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    rules=(),
  )

  assert result.source_matches is False
  assert result.provenance_matches is False
  assert result.stored_matches is False


def test_regeneration_distinguishes_rule_and_tool_version_changes(
  tmp_path,
):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  raw_log.write_text(_event("user-1", "Original."), encoding="utf-8")
  pipeline = importlib.import_module("tools.session_logs.pipeline")
  redaction = importlib.import_module("tools.session_logs.redaction")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )

  assert artifact.provenance.redaction_rules_sha256 == (
    redaction.redaction_rules_digest((), allow_patterns=())
  )

  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )
  result = regeneration.regenerate_transcript(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    rules=(),
    allow_patterns=(r"documented-safe-value",),
    tool_version="0.0.2",
  )

  assert result.source_matches is True
  assert result.rules_match is False
  assert result.tool_version_matches is False
  assert result.status == "conditions_changed"


def test_regeneration_failure_diagnostic_does_not_include_value(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  secret = "B8gL3nR6yS1wU9qM4pD7tX2zJ5kF0cV"
  raw_log.write_text(
    _event("user-1", "token=%s" % secret),
    encoding="utf-8",
  )
  pipeline = importlib.import_module("tools.session_logs.pipeline")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    allow_patterns=(re.escape(secret),),
    tool_version="0.0.1",
  )
  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )

  with pytest.raises(regeneration.RegenerationError) as error:
    regeneration.regenerate_transcript(
      artifact.provenance,
      raw_root=raw_root,
      stored_text=artifact.text,
      rules=(),
      tool_version="0.0.1",
    )

  assert error.value.reason == "SensitiveDataRemaining"
  assert secret not in repr(error.value)


def test_regenerates_public_codex_json_stream(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "codex.jsonl"
  raw_root.mkdir()
  records = (
    {
      "type": "thread.started",
      "thread_id": "thread-1",
    },
    {
      "type": "item.completed",
      "item": {
        "id": "item-agent",
        "type": "agent_message",
        "text": "Done.",
      },
    },
  )
  raw_log.write_text(
    "".join(json.dumps(record) + "\n" for record in records),
    encoding="utf-8",
  )
  pipeline = importlib.import_module("tools.session_logs.pipeline")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
  )
  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )

  result = regeneration.regenerate_transcript(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    rules=(),
    tool_version="0.0.1",
  )

  assert result.status == "matches"
  assert result.text == artifact.text


def test_regenerates_summary_and_detects_summary_only_change(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  raw_log.write_text(_event("user-1", "Original."), encoding="utf-8")
  pipeline = importlib.import_module("tools.session_logs.pipeline")
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(),
    tool_version="0.0.1",
    commits=("abc1234 Add summary verification",),
    changed_files=("z.py", "a.py"),
  )
  regeneration = importlib.import_module(
    "tools.session_logs.regeneration"
  )

  matched = regeneration.regenerate_artifact(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    stored_summary=artifact.summary_text,
    rules=(),
    tool_version="0.0.1",
  )
  changed = regeneration.regenerate_artifact(
    artifact.provenance,
    raw_root=raw_root,
    stored_text=artifact.text,
    stored_summary="# altered summary\n",
    rules=(),
    tool_version="0.0.1",
  )

  assert matched.status == "matches"
  assert matched.summary_text == artifact.summary_text
  assert matched.summary_provenance_matches is True
  assert matched.summary_stored_matches is True
  assert changed.status == "summary_changed"
  assert changed.provenance_matches is True
  assert changed.stored_matches is True
  assert changed.summary_provenance_matches is True
  assert changed.summary_stored_matches is False
