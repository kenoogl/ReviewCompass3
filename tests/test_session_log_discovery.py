"""生セッションログ発見の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


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
