"""版付きpolicyに従う公式Test runnerのAcceptance Test。"""

import importlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config/development-test-runner.json"
SUMMARY_VARIABLE = "RC3_TEST_SUMMARY_PATH"
EXCLUDED_TEST_ENVIRONMENT_NAMES = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_FOUNDRY_API_KEY",
    "ANTHROPIC_VERTEX_PROJECT_ID",
    "AWS_BEARER_TOKEN_BEDROCK",
)


def _write_summary(environment, *, passed, failed=0):
    """runnerが読む構造化集計を、pluginの代わりに書き出す。"""

    summary = {
        "passed": passed, "failed": failed, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "errors": 0, "total": passed + failed,
    }
    Path(environment[SUMMARY_VARIABLE]).write_text(
        json.dumps(summary, sort_keys=True), encoding="utf-8"
    )


@pytest.fixture
def runner():
    return importlib.import_module(
        "tools.development.policy_test_runner"
    )


def test_repository_policy_has_one_machine_test_command(runner):
    config = runner.load_config(CONFIG_PATH)

    assert config["python"]["minimum_version"] == "3.13"
    assert config["python"]["maximum_exclusive_version"] == "3.14"
    assert runner.command_for(config, "full") == (
        ".venv/bin/python3",
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
            return SimpleNamespace(returncode=0, stdout="Python 3.13.1\n", stderr="")
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
        _write_summary(kwargs["env"], passed=448)
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
        (".venv/bin/python3", "--version"),
        (".venv/bin/python3", "-m", "pytest", "--version"),
        (".venv/bin/python3", "-m", "pytest", "-q"),
    ]
    assert result.status == "passed"
    assert receipt["status"] == "passed"
    assert receipt["command"] == ".venv/bin/python3 -m pytest -q"
    assert receipt["python_version"] == "3.13.1"
    assert receipt["pytest_version"] == "8.4.2"
    assert receipt["fallback_used"] is False
    assert len(receipt["config_digest"]) == 64
    assert len(receipt["source_state_digest"]) == 64


def test_full_suite_child_environment_excludes_fixed_auth_names(
    runner,
    tmp_path,
    monkeypatch,
):
    config = runner.load_config(CONFIG_PATH)
    child_environment = {}
    for name in EXCLUDED_TEST_ENVIRONMENT_NAMES:
        monkeypatch.setenv(name, "test-presence-marker")
    monkeypatch.setenv("RC3_TEST_BENIGN", "preserved")

    def fake_run(command, **kwargs):
        prepared = _preflight(command)
        if prepared is not None:
            return prepared
        child_environment.update(kwargs["env"])
        _write_summary(kwargs["env"], passed=1)
        return SimpleNamespace(returncode=0, stdout="1 passed\n", stderr="")

    runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=tmp_path / "isolated.json",
        locate=lambda command: "/usr/bin/python3",
        run=fake_run,
    )

    assert not set(EXCLUDED_TEST_ENVIRONMENT_NAMES) & set(child_environment)
    assert child_environment["RC3_TEST_BENIGN"] == "preserved"
    assert child_environment[SUMMARY_VARIABLE]
    assert tuple(config["test_environment_excluded_names"]) == (
        EXCLUDED_TEST_ENVIRONMENT_NAMES
    )
    for name in EXCLUDED_TEST_ENVIRONMENT_NAMES:
        assert os.environ[name] == "test-presence-marker"


def test_full_suite_uses_temporary_bytecode_cache_outside_project(
    runner,
    tmp_path,
    monkeypatch,
):
    config = runner.load_config(CONFIG_PATH)
    inherited_cache = tmp_path / "inherited-cache"
    inherited_cache.mkdir()
    monkeypatch.setenv("PYTHONPYCACHEPREFIX", str(inherited_cache))
    observed = {}

    def fake_run(command, **kwargs):
        prepared = _preflight(command)
        if prepared is not None:
            return prepared
        cache_path = Path(kwargs["env"]["PYTHONPYCACHEPREFIX"])
        observed["path"] = cache_path
        observed["exists_during_run"] = cache_path.is_dir()
        _write_summary(kwargs["env"], passed=1)
        return SimpleNamespace(returncode=0, stdout="1 passed\n", stderr="")

    runner.execute(
        config=config,
        project_root=PROJECT_ROOT,
        suite="full",
        receipt_path=tmp_path / "isolated-cache.json",
        locate=lambda command: "/usr/bin/python3",
        run=fake_run,
    )

    cache_path = observed["path"]
    assert cache_path != inherited_cache
    assert cache_path.is_absolute()
    assert cache_path != PROJECT_ROOT and PROJECT_ROOT not in cache_path.parents
    assert observed["exists_during_run"] is True
    assert not cache_path.exists()
    assert os.environ["PYTHONPYCACHEPREFIX"] == str(inherited_cache)


