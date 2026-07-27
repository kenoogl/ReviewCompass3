"""セッションログ既知変異の独立検査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _claude_record(text):
  return {
    "uuid": "user-1",
    "type": "user",
    "sessionId": "session-1",
    "message": {
      "role": "user",
      "content": text,
    },
  }


def test_only_lf_delimits_jsonl_records_during_regeneration(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  text_with_separator = "before\u2028after"
  raw_log.write_text(
    json.dumps(
      _claude_record(text_with_separator),
      ensure_ascii=False,
    ) + "\n",
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
  assert text_with_separator in result.text


def test_only_lf_delimits_public_codex_jsonl_bytes():
  text_with_separator = "before\u2028after"
  records = (
    {"type": "thread.started", "thread_id": "thread-1"},
    {
      "type": "item.completed",
      "item": {
        "id": "agent-1",
        "type": "agent_message",
        "text": text_with_separator,
      },
    },
  )
  data = "".join(
    json.dumps(record, ensure_ascii=False) + "\n"
    for record in records
  ).encode("utf-8")
  parser = importlib.import_module("tools.session_logs.parse_codex")

  result = parser.parse_codex_bytes(data)

  assert len(result.events) == 1
  assert result.events[0].text == text_with_separator
  assert result.issues == ()


def test_independent_digest_detects_recorded_byte_mutation(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  original = (
    json.dumps(_claude_record("Original.")) + "\n"
  ).encode("utf-8")
  raw_log.write_bytes(original)
  provenance = importlib.import_module("tools.session_logs.provenance")
  record = provenance.build_provenance(
    raw_log,
    raw_root=raw_root,
    transcript_text="transcript",
    tool_version="0.0.1",
  )
  assert record.source_sha256 == hashlib.sha256(original).hexdigest()

  raw_log.write_bytes(original.replace(b"Original", b"Mutated!"))
  verification = provenance.verify_provenance(
    record,
    raw_log=raw_log,
    transcript_text="transcript",
  )

  assert verification.source_matches is False


def test_sensitive_and_non_append_mutations_fail_closed():
  redaction = importlib.import_module("tools.session_logs.redaction")
  secret = "B8gL3nR6yS1wU9qM4pD7tX2zJ5kF0cV"
  with pytest.raises(redaction.SensitiveDataRemaining) as error:
    redaction.redact_text_strict("token=%s" % secret, ())
  assert secret not in repr(error.value)

  updates = importlib.import_module("tools.session_logs.updates")
  update = updates.merge_append_only(
    ("event-1", "event-2"),
    ("event-1", "mutated-event", "event-2"),
  )
  assert update.action == "preserved"
  assert update.events == ("event-1", "event-2")
