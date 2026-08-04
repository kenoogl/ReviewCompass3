"""Work 4A v3 Reusable Routine Ledgerの最小identity chain。

正本設計：docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md
承認：DEC-WORK4A-REBUILD-DESIGN-003

外部DATA_ROOTのObservationとCandidate Runは、project内のObservation Attestationを
唯一の橋として参照する。BaselineとOperational Decisionはproject相対refだけを持ち、
外部fileが無くてもcurrent Baselineを検証できる。
"""

import ast
import dataclasses
import hashlib
import json
import re
from pathlib import Path


DIGEST_ALGORITHM = "sha256"
PROFILES = ("development", "runtime")
ROOT_KINDS = ("project", "data")
ROOT_SELECTORS = ("data",)
CHANGE_CLASSES = ("ordinary", "security", "authority", "irreversible")
REVALIDATION_REQUIRED_CLASSES = ("security", "authority", "irreversible")
DISPOSITION_CLASSES = ("reuse", "extend", "merge", "split", "new")
CONTINUITY_STATES = ("continuous_fresh", "content_diverged", "universe_diverged")
WORK_PREFIX = "work4a"
LEDGER_DIRECTORY = "reusable-routine-ledger"
BASELINE_PATTERN = re.compile(r"^ledger-baseline--v(\d+)\.json$")
POLICY_PATTERN = re.compile(r"^work4a-freshness-policy-v(\d+)\.json$")

VERIFICATION_OUTCOME_CLASSES = (
    "invalid_manifest",
    "unsafe_root",
    "unknown_root_kind",
    "path_traversal",
    "root_escape",
    "non_regular_file",
    "missing_record",
    "digest_mismatch",
    "content_digest_mismatch",
    "identity_mismatch",
    "unknown_field",
    "foreign_project_data",
    "unlinked_candidate",
    "content_identity_mismatch",
    "summary_vocabulary_violation",
    "decision_candidate_mismatch",
    "stale_observation_reuse",
    "immutable_violation",
    "baseline_series_broken",
    "policy_revalidation_required",
    "data_root_escape",
    "observation_tampered",
    "write_verification_failed",
    "partial_write_detected",
)

ANNOTATION_CLASSES = ("locator_unresolved", "locator_profile_mismatch")

_REFERENCE_FIELDS = (
    "root_kind",
    "record_kind",
    "record_id",
    "version",
    "relative_path",
    "digest_algorithm",
    "file_sha256",
    "content_digest",
)

_LOCATOR_FIELDS = (
    "root_kind",
    "root_selector",
    "profile",
    "project_id",
    "relative_path",
    "digest_algorithm",
    "file_sha256",
    "evidentiary_role",
)

_SCHEMA = {
    "work4a_source_universe": (
        ("record_kind", "schema_version", "digest_algorithm", "source_universe_id",
         "source_universe_version", "include_root", "include_glob", "excluded_roots",
         "path_encoding", "development_policy_ref", "content_digest"),
        (),
    ),
    "work4a_freshness_policy": (
        ("record_kind", "schema_version", "digest_algorithm", "policy_id", "policy_version",
         "change_class", "change_classes", "revalidation_required_classes",
         "disposition_classes", "verification_outcome_classes", "development_policy_ref",
         "content_digest"),
        (),
    ),
    "work4a_source_observation": (
        ("record_kind", "schema_version", "digest_algorithm", "snapshot_id", "source_content_id",
         "source_universe_id", "source_universe_version", "head", "tool_version", "captured_at",
         "files", "content_digest"),
        (),
    ),
    "work4a_candidate_run": (
        ("record_kind", "schema_version", "digest_algorithm", "candidate_run_id",
         "observation_snapshot_id", "source_content_id", "source_universe_id",
         "source_universe_version", "candidates", "content_digest"),
        (),
    ),
    "work4a_observation_attestation": (
        ("record_kind", "schema_version", "digest_algorithm", "attestation_id",
         "attestation_version", "project_id", "profile", "source_universe_id",
         "source_universe_version", "source_universe_ref", "policy_ref", "source_content_id",
         "observation", "candidate_run", "candidate_summary", "supersedes_attestation",
         "content_digest"),
        (),
    ),
    "work4a_operational_decision": (
        ("record_kind", "schema_version", "digest_algorithm", "decision_id", "attestation_ref",
         "approved_candidate_run_id", "approved_candidate_content_digest",
         "approved_source_content_id", "approved_targets", "human_id", "decided_at",
         "content_digest"),
        (),
    ),
    "work4a_ledger_entry": (
        ("record_kind", "schema_version", "digest_algorithm", "entry_id", "entry_version",
         "symbol_id", "responsibility", "side_effects", "disposition", "source_content_id",
         "decision_ref", "content_digest"),
        (),
    ),
    "work4a_ledger_relation": (
        ("record_kind", "schema_version", "digest_algorithm", "relation_id", "relation_version",
         "left_entry_id", "right_entry_id", "relation_kind", "rationale", "decision_ref",
         "content_digest"),
        (),
    ),
    "work4a_ledger_baseline": (
        ("record_kind", "schema_version", "digest_algorithm", "baseline_id", "baseline_version",
         "project_id", "source_universe_id", "source_universe_version", "source_content_id",
         "universe_ref", "policy_ref", "attestation_ref", "decision_ref", "prior_baseline_ref",
         "entry_refs", "relation_refs", "content_digest"),
        (),
    ),
    "work4a_historical_contract_status": (
        ("record_kind", "schema_version", "digest_algorithm", "contract_status_id",
         "status_version", "contract_ref", "creation_commit", "creation_policy_ref",
         "human_decision_id", "outcome", "permits_current_start", "content_digest"),
        (),
    ),
}


