"""Claudeへ実装を委譲する最小の機械境界。"""

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess

from tools.bootstrap.immutable_result_store import (
    ImmutableResultStoreError,
    canonical_json_bytes,
    store_immutable_json,
)
from tools.common.digests import sha256_hex


SCOPE_SHA256 = "063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f"
REQUEST_SHA256 = "bfc2b7ca72ebc731dd72a304d9e645ab0335416b72c683bd39b1ed31e7819213"
REQUIREMENT_SET_SHA256 = "ca2b28f5dc156fc45c1c20808fe16b1e89874bead52da34dc07688015a2a2d69"
CONFIRMATION_INSTRUCTION_SHA256 = (
    "83933a6ff8da30722a74df8fbef0a6f816059edfd2dfc8b084b3427c5d72f9ec"
)
PURPOSE = "claude_implementation_executor_confirmation"
REQUIREMENT_IDS = tuple(
    [f"AC-CD-{number:03d}" for number in range(1, 8)]
    + [f"NG-CD-{number:03d}" for number in range(1, 8)]
    + [f"ST-CD-{number:03d}" for number in range(1, 7)]
    + [f"OUT-CD-{number:03d}" for number in range(1, 6)]
)
ALLOWED_TOOLS = ("Read", "Glob", "Grep", "Edit", "Write")
DISABLED_FEATURES = (
    "agents",
    "background",
    "chrome",
    "fallback",
    "hooks",
    "plugins",
    "skills",
    "web",
)


