"""ポータブル配置先へ書き込む前の非破壊検証。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import os
import shutil
from pathlib import Path

from tools.session_logs.config import load_config


class DeploymentPreflightError(Exception):
  """デプロイ候補を安全に検証できない。"""


@dataclasses.dataclass(frozen=True)
class DeploymentPreflightResult:
  status: str
  check_count: int
  failed_count: int
  reasons: tuple


def _nearest_existing(path):
  candidate = Path(path)
  while not candidate.exists():
    parent = candidate.parent
    if parent == candidate:
      break
    candidate = parent
  return candidate


def _check_directory(
  path,
  *,
  minimum_free_bytes,
  access_check,
  disk_usage,
):
  if path is None:
    return "missing_required_path"
  target = Path(path)
  if not target.is_absolute():
    return "unsafe_relative_path"
  if target.exists() and not target.is_dir():
    return "directory_collision"
  ancestor = _nearest_existing(target)
  try:
    if not ancestor.is_dir():
      return "directory_collision"
    if not access_check(ancestor, os.W_OK):
      return "destination_not_writable"
    if disk_usage(ancestor).free < minimum_free_bytes:
      return "insufficient_space"
  except OSError:
    return "destination_unavailable"
  return None


def preflight_deployment(
  config,
  *,
  minimum_free_bytes=0,
  access_check=os.access,
  disk_usage=shutil.disk_usage,
) -> DeploymentPreflightResult:
  if (
    isinstance(minimum_free_bytes, bool)
    or not isinstance(minimum_free_bytes, int)
    or minimum_free_bytes < 0
  ):
    raise DeploymentPreflightError(
      "Invalid minimum free bytes"
    )
  checks = []
  raw_root = Path(config.raw_root)
  checks.append(
    None
    if raw_root.is_absolute() and raw_root.is_dir()
    else "raw_root_unavailable"
  )
  destinations = (
    config.transcript_root,
    config.summary_root,
    config.provenance_root,
    config.sensitive_report_root,
    config.backup_root,
    (
      Path(config.preservation_ledger_path).parent
      if config.preservation_ledger_path is not None
      else None
    ),
    (
      Path(config.hook_event_log_path).parent
      if config.hook_event_log_path is not None
      else None
    ),
  )
  checks.extend(
    _check_directory(
      destination,
      minimum_free_bytes=minimum_free_bytes,
      access_check=access_check,
      disk_usage=disk_usage,
    )
    for destination in destinations
  )
  failures = tuple(
    reason
    for reason in checks
    if reason is not None
  )
  return DeploymentPreflightResult(
    status="passed" if not failures else "failed",
    check_count=len(checks),
    failed_count=len(failures),
    reasons=tuple(sorted(set(failures))),
  )


def _payload(result):
  return {
    "check_count": result.check_count,
    "failed_count": result.failed_count,
    "reasons": list(result.reasons),
    "status": result.status,
  }


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", required=True)
  parser.add_argument(
    "--minimum-free-bytes",
    type=int,
    default=0,
  )
  args = parser.parse_args(argv)
  try:
    config_path = Path(args.config)
    if not config_path.is_absolute():
      raise DeploymentPreflightError(
        "Config path must be absolute"
      )
    config = load_config(config_path)
    result = preflight_deployment(
      config,
      minimum_free_bytes=args.minimum_free_bytes,
    )
    payload = _payload(result)
  except Exception as error:
    payload = {
      "reason": type(error).__name__,
      "status": "failed",
    }
    print(json.dumps(payload, sort_keys=True))
    return 5
  print(json.dumps(payload, sort_keys=True))
  return 0 if result.status == "passed" else 5


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
