"""Work 4A rebuildの最小identity chain。"""

import ast
import dataclasses
import hashlib
import json
from pathlib import Path


class RebuildValidationError(Exception):
    """Work 4A rebuildの不変条件違反。"""


def _digest(value):
    if isinstance(value, bytes):
        payload = value
    else:
        payload = json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise RebuildValidationError("new-only output already exists")
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _load_manifest(project_root, manifest_override=None):
    if manifest_override is not None:
        return manifest_override
    path = Path(project_root) / ".reviewcompass" / "project-manifest.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RebuildValidationError("project manifest is invalid") from error


def resolve_reuse_root(*, project_root, manifest_override=None):
    root = Path(project_root).resolve()
    manifest = _load_manifest(root, manifest_override)
    try:
        relative = manifest["artifact_roots"]["reuse"]
    except (KeyError, TypeError) as error:
        raise RebuildValidationError("reuse root is invalid") from error
    candidate = Path(relative)
    if candidate.is_absolute() or not candidate.parts:
        raise RebuildValidationError("reuse root is invalid")
    resolved = (root / candidate).resolve()
    if root not in resolved.parents:
        raise RebuildValidationError("reuse root escapes project")
    return resolved / "reusable-routine-ledger"


@dataclasses.dataclass(frozen=True)
class Observation:
    source_content_id: str
    snapshot_id: str
    observation_path: Path
    index_path: Path
    project_id: str


@dataclasses.dataclass(frozen=True)
class CandidateRun:
    candidate_run_id: str
    candidate_path: Path
    candidate_digest: str
    source_content_id: str


@dataclasses.dataclass(frozen=True)
class Decision:
    decision_id: str
    decision_path: Path
    decision_digest: str


@dataclasses.dataclass(frozen=True)
class Baseline:
    baseline_path: Path
    baseline_digest: str
    source_content_id: str
    entry_paths: tuple
    new_entry_paths: tuple
    entry_refs: tuple
    relation_paths: tuple


@dataclasses.dataclass(frozen=True)
class BaselineValidation:
    status: str


@dataclasses.dataclass(frozen=True)
class HistoricalContractStatus:
    contract_sha256: str
    outcome: str
    permits_current_start: bool
    status_path: Path


