"""記録済み範囲からのセッションログ転写再生成。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path

from tools.session_logs.parse_claude import parse_claude_bytes
from tools.session_logs.parse_codex import parse_codex_bytes
from tools.session_logs.provenance import read_recorded_range
from tools.session_logs.redaction import (
  redact_text_strict,
  redaction_rules_digest,
)
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


def _parse_source_bytes(data):
  first_line = next((
    line
    for line in data.splitlines()
    if line.strip()
  ), b"")
  first_record = json.loads(first_line) if first_line else {}
  if (
    isinstance(first_record, dict)
    and first_record.get("type") == "thread.started"
    and isinstance(first_record.get("thread_id"), str)
  ):
    return parse_codex_bytes(data)
  return parse_claude_bytes(data)


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
    parsed = _parse_source_bytes(source_bytes)
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
