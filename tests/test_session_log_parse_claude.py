"""Claude生セッションログ解析の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_parses_user_and_assistant_text_as_ordered_events(tmp_path):
  raw_log = tmp_path / "session.jsonl"
  records = (
    {
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "Review this change.",
      },
    },
    {
      "uuid": "assistant-1",
      "type": "assistant",
      "sessionId": "session-1",
      "message": {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "I found one issue.",
          },
        ],
      },
    },
  )
  raw_log.write_text(
    "".join(json.dumps(record) + "\n" for record in records),
    encoding="utf-8",
  )

  parse_claude = importlib.import_module("tools.session_logs.parse_claude")

  assert parse_claude.parse_claude_events(raw_log) == (
    parse_claude.Event(
      event_id="user-1",
      role="user",
      text="Review this change.",
      line_no=1,
    ),
    parse_claude.Event(
      event_id="assistant-1",
      role="assistant",
      text="I found one issue.",
      line_no=2,
    ),
  )


def test_reports_invalid_json_and_unsupported_events_while_skipping_empty_lines(
  tmp_path,
):
  raw_log = tmp_path / "session.jsonl"
  unsupported = {
    "uuid": "progress-1",
    "type": "progress",
    "sessionId": "session-1",
  }
  user = {
    "uuid": "user-1",
    "type": "user",
    "sessionId": "session-1",
    "message": {
      "role": "user",
      "content": "Continue.",
    },
  }
  raw_log.write_text(
    "\n"
    "not-json\n"
    + json.dumps(unsupported)
    + "\n"
    + json.dumps(user)
    + "\n",
    encoding="utf-8",
  )

  parse_claude = importlib.import_module("tools.session_logs.parse_claude")

  result = parse_claude.parse_claude_log(raw_log)

  assert result.events == (
    parse_claude.Event(
      event_id="user-1",
      role="user",
      text="Continue.",
      line_no=4,
    ),
  )
  assert tuple((issue.kind, issue.line_no) for issue in result.issues) == (
    ("invalid_json", 2),
    ("unsupported_event", 3),
  )
  assert result.issues[0].detail
  assert result.issues[1].detail == "progress"
