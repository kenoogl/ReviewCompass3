"""Claude実装委譲経路の第1縦切り受入テスト。"""

import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import types

import pytest


SCOPE_SHA256 = "063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f"
REQUEST_SHA256 = "bfc2b7ca72ebc731dd72a304d9e645ab0335416b72c683bd39b1ed31e7819213"
REQUIREMENT_SET_SHA256 = (
    "ca2b28f5dc156fc45c1c20808fe16b1e89874bead52da34dc07688015a2a2d69"
)
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
TEST_PATH = "tests/test_feature.py"
PRODUCTION_PATH = "src/feature.py"
INSTRUCTION_PATH = "instructions/implementation.md"
MATERIAL_PATH = "materials/requirements.md"

TRACEABILITY = {
    "AC-CD-001": (
        "test_happy_path_records_red_then_green_and_becomes_ready_for_review",
        "test_prepare_rejects_invalid_start_boundary_without_artifacts",
    ),
    "AC-CD-002": (
        "test_prepare_rejects_invalid_start_boundary_without_artifacts",
    ),
    "AC-CD-003": (
        "test_prepare_emits_only_the_fixed_safe_claude_capabilities",
        "test_record_turn_rejects_main_worktree_change",
        "test_administrator_boundaries_stop_without_writes",
    ),
    "AC-CD-004": (
        "test_happy_path_records_red_then_green_and_becomes_ready_for_review",
        "test_implementation_turn_rejects_test_fingerprint_change",
    ),
    "AC-CD-005": (
        "test_prepare_emits_only_the_fixed_safe_claude_capabilities",
        "test_prepare_rejects_unfixed_or_shell_test_commands",
        "test_machine_test_result_not_claude_report_controls_red_and_green",
    ),
    "AC-CD-006": (
        "test_turn_artifacts_are_preserved_once",
        "test_status_rejects_missing_extra_or_tampered_artifacts",
    ),
    "AC-CD-007": (
        "test_review_and_human_completion_remain_separate_after_machine_commit",
    ),
    "NG-CD-001": (
        "test_prepare_rejects_confirmation_run_boundary_violations",
    ),
    "NG-CD-002": (
        "test_prepare_emits_only_the_fixed_safe_claude_capabilities",
        "test_prepare_rejects_unfixed_or_shell_test_commands",
    ),
    "NG-CD-003": (
        "test_prepare_emits_only_the_fixed_safe_claude_capabilities",
    ),
    "NG-CD-004": (
        "test_claude_forbidden_tool_use_is_rejected",
    ),
    "NG-CD-005": (
        "test_prepare_rejects_automatic_switch_or_retry_without_processes",
    ),
    "NG-CD-006": (
        "test_machine_test_result_not_claude_report_controls_red_and_green",
        "test_review_and_human_completion_remain_separate_after_machine_commit",
    ),
    "NG-CD-007": (
        "test_prepare_rejects_confirmation_run_boundary_violations",
    ),
    "ST-CD-001": (
        "test_prepare_rejects_invalid_start_boundary_without_artifacts",
    ),
    "ST-CD-002": (
        "test_prepare_rejects_untrusted_claude_runtime_without_artifacts",
    ),
    "ST-CD-003": (
        "test_test_turn_rejects_forbidden_changes",
        "test_administrator_boundaries_stop_without_writes",
        "test_claude_forbidden_tool_use_is_rejected",
    ),
    "ST-CD-004": (
        "test_machine_test_result_not_claude_report_controls_red_and_green",
        "test_implementation_turn_rejects_test_fingerprint_change",
    ),
    "ST-CD-005": (
        "test_test_turn_rejects_forbidden_changes",
        "test_status_rejects_missing_extra_or_tampered_artifacts",
    ),
    "ST-CD-006": (
        "test_review_and_human_completion_remain_separate_after_machine_commit",
    ),
    "OUT-CD-001": (
        "test_prepare_emits_only_the_fixed_safe_claude_capabilities",
        "test_prepare_rejects_invalid_start_boundary_without_artifacts",
    ),
    "OUT-CD-002": (
        "test_turn_artifacts_are_preserved_once",
    ),
    "OUT-CD-003": (
        "test_happy_path_records_red_then_green_and_becomes_ready_for_review",
        "test_machine_test_result_not_claude_report_controls_red_and_green",
    ),
    "OUT-CD-004": (
        "test_happy_path_records_red_then_green_and_becomes_ready_for_review",
        "test_turn_artifacts_are_preserved_once",
    ),
    "OUT-CD-005": (
        "test_review_and_human_completion_remain_separate_after_machine_commit",
    ),
}


