"""systemd user定期実行バックエンドの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path
from types import SimpleNamespace


def _request(tmp_path, backends):
  return backends.PeriodicScheduleRequest(
    schedule_path=(
      tmp_path
      / "systemd"
      / "reviewcompass3-session-logs.timer"
    ),
    python_executable=Path("/usr/bin/python3"),
    config_path=tmp_path / "config" / "session-logs.json",
    interval_seconds=300,
    stdout_path=tmp_path / "logs" / "stdout.log",
    stderr_path=tmp_path / "logs" / "stderr.log",
    user_id=501,
  )


def test_systemd_backend_dry_run_and_idempotent_install(tmp_path):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  backend = backends.select_schedule_backend(
    platform_name="linux",
  )
  request = _request(tmp_path, backends)

  assert backend.run(
    "install",
    request,
    dry_run=True,
  ) == backends.ScheduleBackendResult(
    backend="systemd_user",
    action="planned",
    status="ok",
  )
  assert not request.schedule_path.exists()

  assert backend.run(
    "install",
    request,
  ) == backends.ScheduleBackendResult(
    backend="systemd_user",
    action="installed",
    status="ok",
  )
  service_path = request.schedule_path.with_suffix(".service")
  assert request.schedule_path.is_file()
  assert service_path.is_file()
  service = service_path.read_text(encoding="utf-8")
  timer = request.schedule_path.read_text(encoding="utf-8")
  assert str(request.config_path) in service
  assert "OnUnitActiveSec=300s" in timer

  assert backend.run(
    "install",
    request,
  ).action == "unchanged"


def test_systemd_backend_status_activation_and_owned_uninstall(
  tmp_path,
):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  commands = []
  active = {"value": False}

  def runner(command, **_arguments):
    commands.append(command)
    if command[2] == "is-active":
      return SimpleNamespace(
        returncode=0 if active["value"] else 3,
        stdout="private output",
        stderr="private error",
      )
    if command[2:4] == ["enable", "--now"]:
      active["value"] = True
    if command[2:4] == ["disable", "--now"]:
      active["value"] = False
    return SimpleNamespace(
      returncode=0,
      stdout="private output",
      stderr="private error",
    )

  backend = backends.SystemdUserBackend(runner=runner)
  request = _request(tmp_path, backends)
  assert backend.run("install", request).action == "installed"

  activated = backend.run("activate", request)
  assert activated == backends.ScheduleBackendResult(
    backend="systemd_user",
    action="activated",
    status="running",
  )
  assert backend.run("status", request).status == "running"

  deactivated = backend.run("deactivate", request)
  assert deactivated == backends.ScheduleBackendResult(
    backend="systemd_user",
    action="deactivated",
    status="stopped",
  )
  assert backend.run("uninstall", request).action == "uninstalled"
  assert not request.schedule_path.exists()
  assert not request.schedule_path.with_suffix(".service").exists()
  assert all("private" not in repr(command) for command in commands)


def test_systemd_backend_preserves_unowned_unit(tmp_path):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  request = _request(tmp_path, backends)
  request.schedule_path.parent.mkdir()
  request.schedule_path.write_text("unowned\n", encoding="utf-8")
  service_path = request.schedule_path.with_suffix(".service")
  service_path.write_text("unowned\n", encoding="utf-8")
  backend = backends.SystemdUserBackend()

  result = backend.run("install", request)

  assert result.action == "preserved"
  assert result.status == "error"
  assert request.schedule_path.read_text(encoding="utf-8") == (
    "unowned\n"
  )
