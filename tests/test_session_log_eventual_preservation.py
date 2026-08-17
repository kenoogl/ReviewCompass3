"""終了hookに依存しないsession log保全のAcceptance Test。"""

import hashlib
import importlib
import json
import stat

import pytest

from shared_fixtures import claude_conversation_records, write_jsonl


def _repository(tmp_path):
  repository = tmp_path / "repository"
  (repository / ".git").mkdir(parents=True)
  return repository


def _write_jsonl(path, records):
  return write_jsonl(path, records)


def _claude_records(secret="SECRET-123"):
  return claude_conversation_records(
    "保存対象 %s" % secret,
    "保存しました。",
  )


def _codex_exec_records():
  return (
    {"type": "thread.started", "thread_id": "thread-1"},
    {
      "type": "item.completed",
      "item": {
        "id": "user-1",
        "type": "user_message",
        "text": "Codex execの会話。",
      },
    },
  )


def _codex_rollout_records():
  return (
    {
      "timestamp": "2026-08-03T10:00:00Z",
      "type": "session_meta",
      "payload": {
        "id": "thread-1",
        "cwd": "/workspace/project",
        "originator": "Codex Desktop",
      },
    },
    {
      "timestamp": "2026-08-03T10:00:01Z",
      "type": "response_item",
      "payload": {
        "id": "user-1",
        "type": "message",
        "role": "user",
        "content": [
          {"type": "input_text", "text": "Codex rolloutの会話。"},
        ],
      },
    },
  )


def _collect(module, raw_log, source_root, private_root, repository, **kwargs):
  return module.collect_source(
    raw_log,
    source_root=source_root,
    private_root=private_root,
    repository_root=repository,
    tool_version="test-v1",
    run_id=kwargs.pop("run_id", "run-1"),
    observed_at=kwargs.pop("observed_at", "2026-08-03T10:00:00+09:00"),
    **kwargs,
  )


def test_collects_raw_private_verbatim_redacted_and_cursor_idempotently(
  tmp_path,
):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "claude" / "session.jsonl"
  raw_bytes = _write_jsonl(raw_log, _claude_records())
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )
  redaction = importlib.import_module("tools.session_logs.redaction")

  created = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    redaction_rules=(redaction.Rule("secret", r"SECRET-[0-9]+"),),
  )
  cursor_before = created.cursor_path.read_bytes()
  repeated = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-2",
    observed_at="2026-08-03T10:05:00+09:00",
    redaction_rules=(redaction.Rule("secret", r"SECRET-[0-9]+"),),
  )

  assert created.action == "created"
  assert repeated.action == "unchanged"
  assert created.state == repeated.state == "reconciled"
  assert created.source_kind == "claude"
  assert created.raw_path.read_bytes() == raw_bytes
  assert "SECRET-123" in created.verbatim_path.read_text(encoding="utf-8")
  redacted_text = created.redacted_path.read_text(encoding="utf-8")
  assert "SECRET-123" not in redacted_text
  assert "[REDACTED:secret]" in redacted_text
  assert created.raw_path != created.verbatim_path
  assert created.verbatim_path != created.redacted_path
  assert created.cursor_path.read_bytes() == cursor_before

  cursor = json.loads(created.cursor_path.read_text(encoding="utf-8"))
  provenance = json.loads(
    created.provenance_path.read_text(encoding="utf-8")
  )
  assert cursor["raw"]["committed_offset"] == len(raw_bytes)
  assert cursor["parse"]["committed_offset"] == len(raw_bytes)
  assert cursor["raw"]["sha256"] == hashlib.sha256(raw_bytes).hexdigest()
  assert cursor["state"] == "reconciled"
  assert provenance["artifacts"]["verbatim_sha256"] == hashlib.sha256(
    created.verbatim_path.read_bytes()
  ).hexdigest()
  assert provenance["artifacts"]["redacted_sha256"] == hashlib.sha256(
    created.redacted_path.read_bytes()
  ).hexdigest()


def test_append_advances_offsets_once_and_preserves_event_order(tmp_path):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  records = _claude_records()
  first_bytes = _write_jsonl(raw_log, records[:1])
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  first = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
  )
  complete_bytes = _write_jsonl(raw_log, records)
  updated = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-2",
  )
  repeated = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-3",
  )

  assert first.action == "created"
  assert first.parsed_size == len(first_bytes)
  assert updated.action == "updated"
  assert updated.parsed_size == len(complete_bytes)
  assert updated.event_count == 2
  assert repeated.action == "unchanged"
  transcript = updated.verbatim_path.read_text(encoding="utf-8")
  assert transcript.count("## user") == 1
  assert transcript.count("## assistant") == 1
  assert transcript.index("## user") < transcript.index("## assistant")


