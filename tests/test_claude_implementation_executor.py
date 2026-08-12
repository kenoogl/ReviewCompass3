"""Claude実装委譲の起動・応答変換境界テスト。"""

import importlib
import json
import os
from pathlib import Path
import subprocess

import pytest

from tests import test_claude_implementation_route as route_test


ALLOWED_RESPONSE_MODELS = (
    "claude-fable-5",
    "claude-opus-5",
    "claude-opus-4-8",
)
APPROVAL_ID = "RC3-CD-SEND-APPROVAL-001"


def _executor():
    return importlib.import_module(
        "tools.development.claude_implementation_executor"
    )


def _write_send_approval(case):
    store = case.private_root / "approval-store"
    store.mkdir(parents=True, exist_ok=True)
    store.chmod(0o700)
    for state in ("pending", "claimed", "consumed"):
        directory = store / state
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
    token = store / "pending" / f"{APPROVAL_ID}.json"
    route_test._write_json(
        token,
        {
            "schema_version": 1,
            "approval_id": APPROVAL_ID,
            "approved_by": "user",
            "purpose": "claude_implementation_executor_confirmation",
            "run_id": case.run_id,
            "configuration_sha256": route_test._sha256(
                (
                    case.private_root
                    / case.run_id
                    / "configuration/start.json"
                ).read_bytes()
            ),
            "private_root_sha256": route_test._sha256(
                str(case.private_root.resolve()).encode("utf-8")
            ),
            "expires_at": "2999-01-01T00:00:00Z",
            "maximum_payload_processes": 2,
        },
    )
    token.chmod(0o600)


def _manifest_arguments(case):
    path = case.private_root / case.run_id / "configuration/start.json"
    return path, route_test._sha256(path.read_bytes())


def _prepared_case(tmp_path, *, approval=True):
    route = route_test._route()
    case = route_test._create_case(tmp_path)
    case.config["claude_runtime"]["allowed_response_models"] = list(
        ALLOWED_RESPONSE_MODELS
    )
    route_test._save_config(case)
    outcome = route.prepare(case.repository, case.config_path, case.private_root)
    case.worktree = Path(outcome["worktree"])
    if approval:
        _write_send_approval(case)
    return route, case


def _outer_result(
    session_id,
    tool_name,
    file_path,
    *,
    model="claude-fable-5",
    tool_input=None,
):
    return "\n".join(
        json.dumps(value, separators=(",", ":"), sort_keys=True)
        for value in (
            {
                "type": "system",
                "subtype": "init",
                "session_id": session_id,
                "model": model,
                "tools": ["Edit", "Glob", "Grep", "Read", "Write"],
                "mcp_servers": [],
                "plugins": [],
                "permissionMode": "dontAsk",
                "slash_commands": [],
                "skills": [],
                "agents": [],
            },
            {
                "type": "assistant",
                "session_id": session_id,
                "message": {
                    "model": model,
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "tool-use-001",
                            "name": tool_name,
                            "input": (
                                {"file_path": str(file_path)}
                                if tool_input is None
                                else tool_input
                            ),
                        }
                    ],
                },
            },
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "session_id": session_id,
                "result": "changed one synthetic file",
                "modelUsage": {model: {}},
                "permission_denials": [],
            },
        )
    ) + "\n"


