"""Commitと循環しないTODO Git欄の検査Test。"""

import importlib
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def _module():
    return importlib.import_module("tools.development.todo_handoff")


def _stable_document():
    return """# TODO_NEXT_SESSION

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の全Test：`490 passed`

## 更新規則
"""


def test_accepts_commit_stable_git_handoff_section():
    result = _module().validate_commit_stable_git_section(
        _stable_document()
    )

    assert result.status == "passed"
    assert result.findings == ()


def test_rejects_self_sha_mutable_remote_and_uncommitted_snapshot():
    document = """# TODO_NEXT_SESSION

## Git・Test

- branch：`main`
- HEAD：`e92e9ae190008da24a36824c3043edbfa3a4234f`
- remote：push済み。ahead／behindは`0 / 0`
- worktree：TODOだけを未コミットで保持

## 更新規則
"""

    result = _module().validate_commit_stable_git_section(document)

    assert result.status == "failed"
    assert result.findings == (
        "commit_boundary_missing",
        "git_state_authority_missing",
        "worktree_commit_boundary_missing",
        "self_commit_sha_snapshot",
        "mutable_remote_snapshot",
        "uncommitted_worktree_snapshot",
    )


def test_ignores_commit_sha_evidence_outside_git_section():
    document = _stable_document().replace(
        "## Git・Test",
        """## 実施報告照合

- Evidence commit：`e92e9ae190008da24a36824c3043edbfa3a4234f`

## Git・Test""",
    )

    result = _module().validate_commit_stable_git_section(document)

    assert result.status == "passed"


def test_rejects_missing_or_duplicate_git_section():
    missing = _module().validate_commit_stable_git_section(
        "# TODO_NEXT_SESSION\n"
    )
    duplicate = _module().validate_commit_stable_git_section(
        _stable_document() + "\n" + _stable_document()
    )

    assert missing.findings == ("git_section_missing",)
    assert duplicate.findings == ("git_section_duplicated",)


def test_repository_template_and_current_todo_are_commit_stable():
    paths = (
        ROOT / "docs/development/templates/TODO_NEXT_SESSION.template.md",
        ROOT / "TODO_NEXT_SESSION.md",
    )

    results = [
        _module().validate_commit_stable_git_section(
            path.read_text(encoding="utf-8")
        )
        for path in paths
    ]

    assert all(result.status == "passed" for result in results)


def test_cli_returns_machine_readable_failure(capsys, tmp_path):
    path = tmp_path / "TODO_NEXT_SESSION.md"
    path.write_text(
        "# TODO_NEXT_SESSION\n\n## Git・Test\n\n- HEAD：`abc1234`\n",
        encoding="utf-8",
    )

    exit_code = _module().main((str(path),))

    assert exit_code == 1
    assert '"status": "failed"' in capsys.readouterr().out


def test_cli_returns_failure_when_compaction_rejects_git_stable_todo(
    capsys, monkeypatch, tmp_path
):
    issue_root = tmp_path / ".reviewcompass/workflow/issues-v4"
    issue_root.mkdir(parents=True)
    (issue_root / "issue-todo-handoff-verification-gap-001--v1.json").write_text(
        json.dumps(
            {
                "record_kind": "issue_record",
                "issue_id": "ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001",
            }
        ),
        encoding="utf-8",
    )
    document = _stable_document().replace(
        "## Git・Test",
        """## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：in_progress

## Git・Test""",
    ).encode("utf-8")
    assert len(document) < 12289
    path = tmp_path / "TODO_NEXT_SESSION.md"
    path.write_bytes(document + b" " * (12289 - len(document)))
    monkeypatch.chdir(tmp_path)

    exit_code = _module().main(("TODO_NEXT_SESSION.md",))

    assert exit_code == 1
    output = capsys.readouterr().out
    assert '"status": "failed"' in output
    assert "TODO exceeds 12288 bytes" in output
