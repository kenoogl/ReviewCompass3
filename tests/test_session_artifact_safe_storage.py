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


def _canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _stored_json(path):
    content = path.read_bytes()
    value = json.loads(content)
    assert content == _canonical_bytes(value)
    return value


def test_store_new_commits_fixed_files_with_safe_content(
    tmp_path,
    monkeypatch,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    raw_secret = b"raw-secret-value\n"
    arguments["raw_log"].write_bytes(raw_secret)
    arguments["safe_result"] = _safe_result(raw_secret)
    arguments["safe_result"]["provenance"]["source_path"] = "session.jsonl"
    published = []
    original_publish = getattr(storage, "_publish_file", None)

    def recording_publish(directory_fd, final_name, content):
        published.append(final_name)
        return original_publish(directory_fd, final_name, content)

    monkeypatch.setattr(
        storage,
        "_publish_file",
        recording_publish,
        raising=False,
    )

    result = storage.store_new(
        **arguments,
        stored_at="2026-08-15T00:00:00+00:00",
        retention_until="2026-08-16T00:00:00+00:00",
    )

    assert result["status"] == "stored"
    assert result["committed"] is True
    assert result["external_send_approved"] is False
    assert published[-1] == "commit.json"
    record_id = result["record_id"]
    assert len(record_id) == 64
    assert set(record_id) <= set("0123456789abcdef")

    sensitive_record = arguments["sensitive_root"] / record_id
    data_record = arguments["data_root"] / record_id
    assert {path.name for path in sensitive_record.iterdir()} == {
        "operation.json",
        "raw.bin",
    }
    assert {path.name for path in data_record.iterdir()} == {
        "commit.json",
        "derived.json",
        "manifest.json",
        "operation.json",
    }
    assert not tuple(sensitive_record.glob("*.tmp"))
    assert not tuple(data_record.glob("*.tmp"))

    for directory in (sensitive_record, data_record):
        details = directory.stat()
        assert details.st_uid == os.geteuid()
        assert details.st_mode & 0o777 == 0o700
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            assert storage._has_extended_acl(descriptor) is False
        finally:
            os.close(descriptor)
        for path in directory.iterdir():
            details = path.stat()
            assert path.is_file()
            assert details.st_uid == os.geteuid()
            assert details.st_mode & 0o777 == 0o600
            descriptor = os.open(path, os.O_RDONLY)
            try:
                assert storage._has_extended_acl(descriptor) is False
            finally:
                os.close(descriptor)

    assert (sensitive_record / "raw.bin").read_bytes() == raw_secret
    derived = _stored_json(data_record / "derived.json")
    manifest = _stored_json(data_record / "manifest.json")
    sensitive_operation = _stored_json(sensitive_record / "operation.json")
    data_operation = _stored_json(data_record / "operation.json")
    commit = _stored_json(data_record / "commit.json")
    assert sensitive_operation == data_operation
    assert sensitive_operation["state"] == "committed"
    assert commit["committed"] is True
    assert commit["record_id"] == record_id

    assert set(derived) == {
        "external_send_approved",
        "parse_issues",
        "provenance",
        "redaction_findings",
        "source_kind",
        "status",
        "summary",
        "summary_redaction_findings",
        "transcript",
    }
    assert set(derived["provenance"]) == {
        "end_line",
        "redaction_rules_sha256",
        "source_sha256",
        "start_line",
        "summary_changed_files",
        "summary_commits",
        "summary_sha256",
        "tool_version",
        "transcript_sha256",
    }
    assert "source_path" not in derived["provenance"]

    raw_sha256 = hashlib.sha256(raw_secret).hexdigest()
    derived_sha256 = hashlib.sha256(
        (data_record / "derived.json").read_bytes()
    ).hexdigest()
    manifest_sha256 = hashlib.sha256(
        (data_record / "manifest.json").read_bytes()
    ).hexdigest()
    assert result["raw_sha256"] == raw_sha256
    assert result["derived_sha256"] == derived_sha256
    assert result["manifest_sha256"] == manifest_sha256
    assert manifest["raw_sha256"] == raw_sha256
    assert manifest["derived_sha256"] == derived_sha256
    assert commit["manifest_sha256"] == manifest_sha256
    assert commit["operation_id"] == sensitive_operation["operation_id"]

    visible = _canonical_bytes({
        "result": result,
        "derived": derived,
        "manifest": manifest,
        "operation": sensitive_operation,
        "commit": commit,
        "sensitive_names": sorted(path.name for path in sensitive_record.iterdir()),
        "data_names": sorted(path.name for path in data_record.iterdir()),
    }).decode("utf-8")
    for forbidden in (
        "raw-secret-value",
        "session.jsonl",
        "synthetic-home-value",
        "synthetic-user-value",
        "synthetic-host-value",
        str(arguments["raw_root"]),
        str(arguments["sensitive_root"]),
        str(arguments["data_root"]),
    ):
        assert forbidden not in visible


@pytest.mark.parametrize(
    "reason",
    ("insecure_owner", "insecure_mode", "insecure_acl", "invalid_file_type"),
)
def test_store_new_does_not_commit_when_created_object_is_unsafe(
    tmp_path,
    monkeypatch,
    reason,
):
    storage = _storage()
    arguments = _roots(tmp_path)

    def reject_created_object(file_descriptor, expected_kind, expected_mode):
        raise storage.StorageStop(reason)

    monkeypatch.setattr(
        storage,
        "_validate_created_fd",
        reject_created_object,
        raising=False,
    )

    with pytest.raises(storage.StorageStop) as caught:
        storage.store_new(
            **arguments,
            stored_at="2026-08-15T00:00:00+00:00",
            retention_until="2026-08-16T00:00:00+00:00",
        )

    assert caught.value.reason == reason
    assert not tuple(arguments["sensitive_root"].rglob("commit.json"))
    assert not tuple(arguments["data_root"].rglob("commit.json"))
