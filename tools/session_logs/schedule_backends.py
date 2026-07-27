"""OS別定期実行を共通境界へ接続する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import contextlib
import dataclasses
import io
import json
import sys
from pathlib import Path

from tools.session_logs import scheduler


class ScheduleBackendError(Exception):
  """定期実行バックエンドを安全に使用できない。"""


@dataclasses.dataclass(frozen=True)
class PeriodicScheduleRequest:
  schedule_path: Path
  python_executable: Path
  config_path: Path
  interval_seconds: int
  stdout_path: Path
  stderr_path: Path
  user_id: int


@dataclasses.dataclass(frozen=True)
class ScheduleBackendResult:
  backend: str
  action: str
  status: str
  reason: object = None


class LaunchdBackend:
  backend_id = "launchd"

  def run(self, operation, request, *, dry_run=False):
    arguments = [
      operation,
      "--plist",
      str(request.schedule_path),
      "--python",
      str(request.python_executable),
      "--config",
      str(request.config_path),
      "--interval",
      str(request.interval_seconds),
      "--stdout",
      str(request.stdout_path),
      "--stderr",
      str(request.stderr_path),
      "--uid",
      str(request.user_id),
    ]
    if dry_run:
      arguments.append("--dry-run")
    output = io.StringIO()
    try:
      with contextlib.redirect_stdout(output):
        scheduler.run(tuple(arguments))
      payload = json.loads(output.getvalue())
      action = payload["action"]
      status = payload["status"]
    except Exception as error:
      raise ScheduleBackendError(
        "Schedule backend execution failed"
      ) from error
    return ScheduleBackendResult(
      backend=self.backend_id,
      action=action,
      status=status,
      reason=payload.get("reason"),
    )


class SystemdUserBackend:
  backend_id = "systemd_user"

  def __init__(self, *, runner=None):
    self.runner = runner

  def run(self, operation, request, *, dry_run=False):
    from tools.session_logs import systemd_scheduler
    arguments = [
      operation,
      "--timer",
      str(request.schedule_path),
      "--python",
      str(request.python_executable),
      "--config",
      str(request.config_path),
      "--interval",
      str(request.interval_seconds),
      "--stdout",
      str(request.stdout_path),
      "--stderr",
      str(request.stderr_path),
    ]
    if dry_run:
      arguments.append("--dry-run")
    output = io.StringIO()
    try:
      with contextlib.redirect_stdout(output):
        if self.runner is None:
          systemd_scheduler.run(tuple(arguments))
        else:
          systemd_scheduler.run(
            tuple(arguments),
            runner=self.runner,
          )
      payload = json.loads(output.getvalue())
    except Exception as error:
      raise ScheduleBackendError(
        "Schedule backend execution failed"
      ) from error
    return ScheduleBackendResult(
      backend=self.backend_id,
      action=payload["action"],
      status=payload["status"],
      reason=payload.get("reason"),
    )


class WindowsTaskBackend:
  backend_id = "windows_task"

  def __init__(self, *, runner=None):
    self.runner = runner

  def run(self, operation, request, *, dry_run=False):
    from tools.session_logs import windows_scheduler
    arguments = [
      operation,
      "--definition",
      str(request.schedule_path),
      "--python",
      str(request.python_executable),
      "--config",
      str(request.config_path),
      "--interval",
      str(request.interval_seconds),
    ]
    if dry_run:
      arguments.append("--dry-run")
    output = io.StringIO()
    try:
      with contextlib.redirect_stdout(output):
        if self.runner is None:
          windows_scheduler.run(tuple(arguments))
        else:
          windows_scheduler.run(
            tuple(arguments),
            runner=self.runner,
          )
      payload = json.loads(output.getvalue())
    except Exception as error:
      raise ScheduleBackendError(
        "Schedule backend execution failed"
      ) from error
    return ScheduleBackendResult(
      backend=self.backend_id,
      action=payload["action"],
      status=payload["status"],
      reason=payload.get("reason"),
    )


_PLATFORM_BACKEND_IDS = {
  "darwin": "launchd",
  "linux": "systemd_user",
  "win32": "windows_task",
}


def select_schedule_backend(
  *,
  platform_name=None,
  registry=None,
):
  selected_platform = (
    sys.platform
    if platform_name is None
    else platform_name
  )
  backend_id = _PLATFORM_BACKEND_IDS.get(selected_platform)
  available = (
    {
      "launchd": LaunchdBackend(),
      "systemd_user": SystemdUserBackend(),
      "windows_task": WindowsTaskBackend(),
    }
    if registry is None
    else registry
  )
  backend = available.get(backend_id)
  if backend is None:
    raise ScheduleBackendError(
      "Schedule backend is unavailable"
    )
  return backend


def run_periodic_schedule(
  operation,
  request,
  *,
  dry_run=False,
  platform_name=None,
  registry=None,
) -> ScheduleBackendResult:
  backend = select_schedule_backend(
    platform_name=platform_name,
    registry=registry,
  )
  try:
    return backend.run(
      operation,
      request,
      dry_run=dry_run,
    )
  except ScheduleBackendError:
    raise
  except Exception as error:
    raise ScheduleBackendError(
      "Schedule backend execution failed"
    ) from error
