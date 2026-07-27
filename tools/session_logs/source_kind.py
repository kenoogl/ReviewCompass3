"""生セッションログ種別の識別。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
from pathlib import Path


def identify_source_kind(path):
  with Path(path).open(encoding="utf-8") as raw_log:
    first_line = raw_log.readline()

  if not first_line:
    return None

  first_event = json.loads(first_line)
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
    return "codex"

  return None


def identify_auxiliary_kind(path):
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
