"""一件のSession記録を安全保存する製品契約試験。"""

import hashlib
import importlib
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
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


def test_manifest_and_operation_match_independent_contract_oracle(tmp_path):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    manifest = _stored_json(data_record / "manifest.json")
    operation = _stored_json(sensitive_record / "operation.json")

    assert set(manifest) == {
        "derived_sha256",
        "prior_contract_id",
        "prior_contract_sha256",
        "prior_contract_version",
        "raw_sha256",
        "read_only_entry_version",
        "record_id",
        "redaction_rules_sha256",
        "retention_until",
        "schema_version",
        "storage_writer_version",
        "stored_at",
    }
    assert manifest["prior_contract_id"] == (
        "TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001"
    )
    assert manifest["prior_contract_sha256"] == (
        "20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b"
    )
    assert manifest["prior_contract_version"] == 1
    assert manifest["read_only_entry_version"] == "0.0.1"
    assert manifest["redaction_rules_sha256"] == "1" * 64
    assert manifest["storage_writer_version"] == 1
    assert operation["files"] == {
        "data": {
            "final": [
                "operation.json",
                "derived.json",
                "manifest.json",
                "commit.json",
                "deleted.json",
            ],
            "temporary": [
                "operation.json.tmp",
                "derived.json.tmp",
                "manifest.json.tmp",
                "commit.json.tmp",
                "deleted.json.tmp",
            ],
        },
        "sensitive": {
            "final": ["operation.json", "raw.bin"],
            "temporary": ["operation.json.tmp", "raw.bin.tmp"],
        },
    }


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


def _record_snapshot(record_directory):
    return {
        path.name: (
            path.read_bytes(),
            path.stat().st_ino,
            path.stat().st_mtime_ns,
        )
        for path in record_directory.iterdir()
    }


def test_store_new_returns_unchanged_without_touching_existing_record(tmp_path):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    first = storage.store_new(**arguments, **times)
    record_id = first["record_id"]
    sensitive_record = arguments["sensitive_root"] / record_id
    data_record = arguments["data_root"] / record_id
    before = (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    )

    second = storage.store_new(**arguments, **times)

    assert second == {**first, "status": "unchanged"}
    assert (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    ) == before