class FakeClaudeProcess:
    def __init__(self, case):
        self.case = case
        self.calls = []
        self.payload_calls = []
        self.response_model = "claude-fable-5"
        self.tool_name = "Write"
        self.tool_input = None
        self.emit_retry = False
        self.payload_stderr = ""

    def __call__(
        self,
        arguments,
        *,
        cwd,
        env,
        check,
        capture_output,
        text,
        shell,
    ):
        call = {
            "arguments": list(arguments),
            "cwd": Path(cwd),
            "env": dict(env),
            "check": check,
            "capture_output": capture_output,
            "text": text,
            "shell": shell,
        }
        self.calls.append(call)
        if list(arguments[1:]) == ["--version"]:
            return subprocess.CompletedProcess(arguments, 0, "1.0.0-pinned (Claude Code)\n", "")
        if list(arguments[1:]) == ["auth", "status", "--json"]:
            value = {
                "loggedIn": True,
                "authMethod": "claude.ai",
                "apiProvider": "firstParty",
            }
            return subprocess.CompletedProcess(
                arguments,
                0,
                json.dumps(value),
                "",
            )
        self.payload_calls.append(call)
        if "--session-id" in arguments:
            session_id = arguments[arguments.index("--session-id") + 1]
            target = self.case.worktree / route_test.TEST_PATH
            route_test._write_test_change(self.case)
        else:
            session_id = arguments[arguments.index("--resume") + 1]
            target = self.case.worktree / route_test.PRODUCTION_PATH
            route_test._write_implementation_change(self.case)
        output = _outer_result(
            session_id,
            self.tool_name,
            target,
            model=self.response_model,
            tool_input=self.tool_input,
        )
        if self.emit_retry:
            retry = json.dumps(
                {"type": "system", "subtype": "api_retry", "attempt": 1}
            )
            output = retry + "\n" + output
        return subprocess.CompletedProcess(
            arguments,
            0,
            output,
            self.payload_stderr,
        )


def _install_fake(monkeypatch, executor, case):
    fake = FakeClaudeProcess(case)
    monkeypatch.setattr(executor.subprocess, "run", fake)
    return fake


def test_parser_ignores_non_action_metadata_without_knowing_its_name(tmp_path):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-observed-metadata"
    base_events = _outer_result(
        session_id,
        "Write",
        worktree / "tests/test_feature.py",
    ).splitlines()
    events = [
        base_events[0],
        json.dumps(
            {
                "type": "system",
                "subtype": "thinking_tokens",
                "token_count": 128,
            }
        ),
        json.dumps(
            {
                "type": "rate_limit_event",
                "rate_limit_info": {"status": "allowed"},
            }
        ),
        json.dumps(
            {
                "type": "future_non_action_metadata",
                "payload": {"new_field": [1, 2, 3]},
            }
        ),
        *base_events[1:],
    ]

    result = executor._parse_stream(
        "\n".join(events) + "\n",
        session_id,
        ALLOWED_RESPONSE_MODELS,
        worktree,
    )

    assert result["response_model"] == "claude-fable-5"
    assert result["tool_uses"][0]["path"] == "tests/test_feature.py"


@pytest.mark.parametrize(
    "variation",
    (
        "non_json_notice",
        "init_optional_fields_missing",
        "init_event_missing",
        "result_optional_fields_missing",
    ),
)
def test_parser_requires_outcome_evidence_but_tolerates_transport_drift(
    tmp_path,
    variation,
):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-transport-drift"
    events = [
        json.loads(line)
        for line in _outer_result(
            session_id,
            "Write",
            worktree / "tests/test_feature.py",
        ).splitlines()
    ]
    prefix = []
    if variation == "non_json_notice":
        prefix = ["Claude Code notice: optional telemetry changed", "[]"]
    elif variation == "init_optional_fields_missing":
        events[0] = {
            "type": "system",
            "subtype": "init",
            "session_id": session_id,
            "model": "claude-fable-5",
            "tools": ["Edit", "Glob", "Grep", "Read", "Write"],
        }
    elif variation == "init_event_missing":
        events.pop(0)
    else:
        events[-1].pop("modelUsage")
        events[-1].pop("permission_denials")

    stdout = "\n".join(
        [*prefix, *(json.dumps(event) for event in events)]
    ) + "\n"
    result = executor._parse_stream(
        stdout,
        session_id,
        ALLOWED_RESPONSE_MODELS,
        worktree,
    )

    assert result["response_model"] == "claude-fable-5"
    assert result["tool_uses"][0]["path"] == "tests/test_feature.py"


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("tools", ["Edit", "Glob", "Grep", "Read", "Write", "Bash"]),
        ("mcp_servers", [{"name": "unapproved"}]),
        ("plugins", [{"name": "unapproved"}]),
        ("permissionMode", "acceptEdits"),
    ),
)
def test_parser_rejects_explicit_runtime_capability_contradictions(
    tmp_path,
    field,
    value,
):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-explicit-capability"
    events = [
        json.loads(line)
        for line in _outer_result(
            session_id,
            "Write",
            worktree / "tests/test_feature.py",
        ).splitlines()
    ]
    events[0][field] = value

    with pytest.raises(executor.ExecutorStop) as caught:
        executor._parse_stream(
            "\n".join(json.dumps(event) for event in events) + "\n",
            session_id,
            ALLOWED_RESPONSE_MODELS,
            worktree,
        )

    assert caught.value.code == "runtime_capabilities_invalid"


