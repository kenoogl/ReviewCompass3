"""完了作業単位から次作業へのcommit関門Test。"""

import importlib
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest


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


def test_preflight_reads_git_state_mechanically(tmp_path):
    """機械的にGit状態を読み、未コミットならblockedを返す。

    Human承認（2026-08-10）「conftest.pyの追加と既存テスト1件の更新を承認する」により、
    F-B5修正後の呼び出し形へ更新した。検査している性質は変えていない。
    """

    calls = []
    project_root = tmp_path / "project"
    project_root.mkdir()

    def fake_run(command, **kwargs):
        calls.append((tuple(command), kwargs))
        if "rev-parse" in command:
            stdout = "%s\n" % project_root
        elif "status" in command:
            stdout = " M TODO_NEXT_SESSION.md\n"
        else:
            stdout = ""
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

    result = _module().preflight_next_work(
        work_status="completed",
        project_root=project_root,
        run=fake_run,
    )

    assert result.status == "blocked"
    expected_kwargs = {
        "cwd": str(project_root),
        "capture_output": True,
        "text": True,
    }
    assert calls == [
        (("git", "rev-parse", "--show-toplevel"), expected_kwargs),
        (
            ("git", "status", "--porcelain=v1", "--untracked-files=all"),
            expected_kwargs,
        ),
        (("git", "diff", "--name-only", "HEAD", "--"), expected_kwargs),
        (("git", "ls-files", "-v"), expected_kwargs),
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


def test_preflight_blocks_request_records_like_any_work_artifact(tmp_path):
    """依頼record（claude-to-codex名を含む）は特別扱いされず、未commitなら
    通常の作業成果物としてblockされる（DEC-IC-HANDOFF-GITIGNORE-RECORD-
    CANONICAL-001：局所メモ除外の廃止とrecord正本方式への整合の固定）。"""

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

    assert _module().preflight_next_work(
        work_status="completed", project_root=repository
    ).status == "passed"

    report = (
        repository
        / "records/session-handoffs/2026-08-05-claude-to-codex-completion.md"
    )
    report.parent.mkdir(parents=True)
    report.write_text("request record\n", encoding="utf-8")

    assert _module().preflight_next_work(
        work_status="completed", project_root=repository
    ).status == "blocked"

    _git(repository, "add", str(report.relative_to(repository)))
    _git(repository, "commit", "-m", "land request record")

    (repository / "uncommitted-artifact.md").write_text(
        "artifact\n", encoding="utf-8"
    )
    assert _module().preflight_next_work(
        work_status="completed", project_root=repository
    ).status == "blocked"


class TestTransitionCannotBeBypassed:
    """F-B5反証：indexの隠蔽や別Git rootで完了関門を迂回できない。"""

    def _transition(self):
        import importlib

        return importlib.import_module("tools.development.work_unit_transition")

    def test_head_difference_blocks_even_with_empty_porcelain(self):
        transition = self._transition()
        result = transition.evaluate_transition(
            work_status="completed",
            porcelain="",
            head_difference="tools/development/policy.py\n",
        )
        assert result.status == "blocked"
        assert result.next_work_allowed is False

    def test_clean_state_still_passes(self):
        transition = self._transition()
        result = transition.evaluate_transition(
            work_status="completed",
            porcelain="",
            head_difference="",
        )
        assert result.status == "passed"
        assert result.next_work_allowed is True

    def test_preflight_binds_the_requested_repository_identity(self, tmp_path):
        transition = self._transition()
        calls = []

        def fake_run(command, **kwargs):
            calls.append((tuple(command), kwargs.get("cwd")))
            if "rev-parse" in command:
                return SimpleNamespace(
                    returncode=0, stdout="%s\n" % tmp_path, stderr=""
                )
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        other_root = tmp_path / "other"
        other_root.mkdir()
        with pytest.raises(transition.WorkUnitTransitionError):
            transition.preflight_next_work(
                work_status="completed",
                project_root=other_root,
                run=fake_run,
            )


def _init_repository(path):
  """使い捨ての一時repositoryを作る。実repositoryの索引には触れない。"""

  path.mkdir(parents=True, exist_ok=True)
  for command in (
    ("git", "init", "-q"),
    ("git", "config", "user.email", "test@example.invalid"),
    ("git", "config", "user.name", "test"),
  ):
    subprocess.run(command, cwd=str(path), check=True, capture_output=True)
  tracked = path / "tracked.txt"
  tracked.write_text("original\n", encoding="utf-8")
  subprocess.run(
    ("git", "add", "tracked.txt"), cwd=str(path), check=True, capture_output=True
  )
  subprocess.run(
    ("git", "commit", "-q", "-m", "initial"),
    cwd=str(path),
    check=True,
    capture_output=True,
  )
  return tracked


class TestHiddenIndexCannotBypassTheGate:
  """F-C1反証：索引の隠蔽指定でも未コミット変更を見逃さない。"""

  @pytest.mark.parametrize("flag", ["--skip-worktree", "--assume-unchanged"])
  def test_hidden_tracked_change_still_blocks(self, tmp_path, flag):
    repository = tmp_path / "repository"
    tracked = _init_repository(repository)
    subprocess.run(
      ("git", "update-index", flag, "tracked.txt"),
      cwd=str(repository),
      check=True,
      capture_output=True,
    )
    tracked.write_text("modified after hiding\n", encoding="utf-8")

    porcelain = subprocess.run(
      ("git", "status", "--porcelain=v1", "--untracked-files=all"),
      cwd=str(repository),
      capture_output=True,
      text=True,
    )
    assert porcelain.stdout.strip() == ""

    result = _module().preflight_next_work(
      work_status="completed",
      project_root=repository,
    )
    assert result.status == "blocked"
    assert result.next_work_allowed is False

  def test_clean_repository_still_passes(self, tmp_path):
    repository = tmp_path / "clean"
    _init_repository(repository)
    result = _module().preflight_next_work(
      work_status="completed",
      project_root=repository,
    )
    assert result.status == "passed"
    assert result.next_work_allowed is True

  def test_requested_root_must_be_the_git_root(self, tmp_path):
    repository = tmp_path / "repository"
    _init_repository(repository)
    nested = repository / "nested"
    nested.mkdir()
    with pytest.raises(_module().WorkUnitTransitionError):
      _module().preflight_next_work(
        work_status="completed",
        project_root=nested,
      )
