"""記録済み範囲からのセッションログ転写再生成。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
from pathlib import Path

from tools.session_logs.provenance import read_recorded_range
from tools.session_logs.redaction import (
  redact_text_strict,
  redaction_rules_digest,
)
from tools.session_logs.summary import render_summary
from tools.session_logs.source_adapter import parse_source_bytes
from tools.session_logs.transcript import render_transcript


class RegenerationError(Exception):
  """値を含めない転写再生成エラー。"""

  def __init__(self, reason):
    self.reason = reason
    super().__init__("Transcript regeneration failed: %s" % reason)


@dataclasses.dataclass(frozen=True)
class RegenerationResult:
  text: str
  source_matches: bool
  provenance_matches: bool
  stored_matches: bool
  rules_match: bool = True
  tool_version_matches: bool = True
  status: str = "matches"
  summary_text: str = ""
  summary_provenance_matches: bool = True
  summary_stored_matches: bool = True


def regenerate_transcript(
  record,
  *,
  raw_root,
  stored_text,
  rules,
  allow_patterns=(),
  tool_version=None,
) -> RegenerationResult:
  raw_log = Path(raw_root) / record.source_path
  try:
    source_bytes = read_recorded_range(raw_log, record)
    parsed = parse_source_bytes(source_bytes).parsed
    transcript = render_transcript(parsed)
    redacted = redact_text_strict(
      transcript,
      rules,
      allow_patterns=allow_patterns,
    )
  except Exception as error:
    raise RegenerationError(type(error).__name__) from error
  transcript_sha256 = hashlib.sha256(
    redacted.text.encode("utf-8")
  ).hexdigest()
  source_matches = (
    hashlib.sha256(source_bytes).hexdigest()
    == record.source_sha256
  )
  provenance_matches = (
    transcript_sha256 == record.transcript_sha256
  )
  stored_matches = redacted.text == stored_text
  current_rules_sha256 = redaction_rules_digest(
    rules,
    allow_patterns=allow_patterns,
  )
  rules_match = (
    current_rules_sha256
    == record.redaction_rules_sha256
  )
  tool_version_matches = (
    tool_version is None
    or tool_version == record.tool_version
  )
  if not source_matches:
    status = "source_changed"
  elif not rules_match or not tool_version_matches:
    status = "conditions_changed"
  elif not provenance_matches or not stored_matches:
    status = "transcript_changed"
  else:
    status = "matches"
  return RegenerationResult(
    text=redacted.text,
    source_matches=source_matches,
    provenance_matches=provenance_matches,
    stored_matches=stored_matches,
    rules_match=rules_match,
    tool_version_matches=tool_version_matches,
    status=status,
  )


def regenerate_artifact(
  record,
  *,
  raw_root,
  stored_text,
  stored_summary,
  rules,
  allow_patterns=(),
  tool_version=None,
) -> RegenerationResult:
  transcript_result = regenerate_transcript(
    record,
    raw_root=raw_root,
    stored_text=stored_text,
    rules=rules,
    allow_patterns=allow_patterns,
    tool_version=tool_version,
  )
  raw_log = Path(raw_root) / record.source_path
  try:
    source_bytes = read_recorded_range(raw_log, record)
    parsed = parse_source_bytes(source_bytes).parsed
    summary = render_summary(
      parsed.events,
      commits=getattr(record, "summary_commits", ()),
      changed_files=getattr(
        record,
        "summary_changed_files",
        (),
      ),
      rules=rules,
      allow_patterns=allow_patterns,
    )
  except Exception as error:
    raise RegenerationError(type(error).__name__) from error
  summary_sha256 = hashlib.sha256(
    summary.text.encode("utf-8")
  ).hexdigest()
  summary_provenance_matches = (
    summary_sha256 == record.summary_sha256
  )
  summary_stored_matches = summary.text == stored_summary
  if transcript_result.status != "matches":
    status = transcript_result.status
  elif (
    not summary_provenance_matches
    or not summary_stored_matches
  ):
    status = "summary_changed"
  else:
    status = "matches"
  return dataclasses.replace(
    transcript_result,
    status=status,
    summary_text=summary.text,
    summary_provenance_matches=summary_provenance_matches,
    summary_stored_matches=summary_stored_matches,
  )
