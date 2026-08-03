"""セッションログ成果物候補の統括パイプライン。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.session_logs.provenance import build_provenance
from tools.session_logs.redaction import (
  redact_text_strict,
  redaction_rules_digest,
)
from tools.session_logs.source_adapter import (
  UnsupportedSourceKind,
  parse_source_log,
)
from tools.session_logs.summary import render_summary
from tools.session_logs.transcript import render_transcript


@dataclasses.dataclass(frozen=True)
class PreparedArtifact:
  source_kind: str
  events: tuple
  text: str
  provenance: object
  parse_issues: tuple
  redaction_findings: tuple
  summary_text: str
  summary_redaction_findings: tuple


def prepare_artifact(
  raw_log,
  *,
  raw_root,
  rules,
  tool_version,
  commits=(),
  changed_files=(),
  allow_patterns=(),
) -> PreparedArtifact:
  source = parse_source_log(raw_log)
  source_kind = source.source_kind
  parsed = source.parsed

  transcript_text = render_transcript(parsed)
  redacted = redact_text_strict(
    transcript_text,
    rules,
    allow_patterns=allow_patterns,
  )
  summary = render_summary(
    parsed.events,
    commits=commits,
    changed_files=changed_files,
    rules=rules,
    allow_patterns=allow_patterns,
  )
  artifact_provenance = build_provenance(
    raw_log,
    raw_root=raw_root,
    transcript_text=redacted.text,
    tool_version=tool_version,
    summary_text=summary.text,
    redaction_rules_sha256=redaction_rules_digest(
      rules,
      allow_patterns=allow_patterns,
    ),
    summary_commits=commits,
    summary_changed_files=changed_files,
  )
  return PreparedArtifact(
    source_kind=source_kind,
    events=parsed.events,
    text=redacted.text,
    provenance=artifact_provenance,
    parse_issues=parsed.issues,
    redaction_findings=redacted.findings,
    summary_text=summary.text,
    summary_redaction_findings=summary.redaction_findings,
  )
