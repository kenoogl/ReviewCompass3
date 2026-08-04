"""Development限定Issue Resolution早期Pilotの決定的validator。"""

import argparse
import dataclasses
import hashlib
import json
import re
from pathlib import Path


class PilotValidationError(Exception):
    """Pilot artifactまたはprojectionが契約に違反している。"""


@dataclasses.dataclass(frozen=True)
class ValidationResult:
    record_kind: str
    record_id: str
    content_digest: str


_SHA256 = re.compile(r"[0-9a-f]{64}")
_CANDIDATE_ID = re.compile(r"IC-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_DECISION_ID = re.compile(r"DEC-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_ISSUE_ID = re.compile(r"ISSUE-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_PLAN_ID = re.compile(r"PLAN-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_CHALLENGE_ID = re.compile(r"CHALLENGE-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_PLAN_CHALLENGE_CRITERIA = {
    "obligation_coverage",
    "work_item_granularity",
    "tdd_closure",
    "prohibition_transfer",
    "feasibility_dependencies",
    "oracle_quality",
    "rollback_recovery",
    "stale_binding",
    "pilot_threshold",
    "entrypoint_authority",
}
_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T"
    r"[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+-][0-9]{2}:[0-9]{2})"
)
_ACTIVE_ENTRY = re.compile(
    r"- `(?P<record_id>(?:IC|ISSUE)-[A-Z0-9-]+)`："
    r"`(?P<state>[a-z][a-z0-9_]*)`、影響：(?P<impact>[^\n]+)、"
    r"次：(?P<next_action>[^\n]+)"
)


def _sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path):
    return _sha256_bytes(Path(path).read_bytes())


