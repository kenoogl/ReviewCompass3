"""systemd userによる定期保全。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import os
import subprocess
from pathlib import Path


class SystemdScheduleError(Exception):
  """所有していないsystemd user unitの操作を拒否する。"""


def _absolute_path(value):
  path = Path(value)
  if not path.is_absolute():
    raise SystemdScheduleError(
      "Unsafe systemd schedule inputs"
    )
  return path


def _unit_value(value):
  text = str(value)
  if any(character in text for character in ("\0", "\n", "\r")):
    raise SystemdScheduleError(
      "Unsafe systemd schedule inputs"
    )
  return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_systemd_units(
  *,
  timer_path,
  python_executable,
  config_path,
  interval_seconds,
  stdout_path,
  stderr_path,
):
  timer = _absolute_path(timer_path)
  if timer.suffix != ".timer":
    raise SystemdScheduleError(
      "Unsafe systemd schedule inputs"
    )
  python_path = _absolute_path(python_executable)
  config = _absolute_path(config_path)
  standard_output = _absolute_path(stdout_path)
  standard_error = _absolute_path(stderr_path)
  if (
    isinstance(interval_seconds, bool)
    or not isinstance(interval_seconds, int)
    or interval_seconds <= 0
  ):
    raise SystemdScheduleError(
      "Unsafe systemd schedule inputs"
    )
  service = timer.with_suffix(".service")
  entry_path = Path(__file__).with_name("entry.py").resolve()
  service_text = "\n".join((
    "[Unit]",
    "Description=ReviewCompass3 session log preservation",
    "",
    "[Service]",
    "Type=oneshot",
    "ExecStart=%s %s preserve --config %s" % (
      _unit_value(python_path),
      _unit_value(entry_path),
      _unit_value(config),
    ),
    "StandardOutput=append:%s" % standard_output,
    "StandardError=append:%s" % standard_error,
    "",
  ))
  timer_text = "\n".join((
    "[Unit]",
    "Description=ReviewCompass3 session log preservation timer",
    "",
    "[Timer]",
    "OnBootSec=60s",
    "OnUnitActiveSec=%ds" % interval_seconds,
    "Unit=%s" % service.name,
    "",
    "[Install]",
    "WantedBy=timers.target",
    "",
  ))
  return (
    service,
    service_text.encode("utf-8"),
    timer_text.encode("utf-8"),
  )


def _expected(request):
  return build_systemd_units(
    timer_path=request["timer_path"],
    python_executable=request["python_executable"],
    config_path=request["config_path"],
    interval_seconds=request["interval_seconds"],
    stdout_path=request["stdout_path"],
    stderr_path=request["stderr_path"],
  )


def _install(request):
  timer = Path(request["timer_path"])
  service, service_bytes, timer_bytes = _expected(request)
  if timer.exists() or service.exists():
    try:
      owned = (
        timer.is_file()
        and service.is_file()
        and timer.read_bytes() == timer_bytes
        and service.read_bytes() == service_bytes
      )
    except OSError as error:
      raise SystemdScheduleError(
        "Cannot inspect systemd units"
      ) from error
    return "unchanged" if owned else "preserved"
  timer_tmp = timer.with_name(timer.name + ".tmp")
  service_tmp = service.with_name(service.name + ".tmp")
  installed_service = False
  try:
    timer.parent.mkdir(parents=True, exist_ok=True)
    Path(request["stdout_path"]).parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    Path(request["stderr_path"]).parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    timer_tmp.write_bytes(timer_bytes)
    service_tmp.write_bytes(service_bytes)
    os.replace(service_tmp, service)
    installed_service = True
    os.replace(timer_tmp, timer)
  except OSError as error:
    if installed_service and not timer.exists():
      service.unlink(missing_ok=True)
    raise SystemdScheduleError(
      "Cannot install systemd units"
    ) from error
  finally:
    timer_tmp.unlink(missing_ok=True)
    service_tmp.unlink(missing_ok=True)
  return "installed"


def _validate_owned(request):
  timer = Path(request["timer_path"])
  service, service_bytes, timer_bytes = _expected(request)
  try:
    if (
      not timer.is_file()
      or not service.is_file()
      or timer.read_bytes() != timer_bytes
      or service.read_bytes() != service_bytes
    ):
      raise SystemdScheduleError("Unowned systemd units")
  except OSError as error:
    raise SystemdScheduleError(
      "Cannot inspect systemd units"
    ) from error
  return timer, service


def _systemctl(runner, *arguments):
  try:
    return runner(
      ["/usr/bin/systemctl", "--user", *arguments],
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise SystemdScheduleError(
      "Cannot execute systemctl"
    ) from error


def _is_active(timer, runner):
  return _systemctl(
    runner,
    "is-active",
    timer.name,
  ).returncode == 0


def _print_result(operation, action, status, reason=None):
  payload = {
    "action": action,
    "operation": operation,
    "status": status,
  }
  if reason is not None:
    payload["reason"] = reason
  print(json.dumps(payload, sort_keys=True))


def run(argv=None, *, runner=subprocess.run) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "operation",
    choices=(
      "install",
      "activate",
      "status",
      "deactivate",
      "uninstall",
    ),
  )
  parser.add_argument("--timer", required=True)
  parser.add_argument("--python", required=True)
  parser.add_argument("--config", required=True)
  parser.add_argument("--interval", required=True, type=int)
  parser.add_argument("--stdout", required=True)
  parser.add_argument("--stderr", required=True)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  request = {
    "timer_path": args.timer,
    "python_executable": args.python,
    "config_path": args.config,
    "interval_seconds": args.interval,
    "stdout_path": args.stdout,
    "stderr_path": args.stderr,
  }
  try:
    _expected(request)
    if args.dry_run:
      _print_result(args.operation, "planned", "ok")
      return 0
    if args.operation == "install":
      action = _install(request)
      status = "error" if action == "preserved" else "ok"
    else:
      timer, service = _validate_owned(request)
      if args.operation == "status":
        action = "inspected"
        status = (
          "running"
          if _is_active(timer, runner)
          else "stopped"
        )
      elif args.operation == "activate":
        if _is_active(timer, runner):
          action = "unchanged"
          status = "running"
        else:
          result = _systemctl(
            runner,
            "enable",
            "--now",
            timer.name,
          )
          action = "activated" if result.returncode == 0 else "failed"
          status = "running" if result.returncode == 0 else "stopped"
      elif args.operation == "deactivate":
        if not _is_active(timer, runner):
          action = "unchanged"
          status = "stopped"
        else:
          result = _systemctl(
            runner,
            "disable",
            "--now",
            timer.name,
          )
          action = "deactivated" if result.returncode == 0 else "failed"
          status = "stopped" if result.returncode == 0 else "running"
      else:
        timer.unlink()
        service.unlink()
        action = "uninstalled"
        status = "ok"
  except Exception as error:
    _print_result(
      args.operation,
      "failed",
      "error",
      type(error).__name__,
    )
    return 5
  _print_result(args.operation, action, status)
  return 5 if action in ("failed", "preserved") else 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
