"""実行照合の欠落補修：収集エラーはそのfileの全testの失敗として扱う。

承認：DEC-RED-VERIFICATION-ADOPTION-001（手順が回るための前提）
経緯：層3のRED固定時、module未実装のImportErrorでtest単位の結果行が出ず、
本来REDである宣言が全件`unknown`となって手順が停止した。
"""

from tools.development import declaration_red_map_check as drmc


_COLLECTION_ERROR_OUTPUT = """
==================================== ERRORS ====================================
_______ ERROR collecting tests/test_sample.py _______
ImportError while importing test module 'tests/test_sample.py'.
=========================== short test summary info ============================
ERROR tests/test_sample.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
"""

_NORMAL_OUTPUT = """
PASSED tests/test_sample.py::test_a
FAILED tests/test_sample.py::test_b
"""


def test_collection_error_marks_every_node_in_that_file_as_error():
    outcomes = drmc.parse_pytest_outcomes(
        _COLLECTION_ERROR_OUTPUT,
        node_ids=["tests/test_sample.py::test_a", "tests/test_sample.py::test_b"],
    )
    assert outcomes == {
        "tests/test_sample.py::test_a": "error",
        "tests/test_sample.py::test_b": "error",
    }


def test_per_test_outcomes_are_read_when_available():
    outcomes = drmc.parse_pytest_outcomes(
        _NORMAL_OUTPUT,
        node_ids=["tests/test_sample.py::test_a", "tests/test_sample.py::test_b"],
    )
    assert outcomes == {
        "tests/test_sample.py::test_a": "passed",
        "tests/test_sample.py::test_b": "failed",
    }


def test_unrelated_files_are_not_marked_by_a_collection_error():
    outcomes = drmc.parse_pytest_outcomes(
        _COLLECTION_ERROR_OUTPUT,
        node_ids=["tests/test_other.py::test_c"],
    )
    assert outcomes == {}
