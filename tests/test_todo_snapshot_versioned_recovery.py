"""WI-007 source変更時のversioned snapshot recovery境界。"""

from pathlib import Path

import pytest

from tools.development import todo_snapshot


def _create(project_root, *, suffix):
    return todo_snapshot.create_todo_snapshot(
        project_root=project_root,
        source_path="TODO_NEXT_SESSION.md",
        snapshot_path=(
            "records/session-handoffs/"
            f"todo-before-compaction-{suffix}.md"
        ),
        manifest_path=(
            "records/session-handoffs/"
            f"todo-before-compaction-{suffix}.manifest.json"
        ),
        snapshot_id=f"TODO-SNAPSHOT-{suffix}",
        created_at="2026-08-04T13:00:00+09:00",
    )


def test_source_change_requires_new_version_without_overwriting_old(tmp_path):
    source = tmp_path / "TODO_NEXT_SESSION.md"
    source.write_bytes(b"source version 1\n")
    _create(tmp_path, suffix="001")
    old_snapshot = (
        tmp_path
        / "records/session-handoffs/todo-before-compaction-001.md"
    )
    old_bytes = old_snapshot.read_bytes()

    source.write_bytes(b"source version 2\n")
    with pytest.raises(
        todo_snapshot.TodoSnapshotError,
        match="source digest mismatch",
    ):
        todo_snapshot.verify_todo_snapshot(
            project_root=tmp_path,
            manifest_path=(
                "records/session-handoffs/"
                "todo-before-compaction-001.manifest.json"
            ),
        )

    result = _create(tmp_path, suffix="002")

    assert result.action == "created"
    assert old_snapshot.read_bytes() == old_bytes
    assert (
        tmp_path
        / "records/session-handoffs/todo-before-compaction-002.md"
    ).read_bytes() == b"source version 2\n"
    assert Path(result.snapshot_id).name == "TODO-SNAPSHOT-002"
