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
class ParseIssue:
  kind: str
  line_no: int
  detail: str


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


def _read_lines(path):
  raw_path = Path(path)
  try:
    with raw_path.open(encoding="utf-8") as raw_log:
      yield from raw_log
  except OSError as error:
    raise ParseError(
      "Cannot read raw log: %s" % raw_path
    ) from error


def parse_claude_log(path) -> ParseResult:
  events = []
  issues = []
  for line_no, line in enumerate(_read_lines(path), start=1):
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
    events.append(Event(
      event_id=event_id,
      role=role,
      text=_extract_text(message.get("content")),
      line_no=line_no,
    ))
  return ParseResult(events=tuple(events), issues=tuple(issues))


def parse_claude_events(path) -> tuple:
  return parse_claude_log(path).events
