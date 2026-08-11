"""venv開発環境baselineのAcceptance Test。"""

import hashlib
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/development-environment.json"


def _module():
    return importlib.import_module(
        "tools.development.bootstrap_environment"
    )


def _write_project_scripts(project):
    (project / "pyproject.toml").write_text(
        """[project]
name = "reviewcompass3"

[project.scripts]
reviewcompass3-session-logs = "tools.session_logs.entry:main"
reviewcompass3-bootstrap-review = "tools.bootstrap.review_cli:main"
reviewcompass3-pilot = "tools.development.pilot_collaboration_cli:main"
reviewcompass3-review-plan = "tools.development.review_plan_cli:main"
""",
        encoding="utf-8",
    )


DECLARED_SCRIPTS = {
    "reviewcompass3-session-logs": "tools.session_logs.entry:main",
    "reviewcompass3-bootstrap-review": "tools.bootstrap.review_cli:main",
    "reviewcompass3-pilot": "tools.development.pilot_collaboration_cli:main",
    "reviewcompass3-review-plan": "tools.development.review_plan_cli:main",
}


def test_repository_declares_one_ignored_venv_and_exact_lock():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ignore.splitlines().count(".venv/") == 1

    config = _module().load_config(CONFIG)
    lock = ROOT / config["lock"]["path"]
    content = lock.read_bytes()
    assert hashlib.sha256(content).hexdigest() == config["lock"]["sha256"]
    lines = [line for line in content.decode().splitlines() if line]
    assert all("==" in line for line in lines)
    assert any(line.startswith("pytest==8.4.2") for line in lines)
    assert any(line.startswith("platformdirs==") for line in lines)
    assert any(line.startswith("PyYAML==") for line in lines)
    assert any(line.startswith("pip==") for line in lines)
    assert any(line.startswith("setuptools==") for line in lines)
    assert any(line.startswith("wheel==") for line in lines)
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"PyYAML>=6,<7"' in pyproject


def test_repository_runner_uses_only_venv_python():
    config = _module().load_config(CONFIG)
    runner = __import__("json").loads(
        (ROOT / "config/development-test-runner.json").read_text()
    )

    assert config["venv_python"] == ".venv/bin/python3"
    assert runner["python"]["command"] == config["venv_python"]
    assert runner["suites"]["full"][0] == config["venv_python"]


def test_bootstrap_stops_when_base_python_is_missing():
    config = _module().load_config(CONFIG)

    with pytest.raises(
        _module().DevelopmentEnvironmentError,
        match="base_python_missing",
    ):
        _module().bootstrap_environment(
            config=config,
            project_root=ROOT,
            locate=lambda command: None,
            run=lambda *args, **kwargs: None,
        )


def test_bootstrap_stops_for_unsupported_python_before_creating_venv():
    config = _module().load_config(CONFIG)
    calls = []

    def fake_run(command, **kwargs):
        calls.append(tuple(command))
        return SimpleNamespace(
            returncode=0,
            stdout="Python 3.10.1\n",
            stderr="",
        )

    with pytest.raises(
        _module().DevelopmentEnvironmentError,
        match="base_python_version_out_of_range",
    ):
        _module().bootstrap_environment(
            config=config,
            project_root=ROOT,
            locate=lambda command: "/usr/bin/python3",
            run=fake_run,
        )

    assert calls == [("python3", "--version")]


def test_bootstrap_uses_venv_and_locked_editable_install(tmp_path):
    config = _module().load_config(CONFIG)
    lock_source = ROOT / config["lock"]["path"]
    lock = tmp_path / config["lock"]["path"]
    lock.parent.mkdir(parents=True)
    lock.write_bytes(lock_source.read_bytes())
    calls = []

    def fake_run(command, **kwargs):
        calls.append(tuple(command))
        if command == ["python3", "--version"]:
            return SimpleNamespace(
                returncode=0,
                stdout="Python 3.9.6\n",
                stderr="",
            )
        if command[1:3] == ["-m", "venv"]:
            target = tmp_path / ".venv/bin/python3"
            target.parent.mkdir(parents=True)
            target.write_text("executable\n")
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    result = _module().bootstrap_environment(
        config=config,
        project_root=tmp_path,
        locate=lambda command: "/usr/bin/python3",
        run=fake_run,
        verify=False,
    )

    assert result.status == "created"
    assert calls == [
        ("python3", "--version"),
        ("python3", "-m", "venv", ".venv"),
        tuple(config["toolchain_command"]),
        (
            ".venv/bin/python3",
            "-m",
            "pip",
            "install",
            "--constraint",
            "constraints/development-py39.txt",
            "--no-build-isolation",
            "--editable",
            ".[development]",
        ),
    ]


