"""Work 5A 最小Review Task Contractの受入test。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md（§8）
承認：DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001
対象は`docs/`配下の一文書変更。scenarioは`new_development / fresh`だけ。
"""

import importlib
import json
import types

import pytest


CONTRACT_ID = "TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1"
BASE_COMMIT = "a" * 40
HEAD_COMMIT = "b" * 40
HUMAN_ID = "kenoogl"
DECIDED_AT = "2026-08-05T12:00:00+09:00"
TARGET = "docs/sample-target.md"

BOUND_REQUIREMENTS = (
    "REQ-CONTRACT-001",
    "REQ-CONTRACT-002",
    "REQ-CONTRACT-003",
    "REQ-CONTRACT-004",
    "REQ-CONTRACT-005",
    "REQ-CONTEXT-001",
    "REQ-CONTEXT-002",
    "REQ-CONTEXT-003",
    "REQ-CONTEXT-004",
    "REQ-CONTEXT-005",
    "REQ-EXEC-001",
    "REQ-TRACE-002",
    "REQ-TRACE-005",
    "REQ-TRIAGE-003",
    "REQ-WORKFLOW-004",
    "REQ-WORKFLOW-005",
)

CLEAN_DOCUMENT = """# 見出し

## 目的

この文書は受入testの対象である。

## 範囲

対象は一文書だけとする。
"""

WARNING_DOCUMENT = """# 見出し

## 目的

この文書は受入testの対象である。

## 範囲

対象は一文書だけとする。TODO は後で書く。
"""

ERROR_DOCUMENT = """本文だけで見出しがない文書。
"""


@pytest.fixture
def runtime():
    return importlib.import_module("tools.task_contract")


def _project(tmp_path, *, body=CLEAN_DOCUMENT):
    root = tmp_path / "project"
    (root / "docs").mkdir(parents=True)
    (root / "records" / "requirements" / "definitions").mkdir(parents=True)
    (root / TARGET).write_text(body, encoding="utf-8")
    # B2で「定義は存在するが受け先が無い」Requirementを使うため、定義fileだけ用意する。
    for requirement_id in BOUND_REQUIREMENTS + ("REQ-EVAL-001",):
        name = requirement_id.lower().replace("req-", "req-") + "--v1.json"
        (root / "records" / "requirements" / "definitions" / name).write_text(
            json.dumps(
                {
                    "artifact_kind": "requirement_definition",
                    "requirement_id": requirement_id,
                    "requirement_version": 1,
                    "statement": f"{requirement_id}の固定文",
                },
                ensure_ascii=False, sort_keys=True, indent=2,
            ) + "\n",
            encoding="utf-8",
        )
    return root


def _chain(runtime, tmp_path, *, body=CLEAN_DOCUMENT, requirement_ids=BOUND_REQUIREMENTS):
    root = _project(tmp_path, body=body)
    binding = runtime.bind_requirements(project_root=root, requirement_ids=requirement_ids)
    snapshot = runtime.read_source_snapshot(
        project_root=root, target_paths=(TARGET,),
        base_commit=BASE_COMMIT, head_commit=HEAD_COMMIT,
    )
    contract = runtime.build_review_task_contract(
        contract_id=CONTRACT_ID, contract_version=1,
        requirement_binding=binding, target_paths=(TARGET,),
    )
    compile_verdict = runtime.compile_contract(contract=contract, requirement_binding=binding)
    context = runtime.build_context_manifest(
        contract=contract, plan_bundle=compile_verdict["plan_bundle"], source_snapshot=snapshot,
    )
    return types.SimpleNamespace(
        root=root, binding=binding, snapshot=snapshot, contract=contract,
        compile_verdict=compile_verdict, context=context,
    )


def _run_to_challenge(runtime, chain, *, workflow=None):
    workflow = workflow if workflow is not None else runtime.new_workflow_state()
    permit = runtime.acquire_permit(workflow_state=workflow, context_manifest=chain.context)
    findings = runtime.run_stub_reviewer(
        contract=chain.contract, context_manifest=chain.context, permit=permit,
    )
    conformance = runtime.evaluate_conformance(
        contract=chain.contract, plan_bundle=chain.compile_verdict["plan_bundle"],
        finding_set=findings,
    )
    challenge = runtime.evaluate_final_challenge(
        contract=chain.contract, conformance_verdict=conformance, finding_set=findings,
    )
    return workflow, permit, findings, conformance, challenge


def _full_chain(runtime, chain, *, decision="approved"):
    workflow, permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    human = runtime.record_human_decision(
        contract=chain.contract, context_manifest=chain.context, finding_set=findings,
        conformance_verdict=conformance, final_challenge_verdict=challenge,
        decision=decision, human_id=HUMAN_ID, decided_at=DECIDED_AT,
    )
    provenance = runtime.verify_provenance(
        requirement_binding=chain.binding, contract=chain.contract,
        compile_verdict=chain.compile_verdict, context_manifest=chain.context,
        permit=permit, finding_set=findings, conformance_verdict=conformance,
        final_challenge_verdict=challenge, human_decision=human,
    )
    return workflow, permit, findings, conformance, challenge, human, provenance


