"""セッションログ統括パイプラインの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json


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
  assert len(artifact.events) == 1
