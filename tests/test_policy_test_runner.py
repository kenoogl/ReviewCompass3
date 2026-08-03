"""版付きpolicyに従う公式Test runnerのAcceptance Test。"""

import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config/development-test-runner.json"


@pytest.fixture
def runner():
    return importlib.import_module(
        "tools.development.policy_test_runner"
    )


def test_repository_policy_has_one_machine_test_command(runner):
    config = runner.load_config(CONFIG_PATH)

    assert runner.command_for(config, "full") == (
        "python3",
        "-m",
        "pytest",
        "-q",
    )
    assert config["fallback"] == "forbidden"
    assert config["receipt_required"] is True
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text()
    assert "pytest>=8.4,<9" in pyproject


def test_preflight_stops_without_configured_python_and_never_falls_back(
    runner,
):
    config = runner.load_config(CONFIG_PATH)
    calls = []

    with pytest.raises(
        runner.TestEnvironmentUnavailable,
        match="configured_python_missing",
    ):
        runner.execute(
            config=config,
            project_root=PROJECT_ROOT,
            suite="full",
            receipt_path=None,
            locate=lambda command: None,
            run=lambda *args, **kwargs: calls.append(args),
        )

    assert calls == []


def test_runner_performs_preflight_test_and_writes_verification_receipt(
    runner,
    tmp_path,
):
    config = runner.load_config(CONFIG_PATH)
    calls = []

    def fake_run(command, **kwargs):
        calls.append(tuple(command))
        if command[-1] == "--version" and "pytest" not in command:
            return SimpleNamespace(returncode=0, stdout="Python 3.11.9\n", stderr="")
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
        return SimpleNamespace(
            returncode=0,
            stdout="448 passed in 2.03s\n",
            stderr="",
        )

    receipt_path = tmp_path / "verification-receipt.json"
    result = runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=receipt_path,
        locate=lambda command: "/usr/bin/python3",
        run=fake_run,
    )

    receipt = json.loads(receipt_path.read_text())
    assert calls == [
        ("python3", "--version"),
        ("python3", "-m", "pytest", "--version"),
        ("python3", "-m", "pytest", "-q"),
    ]
    assert result.status == "passed"
    assert receipt["status"] == "passed"
    assert receipt["command"] == "python3 -m pytest -q"
    assert receipt["python_version"] == "3.11.9"
    assert receipt["pytest_version"] == "8.4.2"
    assert receipt["fallback_used"] is False
    assert len(receipt["config_digest"]) == 64
    assert len(receipt["source_state_digest"]) == 64


def test_runner_records_failed_test_without_reclassifying_environment(
    runner,
    tmp_path,
):
    config = runner.load_config(CONFIG_PATH)

    def fake_run(command, **kwargs):
        if command == ["python3", "--version"]:
            return SimpleNamespace(returncode=0, stdout="Python 3.11.9\n", stderr="")
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
        return SimpleNamespace(returncode=1, stdout="1 failed\n", stderr="")

    result = runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=tmp_path / "failed.json",
        locate=lambda command: "/usr/bin/python3",
        run=fake_run,
    )

    assert result.status == "failed"
    assert result.exit_code == 1
