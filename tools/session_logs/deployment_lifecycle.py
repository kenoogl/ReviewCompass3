"""ポータブル設定の安全な移行と解除。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

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
