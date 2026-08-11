from concurrent.futures import ThreadPoolExecutor
import importlib
import inspect
import json
import os
from pathlib import Path

import pytest

from tests.fixtures.claude_bootstrap.helpers import CONTRACT
from tests.fixtures.claude_bootstrap.helpers import STORE_IDENTITY
from tests.fixtures.claude_bootstrap.helpers import all_managed_paths
from tests.fixtures.claude_bootstrap.helpers import assert_stop
from tests.fixtures.claude_bootstrap.helpers import create_scenario
from tests.fixtures.claude_bootstrap.helpers import install_fake_process
from tests.fixtures.claude_bootstrap.helpers import rebind_completion_review
from tests.fixtures.claude_bootstrap.helpers import rebind_decision
from tests.fixtures.claude_bootstrap.helpers import write_json


def test_token_claim_is_once_only_for_sequential_and_parallel_calls(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: scenario.run(), range(2)))

    assert sorted(result["result"] for result in results) == ["stopped", "succeeded"]
    assert len(scenario.fake_process.payload_calls) == 2
    assert not scenario.token_path.exists()
    assert (
        scenario.store_root / "consumed" / f"{scenario.approval_id}.json"
    ).is_file()
    third = scenario.run()
    assert third["result"] == "stopped"
    assert len(scenario.fake_process.payload_calls) == 2


def test_public_api_rejects_prompt_file_model_provider_binary_argv_and_root_inputs():
    module = importlib.import_module("tools.development.claude_bootstrap")
    function = module.run_approved_no_tool_bootstrap

    assert tuple(inspect.signature(function).parameters) == (
        "manifest_digest",
        "approval_id",
    )
    with pytest.raises(TypeError):
        function(
            "0" * 64,
            "approval",
            prompt="not allowed",
            model="other",
            runtime_root="/tmp/not-allowed",
        )


def test_shell_tools_agents_fallback_retry_and_generic_runner_are_unreachable(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    module = install_fake_process(monkeypatch, scenario)

    scenario.run()

    source = inspect.getsource(module)
    assert "structured_argv_executor" not in source
    assert "shell=True" not in source
    assert "fallback" not in source.lower()
    assert "retry" not in source.lower()
    for call in scenario.fake_process.payload_calls:
        argv = call["args"]
        assert call["shell"] is False
        assert "--agent" not in argv
        assert "--agents" not in argv
        assert "--plugin-dir" not in argv
        assert "--fallback-model" not in argv
        assert argv[argv.index("--tools") + 1] == ""


def test_missing_or_replaced_store_never_reinitializes_or_restores_pending(
    tmp_path, monkeypatch
):
    for missing in ("store", "identity", "token"):
        with monkeypatch.context() as local:
            scenario = create_scenario(tmp_path / missing, local)
            if missing == "store":
                scenario.store_root.rename(
                    scenario.store_root.with_name("removed-store")
                )
            elif missing == "identity":
                write_json(
                    scenario.store_root / "store.json",
                    {
                        "schema_version": 1,
                        "store_identity": "replacement-store",
                    },
                    mode=0o600,
                )
            else:
                scenario.token_path.unlink()
            install_fake_process(local, scenario)

            result = scenario.run()

            assert result["result"] == "stopped"
            assert scenario.fake_process.payload_calls == []
            if missing != "identity":
                assert not scenario.token_path.exists()


def test_git_never_contains_raw_credentials_or_user_specific_absolute_paths(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    secret_values = ["secret-api-value", "secret-oauth-value"]
    monkeypatch.setenv("ANTHROPIC_API_KEY", secret_values[0])
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", secret_values[1])
    install_fake_process(monkeypatch, scenario)

    scenario.run()

    for relative in all_managed_paths(scenario.repository):
        data = (scenario.repository / relative).read_text(encoding="utf-8")
        assert "raw-1.json" not in relative
        assert str(scenario.home) not in data
        assert all(secret not in data for secret in secret_values)


def test_fake_process_proves_atomic_claim_and_external_private_storage(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    consumed = scenario.store_root / "consumed" / f"{scenario.approval_id}.json"
    assert consumed.is_file()
    assert scenario.repository not in Path(result["receipt_path"]).parents
    assert (Path(result["receipt_path"]).stat().st_mode & 0o077) == 0


def test_dirty_manifest_symlink_unknown_store_file_and_wide_permissions_stop(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.manifest_path.write_bytes(scenario.manifest_path.read_bytes() + b" ")
    (scenario.store_root / "unknown.txt").write_text("unknown", encoding="utf-8")
    scenario.store_root.chmod(0o755)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert scenario.fake_process.payload_calls == []


def test_host_process_refusal_stops_without_alternate_route(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    module = scenario.module()
    calls = []

    def refused(args, **kwargs):
        calls.append(list(args))
        raise PermissionError("host policy refused process")

    monkeypatch.setattr(module.subprocess, "run", refused)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "host_safety_rejected"
    assert len(calls) == 1


def test_completion_review_identity_digest_status_and_target_are_required(
    tmp_path, monkeypatch
):
    faults = ("missing", "identity", "digest", "status", "target")
    for fault in faults:
        with monkeypatch.context() as local:
            scenario = create_scenario(tmp_path / fault, local)
            if fault == "missing":
                scenario.completion_review_path.unlink()
            elif fault == "identity":
                rebind_completion_review(
                    scenario,
                    lambda value: value.update({"review_id": "other-review"}),
                )
            elif fault == "digest":
                rebind_decision(
                    scenario,
                    lambda value: value.update(
                        {"completion_review_sha256": "0" * 64}
                    ),
                )
            elif fault == "status":
                rebind_completion_review(
                    scenario,
                    lambda value: value.update({"status": "blocked"}),
                )
            else:
                rebind_completion_review(
                    scenario,
                    lambda value: value.update({"target_commit": "0" * 40}),
                )
            install_fake_process(local, scenario)

            result = scenario.run()

            assert result.get("stop_code") == "completion_review_invalid", (
                "completion review identity, digest, status, and target must "
                "be verified before process creation"
            )
            assert scenario.fake_process.calls == []


def test_child_environment_allows_only_fixed_non_secret_names(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    secrets = {
        "AWS_SECRET_ACCESS_KEY": "aws-secret-value",
        "GITHUB_TOKEN": "github-secret-value",
        "DATABASE_URL": "postgres://secret.invalid/database",
        "UNLISTED_CREDENTIAL": "unlisted-secret-value",
    }
    for name, value in secrets.items():
        monkeypatch.setenv(name, value)

    environment = scenario.module()._child_environment()

    assert not set(secrets) & set(environment), (
        "unknown credential environment variables must not reach child processes"
    )
    assert environment["HOME"] == str(scenario.home)
