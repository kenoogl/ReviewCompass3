"""Work 5A Definition ChallengeとHuman Contract approval gateの受入Test。

正本設計：docs/design/2026-08-05-work5a-definition-challenge-proposal.md（§3〜§6）
Amendment：docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md
承認：DEC-WORK5A-DEFINITION-CHALLENGE-001、DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001
指示：records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md

正常経路は次の順序だけである。

    Requirement definition / binding → draft Contract v2 → material set
    → Definition Challenge verdict → Human Contract approval → compile / Plan bundle
    → Context Manifest → Workflow permit → Finding set → Conformance
    → Final Challenge → Human review acceptance → Provenance → accepted artifact

Contract version 1の既存経路（9 node、8 edge）は変更せずそのまま通す。
"""

import importlib
import json
import types
from pathlib import Path

import pytest


CONTRACT_V1_ID = "TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1"
CONTRACT_V2_ID = "TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2"
# 「別Contract」の負例では、record identityまで別にしないと同じrecordになる。
OTHER_CONTRACT_V2_ID = "TC-RC3-REVIEW-OTHER-DOC-CHANGE-2026-08-05-V2"
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
DEFERRED_REQUIREMENT = "REQ-EVAL-001"

MATERIAL_DOCUMENTS = (
    "docs/development/2026-08-02-development-policy.md",
    "docs/current/reviewcompass3-plan-current.md",
    "docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md",
)

CLEAN_DOCUMENT = """# 見出し

## 目的

この文書は受入testの対象である。
"""

V2_NODE_ROLES = (
    "requirement_binding",
    "review_task_contract",
    "definition_challenge_verdict",
    "contract_approval",
    "compile_verdict",
    "context_manifest",
    "workflow_permit",
    "finding_set",
    "conformance_verdict",
    "final_challenge_verdict",
    "human_decision",
)
V1_NODE_ROLES = (
    "requirement_binding",
    "review_task_contract",
    "compile_verdict",
    "context_manifest",
    "workflow_permit",
    "finding_set",
    "conformance_verdict",
    "final_challenge_verdict",
    "human_decision",
)


@pytest.fixture
def runtime():
    return importlib.import_module("tools.task_contract")


@pytest.fixture
def identity():
    return importlib.import_module("tools.task_contract.identity")


def _project(tmp_path):
    """一時directoryだけで完結するproject。実projectへは書かない。"""

    root = tmp_path / "project"
    (root / "docs").mkdir(parents=True)
    (root / "records" / "requirements" / "definitions").mkdir(parents=True)
    (root / TARGET).write_text(CLEAN_DOCUMENT, encoding="utf-8")
    for requirement_id in BOUND_REQUIREMENTS + (DEFERRED_REQUIREMENT,):
        name = f"{requirement_id.lower()}--v1.json"
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
    for relative in MATERIAL_DOCUMENTS:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {relative}\n\n固定材料。\n", encoding="utf-8")
    return root


def _material_paths():
    return tuple(
        f"records/requirements/definitions/{requirement_id.lower()}--v1.json"
        for requirement_id in BOUND_REQUIREMENTS
    ) + MATERIAL_DOCUMENTS


def _v1(runtime, root, *, requirement_ids=BOUND_REQUIREMENTS, allow_unreceived=False):
    binding = runtime.bind_requirements(
        project_root=root,
        requirement_ids=requirement_ids,
        allow_unreceived=allow_unreceived,
    )
    contract = runtime.build_review_task_contract(
        contract_id=CONTRACT_V1_ID, contract_version=1,
        requirement_binding=binding, target_paths=(TARGET,),
    )
    return binding, contract


def _v2(runtime, root, **overrides):
    """draft Contract version 2をnew-onlyで作る。version 1は上書きしない。"""

    requirement_ids = overrides.pop("requirement_ids", BOUND_REQUIREMENTS)
    allow_unreceived = overrides.pop("allow_unreceived", False)
    binding, version_one = _v1(
        runtime, root, requirement_ids=requirement_ids, allow_unreceived=allow_unreceived
    )
    arguments = {
        "contract_id": CONTRACT_V2_ID,
        "contract_version": 2,
        "requirement_binding": binding,
        "target_paths": (TARGET,),
        "supersedes": runtime.record_ref(version_one),
    }
    arguments.update(overrides)
    contract = runtime.build_review_task_contract(**arguments)
    return types.SimpleNamespace(
        root=root, binding=binding, version_one=version_one, contract=contract
    )


