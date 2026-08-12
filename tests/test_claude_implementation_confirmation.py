"""Claude実装委譲の確認運転準備テスト。"""

import importlib
import json
from pathlib import Path
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
