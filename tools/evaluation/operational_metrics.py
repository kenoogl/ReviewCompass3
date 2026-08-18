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
import re
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from tools.common import digests
from tools.common import roots


_HEX_ANYWHERE = re.compile(r"[0-9a-f]{64}")
_SHASUM_LINE = re.compile(r"^\s*([0-9a-f]{64})  (\S+)\s*$")
_INLINE_DIGEST = re.compile(r"SHA-256 `([0-9a-f]{64})`")
_BACKTICK_TOKEN = re.compile(r"`([^`]+)`")
_APPROVAL_FIELD_LINE = re.compile(
  r"^[\s>*#0-9.\-]*承認文言", re.MULTILINE
)
_BARE_HEX_CELL = re.compile(r"^`([0-9a-f]{64})`$")


def _table_pair(line):
  # 書式C（表cell）。裸hexだけのcellがちょうど1つ・path様tokenを含むcellが
  # ちょうど1つの行だけを組として採点する（fail-closed）。hexがfile名の一部の
  # tokenはpath側にもhex側にも数えない。
  stripped = line.strip()
  if not stripped.startswith("|"):
    return None, 0
  cells = [cell.strip() for cell in stripped.strip("|").split("|")]
  digest_values = []
  path_values = []
  for cell in cells:
    bare = _BARE_HEX_CELL.match(cell)
    if bare is not None:
      digest_values.append(bare.group(1))
      continue
    for token in _BACKTICK_TOKEN.findall(cell):
      if (
        ("/" in token or "." in token)
        and _HEX_ANYWHERE.fullmatch(token) is None
        and " " not in token
      ):
        path_values.append(token)
        break
  if len(digest_values) == 1 and len(path_values) == 1:
    return (path_values[0], digest_values[0]), 0
  return None, len(digest_values)


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


def _binding_pairs(text):
  # 正準書式だけを組として採点する（fail-closed）。書式A＝shasum行、
  # 書式B＝同一行にbacktick付きpathを持つ inline。組の閉じない出現はunpaired。
  pairs = []
  unpaired_count = 0
  for line in text.splitlines():
    shasum = _SHASUM_LINE.match(line)
    if shasum is not None:
      pairs.append((shasum.group(2), shasum.group(1)))
      continue
    if not _INLINE_DIGEST.search(line):
      table_pair, table_unpaired = _table_pair(line)
      if table_pair is not None:
        pairs.append(table_pair)
      unpaired_count += table_unpaired
      continue
    for match in _INLINE_DIGEST.finditer(line):
      prefix = line[: match.start()]
      candidates = [
        token
        for token in _BACKTICK_TOKEN.findall(prefix)
        if ("/" in token or "." in token)
        and _HEX_ANYWHERE.fullmatch(token) is None
        and " " not in token
      ]
      if candidates:
        pairs.append((candidates[-1], match.group(1)))
      else:
        unpaired_count += 1
  return pairs, unpaired_count


_HISTORY_CAP = 200


def _history_verdict(base, relative, expected):
  # 不一致が「版の前進」（過去版と一致）か真の不一致かをgit履歴で判別する。
  # 取得失敗・上限超過はhistory_cappedへ明示計上し、照合済みと偽らない。
  revisions = subprocess.run(
    ["git", "rev-list", "HEAD", "--", relative],
    cwd=base,
    capture_output=True,
    text=True,
  )
  if revisions.returncode != 0:
    return "capped"
  hashes = revisions.stdout.split()
  capped = len(hashes) > _HISTORY_CAP
  for commit in hashes[:_HISTORY_CAP]:
    shown = subprocess.run(
      ["git", "show", f"{commit}:{relative}"],
      cwd=base,
      capture_output=True,
    )
    if (
      shown.returncode == 0
      and digests.sha256_hex(shown.stdout) == expected
    ):
      return "match"
  return "capped" if capped else "none"


