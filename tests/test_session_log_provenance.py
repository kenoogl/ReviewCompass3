"""セッションログ来歴の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib


def test_records_source_range_digests_and_tool_version(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  raw_bytes = b'{"event": 1}\n{"event": 2}\n'
  raw_log.write_bytes(raw_bytes)
  transcript_text = "## user\n\nReview this.\n"

  provenance = importlib.import_module("tools.session_logs.provenance")

  assert provenance.build_provenance(
    raw_log,
    raw_root=raw_root,
    transcript_text=transcript_text,
    tool_version="0.0.1",
  ) == provenance.Provenance(
    source_path="nested/session.jsonl",
    start_line=1,
    end_line=2,
    source_sha256=hashlib.sha256(raw_bytes).hexdigest(),
    transcript_sha256=hashlib.sha256(
      transcript_text.encode("utf-8")
    ).hexdigest(),
    tool_version="0.0.1",
  )
