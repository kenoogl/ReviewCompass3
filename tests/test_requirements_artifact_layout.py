"""Work 3 Requirements artifact配置とauthority結線のAcceptance Test。"""

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    PROJECT_ROOT
    / "schemas/requirements/rc3-requirement-artifacts--v1.schema.json"
)
FIXTURE_PATH = (
    PROJECT_ROOT
    / "tests/fixtures/requirements/artifact-layout/valid-artifacts.json"
)
LEGACY_INVENTORY_PATH = (
    PROJECT_ROOT
    / "records/requirements/authority/rc3-legacy-requirements-37--v1.json"
)
EXPECTED_DIRECTORIES = (
    "records/requirements/definitions",
    "records/requirements/candidates",
    "records/requirements/decisions",
    "records/requirements/evidence",
    "records/requirements/authority",
    "schemas/requirements",
)
EXPECTED_REQUIREMENT_IDS = (
    "REQ-CONTEXT-001",
    "REQ-CONTEXT-002",
    "REQ-CONTEXT-003",
    "REQ-CONTEXT-004",
    "REQ-CONTEXT-005",
    "REQ-CONTEXT-006",
    "REQ-CONTEXT-007",
    "REQ-EVAL-001",
    "REQ-EVAL-002",
    "REQ-EVAL-003",
    "REQ-EXEC-001",
    "REQ-EXEC-002",
    "REQ-EXEC-003",
    "REQ-EXEC-004",
    "REQ-EXEC-005",
    "REQ-EXEC-006",
    "REQ-IMPROVE-001",
    "REQ-IMPROVE-002",
    "REQ-PORTABLE-001",
    "REQ-PORTABLE-002",
    "REQ-PORTABLE-003",
    "REQ-PORTABLE-004",
    "REQ-SESSION-001",
    "REQ-SESSION-002",
    "REQ-SESSION-003",
    "REQ-TRACE-001",
    "REQ-TRACE-002",
    "REQ-TRACE-003",
    "REQ-TRACE-004",
    "REQ-TRACE-005",
    "REQ-TRIAGE-001",
    "REQ-TRIAGE-002",
    "REQ-TRIAGE-003",
    "REQ-WORKFLOW-001",
    "REQ-WORKFLOW-002",
    "REQ-WORKFLOW-003",
    "REQ-WORKFLOW-004",
)
DIGEST_FIELDS = {
    "requirement_definition": "canonical_payload_digest",
    "requirements_candidate_manifest": "candidate_digest",
    "requirements_decision_record": "record_digest",
    "requirements_evidence_record": "evidence_digest",
    "requirements_authority_bundle": "bundle_digest",
}


@pytest.fixture
def layout():
    return importlib.import_module(
        "tools.requirements.artifact_layout"
    )


def _digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _seal(record):
    value = copy.deepcopy(record)
    digest_field = DIGEST_FIELDS[value["artifact_kind"]]
    payload = {
        key: item
        for key, item in value.items()
        if key != digest_field
    }
    value[digest_field] = _digest(payload)
    return value


def _ref(logical_id, version, path, sha256):
    return {
        "logical_id": logical_id,
        "version": version,
        "path": path,
        "sha256": sha256,
    }


def _fixture_records():
    source_digest = hashlib.sha256(
        (
            PROJECT_ROOT
            / "docs/requirements/2026-08-02-task-contract-requirements-delta.md"
        ).read_bytes()
    ).hexdigest()
    schema_digest = hashlib.sha256(
        SCHEMA_PATH.read_bytes()
    ).hexdigest()
    records = json.loads(FIXTURE_PATH.read_text())

    definition = records["definition"]
    definition["source_refs"][0]["sha256"] = source_digest
    definition = _seal(definition)
    definition_ref = _ref(
        definition["record_id"],
        definition["requirement_version"],
        "records/requirements/definitions/req-contract-001--v1.json",
        definition["canonical_payload_digest"],
    )

    evidence = records["evidence"]
    evidence["subject_refs"] = [definition_ref]
    evidence["source_refs"][0]["sha256"] = source_digest
    evidence = _seal(evidence)
    evidence_ref = _ref(
        evidence["evidence_id"],
        evidence["evidence_version"],
        "records/requirements/evidence/rc3-requirements-added-13-evidence-2026-08-03-v1.json",
        evidence["evidence_digest"],
    )

    candidate = records["candidate"]
    candidate["definition_refs"] = [definition_ref]
    candidate["schema_refs"][0]["sha256"] = schema_digest
    candidate["fixed_source_refs"][0]["sha256"] = source_digest
    candidate = _seal(candidate)
    candidate_ref = _ref(
        candidate["candidate_id"],
        candidate["candidate_version"],
        "records/requirements/candidates/rc3-requirements-added-13-2026-08-03-v1.json",
        candidate["candidate_digest"],
    )

    decision = records["decision"]
    decision["target_candidate_digest"] = candidate["candidate_digest"]
    decision["evidence_refs"] = [evidence_ref]
    decision = _seal(decision)
    decision_ref = _ref(
        decision["decision_id"],
        decision["decision_version"],
        "records/requirements/decisions/dec-requirements-added-13-2026-08-03-v1.json",
        decision["record_digest"],
    )

    authority_bundle = records["authority_bundle"]
    authority_bundle["definition_refs"] = [definition_ref]
    authority_bundle["decision_refs"] = [decision_ref]
    authority_bundle["evidence_refs"] = [evidence_ref]
    authority_bundle = _seal(authority_bundle)

    return {
        "definition": definition,
        "candidate": candidate,
        "decision": decision,
        "evidence": evidence,
        "authority_bundle": authority_bundle,
        "candidate_ref": candidate_ref,
    }


