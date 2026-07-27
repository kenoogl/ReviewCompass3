"""ブートストラップreviewの固定CLI・配置境界。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
from pathlib import Path, PurePosixPath
import re


_ATTEMPT_PATTERN = re.compile(r"[a-z0-9][a-z0-9._-]*")


class ReviewCliError(Exception):
  """固定CLIの設定または配置境界が安全でない。"""


def _inside(path, root):
  try:
    path.relative_to(root)
    return True
  except ValueError:
    return False


def _load_layout(config_path):
  path = Path(config_path)
  if not path.is_absolute() or not path.is_file():
    raise ReviewCliError(
      "Review CLI config must be an existing absolute path"
    )
  try:
    config = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
    raise ReviewCliError(
      "Cannot load review CLI config"
    ) from error
  if (
    not isinstance(config, dict)
    or set(config) != {
      "repository_root",
      "private_root",
      "triage_root",
      "attempt_id",
    }
  ):
    raise ReviewCliError(
      "Review CLI config has unknown or missing keys"
    )
  repository = Path(config["repository_root"])
  private = Path(config["private_root"])
  triage_value = config["triage_root"]
  attempt_id = config["attempt_id"]
  triage_relative = PurePosixPath(triage_value)
  if (
    not repository.is_absolute()
    or not repository.is_dir()
    or not private.is_absolute()
    or not isinstance(triage_value, str)
    or triage_relative.is_absolute()
    or any(
      part in ("", ".", "..")
      for part in triage_relative.parts
    )
    or _ATTEMPT_PATTERN.fullmatch(attempt_id or "") is None
  ):
    raise ReviewCliError(
      "Review CLI paths or attempt ID are invalid"
    )
  repository = repository.resolve()
  private = private.resolve()
  triage = repository.joinpath(
    *triage_relative.parts
  ).resolve()
  if (
    _inside(private, repository)
    or not _inside(triage, repository)
  ):
    raise ReviewCliError(
      "Raw and parsed must be private; triage must be in Git scope"
    )
  return repository, private, triage, attempt_id


def run(arguments=None) -> int:
  parser = argparse.ArgumentParser(
    prog="reviewcompass3-bootstrap-review"
  )
  parser.add_argument("--config", required=True)
  parser.add_argument(
    "--dry-run",
    action="store_true",
    required=True,
  )
  try:
    options = parser.parse_args(arguments)
    _load_layout(options.config)
  except (ReviewCliError, SystemExit):
    return 2
  print(json.dumps(
    {
      "parsed_location": "private",
      "raw_location": "private",
      "status": "dry_run",
      "triage_location": "git",
      "writes": 0,
    },
    separators=(",", ":"),
    sort_keys=True,
  ))
  return 0


def main():
  raise SystemExit(run())
