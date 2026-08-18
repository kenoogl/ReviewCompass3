"""Session記録安全保存の四操作製品入口契約試験。"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


def _entry():
    return importlib.import_module("tools.session_logs.safe_storage_entry")


def _safe_result(raw_bytes):
    return {
        "external_send_approved": False,
        "parse_issues": [],
        "provenance": {
            "end_line": 1,
            "redaction_rules_sha256": "1" * 64,
            "source_path": "private-session.jsonl",
            "source_sha256": hashlib.sha256(raw_bytes).hexdigest(),
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
    repository_root = tmp_path / "private-repository"
    raw_root = tmp_path / "private-raw"
    sensitive_root = tmp_path / "private-sensitive"
    data_root = tmp_path / "private-data"
    for directory in (
        repository_root,
        raw_root,
        sensitive_root,
        data_root,
    ):
        directory.mkdir(mode=0o700)
    (repository_root / ".git").mkdir(mode=0o700)
    raw_log = raw_root / "private-session.jsonl"
    raw_bytes = b"raw-private-value\n"
    raw_log.write_bytes(raw_bytes)
    raw_log.chmod(0o600)
    return {
        "data_root": data_root.resolve(),
        "raw_bytes": raw_bytes,
        "raw_log": raw_log.resolve(),
        "raw_root": raw_root.resolve(),
        "repository_root": repository_root.resolve(),
        "sensitive_root": sensitive_root.resolve(),
    }


def _run(entry, capsys, arguments):
    exit_code = entry.run(arguments)
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert len(lines) == 1
    assert captured.err == ""
    return exit_code, json.loads(lines[0]), lines[0]


def test_four_operations_use_one_json_entry_without_private_output(
    tmp_path,
    monkeypatch,
    capsys,
):
    entry = _entry()
    roots = _roots(tmp_path)
    monkeypatch.setattr(
        entry,
        "prepare_safe_result",
        lambda raw_root, raw_log: (0, _safe_result(roots["raw_bytes"])),
    )
    common = [
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
    ]
    outputs = []

    exit_code, stored, serialized = _run(entry, capsys, [
        "store",
        "--repository-root",
        str(roots["repository_root"]),
        "--raw-root",
        str(roots["raw_root"]),
        "--raw-log",
        str(roots["raw_log"]),
        *common,
        "--stored-at",
        "2026-08-15T00:00:00+00:00",
        "--retention-until",
        "2026-08-16T00:00:00+00:00",
    ])
    assert exit_code == 0
    assert stored["status"] == "stored"
    outputs.append(serialized)

    exit_code, loaded, serialized = _run(entry, capsys, [
        "load-derived",
        *common,
        "--record-id",
        stored["record_id"],
        "--current-at",
        "2026-08-15T12:00:00+00:00",
    ])
    assert exit_code == 0
    assert loaded["status"] == "loaded"
    outputs.append(serialized)

    exit_code, plan, serialized = _run(entry, capsys, [
        "plan-delete",
        *common,
        "--record-id",
        stored["record_id"],
    ])
    assert exit_code == 0
    assert plan["status"] == "delete_planned"
    outputs.append(serialized)

    exit_code, deleted, serialized = _run(entry, capsys, [
        "delete",
        *common,
        "--record-id",
        stored["record_id"],
        "--confirmation-sha256",
        plan["confirmation_sha256"],
        "--deleted-at",
        "2026-08-15T13:00:00+00:00",
    ])
    assert exit_code == 0
    assert deleted["status"] == "deleted"
    outputs.append(serialized)

    visible = "\n".join(outputs)
    for private in (
        "raw-private-value",
        "private-session.jsonl",
        str(roots["repository_root"]),
        str(roots["raw_root"]),
        str(roots["sensitive_root"]),
        str(roots["data_root"]),
        str(Path.home()),
    ):
        assert private not in visible


@pytest.mark.parametrize(
    ("source_exit_code", "source_status"),
    ((4, "partial"), (5, "stopped")),
)
def test_store_rejects_non_ok_source_without_forwarding_source_result(
    tmp_path,
    monkeypatch,
    capsys,
    source_exit_code,
    source_status,
):
    entry = _entry()
    roots = _roots(tmp_path)
    monkeypatch.setattr(
        entry,
        "prepare_safe_result",
        lambda raw_root, raw_log: (
            source_exit_code,
            {
                "private": "raw-private-value",
                "status": source_status,
            },
        ),
    )

    exit_code, result, serialized = _run(entry, capsys, [
        "store",
        "--repository-root",
        str(roots["repository_root"]),
        "--raw-root",
        str(roots["raw_root"]),
        "--raw-log",
        str(roots["raw_log"]),
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
        "--stored-at",
        "2026-08-15T00:00:00+00:00",
        "--retention-until",
        "2026-08-16T00:00:00+00:00",
    ])

    assert exit_code == 4
    assert result == {
        "error": "unsafe_source_result",
        "external_send_approved": False,
        "status": "stopped",
    }
    assert "raw-private-value" not in serialized
    assert list(roots["sensitive_root"].iterdir()) == []
    assert list(roots["data_root"].iterdir()) == []


def test_storage_stop_is_one_fixed_json_without_exception_or_path(tmp_path, capsys):
    entry = _entry()
    roots = _roots(tmp_path)

    exit_code, result, serialized = _run(entry, capsys, [
        "load-derived",
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
        "--record-id",
        "0" * 64,
        "--current-at",
        "2026-08-15T12:00:00+00:00",
    ])

    assert exit_code == 4
    assert result == {
        "error": "record_not_found",
        "external_send_approved": False,
        "status": "stopped",
    }
    assert str(roots["sensitive_root"]) not in serialized
    assert str(roots["data_root"]) not in serialized
    assert "StorageStop" not in serialized


def test_store_reports_resumable_incomplete_result(tmp_path, monkeypatch, capsys):
    entry = _entry()
    storage = importlib.import_module("tools.session_logs.safe_storage")
    roots = _roots(tmp_path)
    monkeypatch.setattr(
        entry,
        "prepare_safe_result",
        lambda raw_root, raw_log: (0, _safe_result(roots["raw_bytes"])),
    )
    original_publish = storage._publish_file

    def stop_after_raw(directory_fd, final_name, content):
        result = original_publish(directory_fd, final_name, content)
        if final_name == "raw.bin":
            raise storage.StorageStop("private exception detail")
        return result

    monkeypatch.setattr(storage, "_publish_file", stop_after_raw)
    exit_code, result, serialized = _run(entry, capsys, [
        "store",
        "--repository-root",
        str(roots["repository_root"]),
        "--raw-root",
        str(roots["raw_root"]),
        "--raw-log",
        str(roots["raw_log"]),
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
        "--stored-at",
        "2026-08-15T00:00:00+00:00",
        "--retention-until",
        "2026-08-16T00:00:00+00:00",
    ])

    assert exit_code == 3
    assert result["status"] == "incomplete"
    assert result["external_send_approved"] is False
    assert set(result) == {
        "error",
        "external_send_approved",
        "operation_sha256",
        "record_id",
        "status",
    }
    assert "private exception detail" not in serialized
    assert "raw-private-value" not in serialized


def test_store_retry_keeps_incomplete_output_and_can_retry_again(
    tmp_path,
    monkeypatch,
    capsys,
):
    entry = _entry()
    storage = importlib.import_module("tools.session_logs.safe_storage")
    roots = _roots(tmp_path)
    monkeypatch.setattr(
        entry,
        "prepare_safe_result",
        lambda raw_root, raw_log: (0, _safe_result(roots["raw_bytes"])),
    )
    arguments = [
        "store",
        "--repository-root",
        str(roots["repository_root"]),
        "--raw-root",
        str(roots["raw_root"]),
        "--raw-log",
        str(roots["raw_log"]),
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
        "--stored-at",
        "2026-08-15T00:00:00+00:00",
        "--retention-until",
        "2026-08-16T00:00:00+00:00",
    ]
    original_publish = storage._publish_file

    def stop_after_raw(directory_fd, final_name, content):
        result = original_publish(directory_fd, final_name, content)
        if final_name == "raw.bin":
            raise storage.StorageStop("private first detail")
        return result

    monkeypatch.setattr(storage, "_publish_file", stop_after_raw)
    first_code, first, first_serialized = _run(entry, capsys, arguments)
    assert first_code == 3
    assert first["status"] == "incomplete"
    assert "private first detail" not in first_serialized

    def stop_after_derived(directory_fd, final_name, content):
        result = original_publish(directory_fd, final_name, content)
        if final_name == "derived.json":
            raise storage.StorageStop("private retry detail")
        return result

    monkeypatch.setattr(storage, "_publish_file", stop_after_derived)
    second_code, second, second_serialized = _run(entry, capsys, arguments)
    assert second_code == 3
    assert second["status"] == "incomplete"
    assert second["record_id"] == first["record_id"]
    assert "private retry detail" not in second_serialized
    assert "raw-private-value" not in second_serialized

    monkeypatch.setattr(storage, "_publish_file", original_publish)
    third_code, third, ignored = _run(entry, capsys, arguments)
    assert third_code == 0
    assert third["status"] == "stored"
    assert third["record_id"] == first["record_id"]


def test_delete_reports_resumable_deletion_incomplete(
    tmp_path,
    monkeypatch,
    capsys,
):
    entry = _entry()
    storage = importlib.import_module("tools.session_logs.safe_storage")
    roots = _roots(tmp_path)
    monkeypatch.setattr(
        entry,
        "prepare_safe_result",
        lambda raw_root, raw_log: (0, _safe_result(roots["raw_bytes"])),
    )
    common = [
        "--sensitive-root",
        str(roots["sensitive_root"]),
        "--data-root",
        str(roots["data_root"]),
    ]
    ignored, stored, ignored = _run(entry, capsys, [
        "store",
        "--repository-root",
        str(roots["repository_root"]),
        "--raw-root",
        str(roots["raw_root"]),
        "--raw-log",
        str(roots["raw_log"]),
        *common,
        "--stored-at",
        "2026-08-15T00:00:00+00:00",
        "--retention-until",
        "2026-08-16T00:00:00+00:00",
    ])
    ignored, plan, ignored = _run(entry, capsys, [
        "plan-delete",
        *common,
        "--record-id",
        stored["record_id"],
    ])
    original_unlink = storage._unlink_verified

    def stop_after_raw(directory_fd, name):
        result = original_unlink(directory_fd, name)
        if name == "raw.bin":
            raise storage.StorageStop("private deletion detail")
        return result

    monkeypatch.setattr(storage, "_unlink_verified", stop_after_raw)
    exit_code, result, serialized = _run(entry, capsys, [
        "delete",
        *common,
        "--record-id",
        stored["record_id"],
        "--confirmation-sha256",
        plan["confirmation_sha256"],
        "--deleted-at",
        "2026-08-15T13:00:00+00:00",
    ])

    assert exit_code == 3
    assert result["status"] == "deletion_incomplete"
    assert result["external_send_approved"] is False
    assert set(result) == {
        "error",
        "external_send_approved",
        "operation_sha256",
        "record_id",
        "status",
    }
    assert plan["confirmation_sha256"] not in serialized
    assert "private deletion detail" not in serialized


def test_pyproject_registers_safe_storage_entry_and_source_has_no_expansion():
    entry = _entry()
    document = importlib.import_module("tomllib").loads(
        Path("pyproject.toml").read_text(encoding="utf-8")
    )

    assert document["project"]["scripts"][
        "reviewcompass3-session-artifact-storage"
    ] == "tools.session_logs.safe_storage_entry:main"
    source = Path(entry.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "subprocess",
        "os.environ",
        "os.getenv",
        "socket",
        "git ",
    ):
        assert forbidden not in source
