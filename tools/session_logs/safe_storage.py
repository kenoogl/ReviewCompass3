"""一件のSession記録を固定fileへ安全保存する核。"""

import ctypes
import errno
import hashlib
import os
import stat
import sys
from pathlib import Path

from tools.session_logs.read_only_entry import _contains_absolute_path


_ACL_TYPE_EXTENDED = 0x00000100
_ACL_FIRST_ENTRY = 0
_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


class StorageStop(Exception):
    """保存境界を安全に満たせない。"""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


def _path(value):
    try:
        path = Path(value)
    except TypeError as error:
        raise StorageStop("invalid_path") from error
    if not path.is_absolute() or ".." in path.parts:
        raise StorageStop("invalid_path")
    return Path(os.path.normpath(path))


def _open_directory_fd(path):
    current_fd = os.open("/", _DIRECTORY_FLAGS)
    try:
        for part in path.parts[1:]:
            try:
                entry = os.stat(
                    part,
                    dir_fd=current_fd,
                    follow_symlinks=False,
                )
            except OSError as error:
                raise StorageStop("unreadable_path") from error
            if stat.S_ISLNK(entry.st_mode):
                raise StorageStop("symlink_not_allowed")
            try:
                next_fd = os.open(part, _DIRECTORY_FLAGS, dir_fd=current_fd)
            except OSError as error:
                if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                    raise StorageStop("symlink_not_allowed") from error
                raise StorageStop("unreadable_path") from error
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _has_extended_acl(file_descriptor):
    if sys.platform != "darwin":
        raise StorageStop("acl_check_unavailable")
    try:
        library = ctypes.CDLL(None, use_errno=True)
        acl_get_fd_np = library.acl_get_fd_np
        acl_get_entry = library.acl_get_entry
        acl_free = library.acl_free
    except (AttributeError, OSError) as error:
        raise StorageStop("acl_check_unavailable") from error

    acl_get_fd_np.argtypes = (ctypes.c_int, ctypes.c_int)
    acl_get_fd_np.restype = ctypes.c_void_p
    acl_get_entry.argtypes = (
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_void_p),
    )
    acl_get_entry.restype = ctypes.c_int
    acl_free.argtypes = (ctypes.c_void_p,)
    acl_free.restype = ctypes.c_int

    ctypes.set_errno(0)
    acl = acl_get_fd_np(file_descriptor, _ACL_TYPE_EXTENDED)
    if not acl:
        if ctypes.get_errno() in {0, errno.ENOENT}:
            return False
        raise StorageStop("acl_check_unavailable")
    try:
        entry = ctypes.c_void_p()
        ctypes.set_errno(0)
        result = acl_get_entry(acl, _ACL_FIRST_ENTRY, ctypes.byref(entry))
        if result == 0:
            return True
        if ctypes.get_errno() in {0, errno.ENOENT}:
            return False
        raise StorageStop("acl_check_unavailable")
    finally:
        acl_free(acl)


def _validate_storage_root(path):
    file_descriptor = _open_directory_fd(path)
    try:
        details = os.fstat(file_descriptor)
        if not stat.S_ISDIR(details.st_mode):
            raise StorageStop("invalid_path")
        if details.st_uid != os.geteuid():
            raise StorageStop("insecure_owner")
        if stat.S_IMODE(details.st_mode) != 0o700:
            raise StorageStop("insecure_mode")
        if _has_extended_acl(file_descriptor):
            raise StorageStop("insecure_acl")
    finally:
        os.close(file_descriptor)


def _validate_repository(path):
    file_descriptor = _open_directory_fd(path)
    try:
        try:
            git_entry = os.stat(
                ".git",
                dir_fd=file_descriptor,
                follow_symlinks=False,
            )
        except OSError as error:
            raise StorageStop("invalid_repository") from error
        if not stat.S_ISDIR(git_entry.st_mode):
            raise StorageStop("invalid_repository")
    finally:
        os.close(file_descriptor)


def _is_within(path, possible_parent):
    return path == possible_parent or possible_parent in path.parents


def _validate_separation(repository_root, sensitive_root, data_root):
    if _is_within(sensitive_root, repository_root) or _is_within(
        data_root,
        repository_root,
    ):
        raise StorageStop("storage_root_inside_repository")
    if _is_within(sensitive_root, data_root) or _is_within(
        data_root,
        sensitive_root,
    ):
        raise StorageStop("storage_roots_overlap")


def _validate_safe_result(safe_result):
    if not isinstance(safe_result, dict) or safe_result.get("status") != "ok":
        raise StorageStop("unsafe_source_result")
    if safe_result.get("external_send_approved") is not False:
        raise StorageStop("external_send_not_allowed")
    if _contains_absolute_path(safe_result):
        raise StorageStop("absolute_path_remaining")


def _read_raw(raw_root, raw_log):
    try:
        relative = raw_log.relative_to(raw_root)
    except ValueError as error:
        raise StorageStop("source_outside_root") from error
    if not relative.parts or ".." in relative.parts:
        raise StorageStop("invalid_path")

    current_fd = _open_directory_fd(raw_root)
    try:
        for part in relative.parts[:-1]:
            try:
                entry = os.stat(
                    part,
                    dir_fd=current_fd,
                    follow_symlinks=False,
                )
            except OSError as error:
                raise StorageStop("unreadable_source") from error
            if stat.S_ISLNK(entry.st_mode):
                raise StorageStop("symlink_not_allowed")
            try:
                next_fd = os.open(part, _DIRECTORY_FLAGS, dir_fd=current_fd)
            except OSError as error:
                raise StorageStop("unreadable_source") from error
            os.close(current_fd)
            current_fd = next_fd

        try:
            file_descriptor = os.open(
                relative.parts[-1],
                os.O_RDONLY | os.O_NOFOLLOW,
                dir_fd=current_fd,
            )
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                raise StorageStop("symlink_not_allowed") from error
            raise StorageStop("unreadable_source") from error
        try:
            details = os.fstat(file_descriptor)
            if not stat.S_ISREG(details.st_mode):
                raise StorageStop("unreadable_source")
            chunks = []
            while True:
                chunk = os.read(file_descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            return b"".join(chunks)
        finally:
            os.close(file_descriptor)
    finally:
        os.close(current_fd)


def preflight_store(
    *,
    repository_root,
    raw_root,
    raw_log,
    sensitive_root,
    data_root,
    safe_result,
):
    """保存前提を検査し、書込みを行わず準備結果だけを返す。"""

    if any(
        value is None
        for value in (repository_root, sensitive_root, data_root)
    ):
        raise StorageStop("missing_root")

    repository_root = _path(repository_root)
    raw_root = _path(raw_root)
    raw_log = _path(raw_log)
    sensitive_root = _path(sensitive_root)
    data_root = _path(data_root)

    _validate_separation(repository_root, sensitive_root, data_root)
    _validate_repository(repository_root)
    _validate_storage_root(sensitive_root)
    _validate_storage_root(data_root)
    _validate_safe_result(safe_result)

    raw_bytes = _read_raw(raw_root, raw_log)
    source_sha256 = safe_result.get("provenance", {}).get("source_sha256")
    if hashlib.sha256(raw_bytes).hexdigest() != source_sha256:
        raise StorageStop("raw_digest_mismatch")

    return {
        "external_send_approved": False,
        "status": "ready",
    }
