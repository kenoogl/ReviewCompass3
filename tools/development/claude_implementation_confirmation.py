"""Claude実装委譲の合成確認運転を外部送信なしで準備する。"""

import datetime
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

from tools.bootstrap.immutable_result_store import canonical_json_bytes
from tools.common.digests import sha256_hex
from tools.development import claude_implementation_route as route


CONFIRMATION_PATH = Path(
    "records/session-handoffs/"
    "2026-08-12-claude-implementation-route-confirmation-run-instruction-v1.md"
)
SCOPE_PATH = Path(
    "records/session-handoffs/"
    "2026-08-12-claude-implementation-route-scope-v3.md"
)
REQUEST_PATH = Path(
    "records/session-handoffs/"
    "2026-08-12-claude-implementation-route-red-test-request-v2.md"
)
PURPOSE = "claude_implementation_executor_confirmation"
CLAUDE_VERSION = "2.1.220"
REQUESTED_MODEL = "claude-fable-5"
ALLOWED_RESPONSE_MODELS = (
    "claude-fable-5",
    "claude-opus-5",
    "claude-opus-4-8",
)
TRUSTED_EXECUTABLE = Path("/usr/local/libexec/reviewcompass/trusted-review-send")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_SHA256 = re.compile(r"[0-9a-f]{64}")


