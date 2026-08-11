"""Pilot collaboration CLI の出力・引数境界テスト。"""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run(*arguments):
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not existing
        else os.pathsep.join((str(PROJECT_ROOT), existing))
    )
    return subprocess.run(
        (
            sys.executable,
            "-m",
            "tools.development.pilot_collaboration_cli",
            *arguments,
        ),
        cwd=PROJECT_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _assert_contract(completed, command, stop_code):
    assert completed.returncode == 2
    assert completed.stderr == ""
    assert completed.stdout.endswith("\n")
    assert completed.stdout.count("\n") == 1
    value = json.loads(completed.stdout)
    assert set(value) == {
        "schema_version",
        "command",
        "result",
        "state",
        "run_id",
        "event_id",
        "stop_code",
        "detail",
    }
    assert value["schema_version"] == 1
    assert value["command"] == command
    assert value["result"] == "stopped"
    assert value["state"] is None
    assert value["event_id"] is None
    assert value["stop_code"] == stop_code
    assert value["detail"] is None or isinstance(value["detail"], str)
    return value


@pytest.mark.parametrize(
    ("arguments", "command", "stop_code"),
    (
        (("prepare",), "prepare", "config_invalid"),
        (("prepare", "--unknown"), "prepare", "config_invalid"),
        (("status", "--run-id", "../unsafe"), "status", "config_invalid"),
    ),
)
def test_cli_normalizes_invalid_arguments_to_contract_json(
    arguments,
    command,
    stop_code,
):
    completed = _run(*arguments)
    value = _assert_contract(completed, command, stop_code)
    assert value["run_id"] is None


@pytest.mark.parametrize("command", ("prepare", "ingest", "status"))
def test_cli_rejects_relative_path_arguments(command, tmp_path):
    relative = "relative/path.json"
    if command == "prepare":
        arguments = (
            "prepare",
            "--config",
            relative,
            "--private-root",
            str(tmp_path),
        )
        stop_code = "config_invalid"
    elif command == "ingest":
        arguments = (
            "ingest",
            "--private-root",
            str(tmp_path),
            "--run-id",
            "run-001",
            "--stage",
            "prompt_audit",
            "--attempt-id",
            "attempt-001",
            "--raw-file",
            relative,
            "--launch-record",
            str(tmp_path / "launch.json"),
        )
        stop_code = "config_invalid"
    else:
        arguments = (
            "status",
            "--private-root",
            relative,
            "--run-id",
            "run-001",
        )
        stop_code = "config_invalid"

    completed = _run(*arguments)

    _assert_contract(completed, command, stop_code)


def test_ingest_rejects_stage_outside_prompt_quality_slice(tmp_path):
    completed = _run(
        "ingest",
        "--private-root",
        str(tmp_path),
        "--run-id",
        "run-001",
        "--stage",
        "implementation",
        "--attempt-id",
        "attempt-001",
        "--raw-file",
        str(tmp_path / "raw.json"),
        "--launch-record",
        str(tmp_path / "launch.json"),
    )

    value = _assert_contract(completed, "ingest", "stage_invalid")
    assert value["run_id"] == "run-001"
