"""WI-002 TODO compaction validator／restoreのAcceptance Test。"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


MAX_TODO_BYTES = 12288
ACTIVE_ISSUE_ID = "ISSUE-PILOT-TODO-GROWTH-001"
SOURCE_PATH = "TODO_NEXT_SESSION.md"
SNAPSHOT_PATH = (
    "records/session-handoffs/"
    "2026-08-04-todo-before-compaction-test.md"
)
MANIFEST_PATH = SNAPSHOT_PATH.replace(".md", ".manifest.json")
AUTHORITY_PATH = "records/task-contract/current.json"
EVIDENCE_PATH = "records/development/current-evidence.md"


def _module():
    return importlib.import_module("tools.development.todo_compaction")


def _sha256(content):
    return hashlib.sha256(content).hexdigest()


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


def _write_reference(project_root, relative_path, content):
    path = project_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _valid_document(project_root, *, total_bytes=None):
    _write_reference(project_root, AUTHORITY_PATH, '{"fixed": true}\n')
    _write_reference(project_root, EVIDENCE_PATH, "# Evidence\n")
    document = (
        "# TODO_NEXT_SESSION\n\n"
        "## 現在位置\n\n"
        "- Issue Resolution PilotのWI-002を実施中\n\n"
        "## 現在作業に影響する改善候補／Issue\n\n"
        f"- `{ACTIVE_ISSUE_ID}`：`implementation_in_progress`、"
        "影響：TODO compaction、次：WI-002\n\n"
        "## 最新のauthority／Evidence\n\n"
        f"- [Task Contract]({AUTHORITY_PATH})\n"
        f"- [Completion Evidence]({EVIDENCE_PATH})\n\n"
        "## 次に行う一作業\n\n"
        "WI-002 validator／restoreをtest-firstで実装する。\n"
    ).encode("utf-8")
    if total_bytes is None:
        return document
    assert len(document) <= total_bytes
    return document + b" " * (total_bytes - len(document))


def _validate(project_root, document):
    return _module().validate_compacted_todo(
        document,
        project_root=project_root,
        known_active_ids={ACTIVE_ISSUE_ID},
    )


def _write_restore_fixture(project_root, *, snapshot_content):
    source = project_root / SOURCE_PATH
    snapshot = project_root / SNAPSHOT_PATH
    manifest_path = project_root / MANIFEST_PATH
    source.write_bytes(b"compacted TODO\n")
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(snapshot_content)
    manifest = {
        "manifest_kind": "todo_byte_exact_snapshot",
        "manifest_version": 1,
        "snapshot_id": "TODO-SNAPSHOT-TEST-001",
        "created_at": "2026-08-04T12:30:00+09:00",
        "source": {
            "path": SOURCE_PATH,
            "sha256": _sha256(snapshot_content),
            "bytes": len(snapshot_content),
            "lines": len(snapshot_content.splitlines()),
            "claim_count": sum(
                line.startswith(b"- Claim `")
                for line in snapshot_content.splitlines()
            ),
        },
        "snapshot": {
            "path": SNAPSHOT_PATH,
            "sha256": _sha256(snapshot_content),
            "bytes": len(snapshot_content),
        },
    }
    manifest["content_digest"] = _canonical_digest(manifest)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return source, snapshot, manifest_path, manifest


def _restore(project_root, *, write_bytes=None):
    return _module().restore_todo_from_snapshot(
        project_root=project_root,
        source_path=SOURCE_PATH,
        snapshot_path=SNAPSHOT_PATH,
        manifest_path=MANIFEST_PATH,
        write_bytes=write_bytes,
    )


def test_accepts_exactly_12288_bytes_and_resolved_references(tmp_path):
    document = _valid_document(tmp_path, total_bytes=MAX_TODO_BYTES)

    result = _validate(tmp_path, document)

    assert result.bytes_count == MAX_TODO_BYTES
    assert result.active_ids == (ACTIVE_ISSUE_ID,)
    assert result.reference_paths == (AUTHORITY_PATH, EVIDENCE_PATH)


def test_rejects_12289_bytes(tmp_path):
    document = _valid_document(tmp_path, total_bytes=MAX_TODO_BYTES + 1)

    with pytest.raises(
        _module().TodoCompactionError,
        match="TODO exceeds 12288 bytes",
    ):
        _validate(tmp_path, document)


@pytest.mark.parametrize(
    "forbidden_content",
    (
        "- Claim `EC-999`：過去Claim\n",
        "### 手戻り・機械化候補\n\n詳細\n",
        "## session 2026-08-03\n\n時系列log\n",
    ),
)
def test_rejects_accumulated_history(tmp_path, forbidden_content):
    document = _valid_document(tmp_path) + forbidden_content.encode("utf-8")

    with pytest.raises(
        _module().TodoCompactionError,
        match="detailed history is prohibited",
    ):
        _validate(tmp_path, document)


def test_rejects_unknown_active_id(tmp_path):
    document = _valid_document(tmp_path).replace(
        ACTIVE_ISSUE_ID.encode("utf-8"),
        b"ISSUE-PILOT-UNKNOWN-001",
    )

    with pytest.raises(
        _module().TodoCompactionError,
        match="unknown active ID",
    ):
        _validate(tmp_path, document)


def test_rejects_duplicate_active_id(tmp_path):
    document = _valid_document(tmp_path)
    active_line = next(
        line
        for line in document.splitlines()
        if ACTIVE_ISSUE_ID.encode("utf-8") in line
    )
    document += b"\n" + active_line + b"\n"

    with pytest.raises(
        _module().TodoCompactionError,
        match="duplicate active ID",
    ):
        _validate(tmp_path, document)


def test_rejects_broken_authority_or_evidence_reference(tmp_path):
    document = _valid_document(tmp_path).replace(
        EVIDENCE_PATH.encode("utf-8"),
        b"records/development/missing-evidence.md",
    )

    with pytest.raises(
        _module().TodoCompactionError,
        match="TODO reference is unresolved",
    ):
        _validate(tmp_path, document)


def test_restores_snapshot_bytes_and_verifies_result(tmp_path):
    snapshot_content = (
        b"# TODO_NEXT_SESSION\n\n"
        b"- Claim `EC-001`: historical source\n"
    )
    source, _, _, _ = _write_restore_fixture(
        tmp_path,
        snapshot_content=snapshot_content,
    )

    result = _restore(tmp_path)

    assert source.read_bytes() == snapshot_content
    assert result.source_sha256 == _sha256(snapshot_content)
    assert result.bytes_count == len(snapshot_content)
    assert result.action == "restored"


def test_rejects_snapshot_digest_mismatch_without_changing_source(tmp_path):
    source, snapshot, _, _ = _write_restore_fixture(
        tmp_path,
        snapshot_content=b"fixed source\n",
    )
    source_before = source.read_bytes()
    snapshot.write_bytes(b"tampered snapshot\n")

    with pytest.raises(
        _module().TodoCompactionError,
        match="snapshot digest mismatch",
    ):
        _restore(tmp_path)

    assert source.read_bytes() == source_before


def test_rejects_manifest_digest_mismatch_without_changing_source(tmp_path):
    source, _, manifest_path, manifest = _write_restore_fixture(
        tmp_path,
        snapshot_content=b"fixed source\n",
    )
    source_before = source.read_bytes()
    manifest["source"]["bytes"] += 1
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        _module().TodoCompactionError,
        match="manifest digest mismatch",
    ):
        _restore(tmp_path)

    assert source.read_bytes() == source_before


def test_rolls_back_when_post_restore_verification_mismatches(tmp_path):
    source, _, _, _ = _write_restore_fixture(
        tmp_path,
        snapshot_content=b"fixed source\n",
    )
    source_before = source.read_bytes()

    def write_corrupt_bytes(path, content):
        Path(path).write_bytes(content + b"corrupt")

    with pytest.raises(
        _module().TodoCompactionError,
        match="restore verification mismatch",
    ):
        _restore(tmp_path, write_bytes=write_corrupt_bytes)

    assert source.read_bytes() == source_before
