"""セッション非利用期間の定期保全設定の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import plistlib
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace


def test_installs_and_uninstalls_owned_launchd_schedule_idempotently(
  tmp_path,
):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  plist_path = tmp_path / "LaunchAgents" / "session-logs.plist"
  config_path = tmp_path / "config" / "session-logs.json"
  stdout_path = tmp_path / "private-logs" / "preserve.stdout.jsonl"
  stderr_path = tmp_path / "private-logs" / "preserve.stderr.log"

  first = scheduler.install_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=config_path,
    interval_seconds=1800,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )
  repeated = scheduler.install_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=config_path,
    interval_seconds=1800,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )

  assert first.action == "installed"
  assert repeated.action == "unchanged"
  with plist_path.open("rb") as source:
    settings = plistlib.load(source)
  entry_path = Path(scheduler.__file__).with_name("entry.py").resolve()
  assert settings == {
    "Label": "com.reviewcompass.session-log-preservation",
    "ProgramArguments": [
      "/usr/bin/python3",
      str(entry_path),
      "preserve",
      "--config",
      str(config_path),
    ],
    "RunAtLoad": True,
    "StandardErrorPath": str(stderr_path),
    "StandardOutPath": str(stdout_path),
    "StartInterval": 1800,
  }

  removed = scheduler.uninstall_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=config_path,
    interval_seconds=1800,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )
  missing = scheduler.uninstall_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=config_path,
    interval_seconds=1800,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )
  assert removed.action == "uninstalled"
  assert missing.action == "unchanged"
  assert not plist_path.exists()


def test_scheduler_preserves_unowned_target_and_rejects_unsafe_inputs(
  tmp_path,
):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  plist_path = tmp_path / "LaunchAgents" / "session-logs.plist"
  plist_path.parent.mkdir()
  plist_path.write_bytes(b"unowned schedule\n")

  result = scheduler.install_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=tmp_path / "session-logs.json",
    interval_seconds=60,
    stdout_path=tmp_path / "stdout.log",
    stderr_path=tmp_path / "stderr.log",
  )
  removed = scheduler.uninstall_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=tmp_path / "session-logs.json",
    interval_seconds=60,
    stdout_path=tmp_path / "stdout.log",
    stderr_path=tmp_path / "stderr.log",
  )

  assert result.action == "preserved"
  assert removed.action == "preserved"
  assert plist_path.read_bytes() == b"unowned schedule\n"

  try:
    scheduler.build_launchd_schedule(
      python_executable="python3",
      config_path=tmp_path / "session-logs.json",
      interval_seconds=0,
      stdout_path=tmp_path / "stdout.log",
      stderr_path=tmp_path / "stderr.log",
    )
  except scheduler.ScheduleError as error:
    assert str(error) == "Unsafe launchd schedule inputs"
  else:
    raise AssertionError("unsafe schedule inputs must be rejected")


def test_scheduled_command_runs_outside_repository_cwd(tmp_path):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  raw_log = tmp_path / "raw" / "session.jsonl"
  raw_log.parent.mkdir()
  raw_log.write_text(
    '{"uuid":"user-1","type":"user","sessionId":"session-1",'
    '"message":{"role":"user","content":"Preserve."}}\n',
    encoding="utf-8",
  )
  config_path = tmp_path / "session-logs.json"
  config_path.write_text(
    '{"raw_root":"raw","transcript_root":"transcripts",'
    '"summary_root":"summaries","provenance_root":"provenance",'
    '"backup_root":"private-backup","preservation_enabled":true,'
    '"tool_version":"0.0.1","redaction_rules":[]}\n',
    encoding="utf-8",
  )
  schedule = scheduler.build_launchd_schedule(
    python_executable=sys.executable,
    config_path=config_path,
    interval_seconds=60,
    stdout_path=tmp_path / "stdout.jsonl",
    stderr_path=tmp_path / "stderr.log",
  )
  settings = plistlib.loads(schedule)
  outside_cwd = tmp_path / "outside-cwd"
  outside_cwd.mkdir()

  completed = subprocess.run(
    settings["ProgramArguments"],
    cwd=outside_cwd,
    capture_output=True,
    check=False,
    text=True,
  )

  assert completed.returncode == 0
  assert (
    tmp_path / "private-backup" / "session.jsonl"
  ).read_bytes() == raw_log.read_bytes()


def test_launchd_activation_reports_running_and_stopped_idempotently(
  tmp_path,
):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  plist_path = tmp_path / "LaunchAgents" / "session-logs.plist"
  scheduler.install_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=tmp_path / "session-logs.json",
    interval_seconds=60,
    stdout_path=tmp_path / "stdout.log",
    stderr_path=tmp_path / "stderr.log",
  )
  running = False
  commands = []

  def fake_run(command, **_kwargs):
    nonlocal running
    commands.append(command)
    if command[1] == "print":
      return SimpleNamespace(returncode=0 if running else 1)
    if command[1] == "bootstrap":
      running = True
      return SimpleNamespace(returncode=0)
    if command[1] == "bootout":
      running = False
      return SimpleNamespace(returncode=0)
    raise AssertionError("unexpected launchctl command")

  activated = scheduler.activate_launchd_schedule(
    plist_path,
    uid=501,
    runner=fake_run,
  )
  repeated = scheduler.activate_launchd_schedule(
    plist_path,
    uid=501,
    runner=fake_run,
  )
  stopped = scheduler.deactivate_launchd_schedule(
    plist_path,
    uid=501,
    runner=fake_run,
  )
  repeated_stop = scheduler.deactivate_launchd_schedule(
    plist_path,
    uid=501,
    runner=fake_run,
  )

  assert activated == scheduler.ActivationResult(
    action="activated",
    status="running",
  )
  assert repeated == scheduler.ActivationResult(
    action="unchanged",
    status="running",
  )
  assert stopped == scheduler.ActivationResult(
    action="deactivated",
    status="stopped",
  )
  assert repeated_stop == scheduler.ActivationResult(
    action="unchanged",
    status="stopped",
  )
  assert commands[0] == [
    "/bin/launchctl",
    "print",
    "gui/501/com.reviewcompass.session-log-preservation",
  ]
  assert commands[1] == [
    "/bin/launchctl",
    "bootstrap",
    "gui/501",
    str(plist_path),
  ]


def test_launchd_activation_failure_is_safe_and_value_free(tmp_path):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  plist_path = tmp_path / "LaunchAgents" / "session-logs.plist"
  scheduler.install_launchd_schedule(
    plist_path,
    python_executable="/usr/bin/python3",
    config_path=tmp_path / "session-logs.json",
    interval_seconds=60,
    stdout_path=tmp_path / "stdout.log",
    stderr_path=tmp_path / "stderr.log",
  )

  def failing_run(command, **_kwargs):
    return SimpleNamespace(
      returncode=1 if command[1] == "print" else 5,
      stdout="private launchctl output",
      stderr="private launchctl error",
    )

  result = scheduler.activate_launchd_schedule(
    plist_path,
    uid=501,
    runner=failing_run,
  )

  assert result == scheduler.ActivationResult(
    action="failed",
    status="stopped",
    reason="exit_code_5",
  )
  assert "private launchctl" not in repr(result)


def _schedule_arguments(tmp_path, operation, *extra):
  return (
    operation,
    "--plist",
    str(tmp_path / "LaunchAgents" / "session-logs.plist"),
    "--python",
    sys.executable,
    "--config",
    str(tmp_path / "session-logs.json"),
    "--interval",
    "60",
    "--stdout",
    str(tmp_path / "private-logs" / "stdout.jsonl"),
    "--stderr",
    str(tmp_path / "private-logs" / "stderr.log"),
    "--uid",
    "501",
    *extra,
  )


def test_schedule_cli_dry_run_and_install_prepare_only_explicit_paths(
  tmp_path,
  capsys,
):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  entry = importlib.import_module("tools.session_logs.entry")
  dry_arguments = _schedule_arguments(tmp_path, "install", "--dry-run")

  assert entry.run(("schedule", *dry_arguments)) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "planned",
    "operation": "install",
    "status": "ok",
  }
  assert not (tmp_path / "LaunchAgents").exists()
  assert not (tmp_path / "private-logs").exists()

  assert scheduler.run(_schedule_arguments(tmp_path, "install")) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "installed",
    "operation": "install",
    "status": "ok",
  }
  assert (
    tmp_path / "LaunchAgents" / "session-logs.plist"
  ).is_file()
  assert (tmp_path / "private-logs").is_dir()


def test_schedule_cli_reports_injected_launchd_status(
  tmp_path,
  capsys,
):
  scheduler = importlib.import_module("tools.session_logs.scheduler")
  scheduler.run(_schedule_arguments(tmp_path, "install"))
  capsys.readouterr()

  def running(_command, **_kwargs):
    return SimpleNamespace(returncode=0)

  assert scheduler.run(
    _schedule_arguments(tmp_path, "status"),
    runner=running,
  ) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "inspected",
    "operation": "status",
    "status": "running",
  }
