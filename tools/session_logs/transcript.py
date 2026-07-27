"""生セッションログの最小転写。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json

from tools.session_logs.parse_claude import Event, ToolCall, ToolResult


def _render_event(event) -> str:
  if isinstance(event, Event):
    return "## %s\n\n%s" % (event.role, event.text)
  if isinstance(event, ToolCall):
    arguments = json.dumps(
      event.arguments,
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    )
    return (
      "## tool_call %s (%s)\n\n"
      "```json\n%s\n```"
    ) % (event.name, event.call_id, arguments)
  if isinstance(event, ToolResult):
    status = " error" if event.is_error else ""
    return "## tool_result %s%s\n\n%s" % (
      event.call_id,
      status,
      event.text,
    )
  raise TypeError("Unsupported transcript event: %r" % (event,))


def render_transcript(result) -> str:
  return "\n\n".join(
    _render_event(event)
    for event in result.events
  ) + "\n"