def collect_binding_metrics(records_root, base_root=None, external_bases=None):
  base = roots.repo_root() if base_root is None else Path(base_root)
  externals = tuple(Path(item) for item in (external_bases or ()))
  scanned_record_count = 0
  total_hex_count = 0
  unpaired_count = 0
  resolved_match = 0
  digest_differs = 0
  file_missing = 0
  external_match = 0
  external_differs = 0
  history_match = 0
  true_mismatch = 0
  history_capped = 0
  for path in sorted(Path(records_root).glob("*.md")):
    try:
      text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
      continue
    scanned_record_count += 1
    total_hex_count += len(_HEX_ANYWHERE.findall(text))
    pairs, unpaired = _binding_pairs(text)
    unpaired_count += unpaired
    for target, expected in pairs:
      candidate = Path(target)
      relative = not candidate.is_absolute()
      if relative:
        candidate = base / candidate
      if candidate.is_file():
        try:
          actual = digests.file_sha256(candidate)
        except OSError:
          file_missing += 1
          continue
        if actual == expected:
          resolved_match += 1
        else:
          digest_differs += 1
          if relative:
            verdict = _history_verdict(base, target, expected)
          else:
            verdict = "capped"
          if verdict == "match":
            history_match += 1
          elif verdict == "none":
            true_mismatch += 1
          else:
            history_capped += 1
        continue
      resolved_external = False
      if relative:
        for external in externals:
          external_candidate = external / target
          if external_candidate.is_file():
            try:
              actual = digests.file_sha256(external_candidate)
            except OSError:
              continue
            if actual == expected:
              external_match += 1
            else:
              external_differs += 1
            resolved_external = True
            break
      if not resolved_external:
        file_missing += 1
  return {
    "scanned_record_count": scanned_record_count,
    "scored_count": (
      resolved_match
      + digest_differs
      + file_missing
      + external_match
      + external_differs
    ),
    "resolved_match": resolved_match,
    "digest_differs": digest_differs,
    "history_match": history_match,
    "true_mismatch": true_mismatch,
    "history_capped": history_capped,
    "external_match": external_match,
    "external_differs": external_differs,
    "file_missing": file_missing,
    "unpaired_count": unpaired_count,
    "total_hex_count": total_hex_count,
  }


def collect_approval_metrics(records_root):
  record_count = 0
  field_count = 0
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
    if _APPROVAL_FIELD_LINE.search(text) is not None:
      field_count += 1
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
    "field_count": field_count,
    "skipped_count": skipped_count,
    "by_date": by_date,
  }


def collect_template_metrics():
  """H4手動記入：builder雛形の記入欄と自動導出率を機械算出する。

  雛形は`_render`（純関数）で類型ごとにin-memory生成し、手数えしない。
  自動導出率＝1−（記入欄数÷非空行数）。
  """
  from tools.request_builder import core

  by_type = {}
  for request_type in core.REQUEST_TYPES:
    section = (
      core._FREE_TEXT_SECTION
      if request_type == "free_text"
      else core._POINTS_SECTION
    )
    text = core._render(
      title="probe",
      kind_label=core._TYPE_LABELS[request_type],
      record_date="2026-01-01",
      base_commit_line="- 基点commit：probe\n",
      digest_table="",
      repository_absolute="/probe",
      record_relative="records/session-handoffs/probe-request-v1.md",
      verdict_relative="records/session-handoffs/probe-verdict-v1.md",
      model="probe-model",
      request_section=section,
    )
    nonempty = [line for line in text.splitlines() if line.strip()]
    manual = text.count(core.PLACEHOLDER_PREFIX)
    by_type[request_type] = {
      "manual_fields": manual,
      "nonempty_lines": len(nonempty),
      "auto_ratio": round(1 - manual / len(nonempty), 4),
    }
  return by_type


def _day(timestamp):
  if timestamp is None:
    return None
  return (
    datetime.fromtimestamp(timestamp).astimezone().date().isoformat()
  )


def collect_preservation_metrics(preservation_root):
  """コスト第一段：保全先の区画別規模（内容不読・区画名のみ出力）。"""
  root = Path(preservation_root)
  if not root.is_dir():
    return {"sections": {}, "root_missing": True}
  sections = {}
  for section_dir in sorted(
    path for path in root.iterdir() if path.is_dir()
  ):
    file_count = 0
    total_bytes = 0
    oldest = None
    newest = None
    for item in section_dir.rglob("*"):
      if not item.is_file():
        continue
      stat = item.stat()
      file_count += 1
      total_bytes += stat.st_size
      if oldest is None or stat.st_mtime < oldest:
        oldest = stat.st_mtime
      if newest is None or stat.st_mtime > newest:
        newest = stat.st_mtime
    sections[section_dir.name] = {
      "file_count": file_count,
      "total_bytes": total_bytes,
      "oldest": _day(oldest),
      "newest": _day(newest),
    }
  return {"sections": sections, "root_missing": False}


