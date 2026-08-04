"""Work 4A routine classification candidate extractorのAcceptance Test。"""

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
    files = {
        "tools/api.py": '''from pathlib import Path

def public_api(value):
    return value

def shared(value):
    return value

def write_log(path, value):
    Path(path).write_text(value)

def duplicate_one(value):
    return value.strip()

def duplicate_two(value):
    return value.strip()

def old_api():
    """Deprecated: replaced by public_api."""
    return None

def unused_helper():
    return None

def same():
    return "api"

def dynamic_lookup(target, name):
    return getattr(target, name)
''',
        "tools/consumer_a.py": '''from tools.api import shared

def use_a(value):
    return shared(value)
''',
        "tools/consumer_b.py": '''from tools.api import shared

def use_b(value):
    return shared(value)
''',
        "tools/other.py": '''def same():
    return "other"
''',
        "tools/alpha/api.py": '''def cross_contract(value):
    return value
''',
        "tools/alpha/internal_consumer.py": '''from tools.alpha.api import cross_contract

def use_internal(value):
    return cross_contract(value)
''',
        "tools/beta/consumer.py": '''from tools.alpha.api import cross_contract

def use_cross_contract(value):
    return cross_contract(value)
''',
        "tests/test_api.py": '''from tools.api import public_api

def test_public_api():
    assert public_api("ok") == "ok"
''',
    }
    for relative_path, content in files.items():
        path = project_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _git(project_root, "init", "-q")
    _git(project_root, "config", "user.email", "test@example.invalid")
    _git(project_root, "config", "user.name", "Routine Candidate Test")
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


def _candidate_map(report):
    return {
        (candidate.rule_id, candidate.symbol_ids): candidate
        for candidate in report.candidates
    }


def test_extracts_deterministic_machine_candidates_with_source_evidence(
    tmp_path,
):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)

    first = module.extract_routine_classification_candidates(
        snapshot=snapshot,
        index=index,
    )
    second = module.extract_routine_classification_candidates(
        snapshot=snapshot,
        index=index,
    )
    candidates = _candidate_map(first)

    public_api = "py:tools/api.py:tools.api.public_api:function"
    shared = "py:tools/api.py:tools.api.shared:function"
    write_log = "py:tools/api.py:tools.api.write_log:function"
    duplicate_one = "py:tools/api.py:tools.api.duplicate_one:function"
    duplicate_two = "py:tools/api.py:tools.api.duplicate_two:function"
    old_api = "py:tools/api.py:tools.api.old_api:function"
    same_api = "py:tools/api.py:tools.api.same:function"
    same_other = "py:tools/other.py:tools.other.same:function"
    unused_helper = "py:tools/api.py:tools.api.unused_helper:function"
    cross_contract = (
        "py:tools/alpha/api.py:tools.alpha.api.cross_contract:function"
    )

    assert first == second
    assert first.snapshot_id == snapshot.snapshot_id
    assert candidates[("public", (public_api,))].status == "candidate"
    assert candidates[("shared", (shared,))].evidence == (
        "static_import:tools/consumer_a.py",
        "static_import:tools/consumer_b.py",
    )
    assert candidates[("high_risk", (write_log,))].evidence == (
        "filesystem_write:tools/api.py",
    )
    assert candidates[("cross_contract", (cross_contract,))].evidence == (
        "static_import:tools/beta/consumer.py",
    )
    assert candidates[
        ("duplicate_candidate", (duplicate_one, duplicate_two))
    ].status == "candidate"
    assert candidates[("retired_candidate", (old_api,))].evidence == (
        "deprecation_marker:tools/api.py",
    )
    assert ("duplicate_candidate", (same_api, same_other)) not in candidates
    assert ("retired_candidate", (unused_helper,)) not in candidates
    assert first.unresolved_reference_forms == (
        "dynamic_attribute_lookup:tools/api.py",
    )
    assert all(candidate.snapshot_id == snapshot.snapshot_id for candidate in first.candidates)
    assert all(candidate.source_evidence for candidate in first.candidates)


def test_rejects_index_with_another_snapshot_identity(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    invalid_index = dataclasses.replace(index, snapshot_id="0" * 64)

    with pytest.raises(
        module.SourceSnapshotError,
        match="routine_classification_snapshot_mismatch",
    ):
        module.extract_routine_classification_candidates(
            snapshot=snapshot,
            index=invalid_index,
        )


def test_persists_candidate_list_new_only_and_reloads_it(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    report = module.extract_routine_classification_candidates(
        snapshot=snapshot,
        index=index,
    )
    data_root = tmp_path / "data"

    persisted = module.persist_routine_classification_candidates(
        report=report,
        data_root=data_root,
        project_id="project-alpha",
        profile="development",
    )

    assert persisted.path == (
        data_root
        / "routine-classification-candidates"
        / snapshot.snapshot_id
        / "routine-classification-candidates-v1.json"
    )
    document = json.loads(persisted.path.read_text(encoding="utf-8"))
    assert document["snapshot_id"] == snapshot.snapshot_id
    assert document["project_id"] == "project-alpha"
    assert document["profile"] == "development"
    assert len(document["candidates"]) == len(report.candidates)
    assert str(project_root) not in persisted.path.read_text(encoding="utf-8")
    assert module.verify_persisted_routine_classification_candidates(
        persisted=persisted,
        report=report,
    ) == persisted

    with pytest.raises(
        module.SourceSnapshotError,
        match="routine_classification_candidates_already_exists",
    ):
        module.persist_routine_classification_candidates(
            report=report,
            data_root=data_root,
            project_id="project-alpha",
            profile="development",
        )


def test_detects_tampered_persisted_candidate_list(tmp_path):
    module = _module()
    project_root = _repository(tmp_path)
    snapshot, index = _snapshot_and_index(module, project_root)
    report = module.extract_routine_classification_candidates(
        snapshot=snapshot,
        index=index,
    )
    persisted = module.persist_routine_classification_candidates(
        report=report,
        data_root=tmp_path / "data",
        project_id="project-alpha",
        profile="development",
    )

    persisted.path.write_text("{}\n", encoding="utf-8")
    with pytest.raises(
        module.SourceSnapshotError,
        match="persisted_routine_classification_candidates_digest_mismatch",
    ):
        module.verify_persisted_routine_classification_candidates(
            persisted=persisted,
            report=report,
        )