def _materials(runtime, draft, **overrides):
    arguments = {
        "project_root": draft.root,
        "contract": draft.contract,
        "material_paths": _material_paths(),
    }
    arguments.update(overrides)
    return runtime.build_definition_challenge_material_set(**arguments)


def _challenge(runtime, draft, *, material_set=None, **overrides):
    arguments = {
        "project_root": draft.root,
        "contract": draft.contract,
        "requirement_binding": draft.binding,
        "material_set": material_set if material_set is not None else _materials(runtime, draft),
    }
    arguments.update(overrides)
    return runtime.run_definition_challenge(**arguments)


def _approval(runtime, draft, verdict, *, decision="approved", **overrides):
    arguments = {
        "contract": draft.contract,
        "definition_challenge_verdict": verdict,
        "decision": decision,
        "human_id": HUMAN_ID,
        "decided_at": DECIDED_AT,
    }
    arguments.update(overrides)
    return runtime.build_contract_approval(**arguments)


def _gated(runtime, tmp_path):
    """passed Challengeとapproved approvalまで進めたversion 2の材料一式。"""

    draft = _v2(runtime, _project(tmp_path))
    verdict = _challenge(runtime, draft)
    approval = _approval(runtime, draft, verdict)
    return draft, verdict, approval


def _codes(verdict):
    return {finding["check_id"] for finding in verdict["findings"]}


# ------------------------------------------------------------ G1〜G4：正常例


def test_g1_valid_draft_contract_v2_passes_with_no_findings(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))

    verdict = _challenge(runtime, draft)

    assert verdict["record_kind"] == "definition_challenge_verdict"
    assert verdict["status"] == "passed"
    assert verdict["blocking_count"] == 0
    assert verdict["findings"] == []
    assert verdict["checks"] == ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    assert verdict["owner"] == runtime.DEFINITION_CHALLENGE_OWNER
    assert verdict["contract_ref"] == runtime.record_ref(draft.contract)


def test_g2_compile_requires_a_passed_challenge(runtime, tmp_path):
    draft, verdict, approval = _gated(runtime, tmp_path)

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict, contract_approval=approval,
    )

    assert compiled["status"] == "compiled"
    assert compiled["plan_bundle"]["record_kind"] == "plan_bundle"
    assert compiled["definition_challenge_ref"] == runtime.record_ref(verdict)


def test_g3_definition_challenge_precedes_compile_in_provenance(runtime, tmp_path):
    chain = _v2_chain(runtime, tmp_path)

    roles = [node["node_role"] for node in chain.provenance["verified_nodes"]]

    assert roles.index("definition_challenge_verdict") < roles.index("compile_verdict")
    assert not any(
        edge["from"]["node_role"] == edge["to"]["node_role"]
        for edge in chain.provenance["verified_edges"]
    )


def test_g4_contract_v2_declares_receivers_and_distinct_owners(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))

    receivers = draft.contract["requirement_receivers"]
    owners = draft.contract["review_owners"]

    assert sorted(receivers) == sorted(BOUND_REQUIREMENTS)
    for requirement_id, section in receivers.items():
        assert section in runtime.CONTRACT_SECTIONS, requirement_id
        assert draft.contract[section], f"{requirement_id} -> {section} が空である"
    for role in ("definition_challenge", "conformance", "final_challenge", "human_decision"):
        assert owners[role]
    values = list(owners.values())
    assert len(values) == len(set(values)), "review ownerはpairwise distinctである"
    assert draft.contract["supersedes"]["record_id"] == CONTRACT_V1_ID


# ------------------------------------------------------- G5〜G8：approval gate


