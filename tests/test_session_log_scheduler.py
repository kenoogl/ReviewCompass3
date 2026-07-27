"""セッション非利用期間の定期保全設定の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import plistlib


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
  assert settings == {
    "Label": "com.reviewcompass.session-log-preservation",
    "ProgramArguments": [
      "/usr/bin/python3",
      "-m",
      "tools.session_logs.cli",
      "--config",
      str(config_path),
      "--preserve-only",
      "--json-lines",
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
