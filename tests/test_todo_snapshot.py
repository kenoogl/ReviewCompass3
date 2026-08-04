"""WI-001 TODO byte-exact snapshotのAcceptance Test。"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


SOURCE_PATH = "TODO_NEXT_SESSION.md"
SNAPSHOT_PATH = (
    "records/session-handoffs/"
    "2026-08-04-todo-before-compaction-001.md"
)
MANIFEST_PATH = (
    "records/session-handoffs/"
    "2026-08-04-todo-before-compaction-001.manifest.json"
)
SNAPSHOT_ID = "TODO-SNAPSHOT-2026-08-04-001"
CREATED_AT = "2026-08-04T11:20:00+09:00"


def _module():
    return importlib.import_module("tools.development.todo_snapshot")


def _sha256(value):
    return hashlib.sha256(value).hexdigest()


def _canonical_digest(record):
    payload = {
        key: value
        for key, value in record.items()
        if key != "content_digest"
    }
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _source(project_root, content):
    path = project_root / SOURCE_PATH
    path.write_bytes(content)
    return path


def _create(project_root):
    module = _module()
    return module.create_todo_snapshot(
        project_root=project_root,
        source_path=SOURCE_PATH,
        snapshot_path=SNAPSHOT_PATH,
        manifest_path=MANIFEST_PATH,
        snapshot_id=SNAPSHOT_ID,
        created_at=CREATED_AT,
    )


def test_creates_byte_exact_snapshot_and_separate_manifest(tmp_path):
    source = (
        "# TODO_NEXT_SESSION\n\n"
        "- Claim `EC-001`：一件目\n"
        "本文🍵\n"
        "- Claim `EC-002`：二件目"
    ).encode("utf-8")
    _source(tmp_path, source)

    result = _create(tmp_path)

    snapshot = tmp_path / SNAPSHOT_PATH
    manifest_path = tmp_path / MANIFEST_PATH
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_sha = _sha256(source)
    assert snapshot.read_bytes() == source
    assert manifest == {
        "manifest_kind": "todo_byte_exact_snapshot",
        "manifest_version": 1,
        "snapshot_id": SNAPSHOT_ID,
        "created_at": CREATED_AT,
        "source": {
            "path": SOURCE_PATH,
            "sha256": expected_sha,
            "bytes": len(source),
            "lines": 5,
            "claim_count": 2,
        },
        "snapshot": {
            "path": SNAPSHOT_PATH,
            "sha256": expected_sha,
            "bytes": len(source),
        },
        "content_digest": manifest["content_digest"],
    }
    assert manifest["content_digest"] == _canonical_digest(manifest)
    assert result.snapshot_id == SNAPSHOT_ID
    assert result.action == "created"
    assert result.source_sha256 == result.snapshot_sha256 == expected_sha
    assert result.bytes_count == len(source)
    assert result.line_count == 5
    assert result.claim_count == 2


def test_verifies_snapshot_by_rereading_source_snapshot_and_manifest(
    tmp_path,
):
    source = b"# TODO_NEXT_SESSION\n\ncurrent\n"
    _source(tmp_path, source)
    _create(tmp_path)
    module = _module()

    result = module.verify_todo_snapshot(
        project_root=tmp_path,
        manifest_path=MANIFEST_PATH,
    )

    assert result.action == "verified"
    assert result.source_sha256 == result.snapshot_sha256 == _sha256(
        source
    )
    assert result.bytes_count == len(source)
    assert result.line_count == 3
    assert result.claim_count == 0


def test_accepts_zero_claim_and_no_final_newline_boundary(tmp_path):
    source = "# TODO_NEXT_SESSION\n現在位置：準備中".encode("utf-8")
    _source(tmp_path, source)

    result = _create(tmp_path)

    assert result.bytes_count == len(source)
    assert result.line_count == 2
    assert result.claim_count == 0
    assert (tmp_path / SNAPSHOT_PATH).read_bytes() == source


def test_rejects_tampered_snapshot(tmp_path):
    _source(tmp_path, b"# TODO_NEXT_SESSION\nfixed\n")
    _create(tmp_path)
    (tmp_path / SNAPSHOT_PATH).write_bytes(b"tampered\n")
    module = _module()

    with pytest.raises(
        module.TodoSnapshotError,
        match="snapshot digest mismatch",
    ):
        module.verify_todo_snapshot(
            project_root=tmp_path,
            manifest_path=MANIFEST_PATH,
        )


def test_rejects_source_changed_after_snapshot(tmp_path):
    _source(tmp_path, b"# TODO_NEXT_SESSION\nfixed\n")
    _create(tmp_path)
    _source(tmp_path, b"# TODO_NEXT_SESSION\nchanged\n")
    module = _module()

    with pytest.raises(
        module.TodoSnapshotError,
        match="source digest mismatch",
    ):
        module.verify_todo_snapshot(
            project_root=tmp_path,
            manifest_path=MANIFEST_PATH,
        )


def test_rejects_existing_output_without_overwrite(tmp_path):
    source = b"# TODO_NEXT_SESSION\nfixed\n"
    _source(tmp_path, source)
    _create(tmp_path)
    snapshot_before = (tmp_path / SNAPSHOT_PATH).read_bytes()
    manifest_before = (tmp_path / MANIFEST_PATH).read_bytes()
    module = _module()

    with pytest.raises(
        module.TodoSnapshotError,
        match="snapshot output already exists",
    ):
        _create(tmp_path)

    assert (tmp_path / SNAPSHOT_PATH).read_bytes() == snapshot_before
    assert (tmp_path / MANIFEST_PATH).read_bytes() == manifest_before


@pytest.mark.parametrize(
    ("snapshot_path", "manifest_path"),
    (
        ("snapshot.md", MANIFEST_PATH),
        (SNAPSHOT_PATH, "manifest.json"),
        ("../outside.md", MANIFEST_PATH),
    ),
)
def test_rejects_output_outside_session_handoffs(
    tmp_path,
    snapshot_path,
    manifest_path,
):
    _source(tmp_path, b"# TODO_NEXT_SESSION\nfixed\n")
    module = _module()

    with pytest.raises(
        module.TodoSnapshotError,
        match="snapshot output path is invalid",
    ):
        module.create_todo_snapshot(
            project_root=tmp_path,
            source_path=SOURCE_PATH,
            snapshot_path=snapshot_path,
            manifest_path=manifest_path,
            snapshot_id=SNAPSHOT_ID,
            created_at=CREATED_AT,
        )