def test_partial_final_line_is_raw_preserved_then_parsed_once(tmp_path):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  records = _claude_records()
  first_line = (
    json.dumps(records[0], ensure_ascii=False) + "\n"
  ).encode("utf-8")
  second_line = (
    json.dumps(records[1], ensure_ascii=False) + "\n"
  ).encode("utf-8")
  split = len(second_line) // 2
  raw_log.parent.mkdir(parents=True)
  raw_log.write_bytes(first_line + second_line[:split])
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  partial = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
  )
  raw_log.write_bytes(first_line + second_line)
  completed = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-2",
  )

  assert partial.state == "parse_incomplete"
  assert partial.raw_size == len(first_line) + split
  assert partial.parsed_size == len(first_line)
  assert partial.event_count == 1
  assert partial.raw_path.read_bytes() == first_line + second_line
  assert completed.state == "reconciled"
  assert completed.event_count == 2
  assert completed.verbatim_path.read_text(encoding="utf-8").count(
    "## assistant"
  ) == 1


def test_rerun_recovers_failure_after_artifacts_before_cursor(
  tmp_path,
  monkeypatch,
):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  _write_jsonl(raw_log, _claude_records())
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )
  original = module._write_cursor

  def fail_cursor(*_args, **_kwargs):
    raise OSError("injected cursor failure")

  monkeypatch.setattr(module, "_write_cursor", fail_cursor)
  with pytest.raises(module.CollectionError):
    _collect(
      module,
      raw_log,
      source_root,
      private_root,
      repository,
    )

  assert tuple((private_root / "raw").rglob("*.jsonl"))
  assert tuple((private_root / "verbatim").rglob("*.md"))
  assert tuple((private_root / "cursors").rglob("*.json")) == ()

  monkeypatch.setattr(module, "_write_cursor", original)
  recovered = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-2",
  )
  assert recovered.action == "created"
  assert recovered.cursor_path.is_file()
  assert recovered.state == "reconciled"


def test_non_prefix_source_change_never_overwrites_archive_or_cursor(tmp_path):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  original_bytes = _write_jsonl(raw_log, _claude_records())
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )
  first = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
  )
  cursor_before = first.cursor_path.read_bytes()
  _write_jsonl(raw_log, _claude_records(secret="CHANGED-999"))

  diverged = _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
    run_id="run-2",
  )

  assert diverged.action == "preserved"
  assert diverged.state == "diverged"
  assert first.raw_path.read_bytes() == original_bytes
  assert first.cursor_path.read_bytes() == cursor_before


def test_rejects_private_output_inside_repository_before_writing(tmp_path):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  _write_jsonl(raw_log, _claude_records())
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  with pytest.raises(module.UnsafeCollectionBoundary):
    _collect(
      module,
      raw_log,
      source_root,
      repository / "private",
      repository,
    )

  assert not (repository / "private").exists()


def test_private_artifacts_use_owner_only_permissions(tmp_path):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  _write_jsonl(raw_log, _claude_records())
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  _collect(
    module,
    raw_log,
    source_root,
    private_root,
    repository,
  )

  directories = tuple(
    path for path in private_root.rglob("*") if path.is_dir()
  ) + (private_root,)
  files = tuple(
    path for path in private_root.rglob("*") if path.is_file()
  )
  assert directories
  assert files
  assert all(
    stat.S_IMODE(path.stat().st_mode) == 0o700
    for path in directories
  )
  assert all(
    stat.S_IMODE(path.stat().st_mode) == 0o600
    for path in files
  )


@pytest.mark.parametrize(("records", "source_kind", "expected_text"), (
  (_claude_records(), "claude", "保存対象"),
  (_codex_exec_records(), "codex_exec_json", "Codex execの会話。"),
  (_codex_rollout_records(), "codex_rollout", "Codex rolloutの会話。"),
))
def test_same_collector_handles_three_source_kinds(
  tmp_path,
  records,
  source_kind,
  expected_text,
):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  _write_jsonl(raw_log, records)
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  result = _collect(
    module,
    raw_log,
    source_root,
    tmp_path / "private",
    repository,
  )

  assert result.source_kind == source_kind
  assert expected_text in result.verbatim_path.read_text(encoding="utf-8")
  assert result.redacted_path is None


