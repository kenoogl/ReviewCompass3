"""利用者向けSession記録読取り専用入口の契約試験。"""

import importlib
import json
from pathlib import Path

import pytest


def _entry():
    return importlib.import_module("tools.session_logs.read_only_entry")


def _write_records(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )


def _run(entry, capsys, raw_root, raw_log):
    exit_code = entry.run((
        "--raw-root",
        str(raw_root),
        "--raw-log",
        str(raw_log),
    ))
    captured = capsys.readouterr()
    assert captured.err == ""
    lines = captured.out.splitlines()
    assert len(lines) == 1
    return exit_code, json.loads(lines[0]), lines[0]


@pytest.mark.parametrize(
    ("records", "source_kind", "expected_text"),
    (
        (
            ({
                "uuid": "user-1",
                "type": "user",
                "sessionId": "session-1",
                "message": {
                    "role": "user",
                    "content": "mail=user@example.com",
                },
            },),
            "claude",
            "mail=[REDACTED:email]",
        ),
        (
            (
                {"type": "thread.started", "thread_id": "thread-1"},
                {
                    "type": "item.completed",
                    "item": {
                        "id": "item-1",
                        "type": "agent_message",
                        "text": "Done.",
                    },
                },
            ),
            "codex_exec_json",
            "Done.",
        ),
        (
            (
                {
                    "timestamp": "2026-08-14T00:00:00Z",
                    "type": "session_meta",
                    "payload": {"id": "thread-1", "cwd": "workspace"},
                },
                {
                    "timestamp": "2026-08-14T00:00:01Z",
                    "type": "response_item",
                    "payload": {
                        "id": "message-1",
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {"type": "output_text", "text": "Rollout done."},
                        ],
                    },
                },
            ),
            "codex_rollout",
            "Rollout done.",
        ),
    ),
)
def test_returns_safe_read_only_result_for_three_formats(
    tmp_path,
    capsys,
    monkeypatch,
    records,
    source_kind,
    expected_text,
):
    entry = _entry()
    monkeypatch.setattr(entry.metadata, "version", lambda name: "0.0.1")
    raw_root = tmp_path / "raw"
    raw_log = raw_root / "session.jsonl"
    _write_records(raw_log, records)
    before = raw_log.read_bytes()

    exit_code, result, serialized = _run(
        entry,
        capsys,
        raw_root.resolve(),
        raw_log.resolve(),
    )

    assert exit_code == 0
    assert result["status"] == "ok"
    assert result["source_kind"] == source_kind
    assert expected_text in result["transcript"]
    assert result["external_send_approved"] is False
    assert result["provenance"]["source_path"] == "session.jsonl"
    assert "events" not in result
    assert "detail" not in serialized
    assert str(raw_root.resolve()) not in serialized
    assert raw_log.read_bytes() == before


def test_returns_only_safe_parse_issue_fields(tmp_path, capsys, monkeypatch):
    entry = _entry()
    monkeypatch.setattr(entry.metadata, "version", lambda name: "0.0.1")
    raw_root = tmp_path / "raw"
    raw_log = raw_root / "session.jsonl"
    unsafe_detail = "private_issue_detail"
    _write_records(raw_log, (
        {
            "uuid": "user-1",
            "type": "user",
            "sessionId": "session-1",
            "message": {"role": "user", "content": "safe"},
        },
        {
            "uuid": "event-2",
            "type": unsafe_detail,
            "sessionId": "session-1",
            "message": {"role": "user", "content": "ignored"},
        },
    ))

    exit_code, result, serialized = _run(
        entry,
        capsys,
        raw_root.resolve(),
        raw_log.resolve(),
    )

    assert exit_code == 3
    assert result["status"] == "partial"
    assert result["parse_issues"] == [{
        "block_index": -1,
        "kind": "unsupported_event",
        "line_no": 2,
    }]
    assert unsafe_detail not in serialized


@pytest.mark.parametrize("outside_kind", ("path", "symlink"))
def test_rejects_source_outside_root_before_reading(
    tmp_path,
    capsys,
    outside_kind,
):
    entry = _entry()
    raw_root = tmp_path / "raw"
    raw_root.mkdir()
    outside = tmp_path / "outside.jsonl"
    _write_records(outside, ({
        "uuid": "user-1",
        "type": "user",
        "sessionId": "session-1",
        "message": {"role": "user", "content": "outside"},
    },))
    raw_log = outside
    if outside_kind == "symlink":
        raw_log = raw_root / "linked.jsonl"
        raw_log.symlink_to(outside)

    exit_code, result, serialized = _run(
        entry,
        capsys,
        raw_root.resolve(),
        raw_log.absolute(),
    )

    assert exit_code == 4
    assert result == {
        "error": "source_outside_root",
        "external_send_approved": False,
        "status": "stopped",
    }
    assert str(outside) not in serialized


@pytest.mark.parametrize(
    ("content", "reason"),
    (
        ("value=A9fK2mQ7xR4vT8pL3nC6sW1yH5jD0bZ", "sensitive_data_remaining"),
        ("work=/Users/example/project", "absolute_path_remaining"),
    ),
)
def test_stops_without_returning_unsafe_content(
    tmp_path,
    capsys,
    monkeypatch,
    content,
    reason,
):
    entry = _entry()
    monkeypatch.setattr(entry.metadata, "version", lambda name: "0.0.1")
    raw_root = tmp_path / "raw"
    raw_log = raw_root / "session.jsonl"
    _write_records(raw_log, ({
        "uuid": "user-1",
        "type": "user",
        "sessionId": "session-1",
        "message": {"role": "user", "content": content},
    },))

    exit_code, result, serialized = _run(
        entry,
        capsys,
        raw_root.resolve(),
        raw_log.resolve(),
    )

    assert exit_code == 4
    assert result == {
        "error": reason,
        "external_send_approved": False,
        "status": "stopped",
    }
    assert content not in serialized


def test_rejects_unknown_format_without_input_details(tmp_path, capsys):
    entry = _entry()
    raw_root = tmp_path / "raw"
    raw_log = raw_root / "unknown.jsonl"
    private_value = "unknown_private_value"
    _write_records(raw_log, ({"unknown": private_value},))

    exit_code, result, serialized = _run(
        entry,
        capsys,
        raw_root.resolve(),
        raw_log.resolve(),
    )

    assert exit_code == 4
    assert result == {
        "error": "unsupported_source",
        "external_send_approved": False,
        "status": "stopped",
    }
    assert private_value not in serialized


def test_pyproject_registers_the_installed_entry():
    document = importlib.import_module("tomllib").loads(
        Path("pyproject.toml").read_text(encoding="utf-8")
    )

    assert document["project"]["scripts"]["reviewcompass3-session-artifact"] == (
        "tools.session_logs.read_only_entry:main"
    )
