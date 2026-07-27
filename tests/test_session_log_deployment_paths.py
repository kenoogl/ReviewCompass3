"""クロスプラットフォーム配置先の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path

import pytest


class _FakePlatformDirs:
  user_config_path = Path("/portable/config")
  user_data_path = Path("/portable/data")
  user_state_path = Path("/portable/state")
  user_log_path = Path("/portable/log")
  user_cache_path = Path("/portable/cache")


def test_resolves_typed_standard_directories_through_platform_adapter():
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )
  received = {}

  def factory(**arguments):
    received.update(arguments)
    return _FakePlatformDirs()

  result = deployment_paths.resolve_deployment_paths(
    platform_dirs_factory=factory,
  )

  assert received == {
    "appauthor": "ReviewCompass",
    "appname": "ReviewCompass3",
    "ensure_exists": False,
  }
  assert result.config_file == Path(
    "/portable/config/session-logs.json"
  )
  assert result.data_root == Path("/portable/data")
  assert result.state_root == Path("/portable/state")
  assert result.log_root == Path("/portable/log")
  assert result.cache_root == Path("/portable/cache")


def test_rejects_non_absolute_platform_directory_results():
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )

  class UnsafePlatformDirs(_FakePlatformDirs):
    user_state_path = Path("relative-state")

  with pytest.raises(deployment_paths.DeploymentPathError):
    deployment_paths.resolve_deployment_paths(
      platform_dirs_factory=lambda **_arguments: UnsafePlatformDirs(),
    )
