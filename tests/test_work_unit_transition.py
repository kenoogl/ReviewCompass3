"""完了作業単位から次作業へのcommit関門Test。"""

import importlib
import subprocess
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]


def _module():
    return importlib.import_module(
        "tools.development.work_unit_transition"
    )


def test_blocks_next_work_and_reminds_when_completed_work_is_dirty():
    result = _module().evaluate_transition(
        work_status="completed",
        porcelain=" M AGENTS.md\n?? evidence.json\n",
    )

    assert result.status == "blocked"
    assert result.next_work_allowed is False
    assert result.findings == ("completed_work_unit_uncommitted",)
    assert result.reminder == (
        "作業単位は完了していますが、未コミットです。"
        "コミットされるまで次の作業を開始できません。"
    )


def test_allows_next_work_when_completed_worktree_is_clean():
    result = _module().evaluate_transition(
        work_status="completed",
        porcelain="",
    )

    assert result.status == "passed"
    assert result.next_work_allowed is True
    assert result.findings == ()
    assert result.reminder is None


def test_does_not_misclassify_in_progress_changes_as_completed_work():
    result = _module().evaluate_transition(
        work_status="in_progress",
        porcelain=" M implementation.py\n",
    )

    assert result.status == "not_applicable"
    assert result.next_work_allowed is None
    assert result.findings == ()
    assert result.reminder is None


def test_preflight_reads_git_state_mechanically():
    calls = []

    def fake_run(command, **kwargs):
        calls.append((tuple(command), kwargs))
        return SimpleNamespace(
            returncode=0,
            stdout=" M TODO_NEXT_SESSION.md\n",
            stderr="",
        )

    result = _module().preflight_next_work(
        work_status="completed",
        project_root="/project",
        run=fake_run,
    )

    assert result.status == "blocked"
    assert calls == [
        (
            ("git", "status", "--porcelain=v1", "--untracked-files=all"),
            {
                "cwd": "/project",
                "capture_output": True,
                "text": True,
            },
        )
    ]


def test_cli_returns_machine_readable_block(capsys, monkeypatch):
    module = _module()
    monkeypatch.setattr(
        module,
        "preflight_next_work",
        lambda **kwargs: module.evaluate_transition(
            work_status="completed",
            porcelain=" M policy.md\n",
        ),
    )

    exit_code = module.main(("--work-status", "completed"))

    assert exit_code == 1
    output = capsys.readouterr().out
    assert '"status": "blocked"' in output
    assert '"completed_work_unit_uncommitted"' in output


def _git(repository, *arguments):
    return subprocess.run(
        ("git", "-C", str(repository), *arguments),
        check=True,
        capture_output=True,
        text=True,
    )


def test_preflight_ignores_local_claude_reports_but_blocks_work_artifacts(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init")
    _git(repository, "config", "user.email", "test@example.invalid")
    _git(repository, "config", "user.name", "Test User")
    (repository / ".gitignore").write_text(
        (ROOT / ".gitignore").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (repository / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(repository, "add", ".gitignore", "tracked.txt")
    _git(repository, "commit", "-m", "initial")

    report = (
        repository
        / "records/session-handoffs/2026-08-05-claude-to-codex-completion.md"
    )
    report.parent.mkdir(parents=True)
    report.write_text("local report\n", encoding="utf-8")

    assert _module().preflight_next_work(
        work_status="completed", project_root=repository
    ).status == "passed"

    (repository / "uncommitted-artifact.md").write_text(
        "artifact\n", encoding="utf-8"
    )
    assert _module().preflight_next_work(
        work_status="completed", project_root=repository
    ).status == "blocked"
