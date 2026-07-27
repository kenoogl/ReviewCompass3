"""Codex公開JSONLストリーム解析の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_parses_messages_and_command_execution_as_common_events(tmp_path):
  raw_log = tmp_path / "codex.jsonl"
  records = (
    {
      "type": "thread.started",
      "thread_id": "thread-1",
    },
    {
      "type": "item.completed",
      "item": {
        "id": "item-user",
        "type": "user_message",
        "text": "Review this change.",
      },
    },
    {
      "type": "item.completed",
      "item": {
        "id": "item-agent",
        "type": "agent_message",
        "text": "I will inspect it.",
      },
    },
    {
      "type": "item.started",
      "item": {
        "id": "item-command",
        "type": "command_execution",
        "command": "git status --short",
        "status": "in_progress",
      },
    },
    {
      "type": "item.completed",
      "item": {
        "id": "item-command",
        "type": "command_execution",
        "command": "git status --short",
        "aggregated_output": " M app.py\n",
        "exit_code": 0,
        "status": "completed",
      },
    },
  )
  raw_log.write_text(
    "".join(json.dumps(record) + "\n" for record in records),
    encoding="utf-8",
  )
  parse_codex = importlib.import_module("tools.session_logs.parse_codex")
  common = importlib.import_module("tools.session_logs.parse_claude")

  result = parse_codex.parse_codex_log(raw_log)

  assert result.events == (
    common.Event(
      event_id="item-user",
      role="user",
      text="Review this change.",
      line_no=2,
    ),
    common.Event(
      event_id="item-agent",
      role="assistant",
      text="I will inspect it.",
      line_no=3,
    ),
    common.ToolCall(
      event_id="item-command",
      call_id="item-command",
      name="command_execution",
      arguments={"command": "git status --short"},
      line_no=4,
      block_index=0,
    ),
    common.ToolResult(
      event_id="item-command",
      call_id="item-command",
      text=" M app.py\n",
      is_error=False,
      line_no=5,
      block_index=0,
    ),
  )
  assert result.issues == ()
