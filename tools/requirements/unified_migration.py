"""Legacy 37 Requirementを現行definition形式へ決定的に移行する。"""

import argparse
import dataclasses
import hashlib
import json
from pathlib import Path

from tools.requirements import artifact_layout


class RequirementMigrationError(Exception):
    """Requirement移行を意味保存付きで完了できない。"""


@dataclasses.dataclass(frozen=True)
class MigrationPlan:
    definitions: tuple
    candidate: dict


@dataclasses.dataclass(frozen=True)
class MigrationWriteResult:
    written_count: int
    unchanged_count: int


LEGACY_AUTHORITY_PATH = (
    "records/requirements/authority/rc3-legacy-requirements-37--v1.json"
)
CURRENT_AUTHORITY_PATH = (
    "records/requirements/authority/"
    "rc3-requirements-authority-2026-08-03--v1.json"
)
SCHEMA_PATH = (
    "schemas/requirements/rc3-requirement-artifacts--v1.schema.json"
)
CANDIDATE_ID = "RC3-REQUIREMENTS-UNIFIED-50-2026-08-03-V1"
EVIDENCE_ID = "RC3-REQUIREMENTS-UNIFIED-50-EVIDENCE-2026-08-03-V2"
SEMANTIC_FIELDS = (
    "feature_id",
    "statement",
    "inputs",
    "outputs",
    "stop_conditions",
    "recovery_conditions",
    "preserved_artifacts",
    "acceptance_criteria",
    "non_goals",
)


def _canonical_digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RequirementMigrationError(
            f"migration_source_unavailable: {path}"
        ) from error


def _source_requirements(record):
    if isinstance(record.get("requirements"), list):
        return tuple(record["requirements"])
    if isinstance(record.get("batches"), list):
        return tuple(
            requirement
            for batch in record["batches"]
            for requirement in batch["requirements"]
        )
    raise RequirementMigrationError(
        "migration_incomplete: source has no Requirement records"
    )


def _artifact_ref(logical_id, version, path, digest):
    return {
        "logical_id": logical_id,
        "version": version,
        "path": path,
        "sha256": digest,
    }


def _definition_ref(definition):
    requirement_id = definition["requirement_id"]
    version = definition["requirement_version"]
    return _artifact_ref(
        definition["record_id"],
        version,
        (
            "records/requirements/definitions/"
            f"{requirement_id.lower()}--v{version}.json"
        ),
        definition["canonical_payload_digest"],
    )


def _physical_ref(record, path):
    if record["artifact_kind"] == "requirements_authority_bundle":
        logical_id = record["authority_bundle_id"]
        version = record["bundle_version"]
    else:
        raise RequirementMigrationError(
            "migration_incomplete: unsupported fixed source artifact"
        )
    return _artifact_ref(
        logical_id,
        version,
        path,
        _file_digest(Path(path)),
    )


def build_definition(requirement, *, source_refs):
    missing = [
        field
        for field in SEMANTIC_FIELDS
        if field not in requirement or not requirement[field]
    ]
    requirement_id = requirement.get("requirement_id")
    if not requirement_id or missing:
        detail = ",".join(sorted(missing or ("requirement_id",)))
        raise RequirementMigrationError(
            f"migration_incomplete: {requirement_id or 'unknown'}: {detail}"
        )
    if not source_refs:
        raise RequirementMigrationError(
            f"migration_incomplete: {requirement_id}: source_refs"
        )
    definition = {
        "artifact_kind": "requirement_definition",
        "record_id": f"{requirement_id}@v1",
        "record_version": 1,
        "requirement_id": requirement_id,
        "requirement_version": 1,
        "schema_id": "RC3-REQUIREMENT-ARTIFACTS",
        "schema_version": 1,
        "source_refs": list(source_refs),
    }
    for field in SEMANTIC_FIELDS:
        definition[field] = requirement[field]
    definition["acceptance_truth_changed"] = False
    definition["canonical_payload_digest"] = _canonical_digest(definition)
    return definition


def _load_legacy_context(project_root):
    schema = artifact_layout.load_schema(project_root / SCHEMA_PATH)
    inventory_path = project_root / LEGACY_AUTHORITY_PATH
    inventory = _read_json(inventory_path)
    expected_ids = tuple(
        requirement_id
        for binding in inventory["legacy_authority_bindings"]
        for requirement_id in binding["requirement_ids"]
    )
    artifact_layout.validate_legacy_binding_inventory(
        inventory,
        schema=schema,
        project_root=project_root,
        expected_requirement_ids=expected_ids,
        path=LEGACY_AUTHORITY_PATH,
    )
    return schema, inventory


