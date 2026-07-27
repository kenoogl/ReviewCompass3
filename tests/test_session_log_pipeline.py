"""セッションログ統括パイプラインの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def test_prepares_redacted_transcript_with_provenance(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  secret = "sk-ant-pipeline_secret"
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "key=%s" % secret,
      },
    }) + "\n",
    encoding="utf-8",
  )

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  redaction = importlib.import_module("tools.session_logs.redaction")

  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=(
      redaction.Rule(
        label="anthropic_key",
        pattern=r"sk-ant-[A-Za-z0-9_-]+",
      ),
    ),
    tool_version="0.0.1",
    commits=("abc1234 Add feature",),
    changed_files=("z.py", "a.py"),
  )

  assert artifact.source_kind == "claude"
  assert artifact.text == (
    "## user\n\n"
    "key=[REDACTED:anthropic_key]\n"
  )
  assert secret not in artifact.text
  assert artifact.parse_issues == ()
  assert artifact.redaction_findings == (
    redaction.Finding(label="anthropic_key", count=1),
  )
  assert artifact.provenance.source_path == "session.jsonl"
  assert artifact.provenance.transcript_sha256 == hashlib.sha256(
    artifact.text.encode("utf-8")
  ).hexdigest()
  assert artifact.summary_text == (
    "# Session summary\n\n"
    "## User messages\n\n"
    "- key=[REDACTED:anthropic_key]\n\n"
    "## Commits\n\n"
    "- abc1234 Add feature\n\n"
    "## Changed files\n\n"
    "- a.py\n"
    "- z.py\n\n"
    "## Decisions\n\n"
    "- Not inferred automatically.\n"
  )
  assert artifact.provenance.summary_sha256 == hashlib.sha256(
    artifact.summary_text.encode("utf-8")
  ).hexdigest()
  assert len(artifact.events) == 1


def test_pipeline_fails_closed_when_high_entropy_remains(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  secret = "A9fK2mQ7xR4vT8pL3nC6sW1yH5jD0bZ"
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "token=%s" % secret,
      },
    }) + "\n",
    encoding="utf-8",
  )

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  redaction = importlib.import_module("tools.session_logs.redaction")

  with pytest.raises(redaction.SensitiveDataRemaining) as error:
    pipeline.prepare_artifact(
      raw_log,
      raw_root=raw_root,
      rules=(),
      tool_version="0.0.1",
    )

  assert secret not in repr(error.value)
