"""セッションログ転写の来歴。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class Provenance:
  source_path: str
  start_line: int
  end_line: int
  source_sha256: str
  transcript_sha256: str
  tool_version: str
  summary_sha256: str = ""
  redaction_rules_sha256: str = ""


@dataclasses.dataclass(frozen=True)
class VerificationResult:
  source_matches: bool
  transcript_matches: bool


def _line_count(data: bytes) -> int:
  if not data:
    return 0
  return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def _lf_lines(data):
  lines = []
  start = 0
  while start < len(data):
    end = data.find(b"\n", start)
    if end < 0:
      lines.append(data[start:])
      break
    lines.append(data[start:end + 1])
    start = end + 1
  return tuple(lines)


def build_provenance(
  raw_log,
  *,
  raw_root,
  transcript_text,
  tool_version,
  summary_text="",
  redaction_rules_sha256="",
) -> Provenance:
  raw_path = Path(raw_log)
  root_path = Path(raw_root)
  raw_bytes = raw_path.read_bytes()
  transcript_bytes = transcript_text.encode("utf-8")
  return Provenance(
    source_path=raw_path.relative_to(root_path).as_posix(),
    start_line=1,
    end_line=_line_count(raw_bytes),
    source_sha256=hashlib.sha256(raw_bytes).hexdigest(),
    transcript_sha256=hashlib.sha256(transcript_bytes).hexdigest(),
    tool_version=tool_version,
    summary_sha256=hashlib.sha256(
      summary_text.encode("utf-8")
    ).hexdigest() if summary_text else "",
    redaction_rules_sha256=redaction_rules_sha256,
  )


def read_recorded_range(raw_log, record) -> bytes:
  raw_bytes = Path(raw_log).read_bytes()
  lines = _lf_lines(raw_bytes)
  return b"".join(lines[record.start_line - 1:record.end_line])


def verify_provenance(
  record,
  *,
  raw_log,
  transcript_text,
) -> VerificationResult:
  source_bytes = read_recorded_range(raw_log, record)
  transcript_bytes = transcript_text.encode("utf-8")
  return VerificationResult(
    source_matches=(
      hashlib.sha256(source_bytes).hexdigest() == record.source_sha256
    ),
    transcript_matches=(
      hashlib.sha256(transcript_bytes).hexdigest()
      == record.transcript_sha256
    ),
  )
