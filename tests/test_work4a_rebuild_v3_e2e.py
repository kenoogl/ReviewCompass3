"""Work 4A v3設計§17 A〜Hの受入test。

正本：docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md
承認：DEC-WORK4A-REBUILD-DESIGN-003
"""

import importlib
import json
import shutil
import types
from pathlib import Path

import pytest

from shared_fixtures import work4a_manifest


UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
PROJECT_ID = "reviewcompass3"
HEAD_A = "a" * 40
HEAD_B = "b" * 40
CAPTURED_AT = "2026-08-04T20:00:00+09:00"
DECIDED_AT = "2026-08-04T21:00:00+09:00"
DISPOSITIONS = ("reuse", "extend", "merge", "split", "new")
ALPHA_SYMBOL = "tools/development/alpha.py:alpha_one"
BETA_SYMBOL = "tools/development/beta.py:beta_one"


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild_v3")


def _manifest(project_id):
    return work4a_manifest(project_id)


def _project(tmp_path, project_id=PROJECT_ID):
    root = tmp_path / "project"
    (root / "tools" / "development").mkdir(parents=True)
    (root / "docs" / "development").mkdir(parents=True)
    for name in ("contracts", "design-decisions", "policies", "reuse"):
        (root / ".reviewcompass" / name).mkdir(parents=True)
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(_manifest(project_id), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "tools" / "development" / "alpha.py").write_text(
        "def alpha_one():\n    return 1\n", encoding="utf-8"
    )
    (root / "tools" / "development" / "beta.py").write_text(
        "def beta_one():\n    return 2\n", encoding="utf-8"
    )
    development = root / "docs" / "development" / "development-policy.md"
    development.write_text("development policy v1\n", encoding="utf-8")
    return root, development


def _entry(entry_id, symbol_id, responsibility):
    return {
        "entry_id": entry_id,
        "symbol_id": symbol_id,
        "responsibility": responsibility,
        "side_effects": "none",
        "disposition": "reuse",
    }


def _chain(rebuild, tmp_path, *, project_id=PROJECT_ID, head=HEAD_A, profile="development"):
    root, development = _project(tmp_path, project_id=project_id)
    runtime = tmp_path / "runtime"
    universe = rebuild.write_source_universe(
        project_root=root,
        universe_id=UNIVERSE_ID,
        universe_version=1,
        development_policy_path=development,
    )
    policy = rebuild.write_freshness_policy(
        project_root=root,
        policy_id=POLICY_ID,
        policy_version=1,
        development_policy_path=development,
        change_class="ordinary",
    )
    observation = rebuild.capture_observation(
        project_root=root,
        runtime_root=runtime,
        profile=profile,
        universe=universe,
        policy=policy,
        head=head,
        tool_version="v3",
        captured_at=CAPTURED_AT,
    )
    candidates = rebuild.build_candidate_run(observation=observation)
    attestation = rebuild.write_attestation(
        project_root=root, observation=observation, candidates=candidates
    )
    decision = rebuild.write_operational_decision(
        project_root=root,
        decision_id="DEC-WORK4A-OPS-001",
        attestation=attestation,
        approved_targets=({"symbol_id": ALPHA_SYMBOL, "disposition": "reuse"},),
        human_id="kenoogl",
        decided_at=DECIDED_AT,
    )
    baseline = rebuild.append_baseline(
        project_root=root,
        attestation=attestation,
        decision=decision,
        policy=policy,
        universe=universe,
        entries=(_entry("RRL-ALPHA-ONE", ALPHA_SYMBOL, "alpha routine"),),
        relations=(),
        prior=None,
    )
    return types.SimpleNamespace(
        root=root,
        development=development,
        runtime=runtime,
        universe=universe,
        policy=policy,
        observation=observation,
        candidates=candidates,
        attestation=attestation,
        decision=decision,
        baseline=baseline,
    )


def _ledger_files(root):
    ledger = root / ".reviewcompass" / "reuse" / "reusable-routine-ledger"
    return sorted(str(path.relative_to(ledger)) for path in ledger.rglob("*") if path.is_file())


# A. 参照モデル


