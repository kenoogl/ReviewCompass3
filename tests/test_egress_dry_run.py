"""段階2 dry-run（出口設計v4 §8）の暫定テスト。送信機能は持たない。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _dry_run():
  return importlib.import_module("tools.egress.dry_run")


def _routine(path, start, end, name):
  return {
    "symbol_id": f"{path}:{name}",
    "code_reference": {
      "relative_path": path,
      "start_line": start,
      "end_line": end,
    },
    "signature": {"parameters": [], "returns_annotation": None},
    "return_count": 1,
    "raise_count": 0,
    "raised_exception_names": [],
    "branch_count": 0,
    "line_count": end - start + 1,
    "max_nesting_depth": 0,
    "complexity_signal": "low",
    "public_api_signal": "low",
  }


@pytest.fixture
def dataset(tmp_path):
  source = tmp_path / "mod.py"
  source.write_text(
    "def make_widget():\n"
    "  shared_core = 1\n"
    "def make_widget_copy():\n"
    "  shared_core = 1\n"
    "def alpha_beta():\n"
    "  ccc_value = 1\n"
    "def alpha_beta_two():\n"
    "  ddd_value = 1\n",
    encoding="utf-8",
  )
  routines = [
    _routine("mod.py", 1, 2, "make_widget"),
    _routine("mod.py", 3, 4, "make_widget_copy"),
    _routine("mod.py", 5, 6, "alpha_beta"),
    _routine("mod.py", 7, 8, "alpha_beta_two"),
  ]
  routines_by_id = {r["symbol_id"]: r for r in routines}
  groups_by_id = {
    "g1": [routines[0]["symbol_id"], routines[1]["symbol_id"]],
    "g2": [routines[2]["symbol_id"], routines[3]["symbol_id"]],
    "g3": [routines[2]["symbol_id"], routines[3]["symbol_id"]],
  }
  ranking = [
    {"group_id": "g1", "rank": 1},
    {"group_id": "g2", "rank": 2},
    {"group_id": "g3", "rank": 3},
    {"group_id": "g2", "rank": 21},
  ]
  return tmp_path, ranking, groups_by_id, routines_by_id


class TestBuildDryRun:
  def test_only_ambiguous_pairs_become_payloads(self, dataset):
    dry_run = _dry_run()
    root, ranking, groups, routines = dataset
    result = dry_run.build_dry_run(
      repository_root=root,
      ranking_entries=ranking,
      groups_by_id=groups,
      routines_by_id=routines,
      top_rank=20,
    )
    assert result.band_counts["clearly_same"] == 1
    assert result.band_counts["ambiguous"] == 1
    assert len(result.payloads) == 1
    entry = result.entries[0]
    assert entry["symbol_a"] == "mod.py:alpha_beta"
    assert entry["symbol_b"] == "mod.py:alpha_beta_two"

  def test_duplicate_pairs_across_groups_are_counted_once(self, dataset):
    dry_run = _dry_run()
    root, ranking, groups, routines = dataset
    result = dry_run.build_dry_run(
      repository_root=root,
      ranking_entries=ranking,
      groups_by_id=groups,
      routines_by_id=routines,
      top_rank=20,
    )
    total = sum(result.band_counts.values())
    assert total == 2

  def test_list_digest_matches_approval_form(self, dataset):
    dry_run = _dry_run()
    approval = importlib.import_module("tools.egress.approval")
    root, ranking, groups, routines = dataset
    result = dry_run.build_dry_run(
      repository_root=root,
      ranking_entries=ranking,
      groups_by_id=groups,
      routines_by_id=routines,
      top_rank=20,
    )
    assert result.list_digest == approval.payload_list_digest(
      [p.digest for p in result.payloads]
    )


class TestWriteDryRun:
  def test_outputs_are_written_for_human_review(self, dataset, tmp_path):
    dry_run = _dry_run()
    root, ranking, groups, routines = dataset
    result = dry_run.build_dry_run(
      repository_root=root,
      ranking_entries=ranking,
      groups_by_id=groups,
      routines_by_id=routines,
      top_rank=20,
    )
    output = tmp_path / "out"
    manifest_path = dry_run.write_dry_run(result, output)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["payload_list_digest"] == result.list_digest
    assert len(manifest["entries"]) == 1
    digest = manifest["entries"][0]["digest"]
    stored = (output / "payloads" / f"payload-{digest}.json").read_text(
      encoding="utf-8"
    )
    assert (output / "report.md").is_file()
    assert json.loads(stored)["question_id"] == "impl-sameness-v1"
