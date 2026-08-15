"""一件のSession記録を安全保存する製品契約試験。"""

import hashlib
import importlib
import json
import os
from pathlib import Path

import pytest


def _storage():
    return importlib.import_module("tools.session_logs.safe_storage")


def _write_raw(path, content=b"synthetic session\n"):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.write_bytes(content)
    path.chmod(0o600)
    return content


def _safe_result(raw_bytes):
    digest = hashlib.sha256(raw_bytes).hexdigest()
    return {
        "external_send_approved": False,
        "parse_issues": [],
        "provenance": {
            "end_line": 1,
            "redaction_rules_sha256": "1" * 64,
            "source_path": "session.jsonl",
            "source_sha256": digest,
            "start_line": 1,
            "summary_changed_files": [],
            "summary_commits": [],
            "summary_sha256": "2" * 64,
            "tool_version": "0.0.1",
            "transcript_sha256": "3" * 64,
        },
        "redaction_findings": [],
        "source_kind": "claude",
        "status": "ok",
        "summary": "safe summary",
        "summary_redaction_findings": [],
        "transcript": "safe transcript",
    }


def _roots(tmp_path):
    repository_root = tmp_path / "repository"
    raw_root = tmp_path / "raw"
    sensitive_root = tmp_path / "sensitive"
    data_root = tmp_path / "data"
    for directory in (
        repository_root,
        raw_root,
        sensitive_root,
        data_root,
    ):
        directory.mkdir(mode=0o700)
    (repository_root / ".git").mkdir(mode=0o700)
    raw_log = raw_root / "session.jsonl"
    raw_bytes = _write_raw(raw_log)
    return {
        "repository_root": repository_root.resolve(),
        "raw_root": raw_root.resolve(),
        "raw_log": raw_log.resolve(),
        "sensitive_root": sensitive_root.resolve(),
        "data_root": data_root.resolve(),
        "safe_result": _safe_result(raw_bytes),
    }


def _snapshot(root):
    entries = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries.append((relative, "symlink", os.readlink(path)))
        elif path.is_dir():
            entries.append((relative, "directory", path.stat().st_mode & 0o777))
        else:
            entries.append((relative, "file", path.read_bytes()))
    return tuple(entries)


def _assert_rejected_without_writes(storage, arguments, reason):
    snapshots = {
        name: _snapshot(arguments[name])
        for name in ("sensitive_root", "data_root")
        if isinstance(arguments[name], Path) and arguments[name].is_dir()
    }

    with pytest.raises(storage.StorageStop) as caught:
        storage.preflight_store(**arguments)

    assert caught.value.reason == reason
    for name, before in snapshots.items():
        assert _snapshot(arguments[name]) == before


@pytest.mark.parametrize(
    "missing_name",
    ("repository_root", "sensitive_root", "data_root"),
)
def test_preflight_rejects_missing_required_root_without_writes(
    tmp_path,
    missing_name,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    arguments[missing_name] = None

    _assert_rejected_without_writes(storage, arguments, "missing_root")


@pytest.mark.parametrize(
    "relative_name",
    (
        "repository_root",
        "raw_root",
        "raw_log",
        "sensitive_root",
        "data_root",
    ),
)
def test_preflight_rejects_non_absolute_path_without_writes(
    tmp_path,
    relative_name,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    arguments[relative_name] = Path("relative") / relative_name

    _assert_rejected_without_writes(storage, arguments, "invalid_path")


@pytest.mark.parametrize("relation", ("inside_repository", "same", "nested"))
def test_preflight_rejects_unseparated_storage_roots_without_writes(
    tmp_path,
    relation,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    if relation == "inside_repository":
        unsafe = arguments["repository_root"] / "unsafe"
        unsafe.mkdir(mode=0o700)
        arguments["sensitive_root"] = unsafe
        reason = "storage_root_inside_repository"
    elif relation == "same":
        arguments["data_root"] = arguments["sensitive_root"]
        reason = "storage_roots_overlap"
    else:
        nested = arguments["sensitive_root"] / "nested"
        nested.mkdir(mode=0o700)
        arguments["data_root"] = nested
        reason = "storage_roots_overlap"

    _assert_rejected_without_writes(storage, arguments, reason)


def test_preflight_rejects_storage_root_with_broad_mode_without_writes(
    tmp_path,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    arguments["sensitive_root"].chmod(0o750)

    _assert_rejected_without_writes(storage, arguments, "insecure_mode")


def test_preflight_rejects_storage_root_owned_by_another_user_without_writes(
    tmp_path,
    monkeypatch,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    effective_uid = os.geteuid()
    monkeypatch.setattr(storage.os, "geteuid", lambda: effective_uid + 1)

    _assert_rejected_without_writes(storage, arguments, "insecure_owner")


def test_preflight_rejects_storage_root_with_extended_acl_without_writes(
    tmp_path,
    monkeypatch,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    monkeypatch.setattr(storage, "_has_extended_acl", lambda file_descriptor: True)

    _assert_rejected_without_writes(storage, arguments, "insecure_acl")


def test_preflight_rejects_symlinked_storage_root_without_writes(tmp_path):
    storage = _storage()
    arguments = _roots(tmp_path)
    linked_root = tmp_path / "linked-sensitive"
    linked_root.symlink_to(arguments["sensitive_root"], target_is_directory=True)
    arguments["sensitive_root"] = linked_root.absolute()

    _assert_rejected_without_writes(storage, arguments, "symlink_not_allowed")


@pytest.mark.parametrize(
    ("change", "reason"),
    (
        ("stopped", "unsafe_source_result"),
        ("partial", "unsafe_source_result"),
        ("external_send", "external_send_not_allowed"),
        ("absolute_path", "absolute_path_remaining"),
    ),
)
def test_preflight_rejects_unsafe_formal_result_without_writes(
    tmp_path,
    change,
    reason,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    if change in {"stopped", "partial"}:
        arguments["safe_result"]["status"] = change
    elif change == "external_send":
        arguments["safe_result"]["external_send_approved"] = True
    else:
        arguments["safe_result"]["summary"] = "/private/secret/value"

    _assert_rejected_without_writes(storage, arguments, reason)


def test_preflight_rejects_raw_digest_mismatch_without_writes(tmp_path):
    storage = _storage()
    arguments = _roots(tmp_path)
    arguments["safe_result"]["provenance"]["source_sha256"] = "f" * 64

    _assert_rejected_without_writes(storage, arguments, "raw_digest_mismatch")


def test_preflight_accepts_safe_values_without_creating_files(tmp_path):
    storage = _storage()
    arguments = _roots(tmp_path)
    sensitive_before = _snapshot(arguments["sensitive_root"])
    data_before = _snapshot(arguments["data_root"])

    result = storage.preflight_store(**arguments)

    assert result == {
        "external_send_approved": False,
        "status": "ready",
    }
    assert _snapshot(arguments["sensitive_root"]) == sensitive_before
    assert _snapshot(arguments["data_root"]) == data_before
