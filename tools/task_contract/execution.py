"""Source Snapshotからaccepted artifactまでの最小実行経路。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md（§3、§4）
reviewerはdeterministic stubであり、LLMを呼ばない。
"""

from pathlib import Path

from tools.task_contract.identity import (
    DIGEST_ALGORITHM,
    ContractError,
    content_digest,
    file_sha256,
    record_ref,
    safe_relative_path,
    seal,
)


CONFORMANCE_OWNER = "conformance_owner"
FINAL_CHALLENGE_OWNER = "final_challenge_owner"
HUMAN_DECISION_OWNER = "human_decision_owner"
DECISION_CLASSES = ("approved", "rejected")

CONTEXT_DECLARATION_FIELDS = (
    "goal",
    "target",
    "constraints",
    "expected_output",
    "context_requirements",
    "validation_policy",
    "provenance_requirements",
)

PROVENANCE_EDGE_ORDER = (
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

# Contract version 2は、Definition Challengeとcompileの間へHumanのContract approvalを
# 置く（Amendment§4）。version 1の9 node、8 edge履歴はそのまま読める。
CONTRACT_V2_EDGE_ORDER = (
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
GATED_CONTRACT_VERSION = 2


def read_source_snapshot(*, project_root, target_paths, base_commit, head_commit):
    """固定source treeを読取りだけで観測する。Gitへ書かない。"""

    root = Path(project_root)
    files = []
    for relative in target_paths:
        safe_relative_path(relative)
        path = root / relative
        if not path.is_file():
            raise ContractError("path_out_of_scope", relative)
        files.append(
            {
                "relative_path": relative,
                "sha256": file_sha256(path),
                "text": path.read_text(encoding="utf-8"),
            }
        )
    files.sort(key=lambda item: item["relative_path"])
    return seal(
        {
            "record_kind": "source_snapshot",
            "record_id": "SS-FIRST-REVIEW-CONTRACT",
            "record_version": 1,
            "files": files,
            "change_set": {
                "base_commit": base_commit,
                "head_commit": head_commit,
                "changed_paths": [item["relative_path"] for item in files],
            },
        }
    )


def build_context_manifest(
    *,
    contract,
    plan_bundle,
    source_snapshot,
    declaration_overrides=None,
    extra_material_paths=(),
):
    """明示した材料だけでContextを組む。暗黙資料と範囲外pathを拒否する。"""

    allowed = set(plan_bundle["views"]["context_acquisition"]["target_paths"])
    for path in extra_material_paths:
        safe_relative_path(path)
        if path not in allowed:
            raise ContractError("implicit_material_rejected", path)

    declaration = {
        "goal": "束縛Requirementに対する文書変更の適合を判定する。",
        "target": ", ".join(contract["boundary"]["target_paths"]),
        "constraints": "固定Snapshotの材料だけを使い、文書を書き換えない。",
        "expected_output": "閉じたseverityを持つFinding集合と各verdict。",
        "context_requirements": "材料束、Scope contract、Digest固定。",
        "validation_policy": "errorで停止し、warningはHuman判断へ回す。",
        "provenance_requirements": "Contractからdecisionまでを型付き辺で結ぶ。",
    }
    declaration.update(declaration_overrides or {})
    for field in CONTEXT_DECLARATION_FIELDS:
        if not declaration.get(field):
            raise ContractError("context_incomplete", field)

    materials = [
        {
            "role": "target",
            "relative_path": item["relative_path"],
            "origin": "fixed_source_snapshot",
            "sha256": item["sha256"],
        }
        for item in source_snapshot["files"]
    ]
    if not materials:
        raise ContractError("context_incomplete", "material_bundle")

    return seal(
        {
            "record_kind": "context_manifest",
            "record_id": f"CM-{contract['record_id']}",
            "record_version": 1,
            "contract_ref": record_ref(contract),
            "plan_bundle_ref": record_ref(plan_bundle),
            "declaration": declaration,
            "material_bundle": materials,
            "material_contents": [
                {"relative_path": item["relative_path"], "text": item["text"]}
                for item in source_snapshot["files"]
            ],
            "scope_contract": {
                "population": list(contract["boundary"]["target_paths"]),
                "in_scope": [item["relative_path"] for item in materials],
                "exclusions": [],
                "classification": "single_document_change",
            },
            "source_change_set": dict(source_snapshot["change_set"]),
        }
    )


def assert_context_fresh(*, context_manifest, source_snapshot):
    """入力が変わった場合は旧結果を再利用せず停止する。"""

    fixed = {item["relative_path"]: item["sha256"] for item in context_manifest["material_bundle"]}
    current = {item["relative_path"]: item["sha256"] for item in source_snapshot["files"]}
    if fixed != current:
        raise ContractError("stale", "source digest changed")
    return True


def new_workflow_state():
    return {"active_permits": [], "waiting_candidates": [], "completed_permits": []}


def active_leaf_count(workflow_state):
    return len(workflow_state["active_permits"])


def acquire_permit(*, workflow_state, context_manifest):
    """active leafを一件だけ許可する。二件目は待機候補として記録する。"""

    if workflow_state["active_permits"]:
        workflow_state["waiting_candidates"].append(
            {
                "context_digest": context_manifest["content_digest"],
                "reason": "single_active_leaf",
            }
        )
        raise ContractError("not_permitted", "single_active_leaf")
    permit = seal(
        {
            "record_kind": "workflow_permit",
            "record_id": f"WP-{context_manifest['record_id']}",
            "record_version": 1,
            "scheduler_policy": "single_active_leaf",
            "context_ref": record_ref(context_manifest),
        }
    )
    workflow_state["active_permits"].append(permit["content_digest"])
    return permit


def release_permit(*, workflow_state, permit):
    digest = permit["content_digest"]
    if digest in workflow_state["active_permits"]:
        workflow_state["active_permits"].remove(digest)
        workflow_state["completed_permits"].append(digest)
    workflow_state["waiting_candidates"] = [
        item
        for item in workflow_state["waiting_candidates"]
        if item["context_digest"] != digest
    ]
    return workflow_state


def _stub_rules(text):
    """決定的なrule。LLMを呼ばない。"""

    findings = []
    if not text.lstrip().startswith("# "):
        findings.append(
            ("R-HEADING-001", "error", "REQ-CONTEXT-003", "文書に最上位見出しがない。")
        )
    if "TODO" in text:
        findings.append(
            ("R-TODO-001", "warning", "REQ-TRIAGE-003", "未処理のTODO表記が残っている。")
        )
    return findings


def run_stub_reviewer(*, contract, context_manifest, permit):
    """permitされた場合だけ、Contextへ実体化した材料に固定ruleを当てる。"""

    if permit is None or permit.get("record_kind") != "workflow_permit":
        raise ContractError("not_permitted", "permit required")
    texts = {
        item["relative_path"]: item["text"]
        for item in context_manifest["material_contents"]
    }
    findings = []
    for index, material in enumerate(context_manifest["material_bundle"], start=1):
        text = texts.get(material["relative_path"])
        if text is None:
            raise ContractError("context_incomplete", material["relative_path"])
        for rule_id, severity, requirement_id, description in _stub_rules(text):
            findings.append(
                {
                    "finding_id": f"F-{index:03d}-{rule_id}",
                    "severity": severity,
                    "target_ref": {
                        "relative_path": material["relative_path"],
                        "sha256": material["sha256"],
                    },
                    "requirement_ref": requirement_id,
                    "rule_id": rule_id,
                    "description": description,
                }
            )
    findings.sort(key=lambda item: item["finding_id"])
    return seal(
        {
            "record_kind": "finding_set",
            "record_id": f"FS-{context_manifest['record_id']}",
            "record_version": 1,
            "reviewer": "deterministic_stub",
            "calls_llm": False,
            "context_ref": record_ref(context_manifest),
            "permit_ref": record_ref(permit),
            "findings": findings,
        }
    )


def _severity_counts(finding_set):
    counts = {"error": 0, "warning": 0, "info": 0}
    for item in finding_set["findings"]:
        counts[item["severity"]] += 1
    return counts


def evaluate_conformance(*, contract, plan_bundle, finding_set, owner=CONFORMANCE_OWNER):
    """errorで停止し、warningでは自動失格にしない。"""

    counts = _severity_counts(finding_set)
    status = "failed" if counts["error"] else "passed"
    return seal(
        {
            "record_kind": "conformance_verdict",
            "record_id": f"CFV-{contract['record_id']}",
            "record_version": 1,
            "owner": owner,
            "status": status,
            "severity_counts": counts,
            "contract_ref": record_ref(contract),
            "plan_bundle_ref": record_ref(plan_bundle),
            "finding_set_ref": record_ref(finding_set),
        }
    )


def evaluate_final_challenge(
    *, contract, conformance_verdict, finding_set, owner=FINAL_CHALLENGE_OWNER
):
    """Conformanceと別ownerで判定する。ownerが同一なら停止する。"""

    if owner == conformance_verdict["owner"]:
        raise ContractError("owner_separation_violated", owner)
    counts = _severity_counts(finding_set)
    status = "passed" if conformance_verdict["status"] == "passed" else "failed"
    return seal(
        {
            "record_kind": "final_challenge_verdict",
            "record_id": f"FCV-{contract['record_id']}",
            "record_version": 1,
            "owner": owner,
            "status": status,
            "human_decision_required": True,
            "warning_count": counts["warning"],
            "contract_ref": record_ref(contract),
            "conformance_ref": record_ref(conformance_verdict),
            "finding_set_ref": record_ref(finding_set),
        }
    )


def record_human_decision(
    *,
    contract,
    context_manifest,
    finding_set,
    conformance_verdict,
    final_challenge_verdict,
    decision,
    human_id,
    decided_at,
    owner=HUMAN_DECISION_OWNER,
):
    """Human decisionを対象Digestへ束縛する。ownerは両verdictと別にする。"""

    if decision not in DECISION_CLASSES:
        raise ContractError("schema_violation", str(decision))
    if owner in (conformance_verdict["owner"], final_challenge_verdict["owner"]):
        raise ContractError("owner_separation_violated", owner)
    if not human_id:
        raise ContractError("human_decision_missing", "human_id")
    return seal(
        {
            "record_kind": "human_decision",
            "record_id": f"HD-{contract['record_id']}",
            "record_version": 1,
            "owner": owner,
            "decision": decision,
            "decision_class": "review_acceptance",
            "human_id": human_id,
            "decided_at": decided_at,
            "target_digest": context_manifest["content_digest"],
            "conformance_ref": record_ref(conformance_verdict),
            "final_challenge_ref": record_ref(final_challenge_verdict),
            "finding_set_ref": record_ref(finding_set),
        }
    )


PROVENANCE_NODE_ROLES = PROVENANCE_EDGE_ORDER


def _edge_pairs(node_roles):
    return tuple(
        (node_roles[index], node_roles[index + 1])
        for index in range(len(node_roles) - 1)
    )


PROVENANCE_EDGE_PAIRS = _edge_pairs(PROVENANCE_EDGE_ORDER)
CONTRACT_V2_EDGE_PAIRS = _edge_pairs(CONTRACT_V2_EDGE_ORDER)


def provenance_node_roles(contract_version):
    """Contract versionごとの期待node列。辺数だけで判定しない。"""

    if contract_version >= GATED_CONTRACT_VERSION:
        return CONTRACT_V2_EDGE_ORDER
    return PROVENANCE_EDGE_ORDER


def _assert_contract_gate(*, contract, definition_challenge_verdict, contract_approval):
    """来歴へ載せる前に、Challengeとapprovalが実際に束縛されているかを見る。

    compile事前gateと同じ判定を、Amendment§3の閉じたreasonで再確認する。
    """

    from tools.task_contract.contract import compile_gate_reason

    reason = compile_gate_reason(
        contract=contract,
        definition_challenge_verdict=definition_challenge_verdict,
        contract_approval=contract_approval,
    )
    if reason is not None:
        raise ContractError(reason, contract["record_id"])
    return True


def _node_ref(node_role, document):
    return {
        "node_role": node_role,
        "record_kind": document["record_kind"],
        "record_id": document["record_id"],
        "record_version": document["record_version"],
        "digest_algorithm": DIGEST_ALGORITHM,
        "content_digest": document["content_digest"],
    }


def validate_provenance_verdict(verdict, *, upstream_records=None):
    """V1〜V8を照合する。辺数では判定せず、両端のidentityとDigestを見る。

    `provenance_verdict`自身を端点とするedgeを許さない。自己参照も許さない。
    """

    if not isinstance(verdict, dict) or verdict.get("record_kind") != "provenance_verdict":
        raise ContractError("schema_violation", "provenance_verdict required")
    nodes = verdict.get("verified_nodes")
    edges = verdict.get("verified_edges")
    if not isinstance(nodes, list):
        raise ContractError("provenance_node_missing", "verified_nodes")
    if not isinstance(edges, list):
        raise ContractError("provenance_edge_missing", "verified_edges")

    seen = {}
    for node in nodes:
        role = node.get("node_role")
        if role in seen:
            raise ContractError("provenance_node_duplicated", str(role))
        seen[role] = node

    # 期待するnode列は、来歴が主張するContract versionから決める。
    # version 2を名乗るnodeがあれば、Definition ChallengeとContract approvalを必ず要求する。
    contract_node = seen.get("review_task_contract") or {}
    contract_version = contract_node.get("record_version") or 1
    if not isinstance(contract_version, int):
        raise ContractError(
            "provenance_node_identity_mismatch", "review_task_contract.record_version"
        )
    node_roles = provenance_node_roles(contract_version)
    edge_pairs = _edge_pairs(node_roles)

    for role in node_roles:
        if role not in seen:
            raise ContractError("provenance_node_missing", role)
    unexpected = sorted(set(seen) - set(node_roles))
    if unexpected:
        raise ContractError("provenance_node_duplicated", ",".join(unexpected))

    for role, node in seen.items():
        if node.get("record_kind") != role:
            raise ContractError("provenance_node_kind_mismatch", role)
        for field in ("record_id", "record_version", "content_digest"):
            if not node.get(field):
                raise ContractError("provenance_node_identity_mismatch", f"{role}.{field}")

    pairs = []
    for edge in edges:
        source = edge.get("from", {}).get("node_role")
        target = edge.get("to", {}).get("node_role")
        if source == "provenance_verdict" or target == "provenance_verdict" or source == target:
            raise ContractError("provenance_self_reference", f"{source}->{target}")
        if source not in seen or target not in seen:
            raise ContractError("provenance_edge_endpoint_unresolved", f"{source}->{target}")
        pairs.append((source, target))
    for pair in edge_pairs:
        if pair not in pairs:
            raise ContractError("provenance_edge_missing", "->".join(pair))
    if len(pairs) != len(edge_pairs) or pairs != list(edge_pairs):
        raise ContractError("provenance_edge_unexpected", str(pairs))

    closure = verdict.get("closure", {})
    if (
        closure.get("terminal_node_role") != "human_decision"
        or closure.get("self_edge_present") is not False
        or closure.get("closed_by") != "accepted_artifact"
    ):
        raise ContractError("provenance_self_reference", "closure")

    if upstream_records:
        for role, document in upstream_records.items():
            node = seen.get(role)
            if node is None:
                raise ContractError("provenance_node_missing", role)
            if (
                node["record_id"] != document["record_id"]
                or node["record_version"] != document["record_version"]
            ):
                raise ContractError("provenance_node_identity_mismatch", role)
            if node["content_digest"] != document["content_digest"]:
                raise ContractError("provenance_node_digest_mismatch", role)

    # 封をしたあとに中身が書き換えられていないかを最後に見る。
    # node、edge、closureの構造検査を先に通すため、既存の停止codeは変わらない。
    if "content_digest" in verdict and content_digest(verdict) != verdict[
        "content_digest"
    ]:
        raise ContractError("provenance_node_digest_mismatch", verdict["record_id"])
    return verdict


def verify_provenance(
    *,
    requirement_binding,
    contract,
    compile_verdict,
    context_manifest,
    permit,
    finding_set,
    conformance_verdict,
    final_challenge_verdict,
    human_decision,
    definition_challenge_verdict=None,
    contract_approval=None,
    record_version=1,
):
    """Contract versionに応じたnodeとedgeを検証する。

    version 1は9 node、8 edge。version 2はDefinition ChallengeとContract approvalを
    含む11 node、10 edgeである。verdict自身へ向かうedgeを内容へ含めない。
    """

    node_roles = provenance_node_roles(contract.get("record_version", 1))
    stages = {
        "requirement_binding": requirement_binding,
        "review_task_contract": contract,
        "definition_challenge_verdict": definition_challenge_verdict,
        "contract_approval": contract_approval,
        "compile_verdict": compile_verdict,
        "context_manifest": context_manifest,
        "workflow_permit": permit,
        "finding_set": finding_set,
        "conformance_verdict": conformance_verdict,
        "final_challenge_verdict": final_challenge_verdict,
        "human_decision": human_decision,
    }
    stages = {role: stages[role] for role in node_roles}
    for role in node_roles:
        if not stages.get(role):
            raise ContractError("provenance_node_missing", role)
    if human_decision["target_digest"] != context_manifest["content_digest"]:
        raise ContractError("decision_digest_mismatch", human_decision["record_id"])

    owners = [
        conformance_verdict["owner"],
        final_challenge_verdict["owner"],
        human_decision["owner"],
    ]
    if definition_challenge_verdict is not None and "definition_challenge_verdict" in stages:
        _assert_contract_gate(
            contract=contract,
            definition_challenge_verdict=definition_challenge_verdict,
            contract_approval=contract_approval,
        )
        owners.append(definition_challenge_verdict["owner"])
        owners.append(contract_approval["owner"])
    for index, owner in enumerate(owners):
        if owner in owners[index + 1:]:
            raise ContractError("owner_separation_violated", owner)

    document = {
        "record_kind": "provenance_verdict",
        "record_id": f"PV-{contract['record_id']}",
        "record_version": record_version,
        "status": "verified",
        "verified_nodes": [_node_ref(role, stages[role]) for role in node_roles],
        "verified_edges": [
            {"edge_kind": "precedes",
             "from": {"node_role": source},
             "to": {"node_role": target}}
            for source, target in _edge_pairs(node_roles)
        ],
        "closure": {
            "terminal_node_role": "human_decision",
            "self_edge_present": False,
            "closed_by": "accepted_artifact",
        },
    }
    validate_provenance_verdict(document, upstream_records=stages)
    return seal(document)


def accept_artifact(
    *, provenance_verdict, human_decision, context_manifest, record_version=1
):
    """Human承認と新形式のProvenance検証が揃った場合だけaccepted artifactを確定する。"""

    if human_decision is None:
        raise ContractError("human_decision_missing", "human decision required")
    if human_decision.get("decision") != "approved":
        raise ContractError("human_decision_not_approved", human_decision.get("decision"))
    if provenance_verdict.get("status") != "verified":
        raise ContractError("provenance_edge_missing", "provenance not verified")
    validate_provenance_verdict(provenance_verdict)
    if context_manifest is None:
        raise ContractError("context_incomplete", "context manifest required")
    if human_decision["target_digest"] != context_manifest["content_digest"]:
        raise ContractError("decision_digest_mismatch", human_decision["record_id"])
    return seal(
        {
            "record_kind": "accepted_artifact",
            "record_id": f"AA-{context_manifest['record_id']}",
            "record_version": record_version,
            "target_paths": [
                item["relative_path"] for item in context_manifest["material_bundle"]
            ],
            "provenance_ref": record_ref(provenance_verdict),
            "decision_ref": record_ref(human_decision),
        }
    )
