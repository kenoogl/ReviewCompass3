"""ネイティブ標準配置検証の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
WORKFLOW_PATH = (
  REPOSITORY_ROOT
  / ".github"
  / "workflows"
  / "native-deployment-validation.yml"
)


def test_native_paths_are_external_and_precedence_is_verified(tmp_path):
  validation = importlib.import_module(
    "tools.session_logs.native_validation"
  )
  repository_root = tmp_path / "repository"
  repository_root.mkdir()
  native_root = tmp_path / "native"

  class NativePlatformDirs:
    user_config_path = native_root / "config"
    user_data_path = native_root / "data"
    user_state_path = native_root / "state"
    user_log_path = native_root / "log"
    user_cache_path = native_root / "cache"

  result = validation.validate_native_paths(
    repository_root,
    tmp_path / "raw",
    platform_dirs_factory=lambda **_arguments: NativePlatformDirs(),
  )

  assert result == {
    "absolute_path_count": 5,
    "check": "paths",
    "environment_precedence": True,
    "explicit_precedence": True,
    "external_path_count": 5,
    "path_count": 5,
    "platform": "macos",
    "status": "passed",
  }
  assert str(tmp_path) not in str(result)


def test_native_ci_runs_path_validation_on_each_matrix_host():
  workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

  assert (
    "reviewcompass3-session-logs validate-native "
    "--check paths"
  ) in workflow
  assert "--project-root" in workflow
  assert "--raw-root" in workflow
