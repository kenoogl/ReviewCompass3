"""前置record解釈（契約014）のAcceptance Test。

契約候補v2（records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v2.md）
§7の取り決めを固定する。
- §7.1 正準列：既知前置4種の必須欄・スキップ上限16・偽装/未知/本文不在はfail-closed
- §7.2 互換：本文形式・Codex 2形式の従来判定は不変
- §7.3 解釈器は前置4種を無issueでスキップ（他の非会話recordは従来どおりissue計上）
- §7.4 補助分類：本文recordへ到達できるfileは補助でない
- §7.5-1 敵対fixture 5形（(a)偽装前置・(b)欠落前置・(c)未知混入・(d)本文なし・(e)上限超過）
"""

import importlib
import json

from shared_fixtures import claude_conversation_records, write_jsonl


def _source_kind():
  return importlib.import_module("tools.session_logs.source_kind")


def _parse_claude():
  return importlib.import_module("tools.session_logs.parse_claude")


def _encode(records):
  return b"".join(
    (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    for record in records
  )


def _queue_record(**overrides):
  record = {
    "type": "queue-operation",
    "operation": "enqueue",
    "sessionId": "session-1",
    "content": "queued",
  }
  record.update(overrides)
  return record


def _mode_record():
  return {"type": "mode", "mode": "normal", "sessionId": "session-1"}


def _title_record():
  return {
    "type": "custom-title",
    "customTitle": "作業表題",
    "sessionId": "session-1",
  }


def _agent_record():
  return {"type": "started", "agentId": "agent-1", "key": "task-1"}


def _body_records():
  return claude_conversation_records("保存対象の本文。", "はい。")


def test_identify_bytes_skips_queue_prefix():
  source_kind = _source_kind()
  data = _encode((_queue_record(), _queue_record(), _queue_record())
                 + _body_records())

  assert source_kind.identify_source_kind_bytes(data) == "claude"


def test_identify_bytes_skips_all_known_prefix_kinds():
  source_kind = _source_kind()
  data = _encode((
    _queue_record(),
    _mode_record(),
    _title_record(),
    _agent_record(),
  ) + _body_records())

  assert source_kind.identify_source_kind_bytes(data) == "claude"


def test_identify_bytes_plain_body_and_codex_unchanged():
  source_kind = _source_kind()

  assert source_kind.identify_source_kind_bytes(
    _encode(_body_records())
  ) == "claude"
  assert source_kind.identify_source_kind_bytes(_encode((
    {"type": "thread.started", "thread_id": "thread-1"},
  ))) == "codex_exec_json"
  assert source_kind.identify_source_kind_bytes(_encode((
    {
      "type": "session_meta",
      "timestamp": "2026-08-17T10:00:00Z",
      "payload": {"id": "thread-1"},
    },
  ))) == "codex_rollout"


def test_identify_bytes_rejects_prefix_only_file():
  source_kind = _source_kind()
  data = _encode((_queue_record(), _mode_record()))

  assert source_kind.identify_source_kind_bytes(data) is None


def test_identify_bytes_rejects_unknown_kind_in_prefix_run():
  source_kind = _source_kind()
  data = _encode((
    _queue_record(),
    {"type": "unknown-marker", "sessionId": "session-1"},
  ) + _body_records())

  assert source_kind.identify_source_kind_bytes(data) is None


def test_identify_bytes_rejects_malformed_prefix_record():
  source_kind = _source_kind()
  malformed = {
    "type": "queue-operation",
    "operation": "enqueue",
    "sessionId": "session-1",
  }
  data = _encode((malformed,) + _body_records())

  assert source_kind.identify_source_kind_bytes(data) is None


def test_identify_bytes_rejects_forged_body_like_prefix():
  source_kind = _source_kind()
  forged = _queue_record(uuid="user-1")
  data = _encode((forged,))

  assert source_kind.identify_source_kind_bytes(data) is None


def test_identify_bytes_rejects_prefix_run_over_limit():
  source_kind = _source_kind()
  data = _encode(tuple(_queue_record() for _ in range(17)) + _body_records())

  assert source_kind.identify_source_kind_bytes(data) is None


def test_identify_source_kind_path_skips_prefix(tmp_path):
  source_kind = _source_kind()
  raw_log = tmp_path / "prefixed.jsonl"
  write_jsonl(raw_log, (_queue_record(), _mode_record()) + _body_records())

  assert source_kind.identify_source_kind(raw_log) == "claude"


def test_parse_claude_skips_prefix_without_issues():
  parse_claude = _parse_claude()
  body_only = parse_claude.parse_claude_bytes(_encode(_body_records()))
  with_prefix = parse_claude.parse_claude_bytes(_encode((
    _queue_record(),
    _mode_record(),
    _title_record(),
    _agent_record(),
  ) + _body_records()))

  assert with_prefix.issues == ()
  assert [event.event_id for event in with_prefix.events] == [
    event.event_id for event in body_only.events
  ]
  assert with_prefix.events


def test_parse_claude_keeps_issue_for_unknown_records():
  parse_claude = _parse_claude()
  result = parse_claude.parse_claude_bytes(_encode((
    {"type": "unknown-marker", "sessionId": "session-1"},
  ) + _body_records()))

  unknown_issues = [
    issue for issue in result.issues if issue.kind == "unsupported_event"
  ]
  assert len(unknown_issues) == 1


def test_parse_claude_forged_prefix_not_event():
  parse_claude = _parse_claude()
  body_only = parse_claude.parse_claude_bytes(_encode(_body_records()))
  result = parse_claude.parse_claude_bytes(_encode((
    _queue_record(uuid="user-1"),
  ) + _body_records()))

  assert result.issues == ()
  assert [event.event_id for event in result.events] == [
    event.event_id for event in body_only.events
  ]


def test_auxiliary_none_for_prefixed_body_file(tmp_path):
  source_kind = _source_kind()
  raw_log = tmp_path / "prefixed-body.jsonl"
  write_jsonl(raw_log, (_queue_record(), _queue_record()) + _body_records())

  assert source_kind.identify_auxiliary_kind(raw_log) is None


def test_auxiliary_kind_for_bodyless_queue_file(tmp_path):
  source_kind = _source_kind()
  raw_log = tmp_path / "bodyless-queue.jsonl"
  write_jsonl(raw_log, (_queue_record(), _queue_record()))

  assert source_kind.identify_auxiliary_kind(raw_log) == "claude_queue"


def test_auxiliary_kind_for_bodyless_agent_file(tmp_path):
  source_kind = _source_kind()
  raw_log = tmp_path / "bodyless-agent.jsonl"
  write_jsonl(raw_log, (_agent_record(),))

  assert source_kind.identify_auxiliary_kind(raw_log) == "claude_agent"
