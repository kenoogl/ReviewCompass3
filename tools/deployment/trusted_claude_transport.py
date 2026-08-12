"""Claude用正式送信入口の配置状態を検査し、固定配布物だけを配置する。"""

import json
import os
from pathlib import Path
import sys

from tools.common import digests


INSTALL_ROOT = Path("/usr/local/libexec/reviewcompass")
EXPECTED_BASE_SENDER_SHA256 = (
    "623c08488ec984627355b1fc39556265ef4899ec90500238121b3803bdb4ffc2"
)
EXPECTED_LEGACY_WRAPPER_SHA256 = (
    "346e0638958d402ce9c0867a692f9356141b5ca4040f225e1e8aacfa61445893"
)
EXPECTED_PRIOR_DISPATCH_SHA256 = (
    "ee6bf62f8c5e57f1c262176cc92dabffae3f487debcfd04e2f1283b88a362ef7"
)
EXPECTED_EXECUTOR_PRIOR_DISPATCH_SHA256 = (
    "c1586a46d0d39fb681d8265305bbf32533b79afec12d2f13b15c73f7108bd267"
)
EXPECTED_MANIFEST_PRIOR_DISPATCH_SHA256 = (
    "b5f4dfaad2e1472ea9cc6761b0dfc449e24d85bf806fcb8523f27937e17fd24b"
)
_SOURCE_DISPATCH = Path(
    "tools/deployment/installed/trusted_review_send_dispatch.py"
)
_SOURCE_WRAPPER = Path("tools/deployment/installed/trusted-review-send")
_TARGET_DISPATCH = Path("tools/api_providers/trusted_review_send_dispatch.py")
_TARGET_BASE = Path("tools/api_providers/trusted_review_send.py")
_TARGET_WRAPPER = Path("trusted-review-send")
_BACKUP_WRAPPER = Path("trusted-review-send.pre-claude-bootstrap-v1")
TRUSTED_RUNTIME_FILES = (
    Path("tools/development/claude_bootstrap.py"),
    Path("tools/development/claude_implementation_route.py"),
    Path("tools/development/claude_implementation_executor.py"),
    Path("tools/bootstrap/immutable_result_store.py"),
    Path("tools/common/__init__.py"),
    Path("tools/common/digests.py"),
    Path("tools/common/errors.py"),
)
NEW_TRUSTED_RUNTIME_FILES = {
    Path("tools/development/claude_implementation_route.py"),
    Path("tools/development/claude_implementation_executor.py"),
    Path("tools/bootstrap/immutable_result_store.py"),
}
EXPECTED_PRIOR_RUNTIME_SHA256 = {
    Path("tools/development/claude_implementation_executor.py"): (
        "071ba8d034789ace02d037e5dbe1f1d0429d0fa14d7fd3161d99e031f19e9b49"
    ),
    Path("tools/development/claude_bootstrap.py"): (
        "14f352afb54353ccac45d84db2ce2a02c7c8a97204c0712651a5bd6218bc4133"
    ),
    Path("tools/common/__init__.py"): (
        "fdb99f627d54b0661d5b3d3f487c2a3e0266df9ac97ea642529c39e6b17774cd"
    ),
    Path("tools/common/digests.py"): (
        "fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7"
    ),
    Path("tools/common/errors.py"): (
        "1d2fefcc075080138f3ab9a8b19775e0ff0fb333e811d6918a06c6730236c4c0"
    ),
}


def _source_root():
    return Path(__file__).resolve().parents[2]


def _regular(path):
    return path.is_file() and not path.is_symlink()


def _digest(path):
    return digests.sha256_hex(path.read_bytes())


