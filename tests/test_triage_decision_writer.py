"""仕分け決定writer（草稿→機械組み立て→検証合格時のみ書き出し）の契約試験。"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_FILES = (
  "config/development-issue-resolution-pilot-v2.json",
  "config/development-issue-resolution-pilot-v3.json",
  "config/development-issue-resolution-pilot-v4.json",
)
DECISION_DIRECTORY = ".reviewcompass/workflow/triage-decisions-v4"


def _fixture_root(tmp_path):
  root = tmp_path / "proj"
  (root / ".reviewcompass/workflow/improvement-candidates").mkdir(parents=True)
  (root / DECISION_DIRECTORY).mkdir(parents=True)
  (root / ".reviewcompass/workflow/issues-v4").mkdir(parents=True)
  (root / "config").mkdir()
  (root / "records" / "development").mkdir(parents=True)
  for name in CONFIG_FILES:
    shutil.copy(PROJECT_ROOT / name, root / name)
  source = root / "records" / "development" / "2026-08-19-obs-v1.md"
  source.write_text("# 観測\n\n本文。\n", encoding="utf-8")
  return root


def _make_candidate(root, number="001"):
  from tools.development import improvement_candidate_writer as writer

  candidate_id = f"IC-RETURN-PATH-FIXTURE-{number}"
  draft = root / f"candidate-draft-{number}.json"
  draft.write_text(
    json.dumps(
      {
        "record_kind": "improvement_candidate",
        "schema_version": 1,
        "candidate_id": candidate_id,
        "candidate_version": 1,
        "source_work": "return-path-fixture",
        "source_identity": {
          "kind": "observation",
          "source_id": f"OBS-RETURN-PATH-FIXTURE-{number}-V1",
          "source_version": 1,
          "path": "records/development/2026-08-19-obs-v1.md",
        },
        "problem": f"fixtureの問題記述{number}。",
        "impact": ["影響の記述。"],
        "scope": ["対象の記述。"],
        "non_scope": ["対象外の記述。"],
        "classification_candidates": ["process_improvement"],
        "route_candidates": ["issue_resolution"],
        "consumer_candidates": ["reviewcompass3-development"],
        "evidence_refs": [
          {"path": "records/development/2026-08-19-obs-v1.md"}
        ],
        "proposed_action": "fixtureの処置案。",
      },
      ensure_ascii=False,
      indent=1,
    )
    + "\n",
    encoding="utf-8",
  )
  exit_code, result = writer.finalize_draft(draft, project_root=root)
  assert exit_code == 0
  return candidate_id, result["path"]


def _decision_draft(root, candidate_id, candidate_path, *, promote, number="001"):
  draft = root / f"decision-draft-{number}.json"
  draft.write_text(
    json.dumps(
      {
        "candidate_id": candidate_id,
        "candidate_record_path": candidate_path,
        "human_fields": {
          "unresolved": True,
          "recurrence": False,
          "impact": "low",
          "priority": "low",
          "promote_to_issue": promote,
        },
        "disposition": "issue_resolution" if promote else "defer",
        "blocking": False,
        "rationale": "fixtureの理由。",
        "next_action": "fixtureの次の一手。",
      },
      ensure_ascii=False,
      indent=1,
    )
    + "\n",
    encoding="utf-8",
  )
  return draft


def test_valid_draft_writes_validated_decision(tmp_path):
  from tools.development import issue_intake_v4 as intake
  from tools.development import triage_decision_writer as writer

  root = _fixture_root(tmp_path)
  candidate_id, candidate_path = _make_candidate(root)
  draft = _decision_draft(root, candidate_id, candidate_path, promote=False)

  exit_code, result = writer.finalize_draft(draft, project_root=root)

  assert exit_code == 0
  assert result["status"] == "ok"
  target = root / result["path"]
  assert target.is_file()
  document = json.loads(target.read_text(encoding="utf-8"))
  assert document["decided_at"]
  assert document["disposition"] == "defer"
  config = json.loads(
    (root / CONFIG_FILES[2]).read_text(encoding="utf-8")
  )
  effective = intake.validate_triage_decision_repository(
    project_root=root, config=config
  )
  assert effective[candidate_id]["decision_id"] == document["decision_id"]


def test_invalid_disposition_writes_nothing(tmp_path):
  from tools.development import triage_decision_writer as writer

  root = _fixture_root(tmp_path)
  candidate_id, candidate_path = _make_candidate(root)
  draft = _decision_draft(root, candidate_id, candidate_path, promote=False)
  document = json.loads(draft.read_text(encoding="utf-8"))
  document["disposition"] = "bogus_disposition"
  draft.write_text(
    json.dumps(document, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
  )

  exit_code, result = writer.finalize_draft(draft, project_root=root)

  assert exit_code != 0
  assert result["status"] in ("build_failed", "validation_failed")
  assert list((root / DECISION_DIRECTORY).glob("*.json")) == []


def test_existing_decision_is_refused(tmp_path):
  from tools.development import triage_decision_writer as writer

  root = _fixture_root(tmp_path)
  candidate_id, candidate_path = _make_candidate(root)
  draft = _decision_draft(root, candidate_id, candidate_path, promote=False)

  first_code, _first = writer.finalize_draft(draft, project_root=root)
  second_code, second = writer.finalize_draft(draft, project_root=root)

  assert first_code == 0
  assert second_code != 0
  assert second["status"] == "already_exists"


def test_module_entry_runs(tmp_path):
  root = _fixture_root(tmp_path)
  candidate_id, candidate_path = _make_candidate(root)
  draft = _decision_draft(root, candidate_id, candidate_path, promote=False)

  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.triage_decision_writer",
      "--draft",
      str(draft),
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
