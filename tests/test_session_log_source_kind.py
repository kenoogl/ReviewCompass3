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
