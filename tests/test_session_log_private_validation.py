"""私的領域での実ログ検証ハーネスの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import subprocess

import pytest


def _git_status(repository_root):
  return subprocess.run(
    [
      "git",
      "-C",
      str(repository_root),
      "status",
      "--porcelain=v1",
      "--untracked-files=all",
    ],
    capture_output=True,
    check=True,
    text=True,
  ).stdout


def test_private_validation_records_counts_without_values_or_git_changes(
  tmp_path,
):
  repository_root = tmp_path / "repository"
  repository_root.mkdir()
  subprocess.run(
    ["git", "init", str(repository_root)],
    capture_output=True,
    check=True,
    text=True,
  )
  raw_root = tmp_path / "private" / "raw"
  raw_root.mkdir(parents=True)
  private_text = "Private validation sentence."
  (raw_root / "claude.jsonl").write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": private_text,
      },
    }) + "\n",
    encoding="utf-8",
  )
  (raw_root / "codex.jsonl").write_text(
    '{"type":"thread.started","thread_id":"thread-1"}\n'
    '{"type":"item.completed","item":{"id":"agent-1",'
    '"type":"agent_message","text":"Private Codex sentence."}}\n',
    encoding="utf-8",
  )
  evidence_path = (
    tmp_path / "private" / "evidence" / "validation.json"
  )
  before = _git_status(repository_root)
  validation = importlib.import_module(
    "tools.session_logs.private_validation"
  )

  result = validation.validate_private_logs(
    raw_root,
    repository_root=repository_root,
    evidence_path=evidence_path,
    rules=(),
    tool_version="0.0.1",
  )

  assert result.status == "passed"
  assert result.git_unchanged is True
  assert result.counts == {
    "claude": 1,
    "codex": 1,
    "failed": 0,
    "unsupported": 0,
  }
  evidence = evidence_path.read_text(encoding="utf-8")
  assert json.loads(evidence) == {
    "counts": result.counts,
    "git_unchanged": True,
    "status": "passed",
  }
  assert private_text not in evidence
  assert str(raw_root) not in evidence
  assert _git_status(repository_root) == before


def test_private_validation_rejects_repository_paths_without_leaking_them(
  tmp_path,
):
  repository_root = tmp_path / "repository-private-name"
  raw_root = repository_root / "raw-secret-name"
  raw_root.mkdir(parents=True)
  (repository_root / ".git").mkdir()
  validation = importlib.import_module(
    "tools.session_logs.private_validation"
  )

  with pytest.raises(validation.PrivateValidationError) as error:
    validation.validate_private_logs(
      raw_root,
      repository_root=repository_root,
      evidence_path=tmp_path / "evidence.json",
      rules=(),
      tool_version="0.0.1",
    )

  assert str(error.value) == "Unsafe private validation boundary"
  assert "private-name" not in repr(error.value)
  assert "secret-name" not in repr(error.value)


def test_private_validation_fixed_cli_outputs_counts_only(
  tmp_path,
  capsys,
):
  repository_root = tmp_path / "repository"
  repository_root.mkdir()
  subprocess.run(
    ["git", "init", str(repository_root)],
    capture_output=True,
    check=True,
    text=True,
  )
  raw_root = tmp_path / "private" / "raw"
  raw_root.mkdir(parents=True)
  private_text = "Private fixed CLI sentence."
  (raw_root / "session.jsonl").write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": private_text,
      },
    }) + "\n",
    encoding="utf-8",
  )
  evidence_path = tmp_path / "private" / "validation.json"
  config_path = tmp_path / "private" / "session-logs.json"
  config_path.write_text(
    json.dumps({
      "raw_root": "unused-raw",
      "transcript_root": "unused-transcripts",
      "summary_root": "unused-summaries",
      "provenance_root": "unused-provenance",
      "tool_version": "0.0.1",
      "redaction_rules": [],
      "allow_patterns": [],
    }),
    encoding="utf-8",
  )
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "validate-private",
    "--raw-root",
    str(raw_root),
    "--repository-root",
    str(repository_root),
    "--evidence",
    str(evidence_path),
    "--config",
    str(config_path),
  )) == 0

  output = capsys.readouterr().out
  assert json.loads(output) == {
    "counts": {
      "claude": 1,
      "codex": 0,
      "failed": 0,
      "unsupported": 0,
    },
    "git_unchanged": True,
    "status": "passed",
  }
  assert private_text not in output
  assert str(raw_root) not in output


def test_private_validation_fixed_cli_rejects_relative_paths(capsys):
  validation = importlib.import_module(
    "tools.session_logs.private_validation"
  )

  assert validation.run((
    "--raw-root",
    "relative-raw",
    "--repository-root",
    "relative-repository",
    "--evidence",
    "relative-evidence.json",
    "--config",
    "relative-config.json",
  )) == 5

  assert json.loads(capsys.readouterr().out) == {
    "reason": "PrivateValidationError",
    "status": "failed",
  }