def test_a1_chain_closes_with_project_refs_only(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    text = chain.baseline.path.read_text(encoding="utf-8")
    document = json.loads(text)
    references = [
        document["universe_ref"],
        document["policy_ref"],
        document["attestation_ref"],
        document["decision_ref"],
        *document["entry_refs"],
        *document["relation_refs"],
    ]
    assert len(references) == 5
    for reference in references:
        assert reference["root_kind"] == "project"
        assert not reference["relative_path"].startswith("/")
        assert ".." not in Path(reference["relative_path"]).parts
    assert "advisory_locator" not in text
    assert "root_kind\": \"data\"" not in text
    assert str(tmp_path) not in text
    state = rebuild.validate_current(project_root=chain.root)
    assert state.baseline_version == 1


def test_a2_decision_schema_rejects_external_reference_field(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document = json.loads(chain.decision.path.read_text(encoding="utf-8"))
    document["candidate_ref"] = {"root_kind": "data", "relative_path": "work4a/candidates/x.json"}
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_record_schema(document, record_kind="work4a_operational_decision")
    assert error.value.code == "unknown_field"


# B. 外部非依存


def test_b1_current_is_validated_without_data_root(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    shutil.rmtree(chain.runtime)
    state = rebuild.validate_current(
        project_root=chain.root, runtime_root=chain.runtime, profile="development"
    )
    assert state.baseline_version == 1
    assert "locator_unresolved" in state.annotations


def test_b2_locator_of_other_profile_is_not_collated(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    state = rebuild.validate_current(
        project_root=chain.root, runtime_root=chain.runtime, profile="runtime"
    )
    assert state.baseline_version == 1
    assert "locator_profile_mismatch" in state.annotations
    assert "locator_unresolved" not in state.annotations


# C. 外部照合


def test_c1_tampered_candidate_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    chain.candidates.path.write_text("tampered\n", encoding="utf-8")
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(
            project_root=chain.root, runtime_root=chain.runtime, profile="development"
        )
    assert error.value.code == "observation_tampered"


def test_c2_foreign_project_data_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    manifest_path = chain.root / ".reviewcompass" / "project-manifest.json"
    document = json.loads(manifest_path.read_text(encoding="utf-8"))
    document["project_id"] = "other-project"
    manifest_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(
            project_root=chain.root, runtime_root=chain.runtime, profile="development"
        )
    assert error.value.code == "foreign_project_data"


def test_c3_data_root_escape_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    outside = tmp_path / "outside-candidate.json"
    outside.write_text(chain.candidates.path.read_text(encoding="utf-8"), encoding="utf-8")
    chain.candidates.path.unlink()
    chain.candidates.path.symlink_to(outside)
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(
            project_root=chain.root, runtime_root=chain.runtime, profile="development"
        )
    assert error.value.code == "data_root_escape"


# D. path安全性


def test_d1_project_ref_rejects_traversal_absolute_and_symlink(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    reference = json.loads(chain.baseline.path.read_text(encoding="utf-8"))["policy_ref"]

    with pytest.raises(rebuild.V3ValidationError) as traversal:
        rebuild.verify_project_ref(
            project_root=chain.root, reference=dict(reference, relative_path="../outside.json")
        )
    assert traversal.value.code == "path_traversal"

    with pytest.raises(rebuild.V3ValidationError) as absolute:
        rebuild.verify_project_ref(
            project_root=chain.root,
            reference=dict(reference, relative_path=str(tmp_path / "outside.json")),
        )
    assert absolute.value.code == "path_traversal"

    link = chain.root / ".reviewcompass" / "policies" / "linked-policy.json"
    link.symlink_to(chain.policy.path)
    with pytest.raises(rebuild.V3ValidationError) as symlink:
        rebuild.verify_project_ref(
            project_root=chain.root,
            reference=dict(reference, relative_path=".reviewcompass/policies/linked-policy.json"),
        )
    assert symlink.value.code == "non_regular_file"


def test_d2_root_overlap_stops_before_policy(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    vocabulary = json.loads(chain.policy.path.read_text(encoding="utf-8"))
    assert "invalid_layout" not in vocabulary["verification_outcome_classes"]
    chain.policy.path.unlink()
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(
            project_root=chain.root,
            runtime_root=chain.root / "runtime-inside",
            profile="development",
        )
    assert error.value.code == "root_overlap"
    assert error.value.classification == "invalid_layout"


# E. 同一性と鮮度


def test_e1_stale_observation_reuse_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    (chain.root / "tools" / "development" / "beta.py").write_text(
        "def beta_one():\n    return 3\n", encoding="utf-8"
    )
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.append_baseline(
            project_root=chain.root,
            attestation=chain.attestation,
            decision=chain.decision,
            policy=chain.policy,
            universe=chain.universe,
            entries=(_entry("RRL-BETA-ONE", BETA_SYMBOL, "beta routine"),),
            relations=(),
            prior=chain.baseline,
        )
    assert error.value.code == "stale_observation_reuse"


def test_e2_head_only_change_is_continuous_fresh(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    receipt = rebuild.evaluate_continuity(
        project_root=chain.root,
        runtime_root=chain.runtime,
        profile="development",
        head=HEAD_B,
        captured_at=CAPTURED_AT,
    )
    assert receipt.state == "continuous_fresh"
    assert receipt.permits_baseline_advance is True


def test_e3_content_and_universe_divergence_block_advance(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    (chain.root / "tools" / "development" / "beta.py").write_text(
        "def beta_one():\n    return 3\n", encoding="utf-8"
    )
    content = rebuild.evaluate_continuity(
        project_root=chain.root,
        runtime_root=chain.runtime,
        profile="development",
        head=HEAD_A,
        captured_at=CAPTURED_AT,
    )
    assert content.state == "content_diverged"
    assert content.permits_baseline_advance is False

    universe_v2 = rebuild.write_source_universe(
        project_root=chain.root,
        universe_id="SRCU-WORK4A-TOOLS-PY-V2",
        universe_version=2,
        development_policy_path=chain.development,
    )
    universe = rebuild.evaluate_continuity(
        project_root=chain.root,
        runtime_root=chain.runtime,
        profile="development",
        head=HEAD_A,
        captured_at=CAPTURED_AT,
        universe=universe_v2,
    )
    assert universe.state == "universe_diverged"
    assert universe.permits_baseline_advance is False


def test_e4_attestation_content_identity_mismatch(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    document["candidate_run"]["source_content_id"] = "0" * 64
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_attestation_document(
            document, project_id=PROJECT_ID, disposition_classes=DISPOSITIONS
        )
    assert error.value.code == "content_identity_mismatch"

    unlinked = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    unlinked["candidate_run"]["observation_snapshot_id"] = "1" * 64
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_attestation_document(
            unlinked, project_id=PROJECT_ID, disposition_classes=DISPOSITIONS
        )
    assert second.value.code == "unlinked_candidate"


def test_e5_decision_candidate_mismatch(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    attestation = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    decision = json.loads(chain.decision.path.read_text(encoding="utf-8"))
    decision["approved_candidate_content_digest"] = "0" * 64
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_decision_against_attestation(decision, attestation)
    assert error.value.code == "decision_candidate_mismatch"


# F. 台帳の不変性


def test_f1_new_only_keeps_existing_records(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    baseline_bytes = chain.baseline.path.read_bytes()
    entry_bytes = {path: path.read_bytes() for path in chain.baseline.entry_paths}
    second = rebuild.append_baseline(
        project_root=chain.root,
        attestation=chain.attestation,
        decision=chain.decision,
        policy=chain.policy,
        universe=chain.universe,
        entries=(_entry("RRL-BETA-ONE", BETA_SYMBOL, "beta routine"),),
        relations=(
            {
                "relation_id": "RRL-REL-ALPHA-BETA",
                "left_entry_id": "RRL-ALPHA-ONE",
                "right_entry_id": "RRL-BETA-ONE",
                "relation_kind": "extends",
                "rationale": "beta extends alpha",
            },
        ),
        prior=chain.baseline,
    )
    assert second.baseline_version == 2
    assert chain.baseline.path.read_bytes() == baseline_bytes
    for path, data in entry_bytes.items():
        assert path.read_bytes() == data
    document = json.loads(second.path.read_text(encoding="utf-8"))
    assert len(document["entry_refs"]) == 2
    assert len(document["relation_refs"]) == 1
    assert rebuild.validate_current(project_root=chain.root).baseline_version == 2


def test_f2_missing_baseline_version_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    rebuild.append_baseline(
        project_root=chain.root,
        attestation=chain.attestation,
        decision=chain.decision,
        policy=chain.policy,
        universe=chain.universe,
        entries=(_entry("RRL-BETA-ONE", BETA_SYMBOL, "beta routine"),),
        relations=(),
        prior=chain.baseline,
    )
    chain.baseline.path.unlink()
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(project_root=chain.root)
    assert error.value.code == "baseline_series_broken"


def test_f3_failed_write_leaves_nothing(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    before = _ledger_files(chain.root)
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.append_baseline(
            project_root=chain.root,
            attestation=chain.attestation,
            decision=chain.decision,
            policy=chain.policy,
            universe=chain.universe,
            entries=(_entry("RRL-ALPHA-ONE", ALPHA_SYMBOL, "duplicate"),),
            relations=(),
            prior=chain.baseline,
        )
    assert error.value.code == "immutable_violation"
    assert _ledger_files(chain.root) == before


# G. Policyとlegacy


def test_g1_missing_policy_or_decision_stops(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    chain.policy.path.unlink()
    with pytest.raises(rebuild.V3ValidationError) as missing_policy:
        rebuild.append_baseline(
            project_root=chain.root,
            attestation=chain.attestation,
            decision=chain.decision,
            policy=chain.policy,
            universe=chain.universe,
            entries=(_entry("RRL-BETA-ONE", BETA_SYMBOL, "beta routine"),),
            relations=(),
            prior=chain.baseline,
        )
    assert missing_policy.value.code == "missing_record"

    other = _chain(rebuild, tmp_path / "second")
    other.decision.path.unlink()
    with pytest.raises(rebuild.V3ValidationError) as missing_decision:
        rebuild.append_baseline(
            project_root=other.root,
            attestation=other.attestation,
            decision=other.decision,
            policy=other.policy,
            universe=other.universe,
            entries=(_entry("RRL-BETA-ONE", BETA_SYMBOL, "beta routine"),),
            relations=(),
            prior=other.baseline,
        )
    assert missing_decision.value.code == "missing_record"


def test_g2_security_policy_change_requires_revalidation(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    rebuild.write_freshness_policy(
        project_root=chain.root,
        policy_id=POLICY_ID,
        policy_version=2,
        development_policy_path=chain.development,
        change_class="security",
    )
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_current(project_root=chain.root)
    assert error.value.code == "policy_revalidation_required"


def test_g3_legacy_contract_requires_full_evidence(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    contract = chain.root / "records" / "task-contract" / "legacy-v1.json"
    contract.parent.mkdir(parents=True)
    contract.write_text('{"status": "active"}\n', encoding="utf-8")

    insufficient = rebuild.record_historical_status(
        project_root=chain.root,
        contract_path=contract,
        creation_commit=None,
        creation_policy_ref=None,
        human_decision_id=None,
    )
    assert insufficient.outcome == "evidence_insufficient"
    assert insufficient.permits_current_start is False
    assert insufficient.path.is_relative_to(
        chain.root / ".reviewcompass" / "contracts" / "historical-status"
    )

    complete = rebuild.record_historical_status(
        project_root=chain.root,
        contract_path=contract,
        creation_commit="c" * 40,
        creation_policy_ref=rebuild.build_project_ref(
            project_root=chain.root,
            path=chain.policy.path,
            record_kind="work4a_freshness_policy",
            record_id=POLICY_ID,
            version=1,
        ),
        human_decision_id="DEC-WORK4A-HISTORICAL-001",
    )
    assert complete.outcome == "completed_historical"
    assert complete.permits_current_start is False


# H. 要約


def test_h1_summary_vocabulary_violation(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    unknown_key = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    unknown_key["candidate_summary"]["classification_counts"]["unknown"] = 1
    with pytest.raises(rebuild.V3ValidationError) as first:
        rebuild.validate_attestation_document(
            unknown_key, project_id=PROJECT_ID, disposition_classes=DISPOSITIONS
        )
    assert first.value.code == "summary_vocabulary_violation"

    sensitive = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    sensitive["candidate_summary"]["sensitive_content_included"] = True
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_attestation_document(
            sensitive, project_id=PROJECT_ID, disposition_classes=DISPOSITIONS
        )
    assert second.value.code == "summary_vocabulary_violation"


def test_h2_symbol_id_list_digest_is_recomputable(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document = json.loads(chain.attestation.path.read_text(encoding="utf-8"))
    summary = document["candidate_summary"]
    assert summary["candidate_count"] == 2
    assert summary["sensitive_content_included"] is False
    assert set(summary["classification_counts"]) <= set(DISPOSITIONS)
    again = rebuild.build_candidate_run(observation=chain.observation)
    assert again.symbol_id_list_digest == summary["symbol_id_list_digest"]
    assert rebuild.symbol_id_list_digest((ALPHA_SYMBOL, BETA_SYMBOL)) == summary[
        "symbol_id_list_digest"
    ]