def deployment_status(*, install_root=INSTALL_ROOT, source_root=None):
    source_root = _source_root() if source_root is None else Path(source_root)
    install_root = Path(install_root)
    source_dispatch = source_root / _SOURCE_DISPATCH
    source_wrapper = source_root / _SOURCE_WRAPPER
    target_dispatch = install_root / _TARGET_DISPATCH
    target_base = install_root / _TARGET_BASE
    target_wrapper = install_root / _TARGET_WRAPPER
    source_runtime = [source_root / path for path in TRUSTED_RUNTIME_FILES]
    if (
        not _regular(source_dispatch)
        or not _regular(source_wrapper)
        or any(not _regular(path) for path in source_runtime)
        or not set(TRUSTED_RUNTIME_FILES) - NEW_TRUSTED_RUNTIME_FILES
        <= set(EXPECTED_PRIOR_RUNTIME_SHA256)
        or not set(EXPECTED_PRIOR_RUNTIME_SHA256) <= set(TRUSTED_RUNTIME_FILES)
    ):
        return {"schema_version": 1, "state": "source_invalid"}
    source_dispatch_digest = _digest(source_dispatch)
    source_wrapper_digest = _digest(source_wrapper)
    base_matches = (
        _regular(target_base)
        and _digest(target_base) == EXPECTED_BASE_SENDER_SHA256
    )
    wrapper_digest = _digest(target_wrapper) if _regular(target_wrapper) else None
    dispatch_digest = (
        _digest(target_dispatch) if _regular(target_dispatch) else None
    )
    wrapper_current = wrapper_digest == source_wrapper_digest
    wrapper_legacy = wrapper_digest == EXPECTED_LEGACY_WRAPPER_SHA256
    dispatch_current = dispatch_digest == source_dispatch_digest
    runtime_files_current = all(
        _regular(install_root / relative)
        and (install_root / relative).read_bytes()
        == (source_root / relative).read_bytes()
        for relative in TRUSTED_RUNTIME_FILES
    )
    runtime_files_absent_or_current = all(
        (
            not (install_root / relative).exists()
            and not (install_root / relative).is_symlink()
        )
        or (
            _regular(install_root / relative)
            and (install_root / relative).read_bytes()
            == (source_root / relative).read_bytes()
        )
        for relative in TRUSTED_RUNTIME_FILES
    )
    runtime_files_known = all(
        (
            relative in NEW_TRUSTED_RUNTIME_FILES
            and not (install_root / relative).exists()
            and not (install_root / relative).is_symlink()
        )
        or (
            _regular(install_root / relative)
            and _digest(install_root / relative)
            in {
                _digest(source_root / relative),
                EXPECTED_PRIOR_RUNTIME_SHA256.get(relative),
            }
        )
        for relative in TRUSTED_RUNTIME_FILES
    )
    if (
        base_matches
        and wrapper_current
        and dispatch_current
        and runtime_files_current
    ):
        state = "ready"
    elif (
        base_matches
        and wrapper_legacy
        and dispatch_digest in (None, source_dispatch_digest)
        and runtime_files_absent_or_current
    ):
        state = "claude_capability_missing"
    elif (
        base_matches
        and wrapper_current
        and dispatch_digest in (
            source_dispatch_digest,
            EXPECTED_PRIOR_DISPATCH_SHA256,
            EXPECTED_EXECUTOR_PRIOR_DISPATCH_SHA256,
            EXPECTED_MANIFEST_PRIOR_DISPATCH_SHA256,
        )
        and runtime_files_known
    ):
        state = "trusted_runtime_update_required"
    else:
        state = "installed_mismatch"
    return {
        "schema_version": 1,
        "state": state,
        "base_sender_matches": base_matches,
        "wrapper_current": wrapper_current,
        "dispatch_current": dispatch_current,
        "runtime_files_current": runtime_files_current,
    }


def _write_new(path, data, mode):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    path.chmod(mode)


def _replace(path, data, mode):
    temporary = path.with_name(f".{path.name}.claude-bootstrap.tmp")
    if temporary.exists() or temporary.is_symlink():
        raise ValueError("trusted transport temporary path exists")
    try:
        _write_new(temporary, data, mode)
        os.replace(temporary, path)
        path.chmod(mode)
    finally:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def _ensure_directory(path):
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_dir():
            raise ValueError("trusted transport directory mismatch")
        return
    path.mkdir(mode=0o755)


