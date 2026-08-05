"""Requirement binding、Review Task Contract、compileとPlan bundle。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md（§2、§7）
"""

import json
from pathlib import Path

from tools.task_contract.identity import (
    CONTRACT_SECTIONS,
    ContractError,
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
):
    """設計§2の10節を持つ最小Review Task Contractを作る。"""

    if origin not in ORIGIN_CLASSES or continuation not in CONTINUATION_CLASSES:
        raise ContractError("schema_violation", "origin/continuation")
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
    return seal(document)


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


def compile_contract(*, contract, requirement_binding):
    """一Contract typeから一Plan bundleと6 typed viewだけを決定的に作る。"""

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
    return seal(
        {
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
    )
