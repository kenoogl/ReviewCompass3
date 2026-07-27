"""セッション非利用期間に生ログを保全するLaunchAgent設定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import os
import plistlib
import subprocess
from pathlib import Path


LABEL = "com.reviewcompass.session-log-preservation"


class ScheduleError(Exception):
  """定期保全設定を安全に生成または更新できない。"""


@dataclasses.dataclass(frozen=True)
class ScheduleResult:
  action: str
  plist_path: Path


@dataclasses.dataclass(frozen=True)
class ActivationResult:
  action: str
  status: str
  reason: object = None


def _absolute_path(value):
  path = Path(value)
  if not path.is_absolute():
    raise ScheduleError("Unsafe launchd schedule inputs")
  return path


def build_launchd_schedule(
  *,
  python_executable,
  config_path,
  interval_seconds,
  stdout_path,
  stderr_path,
) -> bytes:
  python_path = _absolute_path(python_executable)
  config = _absolute_path(config_path)
  standard_output = _absolute_path(stdout_path)
  standard_error = _absolute_path(stderr_path)
  entry_path = Path(__file__).with_name("entry.py").resolve()
  if (
    isinstance(interval_seconds, bool)
    or not isinstance(interval_seconds, int)
    or interval_seconds <= 0
  ):
    raise ScheduleError("Unsafe launchd schedule inputs")
  settings = {
    "Label": LABEL,
    "ProgramArguments": [
      str(python_path),
      str(entry_path),
      "preserve",
      "--config",
      str(config),
    ],
    "RunAtLoad": True,
    "StandardErrorPath": str(standard_error),
    "StandardOutPath": str(standard_output),
    "StartInterval": interval_seconds,
  }
  return plistlib.dumps(
    settings,
    fmt=plistlib.FMT_XML,
    sort_keys=True,
  )


def _expected_schedule(
  *,
  python_executable,
  config_path,
  interval_seconds,
  stdout_path,
  stderr_path,
):
  return build_launchd_schedule(
    python_executable=python_executable,
    config_path=config_path,
    interval_seconds=interval_seconds,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )


def install_launchd_schedule(
  plist_path,
  *,
  python_executable,
  config_path,
  interval_seconds,
  stdout_path,
  stderr_path,
) -> ScheduleResult:
  path = _absolute_path(plist_path)
  expected = _expected_schedule(
    python_executable=python_executable,
    config_path=config_path,
    interval_seconds=interval_seconds,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )
  try:
    if path.exists():
      action = (
        "unchanged"
        if path.read_bytes() == expected
        else "preserved"
      )
      return ScheduleResult(action=action, plist_path=path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(path.name + ".tmp")
    temporary_path.write_bytes(expected)
    os.replace(temporary_path, path)
  except OSError as error:
    raise ScheduleError("Cannot install launchd schedule") from error
  finally:
    if "temporary_path" in locals():
      temporary_path.unlink(missing_ok=True)
  return ScheduleResult(action="installed", plist_path=path)


def uninstall_launchd_schedule(
  plist_path,
  *,
  python_executable,
  config_path,
  interval_seconds,
  stdout_path,
  stderr_path,
) -> ScheduleResult:
  path = _absolute_path(plist_path)
  expected = _expected_schedule(
    python_executable=python_executable,
    config_path=config_path,
    interval_seconds=interval_seconds,
    stdout_path=stdout_path,
    stderr_path=stderr_path,
  )
  try:
    if not path.exists():
      return ScheduleResult(action="unchanged", plist_path=path)
    if path.read_bytes() != expected:
      return ScheduleResult(action="preserved", plist_path=path)
    path.unlink()
  except OSError as error:
    raise ScheduleError("Cannot uninstall launchd schedule") from error
  return ScheduleResult(action="uninstalled", plist_path=path)


def _launchd_domain(uid):
  if (
    isinstance(uid, bool)
    or not isinstance(uid, int)
    or uid < 0
  ):
    raise ScheduleError("Unsafe launchd activation inputs")
  return "gui/%d" % uid


def _validate_owned_schedule(path):
  plist_path = _absolute_path(path)
  try:
    settings = plistlib.loads(plist_path.read_bytes())
  except (OSError, ValueError) as error:
    raise ScheduleError("Cannot read launchd schedule") from error
  arguments = settings.get("ProgramArguments")
  expected_entry = str(
    Path(__file__).with_name("entry.py").resolve()
  )
  if (
    settings.get("Label") != LABEL
    or not isinstance(arguments, list)
    or len(arguments) < 3
    or arguments[1:3] != [expected_entry, "preserve"]
  ):
    raise ScheduleError("Unowned launchd schedule")
  return plist_path


def _run_launchctl(runner, command):
  try:
    return runner(
      command,
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise ScheduleError("Cannot execute launchctl") from error


def _is_running(domain, runner):
  result = _run_launchctl(
    runner,
    [
      "/bin/launchctl",
      "print",
      "%s/%s" % (domain, LABEL),
    ],
  )
  return result.returncode == 0


def activate_launchd_schedule(
  plist_path,
  *,
  uid,
  runner=subprocess.run,
) -> ActivationResult:
  path = _validate_owned_schedule(plist_path)
  domain = _launchd_domain(uid)
  if _is_running(domain, runner):
    return ActivationResult(
      action="unchanged",
      status="running",
    )
  result = _run_launchctl(
    runner,
    [
      "/bin/launchctl",
      "bootstrap",
      domain,
      str(path),
    ],
  )
  if result.returncode != 0:
    return ActivationResult(
      action="failed",
      status="stopped",
      reason="exit_code_%d" % result.returncode,
    )
  return ActivationResult(
    action="activated",
    status="running",
  )


def deactivate_launchd_schedule(
  plist_path,
  *,
  uid,
  runner=subprocess.run,
) -> ActivationResult:
  path = _validate_owned_schedule(plist_path)
  domain = _launchd_domain(uid)
  if not _is_running(domain, runner):
    return ActivationResult(
      action="unchanged",
      status="stopped",
    )
  result = _run_launchctl(
    runner,
    [
      "/bin/launchctl",
      "bootout",
      domain,
      str(path),
    ],
  )
  if result.returncode != 0:
    return ActivationResult(
      action="failed",
      status="running",
      reason="exit_code_%d" % result.returncode,
    )
  return ActivationResult(
    action="deactivated",
    status="stopped",
  )


def inspect_launchd_schedule(
  plist_path,
  *,
  uid,
  runner=subprocess.run,
) -> ActivationResult:
  _validate_owned_schedule(plist_path)
  domain = _launchd_domain(uid)
  return ActivationResult(
    action="inspected",
    status=(
      "running"
      if _is_running(domain, runner)
      else "stopped"
    ),
  )


def _print_cli_result(operation, action, status, reason=None):
  payload = {
    "action": action,
    "operation": operation,
    "status": status,
  }
  if reason is not None:
    payload["reason"] = reason
  print(json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
  ))


def _prepare_log_directories(stdout_path, stderr_path):
  try:
    Path(stdout_path).parent.mkdir(parents=True, exist_ok=True)
    Path(stderr_path).parent.mkdir(parents=True, exist_ok=True)
  except OSError as error:
    raise ScheduleError(
      "Cannot prepare launchd log directories"
    ) from error


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
  parser.add_argument("--plist", required=True)
  parser.add_argument("--python", required=True)
  parser.add_argument("--config", required=True)
  parser.add_argument("--interval", required=True, type=int)
  parser.add_argument("--stdout", required=True)
  parser.add_argument("--stderr", required=True)
  parser.add_argument("--uid", required=True, type=int)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  schedule_arguments = {
    "python_executable": args.python,
    "config_path": args.config,
    "interval_seconds": args.interval,
    "stdout_path": args.stdout,
    "stderr_path": args.stderr,
  }
  try:
    build_launchd_schedule(**schedule_arguments)
    if args.dry_run:
      _print_cli_result(
        args.operation,
        "planned",
        "ok",
      )
      return 0
    if args.operation == "install":
      _prepare_log_directories(args.stdout, args.stderr)
      result = install_launchd_schedule(
        args.plist,
        **schedule_arguments,
      )
      status = "error" if result.action == "preserved" else "ok"
    elif args.operation == "activate":
      result = activate_launchd_schedule(
        args.plist,
        uid=args.uid,
        runner=runner,
      )
      status = result.status
    elif args.operation == "status":
      result = inspect_launchd_schedule(
        args.plist,
        uid=args.uid,
        runner=runner,
      )
      status = result.status
    elif args.operation == "deactivate":
      result = deactivate_launchd_schedule(
        args.plist,
        uid=args.uid,
        runner=runner,
      )
      status = result.status
    else:
      result = uninstall_launchd_schedule(
        args.plist,
        **schedule_arguments,
      )
      status = "error" if result.action == "preserved" else "ok"
  except Exception as error:
    _print_cli_result(
      args.operation,
      "failed",
      "error",
      reason=type(error).__name__,
    )
    return 5
  reason = getattr(result, "reason", None)
  _print_cli_result(
    args.operation,
    result.action,
    status,
    reason=reason,
  )
  return (
    5
    if result.action in ("failed", "preserved")
    else 0
  )


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