def test_reconcile_reports_missing_and_unsupported_without_private_values(
  tmp_path,
):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  first_log = source_root / "first.jsonl"
  second_log = source_root / "nested" / "second.jsonl"
  unknown_log = source_root / "unknown.jsonl"
  _write_jsonl(first_log, _claude_records(secret="FIRST-SECRET"))
  _write_jsonl(second_log, _codex_exec_records())
  unknown_log.write_text("{}\n", encoding="utf-8")
  private_root = tmp_path / "private"
  module = importlib.import_module(
    "tools.session_logs.eventual_preservation"
  )

  initial = module.reconcile_source_root(
    source_root,
    private_root=private_root,
    repository_root=repository,
    tool_version="test-v1",
    run_id="run-1",
    observed_at="2026-08-03T10:00:00+09:00",
  )
  second_log.unlink()
  resumed = module.reconcile_source_root(
    source_root,
    private_root=private_root,
    repository_root=repository,
    tool_version="test-v1",
    run_id="run-2",
    observed_at="2026-08-03T10:05:00+09:00",
  )
  report_text = json.dumps(resumed.report(), ensure_ascii=False)

  assert initial.counts == {
    "failed": 0,
    "missing": 0,
    "succeeded": 2,
    "unsupported": 1,
  }
  assert resumed.counts["missing"] == 1
  assert resumed.counts["unsupported"] == 1
  assert "FIRST-SECRET" not in report_text
  assert str(source_root) not in report_text
  assert str(private_root) not in report_text


def test_manual_entry_reports_counts_without_paths_or_content(tmp_path, capsys):
  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  raw_log = source_root / "session.jsonl"
  _write_jsonl(raw_log, _claude_records(secret="CLI-SECRET"))
  _write_jsonl(
    source_root / "not-selected.jsonl",
    _claude_records(secret="NOT-SELECTED"),
  )
  private_root = tmp_path / "private"
  entry = importlib.import_module("tools.session_logs.entry")

  exit_code = entry.run((
    "collect-eventual",
    "--source-root",
    str(source_root),
    "--private-root",
    str(private_root),
    "--source-relative-path",
    "session.jsonl",
    "--repository-root",
    str(repository),
    "--tool-version",
    "test-v1",
    "--run-id",
    "run-1",
    "--observed-at",
    "2026-08-03T10:00:00+09:00",
  ))
  output = capsys.readouterr().out
  payload = json.loads(output)

  assert exit_code == 0
  assert payload["counts"]["succeeded"] == 1
  assert payload["status"] == "ok"
  assert "CLI-SECRET" not in output
  assert "NOT-SELECTED" not in output
  assert str(source_root) not in output
  assert str(private_root) not in output
  assert len(tuple((private_root / "raw").rglob("*.jsonl"))) == 1


def test_manual_entry_exit_codes_distinguish_partial_from_failure(
  tmp_path, capsys
):
  """終了コードの語彙（作業票2026-08-18・候補IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001）。

  partialは既知の正常状態（保全は全件完了・一部が解釈非対応）であり、失敗コード
  5ではなく非対応コード4（cli.pyのEXIT_UNSUPPORTED）を返す。okは0のまま。
  """

  repository = _repository(tmp_path)
  source_root = tmp_path / "native"
  _write_jsonl(
    source_root / "supported.jsonl", _claude_records(secret="EXIT-OK")
  )
  _write_jsonl(
    source_root / "unsupported.jsonl",
    ({"type": "unknown-kind", "value": 1},),
  )
  private_root = tmp_path / "private"
  entry = importlib.import_module("tools.session_logs.entry")

  exit_code = entry.run((
    "collect-eventual",
    "--source-root",
    str(source_root),
    "--private-root",
    str(private_root),
    "--repository-root",
    str(repository),
    "--tool-version",
    "test-v1",
  ))
  payload = json.loads(capsys.readouterr().out)

  assert payload["status"] == "partial"
  assert payload["counts"]["succeeded"] == 1
  assert payload["counts"]["unsupported"] == 1
  # 保全は完了している（正常状態）ため、失敗コード5を返してはならない
  assert exit_code == 4
