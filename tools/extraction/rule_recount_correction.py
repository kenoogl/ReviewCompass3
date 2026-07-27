"""規則再集計のsource重複と規則重複の訂正。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


@dataclasses.dataclass(frozen=True)
class RuleRecountCorrection:
  status: str
  corrected_source_count: int
  duplicate_source_paths: tuple
  removed_source_aliases: tuple
  raw_count: int
  kept_count: int
  fragment_count: int
  substring_count: int
  exact_duplicate_count: int
  unexplained_count: int
  discrepancies: tuple
  digest: str


def _rules(record):
  values = []
  for key in ("raise", "reasons", "stderr"):
    items = record.get(key, ())
    if not isinstance(items, (list, tuple)):
      raise ValueError("raw rule fields must be sequences")
    if any(not isinstance(item, str) for item in items):
      raise ValueError("raw rules must be text")
    values.extend(items)
  return tuple(values)


def _canonical_impl(path, records):
  relative = path[6:] if path.startswith("tools/") else path
  exact = [
    record["impl"]
    for record in records
    if record["impl"] == relative
  ]
  if exact:
    return exact[0]
  return sorted(record["impl"] for record in records)[0]


def correct_rule_recount(
  raw_records,
  recount_rows,
  *,
  expected_source_count,
):
  raw_values = tuple(raw_records)
  row_values = tuple(recount_rows)
  if (
    not isinstance(expected_source_count, int)
    or expected_source_count < 0
    or not raw_values
    or not row_values
  ):
    raise ValueError("rule recount inputs are invalid")
  raw_by_impl = {}
  by_path = {}
  for record in raw_values:
    if (
      not isinstance(record, dict)
      or not isinstance(record.get("impl"), str)
      or not record["impl"]
      or not isinstance(record.get("path"), str)
      or not record["path"]
      or record["impl"] in raw_by_impl
    ):
      raise ValueError("raw rule records require unique impl and path")
    _rules(record)
    raw_by_impl[record["impl"]] = record
    by_path.setdefault(record["path"], []).append(record)
  rows = {}
  for row in row_values:
    if (
      not isinstance(row, dict)
      or set(row) < {"impl", "raw", "kept", "frag", "sub"}
      or row.get("impl") in rows
      or row.get("impl") not in raw_by_impl
      or any(
        not isinstance(row.get(key), int)
        or row[key] < 0
        for key in ("raw", "kept", "frag", "sub")
      )
    ):
      raise ValueError("recount rows require unique non-negative counts")
    rows[row["impl"]] = row
  if set(rows) != set(raw_by_impl):
    raise ValueError("raw records and recount rows must match")
  duplicate_paths = tuple(sorted(
    path for path, records in by_path.items() if len(records) > 1
  ))
  removed = set()
  canonical_impls = set()
  for path, records in by_path.items():
    canonical = _canonical_impl(path, records)
    canonical_impls.add(canonical)
    removed.update(
      record["impl"]
      for record in records
      if record["impl"] != canonical
    )
  totals = {
    key: sum(rows[impl][key] for impl in canonical_impls)
    for key in ("raw", "kept", "frag", "sub")
  }
  exact_duplicates = sum(
    len(_rules(raw_by_impl[impl]))
    - len(set(_rules(raw_by_impl[impl])))
    for impl in canonical_impls
  )
  unexplained = (
    totals["raw"]
    - totals["kept"]
    - totals["frag"]
    - totals["sub"]
    - exact_duplicates
  )
  discrepancies = []
  if len(canonical_impls) != expected_source_count:
    discrepancies.append("source_count")
  if unexplained != 0:
    discrepancies.append("unexplained_partition")
  document = {
    "corrected_source_count": len(canonical_impls),
    "duplicate_source_paths": list(duplicate_paths),
    "exact_duplicate_count": exact_duplicates,
    "expected_source_count": expected_source_count,
    "removed_source_aliases": sorted(removed),
    "schema_version": 1,
    "totals": totals,
    "unexplained_count": unexplained,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return RuleRecountCorrection(
    status="follow_up" if discrepancies else "resolved",
    corrected_source_count=len(canonical_impls),
    duplicate_source_paths=duplicate_paths,
    removed_source_aliases=tuple(sorted(removed)),
    raw_count=totals["raw"],
    kept_count=totals["kept"],
    fragment_count=totals["frag"],
    substring_count=totals["sub"],
    exact_duplicate_count=exact_duplicates,
    unexplained_count=unexplained,
    discrepancies=tuple(discrepancies),
    digest=digest,
  )