class V3ValidationError(Exception):
    """v3のfail-closed条件に触れた。"""

    def __init__(self, code, detail=None, classification="verification_outcome"):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail
        self.classification = classification


@dataclasses.dataclass(frozen=True)
class Universe:
    universe_id: str
    universe_version: int
    path: Path
    content_digest: str


@dataclasses.dataclass(frozen=True)
class Policy:
    policy_id: str
    policy_version: int
    path: Path
    content_digest: str


@dataclasses.dataclass(frozen=True)
class Observation:
    project_root: Path
    data_root: Path
    profile: str
    project_id: str
    path: Path
    snapshot_id: str
    source_content_id: str
    universe_id: str
    universe_version: int
    universe_path: Path
    policy_path: Path
    files: tuple


@dataclasses.dataclass(frozen=True)
class Candidates:
    observation: Observation
    path: Path
    candidate_run_id: str
    content_digest: str
    source_content_id: str
    symbol_ids: tuple
    symbol_id_list_digest: str
    candidate_count: int
    classification_counts: dict


@dataclasses.dataclass(frozen=True)
class Attestation:
    path: Path
    attestation_id: str
    content_digest: str
    source_content_id: str
    candidate_run_id: str
    candidate_content_digest: str


@dataclasses.dataclass(frozen=True)
class Decision:
    path: Path
    decision_id: str
    content_digest: str


@dataclasses.dataclass(frozen=True)
class Baseline:
    path: Path
    baseline_version: int
    entry_paths: tuple
    relation_paths: tuple


@dataclasses.dataclass(frozen=True)
class CurrentState:
    baseline_version: int
    path: Path
    source_content_id: str
    annotations: tuple


@dataclasses.dataclass(frozen=True)
class Continuity:
    state: str
    permits_baseline_advance: bool
    source_content_id: str
    annotations: tuple


@dataclasses.dataclass(frozen=True)
class HistoricalStatus:
    outcome: str
    permits_current_start: bool
    path: Path


def _canonical_bytes(value):
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def _digest(value):
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _content_digest(document):
    return _digest({key: value for key, value in document.items() if key != "content_digest"})


