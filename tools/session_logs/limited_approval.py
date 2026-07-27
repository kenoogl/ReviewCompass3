"""限定配置の未承認候補を安全に生成する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import os
import sys
from pathlib import Path


class LimitedApprovalError(Exception):
  """安全な限定配置承認候補を生成できない。"""


_SCHEDULE_SUFFIXES = {
  "darwin": ".plist",
  "linux": ".timer",
  "win32": ".xml",
}


def build_limited_approval(
  *,
  platform,
  raw_root,
  hook_settings,
  schedule_path,
  python_executable,
  interval_seconds,
  user_id,
  deployment_paths,
  runtime_platform=None,
):
  selected_runtime = (
    sys.platform
    if runtime_platform is None
    else runtime_platform
  )
  suffix = _SCHEDULE_SUFFIXES.get(platform)
  explicit_paths = {
    "raw_root": Path(raw_root),
    "hook_settings": Path(hook_settings),
    "schedule_path": Path(schedule_path),
    "python_executable": Path(python_executable),
  }
  standard_paths = (
    Path(deployment_paths.config_file),
    Path(deployment_paths.data_root),
    Path(deployment_paths.state_root),
    Path(deployment_paths.log_root),
  )
  if (
    suffix is None
    or platform != selected_runtime
    or any(not path.is_absolute() for path in explicit_paths.values())
    or any(not path.is_absolute() for path in standard_paths)
    or explicit_paths["schedule_path"].suffix.lower() != suffix
    or isinstance(interval_seconds, bool)
    or not isinstance(interval_seconds, int)
    or interval_seconds <= 0
    or isinstance(user_id, bool)
    or not isinstance(user_id, int)
    or user_id < 0
  ):
    raise LimitedApprovalError(
      "Unsafe limited deployment approval inputs"
    )
  return {
    "approved": False,
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "interval_seconds": interval_seconds,
    "platform": platform,
    "targets": {
      "config_file": str(standard_paths[0]),
      "data_root": str(standard_paths[1]),
      "hook_settings": str(explicit_paths["hook_settings"]),
      "log_root": str(standard_paths[3]),
      "python_executable": str(
        explicit_paths["python_executable"]
      ),
      "raw_root": str(explicit_paths["raw_root"]),
      "schedule_path": str(explicit_paths["schedule_path"]),
      "state_root": str(standard_paths[2]),
    },
    "user_id": user_id,
  }


def install_limited_approval(path, payload):
  output_path = Path(path)
  if not output_path.is_absolute():
    raise LimitedApprovalError(
      "Limited approval output must be absolute"
    )
  encoded = (
    json.dumps(payload, indent=2, sort_keys=True) + "\n"
  ).encode("utf-8")
  if output_path.exists():
    try:
      return (
        "unchanged"
        if output_path.read_bytes() == encoded
        else "preserved"
      )
    except OSError as error:
      raise LimitedApprovalError(
        "Cannot inspect limited approval output"
      ) from error
  temporary_path = output_path.with_name(output_path.name + ".tmp")
  try:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_bytes(encoded)
    os.replace(temporary_path, output_path)
  except OSError as error:
    raise LimitedApprovalError(
      "Cannot write limited approval output"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)
  return "created"


def _print_result(action, status):
  print(json.dumps({
    "action": action,
    "approved": False,
    "status": status,
  }, sort_keys=True))


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--platform",
    required=True,
    choices=("darwin", "linux", "win32"),
  )
  parser.add_argument("--raw-root", required=True)
  parser.add_argument("--hook-settings", required=True)
  parser.add_argument("--schedule", required=True)
  parser.add_argument("--python", required=True)
  parser.add_argument("--interval", required=True, type=int)
  parser.add_argument("--uid", required=True, type=int)
  parser.add_argument("--output", required=True)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  try:
    from tools.session_logs.deployment_paths import (
      resolve_deployment_paths,
    )
    payload = build_limited_approval(
      platform=args.platform,
      raw_root=args.raw_root,
      hook_settings=args.hook_settings,
      schedule_path=args.schedule,
      python_executable=args.python,
      interval_seconds=args.interval,
      user_id=args.uid,
      deployment_paths=resolve_deployment_paths(),
    )
    output_path = Path(args.output)
    if (
      not output_path.is_absolute()
      or str(output_path) in payload["targets"].values()
    ):
      raise LimitedApprovalError(
        "Unsafe limited approval output"
      )
    if args.dry_run:
      _print_result("planned", "ok")
      return 0
    action = install_limited_approval(output_path, payload)
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  status = "error" if action == "preserved" else "ok"
  _print_result(action, status)
  return 5 if action == "preserved" else 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
