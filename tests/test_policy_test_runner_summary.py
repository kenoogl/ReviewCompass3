"""公式Test receiptの構造化集計のAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md
承認：DEC-RECORD-GENERATION-PLAN-001（TODO最小縦切りだけ）

件数はpytestのmachine API（report object）から数える。stdout／stderrの文字列を
正規表現や分割で解析しない。
"""

import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config/development-test-runner.json"
SUMMARY_FIELDS = (
    "passed", "failed", "skipped", "xfailed", "xpassed", "errors", "total",
)


@pytest.fixture
def runner():
    return importlib.import_module("tools.development.policy_test_runner")


@pytest.fixture
def summary():
    return importlib.import_module("tools.development.pytest_summary")


def _report(*, when, outcome, wasxfail=False):
    report = SimpleNamespace(when=when, outcome=outcome)
    report.passed = outcome == "passed"
    report.failed = outcome == "failed"
    report.skipped = outcome == "skipped"
    if wasxfail:
        report.wasxfail = "expected failure"
    return report


def _fake_run_factory(summary_module, *, counts, returncode=0, write=True):
    def fake_run(command, **kwargs):
        if command[-1] == "--version" and "pytest" not in command:
            return SimpleNamespace(returncode=0, stdout="Python 3.9.6\n", stderr="")
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
        if write:
            target = kwargs["env"][summary_module.SUMMARY_ENVIRONMENT_VARIABLE]
            Path(target).write_text(
                json.dumps(counts, sort_keys=True), encoding="utf-8"
            )
        return SimpleNamespace(returncode=returncode, stdout="", stderr="")

    return fake_run


# ------------------------------------------------------- 集計moduleそのもの


def test_summary_counts_come_from_report_objects(summary):
    counts = summary.new_counts()
    for report in (
        _report(when="setup", outcome="passed"),
        _report(when="call", outcome="passed"),
        _report(when="teardown", outcome="passed"),
        _report(when="call", outcome="failed"),
        _report(when="setup", outcome="failed"),
        _report(when="setup", outcome="skipped"),
        _report(when="call", outcome="skipped", wasxfail=True),
        _report(when="call", outcome="passed", wasxfail=True),
    ):
        summary.record_report(counts, report)

    finalized = summary.finalize(counts)
    assert finalized == {
        "passed": 1,
        "failed": 1,
        "skipped": 1,
        "xfailed": 1,
        "xpassed": 1,
        "errors": 1,
        "total": 6,
    }
    assert summary.validate_summary(finalized) is True


def test_summary_module_documents_every_field(summary):
    document = summary.__doc__ or ""
    for field in SUMMARY_FIELDS:
        assert f"- {field}" in document, field


def test_summary_module_never_parses_output_text(summary):
    text = Path(summary.__file__).read_text(encoding="utf-8")
    for forbidden in ("stdout", "stderr", "import re", "re.search", "splitlines"):
        assert forbidden not in text


def test_summary_rejects_broken_values(summary):
    good = summary.finalize(summary.new_counts())

    def _reject(document):
        with pytest.raises(summary.TestSummaryError):
            summary.validate_summary(document)

    _reject("not a mapping")
    _reject(dict(good, reviewer="claude"))
    _reject({key: value for key, value in good.items() if key != "passed"})
    _reject(dict(good, passed=-1))
    _reject(dict(good, passed=True))
    _reject(dict(good, total=5))


def test_summary_round_trips_through_a_file(summary, tmp_path):
    counts = summary.new_counts()
    summary.record_report(counts, _report(when="call", outcome="passed"))
    path = tmp_path / "summary.json"
    summary.write_summary(path, counts)

    assert summary.read_summary(path) == summary.finalize(counts)

    missing = tmp_path / "absent.json"
    with pytest.raises(summary.TestSummaryError):
        summary.read_summary(missing)

    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(summary.TestSummaryError):
        summary.read_summary(broken)


# ------------------------------------------------------- runnerとの結線


def test_receipt_carries_the_structured_summary(runner, summary, tmp_path):
    config = runner.load_config(CONFIG_PATH)
    counts = {
        "passed": 852, "failed": 0, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "errors": 0, "total": 852,
    }
    receipt_path = tmp_path / "green.json"

    result = runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=receipt_path,
        locate=lambda command: "/usr/bin/python3",
        run=_fake_run_factory(summary, counts=counts),
    )

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert result.status == "passed"
    assert receipt["test_summary"] == counts
    assert set(receipt["test_summary"]) == set(SUMMARY_FIELDS)
    assert all(isinstance(receipt["test_summary"][key], int) for key in SUMMARY_FIELDS)
    # 実行したcommandは設定どおりのままである。
    assert receipt["command"] == ".venv/bin/python3 -m pytest -q"


