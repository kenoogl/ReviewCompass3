"""Work 4A Source Snapshot／Index永続化のAcceptance Test。"""

import dataclasses
import importlib
import json
from pathlib import Path
import subprocess

import pytest


def _module():
    return importlib.import_module("tools.development.source_symbol_index")


def _git(project_root, *arguments):
    result = subprocess.run(
        ["git", *arguments],
        cwd=project_root,
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def _repository(tmp_path):
    project_root = tmp_path / "project"
    (project_root / "tools").mkdir(parents=True)
    (project_root / "tests").mkdir()
    (project_root / "tools" / "alpha.py").write_text(
        "def alpha(value):\n    return value\n",
        encoding="utf-8",
    )
    (project_root / "tests" / "test_alpha.py").write_text(
        "def test_alpha():\n    assert True\n",
        encoding="utf-8",
    )
    _git(project_root, "init", "-q")
    _git(project_root, "config", "user.email", "test@example.invalid")
    _git(project_root, "config", "user.name", "Source Persistence Test")
    _git(project_root, "add", ".")
    _git(project_root, "commit", "-qm", "fixture")
    return project_root


def _snapshot_and_index(module, project_root):
    snapshot = module.capture_source_snapshot(
        project_root=project_root,
        universe=module.SourceUniverse(
            primary_roots=("tools",),
            test_reference_roots=("tests",),
        ),
    )
    return snapshot, module.generate_source_symbol_index(snapshot=snapshot)


def test_persists_new_snapshot_and_index_without_terminal_project_path(
    tmp_path,
):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    data_root = tmp_path / "data"

    persisted = module.persist_source_symbol_index_baseline(
        snapshot=snapshot,
        index=index,
        data_root=data_root,
        project_id="project-alpha",
        profile="development",
    )

    assert persisted.snapshot_path == (
        data_root
        / "source-snapshots"
        / snapshot.snapshot_id
        / "source-snapshot-v1.json"
    )
    assert persisted.index_path == (
        data_root
        / "source-symbol-indexes"
        / snapshot.snapshot_id
        / "source-symbol-index-v1.json"
    )
    snapshot_document = json.loads(
        persisted.snapshot_path.read_text(encoding="utf-8")
    )
    index_document = json.loads(
        persisted.index_path.read_text(encoding="utf-8")
    )
    assert snapshot_document["snapshot_id"] == snapshot.snapshot_id
    assert snapshot_document["project_id"] == "project-alpha"
    assert snapshot_document["profile"] == "development"
    assert index_document["snapshot_id"] == snapshot.snapshot_id
    assert index_document["entries"] == [
        dataclasses.asdict(entry) for entry in index.entries
    ]
    assert str(project_root) not in persisted.snapshot_path.read_text(
        encoding="utf-8"
    )


def test_rejects_existing_output_and_snapshot_index_mismatch(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    data_root = tmp_path / "data"
    persisted = module.persist_source_symbol_index_baseline(
        snapshot=snapshot,
        index=index,
        data_root=data_root,
        project_id="project-alpha",
        profile="development",
    )
    before = persisted.index_path.read_bytes()

    with pytest.raises(
        module.SourceSnapshotError,
        match="source_symbol_baseline_already_exists",
    ):
        module.persist_source_symbol_index_baseline(
            snapshot=snapshot,
            index=index,
            data_root=data_root,
            project_id="project-alpha",
            profile="development",
        )
    assert persisted.index_path.read_bytes() == before

    mismatched = dataclasses.replace(index, snapshot_id="0" * 64)
    with pytest.raises(
        module.SourceSnapshotError,
        match="source_symbol_index_snapshot_mismatch",
    ):
        module.persist_source_symbol_index_baseline(
            snapshot=snapshot,
            index=mismatched,
            data_root=tmp_path / "other-data",
            project_id="project-alpha",
            profile="development",
        )


def test_reloads_and_detects_tampered_persisted_output(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    persisted = module.persist_source_symbol_index_baseline(
        snapshot=snapshot,
        index=index,
        data_root=tmp_path / "data",
        project_id="project-alpha",
        profile="development",
    )

    verified = module.verify_persisted_source_symbol_index_baseline(
        persisted=persisted,
        snapshot=snapshot,
        index=index,
    )
    assert verified.snapshot_sha256 == persisted.snapshot_sha256
    assert verified.index_sha256 == persisted.index_sha256

    persisted.index_path.write_text("{}\n", encoding="utf-8")
    with pytest.raises(
        module.SourceSnapshotError,
        match="persisted_source_symbol_index_digest_mismatch",
    ):
        module.verify_persisted_source_symbol_index_baseline(
            persisted=persisted,
            snapshot=snapshot,
            index=index,
        )


def test_classifies_persisted_output_as_current_or_historical(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    persisted = module.persist_source_symbol_index_baseline(
        snapshot=snapshot,
        index=index,
        data_root=tmp_path / "data",
        project_id="project-alpha",
        profile="development",
    )

    assert module.classify_persisted_source_symbol_index_baseline(
        persisted=persisted,
        current_snapshot=snapshot,
    ) == "current"

    source = project_root / "tools" / "alpha.py"
    source.write_text("def alpha(value):\n    return value + 1\n", encoding="utf-8")
    _git(project_root, "add", "tools/alpha.py")
    _git(project_root, "commit", "-qm", "change")
    next_snapshot, _next_index = _snapshot_and_index(module, project_root)
    assert module.classify_persisted_source_symbol_index_baseline(
        persisted=persisted,
        current_snapshot=next_snapshot,
    ) == "historical"


@pytest.mark.parametrize(
    ("data_root", "project_id", "profile"),
    [
        (Path("relative-data"), "project-alpha", "development"),
        (Path("/tmp/data"), "../escape", "development"),
        (Path("/tmp/data"), "project-alpha", "stable"),
    ],
)
def test_rejects_unsafe_persistence_destination_and_identity(
    tmp_path,
    data_root,
    project_id,
    profile,
):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    if data_root.is_absolute():
        data_root = tmp_path / "data"

    with pytest.raises(module.SourceSnapshotError):
        module.persist_source_symbol_index_baseline(
            snapshot=snapshot,
            index=index,
            data_root=data_root,
            project_id=project_id,
            profile=profile,
        )
