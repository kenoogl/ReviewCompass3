"""セッションログCLIの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_cli_loads_config_and_stores_all_discovered_logs(tmp_path):
  raw_log = tmp_path / "raw" / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  secret = "sk-ant-cli_secret"
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "key=%s" % secret,
      },
    }) + "\n",
    encoding="utf-8",
  )
  config_path = tmp_path / "session-logs.json"
  config_path.write_text(
    json.dumps({
      "raw_root": "raw",
      "transcript_root": "transcripts",
      "summary_root": "summaries",
      "provenance_root": "provenance",
      "tool_version": "0.0.1",
      "redaction_rules": [
        {
          "label": "anthropic_key",
          "pattern": "sk-ant-[A-Za-z0-9_-]+",
        },
      ],
    }),
    encoding="utf-8",
  )

  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 0

  transcript_path = tmp_path / "transcripts" / "nested" / "session.md"
  summary_path = tmp_path / "summaries" / "nested" / "session.md"
  provenance_path = tmp_path / "provenance" / "nested" / "session.json"
  assert transcript_path.is_file()
  assert summary_path.is_file()
  assert provenance_path.is_file()
  assert secret not in transcript_path.read_text(encoding="utf-8")
  assert secret not in summary_path.read_text(encoding="utf-8")


def test_cli_writes_safe_report_and_no_artifacts_on_sensitive_data(tmp_path):
  raw_log = tmp_path / "raw" / "session.jsonl"
  raw_log.parent.mkdir()
  secret = "B8gL3nR6yS1wU9qM4pD7tX2zJ5kF0cV"
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "token=%s" % secret,
      },
    }) + "\n",
    encoding="utf-8",
  )
  config_path = tmp_path / "session-logs.json"
  config_path.write_text(
    json.dumps({
      "raw_root": "raw",
      "transcript_root": "transcripts",
      "summary_root": "summaries",
      "provenance_root": "provenance",
      "sensitive_report_root": "sensitive-reports",
      "tool_version": "0.0.1",
      "redaction_rules": [],
      "allow_patterns": [],
    }),
    encoding="utf-8",
  )

  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 2

  assert not (tmp_path / "transcripts" / "session.md").exists()
  assert not (tmp_path / "summaries" / "session.md").exists()
  assert not (tmp_path / "provenance" / "session.json").exists()
  report_path = tmp_path / "sensitive-reports" / "session.json"
  assert report_path.is_file()
  assert secret not in report_path.read_text(encoding="utf-8")
