"""層1・C-4：宣言→RED対応表の`red_now`を実行で照合する。

承認：DEC-VERIFICATION-BOUNDARY-001（層1、最優先）
所見：records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md 反証C-4
"""

import json
from pathlib import Path

import pytest

from tools.development import declaration_red_map_check as drmc


def _write_tests(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "test_sample.py").write_text(
        "def test_failing():\n    assert False\n\n\n"
        "def test_passing():\n    assert True\n",
        encoding="utf-8",
    )
    return "tests/test_sample.py"


def _map(tmp_path, *, entries):
    test_file = _write_tests(tmp_path)
    document = {
        "record_kind": "declaration_red_map",
        "map_id": "M", "map_version": 1,
        "test_files": {test_file: sorted(name for name, _ in entries)},
        "declarations": {
            "P%d" % index: {
                "summary": "s",
                "tests": [{"test": "%s::%s" % (test_file, name), "red_now": red}],
                "red_now": red,
            }
            for index, (name, red) in enumerate(entries, start=1)
        },
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return path


def _runner(outcomes):
    """node idごとの結果を返す差し替え可能なrunner。"""

    def run(node_ids, *, project_root):
        return {node_id: outcomes[node_id.split("::", 1)[1]] for node_id in node_ids}

    return run


def test_v1_static_check_stays_the_default(tmp_path):
    """既定は静的検査のままであり、実行しない。"""

    path = _map(tmp_path, entries=[("test_passing", True)])

    def forbidden(node_ids, *, project_root):
        raise AssertionError("runner must not be called by default")

    result = drmc.check_declaration_red_map(
        map_path=path, project_root=tmp_path, runner=forbidden
    )
    assert result["status"] == "passed"
    assert "red_verification" not in result


def test_v2_red_claim_is_confirmed_when_the_test_actually_fails(tmp_path):
    path = _map(tmp_path, entries=[("test_failing", True)])
    result = drmc.check_declaration_red_map(
        map_path=path, project_root=tmp_path, verify_red=True,
        runner=_runner({"test_failing": "failed"}),
    )
    assert result["status"] == "passed"
    assert result["red_verification"]["verified"] == 1
    assert result["red_verification"]["mismatched"] == 0


def test_v3_red_claim_is_rejected_when_the_test_actually_passes(tmp_path):
    """反証C-4：REDでないものをREDと称して通せてはならない。"""

    path = _map(tmp_path, entries=[("test_passing", True)])
    result = drmc.check_declaration_red_map(
        map_path=path, project_root=tmp_path, verify_red=True,
        runner=_runner({"test_passing": "passed"}),
    )
    assert result["status"] == "failed"
    assert result["red_verification"]["mismatched"] == 1
    assert any("red_claim_unmet" in finding for finding in result["findings"])


def test_v4_boundary_example_must_actually_pass(tmp_path):
    """red_now falseの境界例は、実際に成功していなければならない。"""

    path = _map(tmp_path, entries=[("test_failing", False)])
    result = drmc.check_declaration_red_map(
        map_path=path, project_root=tmp_path, verify_red=True,
        runner=_runner({"test_failing": "failed"}),
    )
    assert result["status"] == "failed"
    assert any("boundary_claim_unmet" in finding for finding in result["findings"])


def test_v5_unknown_outcome_fails_closed(tmp_path):
    """結果を得られないtestは、合格でも不合格でもなく不明として拒否する。"""

    path = _map(tmp_path, entries=[("test_failing", True)])

    def silent(node_ids, *, project_root):
        return {}

    result = drmc.check_declaration_red_map(
        map_path=path, project_root=tmp_path, verify_red=True, runner=silent
    )
    assert result["status"] == "failed"
    assert any("red_outcome_unknown" in finding for finding in result["findings"])
