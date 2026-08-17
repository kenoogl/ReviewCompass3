"""セッションログ記録run wrapper（record-run）のAcceptance Test。

作業票v2（docs/development/2026-08-17-session-log-run-procedure-work-ticket-v2.md）§2の仕様を固定する。
- 3系統の値のコード固定（転記排除）
- 系統ごとの単独プロセス順次実行と集約（partialは成功扱い）
- 進行中セッションの機械分離：方式(i)＝実行中の変化検出＋実行開始直前の活動窓。既定除外・指定時包含
- 要約はcounts集計のみ（file単位の深掘り・絶対path・本文を出さない）
"""

import importlib
import json
import os
import time

from shared_fixtures import claude_conversation_records, write_jsonl


def _repository(tmp_path):
  repository = tmp_path / "repository"
  (repository / ".git").mkdir(parents=True)
  return repository


def _claude_records(secret="SECRET-123"):
  return claude_conversation_records(
    "保存対象 %s" % secret,
    "保存しました。",
  )


def _queue_records():
  return (
    {
      "type": "queue-operation",
      "operation": "enqueue",
      "sessionId": "queued-session",
      "content": "queued",
    },
  )


def _make_old(path, days=2):
  stamp = time.time() - days * 86400
  os.utime(path, (stamp, stamp))


def _record_run():
  return importlib.import_module("tools.session_logs.record_run")


def test_default_systems_and_private_root_are_fixed():
  record_run = _record_run()

  assert record_run.DEFAULT_PRIVATE_ROOT == (
    "/Users/keno/.reviewcompass3/projects/reviewcompass3"
    "/development/sensitive/eventual-preservation"
  )
  systems = {
    label: (source_root, tool_version)
    for label, source_root, tool_version in record_run.DEFAULT_SYSTEMS
  }
  assert systems == {
    "claude": (
      "/Users/keno/.claude/projects",
      "reviewcompass3-historical-claude-capture-v1",
    ),
    "codex現行": (
      "/Users/keno/.codex/sessions",
      "reviewcompass3-historical-codex-capture-v1",
    ),
    "codex保管": (
      "/Users/keno/.codex/archived_sessions",
      "reviewcompass3-historical-codex-capture-v1",
    ),
  }


def test_partition_in_progress_detects_recent_and_changed():
  record_run = _record_run()
  started_at_ns = 1_000_000_000_000_000_000
  window_ns = 600 * 10**9
  before = {
    "recent.jsonl": (10, started_at_ns - window_ns + 10**9),
    "old.jsonl": (10, started_at_ns - window_ns - 10**9),
    "changed.jsonl": (10, started_at_ns - window_ns - 10**9),
  }
  after = {
    "recent.jsonl": (10, started_at_ns - window_ns + 10**9),
    "old.jsonl": (10, started_at_ns - window_ns - 10**9),
    "changed.jsonl": (20, started_at_ns + 10**9),
    "appeared.jsonl": (5, started_at_ns + 2 * 10**9),
  }

  in_progress = record_run.partition_in_progress(
    before,
    after,
    started_at_ns=started_at_ns,
    window_ns=window_ns,
  )

  assert in_progress == frozenset(
    {"recent.jsonl", "changed.jsonl", "appeared.jsonl"}
  )