def capture_source_observation(
    *, project_root, source_root, data_root, source_paths, head, tool_version
):
    root = Path(source_root).resolve()
    project_id = _load_manifest(project_root)["project_id"]
    files = []
    symbols = []
    for relative in sorted(source_paths):
        candidate = (root / relative).resolve()
        if root not in candidate.parents or not candidate.is_file():
            raise RebuildValidationError("source path is invalid")
        content = candidate.read_bytes()
        files.append({"path": relative, "sha256": _digest(content)})
        try:
            tree = ast.parse(content.decode("utf-8"), filename=relative)
        except (UnicodeDecodeError, SyntaxError) as error:
            raise RebuildValidationError("source parse failed") from error
        symbols.extend(
            {"path": relative, "name": node.name, "line": node.lineno}
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
    content_id = _digest({"source_paths": files})
    snapshot_id = _digest(
        {"source_content_id": content_id, "head": head, "tool_version": tool_version}
    )
    base = Path(data_root).resolve() / "projects" / project_id / "reuse"
    observation_path = base / "observations" / f"{snapshot_id}.json"
    index_path = base / "indexes" / f"{snapshot_id}.json"
    _write_new(
        observation_path,
        {
            "record_kind": "source_observation",
            "snapshot_id": snapshot_id,
            "source_content_id": content_id,
            "head": head,
            "tool_version": tool_version,
            "files": files,
        },
    )
    _write_new(index_path, {"snapshot_id": snapshot_id, "symbols": symbols})
    return Observation(content_id, snapshot_id, observation_path, index_path, project_id)


def build_candidate_run(*, observation, data_root, tool_version):
    index = json.loads(observation.index_path.read_text(encoding="utf-8"))
    payload = {
        "record_kind": "candidate_run",
        "source_content_id": observation.source_content_id,
        "snapshot_id": observation.snapshot_id,
        "tool_version": tool_version,
        "symbols": index["symbols"],
    }
    digest = _digest(payload)
    candidate_id = digest
    path = (
        Path(data_root).resolve()
        / "projects"
        / observation.project_id
        / "reuse"
        / "candidates"
        / f"{candidate_id}.json"
    )
    _write_new(path, {**payload, "content_digest": digest})
    return CandidateRun(candidate_id, path, digest, observation.source_content_id)


def write_human_decision(*, project_root, decision_id, candidate_run, disposition):
    root = Path(project_root).resolve()
    manifest = _load_manifest(root)
    relative = Path(manifest["artifact_roots"]["design_decisions"])
    if relative.is_absolute():
        raise RebuildValidationError("decision root is invalid")
    decision_root = (root / relative).resolve()
    if root not in decision_root.parents:
        raise RebuildValidationError("decision root is invalid")
    payload = {
        "record_kind": "human_reuse_decision",
        "decision_id": decision_id,
        "candidate_run_id": candidate_run.candidate_run_id,
        "candidate_digest": candidate_run.candidate_digest,
        "disposition": disposition,
    }
    digest = _digest(payload)
    path = decision_root / f"{decision_id.lower()}.json"
    _write_new(path, {**payload, "content_digest": digest})
    return Decision(decision_id, path, digest)


def _record_ref(path, root, document):
    return {
        "record_id": document.get("entry_id", document.get("relation_id")),
        "version": document.get("entry_version", document.get("relation_version")),
        "path": str(path.relative_to(root)),
        "sha256": _digest(path.read_bytes()),
    }


def append_reusable_routine_baseline(
    *, project_root, observation, candidate_run, decision, new_entries, new_relations, prior
):
    root = resolve_reuse_root(project_root=project_root)
    old_refs = () if prior is None else prior.entry_refs
    old_relations = () if prior is None else tuple(
        _record_ref(
            path, root, json.loads(path.read_text(encoding="utf-8"))
        )
        for path in prior.relation_paths
    )
    entry_paths = []
    refs = list(old_refs)
    for entry in new_entries:
        document = {**entry, "entry_version": 1, "source_content_id": observation.source_content_id}
        path = root / "entries" / f"{entry['entry_id'].lower()}--v1.json"
        _write_new(path, document)
        entry_paths.append(path)
        refs.append(_record_ref(path, root, document))
    relation_paths = []
    relation_refs = list(old_relations)
    for relation in new_relations:
        document = {**relation, "relation_version": 1}
        path = root / "relations" / f"{relation['relation_id'].lower()}--v1.json"
        _write_new(path, document)
        relation_paths.append(path)
        relation_refs.append(_record_ref(path, root, document))
    version = 1 if prior is None else int(prior.baseline_path.stem.rsplit("v", 1)[1]) + 1
    payload = {
        "record_kind": "reusable_routine_baseline",
        "baseline_version": version,
        "source_content_id": observation.source_content_id,
        "snapshot_id": observation.snapshot_id,
        "candidate_run_id": candidate_run.candidate_run_id,
        "candidate_digest": candidate_run.candidate_digest,
        "decision_ref": {"path": str(decision.decision_path), "sha256": decision.decision_digest},
        "entry_refs": refs,
        "relation_refs": relation_refs,
    }
    digest = _digest(payload)
    baseline_path = root / f"ledger-baseline--v{version}.json"
    _write_new(baseline_path, {**payload, "content_digest": digest})
    prior_paths = () if prior is None else prior.entry_paths
    return Baseline(
        baseline_path,
        digest,
        observation.source_content_id,
        (*prior_paths, *entry_paths),
        tuple(entry_paths),
        tuple(refs),
        (*(() if prior is None else prior.relation_paths), *relation_paths),
    )


def validate_baseline(*, baseline, observation, policy_change):
    if policy_change in {"authority", "security", "irreversible"}:
        return BaselineValidation("revalidation_required")
    for path, reference in zip(baseline.entry_paths, baseline.entry_refs):
        if _digest(path.read_bytes()) != reference["sha256"]:
            raise RebuildValidationError("entry digest mismatch")
    if baseline.source_content_id != observation.source_content_id:
        return BaselineValidation("stale")
    return BaselineValidation("fresh")


def record_historical_contract_status(
    *, contract_path, creation_commit, creation_policy_digest, human_decision, status_root
):
    if not isinstance(human_decision, dict) or human_decision.get("outcome") != "completed_historical":
        raise RebuildValidationError("human approval is required")
    contract = Path(contract_path)
    digest = _digest(contract.read_bytes())
    payload = {
        "record_kind": "historical_contract_status",
        "contract_path": str(contract),
        "contract_sha256": digest,
        "creation_commit": creation_commit,
        "creation_policy_digest": creation_policy_digest,
        "decision_id": human_decision["decision_id"],
        "outcome": "completed_historical",
        "permits_current_start": False,
    }
    path = Path(status_root) / f"{digest}.json"
    _write_new(path, {**payload, "content_digest": _digest(payload)})
    return HistoricalContractStatus(digest, "completed_historical", False, path)
