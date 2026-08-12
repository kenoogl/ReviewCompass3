"""Claude実装委譲の確認運転準備テスト。"""

import importlib
import json
from pathlib import Path
import stat
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "claude-confirmation-20260812-001"
APPROVAL_ID = "RC3-CD-SEND-APPROVAL-20260812-001"


def _module():
    return importlib.import_module(
        "tools.development.claude_implementation_confirmation"
    )


def _prepare(tmp_path):
    executable = tmp_path / "claude"
    executable.write_bytes(b"pinned synthetic Claude executable\n")
    executable.chmod(0o755)
    output_root = tmp_path / "confirmation"
    result = _module().prepare_confirmation(
        workspace_root=PROJECT_ROOT,
        output_root=output_root,
        run_id=RUN_ID,
        approval_id=APPROVAL_ID,
        expires_at="2999-01-01T00:00:00Z",
        claude_executable=executable,
        python_executable=Path(sys.executable),
    )
    return output_root, result


def test_prepare_confirmation_creates_fixed_inputs_without_activating_send(
    tmp_path,
):
    output_root, result = _prepare(tmp_path)
    repository = output_root / "repository"
    private_root = output_root / "private"
    candidate = output_root / "candidates/send-approval.json"
    config_path = output_root / "start.json"

    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    config = json.loads(config_path.read_text(encoding="utf-8"))
    candidate_value = json.loads(candidate.read_text(encoding="utf-8"))
    token = candidate_value["proposed_token"]

    assert tracked == [
        "README.md",
        "instructions/implementation.md",
        "materials/requirements.md",
    ]
    assert status == ""
    assert result["state"] == "prepared_not_approved"
    assert result["claude_process_count"] == 0
    assert result["external_send_count"] == 0
    assert config["run_id"] == RUN_ID
    assert config["purpose"] == "claude_implementation_executor_confirmation"
    assert config["claude_runtime"]["requested_model"] == "claude-fable-5"
    assert config["claude_runtime"]["allowed_response_models"] == [
        "claude-fable-5",
        "claude-opus-5",
        "claude-opus-4-8",
    ]
    assert candidate_value["candidate_status"] == "awaiting_human_approval"
    assert token["approval_id"] == APPROVAL_ID
    assert "approved_by" not in token
    assert token["run_id"] == RUN_ID
    assert token["configuration_sha256"] == result["configuration_sha256"]
    assert token["private_root_sha256"] == result["private_root_sha256"]
    assert not (private_root / "approval-store").exists()
    launch = private_root / RUN_ID / "launch/test.json"
    assert launch.is_file()
    assert json.loads(launch.read_text(encoding="utf-8"))["prompt"] == (
        config["turn_prompts"]["test"]
    )


def test_prepare_confirmation_refuses_existing_or_workspace_internal_output(
    tmp_path,
):
    module = _module()
    executable = tmp_path / "claude"
    executable.write_bytes(b"pinned synthetic Claude executable\n")
    executable.chmod(0o755)
    existing = tmp_path / "existing"
    existing.mkdir()

    for output_root in (existing, PROJECT_ROOT / "private-confirmation"):
        try:
            module.prepare_confirmation(
                workspace_root=PROJECT_ROOT,
                output_root=output_root,
                run_id=RUN_ID,
                approval_id=APPROVAL_ID,
                expires_at="2999-01-01T00:00:00Z",
                claude_executable=executable,
                python_executable=Path(sys.executable),
            )
        except module.ConfirmationPreparationStop as error:
            assert error.code == "confirmation_output_invalid"
        else:
            raise AssertionError("unsafe output root must be rejected")