def test_store_new_rejects_different_content_for_existing_record_id(
    tmp_path,
    monkeypatch,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    first = storage.store_new(**arguments, **times)
    record_id = first["record_id"]
    sensitive_record = arguments["sensitive_root"] / record_id
    data_record = arguments["data_root"] / record_id
    before = (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    )
    different = b"different raw bytes\n"
    arguments["raw_log"].write_bytes(different)
    arguments["safe_result"] = _safe_result(different)
    monkeypatch.setattr(
        storage,
        "_record_id",
        lambda identity: record_id,
        raising=False,
    )

    with pytest.raises(storage.StorageStop) as caught:
        storage.store_new(**arguments, **times)

    assert caught.value.reason == "record_conflict"
    assert (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    ) == before


def test_store_new_concurrent_calls_do_not_both_succeed(
    tmp_path,
    monkeypatch,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    barrier = threading.Barrier(2)
    local = threading.local()
    original_create = storage._create_record_directory

    def synchronized_create(root_fd, record_id):
        if not getattr(local, "first_create_seen", False):
            local.first_create_seen = True
            barrier.wait(timeout=5)
        return original_create(root_fd, record_id)

    monkeypatch.setattr(storage, "_create_record_directory", synchronized_create)

    def attempt():
        try:
            return storage.store_new(**arguments, **times)["status"]
        except storage.StorageStop as error:
            return error.reason

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(lambda ignored: attempt(), range(2)))

    assert outcomes.count("stored") == 1
    assert outcomes.count("record_busy") == 1


@pytest.mark.parametrize(
    "fault_point",
    ("raw.bin", "derived.json", "manifest.json", "before_commit", "raw.bin.tmp"),
)
def test_store_new_resumes_matching_incomplete_record(
    tmp_path,
    monkeypatch,
    fault_point,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    original_publish = storage._publish_file
    original_write_temp = storage._write_temp
    injected = False

    def failing_publish(directory_fd, final_name, content):
        nonlocal injected
        if fault_point == "before_commit" and final_name == "commit.json":
            injected = True
            raise storage.StorageStop("injected_failure")
        result = original_publish(directory_fd, final_name, content)
        if not injected and final_name == fault_point:
            injected = True
            raise storage.StorageStop("injected_failure")
        return result

    def failing_write_temp(directory_fd, temporary_name, content):
        nonlocal injected
        result = original_write_temp(directory_fd, temporary_name, content)
        if not injected and temporary_name == fault_point:
            injected = True
            raise storage.StorageStop("injected_failure")
        return result

    monkeypatch.setattr(storage, "_publish_file", failing_publish)
    monkeypatch.setattr(storage, "_write_temp", failing_write_temp)
    with pytest.raises(storage.StorageStop) as caught:
        storage.store_new(**arguments, **times)
    assert caught.value.reason == "injected_failure"
    assert injected is True
    assert not tuple(arguments["data_root"].rglob("commit.json"))

    monkeypatch.setattr(storage, "_publish_file", original_publish)
    monkeypatch.setattr(storage, "_write_temp", original_write_temp)
    result = storage.store_new(**arguments, **times)

    assert result["status"] == "stored"
    record_id = result["record_id"]
    assert (arguments["data_root"] / record_id / "commit.json").is_file()
    assert not tuple((arguments["sensitive_root"] / record_id).glob("*.tmp"))
    assert not tuple((arguments["data_root"] / record_id).glob("*.tmp"))


@pytest.mark.parametrize(
    ("corruption", "reason"),
    (
        ("unknown_file", "record_conflict"),
        ("changed_operation", "record_conflict"),
        ("missing_operation", "record_unrecoverable"),
    ),
)
def test_store_new_does_not_guess_unsafe_incomplete_record(
    tmp_path,
    monkeypatch,
    corruption,
    reason,
):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    original_publish = storage._publish_file

    def stop_after_raw(directory_fd, final_name, content):
        result = original_publish(directory_fd, final_name, content)
        if final_name == "raw.bin":
            raise storage.StorageStop("injected_failure")
        return result

    monkeypatch.setattr(storage, "_publish_file", stop_after_raw)
    with pytest.raises(storage.StorageStop):
        storage.store_new(**arguments, **times)
    monkeypatch.setattr(storage, "_publish_file", original_publish)
    sensitive_record = next(arguments["sensitive_root"].iterdir())
    data_record = arguments["data_root"] / sensitive_record.name
    if corruption == "unknown_file":
        unknown = data_record / "unknown.bin"
        unknown.write_bytes(b"unknown")
        unknown.chmod(0o600)
    elif corruption == "changed_operation":
        (data_record / "operation.json").write_bytes(b"{}")
    else:
        (sensitive_record / "operation.json").unlink()
        (data_record / "operation.json").unlink()
    before = (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    )

    with pytest.raises(storage.StorageStop) as caught:
        storage.store_new(**arguments, **times)

    assert caught.value.reason == reason
    assert (
        _record_snapshot(sensitive_record),
        _record_snapshot(data_record),
    ) == before


def _store_fixture(storage, tmp_path):
    arguments = _roots(tmp_path)
    result = storage.store_new(
        **arguments,
        stored_at="2026-08-15T00:00:00+00:00",
        retention_until="2026-08-16T00:00:00+00:00",
    )
    return arguments, result


def test_load_derived_returns_only_verified_unexpired_derived_value(tmp_path):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)

    result = storage.load_derived(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        current_at="2026-08-15T12:00:00+00:00",
    )

    assert result["status"] == "loaded"
    assert result["record_id"] == stored["record_id"]
    assert result["external_send_approved"] is False
    assert result["derived"]["transcript"] == "safe transcript"
    serialized = _canonical_bytes(result).decode("utf-8")
    assert "source_path" not in serialized
    assert str(arguments["sensitive_root"]) not in serialized
    assert str(arguments["data_root"]) not in serialized


def test_load_derived_refuses_expired_record_without_deleting(tmp_path):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    result = storage.load_derived(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        current_at="2026-08-16T00:00:01+00:00",
    )

    assert result == {
        "external_send_approved": False,
        "record_id": stored["record_id"],
        "status": "expired_pending_deletion",
    }
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize(
    ("area", "name"),
    (
        ("sensitive", "raw.bin"),
        ("data", "derived.json"),
        ("data", "manifest.json"),
        ("sensitive", "operation.json"),
        ("data", "commit.json"),
    ),
)
def test_load_derived_rejects_any_modified_fixed_file(
    tmp_path,
    area,
    name,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    root = arguments[f"{area}_root"] / stored["record_id"]
    path = root / name
    content = path.read_bytes()
    path.write_bytes(bytes([content[0] ^ 1]) + content[1:])
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        storage.load_derived(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
            current_at="2026-08-15T12:00:00+00:00",
        )

    assert caught.value.reason == "record_integrity_failed"
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize("state", ("committed", "incomplete"))
def test_plan_delete_is_deterministic_and_read_only(tmp_path, monkeypatch, state):
    storage = _storage()
    arguments = _roots(tmp_path)
    times = {
        "stored_at": "2026-08-15T00:00:00+00:00",
        "retention_until": "2026-08-16T00:00:00+00:00",
    }
    if state == "committed":
        stored = storage.store_new(**arguments, **times)
        record_id = stored["record_id"]
    else:
        original_publish = storage._publish_file

        def stop_after_raw(directory_fd, final_name, content):
            result = original_publish(directory_fd, final_name, content)
            if final_name == "raw.bin":
                raise storage.StorageStop("injected_failure")
            return result

        monkeypatch.setattr(storage, "_publish_file", stop_after_raw)
        with pytest.raises(storage.StorageStop):
            storage.store_new(**arguments, **times)
        monkeypatch.setattr(storage, "_publish_file", original_publish)
        record_id = next(arguments["sensitive_root"].iterdir()).name
    sensitive_record = arguments["sensitive_root"] / record_id
    data_record = arguments["data_root"] / record_id
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    first = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=record_id,
    )
    second = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=record_id,
    )

    assert first == second
    confirmation = first.pop("confirmation_sha256")
    assert confirmation == hashlib.sha256(_canonical_bytes(first)).hexdigest()
    assert first["status"] == "delete_planned"
    assert first["state"] == state
    assert first["record_id"] == record_id
    assert first["target_count"] == len(first["targets"])
    assert all(set(target) == {"area", "kind", "name"} for target in first["targets"])
    serialized = _canonical_bytes(first).decode("utf-8")
    assert str(arguments["sensitive_root"]) not in serialized
    assert str(arguments["data_root"]) not in serialized
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


