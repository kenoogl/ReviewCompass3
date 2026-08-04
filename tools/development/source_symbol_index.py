"""Work 4Aの最小Source SnapshotとSource Symbol Index生成器。"""

import ast
import dataclasses
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_PERSISTENCE_PROFILES = {"development", "runtime"}


class SourceSnapshotError(Exception):
    """固定source treeを安全にSnapshotまたはIndex化できない。"""


@dataclasses.dataclass(frozen=True)
class SourceUniverse:
    primary_roots: tuple
    test_reference_roots: tuple


@dataclasses.dataclass(frozen=True)
class SourceFile:
    path: str
    content_sha256: str


@dataclasses.dataclass(frozen=True)
class SourceSnapshot:
    snapshot_id: str
    source_content_id: str
    head: str
    universe: SourceUniverse
    primary_files: tuple
    test_reference_files: tuple
    project_root: Path


@dataclasses.dataclass(frozen=True)
class SourceSymbol:
    symbol_id: str
    qualified_name: str
    kind: str
    source_path: str
    signature: str
    signature_sha256: str
    content_sha256: str
    snapshot_id: str


@dataclasses.dataclass(frozen=True)
class SourceSymbolIndex:
    snapshot_id: str
    entries: tuple


@dataclasses.dataclass(frozen=True)
class PersistedSourceSymbolIndexBaseline:
    """external DATA_ROOTへnew-only保存したSnapshot／Indexのidentity。"""

    snapshot_id: str
    project_id: str
    profile: str
    snapshot_path: Path
    index_path: Path
    snapshot_sha256: str
    index_sha256: str


@dataclasses.dataclass(frozen=True)
class RoutineClassificationCandidate:
    """固定Snapshotから抽出した、Human確定前のroutine分類候補。"""

    candidate_id: str
    snapshot_id: str
    rule_id: str
    symbol_ids: tuple
    evidence: tuple
    source_evidence: tuple
    status: str


@dataclasses.dataclass(frozen=True)
class RoutineClassificationReport:
    """候補と、静的解析で確定できなかった参照形式をまとめる。"""

    snapshot_id: str
    candidates: tuple
    unresolved_reference_forms: tuple


@dataclasses.dataclass(frozen=True)
class PersistedRoutineClassificationCandidates:
    """external DATA_ROOTへnew-only保存したcandidate listのidentity。"""

    snapshot_id: str
    project_id: str
    profile: str
    path: Path
    sha256: str


def _sha256(content):
    return hashlib.sha256(content).hexdigest()


