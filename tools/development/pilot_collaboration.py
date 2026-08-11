"""操縦者別連携pilotの決定的な準備・取込み・状態導出。"""

import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

from tools.bootstrap.immutable_result_store import (
    ImmutableResultStoreError,
    canonical_json_bytes,
    store_immutable_json,
)
from tools.common.digests import sha256_hex as _sha256


INSTRUCTION_PATH = (
    "records/session-handoffs/"
    "2026-08-11-pilot-collaboration-entry-implementation-request-v6.md"
)
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]*")
REQUIREMENT_ID = re.compile(r"(?:AC|NG|ST|OUT)-[A-Z0-9]+(?:-[A-Z0-9]+)*")
FINDING_ID = re.compile(r"PA-[A-Z0-9]+(?:-[A-Z0-9]+)*")
SHA256 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")
START_CONFIG_KEYS = {
    "schema_version",
    "run_id",
    "collaboration_method",
    "request_kind",
    "pilot",
    "implementer",
    "pilot_model",
    "reviewer_model",
    "instruction_quality_model",
    "source_commit",
    "instruction",
    "materials",
    "fixed_input",
    "requirement_ids",
    "result_contract_version",
    "instruction_quality_round",
    "instruction_quality_round_limit",
    "implementation_review_round_limit",
    "mechanical_assurance_status",
}
ASSURANCE_KEYS = {
    "instruction_preflight",
    "stage_ledger",
    "change_inventory",
    "raw_result_store",
    "result_parser",
    "reuse_guard",
    "capability_preflight",
}
LAUNCH_KEYS = {
    "schema_version",
    "execution_id",
    "run_id",
    "stage",
    "attempt_id",
    "provider",
    "model",
    "status",
    "input_payload_sha256",
    "commands",
    "material_observation",
}
EVENT_KEYS = {
    "schema_version",
    "event_id",
    "event_type",
    "run_id",
    "request_kind",
    "stage",
    "round",
    "previous_event_id",
    "previous_event_sha256",
    "attempt_id",
    "input_sha256",
    "output_sha256",
    "status",
    "stop_code",
}


class PilotStop(Exception):
    def __init__(
        self,
        code,
        *,
        state=None,
        run_id=None,
        event_id=None,
        detail=None,
    ):
        super().__init__(code)
        self.code = code
        self.state = state
        self.run_id = run_id
        self.event_id = event_id
        self.detail = detail


def _stop(code, **values):
    raise PilotStop(code, **values)


def _is_int(value, minimum=None):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and (minimum is None or value >= minimum)
    )


def _is_text(value):
    return isinstance(value, str) and bool(value) and "\x00" not in value


def _is_identifier(value):
    return _is_text(value) and IDENTIFIER.fullmatch(value) is not None


def _is_sha256(value):
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def _exact_object(value, keys):
    return isinstance(value, dict) and set(value) == set(keys)


def _safe_relative_path(value):
    if not _is_text(value):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and value not in (".", "..")
        and all(part not in ("", ".", "..") for part in path.parts)
        and str(path) == value
    )


def _read_external_file(path, stop_code):
    value = Path(path)
    if not value.is_absolute() or value.is_symlink() or not value.is_file():
        _stop(stop_code)
    try:
        return value.read_bytes()
    except OSError:
        _stop(stop_code)


def _decode_json(data, stop_code):
    try:
        text = data.decode("utf-8")
        value = json.loads(text)
    except (UnicodeError, json.JSONDecodeError):
        _stop(stop_code)
    return value


