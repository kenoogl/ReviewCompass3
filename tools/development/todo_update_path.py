"""root TODOの更新経路。二段確認で数値と実状態を食い違わせない。

正本設計：docs/design/2026-08-05-record-generation-issue-plan-proposal.md
承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りだけ）

手順は次で固定する。

1. code／Test変更後に公式全Testを一度実行し、**一時receipt**を得る。
2. 一時receiptからroot TODOの候補を機械生成し、atomic writeする。
   自由文、link label、link path、順序は変えない。
3. TODO validator、TODO compaction validator、参照Digest照合、read-back byte一致を通す。
4. 公式全Testを二度目に実行し、commitへ入れる**最終receipt**を得る。
5. 二つのreceiptの集計、suite、Python版、pytest版、fallback、statusが完全一致することを照合する。

どこかで失敗したら、root TODOを更新前のbytesへ戻して停止する。原状復帰できない場合も停止する。
このmoduleはGit操作をしない。commitするかどうかは呼び出す側の判断である。
"""

import json
import os
import re
from pathlib import Path

from tools.development import todo_compaction
from tools.development import todo_handoff
from tools.development import todo_record_generation


#: 二段確認で完全一致を要求するfield。
COMPARED_FIELDS = (
    "test_summary",
    "suite",
    "python_version",
    "pytest_version",
    "fallback_used",
    "status",
)

#: active IDの許可一覧を得る正本root。TODO本文は正本にしない。
ISSUE_ROOTS = (
    ".reviewcompass/workflow/issues",
    ".reviewcompass/workflow/issues-v4",
)

#: record_kindごとに、IDを読むfield。未知のrecord_kindは停止する。
ISSUE_ID_FIELDS = {
    "issue_record": "issue_id",
    "issue": "record_id",
}

_ISSUE_ID = re.compile(r"ISSUE-[A-Z0-9]+(?:-[A-Z0-9]+)*")

#: CLIがreceiptを置いてよい唯一のdirectory。
RECEIPT_ROOT = "records/development"

STOP_CODES = (
    "official_test_failed",
    "todo_update_failed",
    "todo_candidate_failed",
    "todo_write_failed",
    "todo_read_back_mismatch",
    "todo_verification_failed",
    "receipt_summary_mismatch",
    "todo_restore_failed",
    "issue_root_invalid",
    "todo_path_invalid",
    "receipt_path_invalid",
    "config_load_failed",
)


class TodoUpdatePathError(Exception):
    """root TODOの更新経路を安全に完了できない。"""

    def __init__(self, code, detail=None):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def atomic_write(path, data):
    """同じdirectoryへ書いてから一度で置き換える。"""

    target = Path(path)
    temporary = target.with_name(target.name + ".candidate")
    temporary.write_bytes(data)
    os.replace(temporary, target)
    return target


def compare_receipts(first, second):
    """二つのreceiptが同じ実行結果を示すかを照合する。"""

    for field in COMPARED_FIELDS:
        if first.get(field) != second.get(field):
            raise TodoUpdatePathError("receipt_summary_mismatch", field)
    return True


def load_known_active_issue_ids(project_root):
    """許可するactive IDを、project内の既存Issue正本からだけ得る。

    TODO本文は正本にしない。root直下の通常`.json`だけを読み、symlink、JSON不正、
    未知のrecord_kind、IDの欠落・重複・不正では停止する。別directoryは拾わない。
    """

    root = Path(project_root)
    known = set()
    for relative in ISSUE_ROOTS:
        directory = root / relative
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.json")):
            if path.is_symlink() or not path.is_file():
                raise TodoUpdatePathError("issue_root_invalid", str(path))
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError, UnicodeDecodeError) as error:
                raise TodoUpdatePathError("issue_root_invalid", str(path)) from error
            if not isinstance(record, dict):
                raise TodoUpdatePathError("issue_root_invalid", str(path))
            field = ISSUE_ID_FIELDS.get(record.get("record_kind"))
            if field is None:
                raise TodoUpdatePathError(
                    "issue_root_invalid", f"{path}: {record.get('record_kind')}"
                )
            issue_id = record.get(field)
            if not isinstance(issue_id, str) or not _ISSUE_ID.fullmatch(issue_id):
                raise TodoUpdatePathError("issue_root_invalid", f"{path}: {issue_id}")
            if issue_id in known:
                raise TodoUpdatePathError("issue_root_invalid", f"{path}: {issue_id}")
            known.add(issue_id)
    if not known:
        raise TodoUpdatePathError("issue_root_invalid", "no issue record")
    return known