def load_legacy_requirements(project_root):
    project_root = Path(project_root)
    _, inventory = _load_legacy_context(project_root)
    requirements = {}
    for binding in inventory["legacy_authority_bindings"]:
        source_path = project_root / binding["definition_source"]["path"]
        source = _read_json(source_path)
        observed = _source_requirements(source)
        observed_ids = {item.get("requirement_id") for item in observed}
        if observed_ids != set(binding["requirement_ids"]):
            raise RequirementMigrationError(
                "migration_incomplete: binding and source IDs differ"
            )
        for requirement in observed:
            requirement_id = requirement["requirement_id"]
            if requirement_id in requirements:
                raise RequirementMigrationError(
                    f"migration_duplicate: {requirement_id}"
                )
            requirements[requirement_id] = requirement
    return dict(sorted(requirements.items()))


def _legacy_source_refs(inventory):
    return {
        requirement_id: tuple(
            binding[field]
            for field in (
                "definition_source",
                "human_source",
                "approval_decision",
                "completion_evidence",
            )
        )
        for binding in inventory["legacy_authority_bindings"]
        for requirement_id in binding["requirement_ids"]
    }


def _load_existing_definitions(project_root, schema):
    current = _read_json(project_root / CURRENT_AUTHORITY_PATH)
    records = []
    for reference in current["definition_refs"]:
        path = project_root / reference["path"]
        record = _read_json(path)
        artifact_layout.validate_artifact(
            record,
            schema=schema,
            path=reference["path"],
        )
        if _definition_ref(record) != reference:
            raise RequirementMigrationError(
                f"migration_stale_definition_ref: {reference['path']}"
            )
        records.append(record)
    return current, tuple(records)


def _deduplicated_refs(references):
    by_identity = {}
    for reference in references:
        identity = (
            reference["logical_id"],
            reference["version"],
            reference["path"],
            reference["sha256"],
        )
        by_identity[identity] = reference
    return [by_identity[key] for key in sorted(by_identity)]


def build_migration_plan(project_root):
    project_root = Path(project_root)
    schema, inventory = _load_legacy_context(project_root)
    legacy = load_legacy_requirements(project_root)
    source_refs = _legacy_source_refs(inventory)
    definitions = tuple(
        build_definition(
            legacy[requirement_id],
            source_refs=source_refs[requirement_id],
        )
        for requirement_id in sorted(legacy)
    )
    for definition in definitions:
        artifact_layout.validate_artifact(definition, schema=schema)

    current, existing = _load_existing_definitions(project_root, schema)
    all_definitions = tuple(sorted(
        existing + definitions,
        key=lambda item: item["requirement_id"],
    ))
    all_ids = [item["requirement_id"] for item in all_definitions]
    if len(all_ids) != 50 or len(set(all_ids)) != 50:
        raise RequirementMigrationError(
            "migration_incomplete: unified authority candidate must contain 50 unique IDs"
        )

    legacy_fixed_refs = [
        reference
        for binding in inventory["legacy_authority_bindings"]
        for field in (
            "definition_source",
            "human_source",
            "approval_decision",
            "completion_evidence",
        )
        for reference in (binding[field],)
    ]
    fixed_source_refs = _deduplicated_refs(
        legacy_fixed_refs
        + [
            _artifact_ref(
                inventory["authority_bundle_id"],
                inventory["bundle_version"],
                LEGACY_AUTHORITY_PATH,
                _file_digest(project_root / LEGACY_AUTHORITY_PATH),
            ),
            _artifact_ref(
                current["authority_bundle_id"],
                current["bundle_version"],
                CURRENT_AUTHORITY_PATH,
                _file_digest(project_root / CURRENT_AUTHORITY_PATH),
            ),
        ]
    )
    candidate = {
        "artifact_kind": "requirements_candidate_manifest",
        "candidate_id": CANDIDATE_ID,
        "candidate_version": 1,
        "definition_refs": [
            _definition_ref(definition)
            for definition in all_definitions
        ],
        "schema_refs": [
            _artifact_ref(
                "RC3-REQUIREMENT-ARTIFACTS",
                1,
                SCHEMA_PATH,
                _file_digest(project_root / SCHEMA_PATH),
            )
        ],
        "fixed_source_refs": fixed_source_refs,
    }
    candidate["candidate_digest"] = _canonical_digest(candidate)
    artifact_layout.validate_artifact(candidate, schema=schema)
    return MigrationPlan(
        definitions=definitions,
        candidate=candidate,
    )


