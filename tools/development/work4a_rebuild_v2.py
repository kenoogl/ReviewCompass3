"""Work 4A v2のPolicy・universe束縛identity chain。"""

import ast
import dataclasses
import hashlib
import json
from pathlib import Path


class V2ValidationError(Exception):
    pass


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else _canonical(value)).hexdigest()


def _write_new(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise V2ValidationError("new-only output exists")
    path.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _manifest(root):
    return json.loads((Path(root) / ".reviewcompass/project-manifest.json").read_text(encoding="utf-8"))


def _root(root, name):
    base = Path(root).resolve()
    candidate = (base / _manifest(base)["artifact_roots"][name]).resolve()
    if base not in candidate.parents:
        raise V2ValidationError(f"{name} root is invalid")
    return candidate


def _ref(path, record_id, version):
    return {"record_id": record_id, "version": version, "path": str(path), "file_sha256": _digest(path.read_bytes())}


@dataclasses.dataclass(frozen=True)
class Universe:
    universe_id: str
    path: Path
    digest: str


@dataclasses.dataclass(frozen=True)
class Policy:
    policy_id: str
    path: Path
    digest: str


@dataclasses.dataclass(frozen=True)
class Observation:
    source_content_id: str
    snapshot_id: str
    paths: tuple
    path: Path
    universe: Universe


@dataclasses.dataclass(frozen=True)
class Candidates:
    candidate_id: str
    path: Path
    digest: str
    source_content_id: str


@dataclasses.dataclass(frozen=True)
class Decision:
    decision_id: str
    path: Path
    digest: str


@dataclasses.dataclass(frozen=True)
class Baseline:
    path: Path
    current_version: int
    entry_paths: tuple
    relation_paths: tuple
    observation: Observation
    policy: Policy


@dataclasses.dataclass(frozen=True)
class Status:
    status: str


@dataclasses.dataclass(frozen=True)
class HistoricalStatus:
    outcome: str
    permits_current_start: bool


def write_source_universe(*, project_root, universe_id, development_policy_path):
    policy_root = _root(project_root, "policies")
    development = Path(development_policy_path)
    payload = {"record_kind": "work4a_source_universe", "schema_version": 1, "source_universe_id": universe_id, "source_universe_version": 1, "include_root": "tools", "include_glob": "**/*.py", "excluded_roots": ["tests", ".venv", ".git", ".reviewcompass", "docs", "records"], "path_encoding": "posix_relative_utf8", "development_policy_ref": {"path": str(development), "file_sha256": _digest(development.read_bytes())}}
    digest = _digest(payload)
    path = policy_root / "work4a-source-universe-v1.json"
    _write_new(path, {**payload, "content_digest": digest})
    return Universe(universe_id, path, digest)


def write_freshness_policy(*, project_root, policy_id, development_policy_path):
    policy_root = _root(project_root, "policies")
    development = Path(development_policy_path)
    payload = {"record_kind": "work4a_freshness_policy", "schema_version": 1, "policy_id": policy_id, "policy_version": 1, "development_policy_ref": {"path": str(development), "file_sha256": _digest(development.read_bytes())}, "change_classes": ["ordinary", "security", "authority", "irreversible"], "revalidation_required_classes": ["security", "authority", "irreversible"]}
    digest = _digest(payload)
    path = policy_root / "work4a-freshness-policy-v1.json"
    _write_new(path, {**payload, "content_digest": digest})
    return Policy(policy_id, path, digest)


def capture_observation(*, project_root, data_root, universe, policy, head, tool_version):
    root = Path(project_root).resolve()
    document = json.loads(universe.path.read_text(encoding="utf-8"))
    if document["content_digest"] != universe.digest:
        raise V2ValidationError("universe digest mismatch")
    tools = root / document["include_root"]
    paths = tuple(sorted(str(path.relative_to(root).as_posix()) for path in tools.glob(document["include_glob"]) if path.is_file() and not path.is_symlink()))
    files = [{"path": p, "file_sha256": _digest((root / p).read_bytes())} for p in paths]
    for item in files:
        ast.parse((root / item["path"]).read_text(encoding="utf-8"))
    content = _digest({"universe_id": universe.universe_id, "files": files})
    snapshot = _digest({"source_content_id": content, "head": head, "tool_version": tool_version})
    data = Path(data_root) / "projects" / _manifest(root)["project_id"] / "reuse" / "observations" / f"{snapshot}.json"
    _write_new(data, {"snapshot_id": snapshot, "source_content_id": content, "source_universe_ref": _ref(universe.path, universe.universe_id, 1), "policy_ref": _ref(policy.path, policy.policy_id, 1), "head": head, "files": files})
    return Observation(content, snapshot, paths, data, universe)


def build_candidate_run(*, observation):
    doc = json.loads(observation.path.read_text(encoding="utf-8"))
    payload = {"record_kind": "work4a_candidate_run", "snapshot_id": observation.snapshot_id, "source_content_id": observation.source_content_id, "paths": observation.paths}
    digest = _digest(payload)
    path = observation.path.parent.parent / "candidates" / f"{digest}.json"
    _write_new(path, {**payload, "content_digest": digest})
    return Candidates(digest, path, digest, observation.source_content_id)


def write_operational_decision(*, project_root, decision_id, candidates, disposition, human_id):
    root = _root(project_root, "design_decisions")
    payload = {"record_kind": "work4a_operational_decision", "decision_id": decision_id, "candidate_ref": _ref(candidates.path, candidates.candidate_id, 1), "disposition": disposition, "human_id": human_id}
    digest = _digest(payload)
    path = root / f"{decision_id.lower()}.json"
    _write_new(path, {**payload, "content_digest": digest})
    return Decision(decision_id, path, digest)


def _reuse_root(project_root):
    return _root(project_root, "reuse") / "reusable-routine-ledger"


def validate_baseline_series(*, versions):
    if tuple(versions) != tuple(range(1, len(versions) + 1)):
        raise V2ValidationError("baseline series is invalid")
    return Status("valid")


def append_baseline(*, project_root, observation, candidates, policy, decision, entries, relations, prior):
    if decision is None:
        raise V2ValidationError("operational decision is required")
    if candidates.source_content_id != observation.source_content_id:
        raise V2ValidationError("candidate source mismatch")
    root = _reuse_root(project_root)
    old_entries = () if prior is None else prior.entry_paths
    old_relations = () if prior is None else prior.relation_paths
    version = 1 if prior is None else prior.current_version + 1
    entry_paths, relation_paths = [], []
    for entry in entries:
        path = root / "entries" / f"{entry['entry_id'].lower()}--v1.json"
        _write_new(path, {**entry, "entry_version": 1})
        entry_paths.append(path)
    for relation in relations:
        path = root / "relations" / f"{relation['relation_id'].lower()}--v1.json"
        _write_new(path, {**relation, "relation_version": 1})
        relation_paths.append(path)
    all_entries, all_relations = (*old_entries, *entry_paths), (*old_relations, *relation_paths)
    payload = {"record_kind": "work4a_baseline", "baseline_version": version, "observation_ref": _ref(observation.path, observation.snapshot_id, 1), "candidate_ref": _ref(candidates.path, candidates.candidate_id, 1), "policy_ref": _ref(policy.path, policy.policy_id, 1), "decision_ref": _ref(decision.path, decision.decision_id, 1), "entry_refs": [_ref(p, json.loads(p.read_text())["entry_id"], 1) for p in all_entries], "relation_refs": [_ref(p, json.loads(p.read_text())["relation_id"], 1) for p in all_relations]}
    path = root / f"ledger-baseline--v{version}.json"
    _write_new(path, {**payload, "content_digest": _digest(payload)})
    return Baseline(path, version, all_entries, all_relations, observation, policy)


def validate_current(*, project_root, observation, policy):
    root = _reuse_root(project_root)
    baselines = sorted(root.glob("ledger-baseline--v*.json"))
    validate_baseline_series(versions=tuple(int(p.stem.rsplit("v", 1)[1]) for p in baselines))
    if not baselines:
        raise V2ValidationError("baseline series is invalid")
    doc = json.loads(baselines[-1].read_text(encoding="utf-8"))
    for reference in (*doc["entry_refs"], *doc["relation_refs"]):
        if _digest(Path(reference["path"]) .read_bytes()) != reference["file_sha256"]:
            raise V2ValidationError("record digest mismatch")
    return Status("fresh")


def classify_policy_change(*, policy, change_class):
    doc = json.loads(policy.path.read_text(encoding="utf-8"))
    if change_class not in doc["change_classes"]:
        raise V2ValidationError("policy change class is invalid")
    return Status("revalidation_required" if change_class in doc["revalidation_required_classes"] else "fresh")


def validate_universe_change(*, baseline_universe, observed_universe_id):
    return Status("fresh" if baseline_universe.universe_id == observed_universe_id else "stale")


def record_historical_status(*, project_root, contract_path, creation_commit, creation_policy_ref, human_decision):
    if creation_commit is None or creation_policy_ref is None:
        if human_decision and human_decision.get("outcome") == "completed_historical":
            raise V2ValidationError("creation evidence is required")
        return HistoricalStatus("evidence_insufficient", False)
    if not human_decision or human_decision.get("outcome") != "completed_historical":
        raise V2ValidationError("operational decision is required")
    return HistoricalStatus("completed_historical", False)
