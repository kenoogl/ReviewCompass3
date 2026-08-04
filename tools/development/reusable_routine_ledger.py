"""Work 4Aの最小Reusable Routine Ledger保存・照合器。"""

import dataclasses
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_IDENTIFIER = re.compile(r"[A-Z][A-Z0-9-]*\Z")


class ReusableRoutineLedgerError(Exception):
    """Reusable Routine Ledgerを安全に保存または照合できない。"""


@dataclasses.dataclass(frozen=True)
class PersistedReusableRoutineLedger:
    root: Path
    baseline_path: Path
    baseline_sha256: str
    entry_paths: tuple
    entry_sha256s: tuple
    relation_paths: tuple
    relation_sha256s: tuple


def _json_bytes(value):
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(value).hexdigest()


def _canonical_digest(value):
    return _sha256(
        json.dumps(
            value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    )


def _require_sha256(value, field):
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ReusableRoutineLedgerError(f"{field} must be SHA-256")


def _ledger_root(project_root):
    root = Path(project_root).resolve()
    manifest_path = root / ".reviewcompass" / "project-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        relative = manifest["artifact_roots"]["reuse"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ReusableRoutineLedgerError("reuse manifest is invalid") from error
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ReusableRoutineLedgerError("reuse root is unsafe")
    reuse_root = (root / Path(*candidate.parts)).resolve()
    if root not in reuse_root.parents:
        raise ReusableRoutineLedgerError("reuse root escapes project")
    return reuse_root / "reusable-routine-ledger"


def _entry_document(entry, source_snapshot_id):
    required = {
        "record_kind",
        "entry_id",
        "entry_version",
        "source_snapshot_id",
        "symbol_bindings",
        "responsibility",
        "inputs",
        "outputs",
        "side_effects",
        "constraints",
        "consumers",
        "lifecycle",
        "reuse_disposition",
        "decision_refs",
    }
    if not isinstance(entry, dict) or set(entry) != required:
        raise ReusableRoutineLedgerError("entry fields are invalid")
    if entry["record_kind"] != "reusable_routine_entry":
        raise ReusableRoutineLedgerError("entry kind is invalid")
    if _IDENTIFIER.fullmatch(entry["entry_id"] or "") is None:
        raise ReusableRoutineLedgerError("entry identity is invalid")
    if not isinstance(entry["entry_version"], int) or entry["entry_version"] < 1:
        raise ReusableRoutineLedgerError("entry version is invalid")
    if entry["source_snapshot_id"] != source_snapshot_id:
        raise ReusableRoutineLedgerError("entry snapshot mismatch")
    if entry["lifecycle"] not in {"active", "retired"}:
        raise ReusableRoutineLedgerError("entry lifecycle is invalid")
    if entry["reuse_disposition"] not in {
        "reuse", "extend", "merge", "split_with_rationale"
    }:
        raise ReusableRoutineLedgerError("entry disposition is invalid")
    if not entry["symbol_bindings"] or not entry["decision_refs"]:
        raise ReusableRoutineLedgerError("entry bindings are missing")
    for binding in entry["symbol_bindings"]:
        if not isinstance(binding, dict) or set(binding) != {
            "symbol_id", "content_sha256"
        }:
            raise ReusableRoutineLedgerError("entry symbol binding is invalid")
        _require_sha256(binding["content_sha256"], "entry content digest")
    document = dict(entry)
    document["content_digest"] = _canonical_digest(entry)
    return document


def _write_new(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(_json_bytes(document))
    except FileExistsError as error:
        raise ReusableRoutineLedgerError("ledger output already exists") from error


def _relation_document(relation, source_snapshot_id):
    required = {
        "record_kind", "relation_id", "relation_version", "source_snapshot_id",
        "relation_kind", "participant_symbol_ids", "rationale", "decision_refs",
    }
    if not isinstance(relation, dict) or set(relation) != required:
        raise ReusableRoutineLedgerError("relation fields are invalid")
    if relation["record_kind"] != "reusable_routine_relation":
        raise ReusableRoutineLedgerError("relation kind is invalid")
    if _IDENTIFIER.fullmatch(relation["relation_id"] or "") is None:
        raise ReusableRoutineLedgerError("relation identity is invalid")
    if not isinstance(relation["relation_version"], int) or relation["relation_version"] < 1:
        raise ReusableRoutineLedgerError("relation version is invalid")
    if relation["source_snapshot_id"] != source_snapshot_id:
        raise ReusableRoutineLedgerError("relation snapshot mismatch")
    if relation["relation_kind"] not in {"duplicate_candidate", "alias", "successor", "intentional_separation"}:
        raise ReusableRoutineLedgerError("relation type is invalid")
    if len(relation["participant_symbol_ids"]) < 2 or not relation["rationale"] or not relation["decision_refs"]:
        raise ReusableRoutineLedgerError("relation evidence is missing")
    document = dict(relation)
    document["content_digest"] = _canonical_digest(relation)
    return document


def persist_reusable_routine_ledger(
    *,
    project_root,
    source_snapshot_id,
    candidate_list_digest,
    entries,
    relations,
    decision_refs,
):
    """承認済みentryをreuse rootへnew-only保存しbaselineで束縛する。"""
    _require_sha256(source_snapshot_id, "source snapshot")
    _require_sha256(candidate_list_digest, "candidate list digest")
    if not isinstance(entries, tuple) or not isinstance(relations, tuple):
        raise ReusableRoutineLedgerError("ledger records must be tuples")
    if not entries or not decision_refs or not all(
        isinstance(value, str) and value for value in decision_refs
    ):
        raise ReusableRoutineLedgerError("ledger decision references are invalid")
    root = _ledger_root(project_root)
    documents = tuple(
        _entry_document(entry, source_snapshot_id) for entry in entries
    )
    relation_documents = tuple(
        _relation_document(relation, source_snapshot_id) for relation in relations
    )
    identifiers = tuple(document["entry_id"] for document in documents)
    if len(set(identifiers)) != len(identifiers):
        raise ReusableRoutineLedgerError("ledger entry identity is duplicated")
    entry_paths = tuple(
        root / "entries" / f"{identifier.lower()}--v1.json"
        for identifier in identifiers
    )
    relation_paths = tuple(
        root / "relations" / f"{document['relation_id'].lower()}--v1.json"
        for document in relation_documents
    )
    baseline_path = root / "ledger-baseline--v1.json"
    if baseline_path.exists() or any(path.exists() for path in (*entry_paths, *relation_paths)):
        raise ReusableRoutineLedgerError("ledger output already exists")
    for path, document in zip(entry_paths, documents):
        _write_new(path, document)
    entry_sha256s = tuple(_sha256(path.read_bytes()) for path in entry_paths)
    for path, document in zip(relation_paths, relation_documents):
        _write_new(path, document)
    relation_sha256s = tuple(_sha256(path.read_bytes()) for path in relation_paths)
    entry_refs = [
        {
            "entry_id": document["entry_id"],
            "entry_version": document["entry_version"],
            "path": str(path.relative_to(root).as_posix()),
            "sha256": digest,
        }
        for document, path, digest in zip(documents, entry_paths, entry_sha256s)
    ]
    relation_refs = [{"relation_id": document["relation_id"], "relation_version": document["relation_version"], "path": str(path.relative_to(root).as_posix()), "sha256": digest} for document, path, digest in zip(relation_documents, relation_paths, relation_sha256s)]
    baseline = {
        "record_kind": "reusable_routine_ledger_baseline",
        "ledger_id": "RRL-BASELINE",
        "ledger_version": 1,
        "source_snapshot_id": source_snapshot_id,
        "candidate_list_digest": candidate_list_digest,
        "entry_refs": entry_refs,
        "relation_refs": relation_refs,
        "decision_refs": sorted(set(decision_refs)),
    }
    baseline["content_digest"] = _canonical_digest(baseline)
    _write_new(baseline_path, baseline)
    return PersistedReusableRoutineLedger(
        root=root,
        baseline_path=baseline_path,
        baseline_sha256=_sha256(baseline_path.read_bytes()),
        entry_paths=entry_paths,
        entry_sha256s=entry_sha256s,
        relation_paths=relation_paths,
        relation_sha256s=relation_sha256s,
    )


def verify_reusable_routine_ledger(*, persisted):
    """baselineとentryのDigest結線を再読込照合する。"""
    if not isinstance(persisted, PersistedReusableRoutineLedger):
        raise ReusableRoutineLedgerError("persisted ledger is invalid")
    try:
        baseline_bytes = persisted.baseline_path.read_bytes()
        baseline = json.loads(baseline_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReusableRoutineLedgerError("persisted ledger is unreadable") from error
    if _sha256(baseline_bytes) != persisted.baseline_sha256:
        raise ReusableRoutineLedgerError("persisted ledger baseline digest mismatch")
    refs = baseline.get("entry_refs")
    if not isinstance(refs, list) or len(refs) != len(persisted.entry_paths):
        raise ReusableRoutineLedgerError("persisted ledger entry refs are invalid")
    for ref, path, digest in zip(refs, persisted.entry_paths, persisted.entry_sha256s):
        if ref.get("path") != str(path.relative_to(persisted.root).as_posix()):
            raise ReusableRoutineLedgerError("persisted ledger entry path mismatch")
        try:
            actual = _sha256(path.read_bytes())
        except OSError as error:
            raise ReusableRoutineLedgerError("persisted ledger entry missing") from error
        if actual != digest or ref.get("sha256") != digest:
            raise ReusableRoutineLedgerError("persisted ledger entry digest mismatch")
    relation_refs = baseline.get("relation_refs")
    if not isinstance(relation_refs, list) or len(relation_refs) != len(persisted.relation_paths):
        raise ReusableRoutineLedgerError("persisted ledger relation refs are invalid")
    for ref, path, digest in zip(relation_refs, persisted.relation_paths, persisted.relation_sha256s):
        try:
            actual = _sha256(path.read_bytes())
        except OSError as error:
            raise ReusableRoutineLedgerError("persisted ledger relation missing") from error
        if ref.get("path") != str(path.relative_to(persisted.root).as_posix()) or actual != digest or ref.get("sha256") != digest:
            raise ReusableRoutineLedgerError("persisted ledger relation digest mismatch")
    return persisted
