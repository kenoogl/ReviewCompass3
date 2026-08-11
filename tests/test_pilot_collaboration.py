"""Pilot collaboration 共通入口の受入テスト。"""

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_PATH = (
    "records/session-handoffs/"
    "2026-08-11-pilot-collaboration-entry-implementation-request-v6.md"
)
REQUIREMENT_IDS = tuple(
    [f"AC-PC-{number:03d}" for number in range(1, 10)]
    + [f"NG-PC-{number:03d}" for number in range(1, 8)]
    + [f"ST-PC-{number:03d}" for number in range(1, 5)]
    + [f"OUT-PC-{number:03d}" for number in range(1, 7)]
)
TRACEABILITY = {
    "AC-PC-001": "test_repository_exposes_one_common_pilot_entrypoint",
    "AC-PC-002": "test_prepare_rejects_tampered_source_and_requirement_set",
    "AC-PC-003": "test_prepare_is_deterministic_and_hashes_payload_not_saved_envelope",
    "AC-PC-004": "test_launch_failure_is_preserved_before_stopping",
    "AC-PC-005": "test_audit_requires_complete_requirement_coverage",
    "AC-PC-006": "test_judgment_requires_one_recommendation_per_finding",
    "AC-PC-007": "test_successful_audit_and_judgment_derive_state_from_event_chain",
    "AC-PC-008": "test_cli_normalizes_invalid_arguments_to_contract_json",
    "AC-PC-009": "test_existing_raw_review_store_uses_common_immutable_boundary",
    "NG-PC-001": "test_pilot_code_cannot_launch_claude_codex_or_shell_commands",
    "NG-PC-002": "test_ingest_rejects_stage_outside_prompt_quality_slice",
    "NG-PC-003": "test_failed_ingest_never_overwrites_preserved_raw_result",
    "NG-PC-004": "test_status_detects_stored_raw_digest_tampering",
    "NG-PC-005": "test_pilot_does_not_reinterpret_closed_review_pipeline",
    "NG-PC-006": "test_prepare_and_ingest_do_not_write_workflow_ledgers",
    "NG-PC-007": "test_entrypoint_change_is_limited_to_one_reference_per_file",
    "ST-PC-001": "test_change_scope_contains_only_v6_allowlisted_paths",
    "ST-PC-002": "test_existing_raw_review_store_public_contract_is_unchanged",
    "ST-PC-003": "test_prepare_rejects_unsafe_private_root_placements",
    "ST-PC-004": "test_fixed_result_documents_reject_extra_and_missing_keys",
    "OUT-PC-001": "process:red-test-command-receipts",
    "OUT-PC-002": "process:committed-test-baseline",
    "OUT-PC-003": "test_fault_injection_matrix_covers_required_failures",
    "OUT-PC-004": "process:post-implementation-command-receipts",
    "OUT-PC-005": "process:final-requirement-evidence-report",
    "OUT-PC-006": "process:local-commit-receipt",
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
    path.write_bytes(_canonical_bytes(value) + b"\n")


def _git(repository, *arguments):
    return subprocess.run(
        ("git", *arguments),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _create_repository(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    instruction = repository / INSTRUCTION_PATH
    instruction.parent.mkdir(parents=True)
    instruction.write_bytes((PROJECT_ROOT / INSTRUCTION_PATH).read_bytes())
    material = repository / "materials" / "input.txt"
    material.parent.mkdir()
    material.write_text("fixed material\n", encoding="utf-8")
    _git(repository, "init", "--quiet")
    _git(repository, "add", INSTRUCTION_PATH, "materials/input.txt")
    _git(
        repository,
        "-c",
        "user.name=Acceptance Test",
        "-c",
        "user.email=acceptance@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "fixed input",
    )
    source_commit = _git(repository, "rev-parse", "HEAD")
    return repository, source_commit


def _start_config(repository, source_commit, run_id="run-001"):
    instruction_bytes = (repository / INSTRUCTION_PATH).read_bytes()
    material_path = "materials/input.txt"
    material_bytes = (repository / material_path).read_bytes()
    selected_paths = material_path.encode("utf-8")
    return {
        "schema_version": 1,
        "run_id": run_id,
        "collaboration_method": "pilot_specific_claude_codex",
        "request_kind": "implementation",
        "pilot": "codex",
        "implementer": "codex_implementation_subagent",
        "pilot_model": "gpt-5.6-sol",
        "reviewer_model": "gpt-5.6-terra",
        "instruction_quality_model": "gpt-5.6-terra",
        "source_commit": source_commit,
        "instruction": {
            "path": INSTRUCTION_PATH,
            "sha256": _sha256(instruction_bytes),
        },
        "materials": [{"path": material_path, "sha256": _sha256(material_bytes)}],
        "fixed_input": {
            "origin": "machine_derived",
            "count": 1,
            "derivation_argv": ["fixture", "materials/input.txt"],
            "derivation_output_sha256": _sha256(selected_paths),
            "selector": None,
            "selection_basis": None,
            "selected_paths_sha256": _sha256(selected_paths),
        },
        "requirement_ids": list(REQUIREMENT_IDS),
        "result_contract_version": "pilot-collaboration-prompt-quality-v1",
        "instruction_quality_round": 1,
        "instruction_quality_round_limit": 2,
        "implementation_review_round_limit": 2,
        "mechanical_assurance_status": {
            "instruction_preflight": "specified_only",
            "stage_ledger": "specified_only",
            "change_inventory": "specified_only",
            "raw_result_store": "specified_only",
            "result_parser": "specified_only",
            "reuse_guard": "specified_only",
            "capability_preflight": "specified_only",
        },
    }


def _environment():
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not existing
        else os.pathsep.join((str(PROJECT_ROOT), existing))
    )
    return environment


def _run_cli(repository, *arguments):
    return subprocess.run(
        (
            sys.executable,
            "-m",
            "tools.development.pilot_collaboration_cli",
            *arguments,
        ),
        cwd=repository,
        env=_environment(),
        check=False,
        capture_output=True,
        text=True,
    )


def _result(completed):
    assert completed.stderr == ""
    assert completed.stdout.endswith("\n")
    assert completed.stdout.count("\n") == 1
    return json.loads(completed.stdout)


def _prepare(tmp_path, run_id="run-001"):
    repository, source_commit = _create_repository(tmp_path)
    private_root = tmp_path / "private"
    private_root.mkdir()
    config_path = tmp_path / "start.json"
    _write_json(config_path, _start_config(repository, source_commit, run_id))
    completed = _run_cli(
        repository,
        "prepare",
        "--config",
        str(config_path),
        "--private-root",
        str(private_root),
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert _result(completed)["state"] == "ready_for_prompt_audit"
    return repository, private_root, config_path


def _payload_digest(envelope_path):
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    expected_digest = envelope.pop("envelope_sha256")
    calculated = _sha256(_canonical_bytes(envelope))
    assert expected_digest == calculated
    return calculated


def _raw_path(tmp_path, name, document):
    path = tmp_path / name
    _write_json(path, document)
    return path


def _launch_path(
    tmp_path,
    *,
    run_id,
    stage,
    attempt_id,
    input_digest,
    raw_file,
    status="succeeded",
    exit_code=0,
):
    raw_digest = _sha256(raw_file.read_bytes())
    launch = {
        "schema_version": 1,
        "execution_id": f"execution-{attempt_id}",
        "run_id": run_id,
        "stage": stage,
        "attempt_id": attempt_id,
        "provider": "fixture",
        "model": "gpt-5.6-terra",
        "status": status,
        "input_payload_sha256": input_digest,
        "commands": [{"argv": ["fixture", stage], "exit_code": exit_code}],
        "material_observation": {
            "material_mode": "discovery",
            "extractable_count": 1,
            "unextractable_count": 0,
            "unique_count": 1,
            "raw_sha256": raw_digest,
        },
    }
    path = tmp_path / f"{attempt_id}-launch.json"
    _write_json(path, launch)
    return path


def _ingest(
    repository,
    private_root,
    run_id,
    stage,
    attempt_id,
    raw_file,
    launch_file,
):
    return _run_cli(
        repository,
        "ingest",
        "--private-root",
        str(private_root),
        "--run-id",
        run_id,
        "--stage",
        stage,
        "--attempt-id",
        attempt_id,
        "--raw-file",
        str(raw_file),
        "--launch-record",
        str(launch_file),
    )


def _complete_audit(tmp_path, repository, private_root, findings=None):
    findings = [] if findings is None else findings
    raw_file = _raw_path(
        tmp_path,
        "audit-raw.json",
        {
            "schema_version": 1,
            "result_kind": "prompt_audit",
            "status": "completed",
            "findings": findings,
            "requirement_results": [
                {
                    "requirement_id": requirement_id,
                    "status": "checked",
                    "evidence": f"checked {requirement_id}",
                }
                for requirement_id in reversed(REQUIREMENT_IDS)
            ],
        },
    )
    digest = _payload_digest(
        private_root / "run-001" / "prompt-audit-envelope.json"
    )
    launch_file = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-001",
        input_digest=digest,
        raw_file=raw_file,
    )
    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-001",
        raw_file,
        launch_file,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    return _result(completed)


def test_requirement_traceability_covers_all_26_ids():
    assert tuple(TRACEABILITY) == REQUIREMENT_IDS
    assert len(TRACEABILITY) == 26


def test_prepare_is_deterministic_and_hashes_payload_not_saved_envelope(tmp_path):
    repository, source_commit = _create_repository(tmp_path)
    config_path = tmp_path / "start.json"
    _write_json(config_path, _start_config(repository, source_commit))
    roots = (tmp_path / "private-a", tmp_path / "private-b")
    for private_root in roots:
        private_root.mkdir()
        completed = _run_cli(
            repository,
            "prepare",
            "--config",
            str(config_path),
            "--private-root",
            str(private_root),
        )
        assert completed.returncode == 0
        result = _result(completed)
        assert {key: result[key] for key in result if key != "detail"} == {
            "schema_version": 1,
            "command": "prepare",
            "result": "completed",
            "state": "ready_for_prompt_audit",
            "run_id": "run-001",
            "event_id": "0001-prepared",
            "stop_code": None,
        }
        assert result["detail"] is None or isinstance(result["detail"], str)

    relative_paths = (
        "manifest.json",
        "prompt-audit-envelope.json",
        "events/0001-prepared.json",
    )
    for relative_path in relative_paths:
        assert (roots[0] / "run-001" / relative_path).read_bytes() == (
            roots[1] / "run-001" / relative_path
        ).read_bytes()

    envelope_path = roots[0] / "run-001" / "prompt-audit-envelope.json"
    payload_digest = _payload_digest(envelope_path)
    assert payload_digest != _sha256(envelope_path.read_bytes())
    assert not (roots[0] / "run-001" / "prompt-judgment-envelope.json").exists()


@pytest.mark.parametrize(
    ("mutation", "stop_code"),
    (
        (lambda config: config["instruction"].update({"sha256": "0" * 64}), "source_digest_mismatch"),
        (lambda config: config["requirement_ids"].pop(), "requirement_mismatch"),
        (lambda config: config["requirement_ids"].append("AC-PC-999"), "requirement_mismatch"),
    ),
)
def test_prepare_rejects_tampered_source_and_requirement_set(
    tmp_path,
    mutation,
    stop_code,
):
    repository, source_commit = _create_repository(tmp_path)
    private_root = tmp_path / "private"
    private_root.mkdir()
    config = _start_config(repository, source_commit)
    mutation(config)
    config_path = tmp_path / "start.json"
    _write_json(config_path, config)

    completed = _run_cli(
        repository,
        "prepare",
        "--config",
        str(config_path),
        "--private-root",
        str(private_root),
    )

    assert completed.returncode == 2
    result = _result(completed)
    assert result["result"] == "stopped"
    assert result["stop_code"] == stop_code
    assert not (private_root / "run-001").exists()


@pytest.mark.parametrize("placement", ("inside", "parent", "symlink"))
def test_prepare_rejects_unsafe_private_root_placements(tmp_path, placement):
    repository, source_commit = _create_repository(tmp_path)
    config_path = tmp_path / "start.json"
    _write_json(config_path, _start_config(repository, source_commit))
    if placement == "inside":
        private_root = repository / "private"
        private_root.mkdir()
    elif placement == "parent":
        private_root = tmp_path
    else:
        private_target = tmp_path / "private-target"
        private_target.mkdir()
        private_root = tmp_path / "private-link"
        private_root.symlink_to(private_target, target_is_directory=True)

    completed = _run_cli(
        repository,
        "prepare",
        "--config",
        str(config_path),
        "--private-root",
        str(private_root),
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "private_root_invalid"
    assert not (private_root / "run-001").exists()


def test_successful_audit_and_judgment_derive_state_from_event_chain(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    finding = {
        "id": "PA-PC-001",
        "category": "omission",
        "severity": "high",
        "requirement_ids": ["AC-PC-001"],
        "evidence": "entrypoint evidence",
    }
    assert _complete_audit(tmp_path, repository, private_root, [finding])["state"] == (
        "ready_for_prompt_judgment"
    )
    run_root = private_root / "run-001"
    judgment_envelope = json.loads(
        (run_root / "prompt-judgment-envelope.json").read_text(encoding="utf-8")
    )
    judgment_raw = _raw_path(
        tmp_path,
        "judgment-raw.json",
        {
            "schema_version": 1,
            "result_kind": "prompt_judgment",
            "status": "completed",
            "audit_parsed_sha256": judgment_envelope["audit_parsed_sha256"],
            "recommendations": [
                {
                    "finding_id": "PA-PC-001",
                    "recommendation": "accept",
                    "rationale": "complete",
                }
            ],
        },
    )
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_judgment",
        attempt_id="judgment-001",
        input_digest=_payload_digest(run_root / "prompt-judgment-envelope.json"),
        raw_file=judgment_raw,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_judgment",
        "judgment-001",
        judgment_raw,
        launch,
    )

    assert completed.returncode == 0
    result = _result(completed)
    assert result["state"] == "human_decision_required"
    status = _run_cli(
        repository,
        "status",
        "--private-root",
        str(private_root),
        "--run-id",
        "run-001",
    )
    assert status.returncode == 0
    assert _result(status)["state"] == "human_decision_required"


def test_empty_findings_reaches_ready_for_executor_boundary(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    assert _complete_audit(tmp_path, repository, private_root)["state"] == (
        "ready_for_prompt_judgment"
    )
    run_root = private_root / "run-001"
    judgment_envelope = json.loads(
        (run_root / "prompt-judgment-envelope.json").read_text(encoding="utf-8")
    )
    raw_file = _raw_path(
        tmp_path,
        "judgment-empty.json",
        {
            "schema_version": 1,
            "result_kind": "prompt_judgment",
            "status": "completed",
            "audit_parsed_sha256": judgment_envelope["audit_parsed_sha256"],
            "recommendations": [],
        },
    )
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_judgment",
        attempt_id="judgment-empty",
        input_digest=_payload_digest(run_root / "prompt-judgment-envelope.json"),
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_judgment",
        "judgment-empty",
        raw_file,
        launch,
    )

    assert completed.returncode == 0
    assert _result(completed)["state"] == "ready_for_executor"


def test_audit_requires_complete_requirement_coverage(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    raw = {
        "schema_version": 1,
        "result_kind": "prompt_audit",
        "status": "completed",
        "findings": [],
        "requirement_results": [
            {"requirement_id": value, "status": "checked", "evidence": "checked"}
            for value in REQUIREMENT_IDS[:-1]
        ],
    }
    raw_file = _raw_path(tmp_path, "audit-incomplete.json", raw)
    run_root = private_root / "run-001"
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-incomplete",
        input_digest=_payload_digest(run_root / "prompt-audit-envelope.json"),
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-incomplete",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "coverage_incomplete"
    assert (run_root / "raw/audit-incomplete.json").is_file()
    assert (run_root / "launch/audit-incomplete.json").is_file()
    assert not (run_root / "parsed/audit-incomplete.json").exists()
    assert (run_root / "events/0002-prompt-audit-parse-failed.json").is_file()


def test_judgment_requires_one_recommendation_per_finding(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    findings = [
        {
            "id": finding_id,
            "category": "omission",
            "severity": "medium",
            "requirement_ids": ["AC-PC-001"],
            "evidence": finding_id,
        }
        for finding_id in ("PA-PC-001", "PA-PC-002")
    ]
    _complete_audit(tmp_path, repository, private_root, findings)
    run_root = private_root / "run-001"
    judgment_envelope = json.loads(
        (run_root / "prompt-judgment-envelope.json").read_text(encoding="utf-8")
    )
    raw_file = _raw_path(
        tmp_path,
        "judgment-incomplete.json",
        {
            "schema_version": 1,
            "result_kind": "prompt_judgment",
            "status": "completed",
            "audit_parsed_sha256": judgment_envelope["audit_parsed_sha256"],
            "recommendations": [
                {
                    "finding_id": "PA-PC-001",
                    "recommendation": "hold",
                    "rationale": "only one",
                }
            ],
        },
    )
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_judgment",
        attempt_id="judgment-incomplete",
        input_digest=_payload_digest(run_root / "prompt-judgment-envelope.json"),
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_judgment",
        "judgment-incomplete",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "coverage_incomplete"
    assert (run_root / "raw/judgment-incomplete.json").is_file()
    assert not (run_root / "parsed/judgment-incomplete.json").exists()


def test_ingest_rejects_stage_skip_before_writing_attempt(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "judgment.json", {})
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_judgment",
        attempt_id="judgment-early",
        input_digest="0" * 64,
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_judgment",
        "judgment-early",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "transition_invalid"
    run_root = private_root / "run-001"
    assert not (run_root / "raw/judgment-early.json").exists()
    assert not (run_root / "launch/judgment-early.json").exists()


def test_launch_failure_is_preserved_before_stopping(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "launch-failed.json", {"diagnostic": "failed"})
    run_root = private_root / "run-001"
    digest = _payload_digest(run_root / "prompt-audit-envelope.json")
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-failed",
        input_digest=digest,
        raw_file=raw_file,
        status="failed",
        exit_code=17,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-failed",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "launch_failed"
    assert (run_root / "raw/audit-failed.json").is_file()
    assert (run_root / "launch/audit-failed.json").is_file()
    assert not (run_root / "parsed/audit-failed.json").exists()
    assert (run_root / "events/0002-prompt-audit-launch-failed.json").is_file()


@pytest.mark.parametrize("also_failed", (False, True))
def test_stale_input_digest_wins_over_launch_status(tmp_path, also_failed):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "stale-input.json", {"old": True})
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-stale",
        input_digest="0" * 64,
        raw_file=raw_file,
        status="failed" if also_failed else "succeeded",
        exit_code=9 if also_failed else 0,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-stale",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "input_payload_mismatch"
    run_root = private_root / "run-001"
    assert (run_root / "raw/audit-stale.json").is_file()
    assert (run_root / "events/0002-prompt-audit-input-mismatch.json").is_file()


@pytest.mark.parametrize(
    ("status", "exit_code"),
    (("succeeded", 3), ("failed", 0)),
)
def test_launch_status_must_match_all_command_exit_codes(tmp_path, status, exit_code):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "invalid-launch.json", {"not": "parsed"})
    run_root = private_root / "run-001"
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-invalid-launch",
        input_digest=_payload_digest(run_root / "prompt-audit-envelope.json"),
        raw_file=raw_file,
        status=status,
        exit_code=exit_code,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-invalid-launch",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "launch_record_invalid"
    assert not (run_root / "raw/audit-invalid-launch.json").exists()
    assert not (run_root / "launch/audit-invalid-launch.json").exists()


def test_saved_envelope_file_digest_is_not_valid_input_payload_digest(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    run_root = private_root / "run-001"
    envelope_file = run_root / "prompt-audit-envelope.json"
    wrong_digest = _sha256(envelope_file.read_bytes())
    assert wrong_digest != _payload_digest(envelope_file)
    raw_file = _raw_path(tmp_path, "whole-envelope-digest.json", {})
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-whole-file",
        input_digest=wrong_digest,
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-whole-file",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "input_payload_mismatch"


def test_failed_ingest_never_overwrites_preserved_raw_result(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "first.json", {"first": True})
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-reused",
        input_digest="0" * 64,
        raw_file=raw_file,
    )
    first = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-reused",
        raw_file,
        launch,
    )
    assert first.returncode == 2
    stored_path = private_root / "run-001/raw/audit-reused.json"
    original = stored_path.read_bytes()
    raw_file = _raw_path(tmp_path, "second.json", {"second": True})
    second = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-reused",
        raw_file,
        launch,
    )

    assert second.returncode == 2
    assert _result(second)["stop_code"] == "attempt_exists"
    assert stored_path.read_bytes() == original


def test_status_detects_stored_raw_digest_tampering(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    raw_file = _raw_path(tmp_path, "failed.json", {"diagnostic": "failed"})
    run_root = private_root / "run-001"
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-failed",
        input_digest=_payload_digest(run_root / "prompt-audit-envelope.json"),
        raw_file=raw_file,
        status="failed",
        exit_code=7,
    )
    assert _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-failed",
        raw_file,
        launch,
    ).returncode == 2
    stored_raw = run_root / "raw/audit-failed.json"
    stored_raw.write_bytes(stored_raw.read_bytes().replace(b"failed", b"forged", 1))

    completed = _run_cli(
        repository,
        "status",
        "--private-root",
        str(private_root),
        "--run-id",
        "run-001",
    )

    assert completed.returncode == 2
    result = _result(completed)
    assert result["state"] == "blocked"
    assert result["stop_code"] == "stored_record_invalid"


