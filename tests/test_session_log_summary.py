"""セッションログ要約の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_summarizes_user_messages_commits_and_changed_files_safely(tmp_path):
  raw_root = tmp_path / "raw"
  raw_log = raw_root / "session.jsonl"
  raw_root.mkdir()
  secret = "sk-ant-summary_secret"
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "Review key %s." % secret,
      },
    }) + "\n",
    encoding="utf-8",
  )

  pipeline = importlib.import_module("tools.session_logs.pipeline")
  redaction = importlib.import_module("tools.session_logs.redaction")
  summary = importlib.import_module("tools.session_logs.summary")
  rules = (
    redaction.Rule(
      label="anthropic_key",
      pattern=r"sk-ant-[A-Za-z0-9_-]+",
    ),
  )
  artifact = pipeline.prepare_artifact(
    raw_log,
    raw_root=raw_root,
    rules=rules,
    tool_version="0.0.1",
  )

  result = summary.render_summary(
    artifact.events,
    commits=("abc1234 Add feature",),
    changed_files=("z.py", "a.py", "z.py"),
    rules=rules,
  )

  assert result.text == (
    "# Session summary\n\n"
    "## User messages\n\n"
    "- Review key [REDACTED:anthropic_key].\n\n"
    "## Commits\n\n"
    "- abc1234 Add feature\n\n"
    "## Changed files\n\n"
    "- a.py\n"
    "- z.py\n\n"
    "## Decisions\n\n"
    "- Not inferred automatically.\n"
  )
  assert result.redaction_findings == (
    redaction.Finding(label="anthropic_key", count=1),
  )
  assert secret not in repr(result)
