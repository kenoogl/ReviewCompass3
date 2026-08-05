"""TODOの機械管理部分を決定的に作る収集器のAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md
承認：DEC-RECORD-GENERATION-PLAN-001（TODO最小縦切りだけ）

機械が触るのは「直近の全Test」行と、Evidence節のMarkdown linkのSHA-256値だけである。
自由文、link label、link path、行の並びは保持する。見出しと対象行は完全一致でちょうど1回であり、
近傍探索や行番号で書き込まない。
"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


FULL_TEST_PREFIX = "- 直近の全Test："


@pytest.fixture
def generation():
    return importlib.import_module("tools.development.todo_record_generation")


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _receipt(**overrides):
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
            "passed": 863, "failed": 0, "skipped": 0,
            "xfailed": 0, "xpassed": 0, "errors": 0, "total": 863,
        },
        "stdout": "863 passed in 5.44s\n",
        "stderr": "",
    }
    receipt.update(overrides)
    return receipt


def _workspace(tmp_path, *, todo_body=None, references=("first.md", "second.md")):
    root = tmp_path / "project"
    (root / "records").mkdir(parents=True)
    reference_lines = []
    for index, name in enumerate(references, start=1):
        target = root / "records" / name
        target.write_text(f"reference {index}\n", encoding="utf-8")
        reference_lines.append(
            f"- [記録{index}](records/{name}) — SHA-256 `{_sha256(target)}`"
        )
    body = todo_body or """# TODO_NEXT_SESSION

更新日：2026-08-05

## 現在位置

- 全体：人が書いた説明はそのまま残す。
- 補足：この行も機械は触らない。

## 最新のauthority／Evidence

{references}

## 次に行う一作業

人が書いた次の一作業。ここも触らない。

## Git・Test

