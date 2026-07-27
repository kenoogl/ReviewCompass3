"""生セッションログ発見の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_discovers_jsonl_recursively_as_sorted_relative_paths(tmp_path):
  raw_root = tmp_path / "raw"
  nested = raw_root / "subagents"
  nested.mkdir(parents=True)
  (raw_root / "z-session.jsonl").write_text("{}\n", encoding="utf-8")
  (nested / "a-session.jsonl").write_text("{}\n", encoding="utf-8")
  (raw_root / "ignore.txt").write_text("対象外\n", encoding="utf-8")

  discovery = importlib.import_module("tools.session_logs.discovery")

  assert discovery.discover_raw_logs(raw_root) == (
    "subagents/a-session.jsonl",
    "z-session.jsonl",
  )


def test_returns_empty_tuple_for_empty_root(tmp_path):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()

  discovery = importlib.import_module("tools.session_logs.discovery")

  assert discovery.discover_raw_logs(raw_root) == ()


def test_rejects_missing_root(tmp_path):
  missing_root = tmp_path / "missing"

  discovery = importlib.import_module("tools.session_logs.discovery")

  with pytest.raises(FileNotFoundError):
    discovery.discover_raw_logs(missing_root)


def test_rejects_file_as_root(tmp_path):
  file_root = tmp_path / "raw.jsonl"
  file_root.write_text("{}\n", encoding="utf-8")

  discovery = importlib.import_module("tools.session_logs.discovery")

  with pytest.raises(NotADirectoryError):
    discovery.discover_raw_logs(file_root)


def test_excludes_symlinked_jsonl(tmp_path):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  outside_log = tmp_path / "outside.jsonl"
  outside_log.write_text("{}\n", encoding="utf-8")
  (raw_root / "linked.jsonl").symlink_to(outside_log)

  discovery = importlib.import_module("tools.session_logs.discovery")

  assert discovery.discover_raw_logs(raw_root) == ()


def test_discovers_unreadable_jsonl_without_opening_it(tmp_path):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  raw_log = raw_root / "session.jsonl"
  raw_log.write_text("{}\n", encoding="utf-8")
  raw_log.chmod(0)

  discovery = importlib.import_module("tools.session_logs.discovery")

  try:
    assert discovery.discover_raw_logs(raw_root) == ("session.jsonl",)
  finally:
    raw_log.chmod(0o600)