def test_g5_compile_requires_both_passed_challenge_and_approved_approval(
    runtime, tmp_path
):
    draft, verdict, approval = _gated(runtime, tmp_path)

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict, contract_approval=approval,
    )

    assert compiled["status"] == "compiled"
    assert compiled["contract_approval_ref"] == runtime.record_ref(approval)


def test_g6_contract_approval_binds_contract_and_challenge(runtime, tmp_path):
    draft, verdict, approval = _gated(runtime, tmp_path)

    assert approval["record_kind"] == "contract_approval"
    assert approval["decision"] == "approved"
    assert approval["decision_class"] == "contract_definition_approval"
    assert approval["owner"] == runtime.CONTRACT_APPROVAL_OWNER
    assert approval["human_id"] == HUMAN_ID
    assert approval["decided_at"] == DECIDED_AT
    assert approval["contract_ref"] == runtime.record_ref(draft.contract)
    assert approval["definition_challenge_ref"] == runtime.record_ref(verdict)
    assert approval["owner"] != verdict["owner"]


def test_g7_contract_v2_provenance_has_eleven_nodes_and_ten_edges(runtime, tmp_path):
    chain = _v2_chain(runtime, tmp_path)

    verdict = chain.provenance
    assert [node["node_role"] for node in verdict["verified_nodes"]] == list(V2_NODE_ROLES)
    assert len(verdict["verified_edges"]) == 10
    approval_node = _node(verdict, "contract_approval")
    assert approval_node["record_id"] == chain.approval["record_id"]
    assert approval_node["content_digest"] == chain.approval["content_digest"]
    pairs = [
        (edge["from"]["node_role"], edge["to"]["node_role"])
        for edge in verdict["verified_edges"]
    ]
    assert ("definition_challenge_verdict", "contract_approval") in pairs
    assert ("contract_approval", "compile_verdict") in pairs
    assert verdict["closure"]["self_edge_present"] is False


def test_g8_contract_version_one_path_is_unchanged(runtime, tmp_path):
    chain = _v1_chain(runtime, tmp_path)

    assert chain.compile_verdict["status"] == "compiled"
    assert [node["node_role"] for node in chain.provenance["verified_nodes"]] == list(
        V1_NODE_ROLES
    )
    assert len(chain.provenance["verified_edges"]) == 8
    accepted = runtime.accept_artifact(
        provenance_verdict=chain.provenance, human_decision=chain.human,
        context_manifest=chain.context,
    )
    assert accepted["record_kind"] == "accepted_artifact"


# ------------------------------------------------------------ D1〜D8：負例


def test_h1_unreceived_bound_requirement_is_blocking(runtime, tmp_path):
    root = _project(tmp_path)
    receivers = dict(_v2(runtime, root).contract["requirement_receivers"])
    receivers.pop("REQ-CONTRACT-001")
    draft = _v2(runtime, root, requirement_receivers=receivers)

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D1" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_requirement_unreceived"
        for finding in verdict["findings"]
    )


def test_h1b_receiver_pointing_at_an_unknown_section_is_blocking(runtime, tmp_path):
    root = _project(tmp_path)
    receivers = dict(_v2(runtime, root).contract["requirement_receivers"])
    receivers["REQ-CONTRACT-001"] = "not_a_section"
    draft = _v2(runtime, root, requirement_receivers=receivers)

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D1" in _codes(verdict)


def test_h2_empty_contract_section_is_blocking(runtime, identity, tmp_path):
    draft = _v2(runtime, _project(tmp_path))
    draft.contract = identity.seal(dict(draft.contract, escalation={}))

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D2" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_section_missing"
        for finding in verdict["findings"]
    )


def test_h2b_acceptance_without_definition_challenge_is_blocking(
    runtime, identity, tmp_path
):
    draft = _v2(runtime, _project(tmp_path))
    trimmed = [
        item for item in draft.contract["acceptance"]
        if "definition_challenge" not in item
    ]
    draft.contract = identity.seal(dict(draft.contract, acceptance=trimmed))

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D2" in _codes(verdict)