# ---------------------------------------------------------------- 正常例 A1〜A11


def test_a1_contract_schema_requires_every_section(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    for section in (
        "identity", "responsibility", "boundary", "preconditions", "context_obligations",
        "allowed_capabilities", "expected_output", "acceptance", "provenance_obligations",
        "escalation",
    ):
        assert section in chain.contract
    assert chain.contract["identity"]["contract_type"] == "review_task_contract"
    assert chain.contract["identity"]["origin"] == "new_development"
    assert chain.contract["identity"]["continuation"] == "fresh"
    assert chain.contract["identity"]["scheduler_policy"] == "single_active_leaf"
    with pytest.raises(runtime.ContractError) as error:
        runtime.validate_record(dict(chain.contract, responsibility=None))
    assert error.value.code in ("contract_section_missing", "schema_violation")


def test_a2_compile_produces_one_bundle_and_six_views(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    assert chain.compile_verdict["record_kind"] == "compile_verdict"
    assert chain.compile_verdict["status"] == "compiled"
    bundle = chain.compile_verdict["plan_bundle"]
    assert bundle["record_kind"] == "plan_bundle"
    assert set(bundle["views"]) == {
        "context_acquisition", "review_execution", "harness_and_capability",
        "verification", "provenance_capture", "human_interaction",
    }
    again = runtime.compile_contract(
        contract=chain.contract, requirement_binding=chain.binding
    )
    assert again["content_digest"] == chain.compile_verdict["content_digest"]


def test_a3_requirement_coverage_is_bidirectional(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    coverage = runtime.check_requirement_coverage(
        contract=chain.contract, requirement_binding=chain.binding
    )
    assert coverage["status"] == "covered"
    assert sorted(coverage["requirement_ids"]) == sorted(BOUND_REQUIREMENTS)
    assert coverage["unreceived_requirement_ids"] == []
    assert coverage["orphan_obligation_ids"] == []


def test_a4_context_manifest_fixes_materials_and_scope(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    context = chain.context
    assert context["record_kind"] == "context_manifest"
    for key in (
        "goal", "target", "constraints", "expected_output", "context_requirements",
        "validation_policy", "provenance_requirements",
    ):
        assert context["declaration"][key]
    for material in context["material_bundle"]:
        assert set(material) == {"role", "relative_path", "origin", "sha256"}
    scope = context["scope_contract"]
    assert scope["population"] and scope["in_scope"] and "exclusions" in scope
    assert context["content_digest"]


def test_a5_permit_allows_a_single_active_leaf(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    workflow = runtime.new_workflow_state()
    permit = runtime.acquire_permit(workflow_state=workflow, context_manifest=chain.context)
    assert permit["record_kind"] == "workflow_permit"
    assert permit["scheduler_policy"] == "single_active_leaf"
    assert runtime.active_leaf_count(workflow) == 1
    runtime.release_permit(workflow_state=workflow, permit=permit)
    assert runtime.active_leaf_count(workflow) == 0


def test_a6_conformance_and_challenge_run_in_order_with_distinct_owners(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    _workflow, _permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    assert findings["record_kind"] == "finding_set"
    assert conformance["record_kind"] == "conformance_verdict"
    assert challenge["record_kind"] == "final_challenge_verdict"
    assert conformance["status"] == "passed"
    assert challenge["status"] == "passed"
    assert conformance["owner"] != challenge["owner"]
    assert challenge["conformance_ref"]["content_digest"] == conformance["content_digest"]


def test_a7_human_decision_binds_target_digest(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    *_rest, human, _provenance = _full_chain(runtime, chain)
    assert human["record_kind"] == "human_decision"
    assert human["decision"] == "approved"
    assert human["human_id"] == HUMAN_ID
    assert human["target_digest"] == chain.context["content_digest"]
    assert human["decision_class"]
    assert human["owner"] not in (
        "conformance_owner", "final_challenge_owner",
    )


def test_a8_capture_plan_is_generated_before_execution(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    capture = chain.compile_verdict["plan_bundle"]["views"]["provenance_capture"]
    assert capture["capture_plan"]["required_events"]
    assert capture["capture_plan"]["generated_before_execution"] is True


def test_a9_provenance_verdict_and_accepted_artifact(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    *_rest, human, provenance = _full_chain(runtime, chain)
    assert provenance["record_kind"] == "provenance_verdict"
    assert provenance["status"] == "verified"
    assert len(provenance["edges"]) >= 9
    accepted = runtime.accept_artifact(
        provenance_verdict=provenance, human_decision=human, context_manifest=chain.context
    )
    assert accepted["record_kind"] == "accepted_artifact"
    assert accepted["target_paths"] == [TARGET]
    assert accepted["provenance_ref"]["content_digest"] == provenance["content_digest"]


def test_a10_origin_and_continuation_are_independent(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    identity = chain.contract["identity"]
    assert identity["origin"] == "new_development"
    assert identity["continuation"] == "fresh"
    assert "origin_continuation" not in identity
    assert runtime.ORIGIN_CLASSES == ("new_development", "maintenance")
    assert runtime.CONTINUATION_CLASSES == ("fresh", "reopen")


def test_a11_self_target_uses_the_same_gates(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    *_rest, provenance = _full_chain(runtime, chain)
    assert chain.contract["boundary"]["self_application"] is True
    assert chain.contract["boundary"]["gate_bypass_allowed"] is False
    assert provenance["status"] == "verified"
    gates = [edge["to"] for edge in provenance["edges"]]
    for required in ("conformance_verdict", "final_challenge_verdict", "human_decision"):
        assert required in gates


# ---------------------------------------------------------------- 負例 B1〜B10


def test_b1_missing_contract_section_is_not_compilable(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    broken = dict(chain.contract)
    del broken["escalation"]
    verdict = runtime.compile_contract(contract=broken, requirement_binding=chain.binding)
    assert verdict["status"] == "not_compilable"
    assert "plan_bundle" not in verdict


def test_b2_unreceived_obligation_stops(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    extra = runtime.bind_requirements(
        project_root=chain.root, requirement_ids=BOUND_REQUIREMENTS, allow_unreceived=True,
        additional_requirement_ids=("REQ-EVAL-001",),
    )
    verdict = runtime.compile_contract(contract=chain.contract, requirement_binding=extra)
    assert verdict["status"] == "not_compilable"
    assert "REQ-EVAL-001" in verdict["unreceived_requirement_ids"]


def test_b3_missing_context_declaration_stops(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    with pytest.raises(runtime.ContractError) as error:
        runtime.build_context_manifest(
            contract=chain.contract,
            plan_bundle=chain.compile_verdict["plan_bundle"],
            source_snapshot=chain.snapshot,
            declaration_overrides={"validation_policy": ""},
        )
    assert error.value.code == "context_incomplete"


def test_b4_context_digest_change_makes_result_stale(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    workflow, permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    (chain.root / TARGET).write_text(CLEAN_DOCUMENT + "\n追記。\n", encoding="utf-8")
    refreshed = runtime.read_source_snapshot(
        project_root=chain.root, target_paths=(TARGET,),
        base_commit=BASE_COMMIT, head_commit=HEAD_COMMIT,
    )
    with pytest.raises(runtime.ContractError) as error:
        runtime.assert_context_fresh(context_manifest=chain.context, source_snapshot=refreshed)
    assert error.value.code == "stale"


def test_b5_same_owner_for_conformance_and_challenge_is_rejected(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    _workflow, _permit, findings, conformance, _challenge = _run_to_challenge(runtime, chain)
    with pytest.raises(runtime.ContractError) as error:
        runtime.evaluate_final_challenge(
            contract=chain.contract, conformance_verdict=conformance, finding_set=findings,
            owner=conformance["owner"],
        )
    assert error.value.code == "owner_separation_violated"


def test_b6_implicit_material_is_rejected(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    (chain.root / "docs" / "other.md").write_text("別文書。\n", encoding="utf-8")
    with pytest.raises(runtime.ContractError) as error:
        runtime.build_context_manifest(
            contract=chain.contract,
            plan_bundle=chain.compile_verdict["plan_bundle"],
            source_snapshot=chain.snapshot,
            extra_material_paths=("docs/other.md",),
        )
    assert error.value.code == "implicit_material_rejected"


def test_b7_run_without_permit_is_rejected(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    with pytest.raises(runtime.ContractError) as error:
        runtime.run_stub_reviewer(
            contract=chain.contract, context_manifest=chain.context, permit=None
        )
    assert error.value.code == "not_permitted"

    workflow = runtime.new_workflow_state()
    runtime.acquire_permit(workflow_state=workflow, context_manifest=chain.context)
    with pytest.raises(runtime.ContractError) as second:
        runtime.acquire_permit(workflow_state=workflow, context_manifest=chain.context)
    assert second.value.code == "not_permitted"


def test_b8_broken_provenance_edge_is_not_verified(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    workflow, permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    human = runtime.record_human_decision(
        contract=chain.contract, context_manifest=chain.context, finding_set=findings,
        conformance_verdict=conformance, final_challenge_verdict=challenge,
        decision="approved", human_id=HUMAN_ID, decided_at=DECIDED_AT,
    )
    with pytest.raises(runtime.ContractError) as error:
        runtime.verify_provenance(
            requirement_binding=chain.binding, contract=chain.contract,
            compile_verdict=chain.compile_verdict, context_manifest=chain.context,
            permit=permit, finding_set=findings, conformance_verdict=conformance,
            final_challenge_verdict=None, human_decision=human,
        )
    assert error.value.code == "provenance_edge_missing"


def test_b9_human_decision_digest_mismatch_is_rejected(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    workflow, permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    human = runtime.record_human_decision(
        contract=chain.contract, context_manifest=chain.context, finding_set=findings,
        conformance_verdict=conformance, final_challenge_verdict=challenge,
        decision="approved", human_id=HUMAN_ID, decided_at=DECIDED_AT,
    )
    tampered = dict(human, target_digest="0" * 64)
    with pytest.raises(runtime.ContractError) as error:
        runtime.verify_provenance(
            requirement_binding=chain.binding, contract=chain.contract,
            compile_verdict=chain.compile_verdict, context_manifest=chain.context,
            permit=permit, finding_set=findings, conformance_verdict=conformance,
            final_challenge_verdict=challenge, human_decision=tampered,
        )
    assert error.value.code == "decision_digest_mismatch"


def test_b10_error_finding_and_rejection_block_accepted_artifact(runtime, tmp_path):
    chain = _chain(runtime, tmp_path, body=ERROR_DOCUMENT)
    _workflow, _permit, findings, conformance, _challenge = _run_to_challenge(runtime, chain)
    assert any(item["severity"] == "error" for item in findings["findings"])
    assert conformance["status"] == "failed"

    clean = _chain(runtime, tmp_path / "second")
    *_rest, human, provenance = _full_chain(runtime, clean, decision="rejected")
    assert human["decision"] == "rejected"
    with pytest.raises(runtime.ContractError) as error:
        runtime.accept_artifact(
            provenance_verdict=provenance, human_decision=human,
            context_manifest=clean.context,
        )
    assert error.value.code == "human_decision_not_approved"


# ---------------------------------------------------------------- 境界例 C1〜C4


def test_c1_zero_findings_completes_the_normal_path(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    *_rest, human, provenance = _full_chain(runtime, chain)
    findings = _rest[2]
    assert findings["findings"] == []
    assert provenance["status"] == "verified"
    accepted = runtime.accept_artifact(
        provenance_verdict=provenance, human_decision=human, context_manifest=chain.context
    )
    assert accepted["record_kind"] == "accepted_artifact"


def test_c2_warning_only_still_requires_human_decision(runtime, tmp_path):
    chain = _chain(runtime, tmp_path, body=WARNING_DOCUMENT)
    _workflow, _permit, findings, conformance, challenge = _run_to_challenge(runtime, chain)
    severities = {item["severity"] for item in findings["findings"]}
    assert severities == {"warning"}
    assert conformance["status"] == "passed"
    assert challenge["status"] == "passed"
    assert challenge["human_decision_required"] is True

    with pytest.raises(runtime.ContractError) as error:
        runtime.accept_artifact(
            provenance_verdict={"record_kind": "provenance_verdict", "status": "verified",
                                "content_digest": "0" * 64},
            human_decision=None, context_manifest=chain.context,
        )
    assert error.value.code == "human_decision_missing"


def test_c3_minimal_change_set_passes_every_stage(runtime, tmp_path):
    chain = _chain(runtime, tmp_path)
    assert len(chain.snapshot["files"]) == 1
    assert chain.snapshot["change_set"]["changed_paths"] == [TARGET]
    *_rest, human, provenance = _full_chain(runtime, chain)
    assert provenance["status"] == "verified"
    accepted = runtime.accept_artifact(
        provenance_verdict=provenance, human_decision=human, context_manifest=chain.context
    )
    assert accepted["target_paths"] == [TARGET]


def test_c4_second_candidate_does_not_start_concurrently(runtime, tmp_path):
    first = _chain(runtime, tmp_path)
    second = _chain(runtime, tmp_path / "second")
    workflow = runtime.new_workflow_state()
    permit = runtime.acquire_permit(workflow_state=workflow, context_manifest=first.context)
    with pytest.raises(runtime.ContractError) as error:
        runtime.acquire_permit(workflow_state=workflow, context_manifest=second.context)
    assert error.value.code == "not_permitted"
    assert runtime.active_leaf_count(workflow) == 1
    assert workflow["waiting_candidates"]
    runtime.release_permit(workflow_state=workflow, permit=permit)
    later = runtime.acquire_permit(workflow_state=workflow, context_manifest=second.context)
    assert later["record_kind"] == "workflow_permit"
    assert runtime.active_leaf_count(workflow) == 1