def _line_span_seconds(first_line, last_line):
  try:
    first = json.loads(first_line)
    last = json.loads(last_line)
    start = datetime.fromisoformat(
      str(first.get("timestamp")).replace("Z", "+00:00")
    )
    end = datetime.fromisoformat(
      str(last.get("timestamp")).replace("Z", "+00:00")
    )
    return round((end - start).total_seconds(), 3)
  except (ValueError, TypeError):
    return None


def collect_cost_metrics(raw_root):
  """コスト時系列（第一次）：系統dir別の規模とtool_use計数・実時間幅。

  単一の解釈を全系統へ当てない——厳密一致（保守値）と部分一致（上限値）を
  別掲し、timestampを解釈できないfileはduration_unrecognizedへ明示計上する。
  内容は転記しない（数と時刻だけ）。
  """
  root = Path(raw_root)
  if not root.is_dir():
    return {"systems": {}, "root_missing": True}
  systems = {}
  for system_dir in sorted(
    path for path in root.iterdir() if path.is_dir()
  ):
    file_count = 0
    line_count = 0
    typed = 0
    loose = 0
    duration = 0.0
    unrecognized = 0
    for item in sorted(system_dir.rglob("*.jsonl")):
      file_count += 1
      first_line = None
      last_line = None
      with open(item, "rb") as stream:
        for raw_line in stream:
          line_count += 1
          typed += raw_line.count(b'"type":"tool_use"')
          loose += raw_line.count(b"tool_use")
          if first_line is None:
            first_line = raw_line
          last_line = raw_line
      span = (
        _line_span_seconds(first_line, last_line)
        if first_line is not None
        else None
      )
      if span is None:
        unrecognized += 1
      else:
        duration += span
    systems[system_dir.name] = {
      "file_count": file_count,
      "line_count": line_count,
      "tool_use_typed": typed,
      "tool_use_loose": loose,
      "duration_seconds": round(duration, 3),
      "duration_unrecognized": unrecognized,
    }
  return {"systems": systems, "root_missing": False}


def collect_missing_origin(records_root, base_root=None):
  """束縛欠落の由来分類：削除・改名（履歴あり）／履歴なし／絶対path束縛。"""
  base = roots.repo_root() if base_root is None else Path(base_root)
  missing_deleted = 0
  missing_never = 0
  missing_absolute = 0
  for path in sorted(Path(records_root).glob("*.md")):
    try:
      text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
      continue
    pairs, _ = _binding_pairs(text)
    for target, _expected in pairs:
      candidate = Path(target)
      if candidate.is_absolute():
        if not candidate.is_file():
          missing_absolute += 1
        continue
      if (base / candidate).is_file():
        continue
      history = subprocess.run(
        ["git", "rev-list", "--all", "-n", "1", "--", target],
        cwd=base,
        capture_output=True,
        text=True,
      )
      if history.returncode == 0 and history.stdout.strip():
        missing_deleted += 1
      else:
        missing_never += 1
  return {
    "missing_deleted": missing_deleted,
    "missing_never": missing_never,
    "missing_absolute": missing_absolute,
  }


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--launch-root", required=True)
  parser.add_argument("--records-root", default=None)
  parser.add_argument("--preservation-root", default=None)
  parser.add_argument("--raw-root", default=None)
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
  from tools.development.formal_code_reuse_search import default_runtime_root

  external_bases = (
    default_runtime_root() / "projects" / "reviewcompass3" / "development" / "data",
  )
  preservation_root = (
    Path.home()
    / ".reviewcompass3/projects/reviewcompass3/development/sensitive"
    / "eventual-preservation"
    if arguments.preservation_root is None
    else Path(arguments.preservation_root)
  )
  raw_root = (
    preservation_root / "raw"
    if arguments.raw_root is None
    else Path(arguments.raw_root)
  )
  result = {
    "schema_version": 6,
    "status": "ok",
    "launch": collect_launch_metrics(launch_root),
    "approvals": collect_approval_metrics(records_root),
    "bindings": collect_binding_metrics(
      records_root, external_bases=external_bases
    ),
    "templates": collect_template_metrics(),
    "preservation": collect_preservation_metrics(preservation_root),
    "costs": collect_cost_metrics(raw_root),
    "missing_origin": collect_missing_origin(records_root),
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
