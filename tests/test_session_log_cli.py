"""セッションログCLIの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def _write_config(tmp_path):
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
  return config_path


def _write_event(path, event_id="user-1", text="Review this."):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps({
      "uuid": event_id,
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": text,
      },
    }) + "\n",
    encoding="utf-8",
  )


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


def test_cli_dry_run_reports_plan_without_writing_artifacts(
  tmp_path,
  capsys,
):
  raw_log = tmp_path / "raw" / "nested" / "session.jsonl"
  _write_event(raw_log)
  config_path = _write_config(tmp_path)
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run((
    "--config",
    str(config_path),
    "--dry-run",
  )) == 0

  assert capsys.readouterr().out == "planned nested/session.jsonl\n"
  assert not (tmp_path / "transcripts").exists()
  assert not (tmp_path / "summaries").exists()
  assert not (tmp_path / "provenance").exists()


def test_cli_distinguishes_no_targets_and_general_failure(tmp_path):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  config_path = _write_config(tmp_path)
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 3

  raw_root.rmdir()

  assert cli.run(("--config", str(config_path))) == 5


def test_cli_continues_after_unsupported_log_and_reports_exit_value(
  tmp_path,
):
  _write_event(tmp_path / "raw" / "accepted.jsonl")
  unsupported = tmp_path / "raw" / "unsupported.jsonl"
  unsupported.write_text("{}\n", encoding="utf-8")
  config_path = _write_config(tmp_path)
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 4

  assert (tmp_path / "transcripts" / "accepted.md").is_file()
  assert not (tmp_path / "transcripts" / "unsupported.md").exists()


def test_cli_preserves_enabled_raw_logs_and_distinguishes_failure(
  tmp_path,
):
  raw_log = tmp_path / "raw" / "nested" / "session.jsonl"
  _write_event(raw_log)
  config_path = _write_config(tmp_path)
  config = json.loads(config_path.read_text(encoding="utf-8"))
  config.update({
    "backup_root": "private-backup",
    "preservation_enabled": True,
  })
  config_path.write_text(json.dumps(config), encoding="utf-8")
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 0
  assert (
    tmp_path / "private-backup" / "nested" / "session.jsonl"
  ).read_bytes() == raw_log.read_bytes()

  blocked_root = tmp_path / "blocked-backup"
  blocked_root.write_text("not a directory", encoding="utf-8")
  config["backup_root"] = "blocked-backup"
  config_path.write_text(json.dumps(config), encoding="utf-8")

  assert cli.run(("--config", str(config_path))) == 6
  assert (tmp_path / "transcripts" / "nested" / "session.md").is_file()


def test_cli_verifies_saved_transcript_and_reports_condition_change(
  tmp_path,
  capsys,
):
  raw_log = tmp_path / "raw" / "session.jsonl"
  _write_event(raw_log)
  config_path = _write_config(tmp_path)
  cli = importlib.import_module("tools.session_logs.cli")
  assert cli.run(("--config", str(config_path))) == 0

  assert cli.run((
    "--config",
    str(config_path),
    "--verify",
  )) == 0
  matched = json.loads(capsys.readouterr().out)
  assert matched == {
    "provenance_matches": True,
    "rules_match": True,
    "source_matches": True,
    "source_path": "session.jsonl",
    "status": "matches",
    "stored_matches": True,
    "tool_version_matches": True,
  }

  config = json.loads(config_path.read_text(encoding="utf-8"))
  config["tool_version"] = "0.0.2"
  config_path.write_text(json.dumps(config), encoding="utf-8")

  assert cli.run((
    "--config",
    str(config_path),
    "--verify",
  )) == 7
  changed = json.loads(capsys.readouterr().out)
  assert changed["status"] == "conditions_changed"
  assert changed["tool_version_matches"] is False


def test_cli_verification_failure_report_is_safe(tmp_path, capsys):
  raw_log = tmp_path / "raw" / "session.jsonl"
  _write_event(raw_log)
  config_path = _write_config(tmp_path)
  cli = importlib.import_module("tools.session_logs.cli")
  assert cli.run(("--config", str(config_path))) == 0
  raw_log.write_bytes(b"\xffsecret-value-not-for-output\n")

  assert cli.run((
    "--config",
    str(config_path),
    "--verify",
  )) == 8

  report = capsys.readouterr().out
  assert json.loads(report) == {
    "reason": "UnicodeDecodeError",
    "source_path": "session.jsonl",
    "status": "regeneration_failed",
  }
  assert "secret-value-not-for-output" not in report


def test_cli_preserve_only_is_safe_for_scheduled_execution(tmp_path):
  raw_log = tmp_path / "raw" / "session.jsonl"
  _write_event(raw_log)
  config_path = _write_config(tmp_path)
  config = json.loads(config_path.read_text(encoding="utf-8"))
  config.update({
    "backup_root": "private-backup",
    "preservation_enabled": True,
  })
  config_path.write_text(json.dumps(config), encoding="utf-8")
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run((
    "--config",
    str(config_path),
    "--preserve-only",
  )) == 0

  assert (
    tmp_path / "private-backup" / "session.jsonl"
  ).read_bytes() == raw_log.read_bytes()
  assert not (tmp_path / "transcripts").exists()
  assert not (tmp_path / "summaries").exists()
  assert not (tmp_path / "provenance").exists()


def test_cli_lists_and_restores_only_explicit_safe_backup_path(
  tmp_path,
  capsys,
):
  raw_log = tmp_path / "raw" / "nested" / "session.jsonl"
  _write_event(raw_log)
  original = raw_log.read_bytes()
  config_path = _write_config(tmp_path)
  config = json.loads(config_path.read_text(encoding="utf-8"))
  config.update({
    "backup_root": "private-backup",
    "preservation_enabled": True,
  })
  config_path.write_text(json.dumps(config), encoding="utf-8")
  cli = importlib.import_module("tools.session_logs.cli")
  assert cli.run((
    "--config",
    str(config_path),
    "--preserve-only",
  )) == 0

  assert cli.run((
    "--config",
    str(config_path),
    "--list-backups",
  )) == 0
  assert capsys.readouterr().out == "nested/session.jsonl\n"

  raw_log.unlink()
  assert cli.run((
    "--config",
    str(config_path),
    "--restore",
    "nested/session.jsonl",
  )) == 0
  assert raw_log.read_bytes() == original

  raw_log.write_bytes(b"existing divergent data\n")
  assert cli.run((
    "--config",
    str(config_path),
    "--restore",
    "nested/session.jsonl",
  )) == 9
  assert raw_log.read_bytes() == b"existing divergent data\n"

  assert cli.run((
    "--config",
    str(config_path),
    "--restore",
    "../escape.jsonl",
  )) == 5
  assert not (tmp_path / "escape.jsonl").exists()
