"""issue登録writer（昇格決定→issue record・検証合格時のみ書き出し）の契約試験。"""

import json
from pathlib import Path

from tests.test_triage_decision_writer import (
  _decision_draft,
  _fixture_root,
  _make_candidate,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ISSUE_DIRECTORY = ".reviewcompass/workflow/issues-v4"


def _make_promotion_decision(root, number="001"):
  from tools.development import triage_decision_writer as writer

  candidate_id, candidate_path = _make_candidate(root, number=number)
  draft = _decision_draft(
    root, candidate_id, candidate_path, promote=True, number=number
  )
  exit_code, result = writer.finalize_draft(draft, project_root=root)
  assert exit_code == 0
  return candidate_id, root / result["path"]


def test_promotion_decision_registers_issue(tmp_path):
  from tools.development import issue_intake_v4 as intake
  from tools.development import issue_record_writer as writer

  root = _fixture_root(tmp_path)
  candidate_id, decision_path = _make_promotion_decision(root)

  exit_code, result = writer.register_from_decision(
    decision_path, project_root=root
  )

  assert exit_code == 0
  assert result["status"] == "ok"
  target = root / result["path"]
  assert target.is_file()
  issue = json.loads(target.read_text(encoding="utf-8"))
  assert issue["state"] == "registered"
  assert issue["issue_id"] == f"ISSUE-{candidate_id}"
  config = json.loads(
    (root / "config/development-issue-resolution-pilot-v4.json").read_text(
      encoding="utf-8"
    )
  )
  effective = intake.validate_v4_issue_repository(
    project_root=root, config=config
  )
  assert candidate_id in effective


def test_non_promotion_decision_is_rejected(tmp_path):
  from tools.development import issue_record_writer as writer
  from tools.development import triage_decision_writer as decision_writer

  root = _fixture_root(tmp_path)
  candidate_id, candidate_path = _make_candidate(root)
  draft = _decision_draft(root, candidate_id, candidate_path, promote=False)
  exit_code, result = decision_writer.finalize_draft(draft, project_root=root)
  assert exit_code == 0

  issue_code, issue_result = writer.register_from_decision(
    root / result["path"], project_root=root
  )

  assert issue_code != 0
  assert issue_result["status"] in ("build_failed", "validation_failed")
  assert list((root / ISSUE_DIRECTORY).glob("*.json")) == []


def test_existing_issue_is_refused(tmp_path):
  from tools.development import issue_record_writer as writer

  root = _fixture_root(tmp_path)
  _candidate_id, decision_path = _make_promotion_decision(root)

  first_code, _first = writer.register_from_decision(
    decision_path, project_root=root
  )
  second_code, second = writer.register_from_decision(
    decision_path, project_root=root
  )

  assert first_code == 0
  assert second_code != 0
  assert second["status"] == "already_exists"
