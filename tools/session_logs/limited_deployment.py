"""利用者が明示承認した対象だけを扱う限定配置境界。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import sys
from pathlib import Path


class LimitedDeploymentError(Exception):
  """承認されていないOSや配置先への操作を拒否する。"""


@dataclasses.dataclass(frozen=True)
class LimitedDeploymentRequest:
  platform: str
  raw_root: Path
  config_file: Path
  data_root: Path
  state_root: Path
  log_root: Path
  hook_settings: Path
  schedule_path: Path
  python_executable: Path
  interval_seconds: int
  user_id: int


@dataclasses.dataclass(frozen=True)
class LimitedDeploymentResult:
  action: str
  completed_steps: tuple
  data_preserved: bool


_TARGET_NAMES = (
  "config_file",
  "data_root",
  "hook_settings",
  "log_root",
  "python_executable",
  "raw_root",
  "schedule_path",
  "state_root",
)

_SCHEDULE_SUFFIXES = {
  "darwin": ".plist",
  "linux": ".timer",
  "win32": ".xml",
}


def load_limited_approval(path) -> LimitedDeploymentRequest:
  approval_path = Path(path)
  if not approval_path.is_absolute():
    raise LimitedDeploymentError(
      "Limited deployment approval path must be absolute"
    )
  try:
    payload = json.loads(
      approval_path.read_text(encoding="utf-8")
    )
  except (OSError, ValueError) as error:
    raise LimitedDeploymentError(
      "Cannot read limited deployment approval"
    ) from error
  deployment = (
    payload.get("deployment")
    if isinstance(payload, dict)
    else None
  )
  targets = (
    payload.get("targets")
    if isinstance(payload, dict)
    else None
  )
  platform = (
    payload.get("platform")
    if isinstance(payload, dict)
    else None
  )
  interval = (
    payload.get("interval_seconds")
    if isinstance(payload, dict)
    else None
  )
  user_id = (
    payload.get("user_id")
    if isinstance(payload, dict)
    else None
  )
  if (
    payload.get("approved") is not True
    or not isinstance(deployment, dict)
    or deployment.get("owner") != "reviewcompass3"
    or deployment.get("schema_version") != 1
    or platform not in _SCHEDULE_SUFFIXES
    or not isinstance(targets, dict)
    or set(targets) != set(_TARGET_NAMES)
    or isinstance(interval, bool)
    or not isinstance(interval, int)
    or interval <= 0
    or isinstance(user_id, bool)
    or not isinstance(user_id, int)
    or user_id < 0
  ):
    raise LimitedDeploymentError(
      "Invalid limited deployment approval"
    )
  paths = {}
  for name in _TARGET_NAMES:
    value = targets.get(name)
    if not isinstance(value, str) or not Path(value).is_absolute():
      raise LimitedDeploymentError(
        "Limited deployment targets must be absolute"
      )
    paths[name] = Path(value)
  if (
    paths["schedule_path"].suffix.lower()
    != _SCHEDULE_SUFFIXES[platform]
  ):
    raise LimitedDeploymentError(
      "Limited deployment schedule does not match OS"
    )
  return LimitedDeploymentRequest(
    platform=platform,
    raw_root=paths["raw_root"],
    config_file=paths["config_file"],
    data_root=paths["data_root"],
    state_root=paths["state_root"],
    log_root=paths["log_root"],
    hook_settings=paths["hook_settings"],
    schedule_path=paths["schedule_path"],
    python_executable=paths["python_executable"],
    interval_seconds=interval,
    user_id=user_id,
  )


def _approved_request(path, runtime_platform):
  request = load_limited_approval(path)
  if request.platform != runtime_platform:
    raise LimitedDeploymentError(
      "Limited deployment OS is not approved"
    )
  return request


def _data_inventory(root):
  path = Path(root)
  if not path.exists():
    return frozenset()
  try:
    return frozenset(
      item.relative_to(path).parts
      for item in path.rglob("*")
      if item.is_file() and not item.is_symlink()
    )
  except OSError as error:
    raise LimitedDeploymentError(
      "Cannot inspect retained deployment data"
    ) from error


def _run_steps(request, steps):
  completed = []
  for name, callback in steps:
    try:
      result = callback(request)
    except Exception as error:
      raise LimitedDeploymentError(
        "Limited deployment step failed"
      ) from error
    if (
      getattr(result, "action", None) in ("failed", "preserved")
      or getattr(result, "status", None) in ("error", "failed")
    ):
      raise LimitedDeploymentError(
        "Limited deployment step failed"
      )
    completed.append(name)
  return tuple(completed)


def execute_limited_install(
  approval_path,
  *,
  install_config,
  install_hooks,
  install_schedule,
  activate_schedule,
  inspect_schedule,
  runtime_platform=None,
) -> LimitedDeploymentResult:
  selected_platform = (
    sys.platform
    if runtime_platform is None
    else runtime_platform
  )
  request = _approved_request(
    approval_path,
    selected_platform,
  )
  before = _data_inventory(request.data_root)
  completed = _run_steps(request, (
    ("install_config", install_config),
    ("install_hooks", install_hooks),
    ("install_schedule", install_schedule),
    ("activate_schedule", activate_schedule),
    ("inspect_schedule", inspect_schedule),
  ))
  after = _data_inventory(request.data_root)
  if not before.issubset(after):
    raise LimitedDeploymentError(
      "Limited deployment data was removed"
    )
  return LimitedDeploymentResult(
    action="installed",
    completed_steps=completed,
    data_preserved=True,
  )


def execute_limited_uninstall(
  approval_path,
  *,
  deactivate_schedule,
  uninstall_schedule,
  uninstall_hooks,
  remove_config,
  runtime_platform=None,
) -> LimitedDeploymentResult:
  selected_platform = (
    sys.platform
    if runtime_platform is None
    else runtime_platform
  )
  request = _approved_request(
    approval_path,
    selected_platform,
  )
  before = _data_inventory(request.data_root)
  completed = _run_steps(request, (
    ("deactivate_schedule", deactivate_schedule),
    ("uninstall_schedule", uninstall_schedule),
    ("uninstall_hooks", uninstall_hooks),
    ("remove_config", remove_config),
  ))
  after = _data_inventory(request.data_root)
  if before != after:
    raise LimitedDeploymentError(
      "Limited deployment data was not preserved"
    )
  return LimitedDeploymentResult(
    action="uninstalled",
    completed_steps=completed,
    data_preserved=True,
  )


def _portable_candidate(request):
  from tools.session_logs.deployment_paths import DeploymentPaths
  from tools.session_logs.portable_config import build_portable_config
  paths = DeploymentPaths(
    config_file=request.config_file,
    data_root=request.data_root,
    state_root=request.state_root,
    log_root=request.log_root,
    cache_root=request.data_root / "cache",
  )
  return build_portable_config(
    request.raw_root,
    deployment_paths=paths,
    tool_version="0.0.1",
    environment={},
  )


def _schedule_request(request):
  from tools.session_logs.schedule_backends import (
    PeriodicScheduleRequest,
  )
  return PeriodicScheduleRequest(
    schedule_path=request.schedule_path,
    python_executable=request.python_executable,
    config_path=request.config_file,
    interval_seconds=request.interval_seconds,
    stdout_path=request.log_root / "stdout.log",
    stderr_path=request.log_root / "stderr.log",
    user_id=request.user_id,
  )


def _install_callbacks(backend):
  from tools.session_logs.hook_installation import (
    install_configured_claude_hooks,
  )
  from tools.session_logs.portable_config import (
    install_portable_config,
  )
  return {
    "install_config": lambda request: install_portable_config(
      _portable_candidate(request)
    ),
    "install_hooks": lambda request: (
      install_configured_claude_hooks(
        request.hook_settings,
        python_executable=request.python_executable,
        config_path=request.config_file,
      )
    ),
    "install_schedule": lambda request: backend.run(
      "install",
      _schedule_request(request),
    ),
    "activate_schedule": lambda request: backend.run(
      "activate",
      _schedule_request(request),
    ),
    "inspect_schedule": lambda request: backend.run(
      "status",
      _schedule_request(request),
    ),
  }


def _uninstall_hooks(request):
  from tools.session_logs.config import load_config
  from tools.session_logs.hook_installation import (
    uninstall_claude_hooks,
  )
  from tools.session_logs.hooks import build_hook_commands
  config = load_config(request.config_file)
  commands = build_hook_commands(
    request.python_executable,
    request.config_file,
    event_log_path=config.hook_event_log_path,
  )
  return uninstall_claude_hooks(
    request.hook_settings,
    start_command=commands.start,
    end_command=commands.end,
  )


def _remove_owned_config(request):
  from tools.session_logs.deployment_lifecycle import (
    ConfigMigrationResult,
    _owned_config_bytes,
  )
  _owned_config_bytes(request.config_file)
  try:
    request.config_file.unlink()
  except OSError as error:
    raise LimitedDeploymentError(
      "Cannot remove limited deployment config"
    ) from error
  return ConfigMigrationResult(action="uninstalled")


def _uninstall_callbacks(backend):
  return {
    "deactivate_schedule": lambda request: backend.run(
      "deactivate",
      _schedule_request(request),
    ),
    "uninstall_schedule": lambda request: backend.run(
      "uninstall",
      _schedule_request(request),
    ),
    "uninstall_hooks": _uninstall_hooks,
    "remove_config": _remove_owned_config,
  }


def _plan_limited(
  approval_path,
  operation,
  *,
  backend,
  runtime_platform,
):
  request = _approved_request(
    approval_path,
    runtime_platform,
  )
  if operation == "install":
    if not request.raw_root.is_dir():
      raise LimitedDeploymentError(
        "Limited deployment raw root is unavailable"
      )
    _portable_candidate(request)
  elif not request.config_file.is_file():
    raise LimitedDeploymentError(
      "Limited deployment config is unavailable"
    )
  result = backend.run(
    operation,
    _schedule_request(request),
    dry_run=True,
  )
  if result.action != "planned" or result.status != "ok":
    raise LimitedDeploymentError(
      "Limited deployment dry run failed"
    )
  return 5 if operation == "install" else 4


def _print_result(action, status, step_count, data_preserved):
  print(json.dumps({
    "action": action,
    "data_preserved": data_preserved,
    "status": status,
    "step_count": step_count,
  }, sort_keys=True))


def run(
  argv=None,
  *,
  backend_registry=None,
  runtime_platform=None,
) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "operation",
    choices=("install", "uninstall"),
  )
  parser.add_argument("--approval", required=True)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  selected_platform = (
    sys.platform
    if runtime_platform is None
    else runtime_platform
  )
  try:
    from tools.session_logs.schedule_backends import (
      select_schedule_backend,
    )
    request = _approved_request(
      args.approval,
      selected_platform,
    )
    backend = select_schedule_backend(
      platform_name=request.platform,
      registry=backend_registry,
    )
    if args.dry_run:
      step_count = _plan_limited(
        args.approval,
        args.operation,
        backend=backend,
        runtime_platform=selected_platform,
      )
      _print_result("planned", "ok", step_count, True)
      return 0
    if args.operation == "install":
      result = execute_limited_install(
        args.approval,
        runtime_platform=selected_platform,
        **_install_callbacks(backend),
      )
    else:
      result = execute_limited_uninstall(
        args.approval,
        runtime_platform=selected_platform,
        **_uninstall_callbacks(backend),
      )
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  _print_result(
    result.action,
    "ok",
    len(result.completed_steps),
    result.data_preserved,
  )
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
