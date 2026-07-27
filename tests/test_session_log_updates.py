"""セッションログ追記専用更新の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_creates_appends_and_remains_idempotent():
  updates = importlib.import_module("tools.session_logs.updates")

  created = updates.merge_append_only((), ("u1", "a1"))
  appended = updates.merge_append_only(created.events, ("u1", "a1", "u2"))
  repeated = updates.merge_append_only(appended.events, ("u1", "a1", "u2"))

  assert created == updates.UpdateResult(
    action="created",
    events=("u1", "a1"),
    appended=("u1", "a1"),
  )
  assert appended == updates.UpdateResult(
    action="updated",
    events=("u1", "a1", "u2"),
    appended=("u2",),
  )
  assert repeated == updates.UpdateResult(
    action="unchanged",
    events=("u1", "a1", "u2"),
    appended=(),
  )


def test_preserves_existing_events_on_non_append_changes():
  updates = importlib.import_module("tools.session_logs.updates")
  existing = ("u1", "a1", "u2")

  shortened = updates.merge_append_only(existing, ("u1", "a1"))
  changed = updates.merge_append_only(existing, ("u1", "changed", "u2"))
  reordered = updates.merge_append_only(existing, ("a1", "u1", "u2"))

  expected = updates.UpdateResult(
    action="preserved",
    events=existing,
    appended=(),
  )
  assert shortened == expected
  assert changed == expected
  assert reordered == expected