def test_plan_delete_rejects_unknown_file_without_changes(tmp_path):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    unknown = data_record / "unknown.bin"
    unknown.write_bytes(b"unknown")
    unknown.chmod(0o600)
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        storage.plan_delete(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
        )

    assert caught.value.reason == "record_conflict"
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize("bad_confirmation", (None, "0" * 64, "f" * 64))
def test_delete_record_rejects_bad_confirmation_without_changes(
    tmp_path,
    bad_confirmation,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    if bad_confirmation == plan["confirmation_sha256"]:
        bad_confirmation = "e" * 64
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        storage.delete_record(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
            confirmation_sha256=bad_confirmation,
            deleted_at="2026-08-15T13:00:00+00:00",
        )

    assert caught.value.reason == "confirmation_mismatch"
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


def test_delete_record_keeps_audit_until_explicit_post_retention_delete(tmp_path):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    other_sensitive = arguments["sensitive_root"] / ("a" * 64)
    other_data = arguments["data_root"] / ("a" * 64)
    other_sensitive.mkdir(mode=0o700)
    other_data.mkdir(mode=0o700)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )

    result = storage.delete_record(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        confirmation_sha256=plan["confirmation_sha256"],
        deleted_at="2026-08-15T13:00:00+00:00",
    )

    assert result == {
        "deleted": True,
        "external_send_approved": False,
        "record_id": stored["record_id"],
        "status": "deleted",
    }
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    assert list(sensitive_record.iterdir()) == []
    assert {path.name for path in data_record.iterdir()} == {"deleted.json"}
    audit = _stored_json(data_record / "deleted.json")
    assert set(audit) == {
        "deleted",
        "deleted_at",
        "deleted_sha256",
        "record_id",
        "retention_until",
        "schema_version",
    }
    assert audit["deleted"] is True
    assert "confirmation" not in _canonical_bytes(audit).decode("utf-8")
    assert other_sensitive.is_dir()
    assert other_data.is_dir()

    with pytest.raises(storage.StorageStop) as caught:
        storage.plan_delete(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
            current_at="2026-08-15T14:00:00+00:00",
        )
    assert caught.value.reason == "audit_retention_active"

    audit_plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        current_at="2026-08-16T00:00:01+00:00",
    )
    assert audit_plan["state"] == "deleted"
    assert [target["name"] for target in audit_plan["targets"]] == ["deleted.json"]
    removed = storage.delete_record(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        confirmation_sha256=audit_plan["confirmation_sha256"],
        deleted_at="2026-08-16T00:00:02+00:00",
        current_at="2026-08-16T00:00:02+00:00",
    )
    assert removed["status"] == "audit_removed"
    assert list(data_record.iterdir()) == []
    assert other_sensitive.is_dir()
    assert other_data.is_dir()


