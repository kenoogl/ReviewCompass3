"""一件のSession記録を固定fileへ安全保存する核。"""

import ctypes
import errno
import hashlib
import os
import stat
import sys
from datetime import datetime
from pathlib import Path

from tools.common.digests import canonical_json_bytes, sha256_hex
from tools.session_logs.read_only_entry import _contains_absolute_path


_ACL_TYPE_EXTENDED = 0x00000100
_ACL_FIRST_ENTRY = 0
_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
_FILE_FLAGS = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW

_DERIVED_KEYS = (
    "external_send_approved",
    "parse_issues",
    "redaction_findings",
    "source_kind",
    "status",
    "summary",
    "summary_redaction_findings",
    "transcript",
)
_PROVENANCE_KEYS = (
    "end_line",
    "redaction_rules_sha256",
    "source_sha256",
    "start_line",
    "summary_changed_files",
    "summary_commits",
    "summary_sha256",
    "tool_version",
    "transcript_sha256",
)
_SENSITIVE_FINAL_FILES = ("operation.json", "raw.bin")
_DATA_FINAL_FILES = (
    "operation.json",
    "derived.json",
    "manifest.json",
    "commit.json",
    "deleted.json",
)


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


def _validate_created_fd(file_descriptor, expected_kind, expected_mode):
    details = os.fstat(file_descriptor)
    if expected_kind == "directory":
        kind_matches = stat.S_ISDIR(details.st_mode)
    else:
        kind_matches = stat.S_ISREG(details.st_mode)
    if not kind_matches:
        raise StorageStop("invalid_file_type")
    if details.st_uid != os.geteuid():
        raise StorageStop("insecure_owner")
    if stat.S_IMODE(details.st_mode) != expected_mode:
        raise StorageStop("insecure_mode")
    if _has_extended_acl(file_descriptor):
        raise StorageStop("insecure_acl")


def _create_record_directory(root_fd, record_id):
    try:
        os.mkdir(record_id, mode=0o700, dir_fd=root_fd)
    except FileExistsError as error:
        raise StorageStop("record_exists") from error
    except OSError as error:
        raise StorageStop("storage_write_failed") from error
    os.fsync(root_fd)
    try:
        record_fd = os.open(record_id, _DIRECTORY_FLAGS, dir_fd=root_fd)
    except OSError as error:
        raise StorageStop("storage_write_failed") from error
    try:
        os.fchmod(record_fd, 0o700)
        _validate_created_fd(record_fd, "directory", 0o700)
    except Exception:
        os.close(record_fd)
        raise
    return record_fd


