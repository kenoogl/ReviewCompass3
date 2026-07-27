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
