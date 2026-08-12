"""Claude実装委譲経路CLIの最小契約テスト。"""

import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMON_KEYS = {
    "schema_version",
    "command",
    "result",
    "state",
    "run_id",
    "outcome",
    "stop_code",
    "detail",
}


def _cli():
    return importlib.import_module(
        "tools.development.claude_implementation_route_cli"
    )


def _invoke(capsys, arguments):
    cli = _cli()
    exit_code = cli.run(arguments)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out.count("\n") == 1
    assert captured.out.endswith("\n")
    value = json.loads(captured.out)
    assert set(value) == COMMON_KEYS
    assert captured.out == (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )
    return exit_code, value


@pytest.mark.parametrize("command", ("prepare", "record-turn", "status"))
def test_cli_success_preserves_core_outcome(command, tmp_path, monkeypatch, capsys):
    cli = _cli()
    outcome = {
        "schema_version": 1,
        "run_id": "run-001",
        "state": "synthetic-state",
        "marker": ["kept", 1],
    }

    def fake(*arguments):
        assert arguments[0] == PROJECT_ROOT
        return outcome

    if command == "prepare":
        monkeypatch.setattr(cli, "prepare", fake)
        arguments = (
            "prepare",
            "--config",
            str(tmp_path / "config.json"),
            "--private-root",
            str(tmp_path / "private"),
        )
    elif command == "record-turn":
        monkeypatch.setattr(cli, "record_turn", fake)
        arguments = (
            "record-turn",
            "--private-root",
            str(tmp_path / "private"),
            "--run-id",
            "run-001",
            "--turn",
            "test",
            "--launch",
            str(tmp_path / "launch.json"),
            "--raw",
            str(tmp_path / "raw.json"),
        )
    else:
        monkeypatch.setattr(cli, "status", fake)
        arguments = (
            "status",
            "--private-root",
            str(tmp_path / "private"),
            "--run-id",
            "run-001",
        )

    exit_code, value = _invoke(capsys, arguments)

    assert exit_code == 0
    assert value == {
        "schema_version": 1,
        "command": command,
        "result": "completed",
        "state": "synthetic-state",
        "run_id": "run-001",
        "outcome": outcome,
        "stop_code": None,
        "detail": None,
    }


@pytest.mark.parametrize(
    ("arguments", "command", "run_id"),
    (
        (("unknown",), None, None),
        (("prepare", "--config", "/absolute/config.json"), "prepare", None),
        (
            (
                "status",
                "--private-root",
                "/absolute/private",
                "--run-id",
                "run-001",
                "--run-id",
                "run-002",
            ),
            "status",
            None,
        ),
        (
            (
                "prepare",
                "--config",
                "relative.json",
                "--private-root",
                "/absolute/private",
            ),
            "prepare",
            None,
        ),
        (
            (
                "status",
                "--private-root",
                "/absolute/private",
                "--run-id",
                "../unsafe",
            ),
            "status",
            None,
        ),
        (
            (
                "record-turn",
                "--private-root",
                "/absolute/private",
                "--run-id",
                "run-001",
                "--turn",
                "review",
                "--launch",
                "/absolute/launch.json",
                "--raw",
                "/absolute/raw.json",
            ),
            "record-turn",
            "run-001",
        ),
    ),
)
def test_cli_rejects_invalid_arguments(
    arguments,
    command,
    run_id,
    capsys,
):
    exit_code, value = _invoke(capsys, arguments)

    assert exit_code == 2
    assert value["command"] == command
    assert value["result"] == "stopped"
    assert value["state"] is None
    assert value["run_id"] == run_id
    assert value["outcome"] is None
    assert value["stop_code"] == "config_invalid"
    assert value["detail"] is None


def test_cli_normalizes_route_stop(tmp_path, monkeypatch, capsys):
    cli = _cli()

    def stop(*arguments):
        raise cli.RouteStop("synthetic_stop")

    monkeypatch.setattr(cli, "status", stop)
    exit_code, value = _invoke(
        capsys,
        (
            "status",
            "--private-root",
            str(tmp_path),
            "--run-id",
            "run-001",
        ),
    )

    assert exit_code == 2
    assert value["result"] == "stopped"
    assert value["run_id"] == "run-001"
    assert value["stop_code"] == "synthetic_stop"


def test_cli_normalizes_unexpected_exception(tmp_path, monkeypatch, capsys):
    cli = _cli()

    def fail(*arguments):
        raise RuntimeError("must not leak")

    monkeypatch.setattr(cli, "status", fail)
    exit_code, value = _invoke(
        capsys,
        (
            "status",
            "--private-root",
            str(tmp_path),
            "--run-id",
            "run-001",
        ),
    )

    assert exit_code == 1
    assert value["result"] == "failed"
    assert value["run_id"] == "run-001"
    assert value["stop_code"] == "internal_error"
    assert value["detail"] is None


def test_project_registers_claude_implementation_entrypoint():
    text = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert text.count("reviewcompass3-claude-implementation =") == 1
    assert (
        'reviewcompass3-claude-implementation = '
        '"tools.development.claude_implementation_route_cli:main"'
    ) in text
