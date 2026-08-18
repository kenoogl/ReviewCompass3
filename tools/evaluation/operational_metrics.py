"""運用計測の集計装置（評価データ取得計画 順序5・従軸）。

launch計測メタ（launch.json）と判断record群から、起動所要時間の分布と
承認点の日付分布を機械集計し、一行JSONで返す。手集計・転記をしない。
未知形式のfileは数えずskippedへ計上する（fail-closed）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

from tools.common import roots


def _stats(values):
  if not values:
    return {"count": 0}
  return {
    "count": len(values),
    "min": round(min(values), 4),
    "median": round(statistics.median(values), 4),
    "mean": round(statistics.mean(values), 4),
    "max": round(max(values), 4),
    "total": round(sum(values), 4),
  }


def collect_launch_metrics(launch_root):
  instrumented = []
  legacy_count = 0
  skipped_count = 0
  for directory in sorted(
    path for path in Path(launch_root).iterdir() if path.is_dir()
  ):
    launch = directory / "launch.json"
    if not launch.is_file():
      skipped_count += 1
      continue
    try:
      document = json.loads(launch.read_text(encoding="utf-8"))
    except (OSError, ValueError):
      skipped_count += 1
      continue
    if not isinstance(document, dict):
      skipped_count += 1
      continue
    if "elapsed_seconds" not in document:
      legacy_count += 1
      continue
    if not isinstance(document["elapsed_seconds"], (int, float)):
      skipped_count += 1
      continue
    instrumented.append(document)
  prompt_bytes = [
    document["prompt_bytes"]
    for document in instrumented
    if isinstance(document.get("prompt_bytes"), int)
  ]
  return {
    "instrumented_count": len(instrumented),
    "legacy_count": legacy_count,
    "skipped_count": skipped_count,
    "elapsed_seconds": _stats(
      [document["elapsed_seconds"] for document in instrumented]
    ),
    "prompt_bytes": _stats(prompt_bytes),
  }


def collect_approval_metrics(records_root):
  record_count = 0
  skipped_count = 0
  by_date = {}
  for path in sorted(Path(records_root).glob("*.md")):
    try:
      text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
      skipped_count += 1
      continue
    if "承認文言" not in text:
      continue
    record_count += 1
    prefix = path.name[:10]
    if (
      len(prefix) == 10
      and prefix[4] == "-"
      and prefix[7] == "-"
      and prefix.replace("-", "").isdigit()
    ):
      key = prefix
    else:
      key = "undated"
    by_date[key] = by_date.get(key, 0) + 1
  return {
    "record_count": record_count,
    "skipped_count": skipped_count,
    "by_date": by_date,
  }


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--launch-root", required=True)
  parser.add_argument("--records-root", default=None)
  arguments = parser.parse_args(
    list(sys.argv[1:] if argv is None else argv)
  )
  launch_root = Path(arguments.launch_root)
  records_root = (
    roots.repo_root() / "records" / "development"
    if arguments.records_root is None
    else Path(arguments.records_root)
  )
  if not launch_root.is_dir() or not records_root.is_dir():
    print(json.dumps(
      {"schema_version": 1, "status": "input_invalid"},
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ))
    return 2
  result = {
    "schema_version": 1,
    "status": "ok",
    "launch": collect_launch_metrics(launch_root),
    "approvals": collect_approval_metrics(records_root),
  }
  print(json.dumps(
    result,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ))
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
