"""Codex Desktop／CLI内部rollout JSONL解析の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def _write_records(path, records):
  path.write_text(
    "".join(
      json.dumps(record, ensure_ascii=False) + "\n"
      for record in records
    ),
    encoding="utf-8",
  )


def test_parses_rollout_messages_and_complete_tool_payloads(tmp_path):
  raw_log = tmp_path / "rollout.jsonl"
  complete_output = "\n".join(
    "tool output line %02d" % number
    for number in range(1, 46)
  )
  records = (
    {
      "timestamp": "2026-08-03T10:00:00Z",
      "type": "session_meta",
      "payload": {
        "id": "thread-1",
        "cwd": "/workspace/project",
        "originator": "Codex Desktop",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:01Z",
      "type": "turn_context",
      "payload": {"turn_id": "turn-1"},
    },
    {
      "timestamp": "2026-08-03T10:00:02Z",
      "type": "response_item",
      "payload": {
        "id": "message-user",
        "type": "message",
        "role": "user",
        "content": [
          {"type": "input_text", "text": "利用者の逐語記録。"},
        ],
      },
    },
    {
      "timestamp": "2026-08-03T10:00:03Z",
      "type": "response_item",
      "payload": {
        "id": "message-developer",
        "type": "message",
        "role": "developer",
        "content": [
          {"type": "input_text", "text": "適用された開発指示。"},
        ],
      },
    },
    {
      "timestamp": "2026-08-03T10:00:04Z",
      "type": "response_item",
      "payload": {
        "id": "message-assistant",
        "type": "message",
        "role": "assistant",
        "content": [
          {"type": "output_text", "text": "アシスタントの逐語記録。"},
        ],
      },
    },
    {
      "timestamp": "2026-08-03T10:00:05Z",
      "type": "response_item",
      "payload": {
        "id": "custom-call",
        "type": "custom_tool_call",
        "call_id": "call-custom",
        "name": "functions.exec",
        "input": {"cmd": "safe command"},
      },
    },
    {
      "timestamp": "2026-08-03T10:00:06Z",
      "type": "response_item",
      "payload": {
        "id": "custom-output",
        "type": "custom_tool_call_output",
        "call_id": "call-custom",
        "output": complete_output,
        "status": "completed",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:07Z",
      "type": "response_item",
      "payload": {
        "id": "function-call",
        "type": "function_call",
        "call_id": "call-function",
        "name": "lookup",
        "arguments": "{\"query\": \"full value\"}",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:08Z",
      "type": "response_item",
      "payload": {
        "id": "function-output",
        "type": "function_call_output",
        "call_id": "call-function",
        "output": {"result": "full result"},
      },
    },
    {
      "timestamp": "2026-08-03T10:00:09Z",
      "type": "response_item",
      "payload": {
        "id": "reasoning-1",
        "type": "reasoning",
        "encrypted_content": "not-conversation-content",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:10Z",
      "type": "event_msg",
      "payload": {
        "type": "agent_message",
        "message": "response_itemのecho",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:11Z",
      "type": "compacted",
      "payload": {"window_id": "window-1"},
    },
  )
  _write_records(raw_log, records)
  parser = importlib.import_module(
    "tools.session_logs.parse_codex_rollout"
  )
  common = importlib.import_module("tools.session_logs.parse_claude")

  result = parser.parse_codex_rollout_log(raw_log)

  assert result.events == (
    common.Event(
      event_id="message-user",
      role="user",
      text="利用者の逐語記録。",
      line_no=3,
    ),
    common.Event(
      event_id="message-developer",
      role="developer",
      text="適用された開発指示。",
      line_no=4,
    ),
    common.Event(
      event_id="message-assistant",
      role="assistant",
      text="アシスタントの逐語記録。",
      line_no=5,
    ),
    common.ToolCall(
      event_id="custom-call",
      call_id="call-custom",
      name="functions.exec",
      arguments={"cmd": "safe command"},
      line_no=6,
      block_index=0,
    ),
    common.ToolResult(
      event_id="custom-output",
      call_id="call-custom",
      text=complete_output,
      is_error=False,
      line_no=7,
      block_index=0,
    ),
    common.ToolCall(
      event_id="function-call",
      call_id="call-function",
      name="lookup",
      arguments={"query": "full value"},
      line_no=8,
      block_index=0,
    ),
    common.ToolResult(
      event_id="function-output",
      call_id="call-function",
      text='{"result": "full result"}',
      is_error=False,
      line_no=9,
      block_index=0,
    ),
  )
  assert complete_output in result.events[4].text
  assert "tool output line 23" in result.events[4].text
  assert result.issues == ()


def test_parses_inter_agent_messages_and_tool_search_records(tmp_path):
  raw_log = tmp_path / "rollout.jsonl"
  discovered_tools = [
    {
      "description": "検索用の道具群。",
      "name": "project-tools",
      "tools": [
        {
          "description": "案件内を検索する。",
          "name": "search_project",
          "parameters": {
            "properties": {
              "query": {"type": "string"},
            },
            "required": ["query"],
            "type": "object",
          },
          "strict": True,
          "type": "function",
        },
      ],
      "type": "namespace",
    },
  ]
  _write_records(raw_log, (
    {
      "timestamp": "2026-08-10T10:00:00Z",
      "type": "session_meta",
      "payload": {"id": "thread-1", "cwd": "/workspace/project"},
    },
    {
      "timestamp": "2026-08-10T10:00:01Z",
      "type": "inter_agent_communication_metadata",
      "payload": {"trigger_turn": True},
    },
    {
      "timestamp": "2026-08-10T10:00:02Z",
      "type": "response_item",
      "payload": {
        "author": "/root/reviewer",
        "content": [
          {"type": "input_text", "text": "検査結果を共有します。"},
          {
            "type": "encrypted_content",
            "text": "逐語記録へ出してはならない内部値",
          },
        ],
        "id": "agent-message-1",
        "internal_chat_message_metadata_passthrough": {
          "turn_id": "turn-1",
        },
        "recipient": "/root",
        "type": "agent_message",
      },
    },
    {
      "timestamp": "2026-08-10T10:00:03Z",
      "type": "response_item",
      "payload": {
        "arguments": {"query": "対象を探す"},
        "call_id": "call-search-1",
        "execution": "client",
        "id": "tool-search-call-1",
        "status": "completed",
        "type": "tool_search_call",
      },
    },
    {
      "timestamp": "2026-08-10T10:00:04Z",
      "type": "response_item",
      "payload": {
        "call_id": "call-search-1",
        "execution": "client",
        "id": "tool-search-output-1",
        "status": "completed",
        "tools": discovered_tools,
        "type": "tool_search_output",
      },
    },
  ))
  parser = importlib.import_module(
    "tools.session_logs.parse_codex_rollout"
  )
  common = importlib.import_module("tools.session_logs.parse_claude")

  result = parser.parse_codex_rollout_log(raw_log)

  assert result.events == (
    common.Event(
      event_id="agent-message-1",
      role="agent",
      text=(
        "author: /root/reviewer\n"
        "recipient: /root\n\n"
        "検査結果を共有します。"
      ),
      line_no=3,
    ),
    common.ToolCall(
      event_id="tool-search-call-1",
      call_id="call-search-1",
      name="tool_search",
      arguments={"query": "対象を探す"},
      line_no=4,
      block_index=0,
    ),
    common.ToolResult(
      event_id="tool-search-output-1",
      call_id="call-search-1",
      text=json.dumps(
        discovered_tools,
        ensure_ascii=False,
        sort_keys=True,
      ),
      is_error=False,
      line_no=5,
      block_index=0,
    ),
  )
  assert result.issues == ()
  assert "内部値" not in result.events[0].text


def test_reports_unknown_rollout_records_without_guessing(tmp_path):
  raw_log = tmp_path / "rollout.jsonl"
  _write_records(raw_log, (
    {
      "timestamp": "2026-08-03T10:00:00Z",
      "type": "session_meta",
      "payload": {"id": "thread-1", "cwd": "/workspace/project"},
    },
    {
      "timestamp": "2026-08-03T10:00:01Z",
      "type": "response_item",
      "payload": {"id": "future-1", "type": "future_item"},
    },
    {
      "timestamp": "2026-08-03T10:00:02Z",
      "type": "future_outer",
      "payload": {},
    },
  ))
  parser = importlib.import_module(
    "tools.session_logs.parse_codex_rollout"
  )

  result = parser.parse_codex_rollout_log(raw_log)

  assert result.events == ()
  assert tuple(
    (issue.kind, issue.line_no, issue.detail)
    for issue in result.issues
  ) == (
    ("unsupported_item", 2, "future_item"),
    ("unsupported_event", 3, "future_outer"),
  )
