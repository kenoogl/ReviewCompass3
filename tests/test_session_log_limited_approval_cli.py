"""限定配置承認候補生成CLIの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def test_approval_cli_dry_run_then_writes_unapproved_candidate(
  tmp_path,
  monkeypatch,
  capsys,
):
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )
  standard_root = tmp_path / "standard"

  class NativePlatformDirs:
    user_config_path = standard_root / "config"
    user_data_path = standard_root / "data"
    user_state_path = standard_root / "state"
    user_log_path = standard_root / "log"
    user_cache_path = standard_root / "cache"

  monkeypatch.setattr(
    deployment_paths,
    "_default_platform_dirs_factory",
    lambda **_arguments: NativePlatformDirs(),
  )
  output_path = tmp_path / "approval.json"
  raw_root = tmp_path / "raw"
  hook_settings = tmp_path / "claude" / "settings.json"
  schedule_path = tmp_path / "schedule" / "session-logs.plist"
  entry = importlib.import_module("tools.session_logs.entry")
  arguments = (
    "prepare-deployment-approval",
    "--platform",
    "darwin",
    "--raw-root",
    str(raw_root),
    "--hook-settings",
    str(hook_settings),
    "--schedule",
    str(schedule_path),
    "--python",
    "/usr/bin/python3",
    "--interval",
    "300",
    "--uid",
    "501",
    "--output",
    str(output_path),
  )

  assert entry.run((*arguments, "--dry-run")) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "planned",
    "approved": False,
    "status": "ok",
  }
  assert not output_path.exists()
  assert not standard_root.exists()

  assert entry.run(arguments) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "created",
    "approved": False,
    "status": "ok",
  }
  payload = json.loads(output_path.read_text(encoding="utf-8"))
  assert payload == {
    "approved": False,
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "interval_seconds": 300,
    "platform": "darwin",
    "targets": {
      "config_file": str(
        standard_root / "config" / "session-logs.json"
      ),
      "data_root": str(standard_root / "data"),
      "hook_settings": str(hook_settings),
      "log_root": str(standard_root / "log"),
      "python_executable": "/usr/bin/python3",
      "raw_root": str(raw_root),
      "schedule_path": str(schedule_path),
      "state_root": str(standard_root / "state"),
    },
    "user_id": 501,
  }
  limited = importlib.import_module(
    "tools.session_logs.limited_deployment"
  )
  with pytest.raises(limited.LimitedDeploymentError):
    limited.load_limited_approval(output_path)


def test_approval_cli_preserves_different_existing_file(
  tmp_path,
  monkeypatch,
  capsys,
):
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )

  class NativePlatformDirs:
    user_config_path = tmp_path / "config"
    user_data_path = tmp_path / "data"
    user_state_path = tmp_path / "state"
    user_log_path = tmp_path / "log"
    user_cache_path = tmp_path / "cache"

  monkeypatch.setattr(
    deployment_paths,
    "_default_platform_dirs_factory",
    lambda **_arguments: NativePlatformDirs(),
  )
  output_path = tmp_path / "approval.json"
  output_path.write_text('{"keep": true}\n', encoding="utf-8")
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "prepare-deployment-approval",
    "--platform",
    "darwin",
    "--raw-root",
    str(tmp_path / "raw"),
    "--hook-settings",
    str(tmp_path / "hooks.json"),
    "--schedule",
    str(tmp_path / "schedule.plist"),
    "--python",
    "/usr/bin/python3",
    "--interval",
    "300",
    "--uid",
    "501",
    "--output",
    str(output_path),
  )) == 5

  assert json.loads(capsys.readouterr().out) == {
    "action": "preserved",
    "approved": False,
    "status": "error",
  }
  assert output_path.read_text(encoding="utf-8") == (
    '{"keep": true}\n'
  )
