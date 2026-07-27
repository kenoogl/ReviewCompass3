"""生セッションログの追記専用保全と復元。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import os
from pathlib import Path


class PreservationError(Exception):
  """生ログの保全または復元に失敗した。"""


@dataclasses.dataclass(frozen=True)
class PreservationResult:
  action: str
  source_path: Path
  backup_path: Path


def _replace_file(source, target):
  os.replace(source, target)


def _write_atomic(path, data):
  target = Path(path)
  temporary_path = target.with_name(target.name + ".tmp")
  try:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_bytes(data)
    _replace_file(temporary_path, target)
  except OSError as error:
    raise PreservationError(
      "Failed to write preserved raw log"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)


def _safe_relative_path(value) -> Path:
  relative_path = Path(value)
  if (
    relative_path.is_absolute()
    or ".." in relative_path.parts
  ):
    raise PreservationError("Unsafe raw log relative path")
  return relative_path


def preserve_raw_log(
  raw_log,
  *,
  raw_root,
  backup_root,
) -> PreservationResult:
  source_path = Path(raw_log)
  try:
    relative_path = source_path.relative_to(Path(raw_root))
    source_bytes = source_path.read_bytes()
  except (OSError, ValueError) as error:
    raise PreservationError("Cannot read raw log for preservation") from error
  backup_path = Path(backup_root) / relative_path

  if not backup_path.exists():
    _write_atomic(backup_path, source_bytes)
    action = "created"
  else:
    try:
      backup_bytes = backup_path.read_bytes()
    except OSError as error:
      raise PreservationError("Cannot read preserved raw log") from error
    if source_bytes == backup_bytes:
      action = "unchanged"
    elif source_bytes.startswith(backup_bytes):
      _write_atomic(backup_path, source_bytes)
      action = "updated"
    else:
      action = "preserved"

  return PreservationResult(
    action=action,
    source_path=source_path,
    backup_path=backup_path,
  )


def restore_raw_log(
  relative_path,
  *,
  raw_root,
  backup_root,
) -> PreservationResult:
  safe_path = _safe_relative_path(relative_path)
  source_path = Path(raw_root) / safe_path
  backup_path = Path(backup_root) / safe_path
  try:
    backup_bytes = backup_path.read_bytes()
  except OSError as error:
    raise PreservationError("Cannot read preserved raw log") from error

  if source_path.exists():
    try:
      action = (
        "unchanged"
        if source_path.read_bytes() == backup_bytes
        else "preserved"
      )
    except OSError as error:
      raise PreservationError("Cannot read existing raw log") from error
  else:
    _write_atomic(source_path, backup_bytes)
    action = "restored"

  return PreservationResult(
    action=action,
    source_path=source_path,
    backup_path=backup_path,
  )
