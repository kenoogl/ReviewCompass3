"""WI-004 common TODO promptとCodex／Claude入口のAcceptance Test。"""

from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = "docs/development/prompts/todo-handoff-update.md"
PROMPT = PROJECT_ROOT / PROMPT_PATH
AGENTS = PROJECT_ROOT / "AGENTS.md"
CLAUDE = PROJECT_ROOT / "CLAUDE.md"


def _validate_entrypoints(prompt, agents, claude):
    assert 0 < len(prompt.encode("utf-8")) <= 4096
    assert agents.count(PROMPT_PATH) == 1
    assert claude.count(PROMPT_PATH) == 1

    agents_todo_lines = [
        line
        for line in agents.splitlines()
        if "TODO_NEXT_SESSION" in line or "TODO" in line
    ]
    assert len(agents_todo_lines) == 1
    assert PROMPT_PATH in agents_todo_lines[0]

    claude_body = [
        line
        for line in claude.splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert claude_body == [
        f"[TODO handoff update]({PROMPT_PATH})"
    ]


def test_repository_has_one_common_prompt_and_two_link_only_entrypoints():
    _validate_entrypoints(
        PROMPT.read_text(encoding="utf-8"),
        AGENTS.read_text(encoding="utf-8"),
        CLAUDE.read_text(encoding="utf-8"),
    )
    assert len(list(PROJECT_ROOT.glob("**/todo-handoff-update.md"))) == 1


def test_common_prompt_routes_meaning_and_machine_operations():
    prompt = PROMPT.read_text(encoding="utf-8")

    for required in (
        "docs/development/templates/TODO_NEXT_SESSION.template.md",
        "tools/development/todo_handoff_projection.py",
        "tools/development/todo_compaction.py",
        # module起動へ統一（DEC-SHARED-FUNCTION-POLICY-001）に伴い期待文字列を更新
        "python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md",
        "python3 -m tools.development.work_unit_transition --work-status completed",
        "active Issue",
        "Candidate／Issue／Evidence",
        "LLM",
        "機械",
    ):
        assert required in prompt


def test_rejects_independent_todo_rule_in_claude_entrypoint():
    prompt = "共通prompt"
    agents = f"- [TODO common]({PROMPT_PATH})"
    claude = (
        "# CLAUDE.md\n\n"
        f"[TODO handoff update]({PROMPT_PATH})\n\n"
        "- TODOはsession履歴を累積しない。\n"
    )

    with pytest.raises(AssertionError):
        _validate_entrypoints(prompt, agents, claude)
