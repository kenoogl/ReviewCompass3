"""ポータブル設定生成の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
from pathlib import Path

import pytest


def _deployment_paths():
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )
  return deployment_paths.DeploymentPaths(
    config_file=Path("/standard/config/session-logs.json"),
    data_root=Path("/standard/data"),
    state_root=Path("/standard/state"),
    log_root=Path("/standard/log"),
    cache_root=Path("/standard/cache"),
  )


def test_builds_portable_config_from_typed_standard_directories():
  portable = importlib.import_module(
    "tools.session_logs.portable_config"
  )

  result = portable.build_portable_config(
    "/private/raw",
    deployment_paths=_deployment_paths(),
    tool_version="0.0.1",
  )

  assert result.config_file == Path(
    "/standard/config/session-logs.json"
  )
  assert result.payload == {
    "allow_patterns": [],
    "backup_root": "/standard/data/backups",
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "hook_event_log_path": "/standard/log/hooks.jsonl",
    "preservation_enabled": True,
    "preservation_ledger_path": (
      "/standard/state/preservation-ledger.json"
    ),
    "provenance_root": "/standard/data/provenance",
    "raw_root": "/private/raw",
    "redaction_rules": [],
    "sensitive_report_root": "/standard/state/sensitive-reports",
    "summary_root": "/standard/data/summaries",
    "tool_version": "0.0.1",
    "transcript_root": "/standard/data/transcripts",
  }
  assert json.loads(result.render()) == result.payload


def test_explicit_roots_override_environment_and_standard_directories():
  portable = importlib.import_module(
    "tools.session_logs.portable_config"
  )

  result = portable.build_portable_config(
    "/private/raw",
    deployment_paths=_deployment_paths(),
    environment={
      "REVIEWCOMPASS3_CONFIG_FILE": "/environment/config.json",
      "REVIEWCOMPASS3_DATA_ROOT": "/environment/data",
      "REVIEWCOMPASS3_LOG_ROOT": "/environment/log",
      "REVIEWCOMPASS3_STATE_ROOT": "/environment/state",
    },
    overrides={
      "config_file": "/explicit/config.json",
      "data_root": "/explicit/data",
    },
    tool_version="0.0.1",
  )

  assert result.config_file == Path("/explicit/config.json")
  assert result.payload["transcript_root"] == (
    "/explicit/data/transcripts"
  )
  assert result.payload["sensitive_report_root"] == (
    "/environment/state/sensitive-reports"
  )
  assert result.payload["hook_event_log_path"] == (
    "/environment/log/hooks.jsonl"
  )


def test_rejects_relative_raw_or_override_paths():
  portable = importlib.import_module(
    "tools.session_logs.portable_config"
  )

  with pytest.raises(portable.PortableConfigError):
    portable.build_portable_config(
      "relative-raw",
      deployment_paths=_deployment_paths(),
      tool_version="0.0.1",
    )

  with pytest.raises(portable.PortableConfigError):
    portable.build_portable_config(
      "/private/raw",
      deployment_paths=_deployment_paths(),
      overrides={"state_root": "relative-state"},
      tool_version="0.0.1",
    )


def test_init_config_cli_dry_run_and_idempotent_install(
  tmp_path,
  monkeypatch,
  capsys,
):
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )

  class FakePlatformDirs:
    user_config_path = tmp_path / "config"
    user_data_path = tmp_path / "data"
    user_state_path = tmp_path / "state"
    user_log_path = tmp_path / "log"
    user_cache_path = tmp_path / "cache"

  monkeypatch.setattr(
    deployment_paths,
    "_default_platform_dirs_factory",
    lambda **_arguments: FakePlatformDirs(),
  )
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  config_file = tmp_path / "config" / "session-logs.json"
  entry = importlib.import_module("tools.session_logs.entry")
  arguments = (
    "init-config",
    "--raw-root",
    str(raw_root),
    "--tool-version",
    "0.0.1",
  )

  assert entry.run((*arguments, "--dry-run")) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "planned",
    "status": "ok",
  }
  assert not config_file.exists()

  assert entry.run(arguments) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "installed",
    "status": "ok",
  }
  assert config_file.is_file()

  assert entry.run(arguments) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "unchanged",
    "status": "ok",
  }


def test_init_config_cli_preserves_different_existing_file(
  tmp_path,
  monkeypatch,
  capsys,
):
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )

  class FakePlatformDirs:
    user_config_path = tmp_path / "config"
    user_data_path = tmp_path / "data"
    user_state_path = tmp_path / "state"
    user_log_path = tmp_path / "log"
    user_cache_path = tmp_path / "cache"

  monkeypatch.setattr(
    deployment_paths,
    "_default_platform_dirs_factory",
    lambda **_arguments: FakePlatformDirs(),
  )
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  config_file = tmp_path / "config" / "session-logs.json"
  config_file.parent.mkdir()
  config_file.write_text('{"keep": true}\n', encoding="utf-8")
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "init-config",
    "--raw-root",
    str(raw_root),
    "--tool-version",
    "0.0.1",
  )) == 5

  output = capsys.readouterr().out
  assert json.loads(output) == {
    "action": "preserved",
    "status": "error",
  }
  assert config_file.read_text(encoding="utf-8") == (
    '{"keep": true}\n'
  )
  assert str(tmp_path) not in output