def test_confirmation_has_one_json_command_entry(tmp_path, capsys):
    module = _module()
    executable = tmp_path / "claude"
    executable.write_bytes(b"pinned synthetic Claude executable\n")
    executable.chmod(0o755)
    output_root = tmp_path / "confirmation-cli"

    exit_code = module.run(
        [
            "prepare",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--output-root",
            str(output_root),
            "--run-id",
            RUN_ID,
            "--approval-id",
            APPROVAL_ID,
            "--expires-at",
            "2999-01-01T00:00:00Z",
            "--claude-executable",
            str(executable),
            "--python-executable",
            str(Path(sys.executable).resolve()),
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert output.count("\n") == 1
    assert json.loads(output)["state"] == "prepared_not_approved"
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert (
        'reviewcompass3-claude-confirmation = '
        '"tools.development.claude_implementation_confirmation:main"'
    ) in pyproject


def test_activate_confirmation_creates_one_token_and_work_directories(
    tmp_path,
    capsys,
):
    output_root, prepared = _prepare(tmp_path)
    module = _module()

    exit_code = module.run(
        [
            "activate",
            "--output-root",
            str(output_root),
            "--candidate-sha256",
            prepared["approval_candidate_sha256"],
        ]
    )
    result = json.loads(capsys.readouterr().out)

    token = (
        output_root
        / "private/approval-store/pending"
        / f"{APPROVAL_ID}.json"
    )
    value = json.loads(token.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert result["state"] == "approval_activated"
    assert value["approved_by"] == "user"
    assert value["configuration_sha256"] == prepared["configuration_sha256"]
    assert stat.S_IMODE(token.stat().st_mode) == 0o600
    for state in ("pending", "claimed", "consumed"):
        directory = output_root / "private/approval-store" / state
        assert stat.S_IMODE(directory.stat().st_mode) == 0o700
    worktree = output_root / "private" / RUN_ID / "worktree"
    assert (worktree / "tests").is_dir()
    assert (worktree / "src").is_dir()

    try:
        module.activate_approval(
            output_root=output_root,
            expected_candidate_sha256=prepared["approval_candidate_sha256"],
        )
    except module.ConfirmationPreparationStop as error:
        assert error.code == "approval_activation_invalid"
    else:
        raise AssertionError("approval must be activated only once")


def test_run_approved_confirmation_derives_and_runs_both_turns_once(
    tmp_path,
    monkeypatch,
):
    output_root, prepared = _prepare(tmp_path)
    module = _module()
    trusted = tmp_path / "trusted-review-send"
    trusted.write_text("trusted fixture\n", encoding="utf-8")
    trusted.chmod(0o755)
    monkeypatch.setattr(module, "TRUSTED_EXECUTABLE", trusted)
    calls = []

    def fake_trusted(arguments, cwd):
        calls.append((list(arguments), Path(cwd)))
        if arguments == [str(trusted), "--capabilities"]:
            return {
                "schema_version": "trusted-review-send-v1",
                "status": "capabilities",
                "roles": {
                    "claude_implementation_executor": {
                        "model": "from-approved-launch",
                        "purpose": "claude_implementation_executor",
                        "topology": "same_session_test_then_implementation",
                    }
                },
            }
        turn = arguments[arguments.index("--turn") + 1]
        token = (
            output_root
            / "private/approval-store"
            / ("pending" if turn == "test" else "claimed")
            / f"{APPROVAL_ID}.json"
        )
        target = token.parent.parent / (
            "claimed" if turn == "test" else "consumed"
        ) / token.name
        token.replace(target)
        return {
            "schema_version": 1,
            "run_id": RUN_ID,
            "state": (
                "ready_for_implementation_turn"
                if turn == "test"
                else "ready_for_review"
            ),
        }

    monkeypatch.setattr(module, "_run_trusted_command", fake_trusted)
    states = iter(("ready_for_test_turn", "ready_for_review"))
    monkeypatch.setattr(
        module.route,
        "status",
        lambda repository, private_root, run_id: {
            "schema_version": 1,
            "run_id": run_id,
            "state": next(states),
            "independent_review": "pending",
            "human_stage_completion_approval": "pending",
        },
    )

    result = module.run_approved_confirmation(
        output_root=output_root,
        expected_candidate_sha256=prepared["approval_candidate_sha256"],
    )

    assert result["state"] == "ready_for_independent_review"
    assert result["external_send_count"] == 2
    assert result["turns"] == ["test", "implementation"]
    assert [
        arguments[arguments.index("--turn") + 1]
        for arguments, _ in calls[1:]
    ] == ["test", "implementation"]
    for arguments, cwd in calls[1:]:
        assert cwd == PROJECT_ROOT
        assert arguments[0] == str(trusted)
        assert arguments[1] == "claude-implementation-execute"
        assert arguments[arguments.index("--repository") + 1] == str(
            output_root / "repository"
        )
        assert arguments[arguments.index("--private-root") + 1] == str(
            output_root / "private"
        )
        assert arguments[arguments.index("--run-id") + 1] == RUN_ID
        assert arguments[arguments.index("--approval-id") + 1] == APPROVAL_ID
        assert arguments[arguments.index("--manifest-path") + 1] == str(
            output_root / "start.json"
        )
        assert arguments[arguments.index("--manifest-sha256") + 1] == (
            prepared["configuration_sha256"]
        )
    assert (
        output_root / "private/approval-store/consumed" / f"{APPROVAL_ID}.json"
    ).is_file()
    assert (output_root / "machine-completion-receipt.json").is_file()


def test_run_approved_confirmation_stops_before_second_turn_on_first_failure(
    tmp_path,
    monkeypatch,
):
    output_root, prepared = _prepare(tmp_path)
    module = _module()
    trusted = tmp_path / "trusted-review-send"
    trusted.write_text("trusted fixture\n", encoding="utf-8")
    trusted.chmod(0o755)
    monkeypatch.setattr(module, "TRUSTED_EXECUTABLE", trusted)
    payload_turns = []

    def fake_trusted(arguments, cwd):
        del cwd
        if arguments == [str(trusted), "--capabilities"]:
            return {
                "schema_version": "trusted-review-send-v1",
                "status": "capabilities",
                "roles": {
                    "claude_implementation_executor": {
                        "model": "from-approved-launch",
                        "purpose": "claude_implementation_executor",
                        "topology": "same_session_test_then_implementation",
                    }
                },
            }
        payload_turns.append(arguments[arguments.index("--turn") + 1])
        raise module.ConfirmationPreparationStop("claude_process_failed")

    monkeypatch.setattr(module, "_run_trusted_command", fake_trusted)

    try:
        module.run_approved_confirmation(
            output_root=output_root,
            expected_candidate_sha256=prepared["approval_candidate_sha256"],
        )
    except module.ConfirmationPreparationStop as error:
        assert error.code == "claude_process_failed"
    else:
        raise AssertionError("failed first turn must stop the run")
    assert payload_turns == ["test"]


def test_run_approved_confirmation_resumes_activated_run_without_reactivation(
    tmp_path,
    monkeypatch,
):
    output_root, prepared = _prepare(tmp_path)
    module = _module()
    module.activate_approval(
        output_root=output_root,
        expected_candidate_sha256=prepared["approval_candidate_sha256"],
    )
    pending = (
        output_root
        / "private/approval-store/pending"
        / f"{APPROVAL_ID}.json"
    )
    consumed = pending.parent.parent / "consumed" / pending.name
    pending.replace(consumed)
    trusted = tmp_path / "trusted-review-send"
    trusted.write_text("trusted fixture\n", encoding="utf-8")
    trusted.chmod(0o755)
    monkeypatch.setattr(module, "TRUSTED_EXECUTABLE", trusted)
    turns = []

    def fake_trusted(arguments, cwd):
        del cwd
        if arguments == [str(trusted), "--capabilities"]:
            return {
                "schema_version": "trusted-review-send-v1",
                "status": "capabilities",
                "roles": {
                    "claude_implementation_executor": {
                        "model": "from-approved-launch",
                        "purpose": "claude_implementation_executor",
                        "topology": "same_session_test_then_implementation",
                    }
                },
            }
        turn = arguments[arguments.index("--turn") + 1]
        turns.append(turn)
        token_root = output_root / "private/approval-store"
        if turn == "test":
            (token_root / "consumed" / consumed.name).replace(
                token_root / "claimed" / consumed.name
            )
            state = "ready_for_implementation_turn"
        else:
            (token_root / "claimed" / consumed.name).replace(
                token_root / "consumed" / consumed.name
            )
            state = "ready_for_review"
        return {"schema_version": 1, "run_id": RUN_ID, "state": state}

    states = iter(("ready_for_test_turn", "ready_for_review"))
    monkeypatch.setattr(module, "_run_trusted_command", fake_trusted)
    monkeypatch.setattr(
        module.route,
        "status",
        lambda repository, private_root, run_id: {
            "schema_version": 1,
            "run_id": run_id,
            "state": next(states),
            "independent_review": "pending",
            "human_stage_completion_approval": "pending",
        },
    )
    monkeypatch.setattr(
        module,
        "activate_approval",
        lambda **values: (_ for _ in ()).throw(
            AssertionError("activated run must not be activated again")
        ),
    )

    result = module.run_approved_confirmation(
        output_root=output_root,
        expected_candidate_sha256=prepared["approval_candidate_sha256"],
    )

    assert result["state"] == "ready_for_independent_review"
    assert turns == ["test", "implementation"]


def test_run_approved_cli_requires_only_prepared_root_and_candidate_digest(
    tmp_path,
    monkeypatch,
    capsys,
):
    module = _module()
    output_root = tmp_path / "prepared"
    observed = []
    monkeypatch.setattr(
        module,
        "run_approved_confirmation",
        lambda **values: observed.append(values)
        or {
            "schema_version": 1,
            "state": "ready_for_independent_review",
        },
    )

    exit_code = module.run(
        [
            "run-approved",
            "--output-root",
            str(output_root),
            "--candidate-sha256",
            "a" * 64,
        ]
    )

    assert exit_code == 0
    assert observed == [
        {
            "output_root": str(output_root),
            "expected_candidate_sha256": "a" * 64,
        }
    ]
    assert json.loads(capsys.readouterr().out)["state"] == (
        "ready_for_independent_review"
    )
