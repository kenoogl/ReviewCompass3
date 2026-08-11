"""正規JSON documentの共通不変保存境界。"""

import dataclasses
import hashlib
import json
from pathlib import Path, PurePosixPath


class ImmutableResultStoreError(Exception):
    """JSON documentを安全に不変保存できない。"""


@dataclasses.dataclass(frozen=True)
class ImmutableStoredDocument:
    relative_path: str
    document_sha256: str
    file_sha256: str


def canonical_json_bytes(value):
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as error:
        raise ImmutableResultStoreError("Document is not canonical JSON") from error


def _safe_relative_path(relative_path):
    if not isinstance(relative_path, str) or not relative_path or "\x00" in relative_path:
        raise ImmutableResultStoreError("Unsafe immutable result path")
    path = PurePosixPath(relative_path)
    if (
        path.is_absolute()
        or relative_path in (".", "..")
        or any(part in ("", ".", "..") for part in path.parts)
        or str(path) != relative_path
    ):
        raise ImmutableResultStoreError("Unsafe immutable result path")
    return path


def _reject_symlink_chain(root, target_parent):
    if root.is_symlink():
        raise ImmutableResultStoreError("Immutable result root is a symlink")
    current = root
    for part in target_parent.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            raise ImmutableResultStoreError("Immutable result parent is a symlink")


def store_immutable_json(storage_root, relative_path, document):
    relative = _safe_relative_path(relative_path)
    root = Path(storage_root)
    if not root.is_absolute():
        root = root.resolve()
    try:
        if root.exists() and (not root.is_dir() or root.is_symlink()):
            raise ImmutableResultStoreError("Invalid immutable result root")
        root.mkdir(parents=True, exist_ok=True)
        target = root.joinpath(*relative.parts)
        _reject_symlink_chain(root, target.parent)
        target.parent.mkdir(parents=True, exist_ok=True)
        _reject_symlink_chain(root, target.parent)
        document_bytes = canonical_json_bytes(document)
        file_bytes = document_bytes + b"\n"
        with target.open("xb") as output:
            output.write(file_bytes)
        if target.is_symlink() or target.read_bytes() != file_bytes:
            raise ImmutableResultStoreError("Immutable result reread mismatch")
    except FileExistsError as error:
        raise ImmutableResultStoreError("Immutable result already exists") from error
    except OSError as error:
        raise ImmutableResultStoreError("Cannot write immutable result") from error
    return ImmutableStoredDocument(
        relative_path=relative_path,
        document_sha256=hashlib.sha256(document_bytes).hexdigest(),
        file_sha256=hashlib.sha256(file_bytes).hexdigest(),
    )
