"""TODOのbyte-exact snapshotとmanifestを作成・検証する。"""

import dataclasses
import hashlib
import json
from pathlib import Path


_OUTPUT_ROOT = Path("records/session-handoffs")


class TodoSnapshotError(Exception):
    """snapshotの作成または検証に失敗した。"""


@dataclasses.dataclass(frozen=True)
class TodoSnapshotResult:
    snapshot_id: str
    action: str
    source_sha256: str
    snapshot_sha256: str
    bytes_count: int
    line_count: int
    claim_count: int


def _sha256(content):
    return hashlib.sha256(content).hexdigest()


def _canonical_digest(record):
    payload = {
        key: value
        for key, value in record.items()
        if key != "content_digest"
    }
    return _sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _resolve_project_path(project_root, relative_path):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute():
        raise TodoSnapshotError("project path is invalid")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise TodoSnapshotError("project path is invalid") from error
    return resolved


def _resolve_output_path(project_root, relative_path):
    root = Path(project_root).resolve()
    output_root = (root / _OUTPUT_ROOT).resolve()
    path = Path(relative_path)
    if path.is_absolute():
        raise TodoSnapshotError("snapshot output path is invalid")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(output_root)
    except ValueError as error:
        raise TodoSnapshotError(
            "snapshot output path is invalid"
        ) from error
    if resolved == output_root:
        raise TodoSnapshotError("snapshot output path is invalid")
    return resolved


def _measure(content):
    lines = content.splitlines()
    return len(content), len(lines), sum(
        line.startswith(b"- Claim `")
        for line in lines
    )


def _result(*, manifest, action):
    return TodoSnapshotResult(
        snapshot_id=manifest["snapshot_id"],
        action=action,
        source_sha256=manifest["source"]["sha256"],
        snapshot_sha256=manifest["snapshot"]["sha256"],
        bytes_count=manifest["source"]["bytes"],
        line_count=manifest["source"]["lines"],
        claim_count=manifest["source"]["claim_count"],
    )


def create_todo_snapshot(
    *,
    project_root,
    source_path,
    snapshot_path,
    manifest_path,
    snapshot_id,
    created_at,
):
    source = _resolve_project_path(project_root, source_path)
    snapshot = _resolve_output_path(project_root, snapshot_path)
    manifest_file = _resolve_output_path(project_root, manifest_path)
    if snapshot == manifest_file:
        raise TodoSnapshotError("snapshot output path is invalid")
    if snapshot.exists():
        raise TodoSnapshotError("snapshot output already exists")
    if manifest_file.exists():
        raise TodoSnapshotError("manifest output already exists")

    try:
        source_content = source.read_bytes()
    except OSError as error:
        raise TodoSnapshotError("source read failed") from error
    bytes_count, line_count, claim_count = _measure(source_content)
    source_digest = _sha256(source_content)
    manifest = {
        "manifest_kind": "todo_byte_exact_snapshot",
        "manifest_version": 1,
        "snapshot_id": snapshot_id,
        "created_at": created_at,
        "source": {
            "path": str(Path(source_path)),
            "sha256": source_digest,
            "bytes": bytes_count,
            "lines": line_count,
            "claim_count": claim_count,
        },
        "snapshot": {
            "path": str(Path(snapshot_path)),
            "sha256": source_digest,
            "bytes": bytes_count,
        },
    }
    manifest["content_digest"] = _canonical_digest(manifest)
    manifest_content = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")

    snapshot.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    snapshot_created = False
    try:
        with snapshot.open("xb") as output:
            output.write(source_content)
        snapshot_created = True
        with manifest_file.open("xb") as output:
            output.write(manifest_content)
    except FileExistsError as error:
        if snapshot_created:
            snapshot.unlink()
        raise TodoSnapshotError("snapshot output already exists") from error
    except OSError as error:
        if snapshot_created and snapshot.exists():
            snapshot.unlink()
        raise TodoSnapshotError("snapshot write failed") from error

    verified = verify_todo_snapshot(
        project_root=project_root,
        manifest_path=manifest_path,
    )
    return dataclasses.replace(verified, action="created")


def verify_todo_snapshot(*, project_root, manifest_path):
    manifest_file = _resolve_output_path(project_root, manifest_path)
    try:
        manifest_content = manifest_file.read_text(encoding="utf-8")
        manifest = json.loads(manifest_content)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TodoSnapshotError("manifest read failed") from error
    if manifest.get("content_digest") != _canonical_digest(manifest):
        raise TodoSnapshotError("manifest digest mismatch")
    try:
        source_record = manifest["source"]
        snapshot_record = manifest["snapshot"]
        source = _resolve_project_path(
            project_root,
            source_record["path"],
        )
        snapshot = _resolve_output_path(
            project_root,
            snapshot_record["path"],
        )
        source_content = source.read_bytes()
        snapshot_content = snapshot.read_bytes()
    except (KeyError, TypeError, OSError) as error:
        raise TodoSnapshotError("snapshot inputs are invalid") from error

    if _sha256(source_content) != source_record.get("sha256"):
        raise TodoSnapshotError("source digest mismatch")
    if _sha256(snapshot_content) != snapshot_record.get("sha256"):
        raise TodoSnapshotError("snapshot digest mismatch")
    if source_content != snapshot_content:
        raise TodoSnapshotError("snapshot bytes mismatch")
    bytes_count, line_count, claim_count = _measure(source_content)
    if (
        source_record.get("bytes") != bytes_count
        or source_record.get("lines") != line_count
        or source_record.get("claim_count") != claim_count
        or snapshot_record.get("bytes") != bytes_count
    ):
        raise TodoSnapshotError("snapshot measurements mismatch")
    return _result(manifest=manifest, action="verified")
