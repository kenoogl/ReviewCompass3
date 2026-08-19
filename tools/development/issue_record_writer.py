"""issue登録writer（昇格決定→issue record・検証合格時のみ書き出し）。

検証済みのHuman仕分け決定（N1形式・Issue昇格承認つき）からV4 issue recordを
機械組み立てし、単体検証→new-only書き出し→repository検証の順で確定する。
repository検証に不合格なら書いたfileを除去して原状へ戻す（fail-closed）。

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


def _print_json(value):
  print(json.dumps(
    value,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))


def register_from_decision(
  decision_path, *, project_root=None, config_path=DEFAULT_CONFIG, problem=None
):
  root = Path.cwd() if project_root is None else Path(project_root)
  try:
    config = json.loads((root / config_path).read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "config_invalid", "reason": str(error)}

  decision_file = Path(decision_path)
  if not decision_file.is_absolute():
    decision_file = root / decision_file
  try:
    decision = json.loads(decision_file.read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "decision_unreadable", "reason": str(error)}
  try:
    decision_relative = decision_file.resolve().relative_to(
      root.resolve()
    ).as_posix()
  except ValueError:
    return 1, {"status": "decision_unreadable", "reason": "decision outside root"}

  try:
    intake.validate_human_triage_decision(
      decision,
      path=decision_relative,
      project_root=root,
      config=config,
    )
  except intake.IntakeError as error:
    return 1, {"status": "validation_failed", "reason": str(error)}

  candidate_ref = decision.get("candidate_ref", {})
  candidate_relative = candidate_ref.get("record_path")
  if not isinstance(candidate_relative, str):
    return 1, {
      "status": "unsupported_decision_form",
      "reason": "bundle形式の決定は対象外（N1のみ）",
    }
  try:
    candidate = json.loads(
      (root / candidate_relative).read_text(encoding="utf-8")
    )
  except (OSError, ValueError) as error:
    return 1, {"status": "candidate_unreadable", "reason": str(error)}

  try:
    document = intake.build_v4_issue_record(
      candidate=candidate,
      decision=decision,
      project_root=root,
      config=config,
      created_at=datetime.now().astimezone().isoformat(timespec="seconds"),
      problem=problem,
    )
  except intake.IntakeError as error:
    return 1, {"status": "build_failed", "reason": str(error)}

  relative = intake.v4_issue_path(document, config=config)
  target = root / relative
  if target.exists():
    return 1, {"status": "already_exists", "path": relative}

  try:
    intake.validate_v4_issue_record(
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
  try:
    intake.validate_v4_issue_repository(project_root=root, config=config)
  except intake.IntakeError as error:
    target.unlink()
    return 1, {"status": "repository_invalid", "reason": str(error)}
  return 0, {
    "status": "ok",
    "path": relative,
    "issue_id": document["issue_id"],
    "content_digest": document["content_digest"],
  }


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--decision", required=True)
  parser.add_argument("--project-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  exit_code, result = register_from_decision(
    arguments.decision,
    project_root=arguments.project_root,
  )
  _print_json(result)
  return exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
