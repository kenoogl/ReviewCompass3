"""承認付き限定配置の固定実行CLI暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def _write_approval(tmp_path):
  approval_path = tmp_path / "approval.json"
  approval_path.write_text(
    json.dumps({
      "approved": True,
      "deployment": {
        "owner": "reviewcompass3",
        "schema_version": 1,
      },
      "interval_seconds": 300,
      "platform": "darwin",
      "targets": {
        "config_file": str(
          tmp_path / "config" / "session-logs.json"
        ),
        "data_root": str(tmp_path / "data"),
        "hook_settings": str(
          tmp_path / "claude" / "settings.json"
        ),
        "log_root": str(tmp_path / "log"),
        "python_executable": "/usr/bin/python3",
        "raw_root": str(tmp_path / "raw"),
        "schedule_path": str(
          tmp_path / "schedule" / "session-logs.plist"
        ),
        "state_root": str(tmp_path / "state"),
      },
      "user_id": 501,
    }),
    encoding="utf-8",
  )
  return approval_path


class FakeBackend:
  def __init__(self, result_type):
    self.result_type = result_type
    self.calls = []

  def run(self, operation, request, *, dry_run=False):
    self.calls.append((operation, dry_run))
    if dry_run:
      return self.result_type(
        backend="launchd",
        action="planned",
        status="ok",
      )
    values = {
      "install": ("installed", "ok"),
      "activate": ("activated", "running"),
      "status": ("inspected", "running"),
      "deactivate": ("deactivated", "stopped"),
      "uninstall": ("uninstalled", "ok"),
    }
    action, status = values[operation]
    return self.result_type(
      backend="launchd",
      action=action,
      status=status,
    )


def test_limited_deployment_cli_dry_run_then_install_and_uninstall(
  tmp_path,
  capsys,
):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  data_root = tmp_path / "data"
  data_root.mkdir()
  retained = data_root / "retained.txt"
  retained.write_text("retain", encoding="utf-8")
  approval_path = _write_approval(tmp_path)
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  backend = FakeBackend(backends.ScheduleBackendResult)
  registry = {"launchd": backend}
  limited = importlib.import_module(
    "tools.session_logs.limited_deployment"
  )

  assert limited.run(
    (
      "install",
      "--approval",
      str(approval_path),
      "--dry-run",
    ),
    backend_registry=registry,
    runtime_platform="darwin",
  ) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "planned",
    "data_preserved": True,
    "status": "ok",
    "step_count": 5,
  }
  assert backend.calls == [("install", True)]
  assert not (tmp_path / "config").exists()
  assert not (tmp_path / "claude").exists()

  assert limited.run(
    ("install", "--approval", str(approval_path)),
    backend_registry=registry,
    runtime_platform="darwin",
  ) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "installed",
    "data_preserved": True,
    "status": "ok",
    "step_count": 5,
  }
  config_path = tmp_path / "config" / "session-logs.json"
  hook_settings = tmp_path / "claude" / "settings.json"
  assert config_path.is_file()
  assert hook_settings.is_file()
  assert backend.calls[-3:] == [
    ("install", False),
    ("activate", False),
    ("status", False),
  ]

  assert limited.run(
    ("uninstall", "--approval", str(approval_path)),
    backend_registry=registry,
    runtime_platform="darwin",
  ) == 0
  assert json.loads(capsys.readouterr().out) == {
    "action": "uninstalled",
    "data_preserved": True,
    "status": "ok",
    "step_count": 4,
  }
  assert backend.calls[-2:] == [
    ("deactivate", False),
    ("uninstall", False),
  ]
  assert not config_path.exists()
  assert json.loads(hook_settings.read_text(encoding="utf-8")) == {}
  assert retained.read_text(encoding="utf-8") == "retain"


def test_limited_deployment_cli_rejects_unapproved_before_backend(
  tmp_path,
  capsys,
):
  approval_path = _write_approval(tmp_path)
  payload = json.loads(approval_path.read_text(encoding="utf-8"))
  payload["approved"] = False
  approval_path.write_text(json.dumps(payload), encoding="utf-8")
  backends = importlib.import_module(
    "tools.session_logs.schedule_backends"
  )
  backend = FakeBackend(backends.ScheduleBackendResult)
  limited = importlib.import_module(
    "tools.session_logs.limited_deployment"
  )

  assert limited.run(
    ("install", "--approval", str(approval_path)),
    backend_registry={"launchd": backend},
    runtime_platform="darwin",
  ) == 5

  assert json.loads(capsys.readouterr().out) == {
    "reason": "LimitedDeploymentError",
    "status": "failed",
  }
  assert backend.calls == []
