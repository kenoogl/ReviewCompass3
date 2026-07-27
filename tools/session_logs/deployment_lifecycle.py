"""ポータブル設定の安全な移行と解除。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import os
from pathlib import Path


class DeploymentLifecycleError(Exception):
  """所有していない配置や不完全な解除を拒否する。"""


@dataclasses.dataclass(frozen=True)
class ConfigMigrationResult:
  action: str


@dataclasses.dataclass(frozen=True)
class DeploymentLifecycleResult:
  action: str
  completed_steps: tuple
  data_preserved: bool


def _owned_config_bytes(path):
  config_path = Path(path)
  try:
    content = config_path.read_bytes()
    payload = json.loads(content)
  except (OSError, ValueError) as error:
    raise DeploymentLifecycleError(
      "Cannot read owned deployment config"
    ) from error
  deployment = (
    payload.get("deployment")
    if isinstance(payload, dict)
    else None
  )
  if (
    not isinstance(deployment, dict)
    or deployment.get("owner") != "reviewcompass3"
    or deployment.get("schema_version") != 1
  ):
    raise DeploymentLifecycleError(
      "Unowned deployment config"
    )
  return content


def _absolute_config_path(path):
  config_path = Path(path)
  if not config_path.is_absolute():
    raise DeploymentLifecycleError(
      "Deployment config path must be absolute"
    )
  return config_path


def migrate_owned_config(source_path, target_path):
  source = _absolute_config_path(source_path)
  target = _absolute_config_path(target_path)
  if source == target:
    raise DeploymentLifecycleError(
      "Deployment config paths must differ"
    )
  source_bytes = _owned_config_bytes(source)
  if target.exists():
    try:
      target_bytes = target.read_bytes()
    except OSError as error:
      raise DeploymentLifecycleError(
        "Cannot inspect migration target"
      ) from error
    if target_bytes != source_bytes:
      return ConfigMigrationResult(action="preserved")
    try:
      source.unlink()
    except OSError as error:
      raise DeploymentLifecycleError(
        "Cannot remove migrated config"
      ) from error
    return ConfigMigrationResult(action="migrated")

  temporary_path = target.with_name(target.name + ".tmp")
  try:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_bytes(source_bytes)
    os.replace(temporary_path, target)
    if target.read_bytes() != source_bytes:
      raise DeploymentLifecycleError(
        "Migrated config verification failed"
      )
    source.unlink()
  except DeploymentLifecycleError:
    raise
  except OSError as error:
    raise DeploymentLifecycleError(
      "Cannot migrate deployment config"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)
  return ConfigMigrationResult(action="migrated")


def _run_cleanup_step(callback):
  try:
    result = callback()
  except Exception as error:
    raise DeploymentLifecycleError(
      "Deployment cleanup failed"
    ) from error
  if (
    getattr(result, "action", None) in ("failed", "preserved")
    or getattr(result, "status", None) in ("error", "failed")
  ):
    raise DeploymentLifecycleError(
      "Deployment cleanup failed"
    )


def uninstall_portable_deployment(
  config_path,
  *,
  deactivate_schedule,
  uninstall_schedule,
  uninstall_hooks,
) -> DeploymentLifecycleResult:
  path = _absolute_config_path(config_path)
  _owned_config_bytes(path)
  steps = (
    ("deactivate_schedule", deactivate_schedule),
    ("uninstall_schedule", uninstall_schedule),
    ("uninstall_hooks", uninstall_hooks),
  )
  completed = []
  for name, callback in steps:
    _run_cleanup_step(callback)
    completed.append(name)
  try:
    path.unlink()
  except OSError as error:
    raise DeploymentLifecycleError(
      "Cannot remove deployment config"
    ) from error
  completed.append("remove_config")
  return DeploymentLifecycleResult(
    action="uninstalled",
    completed_steps=tuple(completed),
    data_preserved=True,
  )


def _plan_migration(source_path, target_path):
  source = _absolute_config_path(source_path)
  target = _absolute_config_path(target_path)
  if source == target:
    raise DeploymentLifecycleError(
      "Deployment config paths must differ"
    )
  source_bytes = _owned_config_bytes(source)
  if not target.exists():
    return "planned"
  try:
    return (
      "planned"
      if target.read_bytes() == source_bytes
      else "preserved"
    )
  except OSError as error:
    raise DeploymentLifecycleError(
      "Cannot inspect migration target"
    ) from error


def _print_result(action, status, *, data_preserved=None):
  payload = {
    "action": action,
    "status": status,
  }
  if data_preserved is not None:
    payload["data_preserved"] = data_preserved
  print(json.dumps(payload, sort_keys=True))


def _uninstall_request(args):
  from tools.session_logs.schedule_backends import (
    PeriodicScheduleRequest,
  )
  values = (
    args.config,
    args.hook_settings,
    args.schedule,
    args.python,
    args.stdout,
    args.stderr,
  )
  if not all(Path(value).is_absolute() for value in values):
    raise DeploymentLifecycleError(
      "Deployment paths must be absolute"
    )
  return PeriodicScheduleRequest(
    schedule_path=Path(args.schedule),
    python_executable=Path(args.python),
    config_path=Path(args.config),
    interval_seconds=args.interval,
    stdout_path=Path(args.stdout),
    stderr_path=Path(args.stderr),
    user_id=args.uid,
  )


def run(argv=None, *, backend_registry=None) -> int:
  parser = argparse.ArgumentParser()
  commands = parser.add_subparsers(dest="command", required=True)
  migrate = commands.add_parser("migrate")
  migrate.add_argument("--source", required=True)
  migrate.add_argument("--target", required=True)
  migrate.add_argument("--dry-run", action="store_true")
  uninstall = commands.add_parser("uninstall")
  uninstall.add_argument("--config", required=True)
  uninstall.add_argument("--hook-settings", required=True)
  uninstall.add_argument("--schedule", required=True)
  uninstall.add_argument("--python", required=True)
  uninstall.add_argument("--interval", required=True, type=int)
  uninstall.add_argument("--stdout", required=True)
  uninstall.add_argument("--stderr", required=True)
  uninstall.add_argument("--uid", required=True, type=int)
  uninstall.add_argument(
    "--platform",
    required=True,
    choices=("darwin", "linux", "win32"),
  )
  uninstall.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  try:
    if args.command == "migrate":
      if args.dry_run:
        action = _plan_migration(args.source, args.target)
      else:
        action = migrate_owned_config(
          args.source,
          args.target,
        ).action
      status = "error" if action == "preserved" else "ok"
      _print_result(action, status)
      return 5 if action == "preserved" else 0

    from tools.session_logs.config import load_config
    from tools.session_logs.hook_installation import (
      uninstall_claude_hooks,
    )
    from tools.session_logs.hooks import build_hook_commands
    from tools.session_logs.schedule_backends import (
      select_schedule_backend,
    )
    _owned_config_bytes(args.config)
    config = load_config(args.config)
    request = _uninstall_request(args)
    backend = select_schedule_backend(
      platform_name=args.platform,
      registry=backend_registry,
    )
    hook_commands = build_hook_commands(
      args.python,
      args.config,
      event_log_path=config.hook_event_log_path,
    )
    if args.dry_run:
      result = backend.run(
        "uninstall",
        request,
        dry_run=True,
      )
      if result.action != "planned":
        raise DeploymentLifecycleError(
          "Deployment dry run failed"
        )
      _print_result(
        "planned",
        "ok",
        data_preserved=True,
      )
      return 0
    result = uninstall_portable_deployment(
      args.config,
      deactivate_schedule=lambda: backend.run(
        "deactivate",
        request,
      ),
      uninstall_schedule=lambda: backend.run(
        "uninstall",
        request,
      ),
      uninstall_hooks=lambda: uninstall_claude_hooks(
        args.hook_settings,
        start_command=hook_commands.start,
        end_command=hook_commands.end,
      ),
    )
    _print_result(
      result.action,
      "ok",
      data_preserved=result.data_preserved,
    )
    return 0
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
