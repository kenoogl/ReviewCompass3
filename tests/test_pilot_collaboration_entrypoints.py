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
    allowed = {
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

    committed = subprocess.run(
        ("git", "diff", "--name-only", BASE_COMMIT, "HEAD"),
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    status = subprocess.run(
        ("git", "status", "--porcelain", "--untracked-files=all"),
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    uncommitted = [line[3:] for line in status if len(line) >= 4]

    assert set(committed) | set(uncommitted) <= allowed
