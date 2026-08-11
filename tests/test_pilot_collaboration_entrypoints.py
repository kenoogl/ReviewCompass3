"""Pilot collaboration の共通promptと入口参照の受入テスト。"""

from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "30925a54a0e8ee7c53e3503eccfda7a73fa11752"
PROMPT_PATH = "docs/development/prompts/pilot-collaboration-run.md"
INSTRUCTION_PATH = (
    "records/session-handoffs/"
    "2026-08-11-pilot-collaboration-entry-implementation-request-v6.md"
)
ALLOWED_PATHS = {
    "tools/development/pilot_collaboration.py",
    "tools/development/pilot_collaboration_cli.py",
    "tools/bootstrap/immutable_result_store.py",
    "tools/bootstrap/raw_review_store.py",
    "tests/test_pilot_collaboration.py",
    "tests/test_pilot_collaboration_cli.py",
    "tests/test_bootstrap_immutable_result_store.py",
    "docs/development/prompts/pilot-collaboration-run.md",
    "tests/test_pilot_collaboration_entrypoints.py",
    "AGENTS.md",
    "CLAUDE.md",
    "pyproject.toml",
}


def _git(repository, *arguments):
    return subprocess.run(
        ("git", *arguments),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _commit_changed_paths(repository, commit):
    return set(
        _git(
            repository,
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "-r",
            commit,
        ).splitlines()
    )


def _is_followup_record(path):
    return path == "TODO_NEXT_SESSION.md" or path.startswith(
        "records/session-handoffs/"
    )


def _implementation_paths_since_base(repository, base_commit, target_commit="HEAD"):
    commits = _git(
        repository,
        "rev-list",
        "--reverse",
        f"{base_commit}..{target_commit}",
    ).splitlines()
    changed_paths = set()
    for commit in commits:
        changed_paths.update(_commit_changed_paths(repository, commit))
    return {
        path
        for path in changed_paths
        if not _is_followup_record(path)
    }


def _initialize_test_repository(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "--quiet")
    (repository / "README.md").write_text("fixed base\n", encoding="utf-8")
    _git(repository, "add", "README.md")
    _git(
        repository,
        "-c",
        "user.name=Acceptance Test",
        "-c",
        "user.email=acceptance@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "fixed base",
    )
    return repository, _git(repository, "rev-parse", "HEAD")


def _commit_test_change(repository, relative_path, content, message):
    path = repository / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _git(repository, "add", relative_path)
    _git(
        repository,
        "-c",
        "user.name=Acceptance Test",
        "-c",
        "user.email=acceptance@example.invalid",
        "commit",
        "--quiet",
        "-m",
        message,
    )


def test_repository_exposes_one_common_pilot_entrypoint():
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert pyproject.count("reviewcompass3-pilot =") == 1
    assert (
        'reviewcompass3-pilot = "tools.development.pilot_collaboration_cli:main"'
        in pyproject
    )
    assert pyproject.count("reviewcompass3-bootstrap-review =") == 1


def test_entrypoint_change_is_limited_to_one_reference_per_file():
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (PROJECT_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert agents.count(PROMPT_PATH) == 1
    assert claude.count(PROMPT_PATH) == 1
    assert len([line for line in agents.splitlines() if PROMPT_PATH in line]) == 1
    assert len([line for line in claude.splitlines() if PROMPT_PATH in line]) == 1


def test_common_prompt_names_only_the_canonical_instruction_and_commands():
    prompt_file = PROJECT_ROOT / PROMPT_PATH
    prompt = prompt_file.read_text(encoding="utf-8")

    assert prompt.count(INSTRUCTION_PATH) == 1
    assert "implementation-request-v5.md" not in prompt
    assert "v5以前を指示として併用" not in prompt
    for command in (
        "reviewcompass3-pilot prepare",
        "reviewcompass3-pilot ingest",
        "reviewcompass3-pilot status",
    ):
        assert command in prompt
    for boundary in (
        "LLM",
        "機械処理",
        "外部送信",
        "Human",
        "prompt_payload_bytes",
    ):
        assert boundary in prompt


def test_change_scope_contains_only_v6_allowlisted_paths():
    implementation_paths = _implementation_paths_since_base(
        PROJECT_ROOT,
        BASE_COMMIT,
    )

    assert implementation_paths
    assert implementation_paths <= ALLOWED_PATHS


def test_change_scope_ignores_later_record_and_todo_commits(tmp_path):
    repository, base_commit = _initialize_test_repository(tmp_path)
    _commit_test_change(
        repository,
        "tools/development/pilot_collaboration.py",
        "# implementation\n",
        "implementation",
    )
    record = repository / "records/session-handoffs/review.md"
    record.parent.mkdir(parents=True)
    record.write_text("review\n", encoding="utf-8")
    (repository / "TODO_NEXT_SESSION.md").write_text("next\n", encoding="utf-8")
    _git(repository, "add", "records/session-handoffs/review.md", "TODO_NEXT_SESSION.md")
    _git(
        repository,
        "-c",
        "user.name=Acceptance Test",
        "-c",
        "user.email=acceptance@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "follow-up records",
    )
    implementation_paths = _implementation_paths_since_base(
        repository,
        base_commit,
    )

    assert implementation_paths == {
        "tools/development/pilot_collaboration.py"
    }


def test_change_scope_rejects_forbidden_commit_before_later_allowed_commit(tmp_path):
    repository, base_commit = _initialize_test_repository(tmp_path)
    _commit_test_change(
        repository,
        "tools/development/forbidden_production.py",
        "# forbidden\n",
        "forbidden production",
    )
    _commit_test_change(
        repository,
        "tests/test_pilot_collaboration.py",
        "# later allowed test\n",
        "later allowed test",
    )
    _commit_test_change(
        repository,
        "records/session-handoffs/review.md",
        "review\n",
        "follow-up record",
    )

    implementation_paths = _implementation_paths_since_base(
        repository,
        base_commit,
    )

    assert "tools/development/forbidden_production.py" in implementation_paths
    assert not implementation_paths <= ALLOWED_PATHS
