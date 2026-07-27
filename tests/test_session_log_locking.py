"""セッションログ共通排他処理の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_lock_release_does_not_remove_replaced_owner(tmp_path):
  locking = importlib.import_module("tools.session_logs.locking")
  lock_path = tmp_path / "session.lock"

  with locking.exclusive_lock(lock_path, timeout_seconds=60):
    original_token = lock_path.read_text(encoding="utf-8")
    assert original_token
    lock_path.write_text("replacement-owner\n", encoding="utf-8")

  assert lock_path.read_text(encoding="utf-8") == "replacement-owner\n"