def test_bootstrap_rejects_changed_lock_before_running_commands(tmp_path):
    config = _module().load_config(CONFIG)
    lock = tmp_path / config["lock"]["path"]
    lock.parent.mkdir(parents=True)
    lock.write_text("pytest==8.4.1\n")
    calls = []

    with pytest.raises(
        _module().DevelopmentEnvironmentError,
        match="dependency_lock_digest_mismatch",
    ):
        _module().bootstrap_environment(
            config=config,
            project_root=tmp_path,
            locate=lambda command: "/usr/bin/python3",
            run=lambda *args, **kwargs: calls.append(args),
        )

    assert calls == []


def test_verify_rejects_wrong_pytest_version(tmp_path):
    config = _module().load_config(CONFIG)
    python = tmp_path / config["venv_python"]
    python.parent.mkdir(parents=True)
    python.write_text("executable\n")

    def fake_run(command, **kwargs):
        if command[-1] == "--version" and "pytest" not in command:
            return SimpleNamespace(
                returncode=0,
                stdout="Python 3.9.6\n",
                stderr="",
            )
        return SimpleNamespace(
            returncode=0,
            stdout="pytest 8.3.5\n",
            stderr="",
        )

    with pytest.raises(
        _module().DevelopmentEnvironmentError,
        match="pytest_version_mismatch",
    ):
        _module().verify_environment(
            config=config,
            project_root=tmp_path,
            run=fake_run,
        )


def test_verify_accepts_standard_venv_python_symlink(tmp_path):
    config = _module().load_config(CONFIG)
    project = tmp_path / "project"
    target = tmp_path / "base-python"
    target.write_text("base\n")
    python = project / config["venv_python"]
    python.parent.mkdir(parents=True)
    python.symlink_to(target)
    _write_project_scripts(project)

    def fake_run(command, **kwargs):
        if command[-1] == "--version" and "pytest" not in command:
            output = "Python 3.9.6\n"
        elif command[-1] == "--version":
            output = "pytest 8.4.2\n"
        elif "'platformdirs'" in command[-1]:
            output = "4.4.0\n"
        elif "entry_points" in command[-1]:
            output = json.dumps(sorted(DECLARED_SCRIPTS.items()))
        else:
            output = "6.0.3\n"
        return SimpleNamespace(returncode=0, stdout=output, stderr="")

    result = _module().verify_environment(
        config=config,
        project_root=project,
        run=fake_run,
    )

    assert result.status == "verified"


def test_verify_rejects_missing_declared_project_script(tmp_path):
    config = _module().load_config(CONFIG)
    project = tmp_path / "project"
    python = project / config["venv_python"]
    python.parent.mkdir(parents=True)
    python.write_text("executable\n")
    _write_project_scripts(project)
    installed = dict(DECLARED_SCRIPTS)
    installed.pop("reviewcompass3-pilot")

    def fake_run(command, **kwargs):
        if command[-1] == "--version" and "pytest" not in command:
            output = "Python 3.9.6\n"
        elif command[-1] == "--version":
            output = "pytest 8.4.2\n"
        elif "'platformdirs'" in command[-1]:
            output = "4.4.0\n"
        elif "entry_points" in command[-1]:
            output = json.dumps(sorted(installed.items()))
        else:
            output = "6.0.3\n"
        return SimpleNamespace(returncode=0, stdout=output, stderr="")

    with pytest.raises(
        _module().DevelopmentEnvironmentError,
        match="project_scripts_mismatch",
    ):
        _module().verify_environment(
            config=config,
            project_root=project,
            run=fake_run,
        )
