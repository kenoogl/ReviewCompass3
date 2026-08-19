"""workflow台帳の一括検証入口（todo_handoff型の単一コマンド）。

候補置き場の全JSONを保護試験N7と同型の3分岐（validator合格／歴史allowlist／
V4仕分け決定の指紋束縛）で勘定し、V4仕分け決定台帳の全件検証を実行する。
不充足はfindingsへ列挙し、status=failedとexit非0で申告する（fail-closed）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

from tools.development import issue_intake_v4 as intake
from tools.development import issue_resolution_pilot as pilot


CANDIDATE_DIRECTORY = ".reviewcompass/workflow/improvement-candidates"
ALLOWLIST_NAME = "historical-allowlist-v1.json"
LEGACY_CONFIG_FILES = (
  "config/development-issue-resolution-pilot-v2.json",
  "config/development-issue-resolution-pilot-v3.json",
)
V4_CONFIG_FILE = "config/development-issue-resolution-pilot-v4.json"


def _print_json(value):
  print(json.dumps(
    value,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))


def _validator_accepts(path, *, project_root, configs):
  for config in configs:
    try:
      pilot.validate_record_file(
        path, project_root=project_root, config=config
      )
      return True
    except pilot.PilotValidationError:
      continue
  return False


def verify(project_root=None):
  root = Path.cwd() if project_root is None else Path(project_root)
  findings = []

  configs = []
  for name in LEGACY_CONFIG_FILES:
    candidate = root / name
    if candidate.is_file():
      configs.append(pilot.load_config(candidate))
  if not configs:
    findings.append({"kind": "legacy_config_missing", "path": LEGACY_CONFIG_FILES[-1]})

  effective = {}
  v4_config_path = root / V4_CONFIG_FILE
  if v4_config_path.is_file():
    v4_config = json.loads(v4_config_path.read_text(encoding="utf-8"))
    try:
      effective = intake.validate_triage_decision_repository(
        project_root=root, config=v4_config
      )
    except (intake.IntakeError, OSError, ValueError) as error:
      findings.append({
        "kind": "triage_decision_repository_invalid",
        "detail": str(error),
      })
  else:
    findings.append({"kind": "v4_config_missing", "path": V4_CONFIG_FILE})

  allowlist_names = set()
  directory = root / CANDIDATE_DIRECTORY
  allowlist_file = directory / ALLOWLIST_NAME
  if allowlist_file.is_file():
    allowlist = json.loads(allowlist_file.read_text(encoding="utf-8"))
    allowlist_names = {
      Path(entry["path"]).name for entry in allowlist.get("entries", [])
    }

  candidate_total = 0
  accounted = {"validator": 0, "allowlist": 0, "decision": 0}
  candidate_paths = (
    sorted(directory.glob("*.json")) if directory.is_dir() else []
  )
  for path in candidate_paths:
    if path.name == ALLOWLIST_NAME:
      continue
    candidate_total += 1
    if _validator_accepts(path, project_root=root, configs=configs):
      accounted["validator"] += 1
      continue
    if path.name in allowlist_names:
      accounted["allowlist"] += 1
      continue
    try:
      record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
      record = {}
    decision = (
      effective.get(record.get("candidate_id"))
      if isinstance(record, dict)
      else None
    )
    if decision is not None:
      reference = decision.get("candidate_ref", {})
      digest = hashlib.sha256(path.read_bytes()).hexdigest()
      if (
        reference.get("record_sha256") == digest
        and reference.get("candidate_content_digest")
        == record.get("content_digest")
      ):
        accounted["decision"] += 1
        continue
      findings.append({
        "kind": "decision_fingerprint_mismatch",
        "path": path.name,
      })
      continue
    findings.append({"kind": "candidate_unaccounted", "path": path.name})

  issue_total = 0
  issue_states = {}
  if v4_config_path.is_file():
    try:
      issues = intake.load_v4_issues(project_root=root, config=v4_config)
      intake.validate_v4_issue_repository(project_root=root, config=v4_config)
      issue_total = len(issues)
      for issue in issues:
        state = issue["state"]
        issue_states[state] = issue_states.get(state, 0) + 1
    except (intake.IntakeError, OSError, ValueError) as error:
      findings.append({
        "kind": "issue_repository_invalid",
        "detail": str(error),
      })

  return {
    "candidate_total": candidate_total,
    "accounted": accounted,
    "decision_total": len(effective),
    "issue_total": issue_total,
    "issue_states": issue_states,
    "findings": findings,
    "status": "passed" if not findings else "failed",
  }


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--project-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  summary = verify(project_root=arguments.project_root)
  _print_json(summary)
  return 0 if summary["status"] == "passed" else 1


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