def _read_fd_bytes(file_descriptor):
    os.lseek(file_descriptor, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(file_descriptor, 1024 * 1024)
        if not chunk:
            break
        chunks.append(chunk)
    return b"".join(chunks)


def _write_all(file_descriptor, content):
    offset = 0
    while offset < len(content):
        written = os.write(file_descriptor, content[offset:])
        if written <= 0:
            raise StorageStop("storage_write_failed")
        offset += written


def _write_temp(directory_fd, temporary_name, content):
    try:
        file_descriptor = os.open(
            temporary_name,
            _FILE_FLAGS,
            0o600,
            dir_fd=directory_fd,
        )
    except OSError as error:
        raise StorageStop("storage_write_failed") from error
    try:
        os.fchmod(file_descriptor, 0o600)
        _validate_created_fd(file_descriptor, "file", 0o600)
        _write_all(file_descriptor, content)
        os.fsync(file_descriptor)
        if _read_fd_bytes(file_descriptor) != content:
            raise StorageStop("storage_verification_failed")
    finally:
        os.close(file_descriptor)


def _verify_final_file(directory_fd, final_name, expected):
    try:
        file_descriptor = os.open(
            final_name,
            os.O_RDONLY | os.O_NOFOLLOW,
            dir_fd=directory_fd,
        )
    except OSError as error:
        raise StorageStop("storage_verification_failed") from error
    try:
        _validate_created_fd(file_descriptor, "file", 0o600)
        if _read_fd_bytes(file_descriptor) != expected:
            raise StorageStop("storage_verification_failed")
    finally:
        os.close(file_descriptor)


def _publish_file(directory_fd, final_name, content):
    temporary_name = f"{final_name}.tmp"
    _write_temp(directory_fd, temporary_name, content)
    try:
        os.stat(final_name, dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise StorageStop("record_exists")
    try:
        os.rename(
            temporary_name,
            final_name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
        )
        os.fsync(directory_fd)
    except OSError as error:
        raise StorageStop("storage_write_failed") from error
    _verify_final_file(directory_fd, final_name, content)


def _replace_file(directory_fd, final_name, content):
    temporary_name = f"{final_name}.tmp"
    _write_temp(directory_fd, temporary_name, content)
    try:
        os.rename(
            temporary_name,
            final_name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
        )
        os.fsync(directory_fd)
    except OSError as error:
        raise StorageStop("storage_write_failed") from error
    _verify_final_file(directory_fd, final_name, content)


def _derived_result(safe_result):
    try:
        derived = {key: safe_result[key] for key in _DERIVED_KEYS}
        derived["provenance"] = {
            key: safe_result["provenance"][key]
            for key in _PROVENANCE_KEYS
        }
    except (KeyError, TypeError) as error:
        raise StorageStop("unsafe_source_result") from error
    if _contains_absolute_path(derived):
        raise StorageStop("absolute_path_remaining")
    return derived


def _timestamp(value, reason):
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise StorageStop(reason) from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise StorageStop(reason)
    return parsed


def _operation_document(
    *,
    state,
    operation_id,
    record_id,
    retention_until,
    expected_sha256,
):
    sensitive_temporary = [
        f"{name}.tmp" for name in _SENSITIVE_FINAL_FILES
    ]
    data_temporary = [f"{name}.tmp" for name in _DATA_FINAL_FILES]
    return {
        "expected_sha256": expected_sha256,
        "files": {
            "data": {
                "final": list(_DATA_FINAL_FILES),
                "temporary": data_temporary,
            },
            "sensitive": {
                "final": list(_SENSITIVE_FINAL_FILES),
                "temporary": sensitive_temporary,
            },
        },
        "operation_id": operation_id,
        "record_id": record_id,
        "retention_until": retention_until,
        "schema_version": 1,
        "state": state,
        "temporary_to_final": {
            name: name.removesuffix(".tmp")
            for name in sensitive_temporary + data_temporary
        },
    }


def _record_id(identity):
    return sha256_hex(canonical_json_bytes(identity))


def _open_existing_record(root_fd, record_id):
    try:
        record_fd = os.open(record_id, _DIRECTORY_FLAGS, dir_fd=root_fd)
    except FileNotFoundError:
        return None
    except OSError as error:
        raise StorageStop("record_conflict") from error
    try:
        _validate_created_fd(record_fd, "directory", 0o700)
    except Exception:
        os.close(record_fd)
        raise
    return record_fd


def _read_existing_file(record_fd, name):
    try:
        file_descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW,
            dir_fd=record_fd,
        )
    except OSError as error:
        raise StorageStop("record_conflict") from error
    try:
        _validate_created_fd(file_descriptor, "file", 0o600)
        return _read_fd_bytes(file_descriptor)
    finally:
        os.close(file_descriptor)


def _existing_store_outcome(
    *,
    sensitive_root_fd,
    data_root_fd,
    record_id,
    expected_sensitive,
    expected_data,
    incomplete_operation,
    stored_result,
):
    sensitive_record_fd = _open_existing_record(
        sensitive_root_fd,
        record_id,
    )
    data_record_fd = _open_existing_record(data_root_fd, record_id)
    if sensitive_record_fd is None or data_record_fd is None:
        if sensitive_record_fd is not None:
            os.close(sensitive_record_fd)
        if data_record_fd is not None:
            os.close(data_record_fd)
        raise StorageStop("record_busy")
    try:
        sensitive_names = set(os.listdir(sensitive_record_fd))
        data_names = set(os.listdir(data_record_fd))
        if "commit.json" not in data_names:
            return _resume_incomplete_store(
                sensitive_record_fd=sensitive_record_fd,
                data_record_fd=data_record_fd,
                sensitive_names=sensitive_names,
                data_names=data_names,
                expected_sensitive=expected_sensitive,
                expected_data=expected_data,
                incomplete_operation=incomplete_operation,
                stored_result=stored_result,
            )
        if sensitive_names != set(expected_sensitive) or data_names != set(expected_data):
            raise StorageStop("record_conflict")
        _verify_expected_files(sensitive_record_fd, expected_sensitive)
        _verify_expected_files(data_record_fd, expected_data)
    finally:
        os.close(sensitive_record_fd)
        os.close(data_record_fd)
    return {**stored_result, "status": "unchanged"}


def _verify_expected_files(record_fd, expected_files):
    for name, expected in expected_files.items():
        if _read_existing_file(record_fd, name) != expected:
            raise StorageStop("record_conflict")


def _finish_file(record_fd, final_name, expected):
    names = set(os.listdir(record_fd))
    temporary_name = f"{final_name}.tmp"
    if final_name in names:
        if temporary_name in names:
            raise StorageStop("record_conflict")
        if _read_existing_file(record_fd, final_name) != expected:
            raise StorageStop("record_conflict")
        return
    if temporary_name in names:
        if _read_existing_file(record_fd, temporary_name) != expected:
            raise StorageStop("record_conflict")
        os.rename(
            temporary_name,
            final_name,
            src_dir_fd=record_fd,
            dst_dir_fd=record_fd,
        )
        os.fsync(record_fd)
        _verify_final_file(record_fd, final_name, expected)
        return
    _publish_file(record_fd, final_name, expected)


def _resume_incomplete_store(
    *,
    sensitive_record_fd,
    data_record_fd,
    sensitive_names,
    data_names,
    expected_sensitive,
    expected_data,
    incomplete_operation,
    stored_result,
):
    allowed_sensitive = set(expected_sensitive) | {
        f"{name}.tmp" for name in expected_sensitive
    }
    allowed_data = set(expected_data) | {
        f"{name}.tmp" for name in expected_data
    }
    if not sensitive_names <= allowed_sensitive or not data_names <= allowed_data:
        raise StorageStop("record_conflict")

    operation_values = []
    for record_fd, names in (
        (sensitive_record_fd, sensitive_names),
        (data_record_fd, data_names),
    ):
        for name in ("operation.json", "operation.json.tmp"):
            if name in names:
                operation_values.append(_read_existing_file(record_fd, name))
    if not operation_values:
        if sensitive_names or data_names:
            raise StorageStop("record_unrecoverable")
        raise StorageStop("record_busy")
    committed_operation = expected_sensitive["operation.json"]
    if any(
        value not in {incomplete_operation, committed_operation}
        for value in operation_values
    ):
        raise StorageStop("record_conflict")

    for record_fd, names, expected_files in (
        (sensitive_record_fd, sensitive_names, expected_sensitive),
        (data_record_fd, data_names, expected_data),
    ):
        for name in names:
            if name.startswith("operation.json"):
                continue
            final_name = name.removesuffix(".tmp")
            expected = expected_files.get(final_name)
            if expected is None or _read_existing_file(record_fd, name) != expected:
                raise StorageStop("record_conflict")

    for record_fd in (sensitive_record_fd, data_record_fd):
        names = set(os.listdir(record_fd))
        if "operation.json.tmp" in names:
            temporary = _read_existing_file(record_fd, "operation.json.tmp")
            if temporary not in {incomplete_operation, committed_operation}:
                raise StorageStop("record_conflict")
            os.rename(
                "operation.json.tmp",
                "operation.json",
                src_dir_fd=record_fd,
                dst_dir_fd=record_fd,
            )
            os.fsync(record_fd)
        elif "operation.json" not in names:
            _publish_file(record_fd, "operation.json", incomplete_operation)
    _finish_file(sensitive_record_fd, "raw.bin", expected_sensitive["raw.bin"])
    _finish_file(data_record_fd, "derived.json", expected_data["derived.json"])
    _finish_file(data_record_fd, "manifest.json", expected_data["manifest.json"])
    if _read_existing_file(sensitive_record_fd, "operation.json") != committed_operation:
        _replace_file(sensitive_record_fd, "operation.json", committed_operation)
    if _read_existing_file(data_record_fd, "operation.json") != committed_operation:
        _replace_file(data_record_fd, "operation.json", committed_operation)
    _finish_file(data_record_fd, "commit.json", expected_data["commit.json"])
    return stored_result


def store_new(
    *,
    repository_root,
    raw_root,
    raw_log,
    sensitive_root,
    data_root,
    safe_result,
    stored_at,
    retention_until,
):
    """適合する新規一件を二領域へ書き、最後に確定印を置く。"""

    preflight_store(
        repository_root=repository_root,
        raw_root=raw_root,
        raw_log=raw_log,
        sensitive_root=sensitive_root,
        data_root=data_root,
        safe_result=safe_result,
    )
    stored_time = _timestamp(stored_at, "invalid_stored_at")
    retention_time = _timestamp(retention_until, "invalid_retention")
    if retention_time <= stored_time:
        raise StorageStop("invalid_retention")

    raw_root = _path(raw_root)
    raw_log = _path(raw_log)
    sensitive_root = _path(sensitive_root)
    data_root = _path(data_root)
    raw_bytes = _read_raw(raw_root, raw_log)
    raw_sha256 = sha256_hex(raw_bytes)
    if raw_sha256 != safe_result["provenance"]["source_sha256"]:
        raise StorageStop("raw_digest_mismatch")

    derived = _derived_result(safe_result)
    derived_bytes = canonical_json_bytes(derived)
    derived_sha256 = sha256_hex(derived_bytes)
    identity = {
        "derived_sha256": derived_sha256,
        "raw_sha256": raw_sha256,
        "redaction_rules_sha256": derived["provenance"][
            "redaction_rules_sha256"
        ],
        "retention_until": retention_until,
        "tool_version": derived["provenance"]["tool_version"],
    }
    record_id = _record_id(identity)
    manifest = {
        "derived_sha256": derived_sha256,
        "raw_sha256": raw_sha256,
        "record_id": record_id,
        "retention_until": retention_until,
        "schema_version": 1,
        "stored_at": stored_at,
    }
    manifest_bytes = canonical_json_bytes(manifest)
    manifest_sha256 = sha256_hex(manifest_bytes)
    operation_id = sha256_hex(canonical_json_bytes({
        "manifest_sha256": manifest_sha256,
        "record_id": record_id,
        "schema_version": 1,
    }))
    commit = {
        "committed": True,
        "derived_sha256": derived_sha256,
        "manifest_sha256": manifest_sha256,
        "operation_id": operation_id,
        "raw_sha256": raw_sha256,
        "record_id": record_id,
        "schema_version": 1,
    }
    commit_bytes = canonical_json_bytes(commit)
    expected_sha256 = {
        "commit.json": sha256_hex(commit_bytes),
        "derived.json": derived_sha256,
        "manifest.json": manifest_sha256,
        "raw.bin": raw_sha256,
    }
    incomplete_operation = canonical_json_bytes(_operation_document(
        state="incomplete",
        operation_id=operation_id,
        record_id=record_id,
        retention_until=retention_until,
        expected_sha256=expected_sha256,
    ))
    committed_operation = canonical_json_bytes(_operation_document(
        state="committed",
        operation_id=operation_id,
        record_id=record_id,
        retention_until=retention_until,
        expected_sha256=expected_sha256,
    ))

    stored_result = {
        "committed": True,
        "derived_sha256": derived_sha256,
        "external_send_approved": False,
        "manifest_sha256": manifest_sha256,
        "raw_sha256": raw_sha256,
        "record_id": record_id,
        "retention_until": retention_until,
        "status": "stored",
    }
    expected_sensitive = {
        "operation.json": committed_operation,
        "raw.bin": raw_bytes,
    }
    expected_data = {
        "commit.json": commit_bytes,
        "derived.json": derived_bytes,
        "manifest.json": manifest_bytes,
        "operation.json": committed_operation,
    }

    sensitive_root_fd = _open_directory_fd(sensitive_root)
    data_root_fd = _open_directory_fd(data_root)
    sensitive_record_fd = None
    data_record_fd = None
    try:
        try:
            sensitive_record_fd = _create_record_directory(
                sensitive_root_fd,
                record_id,
            )
        except StorageStop as error:
            if error.reason != "record_exists":
                raise
            return _existing_store_outcome(
                sensitive_root_fd=sensitive_root_fd,
                data_root_fd=data_root_fd,
                record_id=record_id,
                expected_sensitive=expected_sensitive,
                expected_data=expected_data,
                incomplete_operation=incomplete_operation,
                stored_result=stored_result,
            )
        _publish_file(
            sensitive_record_fd,
            "operation.json",
            incomplete_operation,
        )
        data_record_fd = _create_record_directory(data_root_fd, record_id)
        _publish_file(
            data_record_fd,
            "operation.json",
            incomplete_operation,
        )
        _publish_file(sensitive_record_fd, "raw.bin", raw_bytes)
        _publish_file(data_record_fd, "derived.json", derived_bytes)
        _publish_file(data_record_fd, "manifest.json", manifest_bytes)
        _replace_file(
            sensitive_record_fd,
            "operation.json",
            committed_operation,
        )
        _replace_file(
            data_record_fd,
            "operation.json",
            committed_operation,
        )
        _publish_file(data_record_fd, "commit.json", commit_bytes)
    finally:
        if sensitive_record_fd is not None:
            os.close(sensitive_record_fd)
        if data_record_fd is not None:
            os.close(data_record_fd)
        os.close(sensitive_root_fd)
        os.close(data_root_fd)

    return stored_result
