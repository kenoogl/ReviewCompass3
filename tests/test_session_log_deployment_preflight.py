"""デプロイ事前検証の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
from pathlib import Path


def _write_candidate(tmp_path, *, transcript_collision=False):
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )
  portable_config = importlib.import_module(
    "tools.session_logs.portable_config"
  )
  raw_root = tmp_path / "private-raw"
  raw_root.mkdir()
  data_root = tmp_path / "portable-data"
  if transcript_collision:
    data_root.mkdir()
    (data_root / "transcripts").write_text(
      "collision",
      encoding="utf-8",
    )
  paths = deployment_paths.DeploymentPaths(
    config_file=tmp_path / "config" / "session-logs.json",
    data_root=data_root,
    state_root=tmp_path / "portable-state",
    log_root=tmp_path / "portable-log",
    cache_root=tmp_path / "portable-cache",
  )
  candidate = portable_config.build_portable_config(
    raw_root,
    deployment_paths=paths,
    tool_version="0.0.1",
  )
  candidate.config_file.parent.mkdir()
  candidate.config_file.write_text(
    candidate.render(),
    encoding="utf-8",
  )
  return candidate, paths


def test_preflight_cli_checks_without_creating_destinations(
  tmp_path,
  capsys,
):
  candidate, paths = _write_candidate(tmp_path)
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "preflight",
    "--config",
    str(candidate.config_file),
    "--minimum-free-bytes",
    "1",
  )) == 0

  assert json.loads(capsys.readouterr().out) == {
    "check_count": 8,
    "failed_count": 0,
    "reasons": [],
    "status": "passed",
  }
  assert not paths.data_root.exists()
  assert not paths.state_root.exists()
  assert not paths.log_root.exists()
  assert not paths.cache_root.exists()


def test_preflight_cli_reports_collision_without_path_value(
  tmp_path,
  capsys,
):
  candidate, paths = _write_candidate(
    tmp_path,
    transcript_collision=True,
  )
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "preflight",
    "--config",
    str(candidate.config_file),
  )) == 5

  output = capsys.readouterr().out
  assert json.loads(output) == {
    "check_count": 8,
    "failed_count": 1,
    "reasons": ["directory_collision"],
    "status": "failed",
  }
  assert str(paths.data_root) not in output
