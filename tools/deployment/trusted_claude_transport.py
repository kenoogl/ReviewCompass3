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
_SOURCE_DISPATCH = Path(
    "tools/deployment/installed/trusted_review_send_dispatch.py"
)
_SOURCE_WRAPPER = Path("tools/deployment/installed/trusted-review-send")
_TARGET_DISPATCH = Path("tools/api_providers/trusted_review_send_dispatch.py")
_TARGET_BASE = Path("tools/api_providers/trusted_review_send.py")
_TARGET_WRAPPER = Path("trusted-review-send")
_BACKUP_WRAPPER = Path("trusted-review-send.pre-claude-bootstrap-v1")


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
    if not _regular(source_dispatch) or not _regular(source_wrapper):
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
    if base_matches and wrapper_current and dispatch_current:
        state = "ready"
    elif base_matches and wrapper_legacy and dispatch_digest in (
        None,
        source_dispatch_digest,
    ):
        state = "claude_capability_missing"
    else:
        state = "installed_mismatch"
    return {
        "schema_version": 1,
        "state": state,
        "base_sender_matches": base_matches,
        "wrapper_current": wrapper_current,
        "dispatch_current": dispatch_current,
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
    if status["state"] != "claude_capability_missing":
        raise ValueError("installed trusted entry mismatch")
    source_dispatch = source_root / _SOURCE_DISPATCH
    source_wrapper = source_root / _SOURCE_WRAPPER
    target_dispatch = install_root / _TARGET_DISPATCH
    target_wrapper = install_root / _TARGET_WRAPPER
    backup_wrapper = install_root / _BACKUP_WRAPPER
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
    dispatch_bytes = source_dispatch.read_bytes()
    if target_dispatch.exists() or target_dispatch.is_symlink():
        if not _regular(target_dispatch) or target_dispatch.read_bytes() != dispatch_bytes:
            raise ValueError("installed trusted dispatch mismatch")
    else:
        _write_new(target_dispatch, dispatch_bytes, 0o644)
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
