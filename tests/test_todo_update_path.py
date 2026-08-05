"""root TODOの更新経路（二段確認）のAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md
承認：DEC-RECORD-GENERATION-PLAN-001（TODO最小縦切りだけ）

一時receiptから候補を作って書き、検証を通し、二度目の正式receiptと集計が完全一致した場合だけ
更新を確定する。どこかで失敗したら、root TODOを更新前のbytesへ戻す。
"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


FULL_TEST_PREFIX = "- 直近の全Test："


@pytest.fixture
def update_path():
    return importlib.import_module("tools.development.todo_update_path")


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _receipt(passed=863, **overrides):
    receipt = {
        "receipt_kind": "policy_test_verification_run",
        "runner_id": "RC3-DEVELOPMENT-TEST-RUNNER",
        "runner_version": 1,
        "recorded_at": "2026-08-05T18:00:00+09:00",
        "suite": "full",
        "command": ".venv/bin/python3 -m pytest -q",
        "configured_python": ".venv/bin/python3",
        "resolved_python": "/usr/bin/python3",
        "python_version": "3.9.6",
        "pytest_version": "8.4.2",
        "fallback_used": False,
        "config_digest": "a" * 64,
        "source_state_digest": "b" * 64,
        "status": "passed",
        "exit_code": 0,
        "test_summary": {
            "passed": passed, "failed": 0, "skipped": 0,
            "xfailed": 0, "xpassed": 0, "errors": 0, "total": passed,
        },
        "stdout": "",
        "stderr": "",
    }
    receipt.update(overrides)
    return receipt


def _workspace(tmp_path):
    root = tmp_path / "project"
    (root / "records").mkdir(parents=True)
    target = root / "records" / "first.md"
    target.write_text("reference\n", encoding="utf-8")
    document = f"""# TODO_NEXT_SESSION

## 現在位置

- 全体：人が書いた説明。機械は触らない。

## 最新のauthority／Evidence

- [記録](records/first.md) — SHA-256 `{_sha256(target)}`

## 次に行う一作業

人が書いた次の一作業。

## Git・Test

- branch：`main`
- 直近の関連Test：関連 `11 passed`
- 直近の全Test：venv公式runner `852 passed`、Python 3.9.6、pytest 8.4.2、fallback false
"""
    todo = root / "TODO_NEXT_SESSION.md"
    todo.write_text(document, encoding="utf-8")
    return root, todo


def _phases(*receipts):
    """段ごとに違うreceiptを返す実行器を作る。呼出し回数も数える。"""

    calls = []

    def run_official_tests(phase):
        calls.append(phase)
        return receipts[len(calls) - 1]

    run_official_tests.calls = calls
    return run_official_tests


# ------------------------------------------------------------------ 正常


def test_two_phase_update_writes_only_the_machine_managed_parts(
    update_path, tmp_path
):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()
    runner = _phases(_receipt(), _receipt())

    result = update_path.run_two_phase_update(
        project_root=root,
        todo_path=todo,
        run_official_tests=runner,
        verify=lambda path, project_root: True,
    )

    after = todo.read_text(encoding="utf-8")
    assert runner.calls == ["first", "second"]
    assert f"{FULL_TEST_PREFIX}venv公式runner `863 passed`" in after
    assert "852 passed" not in after
    assert "- 全体：人が書いた説明。機械は触らない。" in after
    assert "人が書いた次の一作業。" in after
    assert "- 直近の関連Test：関連 `11 passed`" in after
    assert "- [記録](records/first.md) — SHA-256 " in after
    assert todo.read_bytes() == result["todo_bytes"]
    assert result["todo_bytes"] != before
    assert result["first_receipt"]["test_summary"] == result["second_receipt"]["test_summary"]


def test_compared_fields_cover_summary_versions_and_status(update_path):
    assert set(update_path.COMPARED_FIELDS) == {
        "test_summary", "suite", "python_version", "pytest_version",
        "fallback_used", "status",
    }
    assert update_path.compare_receipts(_receipt(), _receipt()) is True


# ------------------------------------------------------------------ 二回の不一致


def test_summary_mismatch_between_the_two_runs_restores_the_todo(
    update_path, tmp_path
):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()
    runner = _phases(_receipt(863), _receipt(864))

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root,
            todo_path=todo,
            run_official_tests=runner,
            verify=lambda path, project_root: True,
        )

    assert error.value.code == "receipt_summary_mismatch"
    assert todo.read_bytes() == before
    assert runner.calls == ["first", "second"]


def test_version_mismatch_between_the_two_runs_restores_the_todo(
    update_path, tmp_path
):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()
    runner = _phases(_receipt(), _receipt(pytest_version="8.4.3"))

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root,
            todo_path=todo,
            run_official_tests=runner,
            verify=lambda path, project_root: True,
        )

    assert error.value.code == "receipt_summary_mismatch"
    assert todo.read_bytes() == before


# ------------------------------------------------------------------ 書込み後の不一致


def test_read_back_mismatch_restores_the_todo(update_path, tmp_path):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()

    def corrupting_write(path, data):
        Path(path).write_bytes(data + b"corrupted\n")

    runner = _phases(_receipt(), _receipt())
    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root,
            todo_path=todo,
            run_official_tests=runner,
            verify=lambda path, project_root: True,
            write=corrupting_write,
        )

    assert error.value.code == "todo_read_back_mismatch"
    assert todo.read_bytes() == before
    assert runner.calls == ["first"], "書込みに失敗したら二度目は実行しない"


# ------------------------------------------------------------------ validator失敗


def test_validator_failure_restores_the_todo(update_path, tmp_path):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()

    def failing_verify(path, project_root):
        raise RuntimeError("handoff validator failed")

    runner = _phases(_receipt(), _receipt())
    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root,
            todo_path=todo,
            run_official_tests=runner,
            verify=failing_verify,
        )

    assert error.value.code == "todo_verification_failed"
    assert todo.read_bytes() == before
    assert runner.calls == ["first"]


def test_broken_receipt_stops_before_writing(update_path, tmp_path):
    root, todo = _workspace(tmp_path)
    before = todo.read_bytes()
    runner = _phases(_receipt(status="failed", exit_code=1), _receipt())

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root,
            todo_path=todo,
            run_official_tests=runner,
            verify=lambda path, project_root: True,
        )

    assert error.value.code == "todo_candidate_failed"
    assert todo.read_bytes() == before
    assert runner.calls == ["first"]


# ------------------------------------------------------------------ 既定の検証


def test_default_verification_runs_the_repository_validators(update_path):
    source = Path(update_path.__file__).read_text(encoding="utf-8")
    for expected in ("todo_handoff", "todo_compaction", "validate_todo_reference_digests"):
        assert expected in source


def test_atomic_write_replaces_in_one_step(update_path, tmp_path):
    target = tmp_path / "file.md"
    target.write_text("before\n", encoding="utf-8")
    update_path.atomic_write(target, "after\n".encode("utf-8"))
    assert target.read_text(encoding="utf-8") == "after\n"
    assert sorted(item.name for item in tmp_path.iterdir()) == ["file.md"]