def _canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(value).hexdigest()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(value) + b"\n")


def _git(repository, *arguments):
    return subprocess.run(
        ("git", *arguments),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _route():
    return importlib.import_module(
        "tools.development.claude_implementation_route"
    )


def _tree_snapshot(root):
    if not root.exists():
        return ()
    return tuple(
        sorted(
            (
                str(path.relative_to(root)),
                "symlink" if path.is_symlink() else "directory" if path.is_dir() else _sha256(path.read_bytes()),
            )
            for path in root.rglob("*")
        )
    )


def _create_case(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    files = {
        INSTRUCTION_PATH: b"Add a deterministic double function.\n",
        MATERIAL_PATH: b"double(4) must return 8.\n",
        "README.md": b"synthetic acceptance repository\n",
    }
    for relative_path, content in files.items():
        path = repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    _git(repository, "init", "--quiet")
    _git(repository, "add", *files)
    _git(
        repository,
        "-c",
        "user.name=Acceptance Test",
        "-c",
        "user.email=acceptance@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "fixed synthetic input",
    )
    source_commit = _git(repository, "rev-parse", "HEAD")
    executable = tmp_path / "trusted-claude-code"
    executable.write_bytes(b"synthetic pinned executable; never run\n")
    executable.chmod(0o755)
    private_root = tmp_path / "private"
    test_command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        TEST_PATH,
    ]
    capabilities = {
        "allowed_tools": list(ALLOWED_TOOLS),
        "permission_mode": "dontAsk",
        "mcp_servers": {},
        "safe_mode": True,
        "disabled_features": list(DISABLED_FEATURES),
        "command_tool": False,
    }
    turn_prompts = {
        "test": "Create only tests/test_feature.py. Do not run commands.",
        "implementation": "Create only src/feature.py. Do not run commands.",
    }
    turn_prompts_sha256 = _sha256(_canonical_bytes(turn_prompts))
    config = {
        "schema_version": 1,
        "run_id": "claude-route-001",
        "workflow_state": "ready_for_executor",
        "source_commit": source_commit,
        "fixed_input": {
            "scope_sha256": SCOPE_SHA256,
            "request_sha256": REQUEST_SHA256,
            "requirement_set_sha256": REQUIREMENT_SET_SHA256,
            "instruction": {
                "path": INSTRUCTION_PATH,
                "sha256": _sha256(files[INSTRUCTION_PATH]),
            },
            "materials": [
                {
                    "path": MATERIAL_PATH,
                    "sha256": _sha256(files[MATERIAL_PATH]),
                }
            ],
            "freshness": "current",
        },
        "requirement_ids": list(REQUIREMENT_IDS),
        "approval": {
            "approval_id": "RC3-CD-RED-APPROVAL-001",
            "decision": "approved",
            "purpose": "claude_implementation_route_red_test",
            "one_time": True,
            "used": False,
            "scope_sha256": SCOPE_SHA256,
            "request_sha256": REQUEST_SHA256,
            "requirement_set_sha256": REQUIREMENT_SET_SHA256,
            "test_command_sha256": _sha256(_canonical_bytes(test_command)),
            "turn_prompts_sha256": turn_prompts_sha256,
        },
        "turn_prompts": turn_prompts,
        "turn_prompts_sha256": turn_prompts_sha256,
        "capabilities": capabilities,
        "claude_runtime": {
            "version": "1.0.0-pinned",
            "expected_version": "1.0.0-pinned",
            "executable": str(executable),
            "executable_sha256": _sha256(executable.read_bytes()),
            "expected_executable_sha256": _sha256(executable.read_bytes()),
            "authentication": {
                "origin": "claude.ai",
                "kind": "firstParty",
                "api_key_derived": False,
            },
            "requested_model": "claude-fable-5",
            "allowed_response_models": ["claude-fable-5"],
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
            "test": [TEST_PATH],
            "implementation": [PRODUCTION_PATH],
        },
        "test_command": test_command,
        "test_command_sha256": _sha256(_canonical_bytes(test_command)),
        "proof": {
            "repository_kind": "synthetic_fixture",
            "project_identity": "claude-route-acceptance-fixture",
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
    config_path = tmp_path / "start.json"
    _write_json(config_path, config)
    return types.SimpleNamespace(
        repository=repository,
        source_commit=source_commit,
        executable=executable,
        private_root=private_root,
        config=config,
        config_path=config_path,
        run_id=config["run_id"],
    )


def _save_config(case):
    _write_json(case.config_path, case.config)


def _prepare(tmp_path):
    route = _route()
    case = _create_case(tmp_path)
    outcome = route.prepare(
        case.repository,
        case.config_path,
        case.private_root,
    )
    assert outcome["schema_version"] == 1
    assert outcome["run_id"] == case.run_id
    assert outcome["state"] == "ready_for_test_turn"
    case.outcome = outcome
    case.worktree = Path(outcome["worktree"])
    case.launch_request_path = Path(outcome["launch_request_path"])
    assert case.worktree.is_dir()
    assert case.repository not in case.worktree.parents
    assert case.launch_request_path.is_file()
    return route, case


def _write_test_change(case, *, passing=False):
    path = case.worktree / TEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if passing:
        path.write_text("def test_incorrect_red_fixture():\n    assert True\n", encoding="utf-8")
    else:
        path.write_text(
            "from src.feature import double\n\n\n"
            "def test_double():\n"
            "    assert double(4) == 8\n",
            encoding="utf-8",
        )


def _write_implementation_change(case, *, passing=True):
    path = case.worktree / PRODUCTION_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    result = "value * 2" if passing else "value"
    path.write_text(
        f"def double(value):\n    return {result}\n",
        encoding="utf-8",
    )


def _turn_inputs(case, turn, launch_request_path, tool_uses, *, reported_exit):
    raw_path = case.config_path.parent / "inputs" / f"{turn}-raw.json"
    raw = {
        "schema_version": 1,
        "run_id": case.run_id,
        "turn": turn,
        "status": "completed",
        "response_model": "claude-fable-5",
        "text": f"synthetic {turn} response",
        "tool_uses": tool_uses,
        "reported_test_exit_code": reported_exit,
    }
    _write_json(raw_path, raw)
    launch_path = case.config_path.parent / "inputs" / f"{turn}-launch.json"
    launch = {
        "schema_version": 1,
        "run_id": case.run_id,
        "turn": turn,
        "session_id": "synthetic-session-001",
        "status": "completed",
        "launch_request_sha256": _sha256(Path(launch_request_path).read_bytes()),
        "raw_sha256": _sha256(raw_path.read_bytes()),
        "process_kind": "synthetic_fixture",
        "external_process_count": 0,
        "model": "claude-fable-5",
        "authentication": {
            "origin": "claude.ai",
            "kind": "firstParty",
            "api_key_derived": False,
        },
    }
    _write_json(launch_path, launch)
    return launch_path, raw_path


def _record_test_turn(route, case, *, reported_exit=0):
    _write_test_change(case)
    launch_path, raw_path = _turn_inputs(
        case,
        "test",
        case.launch_request_path,
        [{"tool": "Write", "path": TEST_PATH}],
        reported_exit=reported_exit,
    )
    outcome = route.record_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "test",
        launch_path,
        raw_path,
    )
    case.test_outcome = outcome
    case.launch_request_path = Path(outcome["next_launch_request_path"])
    return outcome


def _record_implementation_turn(route, case, *, reported_exit=1):
    _write_implementation_change(case)
    launch_path, raw_path = _turn_inputs(
        case,
        "implementation",
        case.launch_request_path,
        [{"tool": "Write", "path": PRODUCTION_PATH}],
        reported_exit=reported_exit,
    )
    outcome = route.record_turn(
        case.repository,
        case.private_root,
        case.run_id,
        "implementation",
        launch_path,
        raw_path,
    )
    case.implementation_outcome = outcome
    return outcome


def _assert_stop(route, code, operation):
    with pytest.raises(route.RouteStop) as caught:
        operation()
    assert caught.value.code == code


def _assert_no_new_artifacts(before, root):
    assert _tree_snapshot(root) == before


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_happy_path_records_red_then_green_and_becomes_ready_for_review(tmp_path):
    route, case = _prepare(tmp_path)

    red = _record_test_turn(route, case, reported_exit=0)

    assert red["state"] == "ready_for_implementation_turn"
    assert red["test_result"]["command"] == case.config["test_command"]
    assert red["test_result"]["exit_code"] != 0
    assert red["test_result"]["executor"] == "reviewcompass_machine"
    assert red["changed_paths"] == [TEST_PATH]
    assert len(red["test_fingerprint_sha256"]) == 64

    green = _record_implementation_turn(route, case, reported_exit=1)

    assert green["state"] == "ready_for_review"
    assert green["test_result"]["command"] == case.config["test_command"]
    assert green["test_result"]["exit_code"] == 0
    assert green["test_result"]["executor"] == "reviewcompass_machine"
    assert green["changed_paths"] == [TEST_PATH, PRODUCTION_PATH]
    assert green["test_fingerprint_sha256"] == red["test_fingerprint_sha256"]
    assert green["base_commit"] == case.source_commit
    assert green["implementation_commit"] != case.source_commit
    status = route.status(case.repository, case.private_root, case.run_id)
    assert status["state"] == "ready_for_review"
    assert status["implementation_commit"] == green["implementation_commit"]


@pytest.mark.parametrize(
    ("mutate", "stop_code"),
    (
        (lambda config: config["approval"].update(decision="pending"), "approval_required"),
        (lambda config: config["fixed_input"].update(scope_sha256="0" * 64), "fixed_input_mismatch"),
        (lambda config: config.update(workflow_state="human_decision_required"), "state_not_ready"),
        (lambda config: config["fixed_input"].update(freshness="stale"), "stale_input"),
        (lambda config: config["approval"].update(used=True), "approval_already_used"),
    ),
)
def test_prepare_rejects_invalid_start_boundary_without_artifacts(
    tmp_path,
    mutate,
    stop_code,
):
    route = _route()
    case = _create_case(tmp_path)
    mutate(case.config)
    _save_config(case)
    before = _tree_snapshot(tmp_path)

    _assert_stop(
        route,
        stop_code,
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )

    _assert_no_new_artifacts(before, tmp_path)


def test_prepare_emits_only_the_fixed_safe_claude_capabilities(tmp_path):
    _, case = _prepare(tmp_path)

    launch = _read_json(case.launch_request_path)

    assert launch["allowed_tools"] == list(ALLOWED_TOOLS)
    assert "Bash" not in launch["allowed_tools"]
    assert launch["permission_mode"] == "dontAsk"
    assert launch["mcp_servers"] == {}
    assert launch["safe_mode"] is True
    assert launch["disabled_features"] == list(DISABLED_FEATURES)
    assert launch["command_tool"] is False
    assert launch["external_process_count"] == 0
    assert launch["prompt"] == case.config["turn_prompts"]["test"]
    assert launch["prompt_sha256"] == _sha256(
        launch["prompt"].encode("utf-8")
    )


def test_prepare_rejects_prompt_and_digest_changed_together(tmp_path):
    route = _route()
    case = _create_case(tmp_path)
    case.config["turn_prompts"]["test"] = "Run an unapproved instruction."
    case.config["turn_prompts_sha256"] = _sha256(
        _canonical_bytes(case.config["turn_prompts"])
    )
    _save_config(case)

    _assert_stop(
        route,
        "fixed_input_mismatch",
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )


@pytest.mark.parametrize(
    ("mutate", "stop_code"),
    (
        (lambda config: config["claude_runtime"].update(version="other"), "claude_version_mismatch"),
        (lambda config: config["claude_runtime"].update(executable_sha256="0" * 64), "claude_executable_mismatch"),
        (lambda config: config["claude_runtime"]["authentication"].update(origin="api"), "claude_authentication_invalid"),
        (lambda config: config["claude_runtime"]["authentication"].update(api_key_derived=True), "claude_authentication_invalid"),
        (lambda config: config["claude_runtime"].update(allowed_response_models=["other-model"]), "claude_model_mismatch"),
    ),
)
def test_prepare_rejects_untrusted_claude_runtime_without_artifacts(
    tmp_path,
    mutate,
    stop_code,
):
    route = _route()
    case = _create_case(tmp_path)
    mutate(case.config)
    _save_config(case)
    before = _tree_snapshot(tmp_path)

    _assert_stop(
        route,
        stop_code,
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )

    _assert_no_new_artifacts(before, tmp_path)


@pytest.mark.parametrize(
    "routing_change",
    (
        {"automatic_fallback": True},
        {"fallback_models": ["other-model"]},
        {"fallback_authentications": ["api-key"]},
        {"fallback_routes": ["other-provider"]},
        {"fallback_destinations": ["other.example.invalid"]},
        {"automatic_retry": True, "maximum_external_attempts": 2},
    ),
)
def test_prepare_rejects_automatic_switch_or_retry_without_processes(
    tmp_path,
    routing_change,
):
    route = _route()
    case = _create_case(tmp_path)
    case.config["routing"].update(routing_change)
    _save_config(case)
    before = _tree_snapshot(tmp_path)

    _assert_stop(
        route,
        "automatic_routing_forbidden",
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )

    _assert_no_new_artifacts(before, tmp_path)


@pytest.mark.parametrize("violation", ("production", "extra", "symlink"))
def test_test_turn_rejects_forbidden_changes(tmp_path, violation):
    route, case = _prepare(tmp_path)
    _write_test_change(case)
    if violation == "production":
        _write_implementation_change(case)
    elif violation == "extra":
        (case.worktree / "extra.txt").write_text("extra\n", encoding="utf-8")
    else:
        (case.worktree / TEST_PATH).unlink()
        (case.worktree / TEST_PATH).symlink_to(case.worktree / "README.md")
    launch_path, raw_path = _turn_inputs(
        case,
        "test",
        case.launch_request_path,
        [{"tool": "Write", "path": TEST_PATH}],
        reported_exit=1,
    )

    _assert_stop(
        route,
        "change_scope_violation",
        lambda: route.record_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            launch_path,
            raw_path,
        ),
    )


def test_implementation_turn_rejects_test_fingerprint_change(tmp_path):
    route, case = _prepare(tmp_path)
    _record_test_turn(route, case)
    _write_implementation_change(case)
    (case.worktree / TEST_PATH).write_text(
        "from src.feature import double\n\n\ndef test_double():\n    assert double(5) == 10\n",
        encoding="utf-8",
    )
    launch_path, raw_path = _turn_inputs(
        case,
        "implementation",
        case.launch_request_path,
        [{"tool": "Write", "path": PRODUCTION_PATH}],
        reported_exit=0,
    )

    _assert_stop(
        route,
        "test_fingerprint_mismatch",
        lambda: route.record_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "implementation",
            launch_path,
            raw_path,
        ),
    )