@pytest.mark.parametrize(
    "fault_point",
    ("first_deleting", "raw.bin", "derived.json", "commit.json"),
)
def test_delete_record_retries_same_confirmation_after_failure(
    tmp_path,
    monkeypatch,
    fault_point,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    original_replace = storage._replace_file
    original_unlink = getattr(storage, "_unlink_verified", None)
    injected = False

    def failing_replace(directory_fd, final_name, content):
        nonlocal injected
        result = original_replace(directory_fd, final_name, content)
        if not injected and fault_point == "first_deleting" and b'"state":"deleting"' in content:
            injected = True
            raise storage.StorageStop("injected_delete_failure")
        return result

    def failing_unlink(directory_fd, name):
        nonlocal injected
        result = original_unlink(directory_fd, name)
        if not injected and name == fault_point:
            injected = True
            raise storage.StorageStop("injected_delete_failure")
        return result

    monkeypatch.setattr(storage, "_replace_file", failing_replace)
    monkeypatch.setattr(storage, "_unlink_verified", failing_unlink, raising=False)
    with pytest.raises(storage.StorageStop) as caught:
        storage.delete_record(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
            confirmation_sha256=plan["confirmation_sha256"],
            deleted_at="2026-08-15T13:00:00+00:00",
        )
    assert caught.value.reason == "injected_delete_failure"
    assert injected is True

    monkeypatch.setattr(storage, "_replace_file", original_replace)
    monkeypatch.setattr(storage, "_unlink_verified", original_unlink, raising=False)
    result = storage.delete_record(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        confirmation_sha256=plan["confirmation_sha256"],
        deleted_at="2026-08-15T13:00:00+00:00",
    )

    assert result["status"] == "deleted"


def _invoke_existing_operation(storage, operation, arguments, stored, plan=None):
    if operation == "store":
        return storage.store_new(
            **arguments,
            stored_at="2026-08-15T00:00:00+00:00",
            retention_until="2026-08-16T00:00:00+00:00",
        )
    if operation == "load-derived":
        return storage.load_derived(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
            current_at="2026-08-15T12:00:00+00:00",
        )
    if operation == "plan-delete":
        return storage.plan_delete(
            sensitive_root=arguments["sensitive_root"],
            data_root=arguments["data_root"],
            record_id=stored["record_id"],
        )
    return storage.delete_record(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
        confirmation_sha256=plan["confirmation_sha256"],
        deleted_at="2026-08-15T13:00:00+00:00",
    )


@pytest.mark.parametrize(
    "operation",
    ("store", "load-derived", "plan-delete", "delete"),
)
def test_existing_operations_reject_changed_file_mode_without_mutation(
    tmp_path,
    operation,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    target = sensitive_record / "raw.bin"
    target.chmod(0o640)
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        _invoke_existing_operation(storage, operation, arguments, stored, plan)

    assert caught.value.reason == "insecure_mode"
    assert target.stat().st_mode & 0o777 == 0o640
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize(
    "operation",
    ("store", "load-derived", "plan-delete", "delete"),
)
def test_existing_operations_reject_changed_directory_mode_without_mutation(
    tmp_path,
    operation,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    sensitive_record.chmod(0o750)
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        _invoke_existing_operation(storage, operation, arguments, stored, plan)

    assert caught.value.reason == "insecure_mode"
    assert sensitive_record.stat().st_mode & 0o777 == 0o750
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize(
    "operation",
    ("store", "load-derived", "plan-delete", "delete"),
)
def test_existing_operations_reject_added_file_acl_without_mutation(
    tmp_path,
    monkeypatch,
    operation,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    target_inode = (sensitive_record / "raw.bin").stat().st_ino
    original_acl_check = storage._has_extended_acl

    def injected_acl(file_descriptor):
        if os.fstat(file_descriptor).st_ino == target_inode:
            return True
        return original_acl_check(file_descriptor)

    monkeypatch.setattr(storage, "_has_extended_acl", injected_acl)
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        _invoke_existing_operation(storage, operation, arguments, stored, plan)

    assert caught.value.reason == "insecure_acl"
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize(
    "operation",
    ("store", "load-derived", "plan-delete", "delete"),
)
def test_existing_operations_reject_replaced_file_symlink_without_mutation(
    tmp_path,
    operation,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    target = sensitive_record / "raw.bin"
    target.unlink()
    target.symlink_to(arguments["raw_log"])
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        _invoke_existing_operation(storage, operation, arguments, stored, plan)

    assert caught.value.reason == "record_conflict"
    assert target.is_symlink()
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before


@pytest.mark.parametrize(
    "operation",
    ("store", "load-derived", "plan-delete", "delete"),
)
@pytest.mark.parametrize("reason", ("insecure_owner", "invalid_file_type"))
def test_existing_operations_reject_changed_owner_or_type_without_mutation(
    tmp_path,
    monkeypatch,
    operation,
    reason,
):
    storage = _storage()
    arguments, stored = _store_fixture(storage, tmp_path)
    plan = storage.plan_delete(
        sensitive_root=arguments["sensitive_root"],
        data_root=arguments["data_root"],
        record_id=stored["record_id"],
    )
    sensitive_record = arguments["sensitive_root"] / stored["record_id"]
    data_record = arguments["data_root"] / stored["record_id"]
    target_inode = (sensitive_record / "raw.bin").stat().st_ino
    original_validator = storage._validate_created_fd

    def injected_attribute(file_descriptor, expected_kind, expected_mode):
        if os.fstat(file_descriptor).st_ino == target_inode:
            raise storage.StorageStop(reason)
        return original_validator(file_descriptor, expected_kind, expected_mode)

    monkeypatch.setattr(storage, "_validate_created_fd", injected_attribute)
    before = (_record_snapshot(sensitive_record), _record_snapshot(data_record))

    with pytest.raises(storage.StorageStop) as caught:
        _invoke_existing_operation(storage, operation, arguments, stored, plan)

    assert caught.value.reason == reason
    assert (_record_snapshot(sensitive_record), _record_snapshot(data_record)) == before
