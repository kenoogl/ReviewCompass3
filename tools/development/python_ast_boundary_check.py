"""Python sourceに現れる操作を、ASTで検査する。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-repair-task-python-cache-ast-boundary-check.md
改善候補：records/development/
          2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md

禁止語をsource文字列から部分一致で探す検査は、正しい公開関数名`bytecode_environment`の中の
`environ`まで違反として拾い、逆にaliasを使った本物の違反を見逃していた。
誤検知と見逃しの両方を持つ検査だった。

このmoduleは、文字の出現ではなくAST（抽象構文木。sourceを構文として解析した木）に現れる
操作を見る。import束縛を辿って別名を解決し、次の操作だけを検出する。

- 実行中processの環境への接触
- fileとdirectoryの削除
- 時間に基づく判断

これは**検査器**であり、実行器ではない。標準ライブラリ`ast`だけを使う決定的な解析であり、
外部process、network、filesystemへの書込みを持たない。

扱う範囲の境界を明示する。import束縛から辿れる名前だけを解決し、変数へ入れ替えた後の値や、
実行時にしか決まらない呼出しは推測しない。列挙した操作を正確に扱うことだけを引き受ける。
"""

import ast
from tools.common.errors import FailClosedError


#: 参照そのものを違反とする操作。呼び出さずに受け渡すだけでも同じ能力を持つ。
WATCHED_PATHS = frozenset(
    {
        "os.environ",
        "os.putenv",
        "os.remove",
        "os.rmdir",
        "os.unlink",
        "shutil.rmtree",
        "time.time",
        "datetime.datetime.now",
    }
)

#: 生成した直後に削除methodを呼ぶ形だけを見る対象。
PATH_CONSTRUCTOR = "pathlib.Path"
PATH_REMOVAL_METHODS = {"unlink": "pathlib.Path.unlink"}

STOP_CODES = ("source_invalid", "source_unparsable")


class PythonAstBoundaryError(FailClosedError):
    """sourceを構文として解析できない。判断できないので続行しない。"""


def inspect_python_source_boundaries(source):
    """検出した操作の正規化名を、重複なくソートしたtupleで返す。

    行や列の位置は結果へ持ち込まない。同じ操作が何度現れても1件である。
    """

    if not isinstance(source, str):
        raise PythonAstBoundaryError("source_invalid", repr(type(source)))
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError) as error:
        raise PythonAstBoundaryError("source_unparsable", str(error)) from error

    bindings = _collect_import_bindings(tree)
    findings = set()
    for node in ast.walk(tree):
        canonical = _canonical_name(node, bindings)
        if canonical in WATCHED_PATHS:
            findings.add(canonical)
        removal = _path_removal_operation(node, bindings)
        if removal is not None:
            findings.add(removal)
    return tuple(sorted(findings))


def _collect_import_bindings(tree):
    """module内の名前が、どのimport元を指すかを集める。

    `import os as runtime_os`は`runtime_os`を`os`へ、`from os import environ`は
    `environ`を`os.environ`へ結び付ける。相対importと`*`は解決しない。
    """

    bindings = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    bindings[alias.asname] = alias.name
                else:
                    top_level = alias.name.split(".")[0]
                    bindings[top_level] = top_level
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                continue
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                bindings[alias.asname or alias.name] = f"{module}.{alias.name}"
    return bindings


def _canonical_name(node, bindings):
    """名前と属性の連なりを、import元からの正規化名へ直す。

    束縛が辿れない名前はNoneを返す。部分一致では判断しない。
    """

    if isinstance(node, ast.Name):
        return bindings.get(node.id)
    if isinstance(node, ast.Attribute):
        parent = _canonical_name(node.value, bindings)
        if parent is None:
            return None
        return f"{parent}.{node.attr}"
    return None


def _path_removal_operation(node, bindings):
    """`Path(...)`を作ってすぐ削除methodを呼ぶ形を見る。"""

    if not isinstance(node, ast.Call):
        return None
    function = node.func
    if not isinstance(function, ast.Attribute):
        return None
    operation = PATH_REMOVAL_METHODS.get(function.attr)
    if operation is None:
        return None
    receiver = function.value
    if not isinstance(receiver, ast.Call):
        return None
    if _canonical_name(receiver.func, bindings) != PATH_CONSTRUCTOR:
        return None
    return operation
