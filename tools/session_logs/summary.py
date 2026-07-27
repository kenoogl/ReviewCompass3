"""人が読むセッション要約。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.session_logs.parse_claude import Event
from tools.session_logs.redaction import redact_text_strict


@dataclasses.dataclass(frozen=True)
class Summary:
  text: str
  redaction_findings: tuple


def _bullets(values) -> str:
  items = tuple(values)
  if not items:
    return "- None"
  return "\n".join("- %s" % value for value in items)


def render_summary(
  events,
  *,
  commits,
  changed_files,
  rules,
) -> Summary:
  user_messages = tuple(
    event.text
    for event in events
    if isinstance(event, Event) and event.role == "user"
  )
  text = "\n\n".join((
    "# Session summary",
    "## User messages\n\n%s" % _bullets(user_messages),
    "## Commits\n\n%s" % _bullets(commits),
    "## Changed files\n\n%s" % _bullets(
      sorted(set(changed_files))
    ),
    "## Decisions\n\n- Not inferred automatically.",
  )) + "\n"
  redacted = redact_text_strict(text, rules)
  return Summary(
    text=redacted.text,
    redaction_findings=redacted.findings,
  )
