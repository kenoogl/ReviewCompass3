"""Python sourceの操作境界をASTで検査する検査器の受入Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-repair-task-python-cache-ast-boundary-check.md
候補：records/development/
      2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md

禁止語の部分一致は、正しい識別子`bytecode_environment`の中の`environ`まで違反にした。
検査するのは文字の出現ではなく、AST（抽象構文木。sourceを構文として解析した木）に現れる操作である。
"""

import ast
import importlib
import textwrap
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
CACHE_MODULE_PATH = PROJECT_ROOT / "tools" / "development" / "task_python_cache.py"


@pytest.fixture
def checker():
    return importlib.import_module("tools.development.python_ast_boundary_check")


def _inspect(checker, source):
    return checker.inspect_python_source_boundaries(textwrap.dedent(source))


# -------------------------------------------------- 誤検知しないことの固定


def test_correct_identifier_is_not_a_violation(checker):
    """`bytecode_environment`という正しい名前を違反にしない。"""

    findings = _inspect(
        checker,
        '''
        """実行中processの環境は変更しない。os.environへは触れない。"""

        BYTECODE_VARIABLE = "PYTHONPYCACHEPREFIX"


        def bytecode_environment(resolution):
            """環境mappingを返すだけの関数である。"""

            return {BYTECODE_VARIABLE: str(resolution.task_directory)}
        ''',
    )

    assert findings == ()


def test_unrelated_names_and_attributes_are_not_violations(checker):
    findings = _inspect(
        checker,
        """
        import time
        import os.path


        def run(values):
            time.sleep(0)
            return os.path.join(*values)
        """,
    )

    assert findings == ()


# -------------------------------------------------- 実行中processの環境


@pytest.mark.parametrize(
    "body",
    [
        "value = os.environ",
        "value = os.environ['PATH']",
        "os.environ['PYTHONPYCACHEPREFIX'] = '/tmp/x'",
        "os.environ.update({'A': 'B'})",
    ],
)
def test_process_environment_access_is_detected(checker, body):
    findings = _inspect(checker, f"import os\n\n\ndef run():\n    {body}\n")

    assert "os.environ" in findings


def test_aliased_module_and_from_import_are_detected(checker):
    aliased = _inspect(
        checker,
        """
        import os as runtime_os


        def run():
            runtime_os.environ['A'] = 'B'
        """,
    )
    from_import = _inspect(
        checker,
        """
        from os import environ


        def run():
            environ['A'] = 'B'
        """,
    )

    assert "os.environ" in aliased
    assert "os.environ" in from_import


# -------------------------------------------------- 削除と環境書換えの呼出し


@pytest.mark.parametrize(
    "statement,expected",
    [
        ("os.putenv('A', 'B')", "os.putenv"),
        ("os.remove('a')", "os.remove"),
        ("os.rmdir('a')", "os.rmdir"),
        ("os.unlink('a')", "os.unlink"),
    ],
)
def test_os_level_removal_calls_are_detected(checker, statement, expected):
    findings = _inspect(checker, f"import os\n\n\ndef run():\n    {statement}\n")

    assert expected in findings


def test_tree_removal_call_is_detected(checker):
    findings = _inspect(
        checker,
        """
        import shutil


        def run(target):
            shutil.rmtree(target)
        """,
    )

    assert "shutil.rmtree" in findings


def test_path_removal_call_is_detected(checker):
    direct = _inspect(
        checker,
        """
        from pathlib import Path


        def run(target):
            Path(target).unlink()
        """,
    )
    aliased = _inspect(
        checker,
        """
        from pathlib import Path as P


        def run(target):
            P(target).unlink()
        """,
    )

    assert "pathlib.Path.unlink" in direct
    assert "pathlib.Path.unlink" in aliased


# -------------------------------------------------- 時間ベースの判断


def test_time_based_calls_are_detected(checker):
    """時間ベースの保持・削除判断をこの最小moduleへ入れない境界の検査である。"""

    clock = _inspect(
        checker,
        """
        import time


        def run():
            return time.time()
        """,
    )
    calendar = _inspect(
        checker,
        """
        import datetime


        def run():
            return datetime.datetime.now()
        """,
    )
    from_import = _inspect(
        checker,
        """
        from datetime import datetime


        def run():
            return datetime.now()
        """,
    )

    assert "time.time" in clock
    assert "datetime.datetime.now" in calendar
    assert "datetime.datetime.now" in from_import


# -------------------------------------------------- 結果の形と失敗の扱い


def test_result_is_a_sorted_immutable_value_without_position(checker):
    first = _inspect(
        checker,
        """
        import os
        import shutil


        def run(target):
            shutil.rmtree(target)
            os.remove(target)
        """,
    )
    reordered = _inspect(
        checker,
        """
        import os
        import shutil


        def run(target):
            os.remove(target)

            shutil.rmtree(target)
        """,
    )

    assert isinstance(first, tuple)
    assert list(first) == sorted(first)
    assert first == ("os.remove", "shutil.rmtree")
    assert first == reordered, "行位置は結果の同一性へ持ち込まない"


def test_repeated_operations_are_reported_once(checker):
    findings = _inspect(
        checker,
        """
        import os


        def run():
            os.remove('a')
            os.remove('b')
        """,
    )

    assert findings == ("os.remove",)


def test_unparsable_source_raises_instead_of_returning(checker):
    with pytest.raises(checker.PythonAstBoundaryError) as error:
        checker.inspect_python_source_boundaries("def broken(:\n")

    assert error.value.code == "source_unparsable"


# -------------------------------------------------- 検査器そのものの性質


def test_checker_uses_only_the_standard_ast_module(checker):
    """外部process、network、filesystem書込みを持たない決定的な解析である。"""

    tree = ast.parse(Path(checker.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])

    assert imported == {"ast"}


# -------------------------------------------------- 実際の対象module


def test_current_task_python_cache_module_has_no_findings(checker):
    source = CACHE_MODULE_PATH.read_text(encoding="utf-8")

    assert checker.inspect_python_source_boundaries(source) == ()
