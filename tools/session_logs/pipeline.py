"""セッションログ成果物候補の統括パイプライン。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.session_logs import parse_claude
from tools.session_logs.provenance import build_provenance
from tools.session_logs.redaction import redact_text_strict
from tools.session_logs.source_kind import identify_source_kind
from tools.session_logs.transcript import render_transcript


class UnsupportedSourceKind(Exception):
  """実装していない、または識別できない入力形式。"""


@dataclasses.dataclass(frozen=True)
class PreparedArtifact:
  source_kind: str
  events: tuple
  text: str
  provenance: object
  parse_issues: tuple
  redaction_findings: tuple


def prepare_artifact(
  raw_log,
  *,
  raw_root,
  rules,
  tool_version,
) -> PreparedArtifact:
  source_kind = identify_source_kind(raw_log)
  if source_kind != "claude":
    raise UnsupportedSourceKind(str(source_kind))

  parsed = parse_claude.parse_claude_log(raw_log)
  transcript_text = render_transcript(parsed)
  redacted = redact_text_strict(transcript_text, rules)
  artifact_provenance = build_provenance(
    raw_log,
    raw_root=raw_root,
    transcript_text=redacted.text,
    tool_version=tool_version,
  )
  return PreparedArtifact(
    source_kind=source_kind,
    events=parsed.events,
    text=redacted.text,
    provenance=artifact_provenance,
    parse_issues=parsed.issues,
    redaction_findings=redacted.findings,
  )