@pytest.mark.parametrize(
    "targets",
    [("docs/a.md", "docs/b.md"), ("records/a.md",)],
)
def test_h3_scope_violation_is_blocking(runtime, identity, tmp_path, targets):
    draft = _v2(runtime, _project(tmp_path))
    boundary = dict(draft.contract["boundary"], target_paths=list(targets))
    draft.contract = identity.seal(dict(draft.contract, boundary=boundary))

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D3" in _codes(verdict)


@pytest.mark.parametrize(
    "capability",
    ["call_llm", "external_transmission", "write_artifact", "git_write"],
)
def test_h4_forbidden_capability_is_blocking(runtime, identity, tmp_path, capability):
    draft = _v2(runtime, _project(tmp_path))
    capabilities = dict(draft.contract["allowed_capabilities"], **{capability: True})
    draft.contract = identity.seal(
        dict(draft.contract, allowed_capabilities=capabilities)
    )

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D4" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_forbidden_capability"
        for finding in verdict["findings"]
    )


def test_h5_shared_review_owner_is_blocking(runtime, tmp_path):
    root = _project(tmp_path)
    owners = dict(_v2(runtime, root).contract["review_owners"])
    owners["final_challenge"] = owners["conformance"]
    draft = _v2(runtime, root, review_owners=owners)

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D5" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_owner_separation"
        for finding in verdict["findings"]
    )


def test_h6_deferred_requirement_acceptance_is_blocking(runtime, tmp_path):
    draft = _v2(
        runtime, _project(tmp_path),
        requirement_ids=BOUND_REQUIREMENTS + (DEFERRED_REQUIREMENT,),
        allow_unreceived=True,
    )

    verdict = _challenge(runtime, draft)

    assert verdict["status"] == "failed"
    assert "D6" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_deferred_requirement_accepted"
        for finding in verdict["findings"]
    )


def test_h7_missing_material_stops_without_issuing_a_verdict(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))
    material_set = _materials(runtime, draft)
    (draft.root / MATERIAL_DOCUMENTS[0]).unlink()

    with pytest.raises(runtime.ContractError) as error:
        _challenge(runtime, draft, material_set=material_set)

    assert error.value.code == "definition_material_missing"


def test_h7b_material_digest_mismatch_stops_without_issuing_a_verdict(
    runtime, tmp_path
):
    draft = _v2(runtime, _project(tmp_path))
    material_set = _materials(runtime, draft)
    (draft.root / MATERIAL_DOCUMENTS[0]).write_text("書き換えた。\n", encoding="utf-8")

    with pytest.raises(runtime.ContractError) as error:
        _challenge(runtime, draft, material_set=material_set)

    assert error.value.code == "definition_material_missing"


@pytest.mark.parametrize(
    "record_kind",
    [
        "plan_bundle",
        "compile_verdict",
        "finding_set",
        "conformance_verdict",
        "final_challenge_verdict",
    ],
)
def test_h8_downstream_material_is_stage_confusion(runtime, tmp_path, record_kind):
    draft = _v2(runtime, _project(tmp_path))
    material_set = _materials(
        runtime, draft,
        material_records=(
            {
                "record_kind": record_kind,
                "record_id": f"X-{record_kind}",
                "record_version": 1,
                "digest_algorithm": "sha256",
                "content_digest": "c" * 64,
            },
        ),
    )

    verdict = _challenge(runtime, draft, material_set=material_set)

    assert verdict["status"] == "failed"
    assert "D8" in _codes(verdict)
    assert any(
        finding["stop_code"] == "definition_stage_confusion"
        for finding in verdict["findings"]
    )


def test_h9_failed_challenge_produces_no_plan_bundle(runtime, tmp_path):
    root = _project(tmp_path)
    owners = dict(_v2(runtime, root).contract["review_owners"])
    owners["final_challenge"] = owners["conformance"]
    draft = _v2(runtime, root, review_owners=owners)
    verdict = _challenge(runtime, draft)
    assert verdict["status"] == "failed"

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict,
        contract_approval=None,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "definition_challenge_failed"
    assert "plan_bundle" not in compiled


