"""承認済みClaude実装ターンの固定起動と応答変換。"""

import datetime
import json
import os
from pathlib import Path
import re
import stat
import subprocess as _subprocess
import uuid

from tools.bootstrap.immutable_result_store import (
    ImmutableResultStoreError,
    canonical_json_bytes,
    store_immutable_json,
)
from tools.common.digests import sha256_hex
from tools.development import claude_implementation_route as route


ALLOWED_TOOLS = ("Read", "Glob", "Grep", "Edit", "Write")
DISALLOWED_TOOLS = (
    "Bash",
    "WebFetch",
    "WebSearch",
    "Agent",
    "Task",
    "Skill",
    "AskUserQuestion",
)
ALLOWED_CHILD_ENVIRONMENT = (
    "HOME",
    "USER",
    "PATH",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "NO_COLOR",
)
FORBIDDEN_AUTH_ENVIRONMENT = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_FOUNDRY_API_KEY",
    "ANTHROPIC_VERTEX_PROJECT_ID",
    "AWS_BEARER_TOKEN_BEDROCK",
)
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_SHA256 = re.compile(r"[0-9a-f]{64}")


class _SubprocessFacade:
    """試験差替えをこのmodule内だけに閉じるprocess入口。"""

    run = staticmethod(_subprocess.run)


subprocess = _SubprocessFacade()


