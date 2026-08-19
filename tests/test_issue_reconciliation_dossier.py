"""issue実態調書tool（機械調書・判断欄なし）の契約試験。"""

import json
import subprocess
import sys
from pathlib import Path

from tests.test_issue_state_transition import _register_issue
from tests.test_triage_decision_writer import _fixture_root

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_fixture_dossier_reports_activity_and_flags(tmp_path):
  from tools.development import issue_reconciliation_dossier as dossier

  root = _fixture_root(tmp_path)
  issue_id, _path = _register_issue(root)
  note = root / "records" / "development" / "2026-08-19-fixture-note-v1.md"
  note.write_text(f"# 記録\n\n{issue_id} への言及。\n", encoding="utf-8")
  todo = root / "TODO_NEXT_SESSION.md"
  todo.write_text(
    f"- `{issue_id}`：`registered`、影響：x、次：状態を変更しない\n",
    encoding="utf-8",
  )

  exit_code, result = dossier.build_dossier(project_root=root)

  assert exit_code == 0
  assert result["status"] == "ok"
  assert result["issue_total"] == 1
  entry = result["issues"][0]
  assert entry["issue_id"] == issue_id
  assert entry["state"] == "registered"
  assert entry["activity"]["records_mention_count"] == 1
  assert entry["activity"]["records_latest"] == note.name
  assert entry["activity"]["git_mention_count"] is None
  assert entry["todo_active"] is True
  assert "状態を変更しない" in entry["todo_line"]


def test_unknown_issue_id_is_rejected(tmp_path):
  from tools.development import issue_reconciliation_dossier as dossier

  root = _fixture_root(tmp_path)
  _register_issue(root)

  exit_code, result = dossier.build_dossier(
    project_root=root, issue_id="ISSUE-NOPE-001"
  )

  assert exit_code != 0
  assert result["status"] == "issue_not_found"


def test_todo_flag_is_false_without_mention(tmp_path):
  from tools.development import issue_reconciliation_dossier as dossier

  root = _fixture_root(tmp_path)
  _register_issue(root)

  exit_code, result = dossier.build_dossier(project_root=root)

  assert exit_code == 0
  entry = result["issues"][0]
  assert entry["todo_active"] is False
  assert entry["todo_line"] is None


def test_module_entry_reports_real_repository():
  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.issue_reconciliation_dossier",
    ],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True,
    timeout=120,
  )

  assert completed.returncode == 0
  payload = json.loads(completed.stdout.strip().splitlines()[-1])
  assert payload["issue_total"] == 8
  by_id = {entry["issue_id"]: entry for entry in payload["issues"]}
  pinned = by_id["ISSUE-TEST-GROWTH-STATE-PINNING-001"]
  assert pinned["todo_active"] is True
  resolved_states = {
    entry["issue_id"]: entry["state"] for entry in payload["issues"]
  }
  assert resolved_states["ISSUE-HTC-C9F6C917"] == "resolved"
