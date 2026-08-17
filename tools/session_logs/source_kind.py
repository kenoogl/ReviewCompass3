"""生セッションログ種別の識別。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
from pathlib import Path


def _identify_first_event(first_event):
  if not isinstance(first_event, dict):
    return None

  uuid = first_event.get("uuid")
  session_id = first_event.get("sessionId")
  if isinstance(uuid, str) and uuid and isinstance(session_id, str) and session_id:
    return "claude"

  thread_id = first_event.get("thread_id")
  if (
    first_event.get("type") == "thread.started"
    and isinstance(thread_id, str)
    and thread_id
  ):
    return "codex_exec_json"

  payload = first_event.get("payload")
  if (
    first_event.get("type") == "session_meta"
    and isinstance(first_event.get("timestamp"), str)
    and isinstance(payload, dict)
    and isinstance(payload.get("id"), str)
    and payload.get("id")
  ):
    return "codex_rollout"

  return None


_PREFIX_TYPES = ("queue-operation", "mode", "custom-title", "started")

PREFIX_RECORD_LIMIT = 16


def is_known_prefix_record(record):
  """既知前置record（契約014 §7.1の必須欄）か判定する。"""
  if not isinstance(record, dict):
    return False
  record_type = record.get("type")
  session_id = record.get("sessionId")
  if record_type == "queue-operation":
    operation = record.get("operation")
    if not (isinstance(session_id, str) and session_id):
      return False
    if operation == "enqueue":
      return "content" in record
    # dequeueはcontentを持たない実物形（契約014 v3 §7.1）
    return operation == "dequeue"
  if record_type == "mode":
    return (
      isinstance(record.get("mode"), str)
      and isinstance(session_id, str)
      and bool(session_id)
    )
  if record_type == "custom-title":
    return (
      isinstance(record.get("customTitle"), str)
      and isinstance(session_id, str)
      and bool(session_id)
    )
  if record_type == "started":
    agent_id = record.get("agentId")
    key = record.get("key")
    return (
      isinstance(agent_id, str)
      and bool(agent_id)
      and isinstance(key, str)
      and bool(key)
    )
  return False


def _iter_records(lines):
  for line in lines:
    if not line.strip():
      continue
    try:
      yield json.loads(line)
    except json.JSONDecodeError:
      yield None
      return


def _identify_record_stream(records):
  # 契約014 §7.1：先頭から連続する既知前置recordだけを読み飛ばし
  # （typeが前置4種なら必須欄不足で打ち切り・上限16超過で打ち切り）、
  # 最初の判定可能recordで従来判定を行う。
  skipped = 0
  for record in records:
    if not isinstance(record, dict):
      return None
    if record.get("type") in _PREFIX_TYPES:
      if not is_known_prefix_record(record):
        return None
      skipped += 1
      if skipped > PREFIX_RECORD_LIMIT:
        return None
      continue
    return _identify_first_event(record)
  return None


def identify_source_kind_bytes(data):
  text = data.decode("utf-8")
  return _identify_record_stream(_iter_records(text.split("\n")))


def identify_source_kind(path):
  try:
    with Path(path).open(encoding="utf-8") as raw_log:
      return _identify_record_stream(_iter_records(raw_log))
  except OSError:
    return None


def identify_auxiliary_kind(path):
  # 契約014 §7.4：本文recordへ到達できるfileは補助でない。
  if identify_source_kind(path) is not None:
    return None
  with Path(path).open(encoding="utf-8") as raw_log:
    first_line = raw_log.readline()

  if not first_line:
    return None

  first_event = json.loads(first_line)
  if not isinstance(first_event, dict):
    return None

  if (
    first_event.get("type") == "queue-operation"
    and first_event.get("operation") in ("enqueue", "dequeue")
    and isinstance(first_event.get("sessionId"), str)
    and first_event.get("sessionId")
    and "content" in first_event
  ):
    return "claude_queue"

  if (
    first_event.get("type") == "started"
    and isinstance(first_event.get("agentId"), str)
    and first_event.get("agentId")
    and isinstance(first_event.get("key"), str)
    and first_event.get("key")
  ):
    return "claude_agent"

  return None
