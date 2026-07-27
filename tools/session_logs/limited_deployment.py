"""利用者が明示承認した対象だけを扱う限定配置境界。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

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