def test_record_turn_rejects_main_worktree_change(tmp_path):
    route, case = _prepare(tmp_path)
    _write_test_change(case)
    (case.repository / "README.md").write_text("changed main worktree\n", encoding="utf-8")
    launch_path, raw_path = _turn_inputs(
        case,
        "test",
        case.launch_request_path,
        [{"tool": "Write", "path": TEST_PATH}],
        reported_exit=1,
    )

    _assert_stop(
        route,
        "main_worktree_changed",
        lambda: route.record_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            launch_path,
            raw_path,
        ),
    )


@pytest.mark.parametrize("boundary", ("configuration", "tool_use"))
def test_administrator_boundaries_stop_without_writes(tmp_path, boundary):
    route = _route()
    case = _create_case(tmp_path)
    administrator_target = tmp_path / "administrator-install" / "forbidden.py"
    if boundary == "configuration":
        case.config["proof"]["administrator_paths"] = [str(administrator_target)]
        _save_config(case)
        before = _tree_snapshot(tmp_path)
        _assert_stop(
            route,
            "administrator_boundary_violation",
            lambda: route.prepare(case.repository, case.config_path, case.private_root),
        )
        _assert_no_new_artifacts(before, tmp_path)
    else:
        outcome = route.prepare(case.repository, case.config_path, case.private_root)
        case.worktree = Path(outcome["worktree"])
        case.launch_request_path = Path(outcome["launch_request_path"])
        private_before = _tree_snapshot(case.private_root)
        _write_test_change(case)
        launch_path, raw_path = _turn_inputs(
            case,
            "test",
            case.launch_request_path,
            [{"tool": "Write", "path": str(administrator_target)}],
            reported_exit=1,
        )
        _assert_stop(
            route,
            "administrator_boundary_violation",
            lambda: route.record_turn(
                case.repository,
                case.private_root,
                case.run_id,
                "test",
                launch_path,
                raw_path,
            ),
        )
        assert _tree_snapshot(case.private_root) == private_before
    assert not administrator_target.exists()
    assert (case.repository / "README.md").read_bytes() == b"synthetic acceptance repository\n"