def _read_stored_json(path):
    value = Path(path)
    if value.is_symlink() or not value.is_file():
        _stop("stored_record_invalid", state="blocked")
    try:
        data = value.read_bytes()
        document = json.loads(data.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        _stop("stored_record_invalid", state="blocked")
    if data != canonical_json_bytes(document) + b"\n":
        _stop("stored_record_invalid", state="blocked")
    return document


def _run_git(repository, *arguments, binary=False):
    completed = subprocess.run(
        ("git", *arguments),
        cwd=str(repository),
        check=False,
        capture_output=True,
        text=not binary,
    )
    return completed


def _git_blob(repository, commit, relative_path, stop_code):
    tree = _run_git(repository, "ls-tree", "-z", commit, "--", relative_path, binary=True)
    if tree.returncode != 0 or not tree.stdout:
        _stop(stop_code)
    try:
        metadata, found_path = tree.stdout[:-1].split(b"\t", 1)
        mode, object_type, _ = metadata.split(b" ", 2)
        decoded_path = found_path.decode("utf-8")
    except (ValueError, UnicodeError):
        _stop(stop_code)
    if object_type != b"blob" or mode not in (b"100644", b"100755") or decoded_path != relative_path:
        _stop(stop_code)
    shown = _run_git(repository, "show", f"{commit}:{relative_path}", binary=True)
    if shown.returncode != 0:
        _stop(stop_code)
    return shown.stdout


def _validate_path_digest_object(value):
    return (
        _exact_object(value, {"path", "sha256"})
        and _safe_relative_path(value["path"])
        and _is_sha256(value["sha256"])
    )


def _validate_fixed_input(value, material_paths):
    keys = {
        "origin",
        "count",
        "derivation_argv",
        "derivation_output_sha256",
        "selector",
        "selection_basis",
        "selected_paths_sha256",
    }
    if not _exact_object(value, keys):
        return False
    expected_paths_digest = _sha256("\n".join(sorted(material_paths)).encode("utf-8"))
    if (
        value["count"] != len(material_paths)
        or not _is_int(value["count"], 1)
        or value["selected_paths_sha256"] != expected_paths_digest
    ):
        return False
    if value["origin"] == "machine_derived":
        return (
            isinstance(value["derivation_argv"], list)
            and bool(value["derivation_argv"])
            and all(_is_text(item) for item in value["derivation_argv"])
            and _is_sha256(value["derivation_output_sha256"])
            and value["selector"] is None
            and value["selection_basis"] is None
        )
    if value["origin"] == "judgment_selected":
        return (
            value["derivation_argv"] is None
            and value["derivation_output_sha256"] is None
            and _is_text(value["selector"])
            and _is_text(value["selection_basis"])
        )
    return False


def _validate_start_config(value):
    if not _exact_object(value, START_CONFIG_KEYS):
        _stop("config_invalid")
    instruction = value["instruction"]
    materials = value["materials"]
    requirements = value["requirement_ids"]
    if (
        value["schema_version"] != 1
        or not _is_identifier(value["run_id"])
        or value["collaboration_method"] != "pilot_specific_claude_codex"
        or value["request_kind"] != "implementation"
        or value["pilot"] != "codex"
        or value["implementer"] not in ("claude", "codex_implementation_subagent")
        or value["pilot_model"] not in ("gpt-5.6-sol", "gpt-5.6-terra")
        or value["reviewer_model"] not in ("gpt-5.6-sol", "gpt-5.6-terra")
        or value["pilot_model"] == value["reviewer_model"]
        or value["instruction_quality_model"] != value["reviewer_model"]
        or not isinstance(value["source_commit"], str)
        or COMMIT.fullmatch(value["source_commit"]) is None
        or not _validate_path_digest_object(instruction)
        or instruction["path"] != INSTRUCTION_PATH
        or not isinstance(materials, list)
        or not materials
        or not all(_validate_path_digest_object(item) for item in materials)
        or len({item["path"] for item in materials}) != len(materials)
        or not isinstance(requirements, list)
        or not requirements
        or not all(
            isinstance(item, str) and REQUIREMENT_ID.fullmatch(item)
            for item in requirements
        )
        or len(set(requirements)) != len(requirements)
        or {item.split("-", 1)[0] for item in requirements} != {"AC", "NG", "ST", "OUT"}
        or value["result_contract_version"] != "pilot-collaboration-prompt-quality-v1"
        or not _is_int(value["instruction_quality_round"], 1)
        or not _is_int(value["instruction_quality_round_limit"], 1)
        or value["instruction_quality_round"] > value["instruction_quality_round_limit"]
        or not _is_int(value["implementation_review_round_limit"], 1)
        or not _exact_object(value["mechanical_assurance_status"], ASSURANCE_KEYS)
        or set(value["mechanical_assurance_status"].values()) != {"specified_only"}
        or not _validate_fixed_input(
            value["fixed_input"],
            [item["path"] for item in materials],
        )
    ):
        _stop("config_invalid")
    normalized = dict(value)
    normalized["materials"] = sorted(
        (dict(item) for item in materials),
        key=lambda item: item["path"],
    )
    normalized["requirement_ids"] = sorted(requirements)
    return normalized


def _verify_sources(repository, config, *, current_mismatch_code):
    commit = config["source_commit"]
    commit_type = _run_git(repository, "cat-file", "-t", commit)
    if commit_type.returncode != 0 or commit_type.stdout.strip() != "commit":
        _stop("source_commit_invalid")
    instruction_text = None
    for source in (config["instruction"], *config["materials"]):
        blob = _git_blob(repository, commit, source["path"], "source_blob_invalid")
        if _sha256(blob) != source["sha256"]:
            _stop("source_digest_mismatch")
        current = repository / source["path"]
        if current.is_symlink() or not current.is_file():
            _stop(current_mismatch_code)
        try:
            current_bytes = current.read_bytes()
        except OSError:
            _stop(current_mismatch_code)
        if current_bytes != blob:
            _stop(current_mismatch_code)
        if source is config["instruction"]:
            try:
                instruction_text = blob.decode("utf-8")
            except UnicodeError:
                _stop("source_blob_invalid")
    extracted = set(REQUIREMENT_ID.findall(instruction_text))
    if extracted != set(config["requirement_ids"]):
        _stop("requirement_mismatch")
    return instruction_text


def _validate_private_root(repository, private_root):
    root = Path(private_root)
    if (
        not root.is_absolute()
        or root.is_symlink()
        or not root.is_dir()
        or root == repository
        or root == repository.parent
        or repository in root.parents
    ):
        _stop("private_root_invalid")
    return root


def _with_digest(document, digest_key):
    value = dict(document)
    value[digest_key] = _sha256(canonical_json_bytes(document))
    return value


def _payload_digest(envelope):
    if not isinstance(envelope, dict) or "envelope_sha256" not in envelope:
        _stop("stored_record_invalid", state="blocked")
    payload = dict(envelope)
    stored = payload.pop("envelope_sha256")
    calculated = _sha256(canonical_json_bytes(payload))
    if stored != calculated:
        _stop("stored_record_invalid", state="blocked")
    return calculated


def _event_document(
    manifest,
    *,
    event_id,
    event_type,
    stage,
    previous,
    attempt_id,
    input_sha256,
    output_sha256,
    status,
    stop_code,
):
    return {
        "schema_version": 1,
        "event_id": event_id,
        "event_type": event_type,
        "run_id": manifest["start_config"]["run_id"],
        "request_kind": "implementation",
        "stage": stage,
        "round": manifest["start_config"]["instruction_quality_round"],
        "previous_event_id": None if previous is None else previous["event_id"],
        "previous_event_sha256": (
            None if previous is None else _sha256(canonical_json_bytes(previous))
        ),
        "attempt_id": attempt_id,
        "input_sha256": input_sha256,
        "output_sha256": output_sha256,
        "status": status,
        "stop_code": stop_code,
    }


def prepare(repository, config_path, private_root):
    repository = Path(repository).resolve()
    if not (repository / ".git").exists():
        _stop("repository_invalid")
    root = _validate_private_root(repository, private_root)
    config_bytes = _read_external_file(config_path, "config_invalid")
    config = _validate_start_config(_decode_json(config_bytes, "config_invalid"))
    instruction_text = _verify_sources(
        repository,
        config,
        current_mismatch_code="source_blob_invalid",
    )
    run_id = config["run_id"]
    run_root = root / run_id
    candidate = root / f".{run_id}.candidate"
    if run_root.exists() or candidate.exists():
        _stop("run_exists", run_id=run_id)
    try:
        candidate.mkdir()
        for directory in ("events", "launch", "raw", "parsed"):
            (candidate / directory).mkdir()
        manifest_body = {
            "schema_version": 1,
            "repository_root": str(repository),
            "config_raw_sha256": _sha256(config_bytes),
            "start_config": config,
        }
        manifest = _with_digest(manifest_body, "manifest_sha256")
        audit_body = {
            "schema_version": 1,
            "result_kind": "prompt_audit",
            "run_id": run_id,
            "source_commit": config["source_commit"],
            "instruction": {
                "path": config["instruction"]["path"],
                "sha256": config["instruction"]["sha256"],
                "text": instruction_text,
            },
            "materials": [dict(item) for item in config["materials"]],
            "fixed_input": config["fixed_input"],
            "requirement_ids": list(config["requirement_ids"]),
            "output_contract": "pilot-prompt-audit-v1",
        }
        audit_envelope = _with_digest(audit_body, "envelope_sha256")
        prepared = _event_document(
            manifest,
            event_id="0001-prepared",
            event_type="prepared",
            stage="prepare",
            previous=None,
            attempt_id=None,
            input_sha256=_sha256(config_bytes),
            output_sha256=manifest["manifest_sha256"],
            status="completed",
            stop_code=None,
        )
        store_immutable_json(candidate, "manifest.json", manifest)
        store_immutable_json(candidate, "prompt-audit-envelope.json", audit_envelope)
        store_immutable_json(candidate, "events/0001-prepared.json", prepared)
        for relative_path in (
            "manifest.json",
            "prompt-audit-envelope.json",
            "events/0001-prepared.json",
        ):
            _read_stored_json(candidate / relative_path)
        os.rename(candidate, run_root)
    except PilotStop:
        if candidate.exists():
            shutil.rmtree(candidate)
        raise
    except (OSError, ImmutableResultStoreError):
        if candidate.exists():
            shutil.rmtree(candidate)
        _stop("internal_error", run_id=run_id)
    return {
        "state": "ready_for_prompt_audit",
        "run_id": run_id,
        "event_id": "0001-prepared",
    }


def _load_manifest(run_root):
    manifest = _read_stored_json(run_root / "manifest.json")
    if not _exact_object(
        manifest,
        {
            "schema_version",
            "repository_root",
            "config_raw_sha256",
            "start_config",
            "manifest_sha256",
        },
    ):
        _stop("stored_record_invalid", state="blocked")
    body = dict(manifest)
    stored = body.pop("manifest_sha256")
    if (
        manifest["schema_version"] != 1
        or not _is_sha256(manifest["config_raw_sha256"])
        or stored != _sha256(canonical_json_bytes(body))
    ):
        _stop("stored_record_invalid", state="blocked")
    try:
        manifest["start_config"] = _validate_start_config(manifest["start_config"])
    except PilotStop:
        _stop("stored_record_invalid", state="blocked")
    return manifest


def _load_events(run_root, manifest):
    event_paths = sorted((run_root / "events").glob("*.json"))
    if not event_paths:
        _stop("stored_record_invalid", state="blocked")
    events = []
    previous = None
    for index, event_path in enumerate(event_paths, 1):
        event = _read_stored_json(event_path)
        expected_prefix = f"{index:04d}-"
        if (
            not _exact_object(event, EVENT_KEYS)
            or not event_path.stem.startswith(expected_prefix)
            or event["event_id"] != event_path.stem
            or event["run_id"] != manifest["start_config"]["run_id"]
            or event["request_kind"] != "implementation"
            or event["round"] != manifest["start_config"]["instruction_quality_round"]
            or event["previous_event_id"] != (
                None if previous is None else previous["event_id"]
            )
            or event["previous_event_sha256"] != (
                None if previous is None else _sha256(canonical_json_bytes(previous))
            )
        ):
            _stop("stored_record_invalid", state="blocked")
        events.append(event)
        previous = event
    return events


def _load_envelope(run_root, stage):
    name = "prompt-audit-envelope.json" if stage == "prompt_audit" else "prompt-judgment-envelope.json"
    envelope = _read_stored_json(run_root / name)
    return envelope, _payload_digest(envelope)


def _validate_command(command):
    return (
        _exact_object(command, {"argv", "exit_code"})
        and isinstance(command["argv"], list)
        and bool(command["argv"])
        and all(_is_text(item) for item in command["argv"])
        and _is_int(command["exit_code"])
    )


def _validate_launch(value, manifest, run_id, stage, attempt_id, raw_digest):
    if not _exact_object(value, LAUNCH_KEYS):
        _stop("launch_record_invalid", run_id=run_id)
    observation = value["material_observation"]
    commands = value["commands"]
    if (
        value["schema_version"] != 1
        or not _is_identifier(value["execution_id"])
        or value["run_id"] != run_id
        or value["stage"] != stage
        or value["attempt_id"] != attempt_id
        or not _is_text(value["provider"])
        or value["model"] != manifest["start_config"]["instruction_quality_model"]
        or value["status"] not in ("succeeded", "failed")
        or not _is_sha256(value["input_payload_sha256"])
        or not isinstance(commands, list)
        or not commands
        or not all(_validate_command(command) for command in commands)
        or not _exact_object(
            observation,
            {
                "material_mode",
                "extractable_count",
                "unextractable_count",
                "unique_count",
                "raw_sha256",
            },
        )
        or observation["material_mode"] != "discovery"
        or not _is_int(observation["extractable_count"], 0)
        or not _is_int(observation["unextractable_count"], 0)
        or not _is_int(observation["unique_count"], 0)
        or observation["unique_count"] > observation["extractable_count"]
        or not _is_sha256(observation["raw_sha256"])
    ):
        _stop("launch_record_invalid", run_id=run_id)
    all_zero = all(command["exit_code"] == 0 for command in commands)
    if (value["status"] == "succeeded") != all_zero:
        _stop("launch_record_invalid", run_id=run_id)
    if observation["raw_sha256"] != raw_digest:
        _stop("raw_digest_mismatch", run_id=run_id)
    return value


def _normalized_audit(raw, requirements):
    keys = {"schema_version", "result_kind", "status", "findings", "requirement_results"}
    if (
        not _exact_object(raw, keys)
        or raw["schema_version"] != 1
        or raw["result_kind"] != "prompt_audit"
        or raw["status"] != "completed"
        or not isinstance(raw["findings"], list)
        or not isinstance(raw["requirement_results"], list)
    ):
        _stop("raw_parse_failed")
    findings = []
    finding_ids = []
    for finding in raw["findings"]:
        if (
            not _exact_object(
                finding,
                {"id", "category", "severity", "requirement_ids", "evidence"},
            )
            or not isinstance(finding["id"], str)
            or FINDING_ID.fullmatch(finding["id"]) is None
            or finding["category"] not in (
                "omission",
                "leading",
                "target_mismatch",
                "insufficient_material",
                "scope_deviation",
            )
            or finding["severity"] not in ("critical", "high", "medium", "low")
            or not isinstance(finding["requirement_ids"], list)
            or not finding["requirement_ids"]
            or len(set(finding["requirement_ids"])) != len(finding["requirement_ids"])
            or not set(finding["requirement_ids"]) <= set(requirements)
            or not _is_text(finding["evidence"])
        ):
            _stop("raw_parse_failed")
        value = dict(finding)
        value["requirement_ids"] = sorted(finding["requirement_ids"])
        findings.append(value)
        finding_ids.append(finding["id"])
    if len(set(finding_ids)) != len(finding_ids):
        _stop("raw_parse_failed")
    results = []
    result_ids = []
    for result in raw["requirement_results"]:
        if (
            not _exact_object(result, {"requirement_id", "status", "evidence"})
            or result["status"] != "checked"
            or not _is_text(result["evidence"])
            or not isinstance(result["requirement_id"], str)
        ):
            _stop("raw_parse_failed")
        results.append(dict(result))
        result_ids.append(result["requirement_id"])
    if len(set(result_ids)) != len(result_ids) or set(result_ids) != set(requirements):
        _stop("coverage_incomplete")
    return {
        "schema_version": 1,
        "result_kind": "prompt_audit",
        "status": "completed",
        "findings": sorted(findings, key=lambda item: item["id"]),
        "requirement_results": sorted(results, key=lambda item: item["requirement_id"]),
    }


def _normalized_judgment(raw, audit_result, audit_digest):
    if (
        not _exact_object(
            raw,
            {"schema_version", "result_kind", "status", "audit_parsed_sha256", "recommendations"},
        )
        or raw["schema_version"] != 1
        or raw["result_kind"] != "prompt_judgment"
        or raw["status"] != "completed"
        or not _is_sha256(raw["audit_parsed_sha256"])
        or not isinstance(raw["recommendations"], list)
    ):
        _stop("raw_parse_failed")
    if raw["audit_parsed_sha256"] != audit_digest:
        _stop("audit_digest_mismatch")
    finding_ids = [finding["id"] for finding in audit_result["findings"]]
    recommendations = []
    recommendation_ids = []
    for recommendation in raw["recommendations"]:
        if (
            not _exact_object(recommendation, {"finding_id", "recommendation", "rationale"})
            or not isinstance(recommendation["finding_id"], str)
            or recommendation["recommendation"] not in ("accept", "reject", "hold")
            or not _is_text(recommendation["rationale"])
        ):
            _stop("raw_parse_failed")
        recommendations.append(dict(recommendation))
        recommendation_ids.append(recommendation["finding_id"])
    if (
        len(set(recommendation_ids)) != len(recommendation_ids)
        or set(recommendation_ids) != set(finding_ids)
    ):
        _stop("coverage_incomplete")
    return {
        "schema_version": 1,
        "result_kind": "prompt_judgment",
        "status": "completed",
        "audit_parsed_sha256": audit_digest,
        "recommendations": sorted(recommendations, key=lambda item: item["finding_id"]),
    }


def _event_spec(stage, outcome):
    number = "0002" if stage == "prompt_audit" else "0003"
    file_stage = stage.replace("_", "-")
    suffixes = {
        "input_mismatch": (
            f"{file_stage}-input-mismatch",
            f"{stage}_input_mismatch",
        ),
        "launch_failed": (f"{file_stage}-launch-failed", f"{stage}_launch_failed"),
        "parsed": (f"{file_stage}-parsed", f"{stage}_parsed"),
        "parse_failed": (f"{file_stage}-parse-failed", f"{stage}_parse_failed"),
    }
    filename_suffix, event_type = suffixes[outcome]
    return f"{number}-{filename_suffix}", event_type


def _store_failure_event(
    run_root,
    manifest,
    previous,
    stage,
    attempt_id,
    input_digest,
    raw_digest,
    outcome,
    stop_code,
):
    event_id, event_type = _event_spec(stage, outcome)
    event = _event_document(
        manifest,
        event_id=event_id,
        event_type=event_type,
        stage=stage,
        previous=previous,
        attempt_id=attempt_id,
        input_sha256=input_digest,
        output_sha256=raw_digest,
        status="failed",
        stop_code=stop_code,
    )
    store_immutable_json(run_root, f"events/{event_id}.json", event)
    return event_id


def ingest(
    repository,
    private_root,
    run_id,
    stage,
    attempt_id,
    raw_file,
    launch_record,
):
    repository = Path(repository).resolve()
    root = _validate_private_root(repository, private_root)
    if not _is_identifier(run_id) or not _is_identifier(attempt_id):
        _stop("config_invalid")
    if stage not in ("prompt_audit", "prompt_judgment"):
        _stop("stage_invalid", run_id=run_id)
    run_root = root / run_id
    if run_root.is_symlink() or not run_root.is_dir():
        _stop("run_invalid", run_id=run_id)
    manifest = _load_manifest(run_root)
    if manifest["repository_root"] != str(repository) or manifest["start_config"]["run_id"] != run_id:
        _stop("run_invalid", run_id=run_id)
    events = _load_events(run_root, manifest)
    if any(
        (run_root / directory / f"{attempt_id}.json").exists()
        for directory in ("launch", "raw", "parsed")
    ) or any(event["attempt_id"] == attempt_id for event in events):
        _stop("attempt_exists", run_id=run_id)
    last = events[-1]
    expected_type = "prepared" if stage == "prompt_audit" else "prompt_audit_parsed"
    if last["event_type"] != expected_type:
        _stop("transition_invalid", run_id=run_id)
    try:
        _verify_sources(
            repository,
            manifest["start_config"],
            current_mismatch_code="stale_input",
        )
    except PilotStop as error:
        if error.code in ("source_blob_invalid", "source_digest_mismatch", "requirement_mismatch"):
            _stop("stale_input", state="stale", run_id=run_id)
        raise
    raw_bytes = _read_external_file(raw_file, "config_invalid")
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeError:
        _stop("raw_parse_failed", run_id=run_id)
    raw_digest = _sha256(raw_bytes)
    launch_bytes = _read_external_file(launch_record, "launch_record_invalid")
    launch = _validate_launch(
        _decode_json(launch_bytes, "launch_record_invalid"),
        manifest,
        run_id,
        stage,
        attempt_id,
        raw_digest,
    )
    envelope, current_input_digest = _load_envelope(run_root, stage)
    launch_document = _with_digest(launch, "launch_record_sha256")
    raw_document = {
        "schema_version": 1,
        "run_id": run_id,
        "stage": stage,
        "attempt_id": attempt_id,
        "input_payload_sha256": launch["input_payload_sha256"],
        "launch_record_sha256": launch_document["launch_record_sha256"],
        "raw_sha256": raw_digest,
        "raw_text": raw_text,
    }
    try:
        store_immutable_json(run_root, f"launch/{attempt_id}.json", launch_document)
        store_immutable_json(run_root, f"raw/{attempt_id}.json", raw_document)
        _read_stored_json(run_root / f"launch/{attempt_id}.json")
        _read_stored_json(run_root / f"raw/{attempt_id}.json")
    except ImmutableResultStoreError:
        _stop("attempt_exists", run_id=run_id)
    if launch["input_payload_sha256"] != current_input_digest:
        event_id = _store_failure_event(
            run_root,
            manifest,
            last,
            stage,
            attempt_id,
            current_input_digest,
            raw_digest,
            "input_mismatch",
            "input_payload_mismatch",
        )
        _stop(
            "input_payload_mismatch",
            state="blocked",
            run_id=run_id,
            event_id=event_id,
        )
    if launch["status"] == "failed":
        event_id = _store_failure_event(
            run_root,
            manifest,
            last,
            stage,
            attempt_id,
            current_input_digest,
            raw_digest,
            "launch_failed",
            "launch_failed",
        )
        _stop("launch_failed", state="blocked", run_id=run_id, event_id=event_id)
    try:
        parsed_raw = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed_raw = None
    try:
        if parsed_raw is None:
            _stop("raw_parse_failed")
        if stage == "prompt_audit":
            parsed = _normalized_audit(
                parsed_raw,
                manifest["start_config"]["requirement_ids"],
            )
            parsed_digest = _sha256(canonical_json_bytes(parsed))
            judgment_body = {
                "schema_version": 1,
                "result_kind": "prompt_judgment",
                "run_id": run_id,
                "audit_parsed_sha256": parsed_digest,
                "audit_result": parsed,
                "output_contract": "pilot-prompt-judgment-v1",
            }
            judgment_envelope = _with_digest(judgment_body, "envelope_sha256")
        else:
            audit_result = _read_stored_json(
                run_root / "parsed" / f"{last['attempt_id']}.json"
            )
            audit_digest = _sha256(canonical_json_bytes(audit_result))
            parsed = _normalized_judgment(parsed_raw, audit_result, audit_digest)
            parsed_digest = _sha256(canonical_json_bytes(parsed))
    except PilotStop as error:
        stop_code = error.code
        event_id = _store_failure_event(
            run_root,
            manifest,
            last,
            stage,
            attempt_id,
            current_input_digest,
            raw_digest,
            "parse_failed",
            stop_code,
        )
        _stop(stop_code, state="blocked", run_id=run_id, event_id=event_id)
    store_immutable_json(run_root, f"parsed/{attempt_id}.json", parsed)
    if stage == "prompt_audit":
        store_immutable_json(
            run_root,
            "prompt-judgment-envelope.json",
            judgment_envelope,
        )
    event_id, event_type = _event_spec(stage, "parsed")
    event = _event_document(
        manifest,
        event_id=event_id,
        event_type=event_type,
        stage=stage,
        previous=last,
        attempt_id=attempt_id,
        input_sha256=current_input_digest,
        output_sha256=parsed_digest,
        status="completed",
        stop_code=None,
    )
    store_immutable_json(run_root, f"events/{event_id}.json", event)
    if stage == "prompt_audit":
        state = "ready_for_prompt_judgment"
    else:
        state = (
            "human_decision_required"
            if parsed["recommendations"]
            else "ready_for_executor"
        )
    return {"state": state, "run_id": run_id, "event_id": event_id}


def _validate_stored_attempt(run_root, manifest, event):
    attempt_id = event["attempt_id"]
    launch = _read_stored_json(run_root / f"launch/{attempt_id}.json")
    raw = _read_stored_json(run_root / f"raw/{attempt_id}.json")
    if not _exact_object(launch, LAUNCH_KEYS | {"launch_record_sha256"}):
        _stop("stored_record_invalid", state="blocked")
    launch_body = dict(launch)
    launch_digest = launch_body.pop("launch_record_sha256")
    raw_text = raw.get("raw_text") if isinstance(raw, dict) else None
    if (
        launch_digest != _sha256(canonical_json_bytes(launch_body))
        or not _exact_object(
            raw,
            {
                "schema_version",
                "run_id",
                "stage",
                "attempt_id",
                "input_payload_sha256",
                "launch_record_sha256",
                "raw_sha256",
                "raw_text",
            },
        )
        or not isinstance(raw_text, str)
        or raw["schema_version"] != 1
        or raw["run_id"] != event["run_id"]
        or raw["stage"] != event["stage"]
        or raw["attempt_id"] != attempt_id
        or raw["raw_sha256"] != _sha256(raw_text.encode("utf-8"))
        or raw["launch_record_sha256"] != launch_digest
        or raw["input_payload_sha256"] != launch["input_payload_sha256"]
        or launch["material_observation"]["raw_sha256"] != raw["raw_sha256"]
        or event["output_sha256"] != (
            raw["raw_sha256"] if event["status"] == "failed" else event["output_sha256"]
        )
    ):
        _stop("stored_record_invalid", state="blocked")
    try:
        _validate_launch(
            launch_body,
            manifest,
            event["run_id"],
            event["stage"],
            attempt_id,
            raw["raw_sha256"],
        )
    except PilotStop:
        _stop("stored_record_invalid", state="blocked")
    _, current_digest = _load_envelope(run_root, event["stage"])
    mismatch_event = event["event_type"].endswith("_input_mismatch")
    if (launch["input_payload_sha256"] != current_digest) != mismatch_event:
        _stop("stored_record_invalid", state="blocked")
    if event["input_sha256"] != current_digest:
        _stop("stored_record_invalid", state="blocked")
    if event["event_type"].endswith("_launch_failed"):
        if launch["status"] != "failed" or event["stop_code"] != "launch_failed":
            _stop("stored_record_invalid", state="blocked")
    elif not mismatch_event and launch["status"] != "succeeded":
        _stop("stored_record_invalid", state="blocked")
    if event["event_type"].endswith("_parsed"):
        parsed = _read_stored_json(run_root / f"parsed/{attempt_id}.json")
        if event["output_sha256"] != _sha256(canonical_json_bytes(parsed)):
            _stop("stored_record_invalid", state="blocked")


def status(repository, private_root, run_id):
    repository = Path(repository).resolve()
    root = _validate_private_root(repository, private_root)
    if not _is_identifier(run_id):
        _stop("config_invalid")
    run_root = root / run_id
    if run_root.is_symlink() or not run_root.is_dir():
        _stop("run_invalid", run_id=run_id)
    manifest = _load_manifest(run_root)
    if manifest["repository_root"] != str(repository) or manifest["start_config"]["run_id"] != run_id:
        _stop("stored_record_invalid", state="blocked", run_id=run_id)
    events = _load_events(run_root, manifest)
    first = events[0]
    if (
        first["event_type"] != "prepared"
        or first["stage"] != "prepare"
        or first["attempt_id"] is not None
        or first["input_sha256"] != manifest["config_raw_sha256"]
        or first["output_sha256"] != manifest["manifest_sha256"]
        or first["status"] != "completed"
        or first["stop_code"] is not None
    ):
        _stop("stored_record_invalid", state="blocked", run_id=run_id)
    allowed_transitions = {
        "prepared": {
            "prompt_audit_input_mismatch",
            "prompt_audit_launch_failed",
            "prompt_audit_parsed",
            "prompt_audit_parse_failed",
        },
        "prompt_audit_parsed": {
            "prompt_judgment_input_mismatch",
            "prompt_judgment_launch_failed",
            "prompt_judgment_parsed",
            "prompt_judgment_parse_failed",
        },
    }
    for previous, event in zip(events, events[1:]):
        if event["event_type"] not in allowed_transitions.get(previous["event_type"], set()):
            _stop("stored_record_invalid", state="blocked", run_id=run_id)
        _validate_stored_attempt(run_root, manifest, event)
    try:
        _verify_sources(
            repository,
            manifest["start_config"],
            current_mismatch_code="stale_input",
        )
    except PilotStop as error:
        if error.code in (
            "stale_input",
            "source_blob_invalid",
            "source_digest_mismatch",
            "requirement_mismatch",
        ):
            _stop("stale_input", state="stale", run_id=run_id)
        raise
    last_type = events[-1]["event_type"]
    if last_type == "prepared":
        state = "ready_for_prompt_audit"
    elif last_type == "prompt_audit_parsed":
        state = "ready_for_prompt_judgment"
    elif last_type == "prompt_judgment_parsed":
        parsed = _read_stored_json(
            run_root / f"parsed/{events[-1]['attempt_id']}.json"
        )
        state = (
            "human_decision_required"
            if parsed["recommendations"]
            else "ready_for_executor"
        )
    else:
        state = "blocked"
    return {"state": state, "run_id": run_id, "event_id": None}
