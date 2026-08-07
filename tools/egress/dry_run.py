"""段階2 dry-run（出口設計v4 §8）。送信機能を持たない。

上位groupへローカル事前分類を適用し、曖昧な組だけを3種構成payloadに
組み立てて、Humanが目視できる形（payload実物・manifest・報告書）で
書き出す。この出力が§4の送信物一覧承認の材料になる。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import itertools
import json
from pathlib import Path

from tools.egress.approval import payload_list_digest
from tools.egress.payload import build_pair_payload, cut_code_fragment
from tools.egress.prefilter import DEFAULT_THRESHOLDS, classify_pair


@dataclasses.dataclass(frozen=True)
class DryRunResult:
  payloads: tuple
  entries: tuple
  band_counts: dict
  list_digest: str


def _symbol_name(symbol_id):
  return symbol_id.rsplit(":", 1)[-1]


def build_dry_run(
  *,
  repository_root,
  ranking_entries,
  groups_by_id,
  routines_by_id,
  top_rank,
  question_id="impl-sameness-v1",
  thresholds=DEFAULT_THRESHOLDS,
):
  """曖昧な組だけからdry-run payload一式を機械的に組み立てる。"""
  band_counts = {"clearly_same": 0, "clearly_diff": 0, "ambiguous": 0}
  payloads = []
  entries = []
  seen_pairs = set()
  code_cache = {}

  def code_text(routine):
    symbol = routine["symbol_id"]
    if symbol not in code_cache:
      code_cache[symbol] = cut_code_fragment(
        repository_root, routine["code_reference"]
      ).content
    return code_cache[symbol]

  for entry in sorted(ranking_entries, key=lambda e: e["rank"]):
    if entry["rank"] > top_rank:
      continue
    members = [
      m for m in groups_by_id.get(entry["group_id"], [])
      if m in routines_by_id
    ]
    for symbol_a, symbol_b in itertools.combinations(members, 2):
      key = frozenset((symbol_a, symbol_b))
      if key in seen_pairs:
        continue
      seen_pairs.add(key)
      routine_a = routines_by_id[symbol_a]
      routine_b = routines_by_id[symbol_b]
      outcome = classify_pair(
        code_a=code_text(routine_a),
        code_b=code_text(routine_b),
        name_a=_symbol_name(symbol_a),
        name_b=_symbol_name(symbol_b),
        routine_a=routine_a,
        routine_b=routine_b,
        thresholds=thresholds,
      )
      band_counts[outcome.band] += 1
      if outcome.band != "ambiguous":
        continue
      built = build_pair_payload(
        repository_root=repository_root,
        routine_a=routine_a,
        routine_b=routine_b,
        question_id=question_id,
      )
      payloads.append(built)
      entries.append({
        "symbol_a": symbol_a,
        "symbol_b": symbol_b,
        "similarity": round(outcome.similarity, 3),
        "digest": built.digest,
      })

  return DryRunResult(
    payloads=tuple(payloads),
    entries=tuple(entries),
    band_counts=band_counts,
    list_digest=payload_list_digest([p.digest for p in payloads]),
  )


def write_dry_run(result, output_dir):
  """payload実物・manifest・報告書を書き出し、manifestのpathを返す。"""
  output = Path(output_dir)
  payload_dir = output / "payloads"
  payload_dir.mkdir(parents=True, exist_ok=True)
  for built in result.payloads:
    (payload_dir / f"payload-{built.digest}.json").write_text(
      built.content + "\n", encoding="utf-8"
    )
  manifest = {
    "schema_version": 1,
    "payload_list_digest": result.list_digest,
    "band_counts": result.band_counts,
    "entries": list(result.entries),
  }
  manifest_path = output / "manifest.json"
  manifest_path.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True)
    + "\n",
    encoding="utf-8",
  )
  lines = [
    "# dry-run報告（送信は行っていない）",
    "",
    f"- 一覧digest：`{result.list_digest}`",
    f"- 分類：明らかに同じ {result.band_counts['clearly_same']}"
    f"／明らかに別 {result.band_counts['clearly_diff']}"
    f"／曖昧（payload化） {result.band_counts['ambiguous']}",
    "",
    "| # | 組 | 合成類似度 | payload digest |",
    "| --- | --- | --- | --- |",
  ]
  for index, item in enumerate(result.entries, start=1):
    lines.append(
      f"| {index} | `{item['symbol_a']}`<br>`{item['symbol_b']}` "
      f"| {item['similarity']} | `{item['digest'][:16]}…` |"
    )
  (output / "report.md").write_text(
    "\n".join(lines) + "\n", encoding="utf-8"
  )
  return manifest_path
