"""CLI要約材料の安全な収集に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import subprocess


def _git(repository, *arguments):
  return subprocess.run(
    ["git", "-C", str(repository), *arguments],
    capture_output=True,
    check=True,
    text=True,
  ).stdout.strip()


def test_cli_collects_redacted_summary_material_from_explicit_range(
  tmp_path,
  capsys,
):
  repository = tmp_path / "repository"
  repository.mkdir()
  _git(repository, "init")
  _git(repository, "config", "user.name", "Session Test")
  _git(repository, "config", "user.email", "session@example.invalid")
  (repository / "base.txt").write_text("base\n", encoding="utf-8")
  _git(repository, "add", "base.txt")
  _git(repository, "commit", "-m", "Add base")
  secret = "sk-ant-summary_secret"
  (repository / "feature.py").write_text("value = 1\n", encoding="utf-8")
  _git(repository, "add", "feature.py")
  _git(repository, "commit", "-m", "Add %s" % secret)
  expected_commit = "%s Add [REDACTED:anthropic_key]" % _git(
    repository,
    "rev-parse",
    "--short",
    "HEAD",
  )

  private_root = tmp_path / "private"
  raw_log = private_root / "raw" / "session.jsonl"
  raw_log.parent.mkdir(parents=True)
  raw_log.write_text(
    '{"uuid":"user-1","type":"user","sessionId":"session-1",'
    '"message":{"role":"user","content":"Review."}}\n',
    encoding="utf-8",
  )
  config_path = repository / "session-logs.json"
  config_path.write_text(
    json.dumps({
      "repository_root": ".",
      "raw_root": "../private/raw",
      "transcript_root": "../private/transcripts",
      "summary_root": "summaries",
      "provenance_root": "provenance",
      "sensitive_report_root": "../private/sensitive-reports",
      "summary_revision_range": "HEAD~1..HEAD",
      "tool_version": "0.0.1",
      "redaction_rules": [
        {
          "label": "anthropic_key",
          "pattern": "sk-ant-[A-Za-z0-9_-]+",
        },
      ],
      "allow_patterns": [],
    }),
    encoding="utf-8",
  )
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 0

  summary_path = repository / "summaries" / "session.md"
  provenance_path = repository / "provenance" / "session.json"
  summary = summary_path.read_text(encoding="utf-8")
  provenance = provenance_path.read_text(encoding="utf-8")
  assert expected_commit in summary
  assert "- feature.py" in summary
  assert secret not in summary
  assert secret not in provenance
  state = json.loads(provenance)
  assert state["provenance"]["summary_commits"] == [expected_commit]
  assert state["provenance"]["summary_changed_files"] == ["feature.py"]

  assert cli.run((
    "--config",
    str(config_path),
    "--verify",
  )) == 0
  assert json.loads(capsys.readouterr().out)["status"] == "matches"
