"""セッションログ処理で共有する所有権付き排他制御。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import os
import time
import uuid
from contextlib import contextmanager
from pathlib import Path


class LockError(Exception):
  """ロックの取得または解放に失敗した。"""


class LockHeld(LockError):
  """有効なロックを別の処理が所有している。"""


def _read_owner(path):
  try:
    return path.read_bytes()
  except FileNotFoundError:
    return None
  except OSError as error:
    raise LockError("Failed to read lock owner") from error


def _release_if_owner(path, owner):
  if _read_owner(path) != owner:
    return
  try:
    path.unlink()
  except FileNotFoundError:
    pass
  except OSError as error:
    raise LockError("Failed to release lock") from error


@contextmanager
def exclusive_lock(path, *, timeout_seconds):
  lock_path = Path(path)
  owner = (uuid.uuid4().hex + "\n").encode("utf-8")
  acquired = False
  try:
    try:
      lock_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
      raise LockError("Failed to prepare lock directory") from error

    for _attempt in range(2):
      try:
        descriptor = os.open(
          str(lock_path),
          os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        )
      except FileExistsError:
        try:
          age = time.time() - lock_path.stat().st_mtime
        except FileNotFoundError:
          continue
        except OSError as error:
          raise LockError("Failed to inspect lock") from error
        if age <= timeout_seconds:
          raise LockHeld("Lock is already held")
        stale_owner = _read_owner(lock_path)
        if stale_owner is not None:
          _release_if_owner(lock_path, stale_owner)
        continue
      except OSError as error:
        raise LockError("Failed to acquire lock") from error

      try:
        os.write(descriptor, owner)
      except OSError as error:
        os.close(descriptor)
        _release_if_owner(lock_path, owner)
        raise LockError("Failed to record lock owner") from error
      else:
        os.close(descriptor)
        acquired = True
        break

    if not acquired:
      raise LockHeld("Lock is already held")
    yield
  finally:
    if acquired:
      _release_if_owner(lock_path, owner)
