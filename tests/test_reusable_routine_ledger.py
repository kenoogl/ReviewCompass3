"""Work 4A Reusable Routine Ledger schemaのAcceptance Test。"""

import importlib
import json
from pathlib import Path

import pytest


def _module():
    return importlib.import_module("tools.development.reusable_routine_ledger")


def _project(tmp_path):
    project_root = tmp_path / "project"
    reuse_root = project_root / ".reviewcompass" / "reuse"
    reuse_root.mkdir(parents=True)
    (project_root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "project_id": "project-alpha",
                "artifact_roots": {"reuse": ".reviewcompass/reuse"},
                "document_links": [],
            }
        ),
        encoding="utf-8",
    )
    return project_root


def _entry(snapshot_id):
    return {
        "record_kind": "reusable_routine_entry",
        "entry_id": "RRL-BUNDLE-DIGEST",
        "entry_version": 1,
        "source_snapshot_id": snapshot_id,
        "symbol_bindings": [
            {
                "symbol_id": (
                    "py:tools/bootstrap/material_bundle.py:"
                    "tools.bootstrap.material_bundle.calculate_bundle_digest:function"
                ),
                "content_sha256": "a" * 64,
            }
        ],
        "responsibility": "material bundleのcanonical digestを計算する",
        "inputs": ["ordered materials"],
        "outputs": ["sha256 digest"],
        "side_effects": [],
        "constraints": ["canonical serialization"],
        "consumers": ["tools.bootstrap.bundle_verification"],
        "lifecycle": "active",
        "reuse_disposition": "reuse",
        "decision_refs": ["DEC-EXAMPLE-001"],
    }


def _relation(snapshot_id):
    return {
        "record_kind": "reusable_routine_relation",
        "relation_id": "RRL-REL-MATERIAL-DOCUMENT",
        "relation_version": 1,
        "source_snapshot_id": snapshot_id,
        "relation_kind": "duplicate_candidate",
        "participant_symbol_ids": [
            "py:tools/bootstrap/closed_payload.py:tools.bootstrap.closed_payload._material_document:function",
            "py:tools/bootstrap/material_bundle.py:tools.bootstrap.material_bundle._material_document:function",
        ],
        "rationale": "normalized body and signature match",
        "decision_refs": ["DEC-EXAMPLE-001"],
    }


def test_persists_individual_entry_and_digest_bound_baseline_in_reuse_root(
    tmp_path,
):
    module = _module()
    project_root = _project(tmp_path)
    snapshot_id = "b" * 64

    persisted = module.persist_reusable_routine_ledger(
        project_root=project_root,
        source_snapshot_id=snapshot_id,
        candidate_list_digest="c" * 64,
        entries=(_entry(snapshot_id),),
        relations=(),
        decision_refs=("DEC-WORK4A-REUSABLE-ROUTINE-LEDGER-STRUCTURE-001",),
    )

    root = project_root / ".reviewcompass" / "reuse" / "reusable-routine-ledger"
    entry_path = root / "entries" / "rrl-bundle-digest--v1.json"
    baseline_path = root / "ledger-baseline--v1.json"
    assert persisted.root == root
    assert persisted.entry_paths == (entry_path,)
    assert persisted.baseline_path == baseline_path
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert baseline["source_snapshot_id"] == snapshot_id
    assert baseline["candidate_list_digest"] == "c" * 64
    assert baseline["entry_refs"] == [
        {
            "entry_id": "RRL-BUNDLE-DIGEST",
            "entry_version": 1,
            "path": "entries/rrl-bundle-digest--v1.json",
            "sha256": persisted.entry_sha256s[0],
        }
    ]
    assert str(project_root) not in baseline_path.read_text(encoding="utf-8")
    assert module.verify_reusable_routine_ledger(persisted=persisted) == persisted


def test_rejects_snapshot_mismatch_and_reuse_root_escape(tmp_path):
    module = _module()
    project_root = _project(tmp_path)
    snapshot_id = "b" * 64
    mismatched = _entry("d" * 64)

    with pytest.raises(module.ReusableRoutineLedgerError, match="snapshot"):
        module.persist_reusable_routine_ledger(
            project_root=project_root,
            source_snapshot_id=snapshot_id,
            candidate_list_digest="c" * 64,
            entries=(mismatched,),
            relations=(),
            decision_refs=("DEC-EXAMPLE-001",),
        )


def test_persists_relation_and_binds_its_digest_from_baseline(tmp_path):
    module = _module()
    project_root = _project(tmp_path)
    snapshot_id = "b" * 64

    persisted = module.persist_reusable_routine_ledger(
        project_root=project_root,
        source_snapshot_id=snapshot_id,
        candidate_list_digest="c" * 64,
        entries=(_entry(snapshot_id),),
        relations=(_relation(snapshot_id),),
        decision_refs=("DEC-EXAMPLE-001",),
    )

    root = project_root / ".reviewcompass" / "reuse" / "reusable-routine-ledger"
    relation_path = root / "relations" / "rrl-rel-material-document--v1.json"
    assert persisted.relation_paths == (relation_path,)
    baseline = json.loads(persisted.baseline_path.read_text(encoding="utf-8"))
    assert baseline["relation_refs"] == [
        {
            "relation_id": "RRL-REL-MATERIAL-DOCUMENT",
            "relation_version": 1,
            "path": "relations/rrl-rel-material-document--v1.json",
            "sha256": persisted.relation_sha256s[0],
        }
    ]
    assert module.verify_reusable_routine_ledger(persisted=persisted) == persisted

    manifest = project_root / ".reviewcompass" / "project-manifest.json"
    document = json.loads(manifest.read_text(encoding="utf-8"))
    document["artifact_roots"]["reuse"] = "../escape"
    manifest.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(module.ReusableRoutineLedgerError, match="reuse"):
        module.persist_reusable_routine_ledger(
            project_root=project_root,
            source_snapshot_id=snapshot_id,
            candidate_list_digest="c" * 64,
            entries=(_entry(snapshot_id),),
            relations=(),
            decision_refs=("DEC-EXAMPLE-001",),
        )
