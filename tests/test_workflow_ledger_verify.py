"""台帳一括検証入口（候補の勘定＋V4決定台帳の全件検証）の契約試験。"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_DIRECTORY = ".reviewcompass/workflow/improvement-candidates"
DECISION_DIRECTORY = ".reviewcompass/workflow/triage-decisions-v4"
CONFIG_FILES = (
  "config/development-issue-resolution-pilot-v2.json",
  "config/development-issue-resolution-pilot-v3.json",
  "config/development-issue-resolution-pilot-v4.json",
)


def _fixture_root(tmp_path):
  root = tmp_path / "proj"
  (root / CANDIDATE_DIRECTORY).mkdir(parents=True)
  (root / DECISION_DIRECTORY).mkdir(parents=True)
  (root / "config").mkdir()
  (root / "records" / "development").mkdir(parents=True)
  for name in CONFIG_FILES:
    shutil.copy(PROJECT_ROOT / name, root / name)
  source = root / "records" / "development" / "2026-08-19-obs-v1.md"
  source.write_text("# 観測\n\n本文。\n", encoding="utf-8")
  return root


def _add_valid_candidate(root):
  from tools.development import improvement_candidate_writer as writer

  draft = root / "draft.json"
  draft.write_text(
    json.dumps(
      {
        "record_kind": "improvement_candidate",
        "schema_version": 1,
        "candidate_id": "IC-VERIFY-FIXTURE-PROBE-001",
        "candidate_version": 1,
        "source_work": "verify-fixture",
        "source_identity": {
          "kind": "observation",
          "source_id": "OBS-VERIFY-FIXTURE-2026-08-19-V1",
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
      },
      ensure_ascii=False,
      indent=1,
    )
    + "\n",
    encoding="utf-8",
  )
  exit_code, _result = writer.finalize_draft(draft, project_root=root)
  assert exit_code == 0


def test_fixture_ledger_passes(tmp_path):
  from tools.development import workflow_ledger_verify as verify

  root = _fixture_root(tmp_path)
  _add_valid_candidate(root)

  summary = verify.verify(project_root=root)

  assert summary["status"] == "passed"
  assert summary["findings"] == []
  assert summary["candidate_total"] == 1
  assert summary["accounted"]["validator"] == 1


def test_broken_candidate_is_listed(tmp_path):
  from tools.development import workflow_ledger_verify as verify

  root = _fixture_root(tmp_path)
  _add_valid_candidate(root)
  broken = root / CANDIDATE_DIRECTORY / "ic-broken-probe-001--v1.json"
  broken.write_text('{"record_kind": "improvement_candidate"}\n', encoding="utf-8")

  summary = verify.verify(project_root=root)

  assert summary["status"] == "failed"
  assert any(
    finding["kind"] == "candidate_unaccounted"
    and finding["path"] == broken.name
    for finding in summary["findings"]
  )


def test_allowlist_branch_accounts_candidate(tmp_path):
  from tools.development import workflow_ledger_verify as verify

  root = _fixture_root(tmp_path)
  _add_valid_candidate(root)
  broken = root / CANDIDATE_DIRECTORY / "ic-broken-probe-001--v1.json"
  broken.write_text('{"record_kind": "improvement_candidate"}\n', encoding="utf-8")
  allowlist = root / CANDIDATE_DIRECTORY / "historical-allowlist-v1.json"
  allowlist.write_text(
    json.dumps(
      {"entries": [{"path": f"{CANDIDATE_DIRECTORY}/{broken.name}", "reason": "歴史record"}]},
      ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
  )

  summary = verify.verify(project_root=root)

  assert summary["status"] == "passed"
  assert summary["accounted"]["allowlist"] == 1


def test_broken_issue_repository_is_listed(tmp_path):
  from tools.development import workflow_ledger_verify as verify

  root = _fixture_root(tmp_path)
  issues = root / ".reviewcompass/workflow/issues-v4"
  issues.mkdir(parents=True)
  (issues / "issue-broken-probe-001--v1.json").write_text(
    '{"record_kind": "issue_record"}\n', encoding="utf-8"
  )

  summary = verify.verify(project_root=root)

  assert summary["status"] == "failed"
  assert any(
    finding["kind"] == "issue_repository_invalid"
    for finding in summary["findings"]
  )


def test_real_repository_counts_issues():
  # 状態の内訳を焼き込まない（状態固定の再発防止。2026-08-19の突合で
  # registered>=8の焼き込みが正当な遷移により破綻した——意図＝「全issueが
  # 勘定に入り内訳が総数と整合する」だけを固定する）。
  from tools.development import workflow_ledger_verify as verify

  summary = verify.verify(project_root=PROJECT_ROOT)

  assert summary["status"] == "passed"
  assert summary["issue_total"] >= 8
  assert sum(summary["issue_states"].values()) == summary["issue_total"]


def test_real_repository_ledger_is_green():
  from tools.development import workflow_ledger_verify as verify

  summary = verify.verify(project_root=PROJECT_ROOT)

  assert summary["status"] == "passed"
  assert summary["findings"] == []
  assert summary["decision_total"] >= 52


def test_module_entry_runs():
  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.development.workflow_ledger_verify",
    ],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True,
    timeout=120,
  )

  assert completed.returncode == 0
  payload = json.loads(completed.stdout.strip().splitlines()[-1])
  assert payload["status"] == "passed"
