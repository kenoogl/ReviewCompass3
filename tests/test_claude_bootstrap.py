import copy
import hashlib
import inspect
import json
from pathlib import Path

import pytest

from tests.fixtures.claude_bootstrap.helpers import APPROVAL_ID
from tests.fixtures.claude_bootstrap.helpers import CONTRACT
from tests.fixtures.claude_bootstrap.helpers import ERROR_RESULTS
from tests.fixtures.claude_bootstrap.helpers import SUCCESS_RESULT
from tests.fixtures.claude_bootstrap.helpers import assert_stop
from tests.fixtures.claude_bootstrap.helpers import create_scenario
from tests.fixtures.claude_bootstrap.helpers import install_fake_process
from tests.fixtures.claude_bootstrap.helpers import rebind_manifest
from tests.fixtures.claude_bootstrap.helpers import sha256_bytes
from tests.fixtures.claude_bootstrap.helpers import write_json


def test_manifest_payload_bytes_digests_order_and_count_are_exact(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    calls = scenario.fake_process.payload_calls
    assert len(calls) == 2
    actual_payloads = [call["args"][-1] for call in calls]
    assert actual_payloads == [item["text"] for item in CONTRACT["payloads"]]
    assert [len(value.encode("utf-8")) for value in actual_payloads] == [296, 221]
    assert [sha256_bytes(value.encode("utf-8")) for value in actual_payloads] == [
        item["sha256"] for item in CONTRACT["payloads"]
    ]
    ordered = [
        {"ordinal": index, "sha256": sha256_bytes(value.encode("utf-8"))}
        for index, value in enumerate(actual_payloads, start=1)
    ]
    assert sha256_bytes(
        json.dumps(ordered, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ) == CONTRACT["ordered_payload_sha256"]


def test_human_approval_all_bindings_expiry_and_pending_state_are_required(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    decision = json.loads(scenario.decision_path.read_text(encoding="utf-8"))
    decision["material_policy"]["forbid_credentials"] = False
    write_json(scenario.decision_path, decision)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert_stop(result, "approval_mismatch", scenario)


def test_single_preflight_rejects_redaction_secret_email_and_phone_before_payload_process(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)

    def add_secret(manifest):
        manifest["payloads"][0]["text"] += " token=sk-test user@example.invalid +81-90-1234-5678"
        payload = manifest["payloads"][0]
        payload["utf8_bytes"] = len(payload["text"].encode("utf-8"))
        payload["sha256"] = sha256_bytes(payload["text"].encode("utf-8"))

    rebind_manifest(scenario, add_secret)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert_stop(result, "unsafe_payload", scenario)


def test_child_environment_and_public_result_exclude_credentials_roots_and_values(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    secrets = {
        "ANTHROPIC_API_KEY": "api-secret-value",
        "ANTHROPIC_AUTH_TOKEN": "auth-secret-value",
        "ANTHROPIC_BASE_URL": "https://secret.invalid",
        "CLAUDE_CODE_OAUTH_TOKEN": "oauth-secret-value",
        "REVIEWCOMPASS3_RUNTIME_ROOT": "/private/forbidden-runtime",
        "REVIEWCOMPASS3_CUSTOM_ROOT": "/private/forbidden-custom",
    }
    for name, value in secrets.items():
        monkeypatch.setenv(name, value)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    serialized = json.dumps(result, ensure_ascii=False)
    for call in scenario.fake_process.calls:
        for name, value in secrets.items():
            assert name not in (call["env"] or {})
            assert value not in serialized
    assert str(scenario.repository) not in serialized


def test_child_environment_preserves_user_for_claude_subscription_lookup(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    monkeypatch.setenv("USER", "subscription-user")

    environment = scenario.module()._child_environment()

    assert environment["USER"] == "subscription-user"


def test_missing_administrator_trusted_claude_capability_stops_before_claim(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.trusted_transport_ready = False
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "trusted_transport_unavailable"
    assert result["approval_state"] == "pending"
    assert result["payload_process_count"] == 0
    assert result["preflight_process_count"] == 1
    assert scenario.token_path.is_file()
    assert list((scenario.store_root / "claimed").iterdir()) == []
    assert list((scenario.store_root / "consumed").iterdir()) == []
    assert list(
        (
            scenario.runtime_root
            / "projects"
            / "reviewcompass3-bootstrap-test"
            / "development"
            / "sensitive"
            / "claude-bootstrap"
            / "runs"
            / scenario.approval_id
        ).iterdir()
    ) == []
    assert [call["args"] for call in scenario.fake_process.calls] == [
        [
            "/usr/local/libexec/reviewcompass/trusted-review-send",
            "--capabilities",
        ]
    ]


def test_missing_administrator_trusted_entry_file_stops_before_claim(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.trusted_transport_missing = True
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "trusted_transport_unavailable"
    assert result["approval_state"] == "pending"
    assert result["payload_process_count"] == 0
    assert result["preflight_process_count"] == 1
    assert scenario.token_path.is_file()
    assert list((scenario.store_root / "claimed").iterdir()) == []
    assert list((scenario.store_root / "consumed").iterdir()) == []


def test_fixed_argv_disables_tools_and_uses_only_external_empty_work_directory(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    scenario.run()

    calls = scenario.fake_process.payload_calls
    assert len(calls) == 2
    first = calls[0]["args"]
    session_id = first[first.index("--session-id") + 1]
    assert first[1:20] == [
        "--print",
        "--safe-mode",
        "--name",
        "reviewcompass3-no-tool-bootstrap",
        "--tools",
        "",
        "--disallowedTools",
        "*",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--disable-slash-commands",
        "--no-chrome",
        "--output-format",
        "json",
        "--model",
        "claude-fable-5",
        "--session-id",
        session_id,
    ]
    assert calls[1]["args"][3:5] == [
        "--name",
        "reviewcompass3-no-tool-bootstrap",
    ]
    assert "--resume" in calls[1]["args"]
    assert all(Path(call["cwd"]) == scenario.work_directory for call in calls)
    assert not any(scenario.work_directory.iterdir())


def test_first_payload_failure_prevents_second_payload_retry_and_fallback(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.fail_first_payload = True
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["payload_process_count"] == 1
    assert len(scenario.fake_process.payload_calls) == 1
    argv = scenario.fake_process.payload_calls[0]["args"]
    assert "--fallback-model" not in argv
    assert "--continue" not in argv


def test_outer_inner_json_session_nonce_no_tools_and_exit_code_must_all_match(
    tmp_path, monkeypatch
):
    mutations = (
        "unknown_outer_key",
        "missing_required_key",
        "success_is_error",
        "permission_denial",
        "error_subtype",
        "wrong_session",
        "extra_turn",
        "wrong_inner_json",
    )
    for mutation in mutations:
        with monkeypatch.context() as local:
            scenario = create_scenario(tmp_path / mutation, local)
            original = scenario.fake_process.__call__

            def malformed(args, **kwargs):
                completed = original(args, **kwargs)
                if "--print" not in args:
                    return completed
                value = copy.deepcopy(SUCCESS_RESULT)
                value["session_id"] = args[args.index("--session-id") + 1]
                if mutation == "unknown_outer_key":
                    value["unknown"] = True
                elif mutation == "missing_required_key":
                    value.pop("usage")
                elif mutation == "success_is_error":
                    value["is_error"] = True
                elif mutation == "permission_denial":
                    value["permission_denials"] = [
                        {
                            "tool_name": "Read",
                            "tool_use_id": "tool-1",
                            "tool_input": {},
                        }
                    ]
                elif mutation == "error_subtype":
                    value = copy.deepcopy(ERROR_RESULTS[0])
                elif mutation == "wrong_session":
                    value["session_id"] = (
                        "33333333-3333-4333-8333-333333333333"
                    )
                elif mutation == "extra_turn":
                    value["num_turns"] = 2
                elif mutation == "wrong_inner_json":
                    value["result"] = "{}"
                completed.stdout = json.dumps(value)
                return completed

            module = scenario.module()
            local.setattr(module.subprocess, "run", malformed)

            result = scenario.run()

            assert result["result"] == "stopped"


@pytest.mark.parametrize(
    "response_models",
    (
        ["claude-fable-5", "claude-fable-5"],
        ["claude-opus-5", "claude-opus-5"],
        ["claude-opus-4-8", "claude-opus-4-8"],
        ["claude-fable-5", "claude-opus-5"],
    ),
)
def test_human_selected_fable_allows_only_approved_response_models(
    tmp_path, monkeypatch, response_models
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.response_models = response_models
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    receipt = json.loads(Path(result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["requested_model"] == "claude-fable-5"
    assert receipt["actual_models_by_payload"] == [
        [response_models[0]],
        [response_models[1]],
    ]


def test_response_model_outside_human_approved_set_stops(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.response_models[0] = "claude-sonnet-5"
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "claude_result_invalid"
    assert result["payload_process_count"] == 1


def test_single_json_fence_is_normalized_before_exact_inner_comparison(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.fake_process.result_text_wrappers = ["json_fence", "json_fence"]
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    assert len(scenario.fake_process.payload_calls) == 2


@pytest.mark.parametrize(
    ("mutation", "expected_reason"),
    (
        ("prefixed", "inner_not_json"),
        ("fenced_with_prefix", "inner_not_json"),
        ("double_fence", "inner_not_json"),
        ("unknown_outer", "outer_contract_mismatch"),
        ("stderr", "stderr_present"),
    ),
)
def test_invalid_response_is_saved_with_precise_replayable_reason(
    tmp_path, monkeypatch, mutation, expected_reason
):
    scenario = create_scenario(tmp_path, monkeypatch)
    if mutation in {"prefixed", "fenced_with_prefix", "double_fence"}:
        scenario.fake_process.result_text_wrappers[0] = mutation
    elif mutation == "unknown_outer":
        scenario.fake_process.result_outer_updates[0] = {"unexpected": True}
    else:
        scenario.fake_process.payload_stderr[0] = "non-empty diagnostic"
    module = install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "claude_result_invalid"
    assert result["payload_process_count"] == 1
    result_root = (
        scenario.runtime_root
        / "projects"
        / "reviewcompass3-bootstrap-test"
        / "development/sensitive/claude-bootstrap/runs"
        / APPROVAL_ID
    )
    raw_path = result_root / "raw-1.json"
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    assert raw["returncode"] == 0
    assert set(raw) == {"schema_version", "returncode", "stdout", "stderr"}
    receipt = json.loads(
        (result_root / "receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["validation_failures"] == [
        {"payload_index": 1, "reason": expected_reason}
    ]
    assert receipt["raw_sha256"] == [sha256_bytes(raw_path.read_bytes())]

    calls_before_replay = len(scenario.fake_process.calls)
    replay = module._revalidate_saved_response(result_root, 1)

    assert replay == {
        "schema_version": 1,
        "payload_index": 1,
        "valid": False,
        "reason": expected_reason,
    }
    assert len(scenario.fake_process.calls) == calls_before_replay


def test_successful_saved_responses_are_revalidated_without_process(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    module = install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    result_root = Path(result["receipt_path"]).parent
    calls_before_replay = len(scenario.fake_process.calls)
    assert module._revalidate_saved_response(result_root, 1) == {
        "schema_version": 1,
        "payload_index": 1,
        "valid": True,
        "reason": "valid",
    }
    assert module._revalidate_saved_response(result_root, 2) == {
        "schema_version": 1,
        "payload_index": 2,
        "valid": True,
        "reason": "valid",
    }
    assert len(scenario.fake_process.calls) == calls_before_replay


def test_user_selected_model_is_loaded_from_approved_manifest(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)

    def select_opus_5(manifest):
        manifest["model"] = "claude-opus-5"
        manifest["allowed_response_models"] = ["claude-opus-5"]

    rebind_manifest(scenario, select_opus_5)
    scenario.fake_process.response_models = ["claude-opus-5", "claude-opus-5"]
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    assert all(
        call["args"][call["args"].index("--model") + 1] == "claude-opus-5"
        for call in scenario.fake_process.payload_calls
    )
    receipt = json.loads(Path(result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["requested_model"] == "claude-opus-5"
    assert receipt["allowed_response_models"] == ["claude-opus-5"]


def test_raw_launch_and_receipt_slots_are_exclusive_external_and_rereadable(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert result["result"] == "succeeded"
    result_root = (
        scenario.runtime_root
        / "projects"
        / "reviewcompass3-bootstrap-test"
        / "development/sensitive/claude-bootstrap/runs"
        / APPROVAL_ID
    )
    files = sorted(path for path in result_root.rglob("*") if path.is_file())
    assert len(files) == 4
    assert {path.name for path in files} == {
        "launch.json",
        "raw-1.json",
        "raw-2.json",
        "receipt.json",
    }
    assert all(scenario.repository not in path.parents for path in files)
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))


def test_every_stop_result_has_reason_process_counts_approval_state_and_recovery(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    scenario.token_path.unlink()
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert_stop(result, "approval_store_missing", scenario)
    assert set(result) == {
        "schema_version",
        "result",
        "stop_code",
        "payload_process_count",
        "preflight_process_count",
        "approval_state",
        "recovery",
    }


def test_fixed_manifest_payload_order_binary_and_result_schema_fail_closed(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)

    def reverse_payloads(manifest):
        manifest["payloads"].reverse()

    rebind_manifest(scenario, reverse_payloads)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    assert_stop(result, "manifest_contract_mismatch", scenario)


def test_only_claude_ai_first_party_authentication_is_accepted(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    original = scenario.fake_process.__call__

    def unauthenticated(args, **kwargs):
        completed = original(args, **kwargs)
        if "auth" in args and "status" in args:
            completed.stdout = json.dumps(
                {
                    "loggedIn": False,
                    "authMethod": "none",
                    "apiProvider": "firstParty",
                }
            )
        return completed

    module = scenario.module()
    monkeypatch.setattr(module.subprocess, "run", unauthenticated)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "authentication_not_approved"
    assert scenario.fake_process.payload_calls == []


def test_claude_ai_authentication_accepts_non_secret_status_metadata(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    original = scenario.fake_process.__call__

    def authenticated_with_metadata(args, **kwargs):
        completed = original(args, **kwargs)
        if "auth" in args and "status" in args:
            value = json.loads(completed.stdout)
            value.update(
                {
                    "email": "reviewer@example.invalid",
                    "orgId": "00000000-0000-4000-8000-000000000000",
                    "orgName": "Example Organization",
                    "subscriptionType": "max",
                }
            )
            completed.stdout = json.dumps(value)
        return completed

    module = scenario.module()
    monkeypatch.setattr(module.subprocess, "run", authenticated_with_metadata)

    result = scenario.run()

    assert result["result"] == "succeeded"
    assert len(scenario.fake_process.payload_calls) == 2
    assert "reviewer@example.invalid" not in json.dumps(result)


def test_api_key_authentication_source_is_rejected(tmp_path, monkeypatch):
    scenario = create_scenario(tmp_path, monkeypatch)
    original = scenario.fake_process.__call__

    def authenticated_with_api_key_source(args, **kwargs):
        completed = original(args, **kwargs)
        if "auth" in args and "status" in args:
            value = json.loads(completed.stdout)
            value["apiKeySource"] = "ANTHROPIC_API_KEY"
            completed.stdout = json.dumps(value)
        return completed

    module = scenario.module()
    monkeypatch.setattr(module.subprocess, "run", authenticated_with_api_key_source)

    result = scenario.run()

    assert result["result"] == "stopped"
    assert result["stop_code"] == "authentication_not_approved"
    assert scenario.fake_process.payload_calls == []


def test_receipt_contract_fixes_real_run_provenance_without_performing_real_run(
    tmp_path, monkeypatch
):
    scenario = create_scenario(tmp_path, monkeypatch)
    install_fake_process(monkeypatch, scenario)

    result = scenario.run()

    receipt_path = Path(result["receipt_path"])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["approval_id"] == APPROVAL_ID
    assert receipt["approval_state"] == "consumed"
    assert receipt["provider"] == "claude-code-first-party"
    assert receipt["requested_model"] == "claude-fable-5"
    assert receipt["allowed_response_models"] == [
        "claude-fable-5",
        "claude-opus-5",
        "claude-opus-4-8",
    ]
    assert receipt["actual_models_by_payload"] == [
        ["claude-fable-5"],
        ["claude-fable-5"],
    ]
    assert receipt["auth_method"] == "claude.ai"
    assert receipt["payload_sha256"] == [
        item["sha256"] for item in CONTRACT["payloads"]
    ]
    assert len(receipt["raw_sha256"]) == 2
    assert len(receipt["session_id"]) == 1
    assert receipt["exit_code"] == [0, 0]
    assert receipt["storage_result"] == "saved"
    assert receipt["local_owner_rollback_detection"] == "not_guaranteed"