def install_trusted_transport(
    *,
    install_root=INSTALL_ROOT,
    source_root=None,
    effective_user_id=None,
):
    effective_user_id = os.geteuid() if effective_user_id is None else effective_user_id
    if effective_user_id != 0:
        raise PermissionError("administrator privileges required")
    source_root = _source_root() if source_root is None else Path(source_root)
    install_root = Path(install_root)
    status = deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    if status["state"] == "ready":
        return status
    if status["state"] not in (
        "claude_capability_missing",
        "trusted_runtime_update_required",
    ):
        raise ValueError("installed trusted entry mismatch")
    updating_runtime = status["state"] == "trusted_runtime_update_required"
    source_dispatch = source_root / _SOURCE_DISPATCH
    source_wrapper = source_root / _SOURCE_WRAPPER
    target_dispatch = install_root / _TARGET_DISPATCH
    target_wrapper = install_root / _TARGET_WRAPPER
    backup_wrapper = install_root / _BACKUP_WRAPPER
    if updating_runtime:
        if (
            not _regular(backup_wrapper)
            or _digest(backup_wrapper) != EXPECTED_LEGACY_WRAPPER_SHA256
        ):
            raise ValueError("trusted entry backup mismatch")
    else:
        legacy_bytes = target_wrapper.read_bytes()
        if digests.sha256_hex(legacy_bytes) != EXPECTED_LEGACY_WRAPPER_SHA256:
            raise ValueError("installed trusted entry mismatch")
        if backup_wrapper.exists() or backup_wrapper.is_symlink():
            if (
                not _regular(backup_wrapper)
                or _digest(backup_wrapper) != EXPECTED_LEGACY_WRAPPER_SHA256
            ):
                raise ValueError("trusted entry backup mismatch")
        else:
            _write_new(backup_wrapper, legacy_bytes, 0o755)
    _ensure_directory(install_root / "tools/development")
    _ensure_directory(install_root / "tools/bootstrap")
    _ensure_directory(install_root / "tools/common")
    for relative in TRUSTED_RUNTIME_FILES:
        source = source_root / relative
        target = install_root / relative
        source_bytes = source.read_bytes()
        if target.exists() or target.is_symlink():
            if not _regular(target):
                raise ValueError("installed trusted runtime mismatch")
            if target.read_bytes() == source_bytes:
                continue
            if not updating_runtime or _digest(target) != (
                EXPECTED_PRIOR_RUNTIME_SHA256.get(relative)
            ):
                raise ValueError("installed trusted runtime mismatch")
            _replace(target, source_bytes, 0o644)
        else:
            _write_new(target, source_bytes, 0o644)
    dispatch_bytes = source_dispatch.read_bytes()
    if target_dispatch.exists() or target_dispatch.is_symlink():
        if not _regular(target_dispatch):
            raise ValueError("installed trusted dispatch mismatch")
        if target_dispatch.read_bytes() != dispatch_bytes:
            if (
                not updating_runtime
                or _digest(target_dispatch)
                not in (
                    EXPECTED_PRIOR_DISPATCH_SHA256,
                    EXPECTED_EXECUTOR_PRIOR_DISPATCH_SHA256,
                    EXPECTED_MANIFEST_PRIOR_DISPATCH_SHA256,
                )
            ):
                raise ValueError("installed trusted dispatch mismatch")
            _replace(target_dispatch, dispatch_bytes, 0o644)
    else:
        _write_new(target_dispatch, dispatch_bytes, 0o644)
    if not updating_runtime:
        _replace(target_wrapper, source_wrapper.read_bytes(), 0o755)
    result = deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    if result["state"] != "ready":
        raise ValueError("trusted transport post-write verification failed")
    return result


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        if arguments == ["status"]:
            result = deployment_status()
            exit_code = 0 if result["state"] == "ready" else 2
        elif arguments == ["install"]:
            result = install_trusted_transport()
            exit_code = 0
        else:
            result = {"schema_version": 1, "state": "input_invalid"}
            exit_code = 2
    except (OSError, PermissionError, ValueError) as error:
        result = {
            "schema_version": 1,
            "state": "stopped",
            "reason": str(error),
        }
        exit_code = 2
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
