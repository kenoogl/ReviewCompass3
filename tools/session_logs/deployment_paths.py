"""OS標準に従うセッションログ配置先。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
from pathlib import Path


class DeploymentPathError(Exception):
  """安全な標準配置先を解決できない。"""


@dataclasses.dataclass(frozen=True)
class DeploymentPaths:
  config_file: Path
  data_root: Path
  state_root: Path
  log_root: Path
  cache_root: Path


def _default_platform_dirs_factory(**arguments):
  try:
    from platformdirs import PlatformDirs
  except ImportError as error:
    raise DeploymentPathError(
      "platformdirs dependency is unavailable"
    ) from error
  return PlatformDirs(**arguments)


def resolve_deployment_paths(
  *,
  app_name="ReviewCompass3",
  app_author="ReviewCompass",
  platform_dirs_factory=None,
) -> DeploymentPaths:
  factory = (
    _default_platform_dirs_factory
    if platform_dirs_factory is None
    else platform_dirs_factory
  )
  try:
    directories = factory(
      appname=app_name,
      appauthor=app_author,
      ensure_exists=False,
    )
    result = DeploymentPaths(
      config_file=(
        Path(directories.user_config_path)
        / "session-logs.json"
      ),
      data_root=Path(directories.user_data_path),
      state_root=Path(directories.user_state_path),
      log_root=Path(directories.user_log_path),
      cache_root=Path(directories.user_cache_path),
    )
  except DeploymentPathError:
    raise
  except Exception as error:
    raise DeploymentPathError(
      "Cannot resolve deployment paths"
    ) from error
  if not all(
    value.is_absolute()
    for value in dataclasses.astuple(result)
  ):
    raise DeploymentPathError(
      "Unsafe deployment path"
    )
  return result
