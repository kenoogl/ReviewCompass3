"""一件レビュー材料と結果集合を扱う読取り専用の製品核。"""

import errno
import os
import stat
from pathlib import Path


MATERIAL_MAX_BYTES = 262_144
REVIEW_SPEC_MAX_BYTES = 65_536
RESULTS_MAX_BYTES = 1_048_576

_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
_FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


class ReviewStop(Exception):
    """契約境界を安全に満たせない。"""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


def _absolute_path(value):
    try:
        path = Path(value)
    except TypeError as error:
        raise ReviewStop("invalid_path") from error
    if not path.is_absolute() or ".." in path.parts:
        raise ReviewStop("invalid_path")
    return Path(os.path.normpath(path))


def _open_directory(parent_fd, name):
    try:
        entry = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except OSError as error:
        raise ReviewStop("unreadable_input") from error
    if stat.S_ISLNK(entry.st_mode) or not stat.S_ISDIR(entry.st_mode):
        raise ReviewStop("invalid_path")
    try:
        return os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise ReviewStop("invalid_path") from error
        raise ReviewStop("unreadable_input") from error


def _open_root(root):
    current_fd = os.open("/", _DIRECTORY_FLAGS)
    try:
        for part in root.parts[1:]:
            next_fd = _open_directory(current_fd, part)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _relative_parts(root, input_path):
    try:
        relative = input_path.relative_to(root)
    except ValueError as error:
        raise ReviewStop("invalid_path") from error
    if not relative.parts:
        raise ReviewStop("invalid_path")
    return relative.parts


def _open_input(root_fd, relative_parts):
    current_fd = os.dup(root_fd)
    try:
        for part in relative_parts[:-1]:
            next_fd = _open_directory(current_fd, part)
            os.close(current_fd)
            current_fd = next_fd
        try:
            file_descriptor = os.open(
                relative_parts[-1],
                _FILE_FLAGS,
                dir_fd=current_fd,
            )
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                raise ReviewStop("invalid_path") from error
            raise ReviewStop("unreadable_input") from error
        return file_descriptor
    finally:
        os.close(current_fd)


def _read_file(root, root_fd, input_path, max_bytes):
    relative_parts = _relative_parts(root, input_path)
    file_descriptor = _open_input(root_fd, relative_parts)
    try:
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ReviewStop("invalid_path")
        if before.st_size > max_bytes:
            raise ReviewStop("size_limit_exceeded")

        chunks = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(file_descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        content = b"".join(chunks)

        after = os.fstat(file_descriptor)
        if not stat.S_ISREG(after.st_mode):
            raise ReviewStop("invalid_path")
        if len(content) > max_bytes or after.st_size > max_bytes:
            raise ReviewStop("size_limit_exceeded")
        if before.st_size != after.st_size or len(content) != after.st_size:
            raise ReviewStop("unreadable_input")
        if not content or b"\x00" in content:
            raise ReviewStop("invalid_schema")
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ReviewStop("invalid_utf8") from error
        return content, (after.st_dev, after.st_ino)
    finally:
        os.close(file_descriptor)


def read_input_files(*, input_root, material, review_spec, results=None):
    """明示されたroot内の二件または三件の通常fileだけを安全に読む。"""

    root = _absolute_path(input_root)
    requested = (
        ("material", _absolute_path(material), MATERIAL_MAX_BYTES),
        ("review_spec", _absolute_path(review_spec), REVIEW_SPEC_MAX_BYTES),
    )
    if results is not None:
        requested += (("results", _absolute_path(results), RESULTS_MAX_BYTES),)

    root_fd = _open_root(root)
    try:
        contents = {}
        identities = set()
        for name, input_path, max_bytes in requested:
            content, identity = _read_file(root, root_fd, input_path, max_bytes)
            if identity in identities:
                raise ReviewStop("invalid_arguments")
            identities.add(identity)
            contents[name] = content
        return contents
    finally:
        os.close(root_fd)
