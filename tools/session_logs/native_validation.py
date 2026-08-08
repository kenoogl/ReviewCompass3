"""ネイティブ環境で配布境界を値なし検証する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import importlib
import json
import os
import sys
from pathlib import Path


class NativeValidationError(Exception):
  """ネイティブ配布検証を安全に完了できない。"""


def _platform_family(platform_name=None):
  selected = sys.platform if platform_name is None else platform_name
  if selected == "darwin":
    return "macos"
  if selected.startswith("linux"):
    return "linux"
  if selected == "win32":
    return "windows"
  raise NativeValidationError("Unsupported native platform")


def validate_installed_package():
  if sys.version_info < (3, 9):
    raise NativeValidationError("Unsupported Python version")
  try:
    entry = importlib.import_module("tools.session_logs.entry")
  except ImportError as error:
    raise NativeValidationError(
      "Installed entry is unavailable"
    ) from error
  if not callable(getattr(entry, "run", None)):
    raise NativeValidationError(
      "Installed entry is unavailable"
    )
  return {
    "check": "package",
    "entry_importable": True,
    "platform": _platform_family(),
    "python_supported": True,
    "status": "passed",
  }


from tools.common.paths import within as _within


def _portable_roots(candidate):
  payload = candidate.payload
  return (
    candidate.config_file,
    Path(payload["transcript_root"]).parent,
    Path(payload["preservation_ledger_path"]).parent,
    Path(payload["hook_event_log_path"]).parent,
  )


def _variant_paths(paths, label):
  return {
    "config_file": paths.config_file.with_name(
      label + "-session-logs.json"
    ),
    "data_root": paths.data_root.with_name(
      paths.data_root.name + "-" + label
    ),
    "state_root": paths.state_root.with_name(
      paths.state_root.name + "-" + label
    ),
    "log_root": paths.log_root.with_name(
      paths.log_root.name + "-" + label
    ),
  }


def validate_native_paths(
  repository_root,
  raw_root,
  *,
  platform_dirs_factory=None,
):
  from tools.session_logs.deployment_paths import (
    resolve_deployment_paths,
  )
  from tools.session_logs.portable_config import (
    build_portable_config,
  )
  repository = Path(repository_root)
  raw = Path(raw_root)
  if not repository.is_absolute() or not raw.is_absolute():
    raise NativeValidationError(
      "Native validation paths must be absolute"
    )
  paths = resolve_deployment_paths(
    platform_dirs_factory=platform_dirs_factory,
  )
  path_values = tuple(Path(value) for value in dataclasses.astuple(paths))
  absolute_count = sum(path.is_absolute() for path in path_values)
  external_count = sum(
    not _within(path, repository)
    for path in path_values
  )
  if (
    absolute_count != len(path_values)
    or external_count != len(path_values)
  ):
    raise NativeValidationError(
      "Unsafe native deployment paths"
    )

  environment_paths = _variant_paths(paths, "environment")
  environment = {
    "REVIEWCOMPASS3_CONFIG_FILE": str(
      environment_paths["config_file"]
    ),
    "REVIEWCOMPASS3_DATA_ROOT": str(
      environment_paths["data_root"]
    ),
    "REVIEWCOMPASS3_STATE_ROOT": str(
      environment_paths["state_root"]
    ),
    "REVIEWCOMPASS3_LOG_ROOT": str(
      environment_paths["log_root"]
    ),
  }
  environment_candidate = build_portable_config(
    raw,
    deployment_paths=paths,
    tool_version="native-validation",
    environment=environment,
  )
  environment_precedence = (
    _portable_roots(environment_candidate)
    == tuple(environment_paths.values())
  )

  explicit_paths = _variant_paths(paths, "explicit")
  explicit_candidate = build_portable_config(
    raw,
    deployment_paths=paths,
    tool_version="native-validation",
    environment=environment,
    overrides=explicit_paths,
  )
  explicit_precedence = (
    _portable_roots(explicit_candidate)
    == tuple(explicit_paths.values())
  )
  if not environment_precedence or not explicit_precedence:
    raise NativeValidationError(
      "Native deployment precedence failed"
    )
  return {
    "absolute_path_count": absolute_count,
    "check": "paths",
    "environment_precedence": environment_precedence,
    "explicit_precedence": explicit_precedence,
    "external_path_count": external_count,
    "path_count": len(path_values),
    "platform": _platform_family(),
    "status": "passed",
  }


def validate_native_schedule(
  raw_root,
  validation_root,
  *,
  platform_name=None,
  platform_dirs_factory=None,
):
  from tools.session_logs.deployment_paths import (
    resolve_deployment_paths,
  )
  from tools.session_logs.portable_config import (
    build_portable_config,
  )
  from tools.session_logs.schedule_backends import (
    PeriodicScheduleRequest,
    select_schedule_backend,
  )
  selected_platform = (
    sys.platform
    if platform_name is None
    else platform_name
  )
  suffixes = {
    "darwin": ".plist",
    "linux": ".timer",
    "win32": ".xml",
  }
  suffix = suffixes.get(selected_platform)
  raw = Path(raw_root)
  validation = Path(validation_root)
  if (
    suffix is None
    or not raw.is_absolute()
    or not validation.is_absolute()
    or validation.exists()
  ):
    raise NativeValidationError(
      "Unsafe native schedule inputs"
    )
  paths = resolve_deployment_paths(
    platform_dirs_factory=platform_dirs_factory,
  )
  candidate = build_portable_config(
    raw,
    deployment_paths=paths,
    tool_version="native-validation",
    environment={},
  )
  schedule_path = validation / ("schedule" + suffix)
  request = PeriodicScheduleRequest(
    schedule_path=schedule_path,
    python_executable=Path(sys.executable).resolve(),
    config_path=candidate.config_file,
    interval_seconds=300,
    stdout_path=paths.log_root / "stdout.log",
    stderr_path=paths.log_root / "stderr.log",
    user_id=0,
  )
  backend = select_schedule_backend(
    platform_name=selected_platform,
  )
  result = backend.run(
    "install",
    request,
    dry_run=True,
  )
  artifact_written = (
    schedule_path.exists()
    or schedule_path.with_suffix(".service").exists()
  )
  if (
    result.action != "planned"
    or result.status != "ok"
    or artifact_written
  ):
    raise NativeValidationError(
      "Native schedule dry run failed"
    )
  return {
    "action": result.action,
    "artifact_written": artifact_written,
    "backend": result.backend,
    "check": "schedule",
    "commands_executed": False,
    "ownership_checked": True,
    "platform": _platform_family(selected_platform),
    "status": "passed",
  }


def _write_evidence(path, payload):
  evidence_path = Path(path)
  if not evidence_path.is_absolute():
    raise NativeValidationError(
      "Native evidence path must be absolute"
    )
  temporary_path = evidence_path.with_name(
    evidence_path.name + ".tmp"
  )
  try:
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(payload, indent=2, sort_keys=True) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, evidence_path)
  except OSError as error:
    raise NativeValidationError(
      "Cannot write native evidence"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--check",
    required=True,
    choices=("package", "paths", "schedule"),
  )
  parser.add_argument("--evidence", required=True)
  parser.add_argument("--project-root")
  parser.add_argument("--raw-root")
  parser.add_argument("--validation-root")
  args = parser.parse_args(argv)
  try:
    if args.check == "package":
      result = validate_installed_package()
    elif args.check == "paths":
      if args.project_root is None or args.raw_root is None:
        raise NativeValidationError(
          "Native path inputs are required"
        )
      result = validate_native_paths(
        args.project_root,
        args.raw_root,
      )
    else:
      if args.raw_root is None or args.validation_root is None:
        raise NativeValidationError(
          "Native schedule inputs are required"
        )
      result = validate_native_schedule(
        args.raw_root,
        args.validation_root,
      )
    _write_evidence(args.evidence, result)
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  print(json.dumps(result, sort_keys=True))
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