def test_parser_rejects_tool_use_hidden_in_unknown_event(tmp_path):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-hidden-action"
    events = [
        json.dumps(
            {
                "type": "future_event",
                "payload": {
                    "type": "tool_use",
                    "name": "Bash",
                    "input": {"command": "echo forbidden"},
                },
            }
        ),
        *_outer_result(
            session_id,
            "Write",
            worktree / "tests/test_feature.py",
        ).splitlines(),
    ]

    with pytest.raises(executor.ExecutorStop) as caught:
        executor._parse_stream(
            "\n".join(events) + "\n",
            session_id,
            ALLOWED_RESPONSE_MODELS,
            worktree,
        )

    assert caught.value.code == "forbidden_tool_use"


def test_parser_rejects_runtime_capabilities_that_exceed_approval(tmp_path):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-extra-capability"
    output = _outer_result(
        session_id,
        "Write",
        worktree / "tests/test_feature.py",
    )
    events = [json.loads(line) for line in output.splitlines()]
    events[0]["tools"].append("Bash")

    with pytest.raises(executor.ExecutorStop) as caught:
        executor._parse_stream(
            "\n".join(json.dumps(event) for event in events) + "\n",
            session_id,
            ALLOWED_RESPONSE_MODELS,
            worktree,
        )

    assert caught.value.code == "runtime_capabilities_invalid"


def test_executor_accepts_harmless_stderr_when_result_is_valid(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    fake.payload_stderr = "non-fatal provider notice\n"

    result = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )

    assert result["state"] == "ready_for_implementation_turn"
    provider_raw = json.loads(Path(result["execution"]["provider_raw"]).read_text())
    assert provider_raw["stderr"] == "non-fatal provider notice\n"


def test_parser_rejects_explicit_permission_denial(tmp_path):
    executor = _executor()
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    session_id = "session-permission-denied"
    events = [
        json.dumps(
            {
                "type": "system",
                "subtype": "permission_denied",
                "session_id": session_id,
                "tool_name": "Write",
            }
        ),
        *_outer_result(
            session_id,
            "Write",
            worktree / "tests/test_feature.py",
        ).splitlines(),
    ]

    with pytest.raises(executor.ExecutorStop) as caught:
        executor._parse_stream(
            "\n".join(events) + "\n",
            session_id,
            ALLOWED_RESPONSE_MODELS,
            worktree,
        )

    assert caught.value.code == "permission_denied"


