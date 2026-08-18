"""運用集計コマンド（順序5）の固定。launch実測の分計と承認点分布。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_launch(root, name, document):
  directory = root / name
  directory.mkdir()
  (directory / "launch.json").write_text(
    json.dumps(document), encoding="utf-8"
  )


def _make_stores(tmp_path):
  launch_root = tmp_path / "launch"
  launch_root.mkdir()
  records_root = tmp_path / "records"
  records_root.mkdir()
  _write_launch(
    launch_root, "run-a", {"elapsed_seconds": 10.0, "prompt_bytes": 100}
  )
  _write_launch(
    launch_root, "run-b", {"elapsed_seconds": 30.0, "prompt_bytes": 300}
  )
  _write_launch(launch_root, "run-c", {"model": "x"})
  broken = launch_root / "run-d"
  broken.mkdir()
  (broken / "launch.json").write_text("{", encoding="utf-8")
  (records_root / "2026-08-01-a-decision-v1.md").write_text(
    "- 承認文言：「進めて」", encoding="utf-8"
  )
  (records_root / "2026-08-01-b-decision-v1.md").write_text(
    "- 承認文言（逐語）：「実施」", encoding="utf-8"
  )
  (records_root / "2026-08-02-c-evidence-v1.md").write_text(
    "記録のみ", encoding="utf-8"
  )
  return launch_root, records_root


def test_launch_metrics_partitions_and_stats(tmp_path):
  from tools.evaluation import operational_metrics

  launch_root, _ = _make_stores(tmp_path)
  result = operational_metrics.collect_launch_metrics(launch_root)
  assert result["instrumented_count"] == 2
  assert result["legacy_count"] == 1
  assert result["skipped_count"] == 1
  assert result["elapsed_seconds"]["total"] == 40.0
  assert result["elapsed_seconds"]["median"] == 20.0
  assert result["prompt_bytes"]["max"] == 300


def test_approval_metrics_by_date(tmp_path):
  from tools.evaluation import operational_metrics

  _, records_root = _make_stores(tmp_path)
  result = operational_metrics.collect_approval_metrics(records_root)
  assert result["record_count"] == 2
  assert result["by_date"] == {"2026-08-01": 2}


def test_run_emits_single_line_json(tmp_path, capsys):
  from tools.evaluation import operational_metrics

  launch_root, records_root = _make_stores(tmp_path)
  exit_code = operational_metrics.run((
    "--launch-root", str(launch_root),
    "--records-root", str(records_root),
  ))
  captured = capsys.readouterr().out
  assert exit_code == 0
  assert captured.count("\n") == 1
  document = json.loads(captured)
  assert document["status"] == "ok"
  assert document["launch"]["instrumented_count"] == 2
  assert document["approvals"]["record_count"] == 2


def test_run_rejects_missing_root(tmp_path, capsys):
  from tools.evaluation import operational_metrics

  exit_code = operational_metrics.run((
    "--launch-root", str(tmp_path / "missing"),
    "--records-root", str(tmp_path),
  ))
  document = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert document["status"] == "input_invalid"


def _make_binding_store(tmp_path):
  from tools.common import digests

  base_root = tmp_path / "base"
  (base_root / "sub").mkdir(parents=True)
  target_a = base_root / "sub" / "target-a.txt"
  target_a.write_text("alpha", encoding="utf-8")
  target_b = base_root / "sub" / "target-b.txt"
  target_b.write_text("beta", encoding="utf-8")
  records_root = tmp_path / "binding-records"
  records_root.mkdir()
  digest_a = digests.file_sha256(target_a)
  wrong_b = "0" * 64
  gone_c = "1" * 64
  unpaired = "2" * 64
  (records_root / "2026-08-18-binding-v1.md").write_text(
    "\n".join([
      "```text",
      f"{digest_a}  sub/target-a.txt",
      "```",
      f"- 資料：`sub/target-b.txt`、SHA-256 `{wrong_b}`",
      f"- 消えたfile：`sub/gone.txt`（SHA-256 `{gone_c}`）",
      f"  SHA-256 `{unpaired}`",
    ]),
    encoding="utf-8",
  )
  return records_root, base_root


def test_binding_metrics_classifies_pairs(tmp_path):
  from tools.evaluation import operational_metrics

  records_root, base_root = _make_binding_store(tmp_path)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root
  )
  assert result["resolved_match"] == 1
  assert result["digest_differs"] == 1
  assert result["file_missing"] == 1
  assert result["scored_count"] == 3


def test_binding_metrics_reports_unscored(tmp_path):
  from tools.evaluation import operational_metrics

  records_root, base_root = _make_binding_store(tmp_path)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root
  )
  assert result["unpaired_count"] == 1
  assert result["total_hex_count"] == 4


def test_approval_metrics_field_count(tmp_path):
  from tools.evaluation import operational_metrics

  _, records_root = _make_stores(tmp_path)
  (records_root / "2026-08-03-d-decision-v1.md").write_text(
    "## 1. 承認文言【記録】\n\n本文", encoding="utf-8"
  )
  result = operational_metrics.collect_approval_metrics(records_root)
  assert result["record_count"] == 3
  assert result["field_count"] == 3


def test_run_schema_version_4(tmp_path, capsys):
  from tools.evaluation import operational_metrics

  launch_root, records_root = _make_stores(tmp_path)
  exit_code = operational_metrics.run((
    "--launch-root", str(launch_root),
    "--records-root", str(records_root),
  ))
  document = json.loads(capsys.readouterr().out)
  assert exit_code == 0
  assert document["schema_version"] == 4
  assert document["bindings"]["total_hex_count"] == 0


def test_module_entry_runs(tmp_path):
  launch_root, records_root = _make_stores(tmp_path)
  completed = subprocess.run(
    [
      sys.executable,
      "-m",
      "tools.evaluation.operational_metrics",
      "--launch-root",
      str(launch_root),
      "--records-root",
      str(records_root),
    ],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True,
    timeout=60,
  )
  assert completed.returncode == 0
  assert json.loads(completed.stdout)["status"] == "ok"


def _make_table_store(tmp_path):
  from tools.common import digests

  base_root = tmp_path / "cbase"
  (base_root / "sub").mkdir(parents=True)
  target = base_root / "sub" / "table-target.txt"
  target.write_text("gamma", encoding="utf-8")
  records_root = tmp_path / "table-records"
  records_root.mkdir()
  digest_c = digests.file_sha256(target)
  (records_root / "2026-08-18-table-v1.md").write_text(
    "\n".join([
      f"| 実装module | `sub/table-target.txt` | `{digest_c}` |",
      f"| `sub/table-target.txt` | `{'1' * 64}` |",
      f"| `work4a/observations/{'2' * 64}.json` | 再観測 |",
      f"| 修正実装 | `{'3' * 64}` |",
    ]),
    encoding="utf-8",
  )
  return records_root, base_root


def test_table_rows_are_scored(tmp_path):
  from tools.evaluation import operational_metrics

  records_root, base_root = _make_table_store(tmp_path)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root
  )
  assert result["resolved_match"] == 1
  assert result["digest_differs"] == 1
  assert result["scored_count"] == 2


def test_hex_inside_filename_is_not_scored(tmp_path):
  from tools.evaluation import operational_metrics

  records_root, base_root = _make_table_store(tmp_path)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root
  )
  assert result["file_missing"] == 0


def test_pathless_hex_row_counts_as_unpaired(tmp_path):
  from tools.evaluation import operational_metrics

  records_root, base_root = _make_table_store(tmp_path)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root
  )
  assert result["unpaired_count"] == 1


def test_external_base_resolution(tmp_path):
  from tools.common import digests
  from tools.evaluation import operational_metrics

  base_root = tmp_path / "repo"
  base_root.mkdir()
  external = tmp_path / "ext"
  (external / "work4b").mkdir(parents=True)
  target = external / "work4b" / "x.json"
  target.write_text("psi", encoding="utf-8")
  records_root = tmp_path / "r"
  records_root.mkdir()
  (records_root / "2026-08-18-e-v1.md").write_text(
    f"| `work4b/x.json` | `{digests.file_sha256(target)}` |",
    encoding="utf-8",
  )
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=base_root, external_bases=(external,)
  )
  assert result["external_match"] == 1
  assert result["file_missing"] == 0


def _git_history_store(tmp_path, cited):
  import subprocess

  repo = tmp_path / "grepo"
  repo.mkdir()

  def _g(*arguments):
    subprocess.run(
      ["git", *arguments], cwd=repo, check=True, capture_output=True
    )

  _g("init", "-q")
  _g("config", "user.email", "x@example.invalid")
  _g("config", "user.name", "x")
  target = repo / "doc.md"
  target.write_text("v1", encoding="utf-8")
  _g("add", ".")
  _g("commit", "-qm", "v1")
  target.write_text("v2", encoding="utf-8")
  _g("add", ".")
  _g("commit", "-qm", "v2")
  records_root = tmp_path / "r2"
  records_root.mkdir()
  (records_root / "2026-08-18-h-v1.md").write_text(
    f"| `doc.md` | `{cited}` |", encoding="utf-8"
  )
  return repo, records_root


def test_history_match_detects_version_progress(tmp_path):
  from tools.common import digests
  from tools.evaluation import operational_metrics

  probe = tmp_path / "probe.md"
  probe.write_text("v1", encoding="utf-8")
  repo, records_root = _git_history_store(
    tmp_path, digests.file_sha256(probe)
  )
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=repo
  )
  assert result["digest_differs"] == 1
  assert result["history_match"] == 1
  assert result["true_mismatch"] == 0


def test_true_mismatch_when_no_version_matches(tmp_path):
  from tools.evaluation import operational_metrics

  repo, records_root = _git_history_store(tmp_path, "9" * 64)
  result = operational_metrics.collect_binding_metrics(
    records_root, base_root=repo
  )
  assert result["digest_differs"] == 1
  assert result["history_match"] == 0
  assert result["true_mismatch"] == 1
