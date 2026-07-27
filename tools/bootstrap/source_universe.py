"""source universeの機械列挙。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from pathlib import Path, PurePosixPath
import subprocess


class SourceUniverseError(Exception):
  """安全なsource universeを列挙できない。"""


def _tracked_paths(repository_root):
  try:
    result = subprocess.run(
      [
        "git",
        "-C",
        str(repository_root),
        "ls-files",
        "--cached",
        "-z",
        "--",
      ],
      capture_output=True,
      check=False,
    )
  except OSError as error:
    raise SourceUniverseError(
      "Cannot enumerate the source universe"
    ) from error

  if result.returncode != 0:
    raise SourceUniverseError(
      "Cannot enumerate the source universe"
    )

  try:
    return tuple(
      value.decode("utf-8")
      for value in result.stdout.split(b"\x00")
      if value
    )
  except UnicodeDecodeError as error:
    raise SourceUniverseError(
      "Source universe paths must be UTF-8"
    ) from error


def _safe_regular_file(repository_root, relative_path):
  parsed = PurePosixPath(relative_path)
  if (
    parsed.is_absolute()
    or not parsed.parts
    or any(part in ("", ".", "..") for part in parsed.parts)
  ):
    raise SourceUniverseError(
      "Source universe contains an unsafe path"
    )

  candidate = repository_root
  for part in parsed.parts:
    candidate = candidate / part
    if candidate.is_symlink():
      return False
  return candidate.is_file()


def enumerate_source_universe(repository_root) -> tuple:
  root = Path(repository_root).resolve()
  if (
    not root.is_dir()
    or not (root / ".git").exists()
  ):
    raise SourceUniverseError(
      "Repository boundary must be an existing Git repository"
    )

  return tuple(sorted(
    relative_path
    for relative_path in _tracked_paths(root)
    if _safe_regular_file(root, relative_path)
  ))