@pytest.mark.parametrize(
    "command_kind",
    ("shell_string", "different_array", "different_bound_array"),
)
def test_prepare_rejects_unfixed_or_shell_test_commands(tmp_path, command_kind):
    route = _route()
    case = _create_case(tmp_path)
    if command_kind == "shell_string":
        case.config["test_command"] = "python -m pytest -q tests/test_feature.py"
    elif command_kind == "different_array":
        case.config["test_command"] = [sys.executable, "-m", "pytest", "-q"]
    else:
        different_command = [sys.executable, "-m", "pytest", "-q", "tests/other.py"]
        case.config["test_command"] = different_command
        case.config["test_command_sha256"] = _sha256(
            _canonical_bytes(different_command)
        )
    _save_config(case)
    before = _tree_snapshot(tmp_path)

    _assert_stop(
        route,
        "test_command_invalid",
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )

    _assert_no_new_artifacts(before, tmp_path)


@pytest.mark.parametrize("boundary", ("red", "green"))
def test_machine_test_result_not_claude_report_controls_red_and_green(
    tmp_path,
    boundary,
):
    route, case = _prepare(tmp_path)
    if boundary == "red":
        _write_test_change(case, passing=True)
        launch_path, raw_path = _turn_inputs(
            case,
            "test",
            case.launch_request_path,
            [{"tool": "Write", "path": TEST_PATH}],
            reported_exit=1,
        )
        _assert_stop(
            route,
            "red_expected",
            lambda: route.record_turn(
                case.repository,
                case.private_root,
                case.run_id,
                "test",
                launch_path,
                raw_path,
            ),
        )
    else:
        _record_test_turn(route, case, reported_exit=0)
        _write_implementation_change(case, passing=False)
        launch_path, raw_path = _turn_inputs(
            case,
            "implementation",
            case.launch_request_path,
            [{"tool": "Write", "path": PRODUCTION_PATH}],
            reported_exit=0,
        )
        _assert_stop(
            route,
            "green_expected",
            lambda: route.record_turn(
                case.repository,
                case.private_root,
                case.run_id,
                "implementation",
                launch_path,
                raw_path,
            ),
        )