def test_failed_run_keeps_the_receipt_and_a_consistent_summary(
    runner, summary, tmp_path
):
    config = runner.load_config(CONFIG_PATH)
    counts = {
        "passed": 851, "failed": 1, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "errors": 0, "total": 852,
    }
    receipt_path = tmp_path / "red.json"

    result = runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=receipt_path,
        locate=lambda command: "/usr/bin/python3",
        run=_fake_run_factory(summary, counts=counts, returncode=1),
    )

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert result.status == "failed"
    assert receipt["status"] == "failed"
    assert receipt["test_summary"] == counts


def test_missing_summary_stops_without_writing_a_receipt(runner, summary, tmp_path):
    config = runner.load_config(CONFIG_PATH)
    receipt_path = tmp_path / "unavailable.json"

    with pytest.raises(runner.TestRunnerPolicyError, match="test_summary_unavailable"):
        runner.execute(
            config=config,
            project_root=PROJECT_ROOT,
            suite="full",
            receipt_path=receipt_path,
            locate=lambda command: "/usr/bin/python3",
            run=_fake_run_factory(summary, counts={}, write=False),
        )

    assert not receipt_path.exists()


def test_summary_contradicting_a_passed_status_stops(runner, summary, tmp_path):
    config = runner.load_config(CONFIG_PATH)
    counts = {
        "passed": 851, "failed": 1, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "errors": 0, "total": 852,
    }
    receipt_path = tmp_path / "contradiction.json"

    with pytest.raises(runner.TestRunnerPolicyError, match="test_summary_inconsistent"):
        runner.execute(
            config=config,
            project_root=PROJECT_ROOT,
            suite="full",
            receipt_path=receipt_path,
            locate=lambda command: "/usr/bin/python3",
            run=_fake_run_factory(summary, counts=counts, returncode=0),
        )

    assert not receipt_path.exists()


def test_runner_never_parses_counts_out_of_output_text(runner):
    text = Path(runner.__file__).read_text(encoding="utf-8")
    for forbidden in ("stdout.split", "stderr.split", "passed in", "re.findall"):
        assert forbidden not in text


def test_repository_conftest_registers_the_summary_hooks():
    conftest = PROJECT_ROOT / "conftest.py"
    assert conftest.is_file()
    text = conftest.read_text(encoding="utf-8")
    assert "pytest_runtest_logreport" in text
    assert "pytest_sessionfinish" in text
    assert "pytest_summary" in text


class TestSummaryCountsAreDeduplicatedAndComplete:
    """F-B3反証：同一testの重複計上と、収集errorの欠落を許さない。"""

    def _summary(self):
        import importlib

        return importlib.import_module("tools.development.pytest_summary")

    def test_duplicate_call_reports_for_one_test_count_once(self):
        summary = self._summary()
        counts = summary.new_counts()
        report = SimpleNamespace(
            nodeid="tests/test_x.py::test_one", when="call", outcome="passed"
        )
        summary.record_report(counts, report)
        summary.record_report(counts, report)
        assert counts["passed"] == 1

    def test_distinct_tests_are_counted_separately(self):
        summary = self._summary()
        counts = summary.new_counts()
        for name in ("test_one", "test_two"):
            summary.record_report(
                counts,
                SimpleNamespace(
                    nodeid="tests/test_x.py::%s" % name,
                    when="call",
                    outcome="passed",
                ),
            )
        assert counts["passed"] == 2

    def test_collection_error_is_counted(self):
        summary = self._summary()
        counts = summary.new_counts()
        summary.record_collect_report(
            counts,
            SimpleNamespace(nodeid="tests/test_broken.py", outcome="failed"),
        )
        finalized = summary.finalize(counts)
        assert finalized["errors"] == 1
        assert finalized["total"] == 1

    def test_successful_collection_is_not_counted(self):
        summary = self._summary()
        counts = summary.new_counts()
        summary.record_collect_report(
            counts,
            SimpleNamespace(nodeid="tests/test_ok.py", outcome="passed"),
        )
        assert summary.finalize(counts)["total"] == 0
