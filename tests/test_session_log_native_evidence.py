"""ネイティブCI証拠集約の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


PLATFORMS = {
  "Linux": ("linux", "systemd_user"),
  "macOS": ("macos", "launchd"),
  "Windows": ("windows", "windows_task"),
}


def _write_artifacts(root):
  for runner_name, (platform, backend) in PLATFORMS.items():
    for python_version in ("3.9", "3.13"):
      artifact = (
        root
        / (
          "native-package-%s-%s"
          % (runner_name, python_version)
        )
      )
      artifact.mkdir(parents=True)
      payloads = {
        "native-package.json": {
          "check": "package",
          "entry_importable": True,
          "platform": platform,
          "python_supported": True,
          "status": "passed",
        },
        "native-paths.json": {
          "absolute_path_count": 5,
          "check": "paths",
          "environment_precedence": True,
          "explicit_precedence": True,
          "external_path_count": 5,
          "path_count": 5,
          "platform": platform,
          "status": "passed",
        },
        "native-schedule.json": {
          "action": "planned",
          "artifact_written": False,
          "backend": backend,
          "check": "schedule",
          "commands_executed": False,
          "ownership_checked": True,
          "platform": platform,
          "status": "passed",
        },
      }
      for name, payload in payloads.items():
        (artifact / name).write_text(
          json.dumps(payload),
          encoding="utf-8",
        )


def test_aggregates_exact_six_artifacts_into_value_free_evidence(
  tmp_path,
  capsys,
):
  artifact_root = tmp_path / "artifacts"
  artifact_root.mkdir()
  _write_artifacts(artifact_root)
  output_path = tmp_path / "native-evidence.json"
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "aggregate-native-evidence",
    "--artifacts",
    str(artifact_root),
    "--output",
    str(output_path),
    "--validated-at",
    "2026-07-27",
  )) == 0

  expected = {
    "checks": {
      "native_package_install": {
        "expected_result_count": 6,
        "passed_result_count": 6,
        "status": "passed",
      },
      "native_periodic_schedule_dry_run": {
        "expected_platform_count": 3,
        "passed_platform_count": 3,
        "status": "passed",
      },
      "native_standard_paths": {
        "expected_platform_count": 3,
        "passed_platform_count": 3,
        "status": "passed",
      },
    },
    "lifecycle": "provisional",
    "normative_status": "non-normative",
    "promotion_required": True,
    "status": "passed",
    "validated_at": "2026-07-27",
  }
  assert json.loads(output_path.read_text(encoding="utf-8")) == expected
  output = json.loads(capsys.readouterr().out)
  assert output == {
    "artifact_count": 6,
    "platform_count": 3,
    "status": "passed",
  }
  assert str(tmp_path) not in str(output)


def test_rejects_artifact_with_unexpected_value_field(tmp_path):
  evidence = importlib.import_module(
    "tools.session_logs.native_evidence"
  )
  artifact_root = tmp_path / "artifacts"
  artifact_root.mkdir()
  _write_artifacts(artifact_root)
  package_path = (
    artifact_root
    / "native-package-Linux-3.9"
    / "native-package.json"
  )
  payload = json.loads(package_path.read_text(encoding="utf-8"))
  payload["source_path"] = "/private/value"
  package_path.write_text(json.dumps(payload), encoding="utf-8")

  with pytest.raises(evidence.NativeEvidenceError):
    evidence.aggregate_native_evidence(
      artifact_root,
      validated_at="2026-07-27",
    )
