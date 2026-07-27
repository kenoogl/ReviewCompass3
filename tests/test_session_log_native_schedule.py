"""ネイティブ定期実行dry-runの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).parents[1]
WORKFLOW_PATH = (
  REPOSITORY_ROOT
  / ".github"
  / "workflows"
  / "native-deployment-validation.yml"
)


@pytest.mark.parametrize(
  ("platform_name", "backend_id", "suffix"),
  (
    ("darwin", "launchd", ".plist"),
    ("linux", "systemd_user", ".timer"),
    ("win32", "windows_task", ".xml"),
  ),
)
def test_native_schedule_dry_run_plans_without_commands_or_writes(
  tmp_path,
  platform_name,
  backend_id,
  suffix,
):
  validation = importlib.import_module(
    "tools.session_logs.native_validation"
  )
  native_root = tmp_path / "native"

  class NativePlatformDirs:
    user_config_path = native_root / "config"
    user_data_path = native_root / "data"
    user_state_path = native_root / "state"
    user_log_path = native_root / "log"
    user_cache_path = native_root / "cache"

  result = validation.validate_native_schedule(
    tmp_path / "raw",
    tmp_path / "validation",
    platform_name=platform_name,
    platform_dirs_factory=lambda **_arguments: NativePlatformDirs(),
  )

  assert result == {
    "action": "planned",
    "artifact_written": False,
    "backend": backend_id,
    "check": "schedule",
    "commands_executed": False,
    "ownership_checked": True,
    "platform": {
      "darwin": "macos",
      "linux": "linux",
      "win32": "windows",
    }[platform_name],
    "status": "passed",
  }
  assert not (
    tmp_path / "validation" / ("schedule" + suffix)
  ).exists()
  assert str(tmp_path) not in str(result)


def test_native_ci_runs_schedule_dry_run_on_each_matrix_host():
  workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

  assert (
    "reviewcompass3-session-logs validate-native "
    "--check schedule"
  ) in workflow