class RouteStop(Exception):
    """安全境界により処理を停止した。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _stop(code):
    raise RouteStop(code)


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
        _stop("invalid_json")


def _run(arguments, cwd, *, check=True):
    try:
        return subprocess.run(
            tuple(arguments),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        _stop("machine_command_failed")


def _git(repository, *arguments, check=True):
    return _run(("git", *arguments), repository, check=check)


def _safe_relative_path(value):
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and all(part not in ("", ".", "..") for part in path.parts)
        and str(path) == value
    )


def _main_is_clean(repository):
    return not _git(repository, "status", "--porcelain=v1", "--untracked-files=all").stdout


def _head(repository):
    return _git(repository, "rev-parse", "HEAD").stdout.strip()


def _validate_start(repository, config):
    if config.get("workflow_state") != "ready_for_executor":
        _stop("state_not_ready")

    approval = config.get("approval", {})
    if approval.get("decision") != "approved":
        _stop("approval_required")
    if approval.get("used") is not False:
        _stop("approval_already_used")
    if (
        config.get("purpose") != PURPOSE
        or approval.get("purpose") != PURPOSE
        or approval.get("approved_by") != "user"
        or approval.get("one_time") is not True
    ):
        _stop("approval_purpose_mismatch")

    fixed = config.get("fixed_input", {})
    expected_digests = {
        "scope_sha256": SCOPE_SHA256,
        "request_sha256": REQUEST_SHA256,
        "requirement_set_sha256": REQUIREMENT_SET_SHA256,
        "confirmation_instruction_sha256": (
            CONFIRMATION_INSTRUCTION_SHA256
        ),
    }
    if any(fixed.get(name) != digest for name, digest in expected_digests.items()):
        _stop("fixed_input_mismatch")
    if any(approval.get(name) != digest for name, digest in expected_digests.items()):
        _stop("fixed_input_mismatch")
    if fixed.get("freshness") != "current":
        _stop("stale_input")
    if (
        config.get("requirement_ids") != list(REQUIREMENT_IDS)
        or sha256_hex(
            ("\n".join(config["requirement_ids"]) + "\n").encode("utf-8")
        )
        != REQUIREMENT_SET_SHA256
    ):
        _stop("fixed_input_mismatch")

    if config.get("source_commit") != _head(repository):
        _stop("fixed_input_mismatch")
    if not _main_is_clean(repository):
        _stop("main_worktree_changed")

    for item in (fixed.get("instruction"), *(fixed.get("materials") or [])):
        if not isinstance(item, dict) or not _safe_relative_path(item.get("path")):
            _stop("fixed_input_mismatch")
        path = repository / item["path"]
        if not path.is_file() or path.is_symlink():
            _stop("fixed_input_mismatch")
        if sha256_hex(path.read_bytes()) != item.get("sha256"):
            _stop("fixed_input_mismatch")

    capabilities = config.get("capabilities", {})
    if (
        capabilities.get("allowed_tools") != list(ALLOWED_TOOLS)
        or capabilities.get("permission_mode") != "dontAsk"
        or capabilities.get("mcp_servers") != {}
        or capabilities.get("safe_mode") is not True
        or capabilities.get("disabled_features") != list(DISABLED_FEATURES)
        or capabilities.get("command_tool") is not False
    ):
        _stop("capabilities_invalid")

    runtime = config.get("claude_runtime", {})
    if runtime.get("version") != runtime.get("expected_version"):
        _stop("claude_version_mismatch")
    executable = Path(runtime.get("executable", ""))
    try:
        executable_digest = sha256_hex(executable.read_bytes())
    except OSError:
        _stop("claude_executable_mismatch")
    if (
        runtime.get("executable_sha256") != runtime.get("expected_executable_sha256")
        or executable_digest != runtime.get("expected_executable_sha256")
    ):
        _stop("claude_executable_mismatch")
    authentication = runtime.get("authentication", {})
    if (
        authentication.get("origin") != "claude.ai"
        or authentication.get("kind") != "firstParty"
        or authentication.get("api_key_derived") is not False
    ):
        _stop("claude_authentication_invalid")
    if runtime.get("requested_model") not in runtime.get("allowed_response_models", []):
        _stop("claude_model_mismatch")

    routing = config.get("routing", {})
    if (
        routing.get("automatic_fallback") is not False
        or routing.get("fallback_models") != []
        or routing.get("fallback_authentications") != []
        or routing.get("fallback_routes") != []
        or routing.get("fallback_destinations") != []
        or routing.get("automatic_retry") is not False
        or routing.get("maximum_external_attempts") != 1
    ):
        _stop("automatic_routing_forbidden")

    command = config.get("test_command")
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(part, str) and part for part in command)
        or sha256_hex(canonical_json_bytes(command)) != config.get("test_command_sha256")
        or approval.get("test_command_sha256") != config.get("test_command_sha256")
    ):
        _stop("test_command_invalid")

    turn_prompts = config.get("turn_prompts")
    if (
        not isinstance(turn_prompts, dict)
        or set(turn_prompts) != {"test", "implementation"}
        or not all(
            isinstance(prompt, str) and prompt and "\x00" not in prompt
            for prompt in turn_prompts.values()
        )
        or sha256_hex(canonical_json_bytes(turn_prompts))
        != config.get("turn_prompts_sha256")
        or approval.get("turn_prompts_sha256")
        != config.get("turn_prompts_sha256")
    ):
        _stop("fixed_input_mismatch")

    proof = config.get("proof", {})
    if proof.get("repository_kind") != "synthetic_fixture" or proof.get("project_identity") == "ReviewCompass3":
        _stop("proof_repository_forbidden")
    if proof.get("contains_secrets") is not False or proof.get("contains_user_information") is not False:
        _stop("sensitive_material_forbidden")
    if proof.get("administrator_paths") != []:
        _stop("administrator_boundary_violation")

    paths = config.get("allowed_paths", {})
    if (
        not isinstance(paths.get("test"), list)
        or not isinstance(paths.get("implementation"), list)
        or not paths["test"]
        or not paths["implementation"]
        or not all(_safe_relative_path(path) for path in paths["test"] + paths["implementation"])
    ):
        _stop("change_scope_violation")


def _store(root, relative_path, document):
    try:
        stored = store_immutable_json(root, relative_path, document)
    except ImmutableResultStoreError:
        _stop("immutable_artifact_error")
    return str(Path(root) / stored.relative_path), stored.file_sha256


def _launch_document(config, turn):
    runtime = config["claude_runtime"]
    prompt = config["turn_prompts"][turn]
    return {
        "schema_version": 1,
        "run_id": config["run_id"],
        "turn": turn,
        "allowed_tools": list(ALLOWED_TOOLS),
        "permission_mode": "dontAsk",
        "mcp_servers": {},
        "safe_mode": True,
        "disabled_features": list(DISABLED_FEATURES),
        "command_tool": False,
        "external_process_count": 0,
        "requested_model": runtime["requested_model"],
        "allowed_response_models": runtime["allowed_response_models"],
        "authentication": runtime["authentication"],
        "fixed_input": config["fixed_input"],
        "prompt": prompt,
        "prompt_sha256": sha256_hex(prompt.encode("utf-8")),
        "turn_prompts_sha256": config["turn_prompts_sha256"],
    }


def prepare(repository, config_path, private_root):
    repository = Path(repository).resolve()
    private_root = Path(private_root).resolve()
    config = _read_json(config_path)
    _validate_start(repository, config)
    run_id = config.get("run_id")
    if not isinstance(run_id, str) or not run_id or not _safe_relative_path(run_id):
        _stop("fixed_input_mismatch")

    run_root = private_root / run_id
    worktree = run_root / "worktree"
    if run_root.exists():
        _stop("run_already_exists")
    _git(repository, "worktree", "add", "--quiet", "--detach", str(worktree), config["source_commit"])
    _, _ = _store(run_root, "configuration/start.json", config)
    launch_path, _ = _store(run_root, "launch/test.json", _launch_document(config, "test"))
    return {
        "schema_version": 1,
        "run_id": run_id,
        "state": "ready_for_test_turn",
        "worktree": str(worktree),
        "launch_request_path": launch_path,
    }


def _changed_paths(worktree):
    tracked = _git(worktree, "diff", "--name-only", "HEAD").stdout.splitlines()
    untracked = _git(worktree, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    return sorted(set(filter(None, tracked + untracked)))


def _discard_worktree_changes(worktree):
    _git(worktree, "restore", "--staged", "--worktree", ":/")
    _git(worktree, "clean", "-fd")


def _validate_tool_uses(raw, allowed_paths, worktree):
    tool_uses = raw.get("tool_uses")
    if not isinstance(tool_uses, list):
        _stop("forbidden_tool_use")
    for use in tool_uses:
        if not isinstance(use, dict) or use.get("tool") not in ALLOWED_TOOLS:
            _stop("forbidden_tool_use")
        path = use.get("path")
        if path is not None:
            if not _safe_relative_path(path):
                _discard_worktree_changes(worktree)
                _stop("administrator_boundary_violation")
            if path not in allowed_paths:
                _stop("change_scope_violation")


def _load_run(private_root, run_id):
    run_root = Path(private_root).resolve() / run_id
    config_path = run_root / "configuration" / "start.json"
    if not config_path.is_file():
        _stop("run_not_found")
    return run_root, _read_json(config_path)


def _validate_turn_inputs(config, turn, launch_path, raw_path, expected_launch_path):
    launch_file = Path(launch_path)
    raw_file = Path(raw_path)
    launch = _read_json(launch_file)
    raw = _read_json(raw_file)
    if launch.get("launch_request_sha256") != sha256_hex(expected_launch_path.read_bytes()):
        _stop("launch_request_mismatch")
    if launch.get("raw_sha256") != sha256_hex(raw_file.read_bytes()):
        _stop("raw_digest_mismatch")
    if (
        launch.get("schema_version") != 1
        or raw.get("schema_version") != 1
        or launch.get("run_id") != config["run_id"]
        or raw.get("run_id") != config["run_id"]
        or launch.get("turn") != turn
        or raw.get("turn") != turn
        or launch.get("status") != "completed"
        or raw.get("status") != "completed"
    ):
        _stop("turn_input_mismatch")
    process_kind = launch.get("process_kind")
    process_count = launch.get("external_process_count")
    if not (
        (process_kind == "synthetic_fixture" and process_count == 0)
        or (process_kind == "claude_code_first_party" and process_count == 1)
    ):
        _stop("turn_input_mismatch")
    runtime = config["claude_runtime"]
    if (
        launch.get("model") not in runtime["allowed_response_models"]
        or raw.get("response_model") not in runtime["allowed_response_models"]
        or launch.get("authentication") != runtime["authentication"]
    ):
        _stop("turn_input_mismatch")
    return launch, raw


def _artifact_receipt(run_root, turn):
    receipt_path = run_root / "receipts" / f"{turn}.json"
    if not receipt_path.is_file():
        return None
    return _read_json(receipt_path)


def _verify_artifacts(run_root, turn):
    receipt = _artifact_receipt(run_root, turn)
    if receipt is None:
        return None
    artifacts = receipt.get("artifacts", {})
    artifact_root = run_root / "artifacts" / turn
    expected_names = {Path(relative).name for relative in artifacts.values()}
    actual_names = {path.name for path in artifact_root.iterdir()} if artifact_root.is_dir() else set()
    missing = expected_names - actual_names
    if missing:
        _stop("stored_artifact_missing")
    if actual_names - expected_names:
        _stop("stored_artifact_unexpected")
    for name, relative in artifacts.items():
        path = run_root / relative
        if not path.is_file() or path.is_symlink():
            _stop("stored_artifact_missing")
        if sha256_hex(path.read_bytes()) != receipt["file_sha256"][name]:
            _stop("stored_artifact_tampered")
    return receipt


def _test_fingerprint(worktree, test_paths):
    digest = hashlib.sha256()
    for relative in sorted(test_paths):
        path = worktree / relative
        if not path.is_file() or path.is_symlink():
            _stop("change_scope_violation")
        digest.update(relative.encode("utf-8") + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def _commit(worktree, paths, message):
    _git(worktree, "add", "--", *paths)
    _git(
        worktree,
        "-c",
        "user.name=ReviewCompass Machine",
        "-c",
        "user.email=reviewcompass@example.invalid",
        "commit",
        "--quiet",
        "-m",
        message,
    )
    return _head(worktree)


def record_turn(repository, private_root, run_id, turn, launch_path, raw_path):
    repository = Path(repository).resolve()
    if turn not in ("test", "implementation"):
        _stop("turn_input_mismatch")
    run_root, config = _load_run(private_root, run_id)
    if _artifact_receipt(run_root, turn) is not None:
        _stop("turn_already_recorded")
    prior = _verify_artifacts(run_root, "test")
    if turn == "test" and prior is not None:
        _stop("turn_already_recorded")
    if turn == "implementation" and prior is None:
        _stop("state_not_ready")
    if not _main_is_clean(repository):
        _stop("main_worktree_changed")

    worktree = run_root / "worktree"
    expected_launch_path = run_root / "launch" / f"{turn}.json"
    launch, raw = _validate_turn_inputs(config, turn, launch_path, raw_path, expected_launch_path)
    allowed = config["allowed_paths"][turn]
    _validate_tool_uses(raw, allowed, worktree)
    changed = _changed_paths(worktree)
    fingerprint = _test_fingerprint(worktree, config["allowed_paths"]["test"])
    if turn == "implementation" and fingerprint != prior["test_fingerprint_sha256"]:
        _stop("test_fingerprint_mismatch")
    if changed != sorted(allowed) or any((worktree / path).is_symlink() for path in changed):
        _stop("change_scope_violation")

    command = config["test_command"]
    result = _run(command, worktree, check=False)
    test_result = {
        "command": command,
        "exit_code": result.returncode,
        "executor": "reviewcompass_machine",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    if turn == "test" and result.returncode == 0:
        _stop("red_expected")
    if turn == "implementation" and result.returncode != 0:
        _stop("green_expected")

    base_commit = config["source_commit"]
    implementation_commit = _commit(
        worktree,
        changed,
        "Record delegated RED test" if turn == "test" else "Implement delegated change",
    )
    cumulative_paths = changed if turn == "test" else prior["changed_paths"] + changed
    artifact_documents = {
        "launch": launch,
        "raw": raw,
        "tool_use": {"tool_uses": raw["tool_uses"]},
        "test_result": test_result,
        "change_inventory": {"changed_paths": cumulative_paths},
    }
    artifacts = {}
    file_sha256 = {}
    relative_artifacts = {}
    for name, document in artifact_documents.items():
        relative = f"artifacts/{turn}/{name}.json"
        path, digest = _store(run_root, relative, document)
        artifacts[name] = path
        relative_artifacts[name] = relative
        file_sha256[name] = digest

    receipt = {
        "schema_version": 1,
        "turn": turn,
        "artifacts": relative_artifacts,
        "file_sha256": file_sha256,
        "changed_paths": cumulative_paths,
        "test_fingerprint_sha256": fingerprint,
        "base_commit": base_commit,
        "implementation_commit": implementation_commit,
    }
    _store(run_root, f"receipts/{turn}.json", receipt)

    outcome = {
        "schema_version": 1,
        "run_id": run_id,
        "state": "ready_for_implementation_turn" if turn == "test" else "ready_for_review",
        "test_result": test_result,
        "changed_paths": cumulative_paths,
        "test_fingerprint_sha256": fingerprint,
        "base_commit": base_commit,
        "implementation_commit": implementation_commit,
        "commit_executor": "reviewcompass_machine",
        "artifacts": artifacts,
    }
    if turn == "test":
        next_path, _ = _store(run_root, "launch/implementation.json", _launch_document(config, "implementation"))
        outcome["next_launch_request_path"] = next_path
    return outcome


def status(repository, private_root, run_id):
    del repository
    run_root, config = _load_run(private_root, run_id)
    test_receipt = _verify_artifacts(run_root, "test")
    implementation_receipt = _verify_artifacts(run_root, "implementation")
    receipt = implementation_receipt or test_receipt
    if receipt is None:
        state = "ready_for_test_turn"
        implementation_commit = config["source_commit"]
    elif implementation_receipt is None:
        state = "ready_for_implementation_turn"
        implementation_commit = receipt["implementation_commit"]
    else:
        state = "ready_for_review"
        implementation_commit = receipt["implementation_commit"]
    review = config["review"]
    return {
        "schema_version": 1,
        "run_id": run_id,
        "state": state,
        "base_commit": config["source_commit"],
        "implementation_commit": implementation_commit,
        "independent_review": review["independent_review"],
        "human_stage_completion_approval": review["human_stage_completion_approval"],
        "completed": False,
    }
