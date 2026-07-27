"""承認付き限定配置の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _approval_payload(tmp_path, *, platform="darwin"):
  return {
    "approved": True,
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "interval_seconds": 300,
    "platform": platform,
    "targets": {
      "config_file": str(tmp_path / "config" / "session-logs.json"),
      "data_root": str(tmp_path / "data"),
      "hook_settings": str(tmp_path / "claude" / "settings.json"),
      "log_root": str(tmp_path / "log"),
      "python_executable": "/usr/bin/python3",
      "raw_root": str(tmp_path / "raw"),
      "schedule_path": str(
        tmp_path / "schedule" / "session-logs.plist"
      ),
      "state_root": str(tmp_path / "state"),
    },
    "user_id": 501,
  }


def _write_approval(tmp_path, payload):
  path = tmp_path / "approval.json"
  path.write_text(json.dumps(payload), encoding="utf-8")
  return path


def test_limited_deployment_rejects_unapproved_or_wrong_os_before_steps(
  tmp_path,
):
  limited = importlib.import_module(
    "tools.session_logs.limited_deployment"
  )
  payload = _approval_payload(tmp_path, platform="linux")
  approval_path = _write_approval(tmp_path, payload)
  calls = []

  with pytest.raises(limited.LimitedDeploymentError):
    limited.execute_limited_install(
      approval_path,
      runtime_platform="darwin",
      install_config=lambda _request: calls.append("config"),
      install_hooks=lambda _request: calls.append("hooks"),
      install_schedule=lambda _request: calls.append("schedule"),
      activate_schedule=lambda _request: calls.append("activate"),
      inspect_schedule=lambda _request: calls.append("inspect"),
    )

  assert calls == []

  payload["platform"] = "darwin"
  payload["targets"]["config_file"] = "relative/config.json"
  approval_path.write_text(json.dumps(payload), encoding="utf-8")
  with pytest.raises(limited.LimitedDeploymentError):
    limited.load_limited_approval(approval_path)


def test_limited_install_and_uninstall_are_ordered_and_preserve_data(
  tmp_path,
):
  limited = importlib.import_module(
    "tools.session_logs.limited_deployment"
  )
  approval_path = _write_approval(
    tmp_path,
    _approval_payload(tmp_path),
  )
  data_root = tmp_path / "data"
  data_root.mkdir()
  retained = data_root / "retained.txt"
  retained.write_text("retain", encoding="utf-8")
  calls = []

  installed = limited.execute_limited_install(
    approval_path,
    runtime_platform="darwin",
    install_config=lambda _request: calls.append("install_config"),
    install_hooks=lambda _request: calls.append("install_hooks"),
    install_schedule=lambda _request: calls.append("install_schedule"),
    activate_schedule=lambda _request: calls.append(
      "activate_schedule"
    ),
    inspect_schedule=lambda _request: calls.append(
      "inspect_schedule"
    ),
  )
  removed = limited.execute_limited_uninstall(
    approval_path,
    runtime_platform="darwin",
    deactivate_schedule=lambda _request: calls.append(
      "deactivate_schedule"
    ),
    uninstall_schedule=lambda _request: calls.append(
      "uninstall_schedule"
    ),
    uninstall_hooks=lambda _request: calls.append(
      "uninstall_hooks"
    ),
    remove_config=lambda _request: calls.append("remove_config"),
  )

  assert calls == [
    "install_config",
    "install_hooks",
    "install_schedule",
    "activate_schedule",
    "inspect_schedule",
    "deactivate_schedule",
    "uninstall_schedule",
    "uninstall_hooks",
    "remove_config",
  ]
  assert installed.action == "installed"
  assert removed.action == "uninstalled"
  assert installed.data_preserved is True
  assert removed.data_preserved is True
  assert retained.read_text(encoding="utf-8") == "retain"
