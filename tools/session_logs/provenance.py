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


def _line_count(data: bytes) -> int:
  if not data:
    return 0
  return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def build_provenance(
  raw_log,
  *,
  raw_root,
  transcript_text,
  tool_version,
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
  )
