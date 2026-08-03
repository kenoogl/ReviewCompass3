"""OS標準に従うセッションログ配置先。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import sys
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


@dataclasses.dataclass(frozen=True)
class _BuiltinPlatformDirs:
  user_config_path: Path
  user_data_path: Path
  user_state_path: Path
  user_log_path: Path
  user_cache_path: Path


def _load_platform_dirs_factory():
  try:
    from platformdirs import PlatformDirs
  except ImportError:
    return None
  return PlatformDirs


def _default_platform_dirs_factory(
  *,
  appname,
  appauthor,
  ensure_exists,
  platform_name=None,
  home_directory=None,
):
  factory = _load_platform_dirs_factory()
  if factory is not None:
    return factory(
      appname=appname,
      appauthor=appauthor,
      ensure_exists=ensure_exists,
    )
  selected_platform = sys.platform if platform_name is None else platform_name
  if selected_platform != "darwin":
    raise DeploymentPathError(
      "platformdirs dependency is unavailable"
    )
  home = (
    Path.home()
    if home_directory is None
    else Path(home_directory)
  )
  if not home.is_absolute():
    raise DeploymentPathError("Unsafe home directory")
  application_support = (
    home / "Library" / "Application Support" / appname
  )
  return _BuiltinPlatformDirs(
    user_config_path=application_support,
    user_data_path=application_support,
    user_state_path=application_support / "state",
    user_log_path=home / "Library" / "Logs" / appname,
    user_cache_path=home / "Library" / "Caches" / appname,
  )


def resolve_deployment_paths(
  *,
  app_name="ReviewCompass3",
  app_author="ReviewCompass",
  platform_dirs_factory=None,
  platform_name=None,
  home_directory=None,
) -> DeploymentPaths:
  try:
    if platform_dirs_factory is None:
      directories = _default_platform_dirs_factory(
        appname=app_name,
        appauthor=app_author,
        ensure_exists=False,
        platform_name=platform_name,
        home_directory=home_directory,
      )
    else:
      directories = platform_dirs_factory(
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
