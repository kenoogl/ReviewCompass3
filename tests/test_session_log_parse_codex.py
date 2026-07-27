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


def test_parses_mcp_file_web_and_todo_items_as_common_events(tmp_path):
  raw_log = tmp_path / "codex.jsonl"
  records = (
    {"type": "thread.started", "thread_id": "thread-1"},
    {
      "type": "item.started",
      "item": {
        "id": "mcp-1",
        "type": "mcp_tool_call",
        "server": "docs",
        "tool": "search",
        "arguments": {"query": "hooks"},
        "status": "in_progress",
      },
    },
    {
      "type": "item.completed",
      "item": {
        "id": "mcp-1",
        "type": "mcp_tool_call",
        "server": "docs",
        "tool": "search",
        "arguments": {"query": "hooks"},
        "result": {
          "content": [{"type": "text", "text": "found"}],
          "structured_content": None,
        },
        "error": None,
        "status": "completed",
      },
    },
    {
      "type": "item.completed",
      "item": {
        "id": "file-1",
        "type": "file_change",
        "changes": [{"path": "app.py", "kind": "update"}],
        "status": "completed",
      },
    },
    {
      "type": "item.started",
      "item": {
        "id": "web-1",
        "type": "web_search",
        "query": "official docs",
        "action": {"type": "search"},
      },
    },
    {
      "type": "item.completed",
      "item": {
        "id": "web-1",
        "type": "web_search",
        "query": "official docs",
        "action": {"type": "search"},
      },
    },
    {
      "type": "item.updated",
      "item": {
        "id": "todo-1",
        "type": "todo_list",
        "items": [
          {"text": "Inspect", "completed": True},
          {"text": "Test", "completed": False},
        ],
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

  assert tuple(type(event) for event in result.events) == (
    common.ToolCall,
    common.ToolResult,
    common.ToolCall,
    common.ToolResult,
    common.ToolCall,
    common.ToolResult,
    common.Event,
  )
  assert result.events[0].name == "mcp:docs/search"
  assert result.events[0].arguments == {"query": "hooks"}
  assert result.events[1].is_error is False
  assert '"text": "found"' in result.events[1].text
  assert result.events[2].name == "file_change"
  assert result.events[2].arguments == {
    "changes": [{"path": "app.py", "kind": "update"}],
  }
  assert result.events[4].name == "web_search"
  assert result.events[4].arguments["query"] == "official docs"
  assert result.events[6] == common.Event(
    event_id="todo-1",
    role="plan",
    text="[x] Inspect\n[ ] Test",
    line_no=7,
  )
  assert result.issues == ()
