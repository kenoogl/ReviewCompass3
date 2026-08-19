"""改善候補recordのwriter（草稿→機械埋め込み→検証合格時のみ書き出し）。

草稿は意味欄だけを持てばよい。出所束縛のSHA-256・時刻・正準content_digest・
置き場（id小文字＋版）の決定はすべて機械処理で行い、v3検証器に合格した
場合だけ台帳へ書き出す（new-only・上書き拒否・fail-closed）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from tools.common.digests import canonical_content_digest, file_sha256
from tools.development import issue_resolution_pilot as pilot


DEFAULT_CONFIG = "config/development-issue-resolution-pilot-v3.json"


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

  document = dict(draft)
  document.pop("content_digest", None)

  source = document.get("source_identity")
  if isinstance(source, dict):
    source = dict(source)
    if "sha256" not in source and isinstance(source.get("path"), str):
      try:
        source["sha256"] = file_sha256(root / source["path"])
      except OSError as error:
        return 1, {"status": "source_unreadable", "reason": str(error)}
    document["source_identity"] = source

  references = document.get("evidence_refs")
  if isinstance(references, list):
    resolved = []
    for reference in references:
      entry = dict(reference) if isinstance(reference, dict) else reference
      if (
        isinstance(entry, dict)
        and "sha256" not in entry
        and isinstance(entry.get("path"), str)
      ):
        try:
          entry["sha256"] = file_sha256(root / entry["path"])
        except OSError as error:
          return 1, {"status": "source_unreadable", "reason": str(error)}
      resolved.append(entry)
    document["evidence_refs"] = resolved

  if not document.get("created_at"):
    document["created_at"] = (
      datetime.now().astimezone().isoformat(timespec="seconds")
    )

  document["content_digest"] = canonical_content_digest(document)

  try:
    config = pilot.load_config(root / config_path)
  except (OSError, pilot.PilotValidationError) as error:
    return 1, {"status": "config_invalid", "reason": str(error)}

  candidate_id = document.get("candidate_id")
  candidate_version = document.get("candidate_version")
  if not isinstance(candidate_id, str) or not isinstance(candidate_version, int):
    return 1, {"status": "validation_failed", "reason": "candidate identity is missing"}
  directory = config["directories"]["improvement_candidate"]
  relative = f"{directory}/{candidate_id.lower()}--v{candidate_version}.json"
  target = root / relative
  if target.exists():
    return 1, {"status": "already_exists", "path": relative}

  try:
    pilot.validate_candidate(
      document,
      path=relative,
      project_root=root,
      config=config,
    )
  except pilot.PilotValidationError as error:
    return 1, {"status": "validation_failed", "reason": str(error)}

  with open(target, "w", encoding="utf-8") as stream:
    json.dump(document, stream, ensure_ascii=False, indent=1)
    stream.write("\n")
  return 0, {
    "status": "ok",
    "path": relative,
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
