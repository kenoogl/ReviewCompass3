"""REDが予定した理由で失敗したことを機械照合する受入試験。"""

import json

from tools.development import declaration_red_map_check as drmc


def _map(tmp_path, *, expected_reason=None, contract_version=2):
    test_file = tmp_path / "tests/test_sample.py"
    test_file.parent.mkdir()
    test_file.write_text(
        "def test_expected_red():\n    assert False, 'planned missing behavior'\n",
        encoding="utf-8",
    )
    item = {
        "test": "tests/test_sample.py::test_expected_red",
        "red_now": True,
    }
    if expected_reason is not None:
        item["expected_failure_reason"] = expected_reason
    document = {
        "schema_version": 2,
        "record_kind": "declaration_red_map",
        "scope": {"kind": "complete"},
        "red_verification_contract": {"version": contract_version},
        "test_files": {"tests/test_sample.py": ["test_expected_red"]},
        "declarations": {
            "RFR-TEST-001": {
                "summary": "予定した理由でREDになる",
                "tests": [item],
            }
        },
    }
    path = tmp_path / "map.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return path


def _runner(outcome, reason):
    def run(node_ids, *, project_root):
        return {
            node_id: {"outcome": outcome, "reason": reason}
            for node_id in node_ids
        }

    return run


def test_reason_bound_red_passes_only_when_failure_reason_matches(tmp_path):
    path = _map(tmp_path, expected_reason="planned missing behavior")

    matching = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
        verify_red=True,
        minimum_red_contract_version=2,
        runner=_runner("failed", "AssertionError: planned missing behavior"),
    )
    assert matching["status"] == "passed"
    assert matching["red_verification"]["reason_verified"] == 1
    for wrong_reason in (
        "FileNotFoundError: missing parent directory",
        "unexpected process: ['git', 'ls-files']",
        "approval store mode is 0755",
        "fixed argv differs at --mcp-config",
    ):
        mismatch = drmc.check_declaration_red_map(
            map_path=path,
            project_root=tmp_path,
            verify_red=True,
            minimum_red_contract_version=2,
            runner=_runner("failed", wrong_reason),
        )
        assert mismatch["status"] == "failed"
        assert mismatch["red_verification"]["reason_mismatched"] == 1
        assert any(
            "red_failure_reason_mismatch" in item
            for item in mismatch["findings"]
        )


def test_collection_or_setup_error_never_counts_as_expected_red(tmp_path):
    path = _map(tmp_path, expected_reason="planned missing behavior")

    result = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
        verify_red=True,
        minimum_red_contract_version=2,
        runner=_runner("error", "ImportError while collecting tests/test_sample.py"),
    )

    assert result["status"] == "failed"
    assert result["red_verification"]["execution_errors"] == 1
    assert any("red_execution_error" in item for item in result["findings"])


def test_reason_bound_contract_requires_expected_reason_for_every_red_test(tmp_path):
    path = _map(tmp_path, expected_reason=None)

    result = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
        minimum_red_contract_version=2,
    )

    assert result["status"] == "failed"
    assert any("expected_failure_reason_missing" in item for item in result["findings"])


def test_legacy_map_remains_readable_but_cannot_satisfy_version_two(tmp_path):
    path = _map(
        tmp_path,
        expected_reason="planned missing behavior",
        contract_version=1,
    )

    legacy = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
    )
    current = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
        minimum_red_contract_version=2,
    )

    assert legacy["status"] == "passed"
    assert current["status"] == "failed"
    assert any("red_contract_too_old" in item for item in current["findings"])


def test_default_runner_captures_a_real_failure_reason(tmp_path):
    path = _map(tmp_path, expected_reason="planned missing behavior")

    result = drmc.check_declaration_red_map(
        map_path=path,
        project_root=tmp_path,
        verify_red=True,
        minimum_red_contract_version=2,
    )

    assert result["status"] == "passed"
    assert result["red_verification"]["reason_verified"] == 1