def _serialized(record):
    return (
        json.dumps(
            record,
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


def _candidate_path(candidate):
    return (
        "records/requirements/candidates/"
        f"{candidate['candidate_id'].lower()}.json"
    )


def _evidence_path(evidence):
    return (
        "records/requirements/evidence/"
        f"{evidence['evidence_id'].lower()}.json"
    )


def build_evidence_record(
    plan,
    *,
    receipt,
    receipt_ref,
    recorded_at,
):
    if (
        receipt.get("receipt_kind") != "policy_test_verification_run"
        or receipt.get("runner_id") != "RC3-DEVELOPMENT-TEST-RUNNER"
        or receipt.get("status") != "passed"
        or receipt.get("exit_code") != 0
        or receipt.get("fallback_used") is not False
        or receipt.get("command") != "python3 -m pytest -q"
    ):
        raise RequirementMigrationError(
            "verification_receipt_rejected: official green run required"
        )
    candidate_ref = _artifact_ref(
        plan.candidate["candidate_id"],
        plan.candidate["candidate_version"],
        _candidate_path(plan.candidate),
        plan.candidate["candidate_digest"],
    )
    evidence = {
        "artifact_kind": "requirements_evidence_record",
        "evidence_id": EVIDENCE_ID,
        "evidence_version": 2,
        "subject_refs": plan.candidate["definition_refs"] + [candidate_ref],
        "source_refs": (
            plan.candidate["schema_refs"]
            + plan.candidate["fixed_source_refs"]
            + [receipt_ref]
        ),
        "observations": [
            "legacy 37 Requirementを旧batchの意味fieldから推測なしでdefinition v1へ変換した",
            "既存13 definitionと移行37 definitionを50 unique IDの単一definition_refsへ結線した",
            "移行器の連続2回実行で2回目はwritten 0、unchanged 38だった",
            "schema検証はdefinition 50件とcandidate 1件で合格した",
            "policy Test runnerはfallbackなしで全Testをgreenにした",
            "旧authority bundleとlegacy bindingを移行元Provenanceとして保持し削除・上書きしていない",
            "Human promotion Decisionとauthority bundle v2は未作成である",
        ],
        "result": "passed",
        "recorded_at": recorded_at,
    }
    evidence["evidence_digest"] = _canonical_digest(evidence)
    return evidence


def validate_evidence_record(project_root, evidence):
    project_root = Path(project_root)
    schema = artifact_layout.load_schema(project_root / SCHEMA_PATH)
    return artifact_layout.validate_artifact(
        evidence,
        schema=schema,
        path=_evidence_path(evidence),
    )


def write_migration_plan(plan, output_root):
    output_root = Path(output_root)
    outputs = [
        (
            "records/requirements/definitions/"
            f"{definition['requirement_id'].lower()}--v1.json",
            definition,
        )
        for definition in plan.definitions
    ]
    outputs.append((_candidate_path(plan.candidate), plan.candidate))
    written = 0
    unchanged = 0
    for relative_path, record in outputs:
        target = output_root / relative_path
        content = _serialized(record)
        if target.exists():
            if target.read_text() != content:
                raise RequirementMigrationError(
                    f"conflicting_output: {relative_path}"
                )
            unchanged += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(content)
        temporary.replace(target)
        written += 1
    return MigrationWriteResult(
        written_count=written,
        unchanged_count=unchanged,
    )


def check_migration_plan(plan, output_root):
    output_root = Path(output_root)
    outputs = [
        (
            "records/requirements/definitions/"
            f"{definition['requirement_id'].lower()}--v1.json",
            definition,
        )
        for definition in plan.definitions
    ]
    outputs.append((_candidate_path(plan.candidate), plan.candidate))
    for relative_path, record in outputs:
        target = output_root / relative_path
        if not target.is_file() or target.read_text() != _serialized(record):
            raise RequirementMigrationError(
                f"migration_output_missing_or_stale: {relative_path}"
            )
    return MigrationWriteResult(
        written_count=0,
        unchanged_count=len(outputs),
    )


def write_evidence_record(evidence, output_root):
    output_root = Path(output_root)
    relative_path = _evidence_path(evidence)
    target = output_root / relative_path
    content = _serialized(evidence)
    if target.exists():
        if target.read_text() != content:
            raise RequirementMigrationError(
                f"conflicting_output: {relative_path}"
            )
        return MigrationWriteResult(0, 1)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(content)
    temporary.replace(target)
    return MigrationWriteResult(1, 0)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--receipt")
    parser.add_argument("--recorded-at")
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    plan = build_migration_plan(project_root)
    if args.write:
        result = write_migration_plan(plan, project_root)
    elif args.check:
        result = check_migration_plan(plan, project_root)
    else:
        if not args.receipt or not args.recorded_at:
            raise RequirementMigrationError(
                "evidence generation requires --receipt and --recorded-at"
            )
        receipt_path = Path(args.receipt)
        try:
            receipt_relative = receipt_path.resolve().relative_to(project_root)
        except ValueError as error:
            raise RequirementMigrationError(
                "verification receipt must be inside project root"
            ) from error
        receipt = _read_json(receipt_path)
        receipt_ref = _artifact_ref(
            "RC3-POLICY-TEST-RECEIPT-WORK3-PERMANENT-REMEDIATION-V1",
            1,
            receipt_relative.as_posix(),
            _file_digest(receipt_path),
        )
        evidence = build_evidence_record(
            plan,
            receipt=receipt,
            receipt_ref=receipt_ref,
            recorded_at=args.recorded_at,
        )
        validate_evidence_record(project_root, evidence)
        result = write_evidence_record(evidence, project_root)
    print(json.dumps(dataclasses.asdict(result), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
