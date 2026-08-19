"""issue状態遷移（版遷移・置換・rollback）の機械処理。

現行のissue recordを読み、stateを更新して版を1進め（`created_at`は初版の値を
保存）、正準digestを再計算する。新版の単体検証→新file書き出し→旧file除去→
repository検証の順で確定し、repository検証に不合格なら旧fileを復元して新file
を除去する（fail-closed）。語彙・active上限1・重複拒否は既存検証が機械強制する。
遷移の意味（判定理由・承認文言）はDecision recordへ残す——本toolは書記に徹する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import sys
from pathlib import Path

from tools.common.digests import canonical_content_digest
from tools.development import issue_intake_v4 as intake


DEFAULT_CONFIG = "config/development-issue-resolution-pilot-v4.json"


def _print_json(value):
  print(json.dumps(
    value,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))


def transition(
  issue_id, to_state, *, project_root=None, config_path=DEFAULT_CONFIG
):
  root = Path.cwd() if project_root is None else Path(project_root)
  try:
    config = json.loads((root / config_path).read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "config_invalid", "reason": str(error)}

  if to_state not in config["issue_states"]:
    return 1, {
      "status": "state_unknown",
      "to_state": to_state,
      "allowed": config["issue_states"],
    }

  directory = root / config["directories"]["issue_record_v2"]
  matches = sorted(directory.glob(f"{issue_id.lower()}--v*.json"))
  if not matches:
    return 1, {"status": "issue_not_found", "issue_id": issue_id}
  if len(matches) > 1:
    return 1, {
      "status": "ledger_inconsistent",
      "reason": "同一issueの版fileが複数存在する",
    }
  current_path = matches[0]
  original_bytes = current_path.read_bytes()
  try:
    record = json.loads(original_bytes.decode("utf-8"))
  except ValueError as error:
    return 1, {"status": "issue_unreadable", "reason": str(error)}
  if record.get("issue_id") != issue_id:
    return 1, {"status": "issue_unreadable", "reason": "issue_id mismatch"}
  if record.get("state") == to_state:
    return 1, {"status": "already_in_state", "state": to_state}

  updated = dict(record)
  updated["state"] = to_state
  updated["issue_version"] = record["issue_version"] + 1
  updated.pop("content_digest", None)
  updated["content_digest"] = canonical_content_digest(updated)

  new_relative = intake.v4_issue_path(updated, config=config)
  new_path = root / new_relative
  if new_path.exists():
    return 1, {"status": "already_exists", "path": new_relative}

  try:
    intake.validate_v4_issue_record(
      updated,
      path=new_relative,
      project_root=root,
      config=config,
    )
  except intake.IntakeError as error:
    return 1, {"status": "validation_failed", "reason": str(error)}

  with open(new_path, "w", encoding="utf-8") as stream:
    json.dump(updated, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
  current_path.unlink()
  try:
    intake.validate_v4_issue_repository(project_root=root, config=config)
  except intake.IntakeError as error:
    current_path.write_bytes(original_bytes)
    new_path.unlink()
    return 1, {"status": "repository_invalid", "reason": str(error)}
  return 0, {
    "status": "ok",
    "issue_id": issue_id,
    "from_state": record["state"],
    "to_state": to_state,
    "path": new_relative,
  }


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--issue-id", required=True)
  parser.add_argument("--to-state", required=True)
  parser.add_argument("--project-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  exit_code, result = transition(
    arguments.issue_id,
    arguments.to_state,
    project_root=arguments.project_root,
  )
  _print_json(result)
  return exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