def test_turn_artifacts_are_preserved_once(tmp_path):
    route, case = _prepare(tmp_path)
    result = _record_test_turn(route, case)
    required = {"launch", "raw", "tool_use", "test_result", "change_inventory"}

    assert set(result["artifacts"]) == required
    preserved = {
        name: Path(path).read_bytes()
        for name, path in result["artifacts"].items()
    }
    launch_path = case.config_path.parent / "inputs" / "test-launch.json"
    raw_path = case.config_path.parent / "inputs" / "test-raw.json"
    _assert_stop(
        route,
        "turn_already_recorded",
        lambda: route.record_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            launch_path,
            raw_path,
        ),
    )
    assert {
        name: Path(path).read_bytes()
        for name, path in result["artifacts"].items()
    } == preserved


@pytest.mark.parametrize("damage", ("missing", "extra", "tampered"))
def test_status_rejects_missing_extra_or_tampered_artifacts(tmp_path, damage):
    route, case = _prepare(tmp_path)
    result = _record_test_turn(route, case)
    if damage == "missing":
        Path(result["artifacts"]["test_result"]).unlink()
        stop_code = "stored_artifact_missing"
    elif damage == "extra":
        extra = Path(result["artifacts"]["raw"]).parent / "unexpected.json"
        _write_json(extra, {"unexpected": True})
        stop_code = "stored_artifact_unexpected"
    else:
        Path(result["artifacts"]["raw"]).write_bytes(b"{}\n")
        stop_code = "stored_artifact_tampered"

    _assert_stop(
        route,
        stop_code,
        lambda: route.status(case.repository, case.private_root, case.run_id),
    )


