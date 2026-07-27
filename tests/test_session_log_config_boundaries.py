"""セッションログ保存区分とGit漏洩防止の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _safe_config_data():
  return {
    "repository_root": "..",
    "raw_root": "../../private/raw",
    "transcript_root": "../../private/transcripts",
    "summary_root": "../summaries",
    "provenance_root": "../provenance",
    "sensitive_report_root": "../../private/sensitive-reports",
    "backup_root": "../../private/backups",
    "preservation_enabled": True,
    "tool_version": "0.0.1",
    "redaction_rules": [],
    "allow_patterns": [],
  }


def _write_repository_config(tmp_path, data):
  repository_root = tmp_path / "repository"
  (repository_root / ".git").mkdir(parents=True)
  config_path = repository_root / "config" / "session-logs.json"
  config_path.parent.mkdir()
  config_path.write_text(json.dumps(data), encoding="utf-8")
  return repository_root, config_path


def test_config_enforces_private_and_git_safe_storage_boundaries(
  tmp_path,
):
  repository_root, config_path = _write_repository_config(
    tmp_path,
    _safe_config_data(),
  )
  config_module = importlib.import_module("tools.session_logs.config")

  config = config_module.load_config(config_path)

  assert config.repository_root == repository_root
  assert config.summary_root == repository_root / "summaries"
  assert config.provenance_root == repository_root / "provenance"
  assert config.raw_root == tmp_path / "private" / "raw"
  assert config.transcript_root == (
    tmp_path / "private" / "transcripts"
  )


@pytest.mark.parametrize("private_key", (
  "raw_root",
  "transcript_root",
  "sensitive_report_root",
  "backup_root",
))
def test_config_rejects_private_storage_inside_repository(
  tmp_path,
  private_key,
):
  data = _safe_config_data()
  data[private_key] = "../leaked-private-data"
  _repository_root, config_path = _write_repository_config(
    tmp_path,
    data,
  )
  config_module = importlib.import_module("tools.session_logs.config")

  with pytest.raises(config_module.ConfigError) as error:
    config_module.load_config(config_path)

  assert str(error.value) == (
    "Unsafe Git storage boundary: %s" % private_key
  )
  assert "leaked-private-data" not in str(error.value)


@pytest.mark.parametrize("git_key", (
  "summary_root",
  "provenance_root",
))
def test_config_rejects_git_artifacts_outside_repository(
  tmp_path,
  git_key,
):
  data = _safe_config_data()
  data[git_key] = "../../private/misplaced-git-artifact"
  _repository_root, config_path = _write_repository_config(
    tmp_path,
    data,
  )
  config_module = importlib.import_module("tools.session_logs.config")

  with pytest.raises(config_module.ConfigError) as error:
    config_module.load_config(config_path)

  assert str(error.value) == (
    "Unsafe Git storage boundary: %s" % git_key
  )


def test_cli_rejects_unsafe_boundary_before_discovery(tmp_path):
  data = _safe_config_data()
  data["raw_root"] = "../raw"
  repository_root, config_path = _write_repository_config(
    tmp_path,
    data,
  )
  raw_log = repository_root / "raw" / "session.jsonl"
  raw_log.parent.mkdir()
  raw_log.write_text(
    json.dumps({
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {
        "role": "user",
        "content": "Must not be processed.",
      },
    }) + "\n",
    encoding="utf-8",
  )
  cli = importlib.import_module("tools.session_logs.cli")

  assert cli.run(("--config", str(config_path))) == 5
  assert not (repository_root / "summaries").exists()
  assert not (repository_root / "provenance").exists()