def default_verify(todo_path, project_root):
    """repositoryの既存validatorと、Evidence節に限定したDigest照合を通す。"""

    document = Path(todo_path).read_bytes()
    stable = todo_handoff.validate_commit_stable_git_section(
        document.decode("utf-8")
    )
    if stable.status != "passed":
        raise TodoUpdatePathError(
            "todo_verification_failed", ",".join(stable.findings)
        )
    todo_compaction.validate_compacted_todo(
        document,
        project_root=project_root,
        known_active_ids=load_known_active_issue_ids(project_root),
    )
    todo_record_generation.verify_reference_digests(
        document.decode("utf-8"), project_root=project_root
    )
    return True


def _run_official_phase(run_official_tests, phase):
    """公式Test実行とreceipt取得の失敗を、意味の分かるstop codeへ正規化する。

    `KeyboardInterrupt`と`SystemExit`は`Exception`を継承しないので捕捉しない。
    """

    try:
        return run_official_tests(phase)
    except TodoUpdatePathError:
        raise
    except Exception as error:
        raise TodoUpdatePathError(
            "official_test_failed", f"{phase}: {error}"
        ) from error


def run_two_phase_update(
    *, project_root, todo_path, run_official_tests, verify=None, write=None
):
    """一時receiptで書き、最終receiptで確定する。失敗したら原状へ戻す。

    TODOを書き始めてから確定するまでを一つのtransactionとして扱う。`Exception`を
    継承する失敗はすべて原状復帰の対象である。1回目の公式Testが失敗した段階では
    まだ何も書いていないので、復帰のためのwriteもしない。
    """

    verify = verify or default_verify
    write = write or atomic_write
    todo_path = Path(todo_path)
    original = todo_path.read_bytes()

    # ここで失敗してもTODOは一度も書き換わっていない。復元は行わない。
    first_receipt = _run_official_phase(run_official_tests, "first")
    try:
        try:
            candidate = todo_record_generation.build_todo_candidate(
                todo_path=todo_path,
                receipt=first_receipt,
                project_root=project_root,
            )
        except todo_record_generation.TodoRecordGenerationError as error:
            raise TodoUpdatePathError("todo_candidate_failed", error.code) from error

        try:
            write(todo_path, candidate)
        except OSError as error:
            raise TodoUpdatePathError("todo_write_failed", str(error)) from error

        if todo_path.read_bytes() != candidate:
            raise TodoUpdatePathError("todo_read_back_mismatch", str(todo_path))

        try:
            verify(todo_path, project_root)
        except TodoUpdatePathError:
            raise
        except Exception as error:
            raise TodoUpdatePathError("todo_verification_failed", str(error)) from error

        second_receipt = _run_official_phase(run_official_tests, "second")
        compare_receipts(first_receipt, second_receipt)
    except TodoUpdatePathError:
        _restore(todo_path, original)
        raise
    except Exception as error:
        _restore(todo_path, original)
        raise TodoUpdatePathError("todo_update_failed", str(error)) from error

    return {
        "todo_bytes": candidate,
        "first_receipt": first_receipt,
        "second_receipt": second_receipt,
    }


def _restore(todo_path, original):
    """元bytesと違っていれば戻す。戻せない場合は`todo_restore_failed`で停止する。"""

    try:
        if Path(todo_path).read_bytes() == original:
            return
        atomic_write(todo_path, original)
        restored = Path(todo_path).read_bytes()
    except OSError as error:  # pragma: no cover - 復帰不能は停止条件そのもの
        raise TodoUpdatePathError("todo_restore_failed", str(error)) from error
    if restored != original:  # pragma: no cover
        raise TodoUpdatePathError("todo_restore_failed", str(todo_path))