def test_executor_runs_two_fixed_turns_and_core_becomes_ready_for_review(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    route, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)

    first = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )
    second = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "implementation",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )

    assert first["state"] == "ready_for_implementation_turn"
    assert second["state"] == "ready_for_review"
    assert route.status(case.repository, case.private_root, case.run_id)["state"] == (
        "ready_for_review"
    )
    assert not (
        case.private_root / "approval-store/claimed" / f"{APPROVAL_ID}.json"
    ).exists()
    assert (
        case.private_root / "approval-store/consumed" / f"{APPROVAL_ID}.json"
    ).is_file()
    assert len(fake.payload_calls) == 2
    first_arguments = fake.payload_calls[0]["arguments"]
    second_arguments = fake.payload_calls[1]["arguments"]
    assert first_arguments[:2] == [str(case.executable), "--print"]
    assert "--tools" in first_arguments
    assert first_arguments[first_arguments.index("--tools") + 1] == (
        "Read,Glob,Grep,Edit,Write"
    )
    allowed_index = first_arguments.index("--allowedTools")
    assert first_arguments[allowed_index + 1:allowed_index + 3] == [
        "Read(/**)",
        f"Edit(/{route_test.TEST_PATH})",
    ]
    second_allowed_index = second_arguments.index("--allowedTools")
    assert second_arguments[
        second_allowed_index + 1:second_allowed_index + 3
    ] == [
        "Read(/**)",
        f"Edit(/{route_test.PRODUCTION_PATH})",
    ]
    disallowed_index = first_arguments.index("--disallowedTools")
    assert first_arguments[disallowed_index + 1:disallowed_index + 8] == list(
        executor.DISALLOWED_TOOLS
    )
    assert first_arguments[first_arguments.index("--permission-mode") + 1] == (
        "dontAsk"
    )
    assert "--fallback-model" not in first_arguments
    assert "--resume" in second_arguments
    assert second_arguments[second_arguments.index("--resume") + 1] == (
        first_arguments[first_arguments.index("--session-id") + 1]
    )
    assert all(call["cwd"] == case.worktree for call in fake.payload_calls)
    assert all(call["shell"] is False for call in fake.calls)
    for call in fake.payload_calls:
        assert call["env"]["CLAUDE_CODE_MAX_RETRIES"] == "0"
        assert "ANTHROPIC_API_KEY" not in call["env"]


def test_executor_preserves_provider_raw_and_normalizes_tool_use(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    _install_fake(monkeypatch, executor, case)

    result = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )

    execution = result["execution"]
    provider_raw = json.loads(Path(execution["provider_raw"]).read_text())
    normalized_raw = json.loads(Path(execution["normalized_raw"]).read_text())
    launch = json.loads(Path(execution["launch_record"]).read_text())
    assert provider_raw["returncode"] == 0
    assert '"type":"assistant"' in provider_raw["stdout"]
    assert normalized_raw["tool_uses"] == [
        {
            "tool": "Write",
            "path": route_test.TEST_PATH,
            "input": {"file_path": str(case.worktree / route_test.TEST_PATH)},
        }
    ]
    assert normalized_raw["response_model"] == "claude-fable-5"
    assert launch["process_kind"] == "claude_code_first_party"
    assert launch["external_process_count"] == 1


@pytest.mark.parametrize(
    ("mutation", "stop_code"),
    (
        ("retry", "automatic_retry_detected"),
        ("forbidden_tool", "forbidden_tool_use"),
        ("model", "response_model_invalid"),
    ),
)
def test_executor_stops_invalid_provider_results_before_core_ingest(
    tmp_path,
    monkeypatch,
    mutation,
    stop_code,
):
    executor = _executor()
    route, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    if mutation == "retry":
        fake.emit_retry = True
    elif mutation == "forbidden_tool":
        fake.tool_name = "Bash"
    else:
        fake.response_model = "claude-unapproved"

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )

    assert caught.value.code == stop_code
    assert route.status(case.repository, case.private_root, case.run_id)["state"] == (
        "ready_for_test_turn"
    )
    raw = case.private_root / case.run_id / "executor" / "test" / "provider-raw.json"
    assert raw.is_file()


@pytest.mark.parametrize(
    ("tool_name", "tool_input"),
    (
        ("Read", {"file_path": "/private/tmp/outside-secret.txt"}),
        (
            "Glob",
            {"pattern": "**/*", "path": "/private/tmp"},
        ),
        (
            "Grep",
            {"pattern": "secret", "path": "/private/tmp"},
        ),
    ),
)
def test_executor_rejects_read_tools_outside_worktree(
    tmp_path,
    monkeypatch,
    tool_name,
    tool_input,
):
    executor = _executor()
    route, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    fake.tool_name = tool_name
    fake.tool_input = tool_input

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )

    assert caught.value.code == "administrator_boundary_violation"
    assert route.status(case.repository, case.private_root, case.run_id)["state"] == (
        "ready_for_test_turn"
    )