- branch：`main`
- 直近の関連Test：関連 `11 passed`
- 直近の全Test：venv公式runner `852 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格
"""
    document = body.replace("{references}", "\n".join(reference_lines))
    todo = root / "TODO_NEXT_SESSION.md"
    todo.write_text(document, encoding="utf-8")
    return root, todo


def _candidate(generation, root, todo, receipt=None):
    return generation.build_todo_candidate(
        todo_path=todo, receipt=receipt or _receipt(), project_root=root
    )


def _reject(generation, root, todo, receipt=None):
    before = todo.read_bytes()
    with pytest.raises(generation.TodoRecordGenerationError) as error:
        _candidate(generation, root, todo, receipt)
    assert todo.read_bytes() == before, "停止時にTODOを変えない"
    return error.value.code


# ------------------------------------------------------------------ 正常


def test_candidate_updates_only_the_machine_managed_parts(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    before = todo.read_text(encoding="utf-8")

    candidate = _candidate(generation, root, todo).decode("utf-8")

    assert f"{FULL_TEST_PREFIX}venv公式runner `863 passed`、Python 3.9.6、pytest 8.4.2、fallback false" in candidate
    assert "852 passed" not in candidate

    # 自由文、link label、link path、行の並びは変わらない。
    for line in before.splitlines():
        if line.startswith(FULL_TEST_PREFIX):
            continue
        assert line in candidate.splitlines()
    assert [
        line for line in candidate.splitlines() if line.startswith("- [記録")
    ] == [
        line for line in before.splitlines() if line.startswith("- [記録")
    ]
    assert "- 直近の関連Test：関連 `11 passed`" in candidate
    assert todo.read_bytes() == before.encode("utf-8"), "候補生成でTODOを書かない"


def test_candidate_is_deterministic(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    assert _candidate(generation, root, todo) == _candidate(generation, root, todo)


def test_reference_digests_are_recomputed_from_bytes(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    recorded = generation.collect_reference_digests(
        todo.read_text(encoding="utf-8"), project_root=root
    )
    assert [item["path"] for item in recorded] == [
        "records/first.md", "records/second.md",
    ]
    for item in recorded:
        assert item["sha256"] == _sha256(root / item["path"])
        assert item["sha256"] == item["recorded_sha256"]


# ------------------------------------------------------------------ 改竄


def test_changed_reference_stops_without_touching_the_todo(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    target = root / "records" / "first.md"
    target.write_text(target.read_text(encoding="utf-8") + "x", encoding="utf-8")

    assert _reject(generation, root, todo) == "reference_digest_mismatch"


# ------------------------------------------------------------------ receipt異常


def test_broken_receipts_stop_without_touching_the_todo(generation, tmp_path):
    root, todo = _workspace(tmp_path)

    missing_summary = _receipt()
    del missing_summary["test_summary"]
    assert _reject(generation, root, todo, missing_summary) == "receipt_field_unknown"

    assert _reject(
        generation, root, todo, _receipt(status="failed", exit_code=1)
    ) == "receipt_not_passed"

    assert _reject(
        generation, root, todo, _receipt(fallback_used=True)
    ) == "receipt_fallback_used"

    unknown_field = _receipt()
    unknown_field["reviewer"] = "claude"
    assert _reject(generation, root, todo, unknown_field) == "receipt_field_unknown"

    negative = _receipt()
    negative["test_summary"] = dict(negative["test_summary"], passed=-1)
    assert _reject(generation, root, todo, negative) == "test_summary_invalid"

    inconsistent = _receipt()
    inconsistent["test_summary"] = dict(inconsistent["test_summary"], total=1)
    assert _reject(generation, root, todo, inconsistent) == "test_summary_invalid"

    contradiction = _receipt()
    contradiction["test_summary"] = dict(contradiction["test_summary"], failed=1, total=864)
    assert _reject(generation, root, todo, contradiction) == "receipt_not_passed"

    for field in ("python_version", "pytest_version"):
        blank = _receipt(**{field: ""})
        assert _reject(generation, root, todo, blank) == "receipt_invalid"


def test_old_receipt_without_the_summary_is_not_accepted(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    legacy = _receipt()
    del legacy["test_summary"]
    assert _reject(generation, root, todo, legacy) == "receipt_field_unknown"


# ------------------------------------------------------------------ 構造異常


def test_missing_or_duplicated_structure_stops(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    original = todo.read_text(encoding="utf-8")

    without_heading = original.replace("## Git・Test\n", "")
    todo.write_text(without_heading, encoding="utf-8")
    assert _reject(generation, root, todo) == "todo_heading_invalid"

    duplicated_heading = original + "\n## Git・Test\n"
    todo.write_text(duplicated_heading, encoding="utf-8")
    assert _reject(generation, root, todo) == "todo_heading_invalid"

    without_evidence = original.replace("## 最新のauthority／Evidence\n", "")
    todo.write_text(without_evidence, encoding="utf-8")
    assert _reject(generation, root, todo) == "todo_heading_invalid"

    without_line = "\n".join(
        line for line in original.splitlines() if not line.startswith(FULL_TEST_PREFIX)
    ) + "\n"
    todo.write_text(without_line, encoding="utf-8")
    assert _reject(generation, root, todo) == "todo_line_invalid"

    duplicated_line = original.replace(
        f"{FULL_TEST_PREFIX}venv公式runner",
        f"{FULL_TEST_PREFIX}venv公式runner `1 passed`\n{FULL_TEST_PREFIX}venv公式runner",
        1,
    )
    todo.write_text(duplicated_line, encoding="utf-8")
    assert _reject(generation, root, todo) == "todo_line_invalid"


# ------------------------------------------------------------------ path異常


def test_reference_path_problems_stop(generation, tmp_path):
    root, todo = _workspace(tmp_path)
    original = todo.read_text(encoding="utf-8")

    absolute = original.replace(
        "](records/first.md)", f"]({(root / 'records' / 'first.md').as_posix()})"
    )
    todo.write_text(absolute, encoding="utf-8")
    assert _reject(generation, root, todo) == "reference_path_invalid"

    escaping = original.replace("](records/first.md)", "](../outside.md)")
    todo.write_text(escaping, encoding="utf-8")
    assert _reject(generation, root, todo) == "reference_path_invalid"

    missing = original.replace("](records/first.md)", "](records/absent.md)")
    todo.write_text(missing, encoding="utf-8")
    assert _reject(generation, root, todo) == "reference_path_invalid"

    todo.write_text(original, encoding="utf-8")
    link = root / "records" / "linked.md"
    link.symlink_to(root / "records" / "second.md")
    symlinked = original.replace("](records/first.md)", "](records/linked.md)")
    todo.write_text(symlinked, encoding="utf-8")
    assert _reject(generation, root, todo) == "reference_path_invalid"


def test_module_never_parses_counts_out_of_output_text(generation):
    """件数は構造化集計からだけ取る。出力文字列を読まない。"""

    text = Path(generation.__file__).read_text(encoding="utf-8")
    for forbidden in (
        'receipt["stdout"]', 'receipt["stderr"]',
        '["stdout"]', '["stderr"]', "passed in",
    ):
        assert forbidden not in text