def test_approved_directories_schema_and_non_authority_notice_exist(layout):
    for relative_path in EXPECTED_DIRECTORIES:
        assert (PROJECT_ROOT / relative_path).is_dir()

    schema = layout.load_schema(SCHEMA_PATH)

    assert schema["$id"] == "urn:reviewcompass3:requirements:artifacts:v1"
    assert {
        "requirement_definition",
        "requirements_candidate_manifest",
        "requirements_decision_record",
        "requirements_evidence_record",
        "requirements_authority_bundle",
    } <= set(schema["$defs"])
    notice = (
        PROJECT_ROOT / "records/requirements/README.md"
    ).read_text()
    assert "directory names do not confer authority" in notice


def test_validates_minimum_artifacts_and_resolves_authority(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    records = _fixture_records()
    expected_paths = {
        "definition": "records/requirements/definitions/req-contract-001--v1.json",
        "candidate": "records/requirements/candidates/rc3-requirements-added-13-2026-08-03-v1.json",
        "decision": "records/requirements/decisions/dec-requirements-added-13-2026-08-03-v1.json",
        "evidence": "records/requirements/evidence/rc3-requirements-added-13-evidence-2026-08-03-v1.json",
        "authority_bundle": "records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json",
    }

    for name, path in expected_paths.items():
        result = layout.validate_artifact(
            records[name],
            schema=schema,
            path=path,
        )
        assert result.status == "valid"

    authority = layout.resolve_authority_chain(
        definitions=(records["definition"],),
        candidate=records["candidate"],
        decisions=(records["decision"],),
        evidence=(records["evidence"],),
        authority_bundle=records["authority_bundle"],
        schema=schema,
    )

    assert authority.status == "effective"
    assert authority.requirement_ids == ("REQ-CONTRACT-001",)


@pytest.mark.parametrize(
    "mutation",
    (
        "missing_statement",
        "record_id_mismatch",
        "digest_mismatch",
        "unknown_field",
        "wrong_path",
    ),
)
def test_rejects_invalid_definition_shape_identity_or_locator(
    layout,
    mutation,
):
    schema = layout.load_schema(SCHEMA_PATH)
    definition = _fixture_records()["definition"]
    path = "records/requirements/definitions/req-contract-001--v1.json"

    if mutation == "missing_statement":
        definition.pop("statement")
        definition = _seal(definition)
    elif mutation == "record_id_mismatch":
        definition["record_id"] = "REQ-CONTRACT-001@v2"
        definition = _seal(definition)
    elif mutation == "digest_mismatch":
        definition["canonical_payload_digest"] = "0" * 64
    elif mutation == "unknown_field":
        definition["approved"] = True
        definition = _seal(definition)
    else:
        path = "records/requirements/definitions/current.json"

    with pytest.raises(layout.RequirementArtifactError):
        layout.validate_artifact(
            definition,
            schema=schema,
            path=path,
        )


def test_directory_or_definition_alone_does_not_confer_authority(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    records = _fixture_records()

    with pytest.raises(layout.RequirementArtifactError):
        layout.resolve_authority_chain(
            definitions=(records["definition"],),
            candidate=records["candidate"],
            decisions=(),
            evidence=(records["evidence"],),
            authority_bundle=records["authority_bundle"],
            schema=schema,
        )


def test_rejects_stale_candidate_or_evidence_binding(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    records = _fixture_records()
    records["decision"]["target_candidate_digest"] = "0" * 64
    records["decision"] = _seal(records["decision"])

    with pytest.raises(layout.RequirementArtifactError):
        layout.resolve_authority_chain(
            definitions=(records["definition"],),
            candidate=records["candidate"],
            decisions=(records["decision"],),
            evidence=(records["evidence"],),
            authority_bundle=records["authority_bundle"],
            schema=schema,
        )


def test_rejects_same_requirement_version_with_different_digest(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    records = _fixture_records()
    conflicting = copy.deepcopy(records["definition"])
    conflicting["statement"] = "異なるRequirement本文"
    conflicting = _seal(conflicting)

    with pytest.raises(layout.RequirementArtifactError):
        layout.resolve_authority_chain(
            definitions=(records["definition"], conflicting),
            candidate=records["candidate"],
            decisions=(records["decision"],),
            evidence=(records["evidence"],),
            authority_bundle=records["authority_bundle"],
            schema=schema,
        )


def test_validates_fixed_legacy_binding_inventory(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    inventory = json.loads(LEGACY_INVENTORY_PATH.read_text())

    result = layout.validate_legacy_binding_inventory(
        inventory,
        schema=schema,
        project_root=PROJECT_ROOT,
        expected_requirement_ids=EXPECTED_REQUIREMENT_IDS,
        path="records/requirements/authority/rc3-legacy-requirements-37--v1.json",
    )

    assert result.status == "valid"
    assert result.requirement_count == 37
    assert result.source_count == 6


def test_rejects_legacy_binding_after_source_digest_change(layout):
    schema = layout.load_schema(SCHEMA_PATH)
    inventory = json.loads(LEGACY_INVENTORY_PATH.read_text())
    inventory["legacy_authority_bindings"][0][
        "definition_source"
    ]["sha256"] = "0" * 64
    inventory = _seal(inventory)

    with pytest.raises(layout.RequirementArtifactError):
        layout.validate_legacy_binding_inventory(
            inventory,
            schema=schema,
            project_root=PROJECT_ROOT,
            expected_requirement_ids=EXPECTED_REQUIREMENT_IDS,
            path="records/requirements/authority/rc3-legacy-requirements-37--v1.json",
        )
