"""改善候補writer（草稿→機械埋め込み→検証合格時のみ書き出し）の契約試験。"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_DIRECTORY = ".reviewcompass/workflow/improvement-candidates"
CONFIG_RELATIVE = "config/development-issue-resolution-pilot-v3.json"


def _fixture_root(tmp_path):
  root = tmp_path / "proj"
  (root / CANDIDATE_DIRECTORY).mkdir(parents=True)
  (root / "config").mkdir()
  (root / "records" / "development").mkdir(parents=True)
  shutil.copy(PROJECT_ROOT / CONFIG_RELATIVE, root / CONFIG_RELATIVE)
  source = root / "records" / "development" / "2026-08-19-obs-v1.md"
  source.write_text("# 観測\n\n本文。\n", encoding="utf-8")
  return root


def _draft_document():
  return {
    "record_kind": "improvement_candidate",
    "schema_version": 1,
    "candidate_id": "IC-WRITER-FIXTURE-PROBE-001",
    "candidate_version": 1,
    "source_work": "writer-fixture",
    "source_identity": {
      "kind": "observation",
      "source_id": "OBS-WRITER-FIXTURE-2026-08-19-V1",
      "source_version": 1,
      "path": "records/development/2026-08-19-obs-v1.md",
    },
    "problem": "fixtureの問題記述。",
    "impact": ["影響の記述。"],
    "scope": ["対象の記述。"],
    "non_scope": ["対象外の記述。"],
    "classification_candidates": ["process_improvement"],
    "route_candidates": ["checkpoint"],
    "consumer_candidates": ["reviewcompass3-development"],
    "evidence_refs": [
      {"path": "records/development/2026-08-19-obs-v1.md"}
    ],
    "proposed_action": "fixtureの処置案。",
  }


def _write_draft(root, document):
  draft = root / "draft.json"
  draft.write_text(
    json.dumps(document, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
  )
  return draft


def _expected_path(root):
  return (
    root
    / CANDIDATE_DIRECTORY
    / "ic-writer-fixture-probe-001--v1.json"
  )


def test_valid_draft_is_finalized_and_validator_passing(tmp_path):
  from tools.development import improvement_candidate_writer as writer
  from tools.development import issue_resolution_pilot as pilot

  root = _fixture_root(tmp_path)
  draft = _write_draft(root, _draft_document())

  exit_code, result = writer.finalize_draft(draft, project_root=root)

  assert exit_code == 0
  assert result["status"] == "ok"
  target = _expected_path(root)
  assert target.is_file()
  written = json.loads(target.read_text(encoding="utf-8"))
  assert written["source_identity"]["sha256"]
  assert written["evidence_refs"][0]["sha256"]
  assert written["created_at"]
  assert written["content_digest"] == result["content_digest"]
  config = pilot.load_config(root / CONFIG_RELATIVE)
  pilot.validate_record_file(target, project_root=root, config=config)


def test_invalid_vocabulary_writes_nothing(tmp_path):
  from tools.development import improvement_candidate_writer as writer

  root = _fixture_root(tmp_path)
  document = _draft_document()
  document["classification_candidates"] = ["bogus_vocabulary"]
  draft = _write_draft(root, document)

  exit_code, result = writer.finalize_draft(draft, project_root=root)

  assert exit_code != 0
  assert result["status"] == "validation_failed"
  assert not _expected_path(root).exists()


def test_existing_output_is_refused(tmp_path):
  from tools.development import improvement_candidate_writer as writer

  root = _fixture_root(tmp_path)
  draft = _write_draft(root, _draft_document())
  target = _expected_path(root)
  target.write_text("{}\n", encoding="utf-8")

  exit_code, result = writer.finalize_draft(draft, project_root=root)

  assert exit_code != 0
  assert result["status"] == "already_exists"
  assert target.read_text(encoding="utf-8") == "{}\n"


def test_module_entry_runs(tmp_path):
  root = _fixture_root(tmp_path)
  draft = _write_draft(root, _draft_document())

  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.improvement_candidate_writer",
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