def test_h10_provenance_without_the_challenge_node_is_rejected(runtime, tmp_path):
    chain = _v2_chain(runtime, tmp_path)
    broken = json.loads(json.dumps(chain.provenance))
    broken["verified_nodes"] = [
        node for node in broken["verified_nodes"]
        if node["node_role"] != "definition_challenge_verdict"
    ]

    with pytest.raises(runtime.ContractError) as error:
        runtime.validate_provenance_verdict(broken)

    assert error.value.code == "provenance_node_missing"


def test_h11_failed_challenge_cannot_reach_an_accepted_artifact(runtime, tmp_path):
    root = _project(tmp_path)
    owners = dict(_v2(runtime, root).contract["review_owners"])
    owners["final_challenge"] = owners["conformance"]
    draft = _v2(runtime, root, review_owners=owners)
    verdict = _challenge(runtime, draft)

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict,
    )

    assert compiled["status"] == "not_compilable"
    assert "plan_bundle" not in compiled
    with pytest.raises(runtime.ContractError):
        runtime.build_contract_approval(
            contract=draft.contract, definition_challenge_verdict=verdict,
            decision="approved", human_id=HUMAN_ID, decided_at=DECIDED_AT,
        )


# --------------------------------------------------- H12〜H17：approval gate


def test_h12_missing_contract_approval_is_not_compilable(runtime, tmp_path):
    draft, verdict, _approval_record = _gated(runtime, tmp_path)

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "contract_approval_missing"
    assert "plan_bundle" not in compiled


def test_h13_rejected_contract_approval_is_not_compilable(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))
    verdict = _challenge(runtime, draft)
    rejected = _approval(runtime, draft, verdict, decision="rejected")

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict, contract_approval=rejected,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "contract_approval_rejected"
    assert "plan_bundle" not in compiled


def test_h14_tampered_contract_approval_is_not_compilable(runtime, tmp_path):
    draft, verdict, approval = _gated(runtime, tmp_path)
    tampered = json.loads(json.dumps(approval))
    tampered["decided_at"] = "2026-01-01T00:00:00+09:00"

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict, contract_approval=tampered,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "contract_approval_invalid"
    assert "plan_bundle" not in compiled


def test_h15_approval_for_another_contract_is_not_compilable(runtime, tmp_path):
    draft, verdict, _approval_record = _gated(runtime, tmp_path)
    other = _v2(
        runtime, _project(tmp_path / "other"), contract_id=OTHER_CONTRACT_V2_ID
    )
    other_verdict = _challenge(runtime, other)
    other_approval = _approval(runtime, other, other_verdict)

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=verdict, contract_approval=other_approval,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "contract_approval_invalid"


def test_h15b_approval_bound_to_another_challenge_is_not_compilable(
    runtime, tmp_path
):
    draft, verdict, approval = _gated(runtime, tmp_path)
    second_verdict = _challenge(runtime, draft, material_set=_materials(
        runtime, draft, record_id="DCM-SECOND"
    ))

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=second_verdict, contract_approval=approval,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "contract_approval_invalid"


def test_h16_provenance_without_the_approval_node_is_rejected(runtime, tmp_path):
    chain = _v2_chain(runtime, tmp_path)
    broken = json.loads(json.dumps(chain.provenance))
    broken["verified_nodes"] = [
        node for node in broken["verified_nodes"]
        if node["node_role"] != "contract_approval"
    ]

    with pytest.raises(runtime.ContractError) as error:
        runtime.validate_provenance_verdict(broken)

    assert error.value.code == "provenance_node_missing"
    assert error.value.detail == "contract_approval"


def test_h17_rejected_or_tampered_approval_cannot_reach_an_accepted_artifact(
    runtime, tmp_path
):
    chain = _v2_chain(runtime, tmp_path)
    tampered = json.loads(json.dumps(chain.provenance))
    for node in tampered["verified_nodes"]:
        if node["node_role"] == "contract_approval":
            node["content_digest"] = "d" * 64

    with pytest.raises(runtime.ContractError):
        runtime.accept_artifact(
            provenance_verdict=tampered, human_decision=chain.human,
            context_manifest=chain.context,
        )

    rejected = _approval(runtime, chain.draft, chain.challenge, decision="rejected")
    with pytest.raises(runtime.ContractError) as error:
        runtime.verify_provenance(
            requirement_binding=chain.draft.binding, contract=chain.draft.contract,
            definition_challenge_verdict=chain.challenge, contract_approval=rejected,
            compile_verdict=chain.compile_verdict, context_manifest=chain.context,
            permit=chain.permit, finding_set=chain.findings,
            conformance_verdict=chain.conformance,
            final_challenge_verdict=chain.final_challenge,
            human_decision=chain.human,
        )
    assert error.value.code == "contract_approval_rejected"


