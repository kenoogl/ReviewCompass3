"""Claude生セッションログの解析。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
from pathlib import Path


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


def parse_claude_log(path) -> ParseResult:
  events = []
  issues = []
  with Path(path).open(encoding="utf-8") as raw_log:
    for line_no, line in enumerate(raw_log, start=1):
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
      message = record.get("message") or {}
      events.append(Event(
        event_id=record.get("uuid"),
        role=role,
        text=_extract_text(message.get("content")),
        line_no=line_no,
      ))
  return ParseResult(events=tuple(events), issues=tuple(issues))


def parse_claude_events(path) -> tuple:
  return parse_claude_log(path).events
