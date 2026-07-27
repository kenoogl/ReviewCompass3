"""生セッションログ保全・復元の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

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