# ------------------------------------------------- 決定性と閉じたschema


def test_challenge_is_deterministic_for_identical_input(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))

    first = _challenge(runtime, draft)
    second = _challenge(runtime, draft)

    assert first["content_digest"] == second["content_digest"]
    assert first == second


def test_material_set_fixes_every_file_digest(runtime, identity, tmp_path):
    draft = _v2(runtime, _project(tmp_path))

    material_set = _materials(runtime, draft)

    assert material_set["record_kind"] == "definition_challenge_material_set"
    assert material_set["contract_ref"] == runtime.record_ref(draft.contract)
    paths = [item["relative_path"] for item in material_set["files"]]
    assert paths == sorted(_material_paths())
    for item in material_set["files"]:
        assert item["sha256"] == identity.file_sha256(draft.root / item["relative_path"])


def test_finding_and_verdict_vocabularies_are_closed(runtime, tmp_path):
    root = _project(tmp_path)
    owners = dict(_v2(runtime, root).contract["review_owners"])
    owners["final_challenge"] = owners["conformance"]
    draft = _v2(runtime, root, review_owners=owners)

    verdict = _challenge(runtime, draft)

    assert runtime.DEFINITION_SEVERITY_CLASSES == ("blocking", "nonblocking")
    assert runtime.DEFINITION_VERDICT_STATUSES == ("passed", "failed")
    assert verdict["status"] in runtime.DEFINITION_VERDICT_STATUSES
    assert verdict["blocking_count"] == len(
        [item for item in verdict["findings"] if item["severity"] == "blocking"]
    )
    for finding in verdict["findings"]:
        assert finding["severity"] in runtime.DEFINITION_SEVERITY_CLASSES
        assert set(finding) == {
            "finding_id", "check_id", "severity", "stop_code",
            "target_ref", "requirement_ref", "description",
        }
        assert finding["severity"] not in runtime.SEVERITY_CLASSES


def test_definition_challenge_record_kinds_and_stop_codes_are_registered(runtime):
    for kind in (
        "definition_challenge_material_set",
        "definition_challenge_verdict",
        "contract_approval",
    ):
        assert kind in runtime.RECORD_KINDS
    for code in (
        "definition_requirement_unreceived",
        "definition_section_missing",
        "definition_scope_violation",
        "definition_forbidden_capability",
        "definition_owner_separation",
        "definition_deferred_requirement_accepted",
        "definition_material_missing",
        "definition_stage_confusion",
        "definition_challenge_missing",
        "definition_challenge_failed",
        "definition_challenge_invalid",
        "contract_approval_missing",
        "contract_approval_rejected",
        "contract_approval_invalid",
    ):
        assert code in runtime.STOP_CODES


def test_challenge_rejects_a_material_set_bound_to_another_contract(
    runtime, tmp_path
):
    draft = _v2(runtime, _project(tmp_path))
    other = _v2(
        runtime, _project(tmp_path / "other"), contract_id=OTHER_CONTRACT_V2_ID
    )

    verdict = _challenge(runtime, draft, material_set=_materials(runtime, other))

    assert verdict["status"] == "failed"
    assert "D7" in _codes(verdict)


def test_missing_challenge_input_is_not_compilable(runtime, tmp_path):
    draft = _v2(runtime, _project(tmp_path))

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "definition_challenge_missing"
    assert "plan_bundle" not in compiled


