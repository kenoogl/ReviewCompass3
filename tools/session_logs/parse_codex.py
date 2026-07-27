"""Codex exec公開JSONLストリームの解析。

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


def _read_lines(path):
  raw_path = Path(path)
  try:
    with raw_path.open(encoding="utf-8") as raw_log:
      yield from raw_log
  except OSError as error:
    raise ParseError(
      "Cannot read Codex JSONL stream: %s" % raw_path
    ) from error


def _output_text(value) -> str:
  if isinstance(value, str):
    return value
  if value is None:
    return ""
  return json.dumps(
    value,
    ensure_ascii=False,
    sort_keys=True,
  )


def _parse_item(record_type, item, line_no, issues) -> tuple:
  if not isinstance(item, dict):
    issues.append(ParseIssue(
      kind="incomplete_event",
      line_no=line_no,
      detail="invalid_item",
    ))
    return ()
  item_id = item.get("id")
  if not isinstance(item_id, str) or not item_id:
    issues.append(ParseIssue(
      kind="incomplete_event",
      line_no=line_no,
      detail="missing_item_id",
    ))
    return ()
  item_type = item.get("type")

  if (
    record_type == "item.completed"
    and item_type in ("user_message", "agent_message")
  ):
    text = item.get("text")
    if not isinstance(text, str):
      issues.append(ParseIssue(
        kind="incomplete_event",
        line_no=line_no,
        detail="missing_text",
      ))
      return ()
    return (Event(
      event_id=item_id,
      role="user" if item_type == "user_message" else "assistant",
      text=text,
      line_no=line_no,
    ),)

  if (
    record_type == "item.started"
    and item_type == "command_execution"
  ):
    return (ToolCall(
      event_id=item_id,
      call_id=item_id,
      name="command_execution",
      arguments={"command": item.get("command", "")},
      line_no=line_no,
      block_index=0,
    ),)

  if (
    record_type == "item.completed"
    and item_type == "command_execution"
  ):
    exit_code = item.get("exit_code")
    return (ToolResult(
      event_id=item_id,
      call_id=item_id,
      text=_output_text(
        item.get("aggregated_output", item.get("output"))
      ),
      is_error=(
        item.get("status") not in (None, "completed")
        or (
          isinstance(exit_code, int)
          and exit_code != 0
        )
      ),
      line_no=line_no,
      block_index=0,
    ),)

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
    if record_type in (
      "thread.started",
      "turn.started",
      "turn.completed",
      "turn.failed",
    ):
      continue
    if record_type in ("item.started", "item.completed"):
      events.extend(_parse_item(
        record_type,
        record.get("item"),
        line_no,
        issues,
      ))
      continue
    issues.append(ParseIssue(
      kind="unsupported_event",
      line_no=line_no,
      detail=str(record_type),
    ))
  return ParseResult(events=tuple(events), issues=tuple(issues))


def parse_codex_bytes(data) -> ParseResult:
  return _parse_lines(
    data.decode("utf-8").splitlines(keepends=True)
  )


def parse_codex_log(path) -> ParseResult:
  return _parse_lines(_read_lines(path))
