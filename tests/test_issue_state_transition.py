"""issue状態遷移（版遷移・置換・rollback）の契約試験。"""

import json
import subprocess
import sys
from pathlib import Path

from tests.test_issue_record_writer import _make_promotion_decision
from tests.test_triage_decision_writer import _fixture_root

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ISSUE_DIRECTORY = ".reviewcompass/workflow/issues-v4"


def _register_issue(root, number="001"):
  from tools.development import issue_record_writer as writer

  candidate_id, decision_path = _make_promotion_decision(root, number=number)
  exit_code, result = writer.register_from_decision(
    decision_path, project_root=root
  )
  assert exit_code == 0
  return f"ISSUE-{candidate_id}", root / result["path"]


def test_transition_replaces_file_and_bumps_version(tmp_path):
  from tools.development import issue_state_transition as transition

  root = _fixture_root(tmp_path)
  issue_id, first_path = _register_issue(root)
  original = json.loads(first_path.read_text(encoding="utf-8"))

  exit_code, result = transition.transition(
    issue_id, "in_progress", project_root=root
  )

  assert exit_code == 0
  assert result["status"] == "ok"
  assert not first_path.exists()
  new_path = root / result["path"]
  assert new_path.is_file()
  updated = json.loads(new_path.read_text(encoding="utf-8"))
  assert updated["state"] == "in_progress"
  assert updated["issue_version"] == original["issue_version"] + 1
  assert updated["created_at"] == original["created_at"]


def test_second_active_issue_rolls_back(tmp_path):
  from tools.development import issue_state_transition as transition

  root = _fixture_root(tmp_path)
  first_id, _first_path = _register_issue(root, number="001")
  second_id, second_path = _register_issue(root, number="002")
  first_code, _ = transition.transition(
    first_id, "in_progress", project_root=root
  )
  assert first_code == 0
  before_bytes = second_path.read_bytes()

  exit_code, result = transition.transition(
    second_id, "in_progress", project_root=root
  )

  assert exit_code != 0
  assert result["status"] == "repository_invalid"
  assert second_path.read_bytes() == before_bytes
  versions = sorted(
    (root / ISSUE_DIRECTORY).glob(f"{second_id.lower()}--v*.json")
  )
  assert [path.name for path in versions] == [second_path.name]


def test_unknown_state_touches_nothing(tmp_path):
  from tools.development import issue_state_transition as transition

  root = _fixture_root(tmp_path)
  issue_id, first_path = _register_issue(root)
  before_bytes = first_path.read_bytes()

  exit_code, result = transition.transition(
    issue_id, "bogus_state", project_root=root
  )

  assert exit_code != 0
  assert result["status"] == "state_unknown"
  assert first_path.read_bytes() == before_bytes


def test_module_entry_resolves_issue(tmp_path):
  root = _fixture_root(tmp_path)
  issue_id, _first_path = _register_issue(root)

  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.issue_state_transition",
      "--issue-id",
      issue_id,
      "--to-state",
      "resolved",
      "--project-root",
      str(root),
    ],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True,
    timeout=60,
  )

  assert completed.returncode == 0
  payload = json.loads(completed.stdout.strip().splitlines()[-1])
  assert payload["status"] == "ok"
  assert payload["to_state"] == "resolved"
