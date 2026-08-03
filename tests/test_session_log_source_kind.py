"""生セッションログ種別識別の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_identifies_claude_log_from_first_event(tmp_path):
  raw_log = tmp_path / "session.jsonl"
  raw_log.write_text(
    json.dumps({
      "uuid": "event-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "hello",
      },
    }) + "\n",
    encoding="utf-8",
  )

  source_kind = importlib.import_module("tools.session_logs.source_kind")

  assert source_kind.identify_source_kind(raw_log) == "claude"


def test_returns_none_for_unidentified_log(tmp_path):
  raw_log = tmp_path / "unknown.jsonl"
  raw_log.write_text('{"record": "unsupported"}\n', encoding="utf-8")

  source_kind = importlib.import_module("tools.session_logs.source_kind")

  assert source_kind.identify_source_kind(raw_log) is None


def test_identifies_public_codex_exec_json_stream(tmp_path):
  raw_log = tmp_path / "codex.jsonl"
  raw_log.write_text(
    json.dumps({
      "type": "thread.started",
      "thread_id": "0199a213-81c0-7800-8aa1-bbab2a035a53",
    }) + "\n",
    encoding="utf-8",
  )

  source_kind = importlib.import_module("tools.session_logs.source_kind")

  assert source_kind.identify_source_kind(raw_log) == "codex_exec_json"


def test_identifies_codex_rollout_stream(tmp_path):
  raw_log = tmp_path / "rollout.jsonl"
  raw_log.write_text(
    json.dumps({
      "timestamp": "2026-08-03T10:00:00Z",
      "type": "session_meta",
      "payload": {
        "id": "019fc541-2734-79b1-b3d9-3e12665d79f5",
        "cwd": "/workspace/project",
        "originator": "Codex Desktop",
      },
    }) + "\n",
    encoding="utf-8",
  )

  source_kind = importlib.import_module("tools.session_logs.source_kind")

  assert source_kind.identify_source_kind(raw_log) == "codex_rollout"
