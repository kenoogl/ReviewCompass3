"""Requirements artifact schema、identity、authority結線の最小validator。"""

import dataclasses
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


class RequirementArtifactError(Exception):
    """Requirements artifactを安全に受理できない。"""


@dataclasses.dataclass(frozen=True)
class ArtifactValidation:
    status: str
    artifact_kind: str
    logical_id: str
    version: int
    digest: str


@dataclasses.dataclass(frozen=True)
class AuthorityResolution:
    status: str
    requirement_ids: tuple
    bundle_digest: str


@dataclasses.dataclass(frozen=True)
class LegacyInventoryValidation:
    status: str
    requirement_count: int
    source_count: int
    digest: str


_ARTIFACT_DEFINITIONS = {
    "requirement_definition": "requirement_definition",
    "requirements_candidate_manifest": "requirements_candidate_manifest",
    "requirements_decision_record": "requirements_decision_record",
    "requirements_evidence_record": "requirements_evidence_record",
    "requirements_authority_bundle": "requirements_authority_bundle",
}
_DIGEST_FIELDS = {
    "requirement_definition": "canonical_payload_digest",
    "requirements_candidate_manifest": "candidate_digest",
    "requirements_decision_record": "record_digest",
    "requirements_evidence_record": "evidence_digest",
    "requirements_authority_bundle": "bundle_digest",
}


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


def _schema_error(location, message):
    raise RequirementArtifactError(
        f"{location}: {message}"
    )


def _resolve_ref(schema, reference):
    prefix = "#/$defs/"
    if not isinstance(reference, str) or not reference.startswith(prefix):
        raise RequirementArtifactError(
            "schema contains an unsupported reference"
        )
    name = reference[len(prefix):]
    try:
        return schema["$defs"][name]
    except KeyError as error:
        raise RequirementArtifactError(
            f"schema reference does not resolve: {reference}"
        ) from error


