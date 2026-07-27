"""OS別定期実行バックエンド境界の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path

import pytest


@pytest.mark.parametrize(
  ("platform_name", "backend_id"),
  (
    ("darwin", "launchd"),
    ("linux", "systemd_user"),
    ("win32", "windows_task"),
  ),
)
def test_routes_platforms_through_common_backend_boundary(
  platform_name,
  backend_id,
):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  selected = object()

  assert backends.select_schedule_backend(
    platform_name=platform_name,
    registry={backend_id: selected},
  ) is selected


def test_launchd_adapter_reuses_existing_dry_run_without_writes(
  tmp_path,
):
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  request = backends.PeriodicScheduleRequest(
    schedule_path=tmp_path / "LaunchAgents" / "session-logs.plist",
    python_executable=Path("/usr/bin/python3"),
    config_path=tmp_path / "config" / "session-logs.json",
    interval_seconds=300,
    stdout_path=tmp_path / "logs" / "stdout.log",
    stderr_path=tmp_path / "logs" / "stderr.log",
    user_id=501,
  )

  result = backends.LaunchdBackend().run(
    "install",
    request,
    dry_run=True,
  )

  assert result == backends.ScheduleBackendResult(
    backend="launchd",
    action="planned",
    status="ok",
  )
  assert not request.schedule_path.exists()
  assert not request.stdout_path.parent.exists()


def test_unregistered_platform_backend_fails_closed():
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )

  with pytest.raises(backends.ScheduleBackendError) as error:
    backends.select_schedule_backend(
      platform_name="linux",
      registry={"launchd": object()},
    )

  assert str(error.value) == "Schedule backend is unavailable"
