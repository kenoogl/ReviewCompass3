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


def test_rebuilds_recorded_range_and_detects_independent_changes(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  recorded_bytes = b'{"event": 1}\n{"event": 2}\n'
  appended_bytes = b'{"event": 3}\n'
  raw_log.write_bytes(recorded_bytes)
  transcript_text = "## user\n\nOriginal.\n"

  provenance = importlib.import_module("tools.session_logs.provenance")
  record = provenance.build_provenance(
    raw_log,
    raw_root=raw_root,
    transcript_text=transcript_text,
    tool_version="0.0.1",
  )

  raw_log.write_bytes(recorded_bytes + appended_bytes)

  assert provenance.read_recorded_range(raw_log, record) == recorded_bytes
  assert provenance.verify_provenance(
    record,
    raw_log=raw_log,
    transcript_text=transcript_text,
  ) == provenance.VerificationResult(
    source_matches=True,
    transcript_matches=True,
  )

  assert provenance.verify_provenance(
    record,
    raw_log=raw_log,
    transcript_text="## user\n\nTampered.\n",
  ) == provenance.VerificationResult(
    source_matches=True,
    transcript_matches=False,
  )

  raw_log.write_bytes(b'{"event": 0}\n{"event": 2}\n' + appended_bytes)

  assert provenance.verify_provenance(
    record,
    raw_log=raw_log,
    transcript_text=transcript_text,
  ) == provenance.VerificationResult(
    source_matches=False,
    transcript_matches=True,
  )