def _canonical_digest(record):
    payload = {
        key: value
        for key, value in record.items()
        if key != "content_digest"
    }
    return _sha256_bytes(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _load_json(path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PilotValidationError(f"cannot load {label}") from error


def _require_exact_fields(record, expected, label):
    if not isinstance(record, dict) or set(record) != set(expected):
        raise PilotValidationError(f"{label} fields are incomplete or unknown")


def _require_text(value):
    if not isinstance(value, str) or not value.strip():
        raise PilotValidationError("text field is empty or invalid")


def _require_text_list(value, label):
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        raise PilotValidationError(f"{label} must be a non-empty text list")


def _require_optional_text_list(value, label):
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise PilotValidationError(f"{label} must be a text list")


def _require_structured_list(value, fields, label):
    if not isinstance(value, list) or not value:
        raise PilotValidationError(f"{label} must be a non-empty list")
    for item in value:
        _require_exact_fields(item, fields, label)


def _safe_relative_path(value):
    if not isinstance(value, str) or not value:
        raise PilotValidationError("artifact path is invalid")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise PilotValidationError("artifact path is invalid")
    return path


def _validate_file_reference(reference, project_root, label):
    _require_exact_fields(reference, ("path", "sha256"), label)
    relative_path = _safe_relative_path(reference["path"])
    if not isinstance(reference["sha256"], str) or not _SHA256.fullmatch(
        reference["sha256"]
    ):
        raise PilotValidationError(f"{label} is invalid")
    path = Path(project_root) / relative_path
    if not path.is_file() or _sha256_file(path) != reference["sha256"]:
        raise PilotValidationError(f"{label} is stale or unavailable")
    return path


def _validate_content_digest(record):
    digest = record.get("content_digest")
    if (
        not isinstance(digest, str)
        or not _SHA256.fullmatch(digest)
        or digest != _canonical_digest(record)
    ):
        raise PilotValidationError("content digest is invalid")


def load_config(path):
    config = _load_json(path, "Pilot config")
    expected = {
        "pilot_id",
        "pilot_version",
        "pilot_mode",
        "maximum_issue_subjects",
        "directories",
        "record_fields",
        "classification_candidates",
        "dispositions",
        "todo_projection",
    }
    if set(config) != expected:
        raise PilotValidationError("Pilot config fields are invalid")
    if (
        config["pilot_id"] != "RC3-DEVELOPMENT-ISSUE-RESOLUTION-PILOT"
        or config["pilot_version"] not in {1, 2, 3}
        or config["pilot_mode"] != "development_only_provisional"
        or config["maximum_issue_subjects"] != 1
    ):
        raise PilotValidationError("Pilot identity or scope is invalid")
    expected_directories = {
        "improvement_candidate",
        "human_triage_decision",
    }
    if config["pilot_version"] >= 2:
        expected_directories.update(
            {"issue_record", "issue_resolution_plan"}
        )
    if config["pilot_version"] == 3:
        expected_directories.add("plan_challenge")
    if set(config["directories"]) != expected_directories:
        raise PilotValidationError("Pilot directories are invalid")
    if set(config["record_fields"]) != set(config["directories"]):
        raise PilotValidationError("Pilot record fields are invalid")
    if (
        not isinstance(config["classification_candidates"], list)
        or not config["classification_candidates"]
        or not isinstance(config["dispositions"], list)
        or "issue_resolution" not in config["dispositions"]
    ):
        raise PilotValidationError("Pilot vocabularies are invalid")
    todo = config["todo_projection"]
    if set(todo) != {
        "heading",
        "maximum_entries",
        "maximum_section_bytes",
        "forbidden_document_markers",
        "forbidden_section_markers",
    }:
        raise PilotValidationError("TODO projection config is invalid")
    return config


def validate_task_contract_sources(path, *, project_root):
    contract = _load_json(path, "Pilot Task Contract")
    if (
        contract.get("task_contract_id")
        != "TC-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1"
        or contract.get("status") != "active"
        or not isinstance(contract.get("fixed_sources"), list)
        or not contract["fixed_sources"]
        or "one Pilot subject: TODO history accumulation and oversized handoff"
        not in contract.get("in_scope", [])
    ):
        raise PilotValidationError("Pilot Task Contract scope is invalid")
    for reference in contract["fixed_sources"]:
        _validate_file_reference(reference, project_root, "fixed source")
    return len(contract["fixed_sources"])


def validate_bootstrap_layout(*, project_root, config):
    project_root = Path(project_root)
    for relative in config["directories"].values():
        path = project_root / _safe_relative_path(relative)
        if not path.is_dir():
            raise PilotValidationError("Pilot bootstrap directory is missing")
        unexpected = [
            item.name
            for item in path.iterdir()
            if item.name != ".gitkeep"
        ]
        if unexpected:
            raise PilotValidationError(
                "Pilot bootstrap directory contains premature records"
            )


def _expected_record_path(config, record_kind, record_id, version):
    directory = config["directories"][record_kind]
    filename = f"{record_id.lower()}--v{version}.json"
    return f"{directory}/{filename}"


def validate_candidate(record, *, path, project_root, config):
    _require_exact_fields(
        record,
        config["record_fields"]["improvement_candidate"],
        "Improvement Candidate",
    )
    if record["record_kind"] != "improvement_candidate":
        raise PilotValidationError("record kind is invalid")
    if record["schema_version"] != 1:
        raise PilotValidationError("schema version is invalid")
    if (
        not isinstance(record["candidate_id"], str)
        or not _CANDIDATE_ID.fullmatch(record["candidate_id"])
        or record["candidate_version"] != 1
        or not isinstance(record["created_at"], str)
        or not _TIMESTAMP.fullmatch(record["created_at"])
    ):
        raise PilotValidationError("Candidate identity is invalid")
    for field in ("source_work", "problem", "proposed_action"):
        _require_text(record[field])
    for field in (
        "impact",
        "scope",
        "non_scope",
        "classification_candidates",
        "route_candidates",
        "consumer_candidates",
    ):
        _require_text_list(record[field], field)
    if not set(record["classification_candidates"]).issubset(
        config["classification_candidates"]
    ):
        raise PilotValidationError("classification candidate is invalid")
    if not set(record["route_candidates"]).issubset(config["dispositions"]):
        raise PilotValidationError("route candidate is invalid")
    expected_path = _expected_record_path(
        config,
        "improvement_candidate",
        record["candidate_id"],
        record["candidate_version"],
    )
    if path != expected_path:
        raise PilotValidationError("record path does not match Candidate identity")
    source = record["source_identity"]
    _require_exact_fields(
        source,
        ("kind", "source_id", "source_version", "path", "sha256"),
        "source identity",
    )
    if (
        source["kind"] != "observation"
        or not isinstance(source["source_id"], str)
        or not source["source_id"].startswith("OBS-")
        or source["source_version"] != 1
    ):
        raise PilotValidationError("source reference identity is invalid")
    _validate_file_reference(
        {"path": source["path"], "sha256": source["sha256"]},
        project_root,
        "source reference",
    )
    if not isinstance(record["evidence_refs"], list) or not record[
        "evidence_refs"
    ]:
        raise PilotValidationError("Evidence references are invalid")
    for reference in record["evidence_refs"]:
        _validate_file_reference(reference, project_root, "Evidence reference")
    _validate_content_digest(record)
    return ValidationResult(
        record_kind=record["record_kind"],
        record_id=record["candidate_id"],
        content_digest=record["content_digest"],
    )


def validate_triage_decision(record, *, path, project_root, config):
    _require_exact_fields(
        record,
        config["record_fields"]["human_triage_decision"],
        "Human Triage Decision",
    )
    if record["record_kind"] != "human_triage_decision":
        raise PilotValidationError("record kind is invalid")
    if record["schema_version"] != 1:
        raise PilotValidationError("schema version is invalid")
    if (
        not isinstance(record["decision_id"], str)
        or not _DECISION_ID.fullmatch(record["decision_id"])
        or record["decision_version"] != 1
        or not isinstance(record["decided_at"], str)
        or not _TIMESTAMP.fullmatch(record["decided_at"])
    ):
        raise PilotValidationError("Decision identity is invalid")
    expected_path = _expected_record_path(
        config,
        "human_triage_decision",
        record["decision_id"],
        record["decision_version"],
    )
    if path != expected_path:
        raise PilotValidationError("record path does not match Decision identity")
    candidate_ref = record["candidate_ref"]
    _require_exact_fields(
        candidate_ref,
        (
            "candidate_id",
            "candidate_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "candidate reference",
    )
    candidate_path = _validate_file_reference(
        {"path": candidate_ref["path"], "sha256": candidate_ref["sha256"]},
        project_root,
        "candidate reference",
    )
    candidate = _load_json(candidate_path, "referenced Candidate")
    validate_candidate(
        candidate,
        path=candidate_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        candidate_ref["candidate_id"] != candidate["candidate_id"]
        or candidate_ref["candidate_version"]
        != candidate["candidate_version"]
        or candidate_ref["content_digest"] != candidate["content_digest"]
    ):
        raise PilotValidationError("candidate reference identity is stale")
    if record["decision_maker"] != "human":
        raise PilotValidationError("Human decision is required")
    if record["disposition"] not in config["dispositions"]:
        raise PilotValidationError("disposition is invalid")
    if not isinstance(record["blocking"], bool):
        raise PilotValidationError("blocking decision is invalid")
    for field in ("rationale", "selected_consumer", "next_action"):
        _require_text(record[field])
    promotion = record["issue_promotion"]
    _require_exact_fields(promotion, ("approved", "issue_id"), "Issue promotion")
    if record["disposition"] == "issue_resolution":
        if (
            promotion["approved"] is not True
            or not isinstance(promotion["issue_id"], str)
            or not _ISSUE_ID.fullmatch(promotion["issue_id"])
        ):
            raise PilotValidationError("Issue promotion is inconsistent")
    elif promotion != {"approved": False, "issue_id": None}:
        raise PilotValidationError("Issue promotion is inconsistent")
    _validate_content_digest(record)
    return ValidationResult(
        record_kind=record["record_kind"],
        record_id=record["decision_id"],
        content_digest=record["content_digest"],
    )


def validate_issue(record, *, path, project_root, config):
    if "issue_record" not in config["record_fields"]:
        raise PilotValidationError("Issue Record is unavailable in this config")
    _require_exact_fields(
        record,
        config["record_fields"]["issue_record"],
        "Issue Record",
    )
    if record["record_kind"] != "issue_record":
        raise PilotValidationError("record kind is invalid")
    if record["schema_version"] != 1:
        raise PilotValidationError("schema version is invalid")
    if (
        not isinstance(record["issue_id"], str)
        or not _ISSUE_ID.fullmatch(record["issue_id"])
        or record["issue_version"] != 1
        or not isinstance(record["created_at"], str)
        or not _TIMESTAMP.fullmatch(record["created_at"])
    ):
        raise PilotValidationError("Issue identity is invalid")
    source = record["source_identity"]
    _require_exact_fields(
        source,
        ("kind", "source_id", "source_version", "path", "sha256"),
        "source identity",
    )
    if (
        source["kind"] != "observation"
        or not isinstance(source["source_id"], str)
        or not source["source_id"].startswith("OBS-")
        or source["source_version"] != 1
    ):
        raise PilotValidationError("source reference identity is invalid")
    _validate_file_reference(
        {"path": source["path"], "sha256": source["sha256"]},
        project_root,
        "source reference",
    )
    candidate_ref = record["candidate_ref"]
    _require_exact_fields(
        candidate_ref,
        (
            "candidate_id",
            "candidate_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "candidate reference",
    )
    candidate_path = _validate_file_reference(
        {"path": candidate_ref["path"], "sha256": candidate_ref["sha256"]},
        project_root,
        "candidate reference",
    )
    candidate = _load_json(candidate_path, "referenced Candidate")
    validate_candidate(
        candidate,
        path=candidate_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        candidate_ref["candidate_id"] != candidate["candidate_id"]
        or candidate_ref["candidate_version"]
        != candidate["candidate_version"]
        or candidate_ref["content_digest"] != candidate["content_digest"]
        or source != candidate["source_identity"]
    ):
        raise PilotValidationError("candidate reference identity is stale")
    decision_ref = record["triage_decision_ref"]
    _require_exact_fields(
        decision_ref,
        (
            "decision_id",
            "decision_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "triage decision reference",
    )
    decision_path = _validate_file_reference(
        {"path": decision_ref["path"], "sha256": decision_ref["sha256"]},
        project_root,
        "triage decision reference",
    )
    decision = _load_json(decision_path, "referenced Triage Decision")
    validate_triage_decision(
        decision,
        path=decision_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        decision_ref["decision_id"] != decision["decision_id"]
        or decision_ref["decision_version"] != decision["decision_version"]
        or decision_ref["content_digest"] != decision["content_digest"]
    ):
        raise PilotValidationError("triage decision reference identity is stale")
    promotion = decision["issue_promotion"]
    if (
        decision["disposition"] != "issue_resolution"
        or promotion["approved"] is not True
        or promotion["issue_id"] != record["issue_id"]
        or decision["candidate_ref"]["candidate_id"]
        != candidate_ref["candidate_id"]
        or decision["candidate_ref"]["content_digest"]
        != candidate_ref["content_digest"]
    ):
        raise PilotValidationError("Issue promotion is not Human-approved")
    expected_path = _expected_record_path(
        config,
        "issue_record",
        record["issue_id"],
        record["issue_version"],
    )
    if path != expected_path:
        raise PilotValidationError("record path does not match Issue identity")
    for field in (
        "source_work",
        "problem",
        "motivation",
        "owner_candidate",
        "route_candidate",
    ):
        _require_text(record[field])
    for field in (
        "impact",
        "scope",
        "non_scope",
        "related_files",
        "related_units",
    ):
        _require_text_list(record[field], field)
    for related_file in record["related_files"]:
        _safe_relative_path(related_file)
    if not isinstance(record["evidence_refs"], list) or not record[
        "evidence_refs"
    ]:
        raise PilotValidationError("Evidence references are invalid")
    for reference in record["evidence_refs"]:
        _validate_file_reference(reference, project_root, "Evidence reference")
    _validate_content_digest(record)
    return ValidationResult(
        record_kind=record["record_kind"],
        record_id=record["issue_id"],
        content_digest=record["content_digest"],
    )


def _structured_ids(records, id_field, label):
    identifiers = []
    for record in records:
        _require_text(record[id_field])
        identifiers.append(record[id_field])
    if len(identifiers) != len(set(identifiers)):
        raise PilotValidationError(f"{label} IDs are duplicated")
    return set(identifiers)


def validate_resolution_plan(record, *, path, project_root, config):
    if "issue_resolution_plan" not in config["record_fields"]:
        raise PilotValidationError(
            "Issue Resolution Plan is unavailable in this config"
        )
    _require_exact_fields(
        record,
        config["record_fields"]["issue_resolution_plan"],
        "Issue Resolution Plan",
    )
    if record["record_kind"] != "issue_resolution_plan":
        raise PilotValidationError("record kind is invalid")
    if record["schema_version"] != 1:
        raise PilotValidationError("schema version is invalid")
    if (
        not isinstance(record["plan_id"], str)
        or not _PLAN_ID.fullmatch(record["plan_id"])
        or not isinstance(record["plan_version"], int)
        or isinstance(record["plan_version"], bool)
        or record["plan_version"] < 1
        or not isinstance(record["created_at"], str)
        or not _TIMESTAMP.fullmatch(record["created_at"])
    ):
        raise PilotValidationError("Plan identity is invalid")
    issue_ref = record["issue_ref"]
    _require_exact_fields(
        issue_ref,
        (
            "issue_id",
            "issue_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "Issue reference",
    )
    issue_path = _validate_file_reference(
        {"path": issue_ref["path"], "sha256": issue_ref["sha256"]},
        project_root,
        "Issue reference",
    )
    issue = _load_json(issue_path, "referenced Issue")
    validate_issue(
        issue,
        path=issue_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        issue_ref["issue_id"] != issue["issue_id"]
        or issue_ref["issue_version"] != issue["issue_version"]
        or issue_ref["content_digest"] != issue["content_digest"]
    ):
        raise PilotValidationError("Issue reference identity is stale")
    expected_path = _expected_record_path(
        config,
        "issue_resolution_plan",
        record["plan_id"],
        record["plan_version"],
    )
    if path != expected_path:
        raise PilotValidationError("record path does not match Plan identity")
    _require_text(record["goal"])
    for field in (
        "scope",
        "non_scope",
        "prohibitions",
        "dependencies",
        "risks",
        "deployment",
        "recovery",
        "task_contract_route_candidates",
    ):
        _require_text_list(record[field], field)
    _require_structured_list(
        record["issue_obligations"],
        ("obligation_id", "statement", "source_field"),
        "issue obligations",
    )
    _require_structured_list(
        record["work_items"],
        (
            "work_item_id",
            "objective",
            "depends_on",
            "obligation_ids",
            "expected_outcome",
            "acceptance_ids",
            "oracle_ids",
            "rollback_step_ids",
        ),
        "work items",
    )
    _require_structured_list(
        record["acceptance"],
        ("acceptance_id", "criterion"),
        "Acceptance",
    )
    _require_structured_list(
        record["oracles"],
        ("oracle_id", "kind", "method", "expected"),
        "oracles",
    )
    _require_structured_list(
        record["rollback"],
        ("rollback_step_id", "trigger", "action", "verification"),
        "rollback",
    )
    obligation_ids = _structured_ids(
        record["issue_obligations"],
        "obligation_id",
        "issue obligations",
    )
    work_item_ids = _structured_ids(
        record["work_items"],
        "work_item_id",
        "work items",
    )
    acceptance_ids = _structured_ids(
        record["acceptance"],
        "acceptance_id",
        "Acceptance",
    )
    oracle_ids = _structured_ids(record["oracles"], "oracle_id", "oracles")
    rollback_ids = _structured_ids(
        record["rollback"],
        "rollback_step_id",
        "rollback",
    )
    covered_obligations = set()
    covered_acceptance = set()
    covered_oracles = set()
    covered_rollback = set()
    for obligation in record["issue_obligations"]:
        _require_text(obligation["statement"])
        _require_text(obligation["source_field"])
    for acceptance in record["acceptance"]:
        _require_text(acceptance["criterion"])
    for oracle in record["oracles"]:
        for field in ("kind", "method", "expected"):
            _require_text(oracle[field])
    for rollback in record["rollback"]:
        for field in ("trigger", "action", "verification"):
            _require_text(rollback[field])
    for work_item in record["work_items"]:
        _require_text(work_item["objective"])
        _require_text(work_item["expected_outcome"])
        _require_optional_text_list(work_item["depends_on"], "depends_on")
        for field in (
            "obligation_ids",
            "acceptance_ids",
            "oracle_ids",
            "rollback_step_ids",
        ):
            _require_text_list(work_item[field], field)
        referenced = {
            "depends_on": set(work_item["depends_on"]),
            "obligation_ids": set(work_item["obligation_ids"]),
            "acceptance_ids": set(work_item["acceptance_ids"]),
            "oracle_ids": set(work_item["oracle_ids"]),
            "rollback_step_ids": set(work_item["rollback_step_ids"]),
        }
        if (
            not referenced["depends_on"].issubset(work_item_ids)
            or work_item["work_item_id"] in referenced["depends_on"]
            or not referenced["obligation_ids"].issubset(obligation_ids)
            or not referenced["acceptance_ids"].issubset(acceptance_ids)
            or not referenced["oracle_ids"].issubset(oracle_ids)
            or not referenced["rollback_step_ids"].issubset(rollback_ids)
        ):
            raise PilotValidationError("Plan coverage reference is unknown")
        covered_obligations.update(referenced["obligation_ids"])
        covered_acceptance.update(referenced["acceptance_ids"])
        covered_oracles.update(referenced["oracle_ids"])
        covered_rollback.update(referenced["rollback_step_ids"])
    if (
        covered_obligations != obligation_ids
        or covered_acceptance != acceptance_ids
        or covered_oracles != oracle_ids
        or covered_rollback != rollback_ids
    ):
        raise PilotValidationError("Plan coverage is incomplete")
    if record["plan_version"] >= 2:
        work_items = {
            item["work_item_id"]: item
            for item in record["work_items"]
        }
        required_closure = (
            "OBL-006" in obligation_ids
            and "WI-006" in work_item_ids
            and "ACC-007" in acceptance_ids
            and "ORACLE-007" in oracle_ids
        )
        resolver = work_items.get("WI-006", {})
        projection = work_items.get("WI-003", {})
        if (
            not required_closure
            or resolver.get("obligation_ids") != ["OBL-006"]
            or resolver.get("acceptance_ids") != ["ACC-007"]
            or resolver.get("oracle_ids") != ["ORACLE-007"]
            or "WI-006" not in projection.get("depends_on", [])
        ):
            raise PilotValidationError(
                "Plan derived state closure is incomplete"
            )
        acceptance_by_id = {
            item["acceptance_id"]: item["criterion"]
            for item in record["acceptance"]
        }
        boundary = acceptance_by_id["ACC-002"]
        if (
            "12288 bytes合格" not in boundary
            or "12289 bytes拒否" not in boundary
        ):
            raise PilotValidationError("Plan Pilot boundary is incomplete")
        entrypoint = acceptance_by_id["ACC-005"]
        if (
            "link-only" not in entrypoint
            or "独立したTODO意味規則" not in entrypoint
            or "拒否" not in entrypoint
        ):
            raise PilotValidationError(
                "Plan entrypoint authority is incomplete"
            )
    if record["plan_version"] >= 3:
        states = (
            "task_contract_commit_pending",
            "implementation_ready",
            "implementation_in_progress",
        )
        acceptance_by_id = {
            item["acceptance_id"]: item["criterion"]
            for item in record["acceptance"]
        }
        transition = acceptance_by_id["ACC-007"]
        if (
            any(state not in transition for state in states)
            or [transition.index(state) for state in states]
            != sorted(transition.index(state) for state in states)
        ):
            raise PilotValidationError(
                "Plan pre-implementation state closure is incomplete"
            )
        oracle_by_id = {
            item["oracle_id"]: item
            for item in record["oracles"]
        }
        oracle = oracle_by_id["ORACLE-007"]
        oracle_text = f'{oracle["method"]} {oracle["expected"]}'
        if any(state not in oracle_text for state in states):
            raise PilotValidationError(
                "Plan pre-implementation state oracle is incomplete"
            )
        if not any(
            "containing commit" in prohibition
            and "WI-001" in prohibition
            for prohibition in record["prohibitions"]
        ):
            raise PilotValidationError(
                "Plan Task Contract commit gate is incomplete"
            )
    _validate_content_digest(record)
    return ValidationResult(
        record_kind=record["record_kind"],
        record_id=record["plan_id"],
        content_digest=record["content_digest"],
    )


def validate_plan_challenge(record, *, path, project_root, config):
    if "plan_challenge" not in config["record_fields"]:
        raise PilotValidationError("Plan Challenge is unavailable in this config")
    _require_exact_fields(
        record,
        config["record_fields"]["plan_challenge"],
        "Plan Challenge",
    )
    if record["record_kind"] != "plan_challenge":
        raise PilotValidationError("record kind is invalid")
    if record["schema_version"] != 1:
        raise PilotValidationError("schema version is invalid")
    if (
        not isinstance(record["challenge_id"], str)
        or not _CHALLENGE_ID.fullmatch(record["challenge_id"])
        or not isinstance(record["challenge_version"], int)
        or isinstance(record["challenge_version"], bool)
        or record["challenge_version"] < 1
        or not isinstance(record["created_at"], str)
        or not _TIMESTAMP.fullmatch(record["created_at"])
    ):
        raise PilotValidationError("Challenge identity is invalid")
    if record["reviewer_kind"] != "llm_semantic_analysis_with_human_gate":
        raise PilotValidationError("Challenge reviewer kind is invalid")
    if record["independence_status"] not in {
        "human_independent_review_pending",
        "independent_review_completed",
    }:
        raise PilotValidationError("Challenge independence status is invalid")
    issue_ref = record["issue_ref"]
    _require_exact_fields(
        issue_ref,
        (
            "issue_id",
            "issue_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "Issue reference",
    )
    issue_path = _validate_file_reference(
        {"path": issue_ref["path"], "sha256": issue_ref["sha256"]},
        project_root,
        "Issue reference",
    )
    issue = _load_json(issue_path, "referenced Issue")
    validate_issue(
        issue,
        path=issue_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        issue_ref["issue_id"] != issue["issue_id"]
        or issue_ref["issue_version"] != issue["issue_version"]
        or issue_ref["content_digest"] != issue["content_digest"]
    ):
        raise PilotValidationError("Issue reference identity is stale")
    plan_ref = record["plan_ref"]
    _require_exact_fields(
        plan_ref,
        (
            "plan_id",
            "plan_version",
            "path",
            "sha256",
            "content_digest",
        ),
        "Plan reference",
    )
    plan_path = _validate_file_reference(
        {"path": plan_ref["path"], "sha256": plan_ref["sha256"]},
        project_root,
        "Plan reference",
    )
    plan = _load_json(plan_path, "referenced Resolution Plan")
    validate_resolution_plan(
        plan,
        path=plan_ref["path"],
        project_root=project_root,
        config=config,
    )
    if (
        plan_ref["plan_id"] != plan["plan_id"]
        or plan_ref["plan_version"] != plan["plan_version"]
        or plan_ref["content_digest"] != plan["content_digest"]
        or plan["issue_ref"]["issue_id"] != issue_ref["issue_id"]
        or plan["issue_ref"]["content_digest"]
        != issue_ref["content_digest"]
    ):
        raise PilotValidationError("Plan reference identity is stale")
    expected_path = _expected_record_path(
        config,
        "plan_challenge",
        record["challenge_id"],
        record["challenge_version"],
    )
    if path != expected_path:
        raise PilotValidationError(
            "record path does not match Challenge identity"
        )
    _require_structured_list(
        record["criteria_results"],
        ("criterion_id", "verdict", "rationale"),
        "Plan Challenge criteria",
    )
    criteria = {}
    for result in record["criteria_results"]:
        criterion_id = result["criterion_id"]
        _require_text(criterion_id)
        if criterion_id in criteria:
            raise PilotValidationError("Plan Challenge criteria are duplicated")
        if result["verdict"] not in {"pass", "warn", "block"}:
            raise PilotValidationError("Plan Challenge criterion verdict is invalid")
        _require_text(result["rationale"])
        criteria[criterion_id] = result["verdict"]
    if set(criteria) != _PLAN_CHALLENGE_CRITERIA:
        raise PilotValidationError("Plan Challenge criteria are incomplete")
    if not isinstance(record["findings"], list):
        raise PilotValidationError("Plan Challenge findings are invalid")
    findings = {}
    for finding in record["findings"]:
        _require_exact_fields(
            finding,
            (
                "finding_id",
                "severity",
                "criterion_id",
                "statement",
                "required_action",
            ),
            "Plan Challenge Finding",
        )
        finding_id = finding["finding_id"]
        _require_text(finding_id)
        if finding_id in findings:
            raise PilotValidationError("Plan Challenge Finding IDs are duplicated")
        if finding["severity"] not in {"blocking", "warning", "note"}:
            raise PilotValidationError("Plan Challenge Finding severity is invalid")
        if finding["criterion_id"] not in criteria:
            raise PilotValidationError("Plan Challenge Finding criterion is unknown")
        _require_text(finding["statement"])
        _require_text(finding["required_action"])
        findings[finding_id] = finding
    _require_optional_text_list(
        record["blocking_finding_ids"],
        "blocking_finding_ids",
    )
    blocking_ids = {
        finding_id
        for finding_id, finding in findings.items()
        if finding["severity"] == "blocking"
    }
    if set(record["blocking_finding_ids"]) != blocking_ids:
        raise PilotValidationError("blocking Finding identity is inconsistent")
    blocking_criteria = {
        criterion_id
        for criterion_id, verdict in criteria.items()
        if verdict == "block"
    }
    finding_blocking_criteria = {
        findings[finding_id]["criterion_id"]
        for finding_id in blocking_ids
    }
    if blocking_criteria != finding_blocking_criteria:
        raise PilotValidationError("blocking Finding does not cover block criteria")
    if not isinstance(record["stale_binding"], bool):
        raise PilotValidationError("stale binding value is invalid")
    if record["human_decision_required"] is not True:
        raise PilotValidationError("Human decision is required")
    expected_verdict = (
        "changes_required"
        if blocking_ids or record["stale_binding"]
        else "ready_for_human_approval"
    )
    if record["overall_verdict"] != expected_verdict:
        raise PilotValidationError("Plan Challenge overall verdict is inconsistent")
    _require_text(record["next_action"])
    _validate_content_digest(record)
    return ValidationResult(
        record_kind=record["record_kind"],
        record_id=record["challenge_id"],
        content_digest=record["content_digest"],
    )


def validate_record_file(path, *, project_root, config):
    project_root = Path(project_root)
    path = Path(path)
    absolute_path = path if path.is_absolute() else project_root / path
    record = _load_json(absolute_path, "Pilot record")
    try:
        relative_path = absolute_path.relative_to(project_root).as_posix()
    except ValueError as error:
        raise PilotValidationError("record path escapes project root") from error
    if record.get("record_kind") == "improvement_candidate":
        return validate_candidate(
            record,
            path=relative_path,
            project_root=project_root,
            config=config,
        )
    if record.get("record_kind") == "human_triage_decision":
        return validate_triage_decision(
            record,
            path=relative_path,
            project_root=project_root,
            config=config,
        )
    if record.get("record_kind") == "issue_record":
        return validate_issue(
            record,
            path=relative_path,
            project_root=project_root,
            config=config,
        )
    if record.get("record_kind") == "issue_resolution_plan":
        return validate_resolution_plan(
            record,
            path=relative_path,
            project_root=project_root,
            config=config,
        )
    if record.get("record_kind") == "plan_challenge":
        return validate_plan_challenge(
            record,
            path=relative_path,
            project_root=project_root,
            config=config,
        )
    raise PilotValidationError("unknown Pilot record kind")


def validate_todo_projection(document, *, known_ids, config):
    todo = config["todo_projection"]
    for marker in todo["forbidden_document_markers"]:
        if marker in document:
            raise PilotValidationError("detailed rework history is prohibited")
    heading = todo["heading"]
    if document.count(heading) != 1:
        raise PilotValidationError("active ID projection heading is missing or duplicated")
    section = document.split(heading, 1)[1]
    next_heading = re.search(r"\n## ", section)
    if next_heading is not None:
        section = section[: next_heading.start()]
    if len(section.encode("utf-8")) > todo["maximum_section_bytes"]:
        raise PilotValidationError("active ID projection exceeds byte limit")
    for marker in todo["forbidden_section_markers"]:
        if marker in section:
            raise PilotValidationError("active ID projection contains detailed content")
    bullets = [line for line in section.splitlines() if line.startswith("- ")]
    if bullets == ["- なし"]:
        return ()
    if not bullets or len(bullets) > todo["maximum_entries"]:
        raise PilotValidationError("active ID projection entry count is invalid")
    record_ids = []
    for line in bullets:
        match = _ACTIVE_ENTRY.fullmatch(line)
        if match is None:
            raise PilotValidationError("active ID projection entry is invalid")
        record_id = match.group("record_id")
        if record_id not in known_ids:
            raise PilotValidationError("unknown active ID")
        record_ids.append(record_id)
    if len(record_ids) != len(set(record_ids)):
        raise PilotValidationError("active ID projection contains duplicate IDs")
    return tuple(record_ids)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config/development-issue-resolution-pilot.json",
    )
    parser.add_argument("--project-root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("path")
    todo_parser = subparsers.add_parser("todo")
    todo_parser.add_argument("path")
    todo_parser.add_argument("--known-id", action="append", default=[])
    subparsers.add_parser("bootstrap")
    contract_parser = subparsers.add_parser("task-contract")
    contract_parser.add_argument("path")
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    config = load_config(project_root / args.config)
    if args.command == "record":
        result = validate_record_file(
            args.path,
            project_root=project_root,
            config=config,
        )
        output = dataclasses.asdict(result)
    elif args.command == "todo":
        document = (project_root / args.path).read_text(encoding="utf-8")
        output = {
            "active_ids": validate_todo_projection(
                document,
                known_ids=set(args.known_id),
                config=config,
            )
        }
    elif args.command == "bootstrap":
        validate_bootstrap_layout(
            project_root=project_root,
            config=config,
        )
        output = {"status": "passed"}
    else:
        output = {
            "fixed_source_count": validate_task_contract_sources(
                args.path,
                project_root=project_root,
            )
        }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
