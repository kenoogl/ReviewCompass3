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

STOP_CODES = (
    "todo_candidate_failed",
    "todo_write_failed",
    "todo_read_back_mismatch",
    "todo_verification_failed",
    "receipt_summary_mismatch",
    "todo_restore_failed",
    "issue_root_invalid",
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


def run_two_phase_update(
    *, project_root, todo_path, run_official_tests, verify=None, write=None
):
    """一時receiptで書き、最終receiptで確定する。失敗したら原状へ戻す。"""

    verify = verify or default_verify
    write = write or atomic_write
    todo_path = Path(todo_path)
    original = todo_path.read_bytes()

    first_receipt = run_official_tests("first")
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

        second_receipt = run_official_tests("second")
        compare_receipts(first_receipt, second_receipt)
    except TodoUpdatePathError:
        _restore(todo_path, original)
        raise

    return {
        "todo_bytes": candidate,
        "first_receipt": first_receipt,
        "second_receipt": second_receipt,
    }


def _restore(todo_path, original):
    try:
        atomic_write(todo_path, original)
    except OSError as error:  # pragma: no cover - 復帰不能は停止条件そのもの
        raise TodoUpdatePathError("todo_restore_failed", str(error)) from error
    if Path(todo_path).read_bytes() != original:  # pragma: no cover
        raise TodoUpdatePathError("todo_restore_failed", str(todo_path))
