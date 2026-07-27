"""記録済み範囲からのセッションログ転写再生成。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
from pathlib import Path

from tools.session_logs.parse_claude import parse_claude_bytes
from tools.session_logs.provenance import read_recorded_range
from tools.session_logs.redaction import redact_text_strict
from tools.session_logs.transcript import render_transcript


@dataclasses.dataclass(frozen=True)
class RegenerationResult:
  text: str
  source_matches: bool
  provenance_matches: bool
  stored_matches: bool


def regenerate_transcript(
  record,
  *,
  raw_root,
  stored_text,
  rules,
  allow_patterns=(),
) -> RegenerationResult:
  raw_log = Path(raw_root) / record.source_path
  source_bytes = read_recorded_range(raw_log, record)
  parsed = parse_claude_bytes(source_bytes)
  transcript = render_transcript(parsed)
  redacted = redact_text_strict(
    transcript,
    rules,
    allow_patterns=allow_patterns,
  )
  transcript_sha256 = hashlib.sha256(
    redacted.text.encode("utf-8")
  ).hexdigest()
  return RegenerationResult(
    text=redacted.text,
    source_matches=(
      hashlib.sha256(source_bytes).hexdigest()
      == record.source_sha256
    ),
    provenance_matches=(
      transcript_sha256 == record.transcript_sha256
    ),
    stored_matches=(redacted.text == stored_text),
  )