def test_runner_records_failed_test_without_reclassifying_environment(
    runner,
    tmp_path,
):
    config = runner.load_config(CONFIG_PATH)

    def fake_run(command, **kwargs):
        if command == [".venv/bin/python3", "--version"]:
            return SimpleNamespace(returncode=0, stdout="Python 3.13.1\n", stderr="")
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
        _write_summary(kwargs["env"], passed=0, failed=1)
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


def test_source_digest_excludes_local_environment_and_install_metadata(
    runner,
    tmp_path,
):
    source = tmp_path / "source.py"
    venv_file = tmp_path / ".venv/lib/python3.13/site-packages/package.py"
    egg_info = tmp_path / "reviewcompass3.egg-info/PKG-INFO"
    source.write_text("value = 1\n")
    venv_file.parent.mkdir(parents=True)
    venv_file.write_text("first environment\n")
    egg_info.parent.mkdir(parents=True)
    egg_info.write_text("first metadata\n")

    before = runner._source_state_digest(tmp_path)
    venv_file.write_text("changed environment\n")
    egg_info.write_text("changed metadata\n")

    assert runner._source_state_digest(tmp_path) == before


def _preflight(command):
    """preflight 2回分の応答。testの本体実行以外を共通化する。"""

    if command[-1] == "--version" and "pytest" not in command:
        return SimpleNamespace(returncode=0, stdout="Python 3.13.1\n", stderr="")
    if command[-1] == "--version":
        return SimpleNamespace(returncode=0, stdout="pytest 8.4.2\n", stderr="")
    return None


class TestSummaryIsBoundToTheCurrentRun:
    """F-B1反証：実行前から在る集計や、実合格0件を公式合格にしない。"""

    def test_pre_existing_summary_is_rejected(self, runner, tmp_path):
        config = runner.load_config(CONFIG_PATH)
        receipt_path = tmp_path / "receipt.json"
        stale = receipt_path.with_name(receipt_path.name + ".summary.json")
        stale.write_text(
            json.dumps(
                {
                    "passed": 999, "failed": 0, "skipped": 0, "xfailed": 0,
                    "xpassed": 0, "errors": 0, "total": 999,
                },
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        def fake_run(command, **kwargs):
            prepared = _preflight(command)
            if prepared is not None:
                return prepared
            # 現在runは集計を書かない（古いfileがそのまま残る）。
            return SimpleNamespace(returncode=0, stdout="1 passed\n", stderr="")

        with pytest.raises(Exception) as caught:
            runner.execute(
                config=config,
                project_root=PROJECT_ROOT,
                suite="full",
                receipt_path=receipt_path,
                locate=lambda command: "/usr/bin/python3",
                run=fake_run,
            )
        assert not isinstance(caught.value, AssertionError)
        assert not receipt_path.exists()

    @pytest.mark.parametrize("field", ["skipped", "xfailed"])
    def test_zero_passed_suite_is_not_official_pass(self, runner, tmp_path, field):
        config = runner.load_config(CONFIG_PATH)

        def fake_run(command, **kwargs):
            prepared = _preflight(command)
            if prepared is not None:
                return prepared
            summary = {
                "passed": 0, "failed": 0, "skipped": 0, "xfailed": 0,
                "xpassed": 0, "errors": 0, "total": 2,
            }
            summary[field] = 2
            Path(kwargs["env"][SUMMARY_VARIABLE]).write_text(
                json.dumps(summary, sort_keys=True), encoding="utf-8"
            )
            return SimpleNamespace(returncode=0, stdout="2 %s\n" % field, stderr="")

        with pytest.raises(runner.TestRunnerPolicyError):
            runner.execute(
                config=config,
                project_root=PROJECT_ROOT,
                suite="full",
                receipt_path=tmp_path / "receipt.json",
                locate=lambda command: "/usr/bin/python3",
                run=fake_run,
            )


class TestReceiptPathIsOutsideTheSource:
    """F-B2反証：receiptで実行対象sourceを上書きできない。"""

    def test_receipt_path_inside_source_tree_is_rejected(self, runner, tmp_path):
        """実repositoryは触らない。使い捨てのproject rootで反証する。"""

        config = runner.load_config(CONFIG_PATH)
        fake_root = tmp_path / "project"
        (fake_root / "tools").mkdir(parents=True)
        target = fake_root / "tools" / "module.py"
        original = b"def value():\n    return 1\n"
        target.write_bytes(original)

        def fake_run(command, **kwargs):
            prepared = _preflight(command)
            if prepared is not None:
                return prepared
            _write_summary(kwargs["env"], passed=1)
            return SimpleNamespace(returncode=0, stdout="1 passed\n", stderr="")

        with pytest.raises(Exception) as caught:
            runner.execute(
                config=config,
                project_root=fake_root,
                suite="full",
                receipt_path=target,
                locate=lambda command: "/usr/bin/python3",
                run=fake_run,
            )
        assert not isinstance(caught.value, AssertionError)
        assert target.read_bytes() == original