@pytest.mark.parametrize(
    "tool_use",
    (
        {"tool": "Bash", "command": ["git", "status"]},
        {"tool": "Web", "url": "https://example.invalid/forbidden"},
    ),
    ids=("bash-git", "web"),
)
def test_claude_forbidden_tool_use_is_rejected(tmp_path, tool_use):
    route, case = _prepare(tmp_path)
    _write_test_change(case)
    launch_path, raw_path = _turn_inputs(
        case,
        "test",
        case.launch_request_path,
        [tool_use],
        reported_exit=1,
    )

    _assert_stop(
        route,
        "forbidden_tool_use",
        lambda: route.record_turn(
            case.repository,
            case.private_root,
            case.run_id,
            "test",
            launch_path,
            raw_path,
        ),
    )


def test_review_and_human_completion_remain_separate_after_machine_commit(tmp_path):
    route, case = _prepare(tmp_path)
    _record_test_turn(route, case)
    result = _record_implementation_turn(route, case)

    status = route.status(case.repository, case.private_root, case.run_id)

    assert result["implementation_commit"] != result["base_commit"]
    assert result["commit_executor"] == "reviewcompass_machine"
    assert status["state"] == "ready_for_review"
    assert status["independent_review"] == "pending"
    assert status["human_stage_completion_approval"] == "pending"
    assert status["completed"] is False


