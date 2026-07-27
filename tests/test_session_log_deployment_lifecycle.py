"""ポータブル配置の移行・解除境界の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
from pathlib import Path

import pytest


def _owned_payload(data_root):
  return {
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "raw_root": "/private/raw",
    "transcript_root": str(data_root / "transcripts"),
    "summary_root": str(data_root / "summaries"),
    "provenance_root": str(data_root / "provenance"),
    "tool_version": "0.0.1",
  }


def _write_owned_config(path, data_root):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps(
      _owned_payload(data_root),
      indent=2,
      sort_keys=True,
    ) + "\n",
    encoding="utf-8",
  )


def test_migrates_owned_config_without_overwriting_conflicts(tmp_path):
  lifecycle = importlib.import_module(
    "tools.session_logs.deployment_lifecycle"
  )
  data_root = tmp_path / "data"
  source = tmp_path / "legacy" / "session-logs.json"
  target = tmp_path / "standard" / "session-logs.json"
  _write_owned_config(source, data_root)
  original = source.read_bytes()

  result = lifecycle.migrate_owned_config(source, target)

  assert result.action == "migrated"
  assert target.read_bytes() == original
  assert not source.exists()

  _write_owned_config(source, data_root)
  target.write_text('{"keep": true}\n', encoding="utf-8")
  result = lifecycle.migrate_owned_config(source, target)

  assert result.action == "preserved"
  assert source.exists()
  assert target.read_text(encoding="utf-8") == '{"keep": true}\n'


def test_uninstall_orders_cleanup_and_preserves_user_data(tmp_path):
  lifecycle = importlib.import_module(
    "tools.session_logs.deployment_lifecycle"
  )
  data_root = tmp_path / "data"
  data_root.mkdir()
  retained = data_root / "retained.txt"
  retained.write_text("retain", encoding="utf-8")
  config_path = tmp_path / "config" / "session-logs.json"
  _write_owned_config(config_path, data_root)
  calls = []

  result = lifecycle.uninstall_portable_deployment(
    config_path,
    deactivate_schedule=lambda: calls.append(
      "deactivate_schedule"
    ),
    uninstall_schedule=lambda: calls.append(
      "uninstall_schedule"
    ),
    uninstall_hooks=lambda: calls.append("uninstall_hooks"),
  )

  assert calls == [
    "deactivate_schedule",
    "uninstall_schedule",
    "uninstall_hooks",
  ]
  assert result == lifecycle.DeploymentLifecycleResult(
    action="uninstalled",
    completed_steps=(
      "deactivate_schedule",
      "uninstall_schedule",
      "uninstall_hooks",
      "remove_config",
    ),
    data_preserved=True,
  )
  assert not config_path.exists()
  assert retained.read_text(encoding="utf-8") == "retain"


def test_uninstall_rejects_unowned_config_before_callbacks(tmp_path):
  lifecycle = importlib.import_module(
    "tools.session_logs.deployment_lifecycle"
  )
  config_path = tmp_path / "session-logs.json"
  config_path.write_text('{"deployment": {}}\n', encoding="utf-8")
  calls = []

  with pytest.raises(lifecycle.DeploymentLifecycleError):
    lifecycle.uninstall_portable_deployment(
      config_path,
      deactivate_schedule=lambda: calls.append("unexpected"),
      uninstall_schedule=lambda: calls.append("unexpected"),
      uninstall_hooks=lambda: calls.append("unexpected"),
    )

  assert calls == []
  assert config_path.exists()
