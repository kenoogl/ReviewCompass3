"""生セッションログ保全・復元の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import hashlib
import json
import os
import time

import pytest


def test_preserves_append_only_raw_log_idempotently_and_restores_loss(
  tmp_path,
):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  backup_root = tmp_path / "private-backup"
  first = b'{"event": 1}\n'
  appended = b'{"event": 2}\n'
  raw_log.write_bytes(first)
  preservation = importlib.import_module(
    "tools.session_logs.preservation"
  )

  created = preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
  )
  raw_log.write_bytes(first + appended)
  updated = preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
  )
  repeated = preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
  )

  backup_path = backup_root / "nested" / "session.jsonl"
  assert created.action == "created"
  assert updated.action == "updated"
  assert repeated.action == "unchanged"
  assert backup_path.read_bytes() == first + appended

  raw_log.write_bytes(b'{"event": "changed"}\n')
  preserved = preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
  )

  assert preserved.action == "preserved"
  assert backup_path.read_bytes() == first + appended

  raw_log.unlink()
  restored = preservation.restore_raw_log(
    "nested/session.jsonl",
    raw_root=raw_root,
    backup_root=backup_root,
  )

  assert restored.action == "restored"
  assert raw_log.read_bytes() == first + appended

  raw_log.write_bytes(b"existing\n")
  not_overwritten = preservation.restore_raw_log(
    "nested/session.jsonl",
    raw_root=raw_root,
    backup_root=backup_root,
  )
  assert not_overwritten.action == "preserved"
  assert raw_log.read_bytes() == b"existing\n"


def test_preservation_failure_keeps_existing_backup(tmp_path, monkeypatch):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  backup_root = tmp_path / "private-backup"
  first = b'{"event": 1}\n'
  raw_log.write_bytes(first)
  preservation = importlib.import_module(
    "tools.session_logs.preservation"
  )
  preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
  )
  raw_log.write_bytes(first + b'{"event": 2}\n')

  def fail_replace(source, target):
    raise OSError("injected preservation failure")

  monkeypatch.setattr(preservation, "_replace_file", fail_replace)

  with pytest.raises(preservation.PreservationError):
    preservation.preserve_raw_log(
      raw_log,
      raw_root=raw_root,
      backup_root=backup_root,
    )

  backup_path = backup_root / "session.jsonl"
  assert backup_path.read_bytes() == first
  assert tuple(backup_root.rglob("*.tmp")) == ()


def test_preservation_lock_rejects_active_and_reclaims_stale_lock(
  tmp_path,
):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  raw_log.write_bytes(b'{"event": 1}\n')
  backup_root = tmp_path / "private-backup"
  lock_path = backup_root / "session.jsonl.lock"
  lock_path.parent.mkdir(parents=True)
  lock_path.write_text("active\n", encoding="utf-8")
  preservation = importlib.import_module(
    "tools.session_logs.preservation"
  )

  with pytest.raises(preservation.PreservationLocked):
    preservation.preserve_raw_log(
      raw_log,
      raw_root=raw_root,
      backup_root=backup_root,
      lock_timeout_seconds=60,
    )

  assert lock_path.is_file()
  assert not (backup_root / "session.jsonl").exists()

  stale_time = time.time() - 120
  os.utime(lock_path, (stale_time, stale_time))
  result = preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
    lock_timeout_seconds=60,
  )

  assert result.action == "created"
  assert not lock_path.exists()


def test_integrity_ledger_blocks_restore_of_tampered_backup(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  raw_bytes = b'{"event": "original"}\n'
  raw_log.write_bytes(raw_bytes)
  backup_root = tmp_path / "private-backup"
  ledger_path = tmp_path / "safe-records" / "preservation.json"
  preservation = importlib.import_module(
    "tools.session_logs.preservation"
  )

  preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
    ledger_path=ledger_path,
  )

  assert json.loads(ledger_path.read_text(encoding="utf-8")) == {
    "entries": {
      "nested/session.jsonl": {
        "action": "created",
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "size": len(raw_bytes),
      },
    },
    "version": 1,
  }

  raw_log.unlink()
  backup_path = backup_root / "nested" / "session.jsonl"
  backup_path.write_bytes(b'{"event": "tampered private value"}\n')
  with pytest.raises(
    preservation.PreservationIntegrityError
  ) as error:
    preservation.restore_raw_log(
      "nested/session.jsonl",
      raw_root=raw_root,
      backup_root=backup_root,
      ledger_path=ledger_path,
    )

  assert str(error.value) == "Preserved raw log integrity mismatch"
  assert "tampered private value" not in repr(error.value)
  assert not raw_log.exists()


def _preservation():
  return importlib.import_module("tools.session_logs.preservation")


def test_tampered_backup_is_not_legitimised_by_a_later_preservation(tmp_path):
  """F-E6反証：保全を1回挟んでも、改変backupを台帳の正本にできない。"""
  preservation = _preservation()
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  backup_root = tmp_path / "backup"
  ledger_path = tmp_path / "ledger.json"
  original = b'{"event": 1}\n'
  raw_log.write_bytes(original)
  preservation.preserve_raw_log(
    raw_log,
    raw_root=raw_root,
    backup_root=backup_root,
    ledger_path=ledger_path,
  )

  backup_path = backup_root / "session.jsonl"
  tampered = b'{"event": "tampered"}\n'
  backup_path.write_bytes(tampered)

  with pytest.raises(preservation.PreservationIntegrityError):
    preservation.preserve_raw_log(
      raw_log,
      raw_root=raw_root,
      backup_root=backup_root,
      ledger_path=ledger_path,
    )

  entry = json.loads(ledger_path.read_text(encoding="utf-8"))["entries"][
    "session.jsonl"
  ]
  assert entry["sha256"] == hashlib.sha256(original).hexdigest()

  raw_log.unlink()
  with pytest.raises(preservation.PreservationIntegrityError):
    preservation.restore_raw_log(
      "session.jsonl",
      raw_root=raw_root,
      backup_root=backup_root,
      ledger_path=ledger_path,
    )
  assert not raw_log.exists()


def test_raw_log_symlink_pointing_outside_root_is_rejected(tmp_path):
  """F-E7反証（読取り側）：root外を指すsymlinkをrawの正本として扱わない。"""
  preservation = _preservation()
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  backup_root = tmp_path / "backup"
  outside = tmp_path / "outside" / "secret.jsonl"
  outside.parent.mkdir(parents=True)
  outside.write_bytes(b'{"secret": true}\n')
  link = raw_root / "session.jsonl"
  link.symlink_to(outside)

  with pytest.raises(preservation.PreservationError):
    preservation.preserve_raw_log(
      link,
      raw_root=raw_root,
      backup_root=backup_root,
    )
  assert not (backup_root / "session.jsonl").exists()


def test_backup_directory_symlink_escaping_root_is_rejected(tmp_path):
  """F-E7反証（書込み側）：backup root外へ書き出すsymlinkは拒否する。"""
  preservation = _preservation()
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "nested" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  raw_log.write_bytes(b'{"event": 1}\n')
  backup_root = tmp_path / "backup"
  backup_root.mkdir()
  outside = tmp_path / "outside"
  outside.mkdir()
  (backup_root / "nested").symlink_to(outside, target_is_directory=True)

  with pytest.raises(preservation.PreservationError):
    preservation.preserve_raw_log(
      raw_log,
      raw_root=raw_root,
      backup_root=backup_root,
    )
  assert not (outside / "session.jsonl").exists()


def test_restore_target_symlink_escaping_raw_root_is_rejected(tmp_path):
  """F-E7反証（復元側）：復元先がroot外を指す場合は書かない。"""
  preservation = _preservation()
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  backup_root = tmp_path / "backup"
  backup_path = backup_root / "nested" / "session.jsonl"
  backup_path.parent.mkdir(parents=True)
  backup_path.write_bytes(b'{"event": 1}\n')
  outside = tmp_path / "outside"
  outside.mkdir()
  (raw_root / "nested").symlink_to(outside, target_is_directory=True)

  with pytest.raises(preservation.PreservationError):
    preservation.restore_raw_log(
      "nested/session.jsonl",
      raw_root=raw_root,
      backup_root=backup_root,
    )
  assert not (outside / "session.jsonl").exists()
