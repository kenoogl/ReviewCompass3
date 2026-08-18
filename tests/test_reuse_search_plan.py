"""計画JSON writer（finalize・verify）の固定。手書きdigest工程の排除。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_PLAN = (
  PROJECT_ROOT
  / "records/development/2026-08-18-measurement-block-plan-v1.json"
)


def _draft_document():
  document = json.loads(COMMITTED_PLAN.read_text(encoding="utf-8"))
  document.pop("content_digest")
  document["plan_id"] = "FCRS-TEST-DRAFT-V1"
  document["searches"][0]["attestation_path"] = (
    "records/development/test-plan-writer-absent-attestation.json"
  )
  return document


def _write_draft(tmp_path, document):
  path = tmp_path / "draft-plan.json"
  path.write_text(
    json.dumps(document, ensure_ascii=False, indent=1, sort_keys=True),
    encoding="utf-8",
  )
  return path


def test_finalize_embeds_digest_and_rewrites(tmp_path, capsys):
  from tools.common import digests
  from tools.development import reuse_search_plan

  draft = _write_draft(tmp_path, _draft_document())
  exit_code = reuse_search_plan.run((
    "finalize", "--plan", str(draft),
    "--project-root", str(PROJECT_ROOT),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 0
  assert summary["status"] == "ok"
  finalized = json.loads(draft.read_text(encoding="utf-8"))
  assert finalized["content_digest"] == digests.canonical_content_digest(
    finalized
  )
  assert summary["content_digest"] == finalized["content_digest"]


def test_finalize_refuses_already_finalized(tmp_path, capsys):
  from tools.development import reuse_search_plan

  document = _draft_document()
  document["content_digest"] = "0" * 64
  draft = _write_draft(tmp_path, document)
  before = draft.read_text(encoding="utf-8")
  exit_code = reuse_search_plan.run((
    "finalize", "--plan", str(draft),
    "--project-root", str(PROJECT_ROOT),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert summary["reason"] == "already_finalized"
  assert draft.read_text(encoding="utf-8") == before


def test_finalize_rejects_invalid_plan_without_writing(tmp_path, capsys):
  from tools.development import reuse_search_plan

  document = _draft_document()
  document["record_kind"] = "wrong_kind"
  draft = _write_draft(tmp_path, document)
  before = draft.read_text(encoding="utf-8")
  exit_code = reuse_search_plan.run((
    "finalize", "--plan", str(draft),
    "--project-root", str(PROJECT_ROOT),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert summary["status"] == "stopped"
  assert draft.read_text(encoding="utf-8") == before


def test_verify_accepts_committed_plan_with_existing_attestation(capsys):
  from tools.development import reuse_search_plan

  exit_code = reuse_search_plan.run((
    "verify", "--plan", str(COMMITTED_PLAN),
    "--project-root", str(PROJECT_ROOT),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 0
  assert summary["status"] == "ok"


def test_verify_detects_tampered_digest(tmp_path, capsys):
  from tools.development import reuse_search_plan

  document = json.loads(COMMITTED_PLAN.read_text(encoding="utf-8"))
  document["content_digest"] = "0" * 64
  tampered = _write_draft(tmp_path, document)
  exit_code = reuse_search_plan.run((
    "verify", "--plan", str(tampered),
    "--project-root", str(PROJECT_ROOT),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert summary["status"] == "stopped"


def test_module_entry_runs(tmp_path):
  draft = _write_draft(tmp_path, _draft_document())
  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.reuse_search_plan",
      "finalize",
      "--plan",
      str(draft),
      "--project-root",
      str(PROJECT_ROOT),
    ],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True,
    timeout=60,
  )
  assert completed.returncode == 0
  assert json.loads(completed.stdout)["status"] == "ok"