class ExecutorStop(Exception):
    """Claudeを起動または結果取込みできないため停止した。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _stop(code):
    raise ExecutorStop(code)


def _read_canonical_json(path, code):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        _stop(code)
    try:
        data = path.read_bytes()
        value = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        _stop(code)
    if data != canonical_json_bytes(value) + b"\n":
        _stop(code)
    return value


def _store(root, relative_path, document):
    try:
        stored = store_immutable_json(root, relative_path, document)
    except ImmutableResultStoreError:
        _stop("executor_storage_unavailable")
    return Path(root) / stored.relative_path, stored.file_sha256


def _safe_approval_directory(path):
    return (
        path.is_dir()
        and not path.is_symlink()
        and stat.S_IMODE(path.stat().st_mode) == 0o700
    )


def _send_approval(private_root, run_id, approval_id, config_path, turn):
    if not isinstance(approval_id, str) or _IDENTIFIER.fullmatch(approval_id) is None:
        _stop("external_send_approval_required")
    store = private_root / "approval-store"
    directories = {
        state: store / state
        for state in ("pending", "claimed", "consumed")
    }
    if not _safe_approval_directory(store) or any(
        not _safe_approval_directory(directory)
        for directory in directories.values()
    ):
        _stop("external_send_approval_required")
    states = []
    for state, directory in directories.items():
        path = directory / f"{approval_id}.json"
        if path.exists() or path.is_symlink():
            states.append((state, path))
    expected_state = "pending" if turn == "test" else "claimed"
    if len(states) != 1 or states[0][0] != expected_state:
        _stop("external_send_approval_required")
    token_path = states[0][1]
    if (
        token_path.is_symlink()
        or not token_path.is_file()
        or stat.S_IMODE(token_path.stat().st_mode) != 0o600
    ):
        _stop("external_send_approval_required")
    token = _read_canonical_json(
        token_path,
        "external_send_approval_required",
    )
    expected = {
        "schema_version": 1,
        "approval_id": approval_id,
        "approved_by": "user",
        "purpose": "claude_implementation_executor_confirmation",
        "run_id": run_id,
        "configuration_sha256": sha256_hex(config_path.read_bytes()),
        "private_root_sha256": sha256_hex(
            str(private_root).encode("utf-8")
        ),
        "expires_at": token.get("expires_at"),
        "maximum_payload_processes": 2,
    }
    if token != expected:
        _stop("external_send_approval_required")
    try:
        expires = datetime.datetime.fromisoformat(
            token["expires_at"].replace("Z", "+00:00")
        )
    except (AttributeError, ValueError):
        _stop("external_send_approval_required")
    if expires <= datetime.datetime.now(datetime.timezone.utc):
        _stop("external_send_approval_expired")
    return token_path, directories


def _move_approval(source, target):
    if target.exists() or target.is_symlink():
        _stop("external_send_approval_required")
    try:
        os.replace(source, target)
    except OSError:
        _stop("external_send_approval_required")
    return target


def _child_environment():
    if any(name in os.environ for name in FORBIDDEN_AUTH_ENVIRONMENT):
        _stop("api_key_environment_forbidden")
    environment = {
        name: os.environ[name]
        for name in ALLOWED_CHILD_ENVIRONMENT
        if name in os.environ
    }
    environment.update(
        {
            "CLAUDE_CODE_MAX_RETRIES": "0",
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
            "CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL": "1",
            "CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS": "1",
            "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
            "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
            "CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS": "1",
            "ENABLE_CLAUDEAI_MCP_SERVERS": "false",
            "DISABLE_AUTOUPDATER": "1",
        }
    )
    return environment


def _invoke(arguments, worktree, environment):
    try:
        return subprocess.run(
            list(arguments),
            cwd=str(worktree),
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
    except (OSError, PermissionError):
        _stop("claude_process_failed")


def _validate_preflight(config, worktree, environment):
    runtime = config["claude_runtime"]
    executable = Path(runtime["executable"])
    try:
        digest = sha256_hex(executable.read_bytes())
    except OSError:
        _stop("claude_executable_mismatch")
    if digest != runtime["expected_executable_sha256"]:
        _stop("claude_executable_mismatch")
    version = _invoke((str(executable), "--version"), worktree, environment)
    if (
        version.returncode != 0
        or version.stderr
        or not version.stdout.strip().startswith(runtime["expected_version"] + " ")
    ):
        _stop("claude_version_mismatch")
    authentication = _invoke(
        (str(executable), "auth", "status", "--json"),
        worktree,
        environment,
    )
    try:
        value = json.loads(authentication.stdout)
    except (TypeError, json.JSONDecodeError):
        _stop("claude_authentication_invalid")
    if (
        authentication.returncode != 0
        or authentication.stderr
        or not isinstance(value, dict)
        or value.get("loggedIn") is not True
        or value.get("authMethod") != "claude.ai"
        or value.get("apiProvider") != "firstParty"
        or "apiKeySource" in value
    ):
        _stop("claude_authentication_invalid")


def _relative_edit_path(value, worktree):
    if not isinstance(value, str) or not value or "\x00" in value:
        _stop("provider_result_invalid")
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = worktree / candidate
    try:
        relative = candidate.resolve().relative_to(worktree.resolve())
    except (OSError, ValueError):
        _stop("administrator_boundary_violation")
    return relative.as_posix()


def _relative_read_path(value, worktree):
    if not isinstance(value, str) or not value or "\x00" in value:
        _stop("provider_result_invalid")
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = worktree / candidate
    try:
        relative = candidate.resolve().relative_to(worktree.resolve())
    except (OSError, ValueError):
        _stop("administrator_boundary_violation")
    return relative.as_posix()


def _contains_marker(value, key, expected):
    if isinstance(value, dict):
        return value.get(key) == expected or any(
            _contains_marker(item, key, expected)
            for item in value.values()
        )
    if isinstance(value, list):
        return any(_contains_marker(item, key, expected) for item in value)
    return False


def _parse_stream(stdout, session_id, allowed_models, worktree):
    events = []
    try:
        for line in stdout.splitlines():
            if not line:
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError
            events.append(value)
    except (json.JSONDecodeError, ValueError):
        _stop("provider_result_invalid")
    if not events:
        _stop("provider_result_invalid")

    tool_uses = []
    actual_models = []
    initialization = None
    result = None
    for event in events:
        event_type = event.get("type")
        if _contains_marker(event, "subtype", "api_retry"):
            _stop("automatic_retry_detected")
        if event_type == "system" and event.get("subtype") == "permission_denied":
            _stop("permission_denied")
        if event_type == "system" and event.get("subtype") == "init":
            if initialization is not None:
                _stop("runtime_capabilities_invalid")
            tools = event.get("tools")
            if event.get("model") not in allowed_models:
                _stop("response_model_invalid")
            if (
                event.get("session_id") != session_id
                or not isinstance(tools, list)
                or len(tools) != len(ALLOWED_TOOLS)
                or set(tools) != set(ALLOWED_TOOLS)
                or event.get("mcp_servers") != []
                or event.get("plugins") != []
                or event.get("plugin_errors") not in (None, [])
                or event.get("mcp_server_errors") not in (None, [])
                or event.get("permissionMode") != "dontAsk"
                or event.get("slash_commands") != []
                or event.get("skills") != []
                or event.get("agents") != []
            ):
                _stop("runtime_capabilities_invalid")
            initialization = event
        if event_type != "assistant" and _contains_marker(
            event,
            "type",
            "tool_use",
        ):
            _stop("forbidden_tool_use")
        if event_type == "assistant":
            message = event.get("message")
            if not isinstance(message, dict):
                _stop("provider_result_invalid")
            model = message.get("model")
            if model not in allowed_models:
                _stop("response_model_invalid")
            actual_models.append(model)
            content = message.get("content")
            if not isinstance(content, list):
                _stop("provider_result_invalid")
            for block in content:
                if not isinstance(block, dict):
                    _stop("provider_result_invalid")
                if block.get("type") != "tool_use":
                    continue
                name = block.get("name")
                input_value = block.get("input")
                if name not in ALLOWED_TOOLS or not isinstance(input_value, dict):
                    _stop("forbidden_tool_use")
                normalized = {"tool": name, "input": input_value}
                if name in ("Edit", "Write"):
                    normalized["path"] = _relative_edit_path(
                        input_value.get("file_path"),
                        worktree,
                    )
                elif name == "Read":
                    normalized["path"] = _relative_read_path(
                        input_value.get("file_path"),
                        worktree,
                    )
                elif name in ("Glob", "Grep"):
                    search_path = input_value.get("path")
                    if search_path is not None:
                        normalized["path"] = _relative_read_path(
                            search_path,
                            worktree,
                        )
                    if name == "Glob":
                        pattern = input_value.get("pattern")
                        if not isinstance(pattern, str) or not pattern:
                            _stop("provider_result_invalid")
                        if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
                            _relative_read_path(pattern, worktree)
                tool_uses.append(normalized)
        elif event_type == "result":
            if result is not None:
                _stop("provider_result_invalid")
            result = event

    if (
        initialization is None
        or result is None
        or result.get("subtype") != "success"
        or result.get("is_error") is not False
        or result.get("session_id") != session_id
        or not isinstance(result.get("result"), str)
        or result.get("permission_denials") != []
        or not isinstance(result.get("modelUsage"), dict)
        or not actual_models
    ):
        _stop("provider_result_invalid")
    for model, usage in result["modelUsage"].items():
        if model not in allowed_models or not isinstance(usage, dict):
            _stop("response_model_invalid")
        actual_models.append(model)
    if any(model not in allowed_models for model in actual_models):
        _stop("response_model_invalid")
    return {
        "response_model": actual_models[-1],
        "text": result["result"],
        "tool_uses": tool_uses,
    }


def _session_id(run_root, turn):
    if turn == "test":
        return str(uuid.uuid4())
    receipt = _read_canonical_json(
        run_root / "executor" / "test" / "receipt.json",
        "state_not_ready",
    )
    value = receipt.get("session_id") if isinstance(receipt, dict) else None
    if not isinstance(value, str) or not value:
        _stop("state_not_ready")
    return value


def _arguments(config, launch, worktree, session_id, turn):
    runtime = config["claude_runtime"]
    allowed_path = config["allowed_paths"][turn][0]
    allowed_rules = (
        "Read(/**)",
        f"Edit(/{allowed_path})",
    )
    base = [
        runtime["executable"],
        "--print",
        "--safe-mode",
        "--name",
        "reviewcompass3-claude-implementation",
        "--tools",
        ",".join(ALLOWED_TOOLS),
        "--allowedTools",
        *allowed_rules,
        "--disallowedTools",
        *DISALLOWED_TOOLS,
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--disable-slash-commands",
        "--no-chrome",
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        runtime["requested_model"],
    ]
    if turn == "test":
        return [*base, "--session-id", session_id, launch["prompt"]]
    return [*base, "--resume", session_id, launch["prompt"]]


def _record_parsed_turn(
    repository,
    private_root,
    run_id,
    turn,
    run_root,
    config,
    launch_path,
    session_id,
    provider_raw_path,
    provider_raw_sha256,
    parsed,
    *,
    revalidated_without_process,
):
    normalized_raw_path, normalized_raw_sha256 = _store(
        run_root,
        f"executor/{turn}/normalized-raw.json",
        {
            "schema_version": 1,
            "run_id": run_id,
            "turn": turn,
            "status": "completed",
            "response_model": parsed["response_model"],
            "text": parsed["text"],
            "tool_uses": parsed["tool_uses"],
            "reported_test_exit_code": None,
            "provider_raw_sha256": provider_raw_sha256,
        },
    )
    launch_record_path, _ = _store(
        run_root,
        f"executor/{turn}/launch-record.json",
        {
            "schema_version": 1,
            "run_id": run_id,
            "turn": turn,
            "session_id": session_id,
            "status": "completed",
            "launch_request_sha256": sha256_hex(launch_path.read_bytes()),
            "raw_sha256": normalized_raw_sha256,
            "process_kind": "claude_code_first_party",
            "external_process_count": 1,
            "model": parsed["response_model"],
            "authentication": config["claude_runtime"]["authentication"],
            "provider_raw_sha256": provider_raw_sha256,
        },
    )
    try:
        outcome = route.record_turn(
            repository,
            private_root,
            run_id,
            turn,
            launch_record_path,
            normalized_raw_path,
        )
    except route.RouteStop as error:
        _store(
            run_root,
            f"executor/{turn}/receipt.json",
            {
                "schema_version": 1,
                "turn": turn,
                "session_id": session_id,
                "status": "stopped",
                "stop_code": error.code,
                "provider_raw_sha256": provider_raw_sha256,
            },
        )
        _stop(error.code)
    receipt_path, _ = _store(
        run_root,
        f"executor/{turn}/receipt.json",
        {
            "schema_version": 1,
            "turn": turn,
            "session_id": session_id,
            "status": "completed",
            "state": outcome["state"],
            "provider_raw_sha256": provider_raw_sha256,
            "revalidated_without_process": revalidated_without_process,
        },
    )
    result = dict(outcome)
    result["execution"] = {
        "invocation": str(run_root / f"executor/{turn}/invocation.json"),
        "provider_raw": str(provider_raw_path),
        "normalized_raw": str(normalized_raw_path),
        "launch_record": str(launch_record_path),
        "receipt": str(receipt_path),
        "revalidated_without_process": revalidated_without_process,
    }
    return result


def _recover_saved_turn(
    repository,
    private_root,
    run_id,
    turn,
    approval_id,
    run_root,
    config,
    launch,
    launch_path,
    worktree,
):
    execution_root = run_root / "executor" / turn
    if execution_root.is_symlink() or not execution_root.is_dir():
        _stop("execution_already_started")
    if {path.name for path in execution_root.iterdir()} != {
        "invocation.json",
        "provider-raw.json",
    }:
        _stop("execution_already_started")
    invocation = _read_canonical_json(
        execution_root / "invocation.json",
        "saved_response_invalid",
    )
    raw_path = execution_root / "provider-raw.json"
    raw = _read_canonical_json(raw_path, "saved_response_invalid")
    session_id = invocation.get("session_id")
    expected_arguments = _arguments(
        config,
        launch,
        worktree,
        session_id,
        turn,
    )
    if (
        set(invocation)
        != {
            "schema_version",
            "turn",
            "session_id",
            "argv",
            "environment_keys",
            "launch_request_sha256",
        }
        or invocation.get("schema_version") != 1
        or invocation.get("turn") != turn
        or not isinstance(session_id, str)
        or not session_id
        or invocation.get("argv") != expected_arguments
        or invocation.get("launch_request_sha256")
        != sha256_hex(launch_path.read_bytes())
        or set(raw) != {"schema_version", "returncode", "stdout", "stderr"}
        or raw.get("schema_version") != 1
        or raw.get("returncode") != 0
        or not isinstance(raw.get("stdout"), str)
        or not isinstance(raw.get("stderr"), str)
    ):
        _stop("saved_response_invalid")
    consumed = (
        private_root
        / "approval-store/consumed"
        / f"{approval_id}.json"
    )
    token = _read_canonical_json(consumed, "external_send_approval_required")
    if (
        token.get("approval_id") != approval_id
        or token.get("run_id") != run_id
        or token.get("configuration_sha256")
        != sha256_hex((run_root / "configuration/start.json").read_bytes())
        or token.get("maximum_payload_processes") != 2
    ):
        _stop("external_send_approval_required")
    parsed = _parse_stream(
        raw["stdout"],
        session_id,
        config["claude_runtime"]["allowed_response_models"],
        worktree,
    )
    result = _record_parsed_turn(
        repository,
        private_root,
        run_id,
        turn,
        run_root,
        config,
        launch_path,
        session_id,
        raw_path,
        sha256_hex(raw_path.read_bytes()),
        parsed,
        revalidated_without_process=True,
    )
    if turn == "test":
        _move_approval(
            consumed,
            private_root / "approval-store/claimed" / consumed.name,
        )
    return result


def _execute_approved_turn(
    repository,
    private_root,
    run_id,
    turn,
    approval_id,
    manifest_path,
    manifest_sha256,
):
    repository = Path(repository).resolve()
    private_root = Path(private_root).resolve()
    if turn not in ("test", "implementation"):
        _stop("turn_invalid")
    run_root = private_root / run_id
    worktree = run_root / "worktree"
    config_path = run_root / "configuration" / "start.json"
    config = _read_canonical_json(
        config_path,
        "run_not_found",
    )
    manifest_path = Path(manifest_path)
    if (
        not manifest_path.is_absolute()
        or manifest_path.is_symlink()
        or _SHA256.fullmatch(manifest_sha256 or "") is None
    ):
        _stop("manifest_mismatch")
    _read_canonical_json(manifest_path, "manifest_mismatch")
    try:
        manifest_bytes = manifest_path.read_bytes()
        config_bytes = config_path.read_bytes()
    except OSError:
        _stop("manifest_mismatch")
    if (
        manifest_bytes != config_bytes
        or sha256_hex(manifest_bytes) != manifest_sha256
    ):
        _stop("manifest_mismatch")
    launch_path = run_root / "launch" / f"{turn}.json"
    launch = _read_canonical_json(launch_path, "launch_request_invalid")
    expected_state = (
        "ready_for_test_turn"
        if turn == "test"
        else "ready_for_implementation_turn"
    )
    try:
        current = route.status(repository, private_root, run_id)
    except route.RouteStop as error:
        _stop(error.code)
    if current.get("state") != expected_state:
        _stop("state_not_ready")
    prompt = config.get("turn_prompts", {}).get(turn)
    if (
        not isinstance(prompt, str)
        or launch.get("run_id") != run_id
        or launch.get("turn") != turn
        or launch.get("prompt") != prompt
        or launch.get("prompt_sha256") != sha256_hex(prompt.encode("utf-8"))
        or launch.get("turn_prompts_sha256")
        != config.get("turn_prompts_sha256")
    ):
        _stop("launch_request_invalid")
    execution_root = run_root / "executor" / turn
    if execution_root.exists() or execution_root.is_symlink():
        return _recover_saved_turn(
            repository,
            private_root,
            run_id,
            turn,
            approval_id,
            run_root,
            config,
            launch,
            launch_path,
            worktree,
        )

    token_path, approval_directories = _send_approval(
        private_root,
        run_id,
        approval_id,
        config_path,
        turn,
    )
    environment = _child_environment()
    _validate_preflight(config, worktree, environment)
    if turn == "test":
        token_path = _move_approval(
            token_path,
            approval_directories["claimed"] / token_path.name,
        )
    session_id = _session_id(run_root, turn)
    arguments = _arguments(config, launch, worktree, session_id, turn)
    invocation_path, _ = _store(
        run_root,
        f"executor/{turn}/invocation.json",
        {
            "schema_version": 1,
            "turn": turn,
            "session_id": session_id,
            "argv": arguments,
            "environment_keys": sorted(environment),
            "launch_request_sha256": sha256_hex(launch_path.read_bytes()),
        },
    )
    completed = _invoke(arguments, worktree, environment)
    provider_raw_path, provider_raw_sha256 = _store(
        run_root,
        f"executor/{turn}/provider-raw.json",
        {
            "schema_version": 1,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        },
    )
    if completed.returncode != 0:
        _stop("claude_process_failed")
    parsed = _parse_stream(
        completed.stdout,
        session_id,
        config["claude_runtime"]["allowed_response_models"],
        worktree,
    )
    return _record_parsed_turn(
        repository,
        private_root,
        run_id,
        turn,
        run_root,
        config,
        launch_path,
        session_id,
        provider_raw_path,
        provider_raw_sha256,
        parsed,
        revalidated_without_process=False,
    )


def _consume_claimed_approval(private_root, approval_id):
    claimed = private_root / "approval-store/claimed" / f"{approval_id}.json"
    if not claimed.is_file() or claimed.is_symlink():
        _stop("external_send_approval_required")
    _move_approval(
        claimed,
        private_root / "approval-store/consumed" / claimed.name,
    )


def execute_turn(
    repository,
    private_root,
    run_id,
    turn,
    approval_id,
    manifest_path,
    manifest_sha256,
):
    private_root = Path(private_root).resolve()
    try:
        result = _execute_approved_turn(
            repository,
            private_root,
            run_id,
            turn,
            approval_id,
            manifest_path,
            manifest_sha256,
        )
    except ExecutorStop:
        execution_root = private_root / run_id / "executor" / turn
        claimed = (
            private_root
            / "approval-store/claimed"
            / f"{approval_id}.json"
        )
        if execution_root.exists() and claimed.is_file() and not claimed.is_symlink():
            try:
                _consume_claimed_approval(private_root, approval_id)
            except ExecutorStop:
                pass
        raise
    if (
        turn == "implementation"
        and result["execution"]["revalidated_without_process"] is not True
    ):
        _consume_claimed_approval(private_root, approval_id)
    return result
