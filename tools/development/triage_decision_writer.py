"""仕分け決定recordのwriter（草稿→機械組み立て→検証合格時のみ書き出し）。

草稿は意味欄（candidate参照・human_fields・disposition・blocking・rationale・
next_action）だけを持てばよい。時刻の機械記録・指紋束縛・置き場解決・検証は
機械処理で行い、単体検証に合格した場合だけ台帳へ書き出す（new-only・
fail-closed）。裁定の中身はHumanの承認文言に基づく（本toolは書記に徹する）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from tools.development import issue_intake_v4 as intake


DEFAULT_CONFIG = "config/development-issue-resolution-pilot-v4.json"

_REQUIRED_DRAFT_FIELDS = (
  "candidate_id",
  "candidate_record_path",
  "human_fields",
  "disposition",
  "blocking",
  "rationale",
  "next_action",
)


def _print_json(value):
  print(json.dumps(
    value,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))


def finalize_draft(draft_path, *, project_root=None, config_path=DEFAULT_CONFIG):
  root = Path.cwd() if project_root is None else Path(project_root)
  try:
    draft = json.loads(Path(draft_path).read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "draft_unreadable", "reason": str(error)}
  if not isinstance(draft, dict):
    return 1, {"status": "draft_unreadable", "reason": "draft must be a mapping"}
  missing = sorted(
    field for field in _REQUIRED_DRAFT_FIELDS if field not in draft
  )
  if missing:
    return 1, {"status": "draft_incomplete", "missing": missing}

  try:
    config = json.loads((root / config_path).read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "config_invalid", "reason": str(error)}

  decided_at = draft.get("decided_at") or (
    datetime.now().astimezone().isoformat(timespec="seconds")
  )
  try:
    document = intake.build_human_triage_decision(
      project_root=root,
      candidate_record_path=draft["candidate_record_path"],
      candidate_id=draft["candidate_id"],
      decided_at=decided_at,
      human_fields=draft["human_fields"],
      disposition=draft["disposition"],
      blocking=draft["blocking"],
      rationale=draft["rationale"],
      next_action=draft["next_action"],
      config=config,
      decision_version=draft.get("decision_version", 1),
      supersedes=draft.get("supersedes"),
      issue_id=draft.get("issue_id"),
      decision_suffix=draft.get("decision_suffix"),
    )
  except intake.IntakeError as error:
    return 1, {"status": "build_failed", "reason": str(error)}

  relative = intake.human_triage_decision_path(document, config=config)
  target = root / relative
  if target.exists():
    return 1, {"status": "already_exists", "path": relative}

  try:
    intake.validate_human_triage_decision(
      document,
      path=relative,
      project_root=root,
      config=config,
    )
  except intake.IntakeError as error:
    return 1, {"status": "validation_failed", "reason": str(error)}

  target.parent.mkdir(parents=True, exist_ok=True)
  with open(target, "w", encoding="utf-8") as stream:
    json.dump(document, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
  return 0, {
    "status": "ok",
    "path": relative,
    "decision_id": document["decision_id"],
    "content_digest": document["content_digest"],
  }


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--draft", required=True)
  parser.add_argument("--project-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  exit_code, result = finalize_draft(
    arguments.draft,
    project_root=arguments.project_root,
  )
  _print_json(result)
  return exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
