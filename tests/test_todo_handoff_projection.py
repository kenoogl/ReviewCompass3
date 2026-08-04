"""WI-003 compact TODO projection rendererのAcceptance Test。"""

import hashlib
import importlib
from pathlib import Path

import pytest


def _module():
    return importlib.import_module(
        "tools.development.todo_handoff_projection"
    )


def _sha256(content):
    return hashlib.sha256(content).hexdigest()


def _fixture(tmp_path):
    template = tmp_path / "docs/development/templates/TODO_NEXT_SESSION.template.md"
    template.parent.mkdir(parents=True)
    template.write_text(
        "# TODO_NEXT_SESSION\n\n## 現在位置\n\n"
        "## 現在作業に影響する改善候補／Issue\n\n"
        "## 最新のauthority／Evidence\n\n"
        "## 次に行う一作業\n\n## blocker・Human判断待ち\n\n"
        "## stale・deferred\n\n## Git・Test\n\n## 更新規則\n",
        encoding="utf-8",
    )
    references = []
    for label, relative_path in (
        ("Task Contract", "records/task-contract/current.json"),
        ("Completion Evidence", "records/development/current.md"),
    ):
        path = tmp_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(label + "\n", encoding="utf-8")
        references.append(
            {
                "label": label,
                "path": relative_path,
                "sha256": _sha256(path.read_bytes()),
            }
        )
    projection = {
        "updated_on": "2026-08-04",
        "overall": "Work 3完了。Work 4前のIssue Resolution早期Pilotを実施中。",
        "current_work": "WI-003 TODO compaction completed / containing commit",
        "task_contract_id": "TC-PILOT-V2",
        "active_issue": {
            "issue_id": "ISSUE-PILOT-TODO-GROWTH-001",
            "state": "implementation_in_progress",
            "impact": "current handoff",
            "next_action": "WI-004",
        },
        "references": references,
        "next_work": {
            "action": "WI-004の共通TODO更新promptをtest-firstで実装する。",
            "start_conditions": ["WI-003 containing commitとclean transition"],
            "completion_conditions": ["CodexとClaudeが同じpromptだけを参照する"],
            "following": "WI-005 post-write verification",
        },
        "blocker": "なし",
        "human_decision": "なし",
        "stale": "Plan v1-v3はv4にsuperseded",
        "deferred": "製品Issue Resolution automation、Work 4以降",
        "branch": "main",
        "related_test": "TODO projection targeted passed",
        "full_test": "official full passed",
    }
    return template, projection


def test_renders_deterministic_compact_todo_accepted_by_validator(tmp_path):
    template, projection = _fixture(tmp_path)

    first = _module().render_todo_handoff(
        projection,
        project_root=tmp_path,
        template_path=template.relative_to(tmp_path).as_posix(),
    )
    second = _module().render_todo_handoff(
        projection,
        project_root=tmp_path,
        template_path=template.relative_to(tmp_path).as_posix(),
    )

    assert first == second
    assert len(first) <= 12288
    assert b"- Claim `" not in first
    result = importlib.import_module(
        "tools.development.todo_compaction"
    ).validate_compacted_todo(
        first,
        project_root=tmp_path,
        known_active_ids={"ISSUE-PILOT-TODO-GROWTH-001"},
    )
    assert result.active_ids == ("ISSUE-PILOT-TODO-GROWTH-001",)


def test_renders_one_active_issue_and_resolved_reference_digests(tmp_path):
    template, projection = _fixture(tmp_path)

    rendered = _module().render_todo_handoff(
        projection,
        project_root=tmp_path,
        template_path=template.relative_to(tmp_path).as_posix(),
    ).decode("utf-8")

    assert rendered.count("ISSUE-PILOT-TODO-GROWTH-001") == 1
    for reference in projection["references"]:
        assert f"[{reference['label']}]({reference['path']})" in rendered
        assert reference["sha256"] in rendered


def test_rejects_missing_or_multiple_active_issue(tmp_path):
    template, projection = _fixture(tmp_path)

    for value in (None, [projection["active_issue"], projection["active_issue"]]):
        invalid = dict(projection)
        invalid["active_issue"] = value
        with pytest.raises(
            _module().TodoHandoffProjectionError,
            match="exactly one active issue is required",
        ):
            _module().render_todo_handoff(
                invalid,
                project_root=tmp_path,
                template_path=template.relative_to(tmp_path).as_posix(),
            )


def test_rejects_stale_or_unresolved_reference(tmp_path):
    template, projection = _fixture(tmp_path)
    projection["references"][0]["sha256"] = "0" * 64

    with pytest.raises(
        _module().TodoHandoffProjectionError,
        match="projection reference is stale or unresolved",
    ):
        _module().render_todo_handoff(
            projection,
            project_root=tmp_path,
            template_path=template.relative_to(tmp_path).as_posix(),
        )


def test_rejects_template_missing_required_heading(tmp_path):
    template, projection = _fixture(tmp_path)
    template.write_text("# TODO_NEXT_SESSION\n", encoding="utf-8")

    with pytest.raises(
        _module().TodoHandoffProjectionError,
        match="TODO template headings are incomplete",
    ):
        _module().render_todo_handoff(
            projection,
            project_root=tmp_path,
            template_path=template.relative_to(tmp_path).as_posix(),
        )