def test_status_reports_stale_when_current_instruction_differs_from_commit(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    instruction = repository / INSTRUCTION_PATH
    instruction.write_bytes(instruction.read_bytes() + b"\nchanged after prepare\n")

    completed = _run_cli(
        repository,
        "status",
        "--private-root",
        str(private_root),
        "--run-id",
        "run-001",
    )

    assert completed.returncode == 2
    result = _result(completed)
    assert result["state"] == "stale"
    assert result["stop_code"] == "stale_input"


@pytest.mark.parametrize(
    "raw_mutation",
    (
        lambda raw: raw.update({"unexpected": True}),
        lambda raw: raw.pop("status"),
    ),
)
def test_fixed_result_documents_reject_extra_and_missing_keys(tmp_path, raw_mutation):
    repository, private_root, _ = _prepare(tmp_path)
    raw = {
        "schema_version": 1,
        "result_kind": "prompt_audit",
        "status": "completed",
        "findings": [],
        "requirement_results": [
            {"requirement_id": value, "status": "checked", "evidence": "checked"}
            for value in REQUIREMENT_IDS
        ],
    }
    raw_mutation(raw)
    raw_file = _raw_path(tmp_path, "invalid-shape.json", raw)
    run_root = private_root / "run-001"
    launch = _launch_path(
        tmp_path,
        run_id="run-001",
        stage="prompt_audit",
        attempt_id="audit-invalid-shape",
        input_digest=_payload_digest(run_root / "prompt-audit-envelope.json"),
        raw_file=raw_file,
    )

    completed = _ingest(
        repository,
        private_root,
        "run-001",
        "prompt_audit",
        "audit-invalid-shape",
        raw_file,
        launch,
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "raw_parse_failed"
    assert (run_root / "raw/audit-invalid-shape.json").is_file()


def test_pilot_code_cannot_launch_claude_codex_or_shell_commands():
    source = PROJECT_ROOT / "tools/development/pilot_collaboration.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    forbidden = ("claude", "codex", "subagent")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function_name = None
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            function_name = f"{node.func.value.id}.{node.func.attr}"
        if function_name != "subprocess.run":
            continue
        for keyword in node.keywords:
            assert not (keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value)
        if not node.args:
            continue
        literal_values = [
            value.value.lower()
            for value in ast.walk(node.args[0])
            if isinstance(value, ast.Constant) and isinstance(value.value, str)
        ]
        assert not any(
            marker in value
            for marker in forbidden
            for value in literal_values
        )


def test_pilot_does_not_reinterpret_closed_review_pipeline():
    source = (PROJECT_ROOT / "tools/development/pilot_collaboration.py").read_text(
        encoding="utf-8"
    )
    assert "tools.bootstrap.review_pipeline" not in source
    assert "review_pipeline" not in source


def test_prepare_and_ingest_do_not_write_workflow_ledgers(tmp_path):
    repository, private_root, _ = _prepare(tmp_path)
    assert not (repository / ".reviewcompass/workflow").exists()
    _complete_audit(tmp_path, repository, private_root)
    assert not (repository / ".reviewcompass/workflow").exists()


def test_round_above_limit_stops_before_run_creation(tmp_path):
    repository, source_commit = _create_repository(tmp_path)
    config = _start_config(repository, source_commit)
    config["instruction_quality_round"] = 3
    config["instruction_quality_round_limit"] = 2
    config_path = tmp_path / "start.json"
    _write_json(config_path, config)
    private_root = tmp_path / "private"
    private_root.mkdir()

    completed = _run_cli(
        repository,
        "prepare",
        "--config",
        str(config_path),
        "--private-root",
        str(private_root),
    )

    assert completed.returncode == 2
    assert _result(completed)["stop_code"] == "config_invalid"
    assert not (private_root / "run-001").exists()
