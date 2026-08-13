"""Work 5B対象helper：宣言→RED対応表検査器の宣言C1〜C4を固定するTest。

承認：DEC-WORK5B-START-001 §2（検査範囲は3判定＋fail-closed）
"""

import json
from pathlib import Path

import pytest

from tools.development import declaration_red_map_check as drmc


def _write_test_file(tmp_path, body):
    target = tmp_path / "tests" / "test_sample.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    return "tests/test_sample.py"


def _write_map(tmp_path, *, test_file, declarations, listed=None):
    functions = sorted(
        {entry["test"].split("::", 1)[1] for d in declarations.values() for entry in d["tests"]}
        if listed is None
        else listed
    )
    document = {
        "record_kind": "declaration_red_map",
        "map_id": "RC3-SAMPLE-MAP-001",
        "map_version": 1,
        "test_files": {test_file: functions},
        "declarations": declarations,
    }
    target = tmp_path / "sample-map.json"
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def _declaration(test_file, names):
    return {
        "summary": "sample declaration",
        "tests": [{"test": f"{test_file}::{name}", "red_now": True} for name in names],
        "red_now": True,
    }


def test_c1_passes_when_all_listed_tests_exist(tmp_path):
    test_file = _write_test_file(
        tmp_path, "def test_a():\n    pass\n\n\ndef test_b():\n    pass\n"
    )
    map_path = _write_map(
        tmp_path,
        test_file=test_file,
        declarations={
            "P1": _declaration(test_file, ["test_a"]),
            "P2": _declaration(test_file, ["test_b"]),
        },
    )
    result = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    assert result["status"] == "passed"
    assert result["machine_count"] == {
        "declarations": 2,
        "declarations_without_tests": 0,
        "listed_tests_missing_in_file": 0,
        "tests_unmapped_to_declarations": 0,
    }


def test_c1_fails_when_a_listed_test_is_missing(tmp_path):
    test_file = _write_test_file(tmp_path, "def test_a():\n    pass\n")
    map_path = _write_map(
        tmp_path,
        test_file=test_file,
        declarations={"P1": _declaration(test_file, ["test_a", "test_ghost"])},
    )
    result = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert result["machine_count"]["listed_tests_missing_in_file"] == 1
    assert any("test_ghost" in finding for finding in result["findings"])


def test_c2_fails_when_a_declaration_has_no_tests(tmp_path):
    test_file = _write_test_file(tmp_path, "def test_a():\n    pass\n")
    declarations = {
        "P1": _declaration(test_file, ["test_a"]),
        "P2": {"summary": "empty declaration", "tests": [], "red_now": False},
    }
    map_path = _write_map(
        tmp_path, test_file=test_file, declarations=declarations, listed=["test_a"]
    )
    result = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert result["machine_count"]["declarations_without_tests"] == 1


def test_c3_fails_when_a_test_is_unmapped(tmp_path):
    test_file = _write_test_file(
        tmp_path, "def test_a():\n    pass\n\n\ndef test_orphan():\n    pass\n"
    )
    map_path = _write_map(
        tmp_path,
        test_file=test_file,
        declarations={"P1": _declaration(test_file, ["test_a"])},
        listed=["test_a", "test_orphan"],
    )
    result = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    assert result["status"] == "failed"
    assert result["machine_count"]["tests_unmapped_to_declarations"] == 1
    assert any("test_orphan" in finding for finding in result["findings"])


def test_c4_fails_closed_on_missing_map_or_test_file(tmp_path):
    missing = drmc.check_declaration_red_map(
        map_path=tmp_path / "absent-map.json", project_root=tmp_path
    )
    assert missing["status"] == "failed"
    assert any("absent-map" in finding for finding in missing["findings"])

    map_path = _write_map(
        tmp_path,
        test_file="tests/never_written.py",
        declarations={"P1": _declaration("tests/never_written.py", ["test_a"])},
    )
    unreadable = drmc.check_declaration_red_map(
        map_path=map_path, project_root=tmp_path
    )
    assert unreadable["status"] == "failed"
    assert any("never_written" in finding for finding in unreadable["findings"])


def test_c4_result_is_deterministic(tmp_path):
    test_file = _write_test_file(tmp_path, "def test_a():\n    pass\n")
    map_path = _write_map(
        tmp_path,
        test_file=test_file,
        declarations={"P1": _declaration(test_file, ["test_a"])},
    )
    first = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    second = drmc.check_declaration_red_map(map_path=map_path, project_root=tmp_path)
    assert first == second


class TestCompleteScopeCannotBeEmptied:
    """F-B4反証：宣言逃れ・型偽装・root脱出を対応表で合格させない。"""

    def test_complete_scope_with_no_declarations_is_rejected(self, tmp_path):
        test_file = _write_test_file(tmp_path, "def test_a():\n    pass\n")
        cases = (
            (
                "without-declarations",
                {
                    "scope": {"kind": "complete"},
                    "test_files": {test_file: ["test_a"]},
                    "declarations": {},
                },
                "complete_scope_without_declarations",
            ),
            (
                "without-test-files",
                {
                    "scope": {"kind": "complete"},
                    "test_files": {},
                    "declarations": {"D1": _declaration(test_file, ["test_a"])},
                },
                "complete_scope_without_test_files",
            ),
        )
        for name, document, expected_finding in cases:
            map_path = tmp_path / f"{name}.json"
            map_path.write_text(
                json.dumps(document, ensure_ascii=False), encoding="utf-8"
            )
            result = drmc.check_declaration_red_map(
                map_path=map_path, project_root=tmp_path
            )
            assert result["status"] == "failed"
            assert any(
                expected_finding in finding for finding in result["findings"]
            )

    def test_non_boolean_red_now_is_rejected(self, tmp_path):
        _write_test_file(tmp_path, "def test_a():\n    pass\n")
        map_path = tmp_path / "typed-map.json"
        map_path.write_text(
            json.dumps(
                {
                    "scope": {"kind": "complete"},
                    "test_files": {"tests/test_sample.py": ["test_a"]},
                    "declarations": {
                        "D1": {
                            "summary": "s",
                            "tests": [
                                {
                                    "test": "tests/test_sample.py::test_a",
                                    "red_now": "false",
                                }
                            ],
                        }
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = drmc.check_declaration_red_map(
            map_path=map_path, project_root=tmp_path
        )
        assert result["status"] == "failed"
        assert any("red_now" in finding for finding in result["findings"])

    def test_test_file_outside_project_root_is_rejected(self, tmp_path):
        outside = tmp_path.parent / "outside_sample.py"
        outside.write_text("def test_a():\n    pass\n", encoding="utf-8")
        map_path = tmp_path / "escape-map.json"
        map_path.write_text(
            json.dumps(
                {
                    "scope": {"kind": "complete"},
                    "test_files": {"../outside_sample.py": ["test_a"]},
                    "declarations": {
                        "D1": {
                            "summary": "s",
                            "tests": [
                                {
                                    "test": "../outside_sample.py::test_a",
                                    "red_now": True,
                                }
                            ],
                        }
                    },
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = drmc.check_declaration_red_map(
            map_path=map_path, project_root=tmp_path
        )
        assert result["status"] == "failed"
        assert any(
            "outside" in finding or "scope" in finding
            for finding in result["findings"]
        )
