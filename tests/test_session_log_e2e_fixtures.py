"""実データ形状fixtureによるセッションログE2E暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import shutil
from pathlib import Path


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "session_logs"


def test_real_shape_fixtures_survive_capture_verify_and_restore(tmp_path):
  metadata = json.loads(
    (FIXTURE_ROOT / "metadata.json").read_text(encoding="utf-8")
  )
  assert metadata == {
    "excluded_fields": [
      "credentials",
      "machine-specific paths",
      "raw reasoning",
    ],
    "fixtures": {
      "claude-public-shape.jsonl": "Claude Code JSONL event shape",
      "codex-exec-public-shape.jsonl": "codex exec --json public shape",
    },
  }

  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  fixture_names = tuple(sorted(metadata["fixtures"]))
  original_bytes = {}
  for fixture_name in fixture_names:
    source = FIXTURE_ROOT / fixture_name
    target = raw_root / fixture_name
    shutil.copyfile(source, target)
    original_bytes[fixture_name] = target.read_bytes()

  config_path = tmp_path / "session-logs.json"
  config_path.write_text(
    json.dumps({
      "raw_root": "raw",
      "transcript_root": "transcripts",
      "summary_root": "summaries",
      "provenance_root": "provenance",
      "sensitive_report_root": "sensitive-reports",
      "backup_root": "private-backup",
      "preservation_enabled": True,
      "tool_version": "0.0.1",
      "redaction_rules": [],
      "allow_patterns": [],
    }),
    encoding="utf-8",
  )
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 0
  assert cli.run(("--config", str(config_path), "--verify")) == 0

  for fixture_name in fixture_names:
    stem = Path(fixture_name).stem
    assert (tmp_path / "transcripts" / (stem + ".md")).is_file()
    assert (tmp_path / "summaries" / (stem + ".md")).is_file()
    assert (tmp_path / "provenance" / (stem + ".json")).is_file()
    (raw_root / fixture_name).unlink()

  for fixture_name in fixture_names:
    assert cli.run((
      "--config",
      str(config_path),
      "--restore",
      fixture_name,
    )) == 0
    assert (
      raw_root / fixture_name
    ).read_bytes() == original_bytes[fixture_name]

  assert cli.run(("--config", str(config_path), "--verify")) == 0
