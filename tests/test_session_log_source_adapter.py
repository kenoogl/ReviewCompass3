"""ClaudeとCodex 2形式の共通入力adapter契約。"""

import importlib
import json


def _write(path, records):
  path.write_text(
    "".join(json.dumps(record) + "\n" for record in records),
    encoding="utf-8",
  )


def test_dispatches_claude_and_two_codex_formats_through_one_entry(tmp_path):
  claude = tmp_path / "claude.jsonl"
  codex_exec = tmp_path / "codex-exec.jsonl"
  codex_rollout = tmp_path / "codex-rollout.jsonl"
  _write(claude, ({
    "uuid": "claude-user",
    "type": "user",
    "sessionId": "claude-session",
    "message": {"role": "user", "content": "Claude message."},
  },))
  _write(codex_exec, (
    {"type": "thread.started", "thread_id": "codex-thread"},
    {
      "type": "item.completed",
      "item": {
        "id": "codex-agent",
        "type": "agent_message",
        "text": "Codex exec message.",
      },
    },
  ))
  _write(codex_rollout, (
    {
      "timestamp": "2026-08-03T10:00:00Z",
      "type": "session_meta",
      "payload": {"id": "rollout-thread", "cwd": "/workspace"},
    },
    {
      "timestamp": "2026-08-03T10:00:01Z",
      "type": "response_item",
      "payload": {
        "id": "rollout-agent",
        "type": "message",
        "role": "assistant",
        "content": [
          {"type": "output_text", "text": "Codex rollout message."},
        ],
      },
    },
  ))
  adapter = importlib.import_module("tools.session_logs.source_adapter")

  results = tuple(
    adapter.parse_source_log(path)
    for path in (claude, codex_exec, codex_rollout)
  )

  assert tuple(result.source_kind for result in results) == (
    "claude",
    "codex_exec_json",
    "codex_rollout",
  )
  assert tuple(result.parsed.events[0].text for result in results) == (
    "Claude message.",
    "Codex exec message.",
    "Codex rollout message.",
  )


def test_common_entry_rejects_unidentified_input(tmp_path):
  raw_log = tmp_path / "unknown.jsonl"
  raw_log.write_text('{"type":"unknown"}\n', encoding="utf-8")
  adapter = importlib.import_module("tools.session_logs.source_adapter")

  try:
    adapter.parse_source_log(raw_log)
  except adapter.UnsupportedSourceKind as error:
    assert str(error) == "None"
  else:
    raise AssertionError("unknown source kind must be rejected")
