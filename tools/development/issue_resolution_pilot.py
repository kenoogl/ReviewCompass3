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
        or config["pilot_version"] != 1
        or config["pilot_mode"] != "development_only_provisional"
        or config["maximum_issue_subjects"] != 1
    ):
        raise PilotValidationError("Pilot identity or scope is invalid")
    if set(config["directories"]) != {
        "improvement_candidate",
        "human_triage_decision",
    }:
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
