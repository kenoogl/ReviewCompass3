"""Requirement binding、Review Task Contract、compileとPlan bundle。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md（§2、§7）
"""

import json
from pathlib import Path

from tools.task_contract.identity import (
    CONTRACT_SECTIONS,
    ContractError,
    content_digest,
    record_ref,
    safe_relative_path,
    seal,
)


ORIGIN_CLASSES = ("new_development", "maintenance")
CONTINUATION_CLASSES = ("fresh", "reopen")
SCHEDULER_POLICIES = ("single_active_leaf",)
SEVERITY_CLASSES = ("error", "warning", "info")

PLAN_VIEWS = (
    "context_acquisition",
    "review_execution",
    "harness_and_capability",
    "verification",
    "provenance_capture",
    "human_interaction",
)

# 設計§7で束縛した16 Requirementと、Contractが受ける義務の対応。
REQUIREMENT_OBLIGATIONS = {
    "REQ-CONTRACT-001": "OBL-CONTRACT-SECTIONS",
    "REQ-CONTRACT-002": "OBL-PLAN-BUNDLE-VIEWS",
    "REQ-CONTRACT-003": "OBL-REQUIREMENT-COVERAGE",
    "REQ-CONTRACT-004": "OBL-OWNER-SEPARATION",
    "REQ-CONTRACT-005": "OBL-CAPTURE-PLAN",
    "REQ-CONTEXT-001": "OBL-CONTEXT-DECLARATION",
    "REQ-CONTEXT-002": "OBL-MATERIAL-BUNDLE",
    "REQ-CONTEXT-003": "OBL-SCOPE-CONTRACT",
    "REQ-CONTEXT-004": "OBL-CONTEXT-FRESHNESS",
    "REQ-CONTEXT-005": "OBL-EXPLICIT-MATERIAL-ONLY",
    "REQ-EXEC-001": "OBL-PERMITTED-RUN-ONLY",
    "REQ-TRACE-002": "OBL-OBLIGATION-RECEIVER",
    "REQ-TRACE-005": "OBL-PROVENANCE-CHAIN",
    "REQ-TRIAGE-003": "OBL-HUMAN-DECISION-BINDING",
    "REQ-WORKFLOW-004": "OBL-SELF-APPLICATION",
    "REQ-WORKFLOW-005": "OBL-ORIGIN-CONTINUATION",
}

#: Work 5Aが直接束縛する16 Requirement。deferred分をここへ足さない。
BOUND_REQUIREMENT_IDS = tuple(sorted(REQUIREMENT_OBLIGATIONS))

# 設計§6.1でversion 2が新しく持つ宣言。束縛16 Requirementを、Contractの
# どの節が受けるかを明示する。値は10節の実在するfield名だけを使う。
REQUIREMENT_RECEIVERS = {
    "REQ-CONTRACT-001": "identity",
    "REQ-CONTRACT-002": "expected_output",
    "REQ-CONTRACT-003": "acceptance",
    "REQ-CONTRACT-004": "acceptance",
    "REQ-CONTRACT-005": "provenance_obligations",
    "REQ-CONTEXT-001": "context_obligations",
    "REQ-CONTEXT-002": "context_obligations",
    "REQ-CONTEXT-003": "boundary",
    "REQ-CONTEXT-004": "preconditions",
    "REQ-CONTEXT-005": "context_obligations",
    "REQ-EXEC-001": "preconditions",
    "REQ-TRACE-002": "responsibility",
    "REQ-TRACE-005": "provenance_obligations",
    "REQ-TRIAGE-003": "escalation",
    "REQ-WORKFLOW-004": "boundary",
    "REQ-WORKFLOW-005": "identity",
}

# 四つのreview判断と、Amendment§2のContract approvalの論理owner。
# 同じHuman個人が兼ねること自体は禁止しないが、論理ownerは分ける。
DEFINITION_CHALLENGE_OWNER = "definition_challenge_owner"
CONTRACT_APPROVAL_OWNER = "contract_approval_owner"
DEFAULT_REVIEW_OWNERS = {
    "definition_challenge": DEFINITION_CHALLENGE_OWNER,
    "contract_approval": CONTRACT_APPROVAL_OWNER,
    "conformance": "conformance_owner",
    "final_challenge": "final_challenge_owner",
    "human_decision": "human_decision_owner",
}
SEPARATED_REVIEW_ROLES = (
    "definition_challenge",
    "conformance",
    "final_challenge",
    "human_decision",
)