def test_executor_rejects_unapproved_prompt_before_any_process(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    launch = case.private_root / case.run_id / "launch" / "test.json"
    value = json.loads(launch.read_text())
    value["prompt"] = "changed prompt"
    route_test._write_json(launch, value)

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )

    assert caught.value.code == "launch_request_invalid"
    assert fake.calls == []


def test_executor_rejects_api_key_environment_before_any_process(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "must-not-be-used")

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )

    assert caught.value.code == "api_key_environment_forbidden"
    assert fake.calls == []


def test_executor_requires_separate_one_time_send_approval_before_any_process(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path, approval=False)
    fake = _install_fake(monkeypatch, executor, case)

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )

    assert caught.value.code == "external_send_approval_required"
    assert fake.calls == []


def test_executor_rejects_manifest_mismatch_before_any_process(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    manifest_path, _ = _manifest_arguments(case)

    with pytest.raises(executor.ExecutorStop) as caught:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            manifest_path,
            "0" * 64,
        )

    assert caught.value.code == "manifest_mismatch"
    assert fake.calls == []


def test_executor_revalidates_saved_response_without_resending(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    route, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    original_parser = executor._parse_stream

    def local_parser_failure(*arguments):
        del arguments
        raise executor.ExecutorStop("provider_result_invalid")

    monkeypatch.setattr(executor, "_parse_stream", local_parser_failure)
    with pytest.raises(executor.ExecutorStop) as first_failure:
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )
    assert first_failure.value.code == "provider_result_invalid"
    assert len(fake.payload_calls) == 1

    claimed = (
        case.private_root / "approval-store/claimed" / f"{APPROVAL_ID}.json"
    )
    consumed = (
        case.private_root / "approval-store/consumed" / f"{APPROVAL_ID}.json"
    )
    if claimed.is_file():
        claimed.replace(consumed)
    monkeypatch.setattr(executor, "_parse_stream", original_parser)

    recovered = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )

    assert recovered["state"] == "ready_for_implementation_turn"
    assert recovered["execution"]["revalidated_without_process"] is True
    assert len(fake.payload_calls) == 1
    assert claimed.is_file()
    assert not consumed.exists()
    assert route.status(case.repository, case.private_root, case.run_id)["state"] == (
        "ready_for_implementation_turn"
    )

    completed = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "implementation",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )
    assert completed["state"] == "ready_for_review"
    assert len(fake.payload_calls) == 2
    assert consumed.is_file()


def test_executor_revalidates_saved_implementation_without_double_consuming(
    tmp_path,
    monkeypatch,
):
    executor = _executor()
    _, case = _prepared_case(tmp_path)
    fake = _install_fake(monkeypatch, executor, case)
    executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )
    original_parser = executor._parse_stream

    def local_parser_failure(*arguments):
        del arguments
        raise executor.ExecutorStop("provider_result_invalid")

    monkeypatch.setattr(executor, "_parse_stream", local_parser_failure)
    with pytest.raises(executor.ExecutorStop):
        executor.execute_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "implementation",
            APPROVAL_ID,
            *_manifest_arguments(case),
        )
    assert len(fake.payload_calls) == 2
    monkeypatch.setattr(executor, "_parse_stream", original_parser)

    recovered = executor.execute_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "implementation",
        APPROVAL_ID,
        *_manifest_arguments(case),
    )

    assert recovered["state"] == "ready_for_review"
    assert recovered["execution"]["revalidated_without_process"] is True
    assert len(fake.payload_calls) == 2
    assert (
        case.private_root / "approval-store/consumed" / f"{APPROVAL_ID}.json"
    ).is_file()
