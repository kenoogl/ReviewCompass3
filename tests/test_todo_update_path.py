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
from types import SimpleNamespace

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
    # 参照Digestは、歴史的なglobal validatorではなくEvidence節に限定した検証を使う。
    for expected in ("todo_handoff", "todo_compaction", "verify_reference_digests"):
        assert expected in source
    assert "issue_resolution_post_write" not in source


def test_atomic_write_replaces_in_one_step(update_path, tmp_path):
    target = tmp_path / "file.md"
    target.write_text("before\n", encoding="utf-8")
    update_path.atomic_write(target, "after\n".encode("utf-8"))
    assert target.read_text(encoding="utf-8") == "after\n"
    assert sorted(item.name for item in tmp_path.iterdir()) == ["file.md"]


# ------------------------------------------- 境界訂正：active IDは正本から得る
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-repair-record-generation-todo-boundaries.md
#
# 許可するactive IDはTODO本文からではなく、project内の既存Issue正本からだけ得る。

LEGACY_ROOT = ".reviewcompass/workflow/issues"
V4_ROOT = ".reviewcompass/workflow/issues-v4"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _issue_workspace(tmp_path, *, active_id="ISSUE-PILOT-TODO-GROWTH-001"):
    root = tmp_path / "project"
    (root / "records").mkdir(parents=True)
    (root / LEGACY_ROOT).mkdir(parents=True)
    (root / V4_ROOT).mkdir(parents=True)
    (root / LEGACY_ROOT / ".gitkeep").write_text("", encoding="utf-8")
    (root / V4_ROOT / ".gitkeep").write_text("", encoding="utf-8")
    (root / LEGACY_ROOT / "issue-pilot-todo-growth-001--v1.json").write_text(
        json.dumps(
            {"record_kind": "issue_record", "issue_id": "ISSUE-PILOT-TODO-GROWTH-001"},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (root / V4_ROOT / "issue-htc-66c3e6ca--v1.json").write_text(
        json.dumps(
            {"record_kind": "issue_record", "issue_id": "ISSUE-HTC-66C3E6CA"},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    target = root / "records" / "first.md"
    target.write_text("reference\n", encoding="utf-8")
    document = f"""# TODO_NEXT_SESSION

## 現在位置

- 全体：人が書いた説明。

## 現在作業に影響する改善候補／Issue

- `{active_id}`：resolved。現行Workへの影響なし。

## 最新のauthority／Evidence

- [記録](records/first.md) — SHA-256 `{_sha256(target)}`

## 次に行う一作業

人が書いた次の一作業。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：関連 `11 passed`
- 直近の全Test：venv公式runner `852 passed`、Python 3.9.6、pytest 8.4.2、fallback false
"""
    todo = root / "TODO_NEXT_SESSION.md"
    todo.write_text(document, encoding="utf-8")
    return root, todo


def test_known_active_ids_come_from_both_issue_roots(update_path, tmp_path):
    root, _todo = _issue_workspace(tmp_path)

    known = update_path.load_known_active_issue_ids(root)

    assert known == {"ISSUE-PILOT-TODO-GROWTH-001", "ISSUE-HTC-66C3E6CA"}


def test_known_active_ids_ignore_the_todo_document(update_path, tmp_path):
    root, todo = _issue_workspace(tmp_path, active_id="ISSUE-UNKNOWN-001")

    known = update_path.load_known_active_issue_ids(root)

    assert "ISSUE-UNKNOWN-001" not in known


def test_unknown_active_id_stops_verification(update_path, tmp_path):
    root, todo = _issue_workspace(tmp_path, active_id="ISSUE-UNKNOWN-001")

    with pytest.raises(Exception) as error:
        update_path.default_verify(todo, root)
    assert "unknown active ID" in str(error.value) or "ISSUE-UNKNOWN-001" in str(error.value)


def test_unknown_active_id_restores_the_todo_without_a_second_run(
    update_path, tmp_path
):
    root, todo = _issue_workspace(tmp_path, active_id="ISSUE-UNKNOWN-001")
    before = todo.read_bytes()
    runner = _phases(_receipt(), _receipt())

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root, todo_path=todo, run_official_tests=runner
        )

    assert error.value.code == "todo_verification_failed"
    assert todo.read_bytes() == before
    assert runner.calls == ["first"]


def test_issue_root_problems_stop(update_path, tmp_path):
    root, _todo = _issue_workspace(tmp_path)

    def _reject_roots():
        with pytest.raises(update_path.TodoUpdatePathError) as error:
            update_path.load_known_active_issue_ids(root)
        return error.value.code

    broken = root / V4_ROOT / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert _reject_roots() == "issue_root_invalid"
    broken.unlink()

    unknown_kind = root / V4_ROOT / "unknown.json"
    unknown_kind.write_text(
        json.dumps({"record_kind": "note", "issue_id": "ISSUE-X-001"}), encoding="utf-8"
    )
    assert _reject_roots() == "issue_root_invalid"
    unknown_kind.unlink()

    missing_id = root / V4_ROOT / "missing.json"
    missing_id.write_text(json.dumps({"record_kind": "issue_record"}), encoding="utf-8")
    assert _reject_roots() == "issue_root_invalid"
    missing_id.unlink()

    duplicated = root / V4_ROOT / "duplicated.json"
    duplicated.write_text(
        json.dumps({"record_kind": "issue_record", "issue_id": "ISSUE-HTC-66C3E6CA"}),
        encoding="utf-8",
    )
    assert _reject_roots() == "issue_root_invalid"
    duplicated.unlink()

    linked = root / V4_ROOT / "linked.json"
    linked.symlink_to(root / V4_ROOT / "issue-htc-66c3e6ca--v1.json")
    assert _reject_roots() == "issue_root_invalid"
    linked.unlink()

    assert update_path.load_known_active_issue_ids(root)


def test_repository_todo_resolves_its_active_id_from_the_issue_records(update_path):
    known = update_path.load_known_active_issue_ids(PROJECT_ROOT)

    assert "ISSUE-PILOT-TODO-GROWTH-001" in known
    assert {"ISSUE-HTC-66C3E6CA", "ISSUE-HTC-BEB5E0BD", "ISSUE-HTC-C9F6C917"} <= known
    assert update_path.default_verify(
        PROJECT_ROOT / "TODO_NEXT_SESSION.md", PROJECT_ROOT
    ) is True


# ------------------------------------------------- CLI（機械更新の入口）
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-repair-todo-test-projection-cli.md
#
# 二段更新経路を機械処理として起動できるCLI。TODO本文を直接編集しない。


def _cli_workspace(tmp_path, *, active_id="ISSUE-PILOT-TODO-GROWTH-001"):
    root, todo = _issue_workspace(tmp_path, active_id=active_id)
    (root / "records" / "development").mkdir(parents=True)
    # CLIはproject rootのrunner configを読む。実configをそのまま写す。
    config = root / "config" / "development-test-runner.json"
    config.parent.mkdir(parents=True)
    config.write_bytes(
        (PROJECT_ROOT / "config/development-test-runner.json").read_bytes()
    )
    return root, todo


def _fake_execute(summaries, *, calls):
    """policy_test_runner.executeの代わり。receipt fileを書いて結果を返す。"""

    def execute(*, config, project_root, suite, receipt_path):
        index = len(calls)
        summary = summaries[index]
        target = Path(receipt_path)
        if not target.is_absolute():
            target = Path(project_root) / target
        receipt = _receipt()
        receipt["test_summary"] = summary
        receipt["suite"] = suite
        # stdoutの数値はsummaryとわざと食い違わせる。出力文字列を読まないことの確認。
        receipt["stdout"] = "999 passed in 1.00s\n"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
        calls.append({"suite": suite, "receipt_path": str(receipt_path)})
        return SimpleNamespace(
            status="passed", exit_code=0, receipt_path=str(target)
        )

    return execute


def _summary(passed):
    return {
        "passed": passed, "failed": 0, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "errors": 0, "total": passed,
    }


def _cli(update_path, root, *arguments, execute=None):
    return update_path.main(
        [
            "--project-root", str(root),
            "--todo", "TODO_NEXT_SESSION.md",
            *arguments,
        ],
        execute=execute,
    )


def test_cli_updates_the_full_test_line_from_the_first_receipt(
    update_path, tmp_path, capsys
):
    root, todo = _cli_workspace(tmp_path)
    before = todo.read_text(encoding="utf-8")
    calls = []

    exit_code = _cli(
        update_path, root,
        "--first-receipt", "records/development/first.json",
        "--final-receipt", "records/development/final.json",
        execute=_fake_execute([_summary(7), _summary(7)], calls=calls),
    )

    assert exit_code == 0
    assert len(calls) == 2
    assert calls[0]["receipt_path"] == "records/development/first.json"
    assert calls[1]["receipt_path"] == "records/development/final.json"

    after = todo.read_text(encoding="utf-8")
    assert f"{FULL_TEST_PREFIX}venv公式runner `7 passed`" in after
    assert "999" not in after, "stdoutの数値を読まない"
    assert "852 passed" not in after

    # 自由文、link label／path、関連Test行は変わらない。
    for line in before.splitlines():
        if line.startswith(FULL_TEST_PREFIX):
            continue
        assert line in after.splitlines()

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "updated"
    assert output["first_receipt"] == "records/development/first.json"
    assert output["final_receipt"] == "records/development/final.json"
    assert output["test_summary"] == _summary(7)


def test_cli_requires_every_path_argument(update_path, tmp_path):
    root, _todo = _cli_workspace(tmp_path)

    for arguments in (
        ["--first-receipt", "records/development/a.json"],
        ["--final-receipt", "records/development/b.json"],
        [],
    ):
        with pytest.raises(SystemExit):
            update_path.main(
                ["--project-root", str(root), "--todo", "TODO_NEXT_SESSION.md", *arguments],
                execute=lambda **kwargs: None,
            )

    with pytest.raises(SystemExit):
        update_path.main(
            [
                "--project-root", str(root),
                "--first-receipt", "records/development/a.json",
                "--final-receipt", "records/development/b.json",
            ],
            execute=lambda **kwargs: None,
        )


def test_cli_rejects_unsafe_paths_without_touching_anything(
    update_path, tmp_path, capsys
):
    root, todo = _cli_workspace(tmp_path)
    before = todo.read_bytes()
    (root / "linked.md").symlink_to(todo)

    cases = {
        "絶対path receipt": ("records/development/a.json", str(root / "final.json")),
        "親への脱出": ("records/development/a.json", "records/development/../../final.json"),
        "development外": ("records/development/a.json", "records/final.json"),
        "json以外": ("records/development/a.json", "records/development/final.txt"),
    }
    for label, (first, final) in cases.items():
        calls = []
        exit_code = _cli(
            update_path, root,
            "--first-receipt", first, "--final-receipt", final,
            execute=_fake_execute([_summary(1), _summary(1)], calls=calls),
        )
        output = json.loads(capsys.readouterr().out)
        assert exit_code != 0, label
        assert output["status"] == "stopped", label
        assert output["code"] == "receipt_path_invalid", label
        assert calls == [], label
        assert todo.read_bytes() == before, label
        assert not (root / "records" / "development" / "a.json").exists(), label

    # TODO側のpath異常も同様に止まる。
    for label, todo_argument in {
        "絶対path": str(todo),
        "親への脱出": "../TODO_NEXT_SESSION.md",
        "symlink": "linked.md",
    }.items():
        calls = []
        exit_code = update_path.main(
            [
                "--project-root", str(root),
                "--todo", todo_argument,
                "--first-receipt", "records/development/a.json",
                "--final-receipt", "records/development/b.json",
            ],
            execute=_fake_execute([_summary(1), _summary(1)], calls=calls),
        )
        output = json.loads(capsys.readouterr().out)
        assert exit_code != 0, label
        assert output["code"] == "todo_path_invalid", label
        assert calls == [], label
        assert todo.read_bytes() == before, label


def test_cli_restores_the_todo_when_the_two_runs_disagree(
    update_path, tmp_path, capsys
):
    root, todo = _cli_workspace(tmp_path)
    before = todo.read_bytes()
    calls = []

    exit_code = _cli(
        update_path, root,
        "--first-receipt", "records/development/first.json",
        "--final-receipt", "records/development/final.json",
        execute=_fake_execute([_summary(7), _summary(8)], calls=calls),
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code != 0
    assert output["status"] == "stopped"
    assert output["code"] == "receipt_summary_mismatch"
    assert len(calls) == 2
    assert todo.read_bytes() == before


def test_cli_never_calls_git(update_path):
    """CLIはGitを呼ばない。散文の語ではなく、実際の呼出し手段が無いことを見る。"""

    source = Path(update_path.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "subprocess", '"git"', "'git'", "os.system", "shell=True", "Popen",
    ):
        assert forbidden not in source


# ------------------------------------------------- transaction境界（例外復元）
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-repair-todo-update-transaction-boundary.md
#
# 一時receiptで書き始めた後、最終receiptの検証が成功するまで更新は確定しない。
# `Exception`を継承する失敗ではTODOを必ず元bytesへ戻す。


def _raising_phases(*, fail_on, error=None):
    """指定した段で例外を送出する実行器。呼出し順を記録する。"""

    calls = []

    def run_official_tests(phase):
        calls.append(phase)
        if phase == fail_on:
            raise error or RuntimeError(f"{phase} run unavailable")
        return _receipt(7)

    run_official_tests.calls = calls
    return run_official_tests


def test_second_run_exception_restores_the_todo(update_path, tmp_path):
    root, todo = _issue_workspace(tmp_path)
    before = todo.read_bytes()
    runner = _raising_phases(fail_on="second")

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root, todo_path=todo, run_official_tests=runner
        )

    assert runner.calls == ["first", "second"]
    assert todo.read_bytes() == before, "最終確認まで更新は確定しない"
    assert error.value.code in update_path.STOP_CODES


def test_first_run_exception_never_touches_the_todo(update_path, tmp_path):
    root, todo = _issue_workspace(tmp_path)
    before = todo.read_bytes()
    runner = _raising_phases(fail_on="first")

    with pytest.raises(update_path.TodoUpdatePathError) as error:
        update_path.run_two_phase_update(
            project_root=root, todo_path=todo, run_official_tests=runner
        )

    assert runner.calls == ["first"], "1回目が失敗したら2回目を呼ばない"
    assert todo.read_bytes() == before
    assert error.value.code in update_path.STOP_CODES


def test_unexpected_exception_inside_the_update_restores_the_todo(
    update_path, tmp_path
):
    root, todo = _issue_workspace(tmp_path)
    before = todo.read_bytes()
    runner = _phases(_receipt(7), _receipt(7))

    def exploding_verify(path, project_root):
        raise ValueError("verifier exploded")

    with pytest.raises(update_path.TodoUpdatePathError):
        update_path.run_two_phase_update(
            project_root=root, todo_path=todo, run_official_tests=runner,
            verify=exploding_verify,
        )

    assert todo.read_bytes() == before


def test_keyboard_interrupt_is_not_swallowed(update_path, tmp_path):
    """`KeyboardInterrupt`と`SystemExit`は捕捉しない。"""

    root, todo = _issue_workspace(tmp_path)
    runner = _raising_phases(fail_on="second", error=KeyboardInterrupt())

    with pytest.raises(KeyboardInterrupt):
        update_path.run_two_phase_update(
            project_root=root, todo_path=todo, run_official_tests=runner
        )

    source = Path(update_path.__file__).read_text(encoding="utf-8")
    assert "except BaseException" not in source


def _unreadable_final_execute(calls, *, missing_phase="second"):
    """2回目のreceipt fileを読めない状態にする実行器。"""

    def execute(*, config, project_root, suite, receipt_path):
        index = len(calls)
        target = Path(project_root) / receipt_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if index == (1 if missing_phase == "second" else 0):
            calls.append({"receipt_path": str(receipt_path)})
            # pathは返すが、fileを作らない。
            return SimpleNamespace(
                status="passed", exit_code=0, receipt_path=str(target)
            )
        receipt = _receipt(7)
        target.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
        calls.append({"receipt_path": str(receipt_path)})
        return SimpleNamespace(status="passed", exit_code=0, receipt_path=str(target))

    return execute


def test_unreadable_final_receipt_restores_the_todo(update_path, tmp_path, capsys):
    root, todo = _cli_workspace(tmp_path)
    before = todo.read_bytes()
    calls = []

    exit_code = _cli(
        update_path, root,
        "--first-receipt", "records/development/first.json",
        "--final-receipt", "records/development/final.json",
        execute=_unreadable_final_execute(calls),
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code != 0
    assert output["status"] == "stopped"
    assert len(calls) == 2
    assert todo.read_bytes() == before


def test_cli_reports_a_second_run_exception_as_a_stop(update_path, tmp_path, capsys):
    root, todo = _cli_workspace(tmp_path)
    before = todo.read_bytes()
    calls = []

    def exploding_execute(*, config, project_root, suite, receipt_path):
        calls.append(str(receipt_path))
        if len(calls) == 2:
            raise RuntimeError("second run unavailable")
        target = Path(project_root) / receipt_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(_receipt(7), ensure_ascii=False), encoding="utf-8"
        )
        return SimpleNamespace(status="passed", exit_code=0, receipt_path=str(target))

    exit_code = _cli(
        update_path, root,
        "--first-receipt", "records/development/first.json",
        "--final-receipt", "records/development/final.json",
        execute=exploding_execute,
    )

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert exit_code != 0
    assert output["status"] == "stopped"
    assert "Traceback" not in captured.out
    assert len(calls) == 2
    assert todo.read_bytes() == before


class TestSecondReceiptIsVerified:
    """F-C3・F-C4・F-C5反証：二段確認の偽造・差替え・改行破壊を許さない。"""

    def _module(self):
        import importlib

        return importlib.import_module("tools.development.todo_update_path")

    def _receipt(self, **overrides):
        receipt = {
            "receipt_kind": "policy_test_verification_run",
            "runner_id": "RC3-DEVELOPMENT-TEST-RUNNER",
            "suite": "full",
            "python_version": "3.9.6",
            "pytest_version": "8.4.2",
            "fallback_used": False,
            "status": "passed",
            "exit_code": 0,
            "test_summary": {
                "passed": 10, "failed": 0, "skipped": 0, "xfailed": 0,
                "xpassed": 0, "errors": 0, "total": 10,
            },
        }
        receipt.update(overrides)
        return receipt

    def test_unknown_receipt_kind_is_rejected(self):
        """U1：未知kindの第2receiptを受理しない。"""
        module = self._module()
        with pytest.raises(module.TodoUpdatePathError):
            module.compare_receipts(
                self._receipt(), self._receipt(receipt_kind="forged")
            )

    def test_nonzero_exit_code_is_rejected(self):
        """U1：exit code 9の第2receiptを受理しない。"""
        module = self._module()
        with pytest.raises(module.TodoUpdatePathError):
            module.compare_receipts(self._receipt(), self._receipt(exit_code=9))

    def test_boolean_and_integer_are_not_equal(self):
        """U1：`False == 0`や整数同値の浮動小数を一致としない。"""
        module = self._module()
        with pytest.raises(module.TodoUpdatePathError):
            module.compare_receipts(
                self._receipt(), self._receipt(fallback_used=0)
            )
        forged = self._receipt()
        summary = dict(forged["test_summary"])
        summary["passed"] = 10.0
        with pytest.raises(module.TodoUpdatePathError):
            module.compare_receipts(
                self._receipt(), self._receipt(test_summary=summary)
            )

    def test_matching_receipts_still_compare_equal(self):
        module = self._module()
        assert module.compare_receipts(self._receipt(), self._receipt()) is True

    def test_todo_swapped_after_verification_is_detected(
        self, tmp_path, monkeypatch
    ):
        """U3：確認後にTODOを差し替えても確定させない。

        候補生成は本反証の対象ではないため差し替え、`run_two_phase_update`の
        transaction境界だけを検査する（別理由での失敗と取り違えない）。
        """

        module = self._module()
        generation = importlib.import_module(
            "tools.development.todo_record_generation"
        )
        todo_path = tmp_path / "TODO_NEXT_SESSION.md"
        todo_path.write_bytes(b"original\n")
        candidate = b"candidate\n"
        monkeypatch.setattr(
            generation, "build_todo_candidate", lambda **kwargs: candidate
        )
        receipts = iter([self._receipt(), self._receipt()])

        def run_official_tests(phase):
            if phase == "second":
                todo_path.write_bytes(b"swapped after verification\n")
            return next(receipts)

        with pytest.raises(module.TodoUpdatePathError):
            module.run_two_phase_update(
                project_root=tmp_path,
                todo_path=todo_path,
                run_official_tests=run_official_tests,
                verify=lambda path, root: True,
            )
        assert todo_path.read_bytes() == b"original\n"
