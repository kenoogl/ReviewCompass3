"""ネイティブCIの値なしartifactを件数証拠へ集約する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import datetime
import json
import os
from pathlib import Path


class NativeEvidenceError(Exception):
  """ネイティブCI証拠を安全に集約できない。"""


_PLATFORMS = {
  "Linux": ("linux", "systemd_user"),
  "macOS": ("macos", "launchd"),
  "Windows": ("windows", "windows_task"),
}

_PYTHON_VERSIONS = ("3.9", "3.13")


def _artifact_specs():
  return {
    "native-package-%s-%s" % (runner_name, python_version): (
      platform,
      backend,
    )
    for runner_name, (platform, backend) in _PLATFORMS.items()
    for python_version in _PYTHON_VERSIONS
  }


def _expected_payloads(platform, backend):
  return {
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


def _validated_date(value):
  try:
    parsed = datetime.date.fromisoformat(value)
  except (TypeError, ValueError) as error:
    raise NativeEvidenceError(
      "Invalid native evidence date"
    ) from error
  if parsed.isoformat() != value:
    raise NativeEvidenceError(
      "Invalid native evidence date"
    )
  return value


def _read_exact_payload(path, expected):
  evidence_path = Path(path)
  if evidence_path.is_symlink() or not evidence_path.is_file():
    raise NativeEvidenceError(
      "Native evidence artifact is unavailable"
    )
  try:
    payload = json.loads(
      evidence_path.read_text(encoding="utf-8")
    )
  except (OSError, ValueError) as error:
    raise NativeEvidenceError(
      "Cannot read native evidence artifact"
    ) from error
  if payload != expected:
    raise NativeEvidenceError(
      "Unexpected native evidence payload"
    )


def aggregate_native_evidence(
  artifact_root,
  *,
  validated_at,
):
  root = Path(artifact_root)
  if not root.is_absolute() or root.is_symlink() or not root.is_dir():
    raise NativeEvidenceError(
      "Unsafe native artifact root"
    )
  specs = _artifact_specs()
  try:
    entries = tuple(root.iterdir())
  except OSError as error:
    raise NativeEvidenceError(
      "Cannot inspect native artifact root"
    ) from error
  if (
    {entry.name for entry in entries} != set(specs)
    or any(entry.is_symlink() or not entry.is_dir() for entry in entries)
  ):
    raise NativeEvidenceError(
      "Unexpected native artifact set"
    )
  passed_platforms = set()
  for artifact_name, (platform, backend) in specs.items():
    artifact = root / artifact_name
    expected_payloads = _expected_payloads(platform, backend)
    try:
      files = tuple(artifact.iterdir())
    except OSError as error:
      raise NativeEvidenceError(
        "Cannot inspect native evidence artifact"
      ) from error
    if {item.name for item in files} != set(expected_payloads):
      raise NativeEvidenceError(
        "Unexpected native evidence file set"
      )
    for name, expected in expected_payloads.items():
      _read_exact_payload(artifact / name, expected)
    passed_platforms.add(platform)
  date_value = _validated_date(validated_at)
  platform_count = len(passed_platforms)
  artifact_count = len(specs)
  if platform_count != 3 or artifact_count != 6:
    raise NativeEvidenceError(
      "Incomplete native evidence"
    )
  return {
    "checks": {
      "native_package_install": {
        "expected_result_count": 6,
        "passed_result_count": artifact_count,
        "status": "passed",
      },
      "native_periodic_schedule_dry_run": {
        "expected_platform_count": 3,
        "passed_platform_count": platform_count,
        "status": "passed",
      },
      "native_standard_paths": {
        "expected_platform_count": 3,
        "passed_platform_count": platform_count,
        "status": "passed",
      },
    },
    "lifecycle": "provisional",
    "normative_status": "non-normative",
    "promotion_required": True,
    "status": "passed",
    "validated_at": date_value,
  }


def _write_evidence(path, payload):
  output_path = Path(path)
  if not output_path.is_absolute():
    raise NativeEvidenceError(
      "Native evidence output must be absolute"
    )
  temporary_path = output_path.with_name(output_path.name + ".tmp")
  try:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(payload, indent=2, sort_keys=True) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, output_path)
  except OSError as error:
    raise NativeEvidenceError(
      "Cannot write native evidence"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--artifacts", required=True)
  parser.add_argument("--output", required=True)
  parser.add_argument("--validated-at", required=True)
  args = parser.parse_args(argv)
  try:
    evidence = aggregate_native_evidence(
      args.artifacts,
      validated_at=args.validated_at,
    )
    _write_evidence(args.output, evidence)
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  print(json.dumps({
    "artifact_count": 6,
    "platform_count": 3,
    "status": "passed",
  }, sort_keys=True))
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
