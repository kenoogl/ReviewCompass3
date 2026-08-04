"""WI-002 restore対象pathの安全境界Test。"""

import importlib

import pytest


def _module():
    return importlib.import_module("tools.development.todo_compaction")


def test_rejects_restore_target_other_than_root_todo(tmp_path):
    module = _module()

    with pytest.raises(
        module.TodoCompactionError,
        match="source path is invalid",
    ):
        module.restore_todo_from_snapshot(
            project_root=tmp_path,
            source_path="records/development/other.md",
            snapshot_path="records/session-handoffs/source.md",
            manifest_path="records/session-handoffs/source.manifest.json",
        )


@pytest.mark.parametrize(
    ("snapshot_path", "manifest_path"),
    (
        ("snapshot.md", "records/session-handoffs/source.manifest.json"),
        ("records/session-handoffs/source.md", "manifest.json"),
        (
            "records/session-handoffs/source.md",
            "records/session-handoffs/source.md",
        ),
    ),
)
def test_rejects_restore_inputs_outside_handoff_root_or_same_path(
    tmp_path,
    snapshot_path,
    manifest_path,
):
    module = _module()

    with pytest.raises(
        module.TodoCompactionError,
        match="snapshot path is invalid",
    ):
        module.restore_todo_from_snapshot(
            project_root=tmp_path,
            source_path="TODO_NEXT_SESSION.md",
            snapshot_path=snapshot_path,
            manifest_path=manifest_path,
        )
