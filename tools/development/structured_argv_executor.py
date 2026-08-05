"""読み取り専用の構造化argv executor（最小slice）。

正本設計：docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md の§2.1と§3.2
承認：`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`

## 何をするか

argvを**配列のまま**渡して読み取り専用の操作を起動する経路を提供する。shell文字列へ組み立てない。

起動できるのは、次の両方を満たす場合だけである。

1. inventoryの**全操作が`read_only`**であること。
2. 各操作のargvが`git status --porcelain`templateに一致すること。
   `--`の後ろにpathspecを0個以上置ける。それ以外の形は受理しない。

## 何をしないか

- 権限の判定・付与・再分類をしない。inventoryとpreflightは`operation_routing`のものをそのまま使う。
- cache rootの設定、環境変数の設定、既存呼出しの置換をしない。
- Git metadataへの書込み、project成果物への書込み、external操作を起動しない。
- shellを経由しない。shell解釈を有効にする実行optionも使わない。

## runnerの契約

`runner(argv, cwd=cwd)`の形で呼ぶ。`argv`はlist、`cwd`は検証済みの絶対pathである。
戻り値は`returncode`を持つmapping、または同名の属性を持つobjectとする。
runnerは呼出し側が渡す。既定のrunnerは持たない。実processを起動したい場合は
`subprocess_runner`を明示的に渡す。

## 停止

入力、template、cwd、分類、preflightのいずれで失敗しても、**runnerを一度も呼ばない**。
processの実行結果が失敗であることは入力の失敗と区別し、例外にせずreceiptへ記録する。
"""

from pathlib import Path

from tools.development import operation_routing


#: 起動を許す唯一の実行template。この後ろに`--`とpathspecを0個以上置ける。
READ_ONLY_TEMPLATE = ("git", "status", "--porcelain")

#: pathspecを区切る語。
PATHSPEC_SEPARATOR = "--"

STOP_CODES = (
    "inventory_not_read_only",
    "template_mismatch",
    "argv_invalid",
    "cwd_invalid",
    "runner_result_invalid",
)


class StructuredArgvExecutorError(Exception):
    """読み取り専用argv executorのfail-closed条件に触れた。"""

    def __init__(self, code, detail=None):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _validate_argv(argv):
    """argvの形を確かめる。要素は文字列で、実行fileは空でない。"""

    if not isinstance(argv, list) or not argv:
        raise StructuredArgvExecutorError("argv_invalid", "empty argv")
    if any(not isinstance(item, str) for item in argv):
        raise StructuredArgvExecutorError("argv_invalid", "non-text element")
    if not argv[0].strip():
        raise StructuredArgvExecutorError("argv_invalid", "empty executable")
    return argv


def _validate_template(argv):
    """`git status --porcelain`＋任意の`-- <pathspec...>`だけを受理する。

    pathspecは空文字列でもよい。区切りより前に余分な引数を置けない。
    """

    head = tuple(argv[: len(READ_ONLY_TEMPLATE)])
    if head != READ_ONLY_TEMPLATE:
        # 診断用でもargvを文字列へ結合しない。listのまま示す。
        raise StructuredArgvExecutorError("template_mismatch", repr(argv[:4]))
    rest = argv[len(READ_ONLY_TEMPLATE):]
    if not rest:
        return argv
    if rest[0] != PATHSPEC_SEPARATOR:
        raise StructuredArgvExecutorError("template_mismatch", rest[0])
    if PATHSPEC_SEPARATOR in rest[1:]:
        raise StructuredArgvExecutorError("template_mismatch", "duplicated separator")
    return argv


def _validate_read_only(inventory):
    """全操作が`read_only`である場合だけ通す。"""

    for operation in inventory["operations"]:
        if operation["classification"] != "read_only":
            raise StructuredArgvExecutorError(
                "inventory_not_read_only", operation["operation_id"]
            )
    return True


def resolve_working_directory(project_root, cwd):
    """project root基準の相対pathだけを受け、実在する通常directoryへ解決する。"""

    if not isinstance(cwd, str) or not cwd:
        raise StructuredArgvExecutorError("cwd_invalid", str(cwd))
    candidate = Path(cwd)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise StructuredArgvExecutorError("cwd_invalid", cwd)
    root = Path(project_root).resolve()
    target = root / candidate
    if target.is_symlink():
        raise StructuredArgvExecutorError("cwd_invalid", cwd)
    try:
        resolved = target.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise StructuredArgvExecutorError("cwd_invalid", cwd) from error
    if resolved != target.absolute() and resolved != target:
        raise StructuredArgvExecutorError("cwd_invalid", cwd)
    if not resolved.is_dir():
        raise StructuredArgvExecutorError("cwd_invalid", cwd)
    return resolved


def _result_returncode(result):
    if isinstance(result, dict):
        if "returncode" not in result:
            raise StructuredArgvExecutorError("runner_result_invalid", "returncode")
        code = result["returncode"]
    else:
        code = getattr(result, "returncode", None)
    if not isinstance(code, int) or isinstance(code, bool):
        raise StructuredArgvExecutorError("runner_result_invalid", str(code))
    return code


def run_read_only_operations(
    *, inventory, host_attestation, project_root, cwd=".", runner
):
    """検証を通った読み取り専用操作だけを起動し、execution receiptを返す。

    権限の判定はしない。inventoryとpreflightは`operation_routing`のものをそのまま使う。
    """

    try:
        operation_routing.validate_operation_inventory(inventory)
    except operation_routing.OperationRoutingError as error:
        raise StructuredArgvExecutorError(error.code, error.detail) from error

    _validate_read_only(inventory)
    for operation in inventory["operations"]:
        _validate_template(_validate_argv(operation["argv"]))

    working_directory = resolve_working_directory(project_root, cwd)

    def _execute(operation):
        result = runner(list(operation["argv"]), cwd=working_directory)
        returncode = _result_returncode(result)
        return {
            "status": "completed" if returncode == 0 else "failed",
            "detail": f"{operation['operation_id']}: exit code {returncode}",
        }

    try:
        return operation_routing.execute_with_preflight(
            inventory=inventory,
            host_attestation=host_attestation,
            execute=_execute,
        )
    except operation_routing.OperationRoutingError as error:
        raise StructuredArgvExecutorError(error.code, error.detail) from error


def subprocess_runner(argv, *, cwd):
    """実processを起動するrunner。呼出し側が明示的に渡した場合だけ使われる。

    argvはlistのまま渡す。shellを経由しない。
    """

    import subprocess

    completed = subprocess.run(
        argv, cwd=str(cwd), capture_output=True, text=True, check=False
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
