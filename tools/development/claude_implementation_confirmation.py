"""Claude実装委譲の合成確認運転を外部送信なしで準備する。"""

import datetime
import json
import os
from pathlib import Path
import re
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
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class ConfirmationPreparationStop(Exception):
    """確認運転の安全な準備を完了できない。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _stop(code):
    raise ConfirmationPreparationStop(code)


def _run(arguments, cwd):
    try:
        return subprocess.run(
            list(arguments),
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
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


def run(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    flags = (
        "--workspace-root",
        "--output-root",
        "--run-id",
        "--approval-id",
        "--expires-at",
        "--claude-executable",
        "--python-executable",
    )
    valid = (
        len(arguments) == 15
        and arguments[0] == "prepare"
        and all(arguments[1 + index * 2] == flag for index, flag in enumerate(flags))
        and all(
            Path(arguments[index]).is_absolute()
            for index in (2, 4, 12, 14)
        )
    )
    if not valid:
        result = {
            "schema_version": 1,
            "state": "stopped",
            "stop_code": "confirmation_input_invalid",
        }
        exit_code = 2
    else:
        try:
            result = prepare_confirmation(
                workspace_root=arguments[2],
                output_root=arguments[4],
                run_id=arguments[6],
                approval_id=arguments[8],
                expires_at=arguments[10],
                claude_executable=arguments[12],
                python_executable=arguments[14],
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
