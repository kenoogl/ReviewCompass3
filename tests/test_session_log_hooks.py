"""セッションログ開始・終了フックの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import shlex
import subprocess
import sys
from pathlib import Path


def _write_setup(tmp_path):
  raw_log = tmp_path / "raw" / "session.jsonl"
  raw_log.parent.mkdir()
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "Review this.",
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
      "backup_root": "private-backup",
      "preservation_enabled": True,
      "tool_version": "0.0.1",
      "redaction_rules": [],
    }),
    encoding="utf-8",
  )
  return config_path


def test_hooks_skip_safely_when_disabled_or_unconfigured(tmp_path):
  hooks = importlib.import_module("tools.session_logs.hooks")

  assert hooks.run_start_hook(None) == hooks.HookResult(
    action="skipped",
    exit_code=0,
  )
  assert hooks.run_end_hook(
    tmp_path / "missing.json",
    enabled=False,
  ) == hooks.HookResult(
    action="skipped",
    exit_code=0,
  )


def test_start_hook_checks_without_writes_and_end_hook_stores(
  tmp_path,
  capsys,
):
  config_path = _write_setup(tmp_path)
  hooks = importlib.import_module("tools.session_logs.hooks")

  started = hooks.run_start_hook(config_path)

  assert started == hooks.HookResult(action="checked", exit_code=0)
  assert capsys.readouterr().out == "planned session.jsonl\n"
  assert not (tmp_path / "transcripts").exists()

  ended = hooks.run_end_hook(config_path)

  assert ended == hooks.HookResult(action="stored", exit_code=0)
  assert (tmp_path / "transcripts" / "session.md").is_file()
  assert (tmp_path / "summaries" / "session.md").is_file()
  assert (tmp_path / "provenance" / "session.json").is_file()
  assert (
    tmp_path / "private-backup" / "session.jsonl"
  ).read_bytes() == (
    tmp_path / "raw" / "session.jsonl"
  ).read_bytes()


def test_builds_installable_commands_and_runs_fixed_phase_entry(
  tmp_path,
  capsys,
):
  config_path = _write_setup(tmp_path)
  hooks = importlib.import_module("tools.session_logs.hooks")
  installation = importlib.import_module(
    "tools.session_logs.hook_installation"
  )
  settings_path = tmp_path / ".claude" / "settings.local.json"

  commands = hooks.build_hook_commands(
    "/usr/bin/python3",
    config_path,
  )
  entry_path = Path(hooks.__file__).with_name("entry.py").resolve()

  assert shlex.split(commands.start) == [
    "/usr/bin/python3",
    str(entry_path),
    "hook",
    "start",
    "--config",
    str(config_path),
  ]
  assert shlex.split(commands.end)[3] == "end"

  installation.install_claude_hooks(
    settings_path,
    start_command=commands.start,
    end_command=commands.end,
  )
  settings = json.loads(settings_path.read_text(encoding="utf-8"))
  assert (
    settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    == commands.start
  )
  assert hooks.run((
    "start",
    "--config",
    str(config_path),
  )) == 0
  capsys.readouterr()
  assert hooks.run((
    "end",
    "--config",
    str(config_path),
  )) == 0


def test_fixed_hook_command_runs_outside_repository_cwd(tmp_path):
  config_path = _write_setup(tmp_path)
  hooks = importlib.import_module("tools.session_logs.hooks")
  commands = hooks.build_hook_commands(
    sys.executable,
    config_path,
  )
  outside_cwd = tmp_path / "outside-cwd"
  outside_cwd.mkdir()

  completed = subprocess.run(
    shlex.split(commands.end),
    cwd=outside_cwd,
    capture_output=True,
    check=False,
    text=True,
  )

  assert completed.returncode == 0
  assert (tmp_path / "transcripts" / "session.md").is_file()


def test_hook_records_safe_outcomes_without_propagating_failures(
  tmp_path,
):
  missing_config = tmp_path / "missing-secret-config.json"
  event_log = tmp_path / "private-events" / "hooks.jsonl"
  hooks = importlib.import_module("tools.session_logs.hooks")

  start_result = hooks.run_start_hook(
    missing_config,
    event_log_path=event_log,
  )
  end_result = hooks.run_end_hook(
    missing_config,
    event_log_path=event_log,
  )

  assert start_result == hooks.HookResult(
    action="failed",
    exit_code=0,
    operation_exit_code=5,
  )
  assert end_result == hooks.HookResult(
    action="failed",
    exit_code=0,
    operation_exit_code=5,
  )
  events = tuple(
    json.loads(line)
    for line in event_log.read_text(encoding="utf-8").splitlines()
  )
  assert events == (
    {
      "action": "failed",
      "phase": "start",
      "reason": "exit_code_5",
      "status": "failed",
    },
    {
      "action": "failed",
      "phase": "end",
      "reason": "exit_code_5",
      "status": "failed",
    },
  )
  assert "missing-secret-config" not in event_log.read_text(
    encoding="utf-8"
  )


def test_hook_records_completed_only_after_success(tmp_path, capsys):
  config_path = _write_setup(tmp_path)
  event_log = tmp_path / "private-events" / "hooks.jsonl"
  hooks = importlib.import_module("tools.session_logs.hooks")

  assert hooks.run((
    "start",
    "--config",
    str(config_path),
    "--event-log",
    str(event_log),
  )) == 0
  capsys.readouterr()
  assert hooks.run((
    "end",
    "--config",
    str(config_path),
    "--event-log",
    str(event_log),
  )) == 0

  events = tuple(
    json.loads(line)
    for line in event_log.read_text(encoding="utf-8").splitlines()
  )
  assert events == (
    {
      "action": "checked",
      "phase": "start",
      "status": "completed",
    },
    {
      "action": "stored",
      "phase": "end",
      "status": "completed",
    },
  )