@pytest.mark.parametrize(
    ("mutate", "stop_code"),
    (
        (lambda config: config["proof"].update(project_identity="ReviewCompass3"), "proof_repository_forbidden"),
        (lambda config: config["proof"].update(contains_secrets=True), "sensitive_material_forbidden"),
        (lambda config: config["proof"].update(contains_user_information=True), "sensitive_material_forbidden"),
        (lambda config: config["approval"].update(purpose="claude_session_bootstrap"), "approval_purpose_mismatch"),
    ),
)
def test_prepare_rejects_confirmation_run_boundary_violations(
    tmp_path,
    mutate,
    stop_code,
):
    route = _route()
    case = _create_case(tmp_path)
    mutate(case.config)
    _save_config(case)
    before = _tree_snapshot(tmp_path)

    _assert_stop(
        route,
        stop_code,
        lambda: route.prepare(case.repository, case.config_path, case.private_root),
    )

    _assert_no_new_artifacts(before, tmp_path)


def test_requirement_traceability_covers_all_25_ids():
    assert len(REQUIREMENT_IDS) == 25
    assert _sha256(("\n".join(REQUIREMENT_IDS) + "\n").encode("utf-8")) == (
        REQUIREMENT_SET_SHA256
    )
    assert set(TRACEABILITY) == set(REQUIREMENT_IDS)
    assert all(TRACEABILITY[requirement_id] for requirement_id in REQUIREMENT_IDS)
    missing_tests = {
        test_name
        for test_names in TRACEABILITY.values()
        for test_name in test_names
        if test_name not in globals() or not callable(globals()[test_name])
    }
    assert missing_tests == set()
