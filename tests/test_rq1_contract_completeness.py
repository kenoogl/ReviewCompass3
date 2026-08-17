"""RQ1装置（Contract completeness計測）のAcceptance Test。

作業票（docs/development/2026-08-17-rq1-apparatus-work-ticket-v1.md）§2・§4を固定する。
- fixture登録形：正常・欠落・競合・staleの4群（各3件以上・後から追加可能）
- 指標の数え方（§4の定義）を検証する。実fixture群の率の値そのものは固定しない
  （値は初回計測でEvidenceへ転記——計測と試験の分離）
- 既存task_contract部品は読み取り専用で利用（無変更）
"""

import importlib
import json


def _apparatus():
    return importlib.import_module(
        "tools.evaluation.rq1_contract_completeness"
    )


def test_fixture_registry_has_four_groups_with_three_each():
    apparatus = _apparatus()
    groups = {}
    for name, group in apparatus.fixture_registry():
        groups.setdefault(group, []).append(name)
    assert set(groups) == {"normal", "missing", "conflict", "stale"}
    for group, names in groups.items():
        assert len(names) >= 3, group
    all_names = [name for name, _ in apparatus.fixture_registry()]
    assert len(all_names) == len(set(all_names))


def test_normal_full_binding_succeeds_with_full_coverage(tmp_path):
    apparatus = _apparatus()
    observation = apparatus.run_fixture("normal-full-binding", tmp_path)
    assert observation["group"] == "normal"
    assert observation["outcome"] == "succeeded"
    assert observation["requirement_to_obligation_coverage"] == 1.0


def test_missing_definition_fixture_is_detected(tmp_path):
    apparatus = _apparatus()
    observation = apparatus.run_fixture(
        "missing-definition-file", tmp_path
    )
    assert observation["group"] == "missing"
    assert observation["outcome"] in ("stopped", "blocking")


def test_regeneration_match_uses_three_byte_identical_compiles(tmp_path):
    apparatus = _apparatus()
    observation = apparatus.run_fixture("normal-full-binding", tmp_path)
    assert observation["regeneration"]["repetitions"] == 3
    assert observation["regeneration"]["byte_identical"] is True


def test_metric_arithmetic_from_observations():
    apparatus = _apparatus()
    observations = [
        {
            "name": "n1",
            "group": "normal",
            "outcome": "succeeded",
            "requirement_to_obligation_coverage": 1.0,
            "obligation_to_plan_coverage": 1.0,
            "regeneration": {"repetitions": 3, "byte_identical": True},
        },
        {
            "name": "n2",
            "group": "normal",
            "outcome": "stopped",
            "stage": "compile",
            "reason": "unexpected",
        },
        {
            "name": "m1",
            "group": "missing",
            "outcome": "blocking",
            "stage": "coverage",
            "reason": "unreceived",
        },
        {
            "name": "m2",
            "group": "missing",
            "outcome": "succeeded",
        },
    ]
    metrics = apparatus.aggregate_metrics(observations)
    assert metrics["negative_detection_rate"] == 0.5
    assert metrics["false_stop_rate"] == 0.5
    assert metrics["regeneration_match_rate"] == 1.0
    assert metrics["requirement_to_obligation_coverage"] == 1.0


def test_cli_outputs_single_line_canonical_json(tmp_path, capsys):
    apparatus = _apparatus()
    exit_code = apparatus.run(("--base-dir", str(tmp_path)))
    output = capsys.readouterr().out
    lines = [line for line in output.strip().splitlines() if line]
    assert exit_code == 0
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert set(payload["fixture_counts"]) == {
        "normal", "missing", "conflict", "stale",
    }
    for key in (
        "requirement_to_obligation_coverage",
        "obligation_to_plan_coverage",
        "regeneration_match_rate",
        "negative_detection_rate",
        "false_stop_rate",
    ):
        assert key in payload["metrics"]
    assert payload["provenance"]["compile_repetitions"] == 3
    assert len(payload["observations"]) == sum(
        payload["fixture_counts"].values()
    )
