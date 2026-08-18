"""セッションログ記録の一括実行wrapper（record-run）。

3系統のcollect-eventualを単独プロセスで順次実行して要約を返す。
進行中セッション（実行中に変化したfile・実行開始直前の活動窓内に更新のあった
file。現セッションを常に含む）は既定で要約から分離し、件数と注記だけを出す。
要約に絶対path・本文を含めない。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from tools.common import roots


PROJECT_ROOT = roots.repo_root()

DEFAULT_SYSTEMS = (
  (
    "claude",
    "/Users/keno/.claude/projects",
    "reviewcompass3-historical-claude-capture-v1",
  ),
  (
    "codex現行",
    "/Users/keno/.codex/sessions",
    "reviewcompass3-historical-codex-capture-v1",
  ),
  (
    "codex保管",
    "/Users/keno/.codex/archived_sessions",
    "reviewcompass3-historical-codex-capture-v1",
  ),
)

DEFAULT_PRIVATE_ROOT = (
  "/Users/keno/.reviewcompass3/projects/reviewcompass3"
  "/development/sensitive/eventual-preservation"
)

RECENT_ACTIVITY_WINDOW_SECONDS = 600

_NOTE_EXCLUDED = (
  "進行中のため対象外（保全は実行時点まで完了。以後の内容は次回実行で追記保全）"
)
_NOTE_INCLUDED = (
  "指定により進行中を含める（保全は実行時点まで完了。以後の内容は次回実行で追記保全）"
)


def observe_sources(source_root):
  root = Path(source_root)
  if not root.is_dir():
    return {}
  observed = {}
  for path in root.rglob("*.jsonl"):
    if not path.is_file():
      continue
    stat_result = path.stat()
    observed[path.relative_to(root).as_posix()] = (
      stat_result.st_size,
      stat_result.st_mtime_ns,
    )
  return observed


def partition_in_progress(before, after, *, started_at_ns, window_ns):
  threshold = started_at_ns - window_ns
  in_progress = set()
  for relative_path, signature in after.items():
    if before.get(relative_path) != signature:
      in_progress.add(relative_path)
    elif signature[1] >= threshold:
      in_progress.add(relative_path)
  return frozenset(in_progress)


def _default_runner(argv):
  completed = subprocess.run(
    [sys.executable, "-m", "tools.session_logs.entry", *argv],
    capture_output=True,
    text=True,
    cwd=str(PROJECT_ROOT),
  )
  return completed.returncode, completed.stdout


def _parse_last_json_line(text):
  lines = text.strip().splitlines()
  if not lines:
    return None
  try:
    payload = json.loads(lines[-1])
  except ValueError:
    return None
  if not isinstance(payload, dict):
    return None
  return payload


def collect_run(
  *,
  systems,
  private_root,
  repository_root,
  include_in_progress=False,
  window_seconds=RECENT_ACTIVITY_WINDOW_SECONDS,
  runner=None,
):
  active_runner = _default_runner if runner is None else runner
  window_ns = int(window_seconds) * 10**9
  system_reports = []
  in_progress_files = []
  in_progress_total = 0
  overall_ok = True
  for label, source_root, tool_version in systems:
    started_at_ns = time.time_ns()
    before = observe_sources(source_root)
    exit_code, stdout_text = active_runner((
      "collect-eventual",
      "--source-root",
      str(source_root),
      "--private-root",
      str(private_root),
      "--repository-root",
      str(repository_root),
      "--tool-version",
      tool_version,
    ))
    after = observe_sources(source_root)
    in_progress = partition_in_progress(
      before,
      after,
      started_at_ns=started_at_ns,
      window_ns=window_ns,
    )
    payload = _parse_last_json_line(stdout_text)
    if payload is None or not isinstance(payload.get("status"), str):
      status = "runner_error"
      counts = None
    else:
      status = payload["status"]
      counts = payload.get("counts")
    if status not in ("ok", "partial"):
      overall_ok = False
    system_reports.append({
      "label": label,
      "exit_code": exit_code,
      "status": status,
      "counts": counts,
      "in_progress_count": len(in_progress),
    })
    in_progress_total += len(in_progress)
    if include_in_progress:
      in_progress_files.extend(sorted(in_progress))
  return {
    "overall_ok": overall_ok,
    "systems": system_reports,
    "in_progress": {
      "total": in_progress_total,
      "files": in_progress_files,
      "note": _NOTE_INCLUDED if include_in_progress else _NOTE_EXCLUDED,
    },
  }


def _load_systems(systems_file):
  if systems_file is None:
    return DEFAULT_SYSTEMS
  loaded = json.loads(Path(systems_file).read_text(encoding="utf-8"))
  return tuple(
    (str(label), str(source_root), str(tool_version))
    for label, source_root, tool_version in loaded
  )


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--systems-file")
  parser.add_argument("--private-root", default=DEFAULT_PRIVATE_ROOT)
  parser.add_argument("--repository-root", default=str(PROJECT_ROOT))
  parser.add_argument("--include-in-progress", action="store_true")
  parser.add_argument(
    "--activity-window-seconds",
    type=int,
    default=RECENT_ACTIVITY_WINDOW_SECONDS,
  )
  args = parser.parse_args(argv)

  summary = collect_run(
    systems=_load_systems(args.systems_file),
    private_root=Path(args.private_root),
    repository_root=Path(args.repository_root),
    include_in_progress=args.include_in_progress,
    window_seconds=args.activity_window_seconds,
  )
  print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
  return 0 if summary["overall_ok"] else 5


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