def _canonical_digest(value):
    return _sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _json_bytes(value):
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _git(project_root, *arguments):
    result = subprocess.run(
        ["git", *arguments],
        cwd=project_root,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        raise SourceSnapshotError("source_snapshot_git_unavailable")
    return result.stdout


def _normalized_roots(roots):
    if not isinstance(roots, tuple) or not roots:
        raise SourceSnapshotError("source_universe_invalid")
    normalized = []
    for root in roots:
        path = PurePosixPath(root)
        if (
            not isinstance(root, str)
            or not root
            or path.is_absolute()
            or ".." in path.parts
            or path == PurePosixPath(".")
        ):
            raise SourceSnapshotError("source_universe_invalid")
        normalized.append(path.as_posix().rstrip("/"))
    if len(normalized) != len(set(normalized)):
        raise SourceSnapshotError("source_universe_invalid")
    return tuple(sorted(normalized))


def _normalized_universe(universe):
    if not isinstance(universe, SourceUniverse):
        raise SourceSnapshotError("source_universe_invalid")
    primary_roots = _normalized_roots(universe.primary_roots)
    test_reference_roots = _normalized_roots(universe.test_reference_roots)
    if set(primary_roots).intersection(test_reference_roots):
        raise SourceSnapshotError("source_universe_invalid")
    return SourceUniverse(
        primary_roots=primary_roots,
        test_reference_roots=test_reference_roots,
    )


def _belongs_to_root(path, roots):
    return any(path == root or path.startswith(f"{root}/") for root in roots)


def _tracked_python_paths(project_root, roots):
    tracked = _git(project_root, "ls-files", "-z")
    paths = []
    for item in tracked.split("\0"):
        if not item:
            continue
        path = PurePosixPath(item)
        if path.suffix != ".py" or not _belongs_to_root(path.as_posix(), roots):
            continue
        target = project_root / path
        if not target.is_file():
            raise SourceSnapshotError("source_snapshot_file_missing")
        paths.append(path.as_posix())
    return tuple(sorted(paths))


def _source_files(project_root, paths):
    return tuple(
        SourceFile(
            path=path,
            content_sha256=_sha256((project_root / path).read_bytes()),
        )
        for path in paths
    )


def _snapshot_payload(*, head, universe, primary_files, test_reference_files):
    return {
        "head": head,
        "primary_files": [dataclasses.asdict(item) for item in primary_files],
        "test_reference_files": [
            dataclasses.asdict(item)
            for item in test_reference_files
        ],
        "universe": dataclasses.asdict(universe),
    }


def _source_content_payload(*, universe, primary_files, test_reference_files):
    return {
        "primary_files": [dataclasses.asdict(item) for item in primary_files],
        "test_reference_files": [
            dataclasses.asdict(item) for item in test_reference_files
        ],
        "universe": dataclasses.asdict(universe),
    }


def capture_source_snapshot(*, project_root, universe):
    """cleanなGit worktreeから追跡済みPython sourceを固定する。"""

    root = Path(project_root).resolve()
    normalized_universe = _normalized_universe(universe)
    if _git(root, "status", "--porcelain"):
        raise SourceSnapshotError("source_snapshot_dirty")
    head = _git(root, "rev-parse", "HEAD").strip()
    primary_files = _source_files(
        root,
        _tracked_python_paths(root, normalized_universe.primary_roots),
    )
    test_reference_files = _source_files(
        root,
        _tracked_python_paths(root, normalized_universe.test_reference_roots),
    )
    snapshot_id = _canonical_digest(
        _snapshot_payload(
            head=head,
            universe=normalized_universe,
            primary_files=primary_files,
            test_reference_files=test_reference_files,
        )
    )
    source_content_id = _canonical_digest(
        _source_content_payload(
            universe=normalized_universe,
            primary_files=primary_files,
            test_reference_files=test_reference_files,
        )
    )
    return SourceSnapshot(
        snapshot_id=snapshot_id,
        source_content_id=source_content_id,
        head=head,
        universe=normalized_universe,
        primary_files=primary_files,
        test_reference_files=test_reference_files,
        project_root=root,
    )


def _validate_source_file(project_root, item):
    if not isinstance(item, SourceFile):
        raise SourceSnapshotError("source_snapshot_file_invalid")
    if not item.content_sha256:
        raise SourceSnapshotError("source_snapshot_file_digest_missing")
    if not _SHA256.fullmatch(item.content_sha256):
        raise SourceSnapshotError("source_snapshot_file_digest_invalid")
    path = PurePosixPath(item.path)
    if path.is_absolute() or ".." in path.parts or path.suffix != ".py":
        raise SourceSnapshotError("source_snapshot_file_invalid")
    target = project_root / path
    if not target.is_file():
        raise SourceSnapshotError("source_snapshot_file_missing")
    if _sha256(target.read_bytes()) != item.content_sha256:
        raise SourceSnapshotError("source_snapshot_file_digest_mismatch")


def validate_source_snapshot(*, snapshot, project_root):
    """Snapshotが現在のclean source treeを正しく束縛することを検証する。"""

    if not isinstance(snapshot, SourceSnapshot):
        raise SourceSnapshotError("source_snapshot_invalid")
    root = Path(project_root).resolve()
    if root != snapshot.project_root:
        raise SourceSnapshotError("source_snapshot_project_root_mismatch")
    universe = _normalized_universe(snapshot.universe)
    if _git(root, "status", "--porcelain"):
        raise SourceSnapshotError("source_snapshot_dirty")
    if _git(root, "rev-parse", "HEAD").strip() != snapshot.head:
        raise SourceSnapshotError("source_snapshot_head_mismatch")
    for item in (*snapshot.primary_files, *snapshot.test_reference_files):
        _validate_source_file(root, item)
    payload = _snapshot_payload(
        head=snapshot.head,
        universe=universe,
        primary_files=snapshot.primary_files,
        test_reference_files=snapshot.test_reference_files,
    )
    if _canonical_digest(payload) != snapshot.snapshot_id:
        raise SourceSnapshotError("source_snapshot_identity_mismatch")
    content_payload = _source_content_payload(
        universe=universe,
        primary_files=snapshot.primary_files,
        test_reference_files=snapshot.test_reference_files,
    )
    if _canonical_digest(content_payload) != snapshot.source_content_id:
        raise SourceSnapshotError("source_content_identity_mismatch")
    return snapshot


def _module_name(path):
    parts = list(PurePosixPath(path).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _symbol_content(source, node):
    content = ast.get_source_segment(source, node)
    if content is None:
        raise SourceSnapshotError("source_symbol_content_unavailable")
    return content.encode("utf-8")


def _symbols_from_body(
    *,
    body,
    module_name,
    source,
    source_path,
    snapshot_id,
    scope=(),
    direct_class_body=False,
):
    entries = []
    for node in body:
        if isinstance(node, ast.ClassDef):
            entries.extend(
                _symbols_from_body(
                    body=node.body,
                    module_name=module_name,
                    source=source,
                    source_path=source_path,
                    snapshot_id=snapshot_id,
                    scope=(*scope, node.name),
                    direct_class_body=True,
                )
            )
            continue
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if isinstance(node, ast.AsyncFunctionDef):
            kind = "async_method" if direct_class_body else "async_function"
        else:
            kind = "method" if direct_class_body else "function"
        qualified_name = ".".join((module_name, *scope, node.name))
        signature = f"({ast.unparse(node.args)})"
        symbol_id = f"py:{source_path}:{qualified_name}:{kind}"
        entries.append(
            SourceSymbol(
                symbol_id=symbol_id,
                qualified_name=qualified_name,
                kind=kind,
                source_path=source_path,
                signature=signature,
                signature_sha256=_sha256(signature.encode("utf-8")),
                content_sha256=_sha256(_symbol_content(source, node)),
                snapshot_id=snapshot_id,
            )
        )
        entries.extend(
            _symbols_from_body(
                body=node.body,
                module_name=module_name,
                source=source,
                source_path=source_path,
                snapshot_id=snapshot_id,
                scope=(*scope, node.name),
                direct_class_body=False,
            )
        )
    return entries


def generate_source_symbol_index(*, snapshot):
    """固定Snapshotの一次sourceからfunction／method Indexを生成する。"""

    validate_source_snapshot(
        snapshot=snapshot,
        project_root=snapshot.project_root,
    )
    entries = []
    for item in snapshot.primary_files:
        source = (snapshot.project_root / item.path).read_text(
            encoding="utf-8"
        )
        entries.extend(
            _symbols_from_body(
                body=ast.parse(source, filename=item.path).body,
                module_name=_module_name(item.path),
                source=source,
                source_path=item.path,
                snapshot_id=snapshot.snapshot_id,
            )
        )
    symbols = tuple(entries)
    if len({entry.symbol_id for entry in symbols}) != len(symbols):
        raise SourceSnapshotError("source_symbol_identity_collision")
    return SourceSymbolIndex(
        snapshot_id=snapshot.snapshot_id,
        entries=symbols,
    )


def _validate_persistence_identity(*, data_root, project_id, profile):
    root = Path(data_root)
    if not root.is_absolute():
        raise SourceSnapshotError("source_symbol_baseline_data_root_not_absolute")
    if _IDENTIFIER.fullmatch(project_id or "") is None:
        raise SourceSnapshotError("source_symbol_baseline_project_identity_invalid")
    if profile not in _PERSISTENCE_PROFILES:
        raise SourceSnapshotError("source_symbol_baseline_profile_invalid")
    return root.resolve()


def _snapshot_document(*, snapshot, project_id, profile):
    return {
        "record_kind": "source_snapshot",
        "schema_version": 1,
        "project_id": project_id,
        "profile": profile,
        "snapshot_id": snapshot.snapshot_id,
        "source_content_id": snapshot.source_content_id,
        "head": snapshot.head,
        "universe": dataclasses.asdict(snapshot.universe),
        "primary_files": [
            dataclasses.asdict(item) for item in snapshot.primary_files
        ],
        "test_reference_files": [
            dataclasses.asdict(item)
            for item in snapshot.test_reference_files
        ],
    }


def _index_document(*, index, project_id, profile):
    return {
        "record_kind": "source_symbol_index",
        "schema_version": 1,
        "project_id": project_id,
        "profile": profile,
        "snapshot_id": index.snapshot_id,
        "entries": [dataclasses.asdict(item) for item in index.entries],
    }


def _write_new_json(path, document, *, exists_error):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(_json_bytes(document))
    except FileExistsError as error:
        raise SourceSnapshotError(exists_error) from error


def persist_source_symbol_index_baseline(
    *,
    snapshot,
    index,
    data_root,
    project_id,
    profile,
):
    """Snapshot／IndexをDATA_ROOTへnew-onlyで保存し、Digestを返す。"""
    if not isinstance(index, SourceSymbolIndex):
        raise SourceSnapshotError("source_symbol_index_invalid")
    validate_source_snapshot(snapshot=snapshot, project_root=snapshot.project_root)
    if index.snapshot_id != snapshot.snapshot_id:
        raise SourceSnapshotError("source_symbol_index_snapshot_mismatch")
    root = _validate_persistence_identity(
        data_root=data_root,
        project_id=project_id,
        profile=profile,
    )
    snapshot_path = (
        root
        / "source-snapshots"
        / snapshot.snapshot_id
        / "source-snapshot-v1.json"
    )
    index_path = (
        root
        / "source-symbol-indexes"
        / snapshot.snapshot_id
        / "source-symbol-index-v1.json"
    )
    if snapshot_path.exists() or index_path.exists():
        raise SourceSnapshotError("source_symbol_baseline_already_exists")
    _write_new_json(
        snapshot_path,
        _snapshot_document(
            snapshot=snapshot,
            project_id=project_id,
            profile=profile,
        ),
        exists_error="source_symbol_baseline_already_exists",
    )
    _write_new_json(
        index_path,
        _index_document(
            index=index,
            project_id=project_id,
            profile=profile,
        ),
        exists_error="source_symbol_baseline_already_exists",
    )
    return PersistedSourceSymbolIndexBaseline(
        snapshot_id=snapshot.snapshot_id,
        project_id=project_id,
        profile=profile,
        snapshot_path=snapshot_path,
        index_path=index_path,
        snapshot_sha256=_sha256(snapshot_path.read_bytes()),
        index_sha256=_sha256(index_path.read_bytes()),
    )


def verify_persisted_source_symbol_index_baseline(
    *,
    persisted,
    snapshot,
    index,
):
    """保存物のDigestと内容を、固定Snapshot／Indexへ再読込照合する。"""
    if not isinstance(persisted, PersistedSourceSymbolIndexBaseline):
        raise SourceSnapshotError("persisted_source_symbol_index_invalid")
    if not isinstance(index, SourceSymbolIndex):
        raise SourceSnapshotError("source_symbol_index_invalid")
    validate_source_snapshot(snapshot=snapshot, project_root=snapshot.project_root)
    if (
        persisted.snapshot_id != snapshot.snapshot_id
        or index.snapshot_id != snapshot.snapshot_id
    ):
        raise SourceSnapshotError("persisted_source_symbol_index_snapshot_mismatch")
    try:
        snapshot_bytes = persisted.snapshot_path.read_bytes()
        index_bytes = persisted.index_path.read_bytes()
    except OSError as error:
        raise SourceSnapshotError("persisted_source_symbol_index_missing") from error
    if _sha256(snapshot_bytes) != persisted.snapshot_sha256:
        raise SourceSnapshotError("persisted_source_snapshot_digest_mismatch")
    if _sha256(index_bytes) != persisted.index_sha256:
        raise SourceSnapshotError("persisted_source_symbol_index_digest_mismatch")
    expected_snapshot = _json_bytes(
        _snapshot_document(
            snapshot=snapshot,
            project_id=persisted.project_id,
            profile=persisted.profile,
        )
    )
    expected_index = _json_bytes(
        _index_document(
            index=index,
            project_id=persisted.project_id,
            profile=persisted.profile,
        )
    )
    if snapshot_bytes != expected_snapshot:
        raise SourceSnapshotError("persisted_source_snapshot_content_mismatch")
    if index_bytes != expected_index:
        raise SourceSnapshotError("persisted_source_symbol_index_content_mismatch")
    return persisted


def classify_persisted_source_symbol_index_baseline(
    *,
    persisted,
    current_snapshot,
):
    """保存baselineが指定された現在Snapshotと同一かを副作用なく示す。"""
    if not isinstance(persisted, PersistedSourceSymbolIndexBaseline):
        raise SourceSnapshotError("persisted_source_symbol_index_invalid")
    if not isinstance(current_snapshot, SourceSnapshot):
        raise SourceSnapshotError("source_snapshot_invalid")
    if persisted.snapshot_id == current_snapshot.snapshot_id:
        return "current"
    return "historical"


def _function_nodes_from_body(
    *,
    body,
    module_name,
    scope=(),
    direct_class_body=False,
):
    for node in body:
        if isinstance(node, ast.ClassDef):
            yield from _function_nodes_from_body(
                body=node.body,
                module_name=module_name,
                scope=(*scope, node.name),
                direct_class_body=True,
            )
            continue
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if isinstance(node, ast.AsyncFunctionDef):
            kind = "async_method" if direct_class_body else "async_function"
        else:
            kind = "method" if direct_class_body else "function"
        qualified_name = ".".join((module_name, *scope, node.name))
        yield qualified_name, kind, node
        yield from _function_nodes_from_body(
            body=node.body,
            module_name=module_name,
            scope=(*scope, node.name),
            direct_class_body=False,
        )


def _candidate(*, snapshot_id, rule_id, symbol_ids, evidence, source_evidence):
    ordered_ids = tuple(sorted(symbol_ids))
    return RoutineClassificationCandidate(
        candidate_id=(
            f"routine-candidate:{snapshot_id}:{rule_id}:"
            + ",".join(ordered_ids)
        ),
        snapshot_id=snapshot_id,
        rule_id=rule_id,
        symbol_ids=ordered_ids,
        evidence=tuple(sorted(evidence)),
        source_evidence=tuple(sorted(source_evidence)),
        status="candidate",
    )


def _static_import_references(snapshot, symbols_by_qualified):
    references = {symbol_id: set() for symbol_id in symbols_by_qualified.values()}
    unresolved = set()
    primary_paths = {item.path for item in snapshot.primary_files}
    for item in (*snapshot.primary_files, *snapshot.test_reference_files):
        tree = ast.parse(
            (snapshot.project_root / item.path).read_text(encoding="utf-8"),
            filename=item.path,
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                for imported in node.names:
                    qualified_name = f"{node.module}.{imported.name}"
                    symbol_id = symbols_by_qualified.get(qualified_name)
                    if symbol_id is not None:
                        references[symbol_id].add(item.path)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "getattr"
            ):
                unresolved.add(f"dynamic_attribute_lookup:{item.path}")
    primary_references = {
        symbol_id: tuple(sorted(paths.intersection(primary_paths)))
        for symbol_id, paths in references.items()
    }
    return references, primary_references, tuple(sorted(unresolved))


def _contract_domain(path):
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[0] != "tools":
        return None
    return parts[1]


def _risk_categories(node):
    categories = set()
    filesystem_methods = {
        "write_bytes",
        "write_text",
        "mkdir",
        "unlink",
        "rmdir",
        "rename",
        "replace",
        "chmod",
    }
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Attribute):
            if child.func.attr in filesystem_methods:
                categories.add("filesystem_write")
            if (
                isinstance(child.func.value, ast.Name)
                and child.func.value.id == "subprocess"
            ):
                categories.add("external_process")
    return tuple(sorted(categories))


def _normalized_function_body(node):
    return ast.dump(
        ast.Module(body=list(node.body), type_ignores=[]),
        annotate_fields=True,
        include_attributes=False,
    )


def extract_routine_classification_candidates(*, snapshot, index):
    """承認済み規則からHuman確定前の静的候補を決定的に抽出する。"""
    if not isinstance(index, SourceSymbolIndex):
        raise SourceSnapshotError("source_symbol_index_invalid")
    validate_source_snapshot(snapshot=snapshot, project_root=snapshot.project_root)
    if index.snapshot_id != snapshot.snapshot_id:
        raise SourceSnapshotError("routine_classification_snapshot_mismatch")

    symbols_by_qualified = {
        entry.qualified_name: entry.symbol_id for entry in index.entries
    }
    symbols_by_id = {entry.symbol_id: entry for entry in index.entries}
    nodes_by_symbol = {}
    for item in snapshot.primary_files:
        source = (snapshot.project_root / item.path).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=item.path)
        module_name = _module_name(item.path)
        for qualified_name, kind, node in _function_nodes_from_body(
            body=tree.body,
            module_name=module_name,
        ):
            symbol_id = f"py:{item.path}:{qualified_name}:{kind}"
            if symbol_id in symbols_by_id:
                nodes_by_symbol[symbol_id] = node

    references, primary_references, unresolved = _static_import_references(
        snapshot,
        symbols_by_qualified,
    )
    candidates = []
    for symbol_id, paths in sorted(references.items()):
        if paths:
            candidates.append(
                _candidate(
                    snapshot_id=snapshot.snapshot_id,
                    rule_id="public",
                    symbol_ids=(symbol_id,),
                    evidence=tuple(f"static_import:{path}" for path in paths),
                    source_evidence=(
                        f"definition:{symbols_by_id[symbol_id].source_path}",
                    ),
                )
            )
    for symbol_id, paths in sorted(primary_references.items()):
        if len(paths) >= 2:
            candidates.append(
                _candidate(
                    snapshot_id=snapshot.snapshot_id,
                    rule_id="shared",
                    symbol_ids=(symbol_id,),
                    evidence=tuple(f"static_import:{path}" for path in paths),
                    source_evidence=(
                        f"definition:{symbols_by_id[symbol_id].source_path}",
                    ),
                )
            )
    for symbol_id, paths in sorted(primary_references.items()):
        definition_domain = _contract_domain(
            symbols_by_id[symbol_id].source_path
        )
        if definition_domain is None:
            continue
        cross_contract_paths = tuple(
            path
            for path in paths
            if (
                _contract_domain(path) is not None
                and _contract_domain(path) != definition_domain
            )
        )
        if cross_contract_paths:
            candidates.append(
                _candidate(
                    snapshot_id=snapshot.snapshot_id,
                    rule_id="cross_contract",
                    symbol_ids=(symbol_id,),
                    evidence=tuple(
                        f"static_import:{path}"
                        for path in cross_contract_paths
                    ),
                    source_evidence=(
                        f"definition:{symbols_by_id[symbol_id].source_path}",
                    ),
                )
            )
    normalized_bodies = {}
    for symbol_id, node in sorted(nodes_by_symbol.items()):
        for category in _risk_categories(node):
            candidates.append(
                _candidate(
                    snapshot_id=snapshot.snapshot_id,
                    rule_id="high_risk",
                    symbol_ids=(symbol_id,),
                    evidence=(
                        f"{category}:{symbols_by_id[symbol_id].source_path}",
                    ),
                    source_evidence=(
                        f"definition:{symbols_by_id[symbol_id].source_path}",
                    ),
                )
            )
        normalized_bodies.setdefault(
            (
                symbols_by_id[symbol_id].kind,
                symbols_by_id[symbol_id].signature,
                _normalized_function_body(node),
            ),
            [],
        ).append(symbol_id)
        docstring = ast.get_docstring(node) or ""
        if (
            not references[symbol_id]
            and "deprecated" in docstring.lower()
            and "replaced" in docstring.lower()
        ):
            candidates.append(
                _candidate(
                    snapshot_id=snapshot.snapshot_id,
                    rule_id="retired_candidate",
                    symbol_ids=(symbol_id,),
                    evidence=(
                        f"deprecation_marker:{symbols_by_id[symbol_id].source_path}",
                    ),
                    source_evidence=(
                        f"definition:{symbols_by_id[symbol_id].source_path}",
                    ),
                )
            )
    for (_kind, _signature, _body), symbol_ids in sorted(
        normalized_bodies.items(),
        key=lambda item: tuple(sorted(item[1])),
    ):
        if len(symbol_ids) < 2:
            continue
        ordered_ids = tuple(sorted(symbol_ids))
        candidates.append(
            _candidate(
                snapshot_id=snapshot.snapshot_id,
                rule_id="duplicate_candidate",
                symbol_ids=ordered_ids,
                evidence=("normalized_body_and_signature_match",),
                source_evidence=tuple(
                    f"definition:{symbols_by_id[symbol_id].source_path}"
                    for symbol_id in ordered_ids
                ),
            )
        )
    return RoutineClassificationReport(
        snapshot_id=snapshot.snapshot_id,
        candidates=tuple(
            sorted(
                candidates,
                key=lambda candidate: (
                    candidate.rule_id,
                    candidate.symbol_ids,
                ),
            )
        ),
        unresolved_reference_forms=unresolved,
    )


