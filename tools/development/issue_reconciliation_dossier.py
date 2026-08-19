"""issue実態調書（dossier）の機械生成。

issueごとに、台帳欄（state・版・created_at）・登録後の活動（records／git履歴の
言及計数）・problem文中の参照pathの生存・TODO active欄の拘束flagを機械収集し、
一行JSONで返す。判断欄は持たない——充足判断・残余riskの受容・裁定はHumanに、
意味所見はLLMに残す。出力は決定的（時刻・乱数を含まない）。読み取り専用。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from tools.development import issue_intake_v4 as intake


DEFAULT_CONFIG = "config/development-issue-resolution-pilot-v4.json"

_PATH_TOKEN = re.compile(
  r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:py|md|json|yaml|toml)"
)
_MISSING_LIMIT = 10
_TODO_LINE_LIMIT = 200


def _print_json(value):
  print(json.dumps(
    value,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))


def _records_mentions(records_dir, issue_id, candidate_id):
  names = []
  if not records_dir.is_dir():
    return names
  for path in sorted(records_dir.glob("*.md")):
    try:
      text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
      continue
    if issue_id in text or candidate_id in text:
      names.append(path.name)
  return names


def _git_mentions(root, issue_id, candidate_id):
  completed = subprocess.run(
    ["git", "log", "--oneline", "--grep", issue_id, "--grep", candidate_id],
    cwd=root,
    capture_output=True,
    text=True,
  )
  if completed.returncode != 0:
    return None
  return len([
    line for line in completed.stdout.splitlines() if line.strip()
  ])


def build_dossier(*, project_root=None, config_path=DEFAULT_CONFIG, issue_id=None):
  root = Path.cwd() if project_root is None else Path(project_root)
  try:
    config = json.loads((root / config_path).read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    return 1, {"status": "config_invalid", "reason": str(error)}
  try:
    issues = intake.load_v4_issues(project_root=root, config=config)
  except intake.IntakeError as error:
    return 1, {"status": "issue_repository_invalid", "reason": str(error)}
  if issue_id is not None:
    issues = [
      issue for issue in issues if issue["issue_id"] == issue_id
    ]
    if not issues:
      return 1, {"status": "issue_not_found", "issue_id": issue_id}

  todo_path = root / "TODO_NEXT_SESSION.md"
  todo_text = ""
  if todo_path.is_file():
    todo_text = todo_path.read_text(encoding="utf-8")
  records_dir = root / "records" / "development"

  entries = []
  for issue in issues:
    identifier = issue["issue_id"]
    candidate_id = issue["candidate_ref"]["candidate_id"]
    mention_names = _records_mentions(records_dir, identifier, candidate_id)
    tokens = sorted({
      token
      for token in _PATH_TOKEN.findall(issue["problem"])
      if "/" in token
    })
    missing = [token for token in tokens if not (root / token).exists()]
    todo_line = None
    if todo_text and identifier in todo_text:
      for line in todo_text.splitlines():
        if identifier in line:
          todo_line = line[:_TODO_LINE_LIMIT]
          break
    entries.append({
      "issue_id": identifier,
      "candidate_id": candidate_id,
      "state": issue["state"],
      "issue_version": issue["issue_version"],
      "created_at": issue["created_at"],
      "activity": {
        "records_mention_count": len(mention_names),
        "records_latest": mention_names[-1] if mention_names else None,
        "git_mention_count": _git_mentions(root, identifier, candidate_id),
      },
      "referenced_paths": {
        "total": len(tokens),
        "missing": missing[:_MISSING_LIMIT],
      },
      "todo_active": todo_line is not None,
      "todo_line": todo_line,
    })
  return 0, {
    "status": "ok",
    "issue_total": len(entries),
    "issues": entries,
  }


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--issue-id", default=None)
  parser.add_argument("--project-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  exit_code, result = build_dossier(
    project_root=arguments.project_root,
    issue_id=arguments.issue_id,
  )
  _print_json(result)
  return exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
