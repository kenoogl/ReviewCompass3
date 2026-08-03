"""Codex Desktop／CLI内部rollout JSONLの解析。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
from pathlib import Path

from tools.session_logs.parse_claude import (
  Event,
  ParseError,
  ParseIssue,
  ParseResult,
  ToolCall,
  ToolResult,
)


_IGNORED_RECORD_TYPES = {
  "compacted",
  "event_msg",
  "session_meta",
  "turn_context",
  "world_state",
}
_IGNORED_ITEM_TYPES = {"reasoning"}
_MESSAGE_ROLES = {"assistant", "developer", "system", "user"}
_TEXT_BLOCK_TYPES = {"input_text", "output_text", "text"}
_TOOL_CALL_TYPES = {"custom_tool_call", "function_call"}
_TOOL_RESULT_TYPES = {
  "custom_tool_call_output",
  "function_call_output",
}


def _read_lines(path):
  raw_path = Path(path)
  try:
    with raw_path.open(encoding="utf-8") as raw_log:
      yield from raw_log
  except OSError as error:
    raise ParseError(
      "Cannot read Codex rollout JSONL stream: %s" % raw_path
    ) from error


def _json_text(value) -> str:
  if isinstance(value, str):
    return value
  if value is None:
    return ""
  return json.dumps(
    value,
    ensure_ascii=False,
    sort_keys=True,
  )


def _arguments(value):
  if not isinstance(value, str):
    return value
  try:
    return json.loads(value)
  except json.JSONDecodeError:
    return value


def _message_text(content, line_no, issues) -> str:
  if isinstance(content, str):
    return content
  if not isinstance(content, list):
    issues.append(ParseIssue(
      kind="incomplete_event",
      line_no=line_no,
      detail="invalid_message_content",
    ))
    return ""
  parts = []
  for block_index, block in enumerate(content):
    if not isinstance(block, dict):
      issues.append(ParseIssue(
        kind="incomplete_event",
        line_no=line_no,
        detail="invalid_message_block",
        block_index=block_index,
      ))
      continue
    block_type = block.get("type")
    if block_type not in _TEXT_BLOCK_TYPES:
      issues.append(ParseIssue(
        kind="unsupported_message_block",
        line_no=line_no,
        detail=str(block_type),
        block_index=block_index,
      ))
      continue
    text = block.get("text")
    if not isinstance(text, str):
      issues.append(ParseIssue(
        kind="incomplete_event",
        line_no=line_no,
        detail="missing_text",
        block_index=block_index,
      ))
      continue
    parts.append(text)
  return "\n".join(parts)


def _item_id(item, line_no, issues):
  item_id = item.get("id")
  if isinstance(item_id, str) and item_id:
    return item_id
  issues.append(ParseIssue(
    kind="incomplete_event",
    line_no=line_no,
    detail="missing_item_id",
  ))
  return None


def _parse_message(item, item_id, line_no, issues):
  role = item.get("role")
  if role not in _MESSAGE_ROLES:
    issues.append(ParseIssue(
      kind="unsupported_message_role",
      line_no=line_no,
      detail=str(role),
    ))
    return ()
  return (Event(
    event_id=item_id,
    role=role,
    text=_message_text(item.get("content"), line_no, issues),
    line_no=line_no,
  ),)


def _parse_tool_call(item, item_id, line_no, issues):
  call_id = item.get("call_id")
  name = item.get("name")
  if not isinstance(call_id, str) or not call_id:
    issues.append(ParseIssue(
      kind="incomplete_tool_event",
      line_no=line_no,
      detail="missing_call_id",
    ))
    return ()
  if not isinstance(name, str) or not name:
    issues.append(ParseIssue(
      kind="incomplete_tool_event",
      line_no=line_no,
      detail="missing_tool_name",
    ))
    return ()
  value = (
    item.get("arguments")
    if "arguments" in item
    else item.get("input")
  )
  return (ToolCall(
    event_id=item_id,
    call_id=call_id,
    name=name,
    arguments=_arguments(value),
    line_no=line_no,
    block_index=0,
  ),)


def _parse_tool_result(item, item_id, line_no, issues):
  call_id = item.get("call_id")
  if not isinstance(call_id, str) or not call_id:
    issues.append(ParseIssue(
      kind="incomplete_tool_event",
      line_no=line_no,
      detail="missing_call_id",
    ))
    return ()
  status = item.get("status")
  return (ToolResult(
    event_id=item_id,
    call_id=call_id,
    text=_json_text(item.get("output")),
    is_error=(
      status not in (None, "completed")
      or item.get("error") is not None
    ),
    line_no=line_no,
    block_index=0,
  ),)


def _parse_item(item, line_no, issues):
  if not isinstance(item, dict):
    issues.append(ParseIssue(
      kind="incomplete_event",
      line_no=line_no,
      detail="invalid_item",
    ))
    return ()
  item_id = _item_id(item, line_no, issues)
  if item_id is None:
    return ()
  item_type = item.get("type")
  if item_type == "message":
    return _parse_message(item, item_id, line_no, issues)
  if item_type in _TOOL_CALL_TYPES:
    return _parse_tool_call(item, item_id, line_no, issues)
  if item_type in _TOOL_RESULT_TYPES:
    return _parse_tool_result(item, item_id, line_no, issues)
  if item_type in _IGNORED_ITEM_TYPES:
    return ()
  issues.append(ParseIssue(
    kind="unsupported_item",
    line_no=line_no,
    detail=str(item_type),
  ))
  return ()


def _parse_lines(lines) -> ParseResult:
  events = []
  issues = []
  for line_no, line in enumerate(lines, start=1):
    if not line.strip():
      continue
    try:
      record = json.loads(line)
    except json.JSONDecodeError as error:
      issues.append(ParseIssue(
        kind="invalid_json",
        line_no=line_no,
        detail=error.msg,
      ))
      continue
    if not isinstance(record, dict):
      issues.append(ParseIssue(
        kind="unsupported_event",
        line_no=line_no,
        detail=type(record).__name__,
      ))
      continue
    record_type = record.get("type")
    if record_type == "response_item":
      events.extend(_parse_item(
        record.get("payload"),
        line_no,
        issues,
      ))
      continue
    if record_type in _IGNORED_RECORD_TYPES:
      continue
    issues.append(ParseIssue(
      kind="unsupported_event",
      line_no=line_no,
      detail=str(record_type),
    ))
  return ParseResult(events=tuple(events), issues=tuple(issues))


def parse_codex_rollout_bytes(data) -> ParseResult:
  return _parse_lines(data.decode("utf-8").split("\n"))


def parse_codex_rollout_log(path) -> ParseResult:
  return _parse_lines(_read_lines(path))
