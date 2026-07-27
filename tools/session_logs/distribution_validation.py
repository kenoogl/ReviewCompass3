"""パッケージ導入とOS別dry-runの隔離検証。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

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


class DistributionValidationError(Exception):
  """隔離された配布検証を完了できない。"""


def _within(path, root):
  target = Path(path).resolve()
  boundary = Path(root).resolve()
  return target == boundary or boundary in target.parents


def _copy_source(project_root, source_root):
  try:
    shutil.copytree(
      project_root,
      source_root,
      ignore=shutil.ignore_patterns(
        ".git",
        ".pytest_cache",
        "__pycache__",
        "*.pyc",
      ),
    )
  except OSError as error:
    raise DistributionValidationError(
      "Cannot prepare distribution source"
    ) from error


def _run_checked(runner, command, *, cwd=None):
  try:
    result = runner(
      command,
      cwd=cwd,
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise DistributionValidationError(
      "Distribution command failed"
    ) from error
  if result.returncode != 0:
    raise DistributionValidationError(
      "Distribution command failed"
    )


def _validate_package_install(
  project_root,
  work_root,
  *,
  runner,
):
  source_root = work_root / "source"
  install_root = work_root / "installed"
  _copy_source(project_root, source_root)
  _run_checked(
    runner,
    [
      sys.executable,
      "-m",
      "pip",
      "install",
      "--no-deps",
      "--no-build-isolation",
      "--use-pep517",
      "--target",
      str(install_root),
      str(source_root),
    ],
    cwd=work_root,
  )
  _run_checked(
    runner,
    [
      sys.executable,
      "-c",
      (
        "import sys;"
        "sys.path.insert(0, sys.argv[1]);"
        "import tools.session_logs.entry"
      ),
      str(install_root),
    ],
    cwd=work_root,
  )
  return install_root


def _profile_paths(root):
  class ProfilePlatformDirs:
    user_config_path = root / "config"
    user_data_path = root / "data"
    user_state_path = root / "state"
    user_log_path = root / "log"
    user_cache_path = root / "cache"

  return resolve_deployment_paths(
    platform_dirs_factory=(
      lambda **_arguments: ProfilePlatformDirs()
    ),
  )


def _validate_profiles(work_root, raw_root):
  suffixes = {
    "darwin": ".plist",
    "linux": ".timer",
    "win32": ".xml",
  }
  backend_ids = set()
  profile_count = 0
  for platform_name, suffix in suffixes.items():
    profile_root = work_root / platform_name
    paths = _profile_paths(profile_root)
    candidate = build_portable_config(
      raw_root,
      deployment_paths=paths,
      tool_version="0.0.1",
      environment={},
    )
    request = PeriodicScheduleRequest(
      schedule_path=profile_root / ("schedule" + suffix),
      python_executable=Path(sys.executable).resolve(),
      config_path=candidate.config_file,
      interval_seconds=300,
      stdout_path=paths.log_root / "stdout.log",
      stderr_path=paths.log_root / "stderr.log",
      user_id=0,
    )
    backend = select_schedule_backend(
      platform_name=platform_name,
    )
    result = backend.run(
      "install",
      request,
      dry_run=True,
    )
    if result.action != "planned" or result.status != "ok":
      raise DistributionValidationError(
        "Distribution profile validation failed"
      )
    backend_ids.add(result.backend)
    profile_count += 1
  return profile_count, len(backend_ids)


def validate_distribution(
  project_root,
  work_root,
  raw_root,
  *,
  runner=subprocess.run,
):
  project = Path(project_root)
  work = Path(work_root)
  raw = Path(raw_root)
  if (
    not project.is_absolute()
    or not work.is_absolute()
    or not raw.is_absolute()
    or not (project / "pyproject.toml").is_file()
    or not (project / "setup.py").is_file()
    or not raw.is_dir()
    or work.exists()
    or _within(work, project)
  ):
    raise DistributionValidationError(
      "Unsafe distribution validation inputs"
    )
  try:
    work.mkdir(parents=True)
  except OSError as error:
    raise DistributionValidationError(
      "Cannot prepare distribution work root"
    ) from error
  install_root = _validate_package_install(
    project,
    work,
    runner=runner,
  )
  profile_count, backend_count = _validate_profiles(
    work,
    raw,
  )
  return {
    "backend_count": backend_count,
    "importable": (
      install_root
      / "tools"
      / "session_logs"
      / "entry.py"
    ).is_file(),
    "installed": install_root.is_dir(),
    "profile_count": profile_count,
    "status": "passed",
  }


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--project-root", required=True)
  parser.add_argument("--work-root", required=True)
  parser.add_argument("--raw-root", required=True)
  args = parser.parse_args(argv)
  try:
    result = validate_distribution(
      args.project_root,
      args.work_root,
      args.raw_root,
    )
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
