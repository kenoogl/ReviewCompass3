import importlib
import inspect
import json

import pytest


def _cli_module():
    return importlib.import_module("tools.development.pilot_collaboration_cli")


def test_bootstrap_is_single_cli_entry_with_two_inputs_and_single_python_function():
    cli = _cli_module()
    bootstrap = importlib.import_module("tools.development.claude_bootstrap")

    assert cli.COMMAND_FLAGS["bootstrap"] == ("manifest-digest", "approval-id")
    signature = inspect.signature(bootstrap.run_approved_no_tool_bootstrap)
    assert tuple(signature.parameters) == ("manifest_digest", "approval_id")
    assert [
        name
        for name, value in vars(bootstrap).items()
        if inspect.isfunction(value) and not name.startswith("_")
    ] == ["run_approved_no_tool_bootstrap"]


def test_bootstrap_cli_returns_one_json_line_and_distinct_exit_codes(
    capsys,
):
    cli = _cli_module()
    cases = (
        [
            "bootstrap",
            "--manifest-digest",
            "0" * 64,
            "--approval-id",
            "missing-approval",
        ],
        [
            "bootstrap",
            "--manifest-digest",
            "0" * 64,
            "--approval-id",
            "missing-approval",
            "extra",
        ],
    )
    for arguments in cases:
        exit_code = cli.run(arguments)
        captured = capsys.readouterr()
        assert exit_code == 2
        assert captured.err == ""
        assert captured.out.endswith("\n")
        assert captured.out.count("\n") == 1
        response = json.loads(captured.out)
        assert response["result"] == "stopped"
        assert response["command"] == "bootstrap"
        assert set(response) >= {
            "schema_version",
            "result",
            "stop_code",
            "payload_process_count",
            "preflight_process_count",
            "approval_state",
            "recovery",
        }
        assert "Traceback" not in captured.out


def test_bootstrap_command_cannot_be_extended_to_general_conversation_or_delegation():
    cli = _cli_module()

    forbidden = (
        "--prompt",
        "--file",
        "--model",
        "--provider",
        "--binary",
        "--argv",
        "--agent",
        "--delegate",
        "--resume",
    )
    for option in forbidden:
        exit_code = cli.run(
            [
                "bootstrap",
                "--manifest-digest",
                "0" * 64,
                "--approval-id",
                "missing-approval",
                option,
                "value",
            ]
        )
        assert exit_code == 2