class ConfirmationPreparationStop(Exception):
    """確認運転の安全な準備を完了できない。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _stop(code):
    raise ConfirmationPreparationStop(code)


def _run(arguments, cwd, *, check=True):
    try:
        return subprocess.run(
            list(arguments),
            cwd=str(cwd),
            check=check,
            capture_output=True,
            text=True,
            shell=False,
        )
    except (OSError, subprocess.CalledProcessError):
        _stop("confirmation_machine_command_failed")


def _write_new(path, data, mode):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    path.chmod(mode)


def _write_json(path, value):
    _write_new(path, canonical_json_bytes(value) + b"\n", 0o600)


def _read_json(path, code):
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


def _run_trusted_command(arguments, cwd):
    completed = _run(arguments, cwd, check=False)
    try:
        value = json.loads(completed.stdout)
    except (TypeError, json.JSONDecodeError):
        _stop("trusted_transport_unavailable")
    if (
        completed.returncode != 0
        or completed.stderr
        or not isinstance(value, dict)
    ):
        code = value.get("stop_code") if isinstance(value, dict) else None
        _stop(code if isinstance(code, str) and code else "trusted_transport_unavailable")
    return value


def _inside(path, parent):
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _fixed_workspace_file(workspace_root, relative_path, expected_digest):
    path = workspace_root / relative_path
    if path.is_symlink() or not path.is_file():
        _stop("confirmation_fixed_input_invalid")
    data = path.read_bytes()
    if sha256_hex(data) != expected_digest:
        _stop("confirmation_fixed_input_invalid")
    blob = _run(
        ("git", "show", f"HEAD:{relative_path.as_posix()}"),
        workspace_root,
    ).stdout.encode("utf-8")
    if blob != data:
        _stop("confirmation_fixed_input_invalid")
    return data


def _text_block(document, marker, *, trailing_newline=False):
    try:
        tail = document.split(marker, 1)[1]
        block = tail.split("```text\n", 1)[1].split("\n```", 1)[0]
    except IndexError:
        _stop("confirmation_instruction_invalid")
    if not block:
        _stop("confirmation_instruction_invalid")
    return block + "\n" if trailing_newline else block


def _validate_inputs(
    workspace_root,
    output_root,
    run_id,
    approval_id,
    expires_at,
    claude_executable,
    python_executable,
):
    workspace_root = Path(workspace_root).resolve()
    output_root = Path(output_root)
    if (
        not output_root.is_absolute()
        or output_root.exists()
        or output_root.is_symlink()
        or _inside(output_root.parent.resolve(), workspace_root)
        or _IDENTIFIER.fullmatch(run_id) is None
        or _IDENTIFIER.fullmatch(approval_id) is None
    ):
        _stop("confirmation_output_invalid")
    for executable in (claude_executable, python_executable):
        executable = Path(executable)
        if not executable.is_absolute() or not executable.is_file():
            _stop("confirmation_runtime_invalid")
    try:
        expires = datetime.datetime.fromisoformat(
            expires_at.replace("Z", "+00:00")
        )
    except (AttributeError, ValueError):
        _stop("confirmation_expiry_invalid")
    if expires <= datetime.datetime.now(datetime.timezone.utc):
        _stop("confirmation_expiry_invalid")
    return workspace_root, output_root


def _initialize_repository(repository, instruction):
    repository.mkdir(mode=0o700)
    files = {
        "README.md": _text_block(
            instruction,
            "### `README.md`",
            trailing_newline=True,
        ),
        "instructions/implementation.md": _text_block(
            instruction,
            "### `instructions/implementation.md`",
            trailing_newline=True,
        ),
        "materials/requirements.md": _text_block(
            instruction,
            "### `materials/requirements.md`",
            trailing_newline=True,
        ),
    }
    for relative, content in files.items():
        _write_new(repository / relative, content.encode("utf-8"), 0o600)
    _run(("git", "init", "--quiet"), repository)
    _run(("git", "add", "--", *sorted(files)), repository)
    _run(
        (
            "git",
            "-c",
            "user.name=ReviewCompass Machine",
            "-c",
            "user.email=reviewcompass@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "Create synthetic confirmation repository",
        ),
        repository,
    )
    source_commit = _run(("git", "rev-parse", "HEAD"), repository).stdout.strip()
    return files, source_commit


def _configuration(
    repository,
    files,
    source_commit,
    run_id,
    approval_id,
    claude_executable,
    python_executable,
    instruction,
):
    test_command = [
        str(Path(python_executable).resolve()),
        "-m",
        "pytest",
        "-q",
        "tests/test_feature.py",
    ]
    prompts = {
        "test": _text_block(instruction, "### 第1ターン：受入試験"),
        "implementation": _text_block(
            instruction,
            "### 第2ターン：製品実装",
        ),
    }
    test_command_sha256 = sha256_hex(canonical_json_bytes(test_command))
    prompts_sha256 = sha256_hex(canonical_json_bytes(prompts))
    fixed_digests = {
        "scope_sha256": route.SCOPE_SHA256,
        "request_sha256": route.REQUEST_SHA256,
        "requirement_set_sha256": route.REQUIREMENT_SET_SHA256,
        "confirmation_instruction_sha256": (
            route.CONFIRMATION_INSTRUCTION_SHA256
        ),
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "purpose": PURPOSE,
        "workflow_state": "ready_for_executor",
        "source_commit": source_commit,
        "fixed_input": {
            **fixed_digests,
            "instruction": {
                "path": "instructions/implementation.md",
                "sha256": sha256_hex(
                    files["instructions/implementation.md"].encode("utf-8")
                ),
            },
            "materials": [
                {
                    "path": "materials/requirements.md",
                    "sha256": sha256_hex(
                        files["materials/requirements.md"].encode("utf-8")
                    ),
                }
            ],
            "freshness": "current",
        },
        "requirement_ids": list(route.REQUIREMENT_IDS),
        "approval": {
            "approval_id": f"{approval_id}-PREPARATION",
            "approved_by": "user",
            "decision": "approved",
            "purpose": PURPOSE,
            "one_time": True,
            "used": False,
            **fixed_digests,
            "test_command_sha256": test_command_sha256,
            "turn_prompts_sha256": prompts_sha256,
        },
        "turn_prompts": prompts,
        "turn_prompts_sha256": prompts_sha256,
        "capabilities": {
            "allowed_tools": list(route.ALLOWED_TOOLS),
            "permission_mode": "dontAsk",
            "mcp_servers": {},
            "safe_mode": True,
            "disabled_features": list(route.DISABLED_FEATURES),
            "command_tool": False,
        },
        "claude_runtime": {
            "version": CLAUDE_VERSION,
            "expected_version": CLAUDE_VERSION,
            "executable": str(Path(claude_executable).resolve()),
            "executable_sha256": sha256_hex(
                Path(claude_executable).read_bytes()
            ),
            "expected_executable_sha256": sha256_hex(
                Path(claude_executable).read_bytes()
            ),
            "authentication": {
                "origin": "claude.ai",
                "kind": "firstParty",
                "api_key_derived": False,
            },
            "requested_model": REQUESTED_MODEL,
            "allowed_response_models": list(ALLOWED_RESPONSE_MODELS),
        },
        "routing": {
            "automatic_fallback": False,
            "fallback_models": [],
            "fallback_authentications": [],
            "fallback_routes": [],
            "fallback_destinations": [],
            "automatic_retry": False,
            "maximum_external_attempts": 1,
        },
        "allowed_paths": {
            "test": ["tests/test_feature.py"],
            "implementation": ["src/feature.py"],
        },
        "test_command": test_command,
        "test_command_sha256": test_command_sha256,
        "proof": {
            "repository_kind": "synthetic_fixture",
            "project_identity": "claude-delegation-confirmation-fixture",
            "contains_secrets": False,
            "contains_user_information": False,
            "administrator_paths": [],
        },
        "review": {
            "reviewer_model": "gpt-5.6-terra",
            "independent_review": "pending",
            "human_stage_completion_approval": "pending",
        },
    }


def prepare_confirmation(
    *,
    workspace_root,
    output_root,
    run_id,
    approval_id,
    expires_at,
    claude_executable,
    python_executable,
):
    workspace_root, output_root = _validate_inputs(
        workspace_root,
        output_root,
        run_id,
        approval_id,
        expires_at,
        claude_executable,
        python_executable,
    )
    instruction_bytes = _fixed_workspace_file(
        workspace_root,
        CONFIRMATION_PATH,
        route.CONFIRMATION_INSTRUCTION_SHA256,
    )
    _fixed_workspace_file(workspace_root, SCOPE_PATH, route.SCOPE_SHA256)
    _fixed_workspace_file(workspace_root, REQUEST_PATH, route.REQUEST_SHA256)
    try:
        instruction = instruction_bytes.decode("utf-8")
    except UnicodeError:
        _stop("confirmation_instruction_invalid")

    output_root.mkdir(mode=0o700)
    repository = output_root / "repository"
    private_root = output_root / "private"
    private_root.mkdir(mode=0o700)
    candidates = output_root / "candidates"
    candidates.mkdir(mode=0o700)
    files, source_commit = _initialize_repository(repository, instruction)
    config = _configuration(
        repository,
        files,
        source_commit,
        run_id,
        approval_id,
        claude_executable,
        python_executable,
        instruction,
    )
    config_path = output_root / "start.json"
    _write_json(config_path, config)
    try:
        prepared = route.prepare(repository, config_path, private_root)
    except route.RouteStop as error:
        _stop(error.code)

    configuration_sha256 = sha256_hex(config_path.read_bytes())
    private_root_sha256 = sha256_hex(
        str(private_root.resolve()).encode("utf-8")
    )
    candidate = {
        "schema_version": 1,
        "record_kind": "human_claude_implementation_send_approval_candidate",
        "candidate_status": "awaiting_human_approval",
        "proposed_token": {
            "schema_version": 1,
            "approval_id": approval_id,
            "purpose": PURPOSE,
            "run_id": run_id,
            "configuration_sha256": configuration_sha256,
            "private_root_sha256": private_root_sha256,
            "expires_at": expires_at,
            "maximum_payload_processes": 2,
        },
    }
    candidate_path = candidates / "send-approval.json"
    _write_json(candidate_path, candidate)
    receipt = {
        "schema_version": 1,
        "state": "prepared_not_approved",
        "run_id": run_id,
        "workspace_root": str(workspace_root),
        "repository": str(repository),
        "private_root": str(private_root),
        "source_commit": source_commit,
        "configuration_path": str(config_path),
        "configuration_sha256": configuration_sha256,
        "launch_request_path": prepared["launch_request_path"],
        "launch_request_sha256": sha256_hex(
            Path(prepared["launch_request_path"]).read_bytes()
        ),
        "approval_candidate_path": str(candidate_path),
        "approval_candidate_sha256": sha256_hex(candidate_path.read_bytes()),
        "private_root_sha256": private_root_sha256,
        "claude_process_count": 0,
        "external_send_count": 0,
        "approval_token_activated": False,
    }
    _write_json(output_root / "preparation-receipt.json", receipt)
    return receipt


def _validate_trusted_entry(workspace_root):
    trusted = Path(TRUSTED_EXECUTABLE)
    if (
        not trusted.is_absolute()
        or trusted.is_symlink()
        or not trusted.is_file()
        or not os.access(trusted, os.X_OK)
    ):
        _stop("trusted_transport_unavailable")
    capabilities = _run_trusted_command(
        [str(trusted), "--capabilities"],
        workspace_root,
    )
    role = capabilities.get("roles", {}).get(
        "claude_implementation_executor",
    )
    if (
        capabilities.get("schema_version") != "trusted-review-send-v1"
        or capabilities.get("status") != "capabilities"
        or role
        != {
            "model": "from-approved-launch",
            "purpose": "claude_implementation_executor",
            "topology": "same_session_test_then_implementation",
        }
    ):
        _stop("trusted_transport_unavailable")
    return trusted


def _trusted_turn_arguments(
    trusted,
    workspace_root,
    repository,
    private_root,
    run_id,
    turn,
    approval_id,
    manifest_path,
    manifest_sha256,
):
    return [
        str(trusted),
        "claude-implementation-execute",
        "--workspace-root",
        str(workspace_root),
        "--repository",
        str(repository),
        "--private-root",
        str(private_root),
        "--run-id",
        run_id,
        "--turn",
        turn,
        "--approval-id",
        approval_id,
        "--manifest-path",
        str(manifest_path),
        "--manifest-sha256",
        manifest_sha256,
    ]


def _validate_existing_activation(
    output_root,
    proposed,
    expected_candidate_sha256,
):
    candidate_path = output_root / "candidates/send-approval.json"
    store = output_root / "private/approval-store"
    if (
        sha256_hex(candidate_path.read_bytes()) != expected_candidate_sha256
        or store.is_symlink()
        or not store.is_dir()
        or stat.S_IMODE(store.stat().st_mode) != 0o700
    ):
        _stop("approval_activation_invalid")
    states = []
    for state in ("pending", "claimed", "consumed"):
        directory = store / state
        if (
            directory.is_symlink()
            or not directory.is_dir()
            or stat.S_IMODE(directory.stat().st_mode) != 0o700
        ):
            _stop("approval_activation_invalid")
        states.extend((state, path) for path in directory.iterdir())
    if len(states) != 1 or states[0][1].name != f"{proposed['approval_id']}.json":
        _stop("approval_activation_invalid")
    token_path = states[0][1]
    if (
        token_path.is_symlink()
        or not token_path.is_file()
        or stat.S_IMODE(token_path.stat().st_mode) != 0o600
    ):
        _stop("approval_activation_invalid")
    token = _read_json(token_path, "approval_activation_invalid")
    expected = dict(proposed)
    expected["approved_by"] = "user"
    if token != expected:
        _stop("approval_activation_invalid")
    return states[0][0]


def run_approved_confirmation(*, output_root, expected_candidate_sha256):
    output_root = Path(output_root)
    receipt = _read_json(
        output_root / "preparation-receipt.json",
        "approval_activation_invalid",
    )
    workspace_root = Path(receipt.get("workspace_root", ""))
    repository = Path(receipt.get("repository", ""))
    private_root = Path(receipt.get("private_root", ""))
    manifest_path = Path(receipt.get("configuration_path", ""))
    run_id = receipt.get("run_id")
    candidate = _read_json(
        output_root / "candidates/send-approval.json",
        "approval_activation_invalid",
    )
    proposed = candidate.get("proposed_token", {})
    approval_id = proposed.get("approval_id")
    manifest_sha256 = receipt.get("configuration_sha256")
    if (
        not output_root.is_absolute()
        or output_root.is_symlink()
        or not workspace_root.is_absolute()
        or workspace_root.is_symlink()
        or not workspace_root.is_dir()
        or not repository.is_absolute()
        or repository.is_symlink()
        or not repository.is_dir()
        or not private_root.is_absolute()
        or private_root.is_symlink()
        or not private_root.is_dir()
        or not manifest_path.is_absolute()
        or manifest_path.is_symlink()
        or not manifest_path.is_file()
        or _IDENTIFIER.fullmatch(run_id or "") is None
        or _IDENTIFIER.fullmatch(approval_id or "") is None
        or _SHA256.fullmatch(manifest_sha256 or "") is None
        or manifest_sha256 != sha256_hex(manifest_path.read_bytes())
    ):
        _stop("approval_activation_invalid")
    trusted = _validate_trusted_entry(workspace_root)
    store = private_root / "approval-store"
    if not store.exists() and not store.is_symlink():
        activate_approval(
            output_root=output_root,
            expected_candidate_sha256=expected_candidate_sha256,
        )
    else:
        _validate_existing_activation(
            output_root,
            proposed,
            expected_candidate_sha256,
        )

    try:
        initial_status = route.status(repository, private_root, run_id)
    except route.RouteStop as error:
        _stop(error.code)
    turns_by_state = {
        "ready_for_test_turn": ("test", "implementation"),
        "ready_for_implementation_turn": ("implementation",),
        "ready_for_review": (),
    }
    turns = turns_by_state.get(initial_status.get("state"))
    if turns is None:
        _stop("confirmation_result_invalid")

    states = {
        "test": "ready_for_implementation_turn",
        "implementation": "ready_for_review",
    }
    turn_results = []
    for turn in turns:
        result = _run_trusted_command(
            _trusted_turn_arguments(
                trusted,
                workspace_root,
                repository,
                private_root,
                run_id,
                turn,
                approval_id,
                manifest_path,
                manifest_sha256,
            ),
            workspace_root,
        )
        if (
            result.get("run_id") != run_id
            or result.get("state") != states[turn]
        ):
            _stop("trusted_transport_result_invalid")
        turn_results.append(turn)

    try:
        status = route.status(repository, private_root, run_id)
    except route.RouteStop as error:
        _stop(error.code)
    if (
        status.get("state") != "ready_for_review"
        or status.get("independent_review") != "pending"
        or status.get("human_stage_completion_approval") != "pending"
    ):
        _stop("confirmation_result_invalid")
    result = {
        "schema_version": 1,
        "state": "ready_for_independent_review",
        "run_id": run_id,
        "approval_id": approval_id,
        "configuration_sha256": manifest_sha256,
        "turns": turn_results,
        "claude_process_count": 2,
        "external_send_count": 2,
        "route_status": status,
    }
    _write_json(output_root / "machine-completion-receipt.json", result)
    return result


def activate_approval(*, output_root, expected_candidate_sha256):
    output_root = Path(output_root)
    if (
        not output_root.is_absolute()
        or output_root.is_symlink()
        or not output_root.is_dir()
        or _SHA256.fullmatch(expected_candidate_sha256) is None
    ):
        _stop("approval_activation_invalid")
    candidate_path = output_root / "candidates/send-approval.json"
    receipt_path = output_root / "preparation-receipt.json"
    config_path = output_root / "start.json"
    if (
        sha256_hex(candidate_path.read_bytes()) != expected_candidate_sha256
        or (output_root / "private/approval-store").exists()
        or (output_root / "private/approval-store").is_symlink()
    ):
        _stop("approval_activation_invalid")
    candidate = _read_json(candidate_path, "approval_activation_invalid")
    receipt = _read_json(receipt_path, "approval_activation_invalid")
    proposed = candidate.get("proposed_token")
    if (
        set(candidate)
        != {
            "schema_version",
            "record_kind",
            "candidate_status",
            "proposed_token",
        }
        or candidate.get("schema_version") != 1
        or candidate.get("record_kind")
        != "human_claude_implementation_send_approval_candidate"
        or candidate.get("candidate_status") != "awaiting_human_approval"
        or not isinstance(proposed, dict)
        or set(proposed)
        != {
            "schema_version",
            "approval_id",
            "purpose",
            "run_id",
            "configuration_sha256",
            "private_root_sha256",
            "expires_at",
            "maximum_payload_processes",
        }
        or proposed.get("schema_version") != 1
        or _IDENTIFIER.fullmatch(proposed.get("approval_id", "")) is None
        or proposed.get("purpose") != PURPOSE
        or proposed.get("run_id") != receipt.get("run_id")
        or proposed.get("configuration_sha256")
        != receipt.get("configuration_sha256")
        or proposed.get("configuration_sha256")
        != sha256_hex(config_path.read_bytes())
        or proposed.get("private_root_sha256")
        != receipt.get("private_root_sha256")
        or proposed.get("private_root_sha256")
        != sha256_hex(str((output_root / "private").resolve()).encode("utf-8"))
        or proposed.get("maximum_payload_processes") != 2
        or receipt.get("approval_token_activated") is not False
        or receipt.get("state") != "prepared_not_approved"
    ):
        _stop("approval_activation_invalid")
    try:
        expires = datetime.datetime.fromisoformat(
            proposed["expires_at"].replace("Z", "+00:00")
        )
    except (AttributeError, ValueError):
        _stop("approval_activation_invalid")
    if expires <= datetime.datetime.now(datetime.timezone.utc):
        _stop("confirmation_expiry_invalid")

    worktree = output_root / "private" / proposed["run_id"] / "worktree"
    if worktree.is_symlink() or not worktree.is_dir():
        _stop("approval_activation_invalid")
    for relative in ("tests", "src"):
        directory = worktree / relative
        if directory.exists() or directory.is_symlink():
            _stop("approval_activation_invalid")

    store = output_root / "private/approval-store"
    store.mkdir(mode=0o700)
    directories = {}
    for state in ("pending", "claimed", "consumed"):
        directory = store / state
        directory.mkdir(mode=0o700)
        directories[state] = directory
    token = dict(proposed)
    token["approved_by"] = "user"
    token_path = directories["pending"] / f"{proposed['approval_id']}.json"
    _write_json(token_path, token)
    for relative in ("tests", "src"):
        (worktree / relative).mkdir(mode=0o700)
    result = {
        "schema_version": 1,
        "state": "approval_activated",
        "run_id": proposed["run_id"],
        "approval_id": proposed["approval_id"],
        "approval_state": "pending",
        "token_path": str(token_path),
        "token_sha256": sha256_hex(token_path.read_bytes()),
        "claude_process_count": 0,
        "external_send_count": 0,
    }
    _write_json(output_root / "candidates/activation-receipt.json", result)
    return result


def run(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    prepare_flags = (
        "--workspace-root",
        "--output-root",
        "--run-id",
        "--approval-id",
        "--expires-at",
        "--claude-executable",
        "--python-executable",
    )
    prepare_valid = (
        len(arguments) == 15
        and arguments[0] == "prepare"
        and all(
            arguments[1 + index * 2] == flag
            for index, flag in enumerate(prepare_flags)
        )
        and all(Path(arguments[index]).is_absolute() for index in (2, 4, 12, 14))
    )
    activate_valid = (
        len(arguments) == 5
        and arguments[0] == "activate"
        and arguments[1] == "--output-root"
        and Path(arguments[2]).is_absolute()
        and arguments[3] == "--candidate-sha256"
        and _SHA256.fullmatch(arguments[4]) is not None
    )
    run_approved_valid = (
        len(arguments) == 5
        and arguments[0] == "run-approved"
        and arguments[1] == "--output-root"
        and Path(arguments[2]).is_absolute()
        and arguments[3] == "--candidate-sha256"
        and _SHA256.fullmatch(arguments[4]) is not None
    )
    if not prepare_valid and not activate_valid and not run_approved_valid:
        result = {
            "schema_version": 1,
            "state": "stopped",
            "stop_code": "confirmation_input_invalid",
        }
        exit_code = 2
    else:
        try:
            if prepare_valid:
                result = prepare_confirmation(
                    workspace_root=arguments[2],
                    output_root=arguments[4],
                    run_id=arguments[6],
                    approval_id=arguments[8],
                    expires_at=arguments[10],
                    claude_executable=arguments[12],
                    python_executable=arguments[14],
                )
            elif activate_valid:
                result = activate_approval(
                    output_root=arguments[2],
                    expected_candidate_sha256=arguments[4],
                )
            else:
                result = run_approved_confirmation(
                    output_root=arguments[2],
                    expected_candidate_sha256=arguments[4],
                )
            exit_code = 0
        except ConfirmationPreparationStop as error:
            result = {
                "schema_version": 1,
                "state": "stopped",
                "stop_code": error.code,
            }
            exit_code = 2
        except Exception:
            result = {
                "schema_version": 1,
                "state": "failed",
                "stop_code": "internal_error",
            }
            exit_code = 1
    sys.stdout.write(
        json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    )
    return exit_code


def main():
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