def _validate_schema_value(value, definition, schema, location):
    if "$ref" in definition:
        _validate_schema_value(
            value,
            _resolve_ref(schema, definition["$ref"]),
            schema,
            location,
        )
        return
    if "const" in definition and value != definition["const"]:
        _schema_error(location, "const value mismatch")
    if "enum" in definition and value not in definition["enum"]:
        _schema_error(location, "value is outside the closed set")

    expected_type = definition.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            _schema_error(location, "must be an object")
        required = set(definition.get("required", ()))
        properties = definition.get("properties", {})
        missing = required - set(value)
        if missing:
            _schema_error(
                location,
                "missing fields: " + ", ".join(sorted(missing)),
            )
        if definition.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                _schema_error(
                    location,
                    "unknown fields: " + ", ".join(sorted(extra)),
                )
        for key, item in value.items():
            if key in properties:
                _validate_schema_value(
                    item,
                    properties[key],
                    schema,
                    f"{location}.{key}",
                )
        return
    if expected_type == "array":
        if not isinstance(value, list):
            _schema_error(location, "must be an array")
        if len(value) < definition.get("minItems", 0):
            _schema_error(location, "contains too few items")
        if definition.get("uniqueItems"):
            identities = tuple(
                json.dumps(
                    item,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                for item in value
            )
            if len(set(identities)) != len(identities):
                _schema_error(location, "contains duplicate items")
        item_definition = definition.get("items")
        if item_definition is not None:
            for index, item in enumerate(value):
                _validate_schema_value(
                    item,
                    item_definition,
                    schema,
                    f"{location}[{index}]",
                )
        return
    if expected_type == "string":
        if not isinstance(value, str):
            _schema_error(location, "must be a string")
        if len(value) < definition.get("minLength", 0):
            _schema_error(location, "must not be empty")
        pattern = definition.get("pattern")
        if pattern is not None and re.fullmatch(pattern, value) is None:
            _schema_error(location, "does not match the fixed pattern")
        return
    if expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            _schema_error(location, "must be an integer")
        if value < definition.get("minimum", value):
            _schema_error(location, "is below the minimum")
        return
    if expected_type == "boolean" and not isinstance(value, bool):
        _schema_error(location, "must be a boolean")


def load_schema(path):
    schema_path = Path(path)
    try:
        schema = json.loads(schema_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RequirementArtifactError(
            f"cannot load Requirement artifact schema: {schema_path}"
        ) from error
    if (
        schema.get("$id")
        != "urn:reviewcompass3:requirements:artifacts:v1"
        or not isinstance(schema.get("$defs"), dict)
        or not set(_ARTIFACT_DEFINITIONS.values()).issubset(
            schema["$defs"]
        )
    ):
        raise RequirementArtifactError(
            "Requirement artifact schema identity or definitions are incomplete"
        )
    return schema


def _artifact_identity(record):
    kind = record["artifact_kind"]
    if kind == "requirement_definition":
        return (
            record["record_id"],
            record["requirement_version"],
            record["canonical_payload_digest"],
        )
    if kind == "requirements_candidate_manifest":
        return (
            record["candidate_id"],
            record["candidate_version"],
            record["candidate_digest"],
        )
    if kind == "requirements_decision_record":
        return (
            record["decision_id"],
            record["decision_version"],
            record["record_digest"],
        )
    if kind == "requirements_evidence_record":
        return (
            record["evidence_id"],
            record["evidence_version"],
            record["evidence_digest"],
        )
    return (
        record["authority_bundle_id"],
        record["bundle_version"],
        record["bundle_digest"],
    )


def _expected_path(record):
    kind = record["artifact_kind"]
    if kind == "requirement_definition":
        filename = (
            f"{record['requirement_id'].lower()}"
            f"--v{record['requirement_version']}.json"
        )
        return f"records/requirements/definitions/{filename}"
    if kind == "requirements_candidate_manifest":
        filename = f"{record['candidate_id'].lower()}.json"
        return f"records/requirements/candidates/{filename}"
    if kind == "requirements_decision_record":
        filename = f"{record['decision_id'].lower()}.json"
        return f"records/requirements/decisions/{filename}"
    if kind == "requirements_evidence_record":
        filename = f"{record['evidence_id'].lower()}.json"
        return f"records/requirements/evidence/{filename}"
    filename = (
        f"{record['authority_bundle_id'].lower()}"
        f"--v{record['bundle_version']}.json"
    )
    return f"records/requirements/authority/{filename}"


def _validate_relative_path(value):
    if not isinstance(value, str):
        raise RequirementArtifactError(
            "artifact path must be project-relative text"
        )
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or "\\" in value
    ):
        raise RequirementArtifactError(
            "artifact path escapes the project root"
        )


def _validate_refs(record):
    for key, value in record.items():
        if key.endswith("_refs") and isinstance(value, list):
            for reference in value:
                _validate_relative_path(reference["path"])
        if key == "legacy_authority_bindings":
            for binding in value:
                for field in (
                    "definition_source",
                    "human_source",
                    "approval_decision",
                    "completion_evidence",
                ):
                    _validate_relative_path(binding[field]["path"])


def validate_artifact(record, *, schema, path=None):
    if not isinstance(record, dict):
        raise RequirementArtifactError(
            "Requirement artifact must be an object"
        )
    kind = record.get("artifact_kind")
    if kind not in _ARTIFACT_DEFINITIONS:
        raise RequirementArtifactError(
            "Requirement artifact kind is unknown"
        )
    definition = schema["$defs"][_ARTIFACT_DEFINITIONS[kind]]
    _validate_schema_value(record, definition, schema, kind)
    _validate_refs(record)

    digest_field = _DIGEST_FIELDS[kind]
    payload = {
        key: value
        for key, value in record.items()
        if key != digest_field
    }
    actual_digest = _canonical_digest(payload)
    if record[digest_field] != actual_digest:
        raise RequirementArtifactError(
            f"{kind} digest does not match its canonical payload"
        )

    if kind == "requirement_definition":
        expected_record_id = (
            f"{record['requirement_id']}"
            f"@v{record['requirement_version']}"
        )
        if record["record_id"] != expected_record_id:
            raise RequirementArtifactError(
                "Requirement record_id does not match ID and version"
            )
    if kind == "requirements_authority_bundle" and not (
        record["definition_refs"]
        or record["legacy_authority_bindings"]
    ):
        raise RequirementArtifactError(
            "authority bundle requires definitions or legacy bindings"
        )
    if path is not None:
        _validate_relative_path(path)
        if path != _expected_path(record):
            raise RequirementArtifactError(
                "artifact locator does not match the approved naming rule"
            )

    logical_id, version, digest = _artifact_identity(record)
    return ArtifactValidation(
        status="valid",
        artifact_kind=kind,
        logical_id=logical_id,
        version=version,
        digest=digest,
    )


def _reference_identity(reference):
    return (
        reference["logical_id"],
        reference["version"],
        reference["sha256"],
    )


def _artifact_reference(record):
    logical_id, version, digest = _artifact_identity(record)
    return (
        logical_id,
        version,
        _expected_path(record),
        digest,
    )


def _record_reference_set(records):
    return {
        _artifact_reference(record)
        for record in records
    }


def _declared_reference_set(references):
    return {
        (
            reference["logical_id"],
            reference["version"],
            reference["path"],
            reference["sha256"],
        )
        for reference in references
    }


def resolve_authority_chain(
    *,
    definitions,
    candidate,
    decisions,
    evidence,
    authority_bundle,
    schema,
):
    definitions = tuple(definitions)
    decisions = tuple(decisions)
    evidence = tuple(evidence)
    if not definitions or not decisions or not evidence:
        raise RequirementArtifactError(
            "directory or definition alone does not confer authority"
        )
    for record in definitions:
        validate_artifact(record, schema=schema)
    validate_artifact(candidate, schema=schema)
    for record in decisions:
        validate_artifact(record, schema=schema)
    for record in evidence:
        validate_artifact(record, schema=schema)
    validate_artifact(authority_bundle, schema=schema)

    definition_keys = tuple(
        (
            record["requirement_id"],
            record["requirement_version"],
        )
        for record in definitions
    )
    if len(set(definition_keys)) != len(definition_keys):
        raise RequirementArtifactError(
            "same Requirement ID and version appears more than once"
        )
    definition_refs = _record_reference_set(definitions)
    if _declared_reference_set(candidate["definition_refs"]) != definition_refs:
        raise RequirementArtifactError(
            "candidate definitions do not match supplied definitions"
        )
    if (
        _declared_reference_set(authority_bundle["definition_refs"])
        != definition_refs
    ):
        raise RequirementArtifactError(
            "authority bundle definitions do not match candidate"
        )

    evidence_refs = _record_reference_set(evidence)
    if not definition_refs.issubset(
        _declared_reference_set(evidence[0]["subject_refs"])
    ):
        raise RequirementArtifactError(
            "Evidence does not cover every candidate definition"
        )
    approved = tuple(
        record
        for record in decisions
        if (
            record["decision_class"] == "requirements_promotion"
            and record["authority"] == "human"
            and record["outcome"] == "approved"
            and record["target_candidate_id"] == candidate["candidate_id"]
            and record["target_candidate_digest"]
            == candidate["candidate_digest"]
            and _declared_reference_set(record["evidence_refs"])
            == evidence_refs
        )
    )
    if len(approved) != 1:
        raise RequirementArtifactError(
            "exactly one matching Human promotion Decision is required"
        )
    if (
        _declared_reference_set(authority_bundle["decision_refs"])
        != _record_reference_set(approved)
        or _declared_reference_set(authority_bundle["evidence_refs"])
        != evidence_refs
    ):
        raise RequirementArtifactError(
            "authority bundle Decision or Evidence binding is stale"
        )

    return AuthorityResolution(
        status="effective",
        requirement_ids=tuple(sorted(
            record["requirement_id"]
            for record in definitions
        )),
        bundle_digest=authority_bundle["bundle_digest"],
    )


def _validate_file_reference(reference, project_root):
    relative_path = reference["path"]
    _validate_relative_path(relative_path)
    path = project_root / relative_path
    if not path.is_file():
        raise RequirementArtifactError(
            f"legacy source does not exist: {relative_path}"
        )
    if _file_digest(path) != reference["sha256"]:
        raise RequirementArtifactError(
            f"legacy source digest mismatch: {relative_path}"
        )
    return path


def _requirement_ids_from_record(path):
    value = json.loads(path.read_text())
    if isinstance(value.get("requirements"), list):
        return {
            item["requirement_id"]
            for item in value["requirements"]
        }
    if isinstance(value.get("batches"), list):
        return {
            item["requirement_id"]
            for batch in value["batches"]
            for item in batch["requirements"]
        }
    raise RequirementArtifactError(
        f"legacy definition source has no Requirement records: {path}"
    )


def validate_legacy_binding_inventory(
    inventory,
    *,
    schema,
    project_root,
    expected_requirement_ids,
    path,
):
    project_root = Path(project_root)
    validate_artifact(
        inventory,
        schema=schema,
        path=path,
    )
    bindings = inventory["legacy_authority_bindings"]
    if not bindings or inventory["definition_refs"]:
        raise RequirementArtifactError(
            "legacy inventory must use bindings rather than new definitions"
        )

    observed_ids = []
    observed_paths = set()
    approval_refs = set()
    completion_refs = set()
    for binding in bindings:
        requirement_ids = tuple(binding["requirement_ids"])
        observed_ids.extend(requirement_ids)
        definition_path = _validate_file_reference(
            binding["definition_source"],
            project_root,
        )
        human_path = _validate_file_reference(
            binding["human_source"],
            project_root,
        )
        _validate_file_reference(
            binding["approval_decision"],
            project_root,
        )
        _validate_file_reference(
            binding["completion_evidence"],
            project_root,
        )
        source_ids = _requirement_ids_from_record(definition_path)
        if set(requirement_ids) != source_ids:
            raise RequirementArtifactError(
                "legacy binding IDs do not match definition source"
            )
        human_text = human_path.read_text()
        if any(
            requirement_id not in human_text
            for requirement_id in requirement_ids
        ):
            raise RequirementArtifactError(
                "legacy human source omits a bound Requirement ID"
            )
        for field in (
            "definition_source",
            "human_source",
            "approval_decision",
            "completion_evidence",
        ):
            observed_paths.add(binding[field]["path"])
        approval_refs.add(_reference_identity(
            binding["approval_decision"]
        ))
        completion_refs.add(_reference_identity(
            binding["completion_evidence"]
        ))

    if (
        len(set(observed_ids)) != len(observed_ids)
        or set(observed_ids) != set(expected_requirement_ids)
    ):
        raise RequirementArtifactError(
            "legacy Requirement coverage is incomplete or duplicated"
        )
    if {
        _reference_identity(reference)
        for reference in inventory["decision_refs"]
    } != approval_refs:
        raise RequirementArtifactError(
            "legacy approval Decision binding is inconsistent"
        )
    if {
        _reference_identity(reference)
        for reference in inventory["evidence_refs"]
    } != completion_refs:
        raise RequirementArtifactError(
            "legacy completion Evidence binding is inconsistent"
        )

    return LegacyInventoryValidation(
        status="valid",
        requirement_count=len(observed_ids),
        source_count=len(observed_paths),
        digest=inventory["bundle_digest"],
    )
