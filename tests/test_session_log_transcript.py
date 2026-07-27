"""生セッションログ転写の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_renders_parsed_text_and_tool_events_deterministically(tmp_path):
  raw_log = tmp_path / "session.jsonl"
  records = (
    {
      "uuid": "user-1",
      "type": "user",
      "message": {
        "role": "user",
        "content": "Review this.",
      },
    },
    {
      "uuid": "assistant-1",
      "type": "assistant",
      "message": {
        "role": "assistant",
        "content": "One issue.",
      },
    },
    {
      "uuid": "assistant-2",
      "type": "assistant",
      "message": {
        "role": "assistant",
        "content": [
          {
            "type": "tool_use",
            "id": "tool-1",
            "name": "Read",
            "input": {
              "line": 2,
              "file_path": "README.md",
            },
          },
        ],
      },
    },
    {
      "uuid": "user-2",
      "type": "user",
      "message": {
        "role": "user",
        "content": [
          {
            "type": "tool_result",
            "tool_use_id": "tool-1",
            "content": "first\nmiddle\nlast",
            "is_error": True,
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
  transcript = importlib.import_module("tools.session_logs.transcript")

  result = parse_claude.parse_claude_log(raw_log)

  assert transcript.render_transcript(result) == (
    "## user\n\n"
    "Review this.\n\n"
    "## assistant\n\n"
    "One issue.\n\n"
    "## tool_call Read (tool-1)\n\n"
    "```json\n"
    "{\n"
    '  "file_path": "README.md",\n'
    '  "line": 2\n'
    "}\n"
    "```\n\n"
    "## tool_result tool-1 error\n\n"
    "first\nmiddle\nlast\n"
  )