def test_tampered_challenge_verdict_is_not_compilable(runtime, tmp_path):
    draft, verdict, approval = _gated(runtime, tmp_path)
    tampered = json.loads(json.dumps(verdict))
    tampered["blocking_count"] = 5

    compiled = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=tampered, contract_approval=approval,
    )

    assert compiled["status"] == "not_compilable"
    assert compiled["reason"] == "definition_challenge_invalid"


# ------------------------------------------------------------ 連鎖helper


def _node(verdict, role):
    for node in verdict["verified_nodes"]:
        if node["node_role"] == role:
            return node
    raise AssertionError(role)


def _downstream(runtime, contract, binding, root, compile_verdict):
    snapshot = runtime.read_source_snapshot(
        project_root=root, target_paths=(TARGET,),
        base_commit=BASE_COMMIT, head_commit=HEAD_COMMIT,
    )
    context = runtime.build_context_manifest(
        contract=contract, plan_bundle=compile_verdict["plan_bundle"],
        source_snapshot=snapshot,
    )
    workflow = runtime.new_workflow_state()
    permit = runtime.acquire_permit(workflow_state=workflow, context_manifest=context)
    findings = runtime.run_stub_reviewer(
        contract=contract, context_manifest=context, permit=permit
    )
    conformance = runtime.evaluate_conformance(
        contract=contract, plan_bundle=compile_verdict["plan_bundle"],
        finding_set=findings,
    )
    final_challenge = runtime.evaluate_final_challenge(
        contract=contract, conformance_verdict=conformance, finding_set=findings
    )
    human = runtime.record_human_decision(
        contract=contract, context_manifest=context, finding_set=findings,
        conformance_verdict=conformance, final_challenge_verdict=final_challenge,
        decision="approved", human_id=HUMAN_ID, decided_at=DECIDED_AT,
    )
    return types.SimpleNamespace(
        snapshot=snapshot, context=context, permit=permit, findings=findings,
        conformance=conformance, final_challenge=final_challenge, human=human,
    )


def _v1_chain(runtime, tmp_path):
    root = _project(tmp_path)
    binding, contract = _v1(runtime, root)
    compile_verdict = runtime.compile_contract(
        contract=contract, requirement_binding=binding
    )
    parts = _downstream(runtime, contract, binding, root, compile_verdict)
    provenance = runtime.verify_provenance(
        requirement_binding=binding, contract=contract,
        compile_verdict=compile_verdict, context_manifest=parts.context,
        permit=parts.permit, finding_set=parts.findings,
        conformance_verdict=parts.conformance,
        final_challenge_verdict=parts.final_challenge, human_decision=parts.human,
    )
    return types.SimpleNamespace(
        root=root, binding=binding, contract=contract,
        compile_verdict=compile_verdict, provenance=provenance, **vars(parts)
    )


def _v2_chain(runtime, tmp_path):
    draft, challenge, approval = _gated(runtime, tmp_path)
    compile_verdict = runtime.compile_contract(
        contract=draft.contract, requirement_binding=draft.binding,
        definition_challenge_verdict=challenge, contract_approval=approval,
    )
    parts = _downstream(
        runtime, draft.contract, draft.binding, draft.root, compile_verdict
    )
    provenance = runtime.verify_provenance(
        requirement_binding=draft.binding, contract=draft.contract,
        definition_challenge_verdict=challenge, contract_approval=approval,
        compile_verdict=compile_verdict, context_manifest=parts.context,
        permit=parts.permit, finding_set=parts.findings,
        conformance_verdict=parts.conformance,
        final_challenge_verdict=parts.final_challenge, human_decision=parts.human,
    )
    return types.SimpleNamespace(
        draft=draft, challenge=challenge, approval=approval,
        compile_verdict=compile_verdict, provenance=provenance, **vars(parts)
    )


def test_v2_accepted_artifact_requires_the_full_gated_chain(runtime, tmp_path):
    chain = _v2_chain(runtime, tmp_path)

    accepted = runtime.accept_artifact(
        provenance_verdict=chain.provenance, human_decision=chain.human,
        context_manifest=chain.context,
    )

    assert accepted["record_kind"] == "accepted_artifact"
    assert accepted["provenance_ref"]["content_digest"] == chain.provenance[
        "content_digest"
    ]
