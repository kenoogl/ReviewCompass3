"""セッション開始・終了時に呼び出す安全な入口。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import shlex
from pathlib import Path

from tools.session_logs.cli import run as run_cli
from tools.session_logs.locking import exclusive_lock


@dataclasses.dataclass(frozen=True)
class HookResult:
  action: str
  exit_code: int
  operation_exit_code: int = 0


@dataclasses.dataclass(frozen=True)
class HookCommands:
  start: str
  end: str


def build_hook_commands(
  python_executable,
  config_path,
  *,
  event_log_path=None,
) -> HookCommands:
  base = [
    str(python_executable),
    "-m",
    "tools.session_logs.hooks",
  ]
  config_arguments = ["--config", str(config_path)]
  if event_log_path is not None:
    config_arguments.extend([
      "--event-log",
      str(event_log_path),
    ])
  return HookCommands(
    start=shlex.join(base + ["start"] + config_arguments),
    end=shlex.join(base + ["end"] + config_arguments),
  )


def _record_hook_event(path, *, phase, result, reason=None):
  if path is None:
    return
  event_path = Path(path)
  payload = {
    "action": result.action,
    "phase": phase,
    "status": (
      "completed"
      if result.operation_exit_code == 0
      else "failed"
    ),
  }
  if reason is not None:
    payload["reason"] = reason
  try:
    event_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = event_path.with_name(event_path.name + ".lock")
    with exclusive_lock(lock_path, timeout_seconds=60):
      with event_path.open("a", encoding="utf-8") as output:
        output.write(json.dumps(
          payload,
          ensure_ascii=False,
          sort_keys=True,
        ) + "\n")
  except Exception:
    pass


def _run_hook(
  phase,
  config_path,
  *,
  enabled,
  event_log_path,
) -> HookResult:
  if not enabled or config_path is None:
    return HookResult(action="skipped", exit_code=0)
  arguments = ["--config", str(config_path)]
  if phase == "start":
    arguments.append("--dry-run")
  try:
    operation_exit_code = run_cli(tuple(arguments))
    reason = (
      None
      if operation_exit_code == 0
      else "exit_code_%d" % operation_exit_code
    )
  except Exception as error:
    operation_exit_code = 1
    reason = type(error).__name__
  result = HookResult(
    action=(
      "checked" if phase == "start" else "stored"
    ) if operation_exit_code == 0 else "failed",
    exit_code=0,
    operation_exit_code=operation_exit_code,
  )
  _record_hook_event(
    event_log_path,
    phase=phase,
    result=result,
    reason=reason,
  )
  return result


def run_start_hook(
  config_path,
  *,
  enabled=True,
  event_log_path=None,
) -> HookResult:
  return _run_hook(
    "start",
    config_path,
    enabled=enabled,
    event_log_path=event_log_path,
  )


def run_end_hook(
  config_path,
  *,
  enabled=True,
  event_log_path=None,
) -> HookResult:
  return _run_hook(
    "end",
    config_path,
    enabled=enabled,
    event_log_path=event_log_path,
  )


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("phase", choices=("start", "end"))
  parser.add_argument("--config", required=True)
  parser.add_argument("--event-log")
  args = parser.parse_args(argv)
  if args.phase == "start":
    return run_start_hook(
      args.config,
      event_log_path=args.event_log,
    ).exit_code
  return run_end_hook(
    args.config,
    event_log_path=args.event_log,
  ).exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
