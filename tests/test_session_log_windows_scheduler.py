"""Windows Task Schedulerバックエンドの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path
from types import SimpleNamespace


def _request(tmp_path, backends):
  return backends.PeriodicScheduleRequest(
    schedule_path=tmp_path / "tasks" / "session-logs.xml",
    python_executable=Path("/usr/bin/python3"),
    config_path=tmp_path / "config" / "session-logs.json",
    interval_seconds=300,
    stdout_path=tmp_path / "logs" / "stdout.log",
    stderr_path=tmp_path / "logs" / "stderr.log",
    user_id=501,
  )


def test_windows_backend_dry_run_and_idempotent_definition(tmp_path):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  backend = backends.select_schedule_backend(
    platform_name="win32",
  )
  request = _request(tmp_path, backends)

  assert backend.run(
    "install",
    request,
    dry_run=True,
  ) == backends.ScheduleBackendResult(
    backend="windows_task",
    action="planned",
    status="ok",
  )
  assert not request.schedule_path.exists()

  assert backend.run(
    "install",
    request,
  ) == backends.ScheduleBackendResult(
    backend="windows_task",
    action="installed",
    status="ok",
  )
  definition = request.schedule_path.read_text(encoding="utf-8")
  assert str(request.config_path) in definition
  assert "PT300S" in definition
  assert backend.run("install", request).action == "unchanged"


def test_windows_backend_registration_status_and_owned_uninstall(
  tmp_path,
):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  commands = []
  registered = {"value": False}

  def runner(command, **_arguments):
    commands.append(command)
    if command[1] == "/Query":
      return SimpleNamespace(
        returncode=0 if registered["value"] else 1,
        stdout="private output",
        stderr="private error",
      )
    if command[1] == "/Create":
      registered["value"] = True
    if command[1] == "/Delete":
      registered["value"] = False
    return SimpleNamespace(
      returncode=0,
      stdout="private output",
      stderr="private error",
    )

  backend = backends.WindowsTaskBackend(runner=runner)
  request = _request(tmp_path, backends)
  assert backend.run("install", request).action == "installed"

  activated = backend.run("activate", request)
  assert activated == backends.ScheduleBackendResult(
    backend="windows_task",
    action="activated",
    status="running",
  )
  assert backend.run("status", request).status == "running"

  deactivated = backend.run("deactivate", request)
  assert deactivated == backends.ScheduleBackendResult(
    backend="windows_task",
    action="deactivated",
    status="stopped",
  )
  assert backend.run("uninstall", request).action == "uninstalled"
  assert not request.schedule_path.exists()
  assert "private output" not in repr(activated)
  assert commands


def test_windows_backend_preserves_unowned_definition(tmp_path):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  request = _request(tmp_path, backends)
  request.schedule_path.parent.mkdir()
  request.schedule_path.write_text("unowned\n", encoding="utf-8")
  backend = backends.WindowsTaskBackend()

  result = backend.run("install", request)

  assert result.action == "preserved"
  assert result.status == "error"
  assert request.schedule_path.read_text(encoding="utf-8") == (
    "unowned\n"
  )
