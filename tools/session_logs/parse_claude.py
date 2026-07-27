"""Claude生セッションログの解析。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
from pathlib import Path


class ParseError(Exception):
  """生ログを読み取れない場合の解析エラー。"""


@dataclasses.dataclass(frozen=True)
class Event:
  event_id: str
  role: str
  text: str
  line_no: int


@dataclasses.dataclass(frozen=True)
class ToolCall:
  event_id: str
  call_id: str
  name: str
  arguments: object
  line_no: int
  block_index: int


@dataclasses.dataclass(frozen=True)
class ToolResult:
  event_id: str
  call_id: str
  text: str
  is_error: bool
  line_no: int
  block_index: int


@dataclasses.dataclass(frozen=True)
class ParseIssue:
  kind: str
  line_no: int
  detail: str
  block_index: int = -1


@dataclasses.dataclass(frozen=True)
class ParseResult:
  events: tuple
  issues: tuple


def _extract_text(content) -> str:
  if isinstance(content, str):
    return content
  if isinstance(content, list):
    return "\n".join(
      block["text"]
      for block in content
      if (
        isinstance(block, dict)
        and block.get("type") == "text"
        and isinstance(block.get("text"), str)
      )
    )
  return ""


def _parse_content(event_id, role, content, line_no, issues) -> tuple:
  if isinstance(content, str):
    return (Event(
      event_id=event_id,
      role=role,
      text=content,
      line_no=line_no,
    ),)
  if not isinstance(content, list):
    return (Event(
      event_id=event_id,
      role=role,
      text="",
      line_no=line_no,
    ),)

  events = []
  for block_index, block in enumerate(content):
    if not isinstance(block, dict):
      continue
    block_type = block.get("type")
    if block_type == "text":
      events.append(Event(
        event_id=event_id,
        role=role,
        text=block.get("text", ""),
        line_no=line_no,
      ))
    elif block_type == "tool_use":
      call_id = block.get("id")
      if not isinstance(call_id, str) or not call_id:
        issues.append(ParseIssue(
          kind="incomplete_tool_event",
          line_no=line_no,
          detail="missing_call_id",
          block_index=block_index,
        ))
        continue
      events.append(ToolCall(
        event_id=event_id,
        call_id=call_id,
        name=block.get("name"),
        arguments=block.get("input"),
        line_no=line_no,
        block_index=block_index,
      ))
    elif block_type == "tool_result":
      call_id = block.get("tool_use_id")
      if not isinstance(call_id, str) or not call_id:
        issues.append(ParseIssue(
          kind="incomplete_tool_event",
          line_no=line_no,
          detail="missing_call_id",
          block_index=block_index,
        ))
        continue
      events.append(ToolResult(
        event_id=event_id,
        call_id=call_id,
        text=_extract_text(block.get("content")),
        is_error=bool(block.get("is_error")),
        line_no=line_no,
        block_index=block_index,
      ))
  return tuple(events)


def _read_lines(path):
  raw_path = Path(path)
  try:
    with raw_path.open(encoding="utf-8") as raw_log:
      yield from raw_log
  except OSError as error:
    raise ParseError(
      "Cannot read raw log: %s" % raw_path
    ) from error


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
    role = record.get("type")
    if role not in ("user", "assistant"):
      issues.append(ParseIssue(
        kind="unsupported_event",
        line_no=line_no,
        detail=str(role),
      ))
      continue
    event_id = record.get("uuid")
    if not isinstance(event_id, str) or not event_id:
      issues.append(ParseIssue(
        kind="incomplete_event",
        line_no=line_no,
        detail="missing_uuid",
      ))
      continue
    message = record.get("message")
    if not isinstance(message, dict):
      issues.append(ParseIssue(
        kind="incomplete_event",
        line_no=line_no,
        detail="invalid_message",
      ))
      continue
    events.extend(_parse_content(
      event_id=event_id,
      role=role,
      content=message.get("content"),
      line_no=line_no,
      issues=issues,
    ))
  return ParseResult(events=tuple(events), issues=tuple(issues))


def parse_claude_bytes(data) -> ParseResult:
  return _parse_lines(
    data.decode("utf-8").splitlines(keepends=True)
  )


def parse_claude_log(path) -> ParseResult:
  return _parse_lines(_read_lines(path))


def parse_claude_events(path) -> tuple:
  return parse_claude_log(path).events
