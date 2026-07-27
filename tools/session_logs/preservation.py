"""生セッションログの追記専用保全と復元。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path

from tools.session_logs.locking import LockError, LockHeld, exclusive_lock


class PreservationError(Exception):
  """生ログの保全または復元に失敗した。"""


class PreservationLocked(PreservationError):
  """別の処理が同じ生ログを保全している。"""


class PreservationIntegrityError(PreservationError):
  """保全ログと完全性台帳が一致しない。"""


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


def _load_ledger(path):
  ledger_path = Path(path)
  if not ledger_path.exists():
    return {
      "entries": {},
      "version": 1,
    }
  try:
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if (
      not isinstance(ledger, dict)
      or ledger.get("version") != 1
      or not isinstance(ledger.get("entries"), dict)
    ):
      raise ValueError("invalid ledger")
  except (OSError, ValueError) as error:
    raise PreservationIntegrityError(
      "Cannot read preservation integrity ledger"
    ) from error
  return ledger


def _update_ledger(
  path,
  relative_path,
  backup_bytes,
  action,
  *,
  timeout_seconds,
):
  ledger_path = Path(path)
  lock_path = ledger_path.with_name(ledger_path.name + ".lock")
  with _preservation_lock(
    lock_path,
    timeout_seconds=timeout_seconds,
  ):
    ledger = _load_ledger(ledger_path)
    entries = dict(ledger["entries"])
    entries[Path(relative_path).as_posix()] = {
      "action": action,
      "sha256": hashlib.sha256(backup_bytes).hexdigest(),
      "size": len(backup_bytes),
    }
    encoded = (
      json.dumps(
        {
          "entries": entries,
          "version": 1,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
      ) + "\n"
    ).encode("utf-8")
    _write_atomic(ledger_path, encoded)


def _verify_ledger(path, relative_path, backup_bytes):
  ledger = _load_ledger(path)
  entry = ledger["entries"].get(Path(relative_path).as_posix())
  expected_digest = hashlib.sha256(backup_bytes).hexdigest()
  if (
    not isinstance(entry, dict)
    or entry.get("size") != len(backup_bytes)
    or entry.get("sha256") != expected_digest
  ):
    raise PreservationIntegrityError(
      "Preserved raw log integrity mismatch"
    )


@contextmanager
def _preservation_lock(path, *, timeout_seconds):
  try:
    with exclusive_lock(path, timeout_seconds=timeout_seconds):
      yield
  except LockHeld as error:
    raise PreservationLocked(
      "Raw log preservation is already locked"
    ) from error
  except LockError as error:
    raise PreservationError(
      "Failed to manage raw log preservation lock"
    ) from error


def preserve_raw_log(
  raw_log,
  *,
  raw_root,
  backup_root,
  ledger_path=None,
  lock_timeout_seconds=300,
) -> PreservationResult:
  source_path = Path(raw_log)
  try:
    relative_path = source_path.relative_to(Path(raw_root))
    source_bytes = source_path.read_bytes()
  except (OSError, ValueError) as error:
    raise PreservationError("Cannot read raw log for preservation") from error
  backup_path = Path(backup_root) / relative_path
  lock_path = backup_path.with_name(backup_path.name + ".lock")

  with _preservation_lock(
    lock_path,
    timeout_seconds=lock_timeout_seconds,
  ):
    if not backup_path.exists():
      _write_atomic(backup_path, source_bytes)
      backup_bytes = source_bytes
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
        backup_bytes = source_bytes
        action = "updated"
      else:
        action = "preserved"
    if ledger_path is not None:
      _update_ledger(
        ledger_path,
        relative_path,
        backup_bytes,
        action,
        timeout_seconds=lock_timeout_seconds,
      )

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
  ledger_path=None,
  lock_timeout_seconds=300,
) -> PreservationResult:
  safe_path = _safe_relative_path(relative_path)
  source_path = Path(raw_root) / safe_path
  backup_path = Path(backup_root) / safe_path
  lock_path = backup_path.with_name(backup_path.name + ".lock")
  with _preservation_lock(
    lock_path,
    timeout_seconds=lock_timeout_seconds,
  ):
    try:
      backup_bytes = backup_path.read_bytes()
    except OSError as error:
      raise PreservationError("Cannot read preserved raw log") from error
    if ledger_path is not None:
      _verify_ledger(ledger_path, safe_path, backup_bytes)

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