def _routine_classification_document(*, report, project_id, profile):
    return {
        "record_kind": "routine_classification_candidates",
        "schema_version": 1,
        "project_id": project_id,
        "profile": profile,
        "snapshot_id": report.snapshot_id,
        "candidates": [
            dataclasses.asdict(candidate) for candidate in report.candidates
        ],
        "unresolved_reference_forms": list(
            report.unresolved_reference_forms
        ),
    }


def persist_routine_classification_candidates(
    *,
    report,
    data_root,
    project_id,
    profile,
):
    """candidate listをDATA_ROOTへnew-only保存し、Digestを返す。"""
    if not isinstance(report, RoutineClassificationReport):
        raise SourceSnapshotError("routine_classification_report_invalid")
    if not _SHA256.fullmatch(report.snapshot_id):
        raise SourceSnapshotError("routine_classification_snapshot_invalid")
    root = _validate_persistence_identity(
        data_root=data_root,
        project_id=project_id,
        profile=profile,
    )
    path = (
        root
        / "routine-classification-candidates"
        / report.snapshot_id
        / "routine-classification-candidates-v1.json"
    )
    if path.exists():
        raise SourceSnapshotError("routine_classification_candidates_already_exists")
    _write_new_json(
        path,
        _routine_classification_document(
            report=report,
            project_id=project_id,
            profile=profile,
        ),
        exists_error="routine_classification_candidates_already_exists",
    )
    return PersistedRoutineClassificationCandidates(
        snapshot_id=report.snapshot_id,
        project_id=project_id,
        profile=profile,
        path=path,
        sha256=_sha256(path.read_bytes()),
    )


def verify_persisted_routine_classification_candidates(*, persisted, report):
    """candidate listのDigestと再読込内容を固定reportへ照合する。"""
    if not isinstance(persisted, PersistedRoutineClassificationCandidates):
        raise SourceSnapshotError("persisted_routine_classification_candidates_invalid")
    if not isinstance(report, RoutineClassificationReport):
        raise SourceSnapshotError("routine_classification_report_invalid")
    if persisted.snapshot_id != report.snapshot_id:
        raise SourceSnapshotError("persisted_routine_classification_snapshot_mismatch")
    try:
        actual = persisted.path.read_bytes()
    except OSError as error:
        raise SourceSnapshotError(
            "persisted_routine_classification_candidates_missing"
        ) from error
    if _sha256(actual) != persisted.sha256:
        raise SourceSnapshotError(
            "persisted_routine_classification_candidates_digest_mismatch"
        )
    expected = _json_bytes(
        _routine_classification_document(
            report=report,
            project_id=persisted.project_id,
            profile=persisted.profile,
        )
    )
    if actual != expected:
        raise SourceSnapshotError(
            "persisted_routine_classification_candidates_content_mismatch"
        )
    return persisted