# ------------------------------------------------------------------ CLI
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-repair-todo-test-projection-cli.md
#
# 二段更新経路を機械処理として起動する入口である。TODO本文を直接編集せず、
# 更新は`run_two_phase_update()`だけを通す。Gitは呼ばない。


def _safe_relative(value, *, project_root, code):
    """project root基準の相対pathだけを受ける。脱出とsymlinkを拒否する。"""

    if not isinstance(value, str) or not value:
        raise TodoUpdatePathError(code, str(value))
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise TodoUpdatePathError(code, value)
    root = Path(project_root).resolve()
    target = root / candidate
    if target.is_symlink():
        raise TodoUpdatePathError(code, value)
    try:
        resolved = target.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise TodoUpdatePathError(code, value) from error
    return target


def validate_todo_argument(value, *, project_root):
    target = _safe_relative(value, project_root=project_root, code="todo_path_invalid")
    if not target.is_file():
        raise TodoUpdatePathError("todo_path_invalid", value)
    return target


def validate_receipt_argument(value, *, project_root):
    """receiptは`records/development/`配下の`.json`だけを許す。"""

    target = _safe_relative(
        value, project_root=project_root, code="receipt_path_invalid"
    )
    relative = Path(value)
    if relative.parent.as_posix() != RECEIPT_ROOT or relative.suffix != ".json":
        raise TodoUpdatePathError("receipt_path_invalid", value)
    if target.is_dir():
        raise TodoUpdatePathError("receipt_path_invalid", value)
    return target


def main(argv=None, *, execute=None):
    """公式Testを2回起動し、二段確認でroot TODOの機械管理部分を更新する。"""

    import argparse

    from tools.development import policy_test_runner

    parser = argparse.ArgumentParser(
        description="公式receiptからTODOの機械管理部分を更新する（Git操作はしない）"
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--todo", required=True)
    parser.add_argument("--first-receipt", required=True)
    parser.add_argument("--final-receipt", required=True)
    parser.add_argument("--config", default="config/development-test-runner.json")
    parser.add_argument("--suite", default="full")
    arguments = parser.parse_args(argv)

    execute = execute or policy_test_runner.execute
    project_root = Path(arguments.project_root).resolve()

    def _report(document):
        print(json.dumps(document, ensure_ascii=False, sort_keys=True))

    try:
        todo_path = validate_todo_argument(
            arguments.todo, project_root=project_root
        )
        first_receipt = validate_receipt_argument(
            arguments.first_receipt, project_root=project_root
        )
        final_receipt = validate_receipt_argument(
            arguments.final_receipt, project_root=project_root
        )
        if first_receipt == final_receipt:
            raise TodoUpdatePathError("receipt_path_invalid", "identical receipts")
    except TodoUpdatePathError as error:
        _report({"status": "stopped", "code": error.code, "detail": error.detail})
        return 2

    try:
        config = policy_test_runner.load_config(project_root / arguments.config)
    except Exception as error:  # TODOはまだ読んでも書いてもいない。
        _report(
            {"status": "stopped", "code": "config_load_failed", "detail": str(error)}
        )
        return 2

    receipts = {"first": arguments.first_receipt, "second": arguments.final_receipt}

    def run_official_tests(phase):
        execution = execute(
            config=config,
            project_root=project_root,
            suite=arguments.suite,
            receipt_path=receipts[phase],
        )
        return json.loads(
            Path(execution.receipt_path).read_text(encoding="utf-8")
        )

    try:
        result = run_two_phase_update(
            project_root=project_root,
            todo_path=todo_path,
            run_official_tests=run_official_tests,
        )
    except TodoUpdatePathError as error:
        _report({"status": "stopped", "code": error.code, "detail": error.detail})
        return 1

    _report(
        {
            "status": "updated",
            "first_receipt": arguments.first_receipt,
            "final_receipt": arguments.final_receipt,
            "test_summary": result["second_receipt"]["test_summary"],
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
