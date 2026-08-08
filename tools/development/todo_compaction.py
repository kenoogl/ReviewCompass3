"""TODO compaction結果の検証とbyte-exact snapshotからの復元。"""

import dataclasses
import hashlib
import json
import re
import tempfile
from pathlib import Path


_MAX_TODO_BYTES = 12288
_ACTIVE_ID = re.compile(
    r"^- `(?P<record_id>ISSUE-[A-Z0-9-]+)`：",
    re.MULTILINE,
)
_MARKDOWN_REFERENCE = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
_FORBIDDEN_HISTORY = (
    re.compile(r"^- Claim `", re.MULTILINE),
    re.compile(r"^### 手戻り・機械化候補\s*$", re.MULTILINE),
    re.compile(r"^## session\b", re.IGNORECASE | re.MULTILINE),
)


class TodoCompactionError(Exception):
    """TODO compactionまたはrestoreが固定境界に違反している。"""


@dataclasses.dataclass(frozen=True)
class TodoCompactionValidation:
    bytes_count: int
    active_ids: tuple
    reference_paths: tuple


@dataclasses.dataclass(frozen=True)
class TodoRestoreResult:
    action: str
    source_sha256: str
    bytes_count: int


from tools.common.digests import sha256_hex as _sha256


from tools.common.digests import canonical_content_digest as _canonical_digest


def _resolve_project_path(project_root, relative_path, *, label):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute() or not path.parts:
        raise TodoCompactionError(f"{label} is invalid")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise TodoCompactionError(f"{label} is invalid") from error
    return resolved


def validate_compacted_todo(document, *, project_root, known_active_ids):
    """短いTODOのsize、履歴、active ID、参照到達性を検査する。"""

    if not isinstance(document, bytes):
        raise TodoCompactionError("TODO must be bytes")
    if len(document) > _MAX_TODO_BYTES:
        raise TodoCompactionError("TODO exceeds 12288 bytes")
    try:
        text = document.decode("utf-8")
    except UnicodeDecodeError as error:
        raise TodoCompactionError("TODO is not valid UTF-8") from error
    if any(pattern.search(text) for pattern in _FORBIDDEN_HISTORY):
        raise TodoCompactionError("detailed history is prohibited")

    active_ids = tuple(
        match.group("record_id")
        for match in _ACTIVE_ID.finditer(text)
    )
    if not active_ids:
        raise TodoCompactionError("active ID is missing")
    if len(active_ids) != len(set(active_ids)):
        raise TodoCompactionError("duplicate active ID")
    known_ids = set(known_active_ids)
    if any(record_id not in known_ids for record_id in active_ids):
        raise TodoCompactionError("unknown active ID")
    if len(active_ids) != 1:
        raise TodoCompactionError("active ID count is invalid")

    references = tuple(_MARKDOWN_REFERENCE.findall(text))
    if not references:
        raise TodoCompactionError("TODO reference is missing")
    for relative_path in references:
        try:
            path = _resolve_project_path(
                project_root,
                relative_path,
                label="TODO reference",
            )
        except TodoCompactionError as error:
            raise TodoCompactionError(
                "TODO reference is unresolved"
            ) from error
        if not path.is_file():
            raise TodoCompactionError("TODO reference is unresolved")
    return TodoCompactionValidation(
        bytes_count=len(document),
        active_ids=active_ids,
        reference_paths=references,
    )


def _load_manifest(path):
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TodoCompactionError("manifest read failed") from error
    if manifest.get("content_digest") != _canonical_digest(manifest):
        raise TodoCompactionError("manifest digest mismatch")
    return manifest


def _atomic_write(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.name}.restore.",
            delete=False,
        ) as output:
            output.write(content)
            temporary = Path(output.name)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def restore_todo_from_snapshot(
    *,
    project_root,
    source_path,
    snapshot_path,
    manifest_path,
    write_bytes=None,
):
    """manifest検証済みsnapshotをTODOへ戻し、書込み後に再検証する。"""

    if Path(source_path).as_posix() != "TODO_NEXT_SESSION.md":
        raise TodoCompactionError("source path is invalid")
    handoff_root = Path("records/session-handoffs")
    snapshot_relative = Path(snapshot_path)
    manifest_relative = Path(manifest_path)
    if (
        handoff_root not in snapshot_relative.parents
        or handoff_root not in manifest_relative.parents
        or snapshot_relative == manifest_relative
    ):
        raise TodoCompactionError("snapshot path is invalid")
    source = _resolve_project_path(
        project_root,
        source_path,
        label="source path",
    )
    snapshot = _resolve_project_path(
        project_root,
        snapshot_path,
        label="snapshot path",
    )
    manifest_file = _resolve_project_path(
        project_root,
        manifest_path,
        label="manifest path",
    )
    manifest = _load_manifest(manifest_file)
    if (
        manifest.get("manifest_kind") != "todo_byte_exact_snapshot"
        or manifest.get("manifest_version") != 1
        or not isinstance(manifest.get("source"), dict)
        or not isinstance(manifest.get("snapshot"), dict)
        or manifest["source"].get("path") != str(Path(source_path))
        or manifest["snapshot"].get("path") != str(Path(snapshot_path))
    ):
        raise TodoCompactionError("manifest identity mismatch")
    try:
        source_before = source.read_bytes()
        snapshot_content = snapshot.read_bytes()
    except OSError as error:
        raise TodoCompactionError("restore input read failed") from error
    expected_digest = manifest["snapshot"].get("sha256")
    if (
        _sha256(snapshot_content) != expected_digest
        or manifest["source"].get("sha256") != expected_digest
        or manifest["snapshot"].get("bytes") != len(snapshot_content)
        or manifest["source"].get("bytes") != len(snapshot_content)
    ):
        raise TodoCompactionError("snapshot digest mismatch")

    writer = write_bytes or _atomic_write
    try:
        writer(source, snapshot_content)
        restored = source.read_bytes()
    except OSError as error:
        try:
            _atomic_write(source, source_before)
        except OSError as rollback_error:
            raise TodoCompactionError("restore rollback failed") from rollback_error
        raise TodoCompactionError("restore write failed") from error
    if restored != snapshot_content or _sha256(restored) != expected_digest:
        try:
            _atomic_write(source, source_before)
        except OSError as error:
            raise TodoCompactionError("restore rollback failed") from error
        raise TodoCompactionError("restore verification mismatch")
    return TodoRestoreResult(
        action="restored",
        source_sha256=expected_digest,
        bytes_count=len(restored),
    )