def _file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _serialize(document):
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _write_new(path, document, *, allow_identical=False):
    """new-onlyで書く。既存fileは上書きしない。書込み後に読み戻して照合する。"""

    path = Path(path)
    data = _serialize(document)
    if path.exists():
        if allow_identical and path.read_bytes() == data.encode("utf-8"):
            return path
        raise V3ValidationError("immutable_violation", str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(data, encoding="utf-8")
    temporary.replace(path)
    if _file_sha256(path) != hashlib.sha256(data.encode("utf-8")).hexdigest():
        raise V3ValidationError("write_verification_failed", str(path))
    return path


def validate_record_schema(document, *, record_kind):
    """閉じたschemaへ照合する。未知fieldと不足fieldを拒否する。"""

    if not isinstance(document, dict):
        raise V3ValidationError("identity_mismatch", record_kind)
    if document.get("record_kind") != record_kind:
        raise V3ValidationError("identity_mismatch", record_kind)
    known = _SCHEMA.get(record_kind)
    if known is None:
        raise V3ValidationError("identity_mismatch", record_kind)
    required, optional = known
    allowed = set(required) | set(optional)
    unknown = sorted(set(document) - allowed)
    if unknown:
        raise V3ValidationError("unknown_field", ",".join(unknown))
    missing = sorted(set(required) - set(document))
    if missing:
        raise V3ValidationError("identity_mismatch", ",".join(missing))
    if document.get("digest_algorithm") != DIGEST_ALGORITHM:
        raise V3ValidationError("identity_mismatch", "digest_algorithm")
    return document


def _read_record(path, *, record_kind=None):
    path = Path(path)
    if not path.exists():
        raise V3ValidationError("missing_record", str(path))
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise V3ValidationError("digest_mismatch", str(path)) from error
    if not isinstance(document, dict):
        raise V3ValidationError("identity_mismatch", str(path))
    if record_kind is not None:
        validate_record_schema(document, record_kind=record_kind)
    if "content_digest" in document and _content_digest(document) != document["content_digest"]:
        raise V3ValidationError("content_digest_mismatch", str(path))
    return document


def _read_manifest(project_root):
    path = Path(project_root).resolve() / ".reviewcompass" / "project-manifest.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise V3ValidationError("invalid_manifest", str(path)) from error
    if not isinstance(document, dict) or document.get("schema_version") != 2:
        raise V3ValidationError("invalid_manifest", "schema_version")
    if not isinstance(document.get("project_id"), str) or not document["project_id"]:
        raise V3ValidationError("invalid_manifest", "project_id")
    if not isinstance(document.get("artifact_roots"), dict):
        raise V3ValidationError("invalid_manifest", "artifact_roots")
    return document


def _artifact_root(project_root, name):
    root = Path(project_root).resolve()
    manifest = _read_manifest(root)
    relative = manifest["artifact_roots"].get(name)
    if not isinstance(relative, str) or not relative:
        raise V3ValidationError("invalid_manifest", name)
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise V3ValidationError("path_traversal", name)
    resolved = (root / relative).resolve()
    if resolved == root or root not in resolved.parents:
        raise V3ValidationError("unsafe_root", name)
    return resolved


def _ledger_root(project_root):
    return _artifact_root(project_root, "reuse") / LEDGER_DIRECTORY


def resolve_data_root(*, project_root, runtime_root, profile):
    """Layout v3の語彙でDATA_ROOTを解決する。root重なりはinvalid_layoutで停止する。"""

    root = Path(project_root).resolve()
    if profile not in PROFILES:
        raise V3ValidationError("unknown_root_kind", f"profile={profile}")
    runtime = Path(runtime_root)
    if not runtime.is_absolute():
        raise V3ValidationError("path_traversal", "runtime_root")
    resolved = runtime.resolve()
    if resolved == root or root in resolved.parents or resolved in root.parents:
        raise V3ValidationError("root_overlap", str(resolved), classification="invalid_layout")
    manifest = _read_manifest(root)
    return resolved / "projects" / manifest["project_id"] / profile / "data"


def build_project_ref(*, project_root, path, record_kind, record_id, version):
    """project相対refを作る。project外のpathは受け付けない。"""

    root = Path(project_root).resolve()
    target = Path(path)
    if target.is_symlink():
        raise V3ValidationError("non_regular_file", str(target))
    resolved = target.resolve()
    if root not in resolved.parents:
        raise V3ValidationError("root_escape", str(target))
    if not resolved.is_file():
        raise V3ValidationError("missing_record", str(target))
    reference = {
        "root_kind": "project",
        "record_kind": record_kind,
        "record_id": record_id,
        "version": version,
        "relative_path": resolved.relative_to(root).as_posix(),
        "digest_algorithm": DIGEST_ALGORITHM,
        "file_sha256": _file_sha256(resolved),
    }
    if resolved.suffix == ".json":
        document = json.loads(resolved.read_text(encoding="utf-8"))
        if isinstance(document, dict) and "content_digest" in document:
            reference["content_digest"] = document["content_digest"]
    return reference


def verify_project_ref(*, project_root, reference):
    """project refをP4の順序で検証する。"""

    root = Path(project_root).resolve()
    if not isinstance(reference, dict):
        raise V3ValidationError("identity_mismatch", "reference")
    unknown = sorted(set(reference) - set(_REFERENCE_FIELDS))
    if unknown:
        raise V3ValidationError("unknown_field", ",".join(unknown))
    if reference.get("root_kind") not in ROOT_KINDS:
        raise V3ValidationError("unknown_root_kind", str(reference.get("root_kind")))
    if reference["root_kind"] != "project":
        raise V3ValidationError("unknown_root_kind", "project ref required")
    if reference.get("digest_algorithm") != DIGEST_ALGORITHM:
        raise V3ValidationError("identity_mismatch", "digest_algorithm")
    relative = reference.get("relative_path")
    _reject_unsafe_relative_path(relative)
    target = root / relative
    if target.is_symlink():
        raise V3ValidationError("non_regular_file", relative)
    resolved = target.resolve()
    if root not in resolved.parents:
        raise V3ValidationError("root_escape", relative)
    if not resolved.exists():
        raise V3ValidationError("missing_record", relative)
    if not resolved.is_file():
        raise V3ValidationError("non_regular_file", relative)
    if _file_sha256(resolved) != reference.get("file_sha256"):
        raise V3ValidationError("digest_mismatch", relative)
    if resolved.suffix == ".json":
        document = _read_record(resolved)
        if document.get("record_kind") != reference.get("record_kind"):
            raise V3ValidationError("identity_mismatch", relative)
        if "content_digest" in reference and document.get("content_digest") != reference["content_digest"]:
            raise V3ValidationError("content_digest_mismatch", relative)
    return resolved


def _reject_unsafe_relative_path(relative):
    if not isinstance(relative, str) or not relative:
        raise V3ValidationError("path_traversal", "empty")
    if "\x00" in relative or "\n" in relative:
        raise V3ValidationError("path_traversal", "control character")
    candidate = Path(relative)
    if candidate.is_absolute() or relative.startswith("/") or ":" in relative:
        raise V3ValidationError("path_traversal", relative)
    if ".." in candidate.parts:
        raise V3ValidationError("path_traversal", relative)
    return relative


def _build_locator(*, data_root, path, profile, project_id):
    resolved = Path(path).resolve()
    return {
        "root_kind": "data",
        "root_selector": "data",
        "profile": profile,
        "project_id": project_id,
        "relative_path": resolved.relative_to(Path(data_root).resolve()).as_posix(),
        "digest_algorithm": DIGEST_ALGORITHM,
        "file_sha256": _file_sha256(resolved),
        "evidentiary_role": "advisory_locator",
    }


def _collate_locator(*, locator, data_root, profile, project_id, annotations):
    """外部locatorを照合する。解決できない場合は非停止で注記する。"""

    unknown = sorted(set(locator) - set(_LOCATOR_FIELDS))
    if unknown:
        raise V3ValidationError("unknown_field", ",".join(unknown))
    if locator.get("root_kind") != "data" or locator.get("root_selector") not in ROOT_SELECTORS:
        raise V3ValidationError("unknown_root_kind", str(locator.get("root_selector")))
    if locator.get("evidentiary_role") != "advisory_locator":
        raise V3ValidationError("identity_mismatch", "evidentiary_role")
    if locator.get("profile") not in PROFILES:
        raise V3ValidationError("unknown_root_kind", str(locator.get("profile")))
    if locator.get("project_id") != project_id:
        raise V3ValidationError("foreign_project_data", str(locator.get("project_id")))
    if locator["profile"] != profile:
        annotations.append("locator_profile_mismatch")
        return
    relative = _reject_unsafe_relative_path(locator.get("relative_path"))
    target = Path(data_root) / relative
    if not target.exists():
        annotations.append("locator_unresolved")
        return
    resolved = target.resolve()
    if Path(data_root).resolve() not in resolved.parents:
        raise V3ValidationError("data_root_escape", relative)
    if not resolved.is_file():
        raise V3ValidationError("non_regular_file", relative)
    if _file_sha256(resolved) != locator.get("file_sha256"):
        raise V3ValidationError("observation_tampered", relative)


def write_source_universe(*, project_root, universe_id, universe_version, development_policy_path):
    root = Path(project_root).resolve()
    policies = _artifact_root(root, "policies")
    document = {
        "record_kind": "work4a_source_universe",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "source_universe_id": universe_id,
        "source_universe_version": universe_version,
        "include_root": "tools",
        "include_glob": "**/*.py",
        "excluded_roots": [".git", ".reviewcompass", ".venv", "docs", "records", "tests"],
        "path_encoding": "posix_relative_utf8",
        "development_policy_ref": build_project_ref(
            project_root=root,
            path=development_policy_path,
            record_kind="development_policy",
            record_id="DEVELOPMENT-POLICY",
            version=1,
        ),
    }
    document["content_digest"] = _content_digest(document)
    validate_record_schema(document, record_kind="work4a_source_universe")
    path = _write_new(
        policies / f"work4a-source-universe-v{universe_version}.json", document, allow_identical=True
    )
    return Universe(universe_id, universe_version, path, document["content_digest"])


def write_freshness_policy(
    *, project_root, policy_id, policy_version, development_policy_path, change_class
):
    if change_class not in CHANGE_CLASSES:
        raise V3ValidationError("unknown_field", f"change_class={change_class}")
    root = Path(project_root).resolve()
    policies = _artifact_root(root, "policies")
    document = {
        "record_kind": "work4a_freshness_policy",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "policy_id": policy_id,
        "policy_version": policy_version,
        "change_class": change_class,
        "change_classes": list(CHANGE_CLASSES),
        "revalidation_required_classes": list(REVALIDATION_REQUIRED_CLASSES),
        "disposition_classes": list(DISPOSITION_CLASSES),
        "verification_outcome_classes": list(VERIFICATION_OUTCOME_CLASSES),
        "development_policy_ref": build_project_ref(
            project_root=root,
            path=development_policy_path,
            record_kind="development_policy",
            record_id="DEVELOPMENT-POLICY",
            version=1,
        ),
    }
    document["content_digest"] = _content_digest(document)
    validate_record_schema(document, record_kind="work4a_freshness_policy")
    path = _write_new(
        policies / f"work4a-freshness-policy-v{policy_version}.json", document, allow_identical=True
    )
    return Policy(policy_id, policy_version, path, document["content_digest"])


def _current_policy(project_root):
    policies = _artifact_root(project_root, "policies")
    versions = []
    for path in policies.glob("work4a-freshness-policy-v*.json"):
        matched = POLICY_PATTERN.match(path.name)
        if matched:
            versions.append((int(matched.group(1)), path))
    if not versions:
        raise V3ValidationError("missing_record", "work4a freshness policy")
    version, path = max(versions)
    document = _read_record(path, record_kind="work4a_freshness_policy")
    if document["policy_version"] != version:
        raise V3ValidationError("identity_mismatch", "policy_version")
    if document["change_class"] not in document["change_classes"]:
        raise V3ValidationError("unknown_field", "change_class")
    if "invalid_layout" in document["verification_outcome_classes"]:
        raise V3ValidationError("unknown_field", "invalid_layout is outside policy vocabulary")
    verify_project_ref(project_root=project_root, reference=document["development_policy_ref"])
    return document, path


def _source_files(project_root, universe_document):
    root = Path(project_root).resolve()
    source_root = (root / universe_document["include_root"]).resolve()
    if root not in source_root.parents:
        raise V3ValidationError("root_escape", universe_document["include_root"])
    excluded = set(universe_document["excluded_roots"])
    files = []
    for path in sorted(source_root.glob(universe_document["include_glob"])):
        if path.is_symlink():
            raise V3ValidationError("non_regular_file", str(path))
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative.split("/")[0] in excluded:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as error:
            raise V3ValidationError("non_regular_file", relative) from error
        files.append({"file_sha256": _file_sha256(path), "path": relative})
    return tuple(files)


def _source_content_id(universe_document, files):
    return _digest(
        {
            "files": [dict(item) for item in files],
            "source_universe_id": universe_document["source_universe_id"],
            "source_universe_version": universe_document["source_universe_version"],
        }
    )


def capture_observation(
    *, project_root, runtime_root, profile, universe, policy, head, tool_version, captured_at
):
    root = Path(project_root).resolve()
    manifest = _read_manifest(root)
    data_root = resolve_data_root(project_root=root, runtime_root=runtime_root, profile=profile)
    universe_document = _read_record(universe.path, record_kind="work4a_source_universe")
    _read_record(policy.path, record_kind="work4a_freshness_policy")
    files = _source_files(root, universe_document)
    content_id = _source_content_id(universe_document, files)
    document = {
        "record_kind": "work4a_source_observation",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "snapshot_id": _digest(
            {
                "captured_at": captured_at,
                "head": head,
                "source_content_id": content_id,
                "tool_version": tool_version,
            }
        ),
        "source_content_id": content_id,
        "source_universe_id": universe_document["source_universe_id"],
        "source_universe_version": universe_document["source_universe_version"],
        "head": head,
        "tool_version": tool_version,
        "captured_at": captured_at,
        "files": [dict(item) for item in files],
    }
    document["content_digest"] = _content_digest(document)
    validate_record_schema(document, record_kind="work4a_source_observation")
    path = _write_new(
        data_root / WORK_PREFIX / "observations" / f"{document['snapshot_id']}.json",
        document,
        allow_identical=True,
    )
    return Observation(
        project_root=root,
        data_root=data_root,
        profile=profile,
        project_id=manifest["project_id"],
        path=path,
        snapshot_id=document["snapshot_id"],
        source_content_id=content_id,
        universe_id=universe_document["source_universe_id"],
        universe_version=universe_document["source_universe_version"],
        universe_path=Path(universe.path),
        policy_path=Path(policy.path),
        files=files,
    )


def symbol_id_list_digest(symbol_ids):
    """候補symbol IDの一覧Digest。外部fileが消えても同一性を照合できる。"""

    return _digest({"symbol_ids": sorted(symbol_ids)})


def _extract_symbol_ids(project_root, files):
    symbols = []
    for item in files:
        path = Path(project_root) / item["path"]
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbols.append(f"{item['path']}:{node.name}")
    return tuple(sorted(symbols))


def build_candidate_run(*, observation, known_symbol_ids=()):
    """観測から候補を機械抽出する。既存Entryのsymbolだけをreuseへ分類する。"""

    known = set(known_symbol_ids)
    symbols = _extract_symbol_ids(observation.project_root, observation.files)
    candidates = [
        {"classification": "reuse" if symbol in known else "new", "symbol_id": symbol}
        for symbol in symbols
    ]
    counts = {}
    for candidate in candidates:
        counts[candidate["classification"]] = counts.get(candidate["classification"], 0) + 1
    document = {
        "record_kind": "work4a_candidate_run",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "candidate_run_id": "",
        "observation_snapshot_id": observation.snapshot_id,
        "source_content_id": observation.source_content_id,
        "source_universe_id": observation.universe_id,
        "source_universe_version": observation.universe_version,
        "candidates": candidates,
    }
    document["candidate_run_id"] = _digest(
        {key: value for key, value in document.items() if key != "candidate_run_id"}
    )
    document["content_digest"] = _content_digest(document)
    validate_record_schema(document, record_kind="work4a_candidate_run")
    path = _write_new(
        observation.data_root / WORK_PREFIX / "candidates" / f"{document['candidate_run_id']}.json",
        document,
        allow_identical=True,
    )
    return Candidates(
        observation=observation,
        path=path,
        candidate_run_id=document["candidate_run_id"],
        content_digest=document["content_digest"],
        source_content_id=observation.source_content_id,
        symbol_ids=symbols,
        symbol_id_list_digest=symbol_id_list_digest(symbols),
        candidate_count=len(candidates),
        classification_counts=counts,
    )


def validate_attestation_document(document, *, project_id, disposition_classes):
    """Attestation内部の同一性と要約語彙を検証する。"""

    validate_record_schema(document, record_kind="work4a_observation_attestation")
    if document["project_id"] != project_id:
        raise V3ValidationError("foreign_project_data", document["project_id"])
    if document["profile"] not in PROFILES:
        raise V3ValidationError("unknown_root_kind", document["profile"])
    observation = document["observation"]
    candidate = document["candidate_run"]
    if candidate["observation_snapshot_id"] != observation["snapshot_id"]:
        raise V3ValidationError("unlinked_candidate", candidate["observation_snapshot_id"])
    if candidate["source_content_id"] != document["source_content_id"]:
        raise V3ValidationError("content_identity_mismatch", "candidate_run")
    if observation.get("source_content_id", document["source_content_id"]) != document[
        "source_content_id"
    ]:
        raise V3ValidationError("content_identity_mismatch", "observation")
    summary = document["candidate_summary"]
    if summary.get("sensitive_content_included") is not False:
        raise V3ValidationError("summary_vocabulary_violation", "sensitive_content_included")
    unknown = sorted(set(summary["classification_counts"]) - set(disposition_classes))
    if unknown:
        raise V3ValidationError("summary_vocabulary_violation", ",".join(unknown))
    if summary["candidate_count"] != sum(summary["classification_counts"].values()):
        raise V3ValidationError("summary_vocabulary_violation", "candidate_count")
    return document


def write_attestation(*, project_root, observation, candidates):
    root = Path(project_root).resolve()
    manifest = _read_manifest(root)
    if observation.project_id != manifest["project_id"]:
        raise V3ValidationError("foreign_project_data", observation.project_id)
    policy_document = _read_record(observation.policy_path, record_kind="work4a_freshness_policy")
    observation_document = _read_record(observation.path, record_kind="work4a_source_observation")
    document = {
        "record_kind": "work4a_observation_attestation",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "attestation_id": f"OBSATT-{observation.snapshot_id}",
        "attestation_version": 1,
        "project_id": manifest["project_id"],
        "profile": observation.profile,
        "source_universe_id": observation.universe_id,
        "source_universe_version": observation.universe_version,
        "source_universe_ref": build_project_ref(
            project_root=root,
            path=observation.universe_path,
            record_kind="work4a_source_universe",
            record_id=observation.universe_id,
            version=observation.universe_version,
        ),
        "policy_ref": build_project_ref(
            project_root=root,
            path=observation.policy_path,
            record_kind="work4a_freshness_policy",
            record_id=policy_document["policy_id"],
            version=policy_document["policy_version"],
        ),
        "source_content_id": observation.source_content_id,
        "observation": {
            "record_kind": "work4a_source_observation",
            "snapshot_id": observation.snapshot_id,
            "content_digest": observation_document["content_digest"],
            "head": observation_document["head"],
            "tool_version": observation_document["tool_version"],
            "captured_at": observation_document["captured_at"],
            "source_file_count": len(observation.files),
            "advisory_locator": _build_locator(
                data_root=observation.data_root,
                path=observation.path,
                profile=observation.profile,
                project_id=manifest["project_id"],
            ),
        },
        "candidate_run": {
            "record_kind": "work4a_candidate_run",
            "candidate_run_id": candidates.candidate_run_id,
            "observation_snapshot_id": observation.snapshot_id,
            "source_content_id": candidates.source_content_id,
            "content_digest": candidates.content_digest,
            "advisory_locator": _build_locator(
                data_root=observation.data_root,
                path=candidates.path,
                profile=observation.profile,
                project_id=manifest["project_id"],
            ),
        },
        "candidate_summary": {
            "candidate_count": candidates.candidate_count,
            "symbol_id_list_digest": candidates.symbol_id_list_digest,
            "classification_counts": dict(candidates.classification_counts),
            "sensitive_content_included": False,
        },
        "supersedes_attestation": None,
    }
    document["content_digest"] = _content_digest(document)
    validate_attestation_document(
        document,
        project_id=manifest["project_id"],
        disposition_classes=policy_document["disposition_classes"],
    )
    path = _write_new(
        _ledger_root(root) / "attestations" / f"obsatt-{observation.snapshot_id}--v1.json",
        document,
        allow_identical=True,
    )
    return Attestation(
        path=path,
        attestation_id=document["attestation_id"],
        content_digest=document["content_digest"],
        source_content_id=document["source_content_id"],
        candidate_run_id=candidates.candidate_run_id,
        candidate_content_digest=candidates.content_digest,
    )


def validate_decision_against_attestation(decision_document, attestation_document):
    """人が同意した対象がAttestationと一致することを相互検査する。"""

    validate_record_schema(decision_document, record_kind="work4a_operational_decision")
    candidate = attestation_document["candidate_run"]
    if decision_document["approved_candidate_run_id"] != candidate["candidate_run_id"]:
        raise V3ValidationError("decision_candidate_mismatch", "candidate_run_id")
    if decision_document["approved_candidate_content_digest"] != candidate["content_digest"]:
        raise V3ValidationError("decision_candidate_mismatch", "content_digest")
    if decision_document["approved_source_content_id"] != attestation_document["source_content_id"]:
        raise V3ValidationError("decision_candidate_mismatch", "source_content_id")
    return decision_document


def write_operational_decision(
    *, project_root, decision_id, attestation, approved_targets, human_id, decided_at
):
    root = Path(project_root).resolve()
    decisions = _artifact_root(root, "design_decisions")
    attestation_document = _read_record(
        attestation.path, record_kind="work4a_observation_attestation"
    )
    policy_document = _read_record(
        verify_project_ref(project_root=root, reference=attestation_document["policy_ref"])
    )
    for target in approved_targets:
        if target.get("disposition") not in policy_document["disposition_classes"]:
            raise V3ValidationError("unknown_field", str(target.get("disposition")))
    document = {
        "record_kind": "work4a_operational_decision",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "decision_id": decision_id,
        "attestation_ref": build_project_ref(
            project_root=root,
            path=attestation.path,
            record_kind="work4a_observation_attestation",
            record_id=attestation.attestation_id,
            version=1,
        ),
        "approved_candidate_run_id": attestation_document["candidate_run"]["candidate_run_id"],
        "approved_candidate_content_digest": attestation_document["candidate_run"]["content_digest"],
        "approved_source_content_id": attestation_document["source_content_id"],
        "approved_targets": [dict(target) for target in approved_targets],
        "human_id": human_id,
        "decided_at": decided_at,
    }
    document["content_digest"] = _content_digest(document)
    validate_decision_against_attestation(document, attestation_document)
    path = _write_new(decisions / f"{decision_id.lower()}.json", document)
    return Decision(path=path, decision_id=decision_id, content_digest=document["content_digest"])


def _baseline_series(project_root):
    ledger = _ledger_root(project_root)
    found = {}
    if ledger.exists():
        for path in ledger.glob("ledger-baseline--v*.json"):
            matched = BASELINE_PATTERN.match(path.name)
            if matched:
                found[int(matched.group(1))] = path
    if not found:
        return ()
    expected = list(range(1, max(found) + 1))
    if sorted(found) != expected:
        raise V3ValidationError("baseline_series_broken", str(sorted(found)))
    return tuple(found[version] for version in expected)


def append_baseline(
    *, project_root, attestation, decision, policy, universe, entries, relations, prior
):
    root = Path(project_root).resolve()
    manifest = _read_manifest(root)
    ledger = _ledger_root(root)

    if not Path(policy.path).exists():
        raise V3ValidationError("missing_record", str(policy.path))
    if not Path(decision.path).exists():
        raise V3ValidationError("missing_record", str(decision.path))
    if not Path(universe.path).exists():
        raise V3ValidationError("missing_record", str(universe.path))
    if not Path(attestation.path).exists():
        raise V3ValidationError("missing_record", str(attestation.path))

    policy_document = _read_record(policy.path, record_kind="work4a_freshness_policy")
    universe_document = _read_record(universe.path, record_kind="work4a_source_universe")
    attestation_document = validate_attestation_document(
        _read_record(attestation.path, record_kind="work4a_observation_attestation"),
        project_id=manifest["project_id"],
        disposition_classes=policy_document["disposition_classes"],
    )
    decision_document = validate_decision_against_attestation(
        _read_record(decision.path, record_kind="work4a_operational_decision"),
        attestation_document,
    )

    files = _source_files(root, universe_document)
    if _source_content_id(universe_document, files) != attestation_document["source_content_id"]:
        raise V3ValidationError("stale_observation_reuse", attestation_document["source_content_id"])

    series = _baseline_series(root)
    version = len(series) + 1
    if prior is None and series:
        raise V3ValidationError("baseline_series_broken", "prior baseline required")
    if prior is not None and (not series or Path(prior.path) != series[-1]):
        raise V3ValidationError("baseline_series_broken", "prior is not current")

    decision_ref = build_project_ref(
        project_root=root,
        path=decision.path,
        record_kind="work4a_operational_decision",
        record_id=decision_document["decision_id"],
        version=1,
    )

    planned = []
    for entry in entries:
        planned.append(
            (
                ledger / "entries" / f"{entry['entry_id'].lower()}--v1.json",
                {
                    "record_kind": "work4a_ledger_entry",
                    "schema_version": 1,
                    "digest_algorithm": DIGEST_ALGORITHM,
                    "entry_id": entry["entry_id"],
                    "entry_version": 1,
                    "symbol_id": entry["symbol_id"],
                    "responsibility": entry["responsibility"],
                    "side_effects": entry["side_effects"],
                    "disposition": entry["disposition"],
                    "source_content_id": attestation_document["source_content_id"],
                    "decision_ref": decision_ref,
                },
                "work4a_ledger_entry",
            )
        )
    for relation in relations:
        planned.append(
            (
                ledger / "relations" / f"{relation['relation_id'].lower()}--v1.json",
                {
                    "record_kind": "work4a_ledger_relation",
                    "schema_version": 1,
                    "digest_algorithm": DIGEST_ALGORITHM,
                    "relation_id": relation["relation_id"],
                    "relation_version": 1,
                    "left_entry_id": relation["left_entry_id"],
                    "right_entry_id": relation["right_entry_id"],
                    "relation_kind": relation["relation_kind"],
                    "rationale": relation["rationale"],
                    "decision_ref": decision_ref,
                },
                "work4a_ledger_relation",
            )
        )
    baseline_path = ledger / f"ledger-baseline--v{version}.json"
    for path, document, record_kind in planned:
        if path.exists():
            raise V3ValidationError("immutable_violation", str(path))
        if record_kind == "work4a_ledger_entry":
            if document["disposition"] not in policy_document["disposition_classes"]:
                raise V3ValidationError("unknown_field", document["disposition"])
    if baseline_path.exists():
        raise V3ValidationError("immutable_violation", str(baseline_path))

    entry_refs = []
    relation_refs = []
    prior_ref = None
    if prior is not None:
        prior_document = _read_record(prior.path, record_kind="work4a_ledger_baseline")
        for reference in prior_document["entry_refs"]:
            verify_project_ref(project_root=root, reference=reference)
            entry_refs.append(reference)
        for reference in prior_document["relation_refs"]:
            verify_project_ref(project_root=root, reference=reference)
            relation_refs.append(reference)
        prior_ref = build_project_ref(
            project_root=root,
            path=prior.path,
            record_kind="work4a_ledger_baseline",
            record_id=prior_document["baseline_id"],
            version=prior_document["baseline_version"],
        )

    written = []
    for path, document, record_kind in planned:
        document["content_digest"] = _content_digest(document)
        validate_record_schema(document, record_kind=record_kind)
        _write_new(path, document)
        written.append(path)
        reference = build_project_ref(
            project_root=root,
            path=path,
            record_kind=record_kind,
            record_id=document.get("entry_id") or document["relation_id"],
            version=1,
        )
        if record_kind == "work4a_ledger_entry":
            entry_refs.append(reference)
        else:
            relation_refs.append(reference)

    baseline_document = {
        "record_kind": "work4a_ledger_baseline",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "baseline_id": "RRL-BASELINE",
        "baseline_version": version,
        "project_id": manifest["project_id"],
        "source_universe_id": universe_document["source_universe_id"],
        "source_universe_version": universe_document["source_universe_version"],
        "source_content_id": attestation_document["source_content_id"],
        "universe_ref": build_project_ref(
            project_root=root,
            path=universe.path,
            record_kind="work4a_source_universe",
            record_id=universe_document["source_universe_id"],
            version=universe_document["source_universe_version"],
        ),
        "policy_ref": build_project_ref(
            project_root=root,
            path=policy.path,
            record_kind="work4a_freshness_policy",
            record_id=policy_document["policy_id"],
            version=policy_document["policy_version"],
        ),
        "attestation_ref": build_project_ref(
            project_root=root,
            path=attestation.path,
            record_kind="work4a_observation_attestation",
            record_id=attestation_document["attestation_id"],
            version=1,
        ),
        "decision_ref": decision_ref,
        "prior_baseline_ref": prior_ref,
        "entry_refs": entry_refs,
        "relation_refs": relation_refs,
    }
    baseline_document["content_digest"] = _content_digest(baseline_document)
    validate_record_schema(baseline_document, record_kind="work4a_ledger_baseline")
    _write_new(baseline_path, baseline_document)
    return Baseline(
        path=baseline_path,
        baseline_version=version,
        entry_paths=tuple(
            (root / reference["relative_path"]) for reference in entry_refs
        ),
        relation_paths=tuple(
            (root / reference["relative_path"]) for reference in relation_refs
        ),
    )


def validate_current(*, project_root, runtime_root=None, profile=None):
    """P0からP7の順序でcurrent Baselineを検証する。外部fileが無くても確定する。"""

    root = Path(project_root).resolve()
    manifest = _read_manifest(root)
    _artifact_root(root, "reuse")
    annotations = []

    data_root = None
    if runtime_root is not None:
        data_root = resolve_data_root(
            project_root=root, runtime_root=runtime_root, profile=profile
        )

    policy_document, _policy_path = _current_policy(root)

    series = _baseline_series(root)
    if not series:
        raise V3ValidationError("baseline_series_broken", "no baseline")
    baseline_path = series[-1]
    baseline_document = _read_record(baseline_path, record_kind="work4a_ledger_baseline")
    if baseline_document["baseline_version"] != len(series):
        raise V3ValidationError("baseline_series_broken", "version mismatch")
    if baseline_document["project_id"] != manifest["project_id"]:
        raise V3ValidationError("foreign_project_data", baseline_document["project_id"])

    references = [
        baseline_document["universe_ref"],
        baseline_document["policy_ref"],
        baseline_document["attestation_ref"],
        baseline_document["decision_ref"],
        *baseline_document["entry_refs"],
        *baseline_document["relation_refs"],
    ]
    if baseline_document["prior_baseline_ref"] is not None:
        references.append(baseline_document["prior_baseline_ref"])
    for reference in references:
        verify_project_ref(project_root=root, reference=reference)
    attestation_path = verify_project_ref(
        project_root=root, reference=baseline_document["attestation_ref"]
    )
    decision_path = verify_project_ref(
        project_root=root, reference=baseline_document["decision_ref"]
    )

    baseline_policy = baseline_document["policy_ref"]
    if (
        baseline_policy["record_id"] != policy_document["policy_id"]
        or baseline_policy["version"] != policy_document["policy_version"]
    ):
        if policy_document["change_class"] in policy_document["revalidation_required_classes"]:
            raise V3ValidationError("policy_revalidation_required", policy_document["change_class"])

    attestation_document = validate_attestation_document(
        _read_record(attestation_path),
        project_id=manifest["project_id"],
        disposition_classes=policy_document["disposition_classes"],
    )
    validate_decision_against_attestation(_read_record(decision_path), attestation_document)

    if data_root is not None:
        for section in ("observation", "candidate_run"):
            _collate_locator(
                locator=attestation_document[section]["advisory_locator"],
                data_root=data_root,
                profile=profile,
                project_id=manifest["project_id"],
                annotations=annotations,
            )

    unique = tuple(dict.fromkeys(annotations))
    return CurrentState(
        baseline_version=baseline_document["baseline_version"],
        path=baseline_path,
        source_content_id=baseline_document["source_content_id"],
        annotations=unique,
    )


def evaluate_continuity(
    *, project_root, runtime_root, profile, head, captured_at, universe=None
):
    """配布先での連続性を判定する。project artifactだけで確定する。"""

    root = Path(project_root).resolve()
    state = validate_current(project_root=root, runtime_root=runtime_root, profile=profile)
    baseline_document = _read_record(state.path, record_kind="work4a_ledger_baseline")

    if universe is None:
        universe_path = verify_project_ref(
            project_root=root, reference=baseline_document["universe_ref"]
        )
    else:
        universe_path = Path(universe.path)
    universe_document = _read_record(universe_path, record_kind="work4a_source_universe")

    if (
        universe_document["source_universe_id"] != baseline_document["source_universe_id"]
        or universe_document["source_universe_version"]
        != baseline_document["source_universe_version"]
    ):
        return Continuity(
            state="universe_diverged",
            permits_baseline_advance=False,
            source_content_id=baseline_document["source_content_id"],
            annotations=state.annotations,
        )

    files = _source_files(root, universe_document)
    content_id = _source_content_id(universe_document, files)
    diverged = content_id != baseline_document["source_content_id"]
    return Continuity(
        state="content_diverged" if diverged else "continuous_fresh",
        permits_baseline_advance=not diverged,
        source_content_id=content_id,
        annotations=state.annotations,
    )


def record_historical_status(
    *, project_root, contract_path, creation_commit, creation_policy_ref, human_decision_id
):
    """legacy Task Contractの歴史的状態を別identityで記録する。根拠不足は昇格させない。"""

    root = Path(project_root).resolve()
    statuses = _artifact_root(root, "contracts") / "historical-status"
    contract = Path(contract_path)
    if not contract.is_file():
        raise V3ValidationError("missing_record", str(contract))

    complete = bool(creation_commit) and bool(human_decision_id) and creation_policy_ref is not None
    if complete:
        verify_project_ref(project_root=root, reference=creation_policy_ref)
    outcome = "completed_historical" if complete else "evidence_insufficient"

    stem = contract.stem
    version = 1
    while (statuses / f"{stem}--v{version}.json").exists():
        version += 1
    document = {
        "record_kind": "work4a_historical_contract_status",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "contract_status_id": f"HCS-{stem.upper()}",
        "status_version": version,
        "contract_ref": {
            "root_kind": "project",
            "record_kind": "legacy_task_contract",
            "record_id": stem,
            "version": 1,
            "relative_path": contract.resolve().relative_to(root).as_posix(),
            "digest_algorithm": DIGEST_ALGORITHM,
            "file_sha256": _file_sha256(contract),
        },
        "creation_commit": creation_commit,
        "creation_policy_ref": creation_policy_ref,
        "human_decision_id": human_decision_id,
        "outcome": outcome,
        "permits_current_start": False,
    }
    document["content_digest"] = _content_digest(document)
    validate_record_schema(document, record_kind="work4a_historical_contract_status")
    path = _write_new(statuses / f"{stem}--v{version}.json", document)
    return HistoricalStatus(outcome=outcome, permits_current_start=False, path=path)