def test_collect_run_aggregates_two_systems(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  systems = []
  for name in ("alpha", "beta"):
    source_root = tmp_path / name
    raw_log = source_root / ("%s-session.jsonl" % name)
    write_jsonl(raw_log, _claude_records(secret="OLD-%s" % name.upper()))
    _make_old(raw_log)
    systems.append((name, str(source_root), "test-capture-v1"))

  summary = record_run.collect_run(
    systems=tuple(systems),
    private_root=private_root,
    repository_root=repository,
  )

  assert summary["overall_ok"] is True
  assert [system["label"] for system in summary["systems"]] == [
    "alpha",
    "beta",
  ]
  for system in summary["systems"]:
    assert system["status"] == "ok"
    assert system["exit_code"] == 0
    assert system["counts"]["succeeded"] == 1
    assert system["in_progress_count"] == 0
  assert len(tuple((private_root / "raw").rglob("*.jsonl"))) == 2


def test_collect_run_treats_partial_as_success(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "mixed"
  supported = source_root / "supported.jsonl"
  write_jsonl(supported, _claude_records(secret="MIXED-OK"))
  _make_old(supported)
  queued = source_root / "queued.jsonl"
  write_jsonl(queued, _queue_records())
  _make_old(queued)

  summary = record_run.collect_run(
    systems=(("mixed", str(source_root), "test-capture-v1"),),
    private_root=private_root,
    repository_root=repository,
  )

  system = summary["systems"][0]
  assert system["status"] == "partial"
  # partialの系統は非対応コード4（失敗の5ではない。候補IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001）
  assert system["exit_code"] == 4
  assert system["counts"]["succeeded"] == 1
  assert system["counts"]["unsupported"] == 1
  assert summary["overall_ok"] is True


def test_collect_run_reports_failure_for_broken_runner(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "solo"
  raw_log = source_root / "session.jsonl"
  write_jsonl(raw_log, _claude_records(secret="SOLO"))
  _make_old(raw_log)

  def broken_runner(argv):
    return 7, "not-json"

  summary = record_run.collect_run(
    systems=(("solo", str(source_root), "test-capture-v1"),),
    private_root=private_root,
    repository_root=repository,
    runner=broken_runner,
  )

  system = summary["systems"][0]
  assert system["status"] == "runner_error"
  assert summary["overall_ok"] is False


def test_collect_run_partitions_in_progress_by_default(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "active"
  finished = source_root / "old-session.jsonl"
  write_jsonl(finished, _claude_records(secret="OLD-DONE"))
  _make_old(finished)
  active = source_root / "active-session.jsonl"
  write_jsonl(active, _claude_records(secret="ACTIVE-NOW"))

  summary = record_run.collect_run(
    systems=(("active", str(source_root), "test-capture-v1"),),
    private_root=private_root,
    repository_root=repository,
  )

  system = summary["systems"][0]
  assert system["in_progress_count"] == 1
  assert summary["in_progress"]["total"] == 1
  assert summary["in_progress"]["files"] == []
  assert "保全" in summary["in_progress"]["note"]
  assert len(tuple((private_root / "raw").rglob("*.jsonl"))) == 2
  assert summary["overall_ok"] is True


def test_collect_run_includes_in_progress_when_requested(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "active"
  active = source_root / "active-session.jsonl"
  write_jsonl(active, _claude_records(secret="ACTIVE-NOW"))

  summary = record_run.collect_run(
    systems=(("active", str(source_root), "test-capture-v1"),),
    private_root=private_root,
    repository_root=repository,
    include_in_progress=True,
  )

  assert summary["in_progress"]["total"] == 1
  assert summary["in_progress"]["files"] == ["active-session.jsonl"]
  assert "実行時点" in summary["in_progress"]["note"]


def test_collect_run_window_override_disables_recent_partition(tmp_path):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "quiet"
  raw_log = source_root / "session.jsonl"
  write_jsonl(raw_log, _claude_records(secret="QUIET"))

  summary = record_run.collect_run(
    systems=(("quiet", str(source_root), "test-capture-v1"),),
    private_root=private_root,
    repository_root=repository,
    window_seconds=0,
  )

  assert summary["systems"][0]["in_progress_count"] == 0
  assert summary["in_progress"]["total"] == 0


def test_run_cli_outputs_summary_json_without_paths_or_content(
  tmp_path, capsys
):
  record_run = _record_run()
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "cli"
  raw_log = source_root / "session.jsonl"
  write_jsonl(raw_log, _claude_records(secret="CLI-HIDDEN"))
  _make_old(raw_log)
  systems_file = tmp_path / "systems.json"
  systems_file.write_text(
    json.dumps([["cli", str(source_root), "test-capture-v1"]]),
    encoding="utf-8",
  )

  exit_code = record_run.run((
    "--systems-file",
    str(systems_file),
    "--private-root",
    str(private_root),
    "--repository-root",
    str(repository),
  ))
  output = capsys.readouterr().out
  payload = json.loads(output.strip().splitlines()[-1])

  assert exit_code == 0
  assert payload["overall_ok"] is True
  assert payload["systems"][0]["label"] == "cli"
  assert str(source_root) not in output
  assert str(private_root) not in output
  assert "CLI-HIDDEN" not in output


def test_entry_delegates_record_run(tmp_path, capsys):
  repository = _repository(tmp_path)
  private_root = tmp_path / "private"
  source_root = tmp_path / "delegated"
  raw_log = source_root / "session.jsonl"
  write_jsonl(raw_log, _claude_records(secret="DELEGATED"))
  _make_old(raw_log)
  systems_file = tmp_path / "systems.json"
  systems_file.write_text(
    json.dumps([["delegated", str(source_root), "test-capture-v1"]]),
    encoding="utf-8",
  )
  entry = importlib.import_module("tools.session_logs.entry")

  exit_code = entry.run((
    "record-run",
    "--systems-file",
    str(systems_file),
    "--private-root",
    str(private_root),
    "--repository-root",
    str(repository),
  ))
  output = capsys.readouterr().out
  payload = json.loads(output.strip().splitlines()[-1])

  assert exit_code == 0
  assert payload["overall_ok"] is True
  assert payload["systems"][0]["label"] == "delegated"
