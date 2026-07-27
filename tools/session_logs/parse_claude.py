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


def parse_claude_events(path) -> tuple:
  events = []
  with Path(path).open(encoding="utf-8") as raw_log:
    for line_no, line in enumerate(raw_log, start=1):
      record = json.loads(line)
      role = record.get("type")
      if role not in ("user", "assistant"):
        continue
      message = record.get("message") or {}
      events.append(Event(
        event_id=record.get("uuid"),
        role=role,
        text=_extract_text(message.get("content")),
        line_no=line_no,
      ))
  return tuple(events)