#: Contract version 2がcompile前に通す来歴step。Amendment§4の11 node。
CONTRACT_V2_REQUIRED_EDGES = (
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

#: Amendment§3の閉じたreason。compile事前gateはこれ以外を返さない。
COMPILE_GATE_REASONS = (
    "definition_challenge_missing",
    "definition_challenge_failed",
    "definition_challenge_invalid",
    "contract_approval_missing",
    "contract_approval_rejected",
    "contract_approval_invalid",
)

#: このversion以上でDefinition ChallengeとContract approvalを必須にする。
GATED_CONTRACT_VERSION = 2


def bind_requirements(
    *,
    project_root,
    requirement_ids,
    allow_unreceived=False,
    additional_requirement_ids=(),
):
    """固定Requirementを束縛する。定義fileが無いIDは受け付けない。"""

    root = Path(project_root)
    identifiers = list(requirement_ids) + list(additional_requirement_ids)
    bound = []
    for requirement_id in identifiers:
        path = root / "records" / "requirements" / "definitions" / (
            f"{requirement_id.lower()}--v1.json"
        )
        if not path.is_file():
            raise ContractError("schema_violation", f"requirement not found: {requirement_id}")
        document = json.loads(path.read_text(encoding="utf-8"))
        bound.append(
            {
                "requirement_id": document["requirement_id"],
                "requirement_version": document["requirement_version"],
                "relative_path": safe_relative_path(
                    path.resolve().relative_to(root.resolve()).as_posix()
                ),
            }
        )
    bound.sort(key=lambda item: item["requirement_id"])
    unreceived = [
        item["requirement_id"]
        for item in bound
        if item["requirement_id"] not in REQUIREMENT_OBLIGATIONS
    ]
    if unreceived and not allow_unreceived:
        raise ContractError("unreceived_obligation", ",".join(unreceived))
    return seal(
        {
            "record_kind": "requirement_binding",
            "record_id": "RB-FIRST-REVIEW-CONTRACT",
            "record_version": 1,
            "requirements": bound,
            "unreceived_requirement_ids": unreceived,
        }
    )


def build_review_task_contract(
    *,
    contract_id,
    contract_version,
    requirement_binding,
    target_paths,
    origin="new_development",
    continuation="fresh",
    supersedes=None,
    requirement_receivers=None,
    review_owners=None,
):
    """設計§2の10節を持つ最小Review Task Contractを作る。

    version 2では設計§6.1の差分だけをversion 1へ足す。version 1の出力は変えない。
    """

    if origin not in ORIGIN_CLASSES or continuation not in CONTINUATION_CLASSES:
        raise ContractError("schema_violation", "origin/continuation")
    version_two = contract_version >= GATED_CONTRACT_VERSION
    if not version_two and any(
        value is not None for value in (supersedes, requirement_receivers, review_owners)
    ):
        raise ContractError("schema_violation", "version 2 only field")
    targets = [safe_relative_path(path) for path in target_paths]
    for path in targets:
        if not path.startswith("docs/"):
            raise ContractError("path_out_of_scope", path)
    requirement_ids = [item["requirement_id"] for item in requirement_binding["requirements"]]
    document = {
        "record_kind": "review_task_contract",
        "record_id": contract_id,
        "record_version": contract_version,
        "identity": {
            "task_contract_id": contract_id,
            "task_contract_version": contract_version,
            "contract_type": "review_task_contract",
            "origin": origin,
            "continuation": continuation,
            "scheduler_policy": "single_active_leaf",
        },
        "responsibility": (
            "固定した一件の文書変更が束縛Requirementへ適合するかを判定し、"
            "不適合を構造化Findingとして返す。文書を書き換えず、Requirementを改訂しない。"
        ),
        "boundary": {
            "target_paths": targets,
            "source_universe": "fixed_source_snapshot",
            "writes_artifact": False,
            "self_application": True,
            "gate_bypass_allowed": False,
        },
        "preconditions": [
            "requirement_binding_resolved",
            "source_snapshot_fixed",
            "contract_compiled",
            "workflow_permitted",
            "single_active_leaf_free",
        ],
        "context_obligations": [
            "OBL-CONTEXT-DECLARATION",
            "OBL-MATERIAL-BUNDLE",
            "OBL-SCOPE-CONTRACT",
            "OBL-CONTEXT-FRESHNESS",
            "OBL-EXPLICIT-MATERIAL-ONLY",
        ],
        "allowed_capabilities": {
            "read_fixed_snapshot": True,
            "compute_digest": True,
            "run_deterministic_reviewer": True,
            "call_llm": False,
            "external_transmission": False,
            "write_artifact": False,
            "git_write": False,
        },
        "expected_output": {
            "finding_severity_classes": list(SEVERITY_CLASSES),
            "finding_fields": [
                "finding_id", "severity", "target_ref", "requirement_ref", "rule_id",
                "description",
            ],
        },
        "acceptance": [
            "every_bound_requirement_has_receiver",
            "conformance_passed",
            "final_challenge_passed",
            "human_decision_bound_to_target_digest",
            "provenance_verified",
        ],
        "provenance_obligations": {
            "capture_plan_before_execution": True,
            "decision_class": "review_acceptance",
            "required_edges": [
                "requirement_binding", "review_task_contract", "compile_verdict",
                "context_manifest", "workflow_permit", "finding_set",
                "conformance_verdict", "final_challenge_verdict", "human_decision",
            ],
        },
        "escalation": {
            "requirement_missing": "not_compilable",
            "context_incomplete": "context_incomplete",
            "context_stale": "stale",
            "conformance_failed": "stop",
            "final_challenge_failed": "stop",
            "human_rejected": "stop",
            "source_changed": "stale",
        },
        "requirement_ids": sorted(requirement_ids),
        "requirement_binding_ref": record_ref(requirement_binding),
    }
    if version_two:
        _apply_version_two_declarations(
            document,
            contract_version=contract_version,
            supersedes=supersedes,
            requirement_receivers=requirement_receivers,
            review_owners=review_owners,
        )
    return seal(document)


def _apply_version_two_declarations(
    document, *, contract_version, supersedes, requirement_receivers, review_owners
):
    """設計§6.1が列挙した差分だけをversion 2へ足す。"""

    if not isinstance(supersedes, dict):
        raise ContractError("schema_violation", "supersedes")
    if (
        supersedes.get("record_kind") != "review_task_contract"
        or not supersedes.get("record_id")
        or not supersedes.get("content_digest")
        or not isinstance(supersedes.get("record_version"), int)
        or supersedes["record_version"] >= contract_version
    ):
        raise ContractError("schema_violation", "supersedes")

    document["requirement_receivers"] = dict(
        REQUIREMENT_RECEIVERS if requirement_receivers is None else requirement_receivers
    )
    document["review_owners"] = dict(
        DEFAULT_REVIEW_OWNERS if review_owners is None else review_owners
    )
    document["supersedes"] = dict(supersedes)
    document["acceptance"] = list(document["acceptance"]) + [
        "definition_challenge_passed",
        "contract_approval_recorded",
    ]
    document["provenance_obligations"] = dict(
        document["provenance_obligations"],
        required_edges=list(CONTRACT_V2_REQUIRED_EDGES),
    )
    document["escalation"] = dict(
        document["escalation"],
        definition_challenge_failed="stop",
        contract_approval_missing="not_compilable",
        contract_approval_rejected="stop",
    )
    return document


def check_requirement_coverage(*, contract, requirement_binding):
    """順逆被覆を検査する。受け先の無い義務と孤立obligationを出す。"""

    requirement_ids = [item["requirement_id"] for item in requirement_binding["requirements"]]
    unreceived = sorted(
        requirement_id
        for requirement_id in requirement_ids
        if requirement_id not in REQUIREMENT_OBLIGATIONS
    )
    received = {
        REQUIREMENT_OBLIGATIONS[requirement_id]
        for requirement_id in requirement_ids
        if requirement_id in REQUIREMENT_OBLIGATIONS
    }
    declared = set(contract["context_obligations"])
    orphans = sorted(declared - received)
    return {
        "status": "covered" if not unreceived and not orphans else "incomplete",
        "requirement_ids": sorted(requirement_ids),
        "unreceived_requirement_ids": unreceived,
        "orphan_obligation_ids": orphans,
    }


def _plan_views(contract):
    targets = contract["boundary"]["target_paths"]
    return {
        "context_acquisition": {
            "target_paths": list(targets),
            "material_roles": ["target", "requirement"],
            "implicit_material_allowed": False,
        },
        "review_execution": {
            "reviewer": "deterministic_stub",
            "calls_llm": False,
            "severity_classes": list(SEVERITY_CLASSES),
        },
        "harness_and_capability": dict(contract["allowed_capabilities"]),
        "verification": {
            "conformance_owner": "conformance_owner",
            "final_challenge_owner": "final_challenge_owner",
            "owner_separation_required": True,
        },
        "provenance_capture": {
            "capture_plan": {
                "generated_before_execution": True,
                "required_events": list(
                    contract["provenance_obligations"]["required_edges"]
                ),
            }
        },
        "human_interaction": {
            "decision_owner": "human_decision_owner",
            "decision_required": True,
            "binds_target_digest": True,
        },
    }


def _sealed_record(document, kind):
    """recordがその種別として封をされたままかを見る。改竄はDigestで分かる。"""

    if not isinstance(document, dict) or document.get("record_kind") != kind:
        return False
    for field in ("record_id", "record_version", "content_digest"):
        if not document.get(field):
            return False
    return content_digest(document) == document["content_digest"]


def compile_gate_reason(*, contract, definition_challenge_verdict, contract_approval):
    """Amendment§3のcompile事前gate。通れば`None`を返す。

    Contract version 1は履歴再読込みのため、この検査を通さない。
    """

    if contract.get("record_version", 1) < GATED_CONTRACT_VERSION:
        return None

    if definition_challenge_verdict is None:
        return "definition_challenge_missing"
    if not _sealed_record(definition_challenge_verdict, "definition_challenge_verdict"):
        return "definition_challenge_invalid"
    if definition_challenge_verdict.get("status") != "passed":
        return "definition_challenge_failed"
    if definition_challenge_verdict.get("contract_ref") != record_ref(contract):
        return "definition_challenge_invalid"

    if contract_approval is None:
        return "contract_approval_missing"
    if not _sealed_record(contract_approval, "contract_approval"):
        return "contract_approval_invalid"
    if contract_approval.get("decision") != "approved":
        return "contract_approval_rejected"
    if contract_approval.get("contract_ref") != record_ref(contract):
        return "contract_approval_invalid"
    if contract_approval.get("definition_challenge_ref") != record_ref(
        definition_challenge_verdict
    ):
        return "contract_approval_invalid"

    owners = contract.get("review_owners") or {}
    separated = {
        definition_challenge_verdict.get("owner"),
        contract_approval.get("owner"),
        owners.get("human_decision"),
    }
    if len(separated) != 3 or None in separated:
        return "contract_approval_invalid"
    return None


def compile_contract(
    *,
    contract,
    requirement_binding,
    definition_challenge_verdict=None,
    contract_approval=None,
):
    """一Contract typeから一Plan bundleと6 typed viewだけを決定的に作る。

    Contract version 2以降は、Plan bundleを作る前にDefinition Challengeと
    Human Contract approvalを検証する。一件でも満たさなければPlan bundleを含めない。
    """

    missing = [section for section in CONTRACT_SECTIONS if not contract.get(section)]
    if missing:
        return seal(
            {
                "record_kind": "compile_verdict",
                "record_id": f"CV-{contract.get('record_id', 'UNKNOWN')}",
                "record_version": 1,
                "status": "not_compilable",
                "reason": "contract_section_missing",
                "missing_sections": missing,
                "unreceived_requirement_ids": [],
            }
        )
    gate_reason = compile_gate_reason(
        contract=contract,
        definition_challenge_verdict=definition_challenge_verdict,
        contract_approval=contract_approval,
    )
    if gate_reason is not None:
        return seal(
            {
                "record_kind": "compile_verdict",
                "record_id": f"CV-{contract['record_id']}",
                "record_version": 1,
                "status": "not_compilable",
                "reason": gate_reason,
                "missing_sections": [],
                "unreceived_requirement_ids": [],
            }
        )
    coverage = check_requirement_coverage(
        contract=contract, requirement_binding=requirement_binding
    )
    if coverage["status"] != "covered":
        return seal(
            {
                "record_kind": "compile_verdict",
                "record_id": f"CV-{contract['record_id']}",
                "record_version": 1,
                "status": "not_compilable",
                "reason": "unreceived_obligation",
                "missing_sections": [],
                "unreceived_requirement_ids": coverage["unreceived_requirement_ids"],
            }
        )
    bundle = seal(
        {
            "record_kind": "plan_bundle",
            "record_id": f"PB-{contract['record_id']}",
            "record_version": contract["record_version"],
            "contract_ref": record_ref(contract),
            "views": _plan_views(contract),
        }
    )
    document = {
        "record_kind": "compile_verdict",
        "record_id": f"CV-{contract['record_id']}",
        "record_version": 1,
        "status": "compiled",
        "reason": None,
        "missing_sections": [],
        "unreceived_requirement_ids": [],
        "contract_ref": record_ref(contract),
        "plan_bundle": bundle,
    }
    if contract.get("record_version", 1) >= GATED_CONTRACT_VERSION:
        document["definition_challenge_ref"] = record_ref(definition_challenge_verdict)
        document["contract_approval_ref"] = record_ref(contract_approval)
    return seal(document)
