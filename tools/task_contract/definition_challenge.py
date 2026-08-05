"""compile前のDefinition Challengeと、HumanのContract approval record。

正本設計：docs/design/2026-08-05-work5a-definition-challenge-proposal.md（§2〜§4）
Amendment：docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md
承認：DEC-WORK5A-DEFINITION-CHALLENGE-001、DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001

Definition Challengeは**Contractの定義**を見る検査である。成果の再評価ではない。
compileより前に実行し、compile後のPlan bundle、compile verdict、Finding集合、
Conformance verdict、Final Challenge verdictを入力に使わない。

判定はLLMを使わず、固定入力から同じ結果を再生成できる決定的な処理である。
対象は後継する一つのContract versionだけで、汎用Challenge frameworkを作らない。
"""

from pathlib import Path

from tools.task_contract.contract import (
    BOUND_REQUIREMENT_IDS,
    CONTRACT_APPROVAL_OWNER,
    DEFINITION_CHALLENGE_OWNER,
    SEPARATED_REVIEW_ROLES,
)
from tools.task_contract.identity import (
    CONTRACT_SECTIONS,
    DIGEST_ALGORITHM,
    ContractError,
    file_sha256,
    record_ref,
    safe_relative_path,
    seal,
)


#: 実行する決定的検査。設計§3のD1〜D8だけを持つ。
DEFINITION_CHECKS = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8")

#: Findingのseverity。既存の`error / warning / info`とは別語彙にする。
DEFINITION_SEVERITY_CLASSES = ("blocking", "nonblocking")

#: verdictのstatus。`blocking_count`が1以上なら必ず`failed`である。
DEFINITION_VERDICT_STATUSES = ("passed", "failed")

#: Contractが偽であると明示しなければならない能力。
FORBIDDEN_CAPABILITIES = (
    "call_llm",
    "external_transmission",
    "write_artifact",
    "git_write",
)

#: material setへ混ざってはならないcompile後・成果側のrecord種別（D8）。
STAGE_CONFUSION_KINDS = (
    "plan_bundle",
    "compile_verdict",
    "finding_set",
    "conformance_verdict",
    "final_challenge_verdict",
)

#: 各検査が返す停止code。
CHECK_STOP_CODES = {
    "D1": "definition_requirement_unreceived",
    "D2": "definition_section_missing",
    "D3": "definition_scope_violation",
    "D4": "definition_forbidden_capability",
    "D5": "definition_owner_separation",
    "D6": "definition_deferred_requirement_accepted",
    "D7": "definition_material_missing",
    "D8": "definition_stage_confusion",
}

#: 各検査が対応するRequirement。D1だけは欠けたRequirement自身を指す。
CHECK_REQUIREMENTS = {
    "D2": "REQ-CONTRACT-001",
    "D3": "REQ-CONTEXT-003",
    "D4": "REQ-EXEC-001",
    "D5": "REQ-CONTRACT-004",
    "D6": "REQ-CONTRACT-003",
    "D7": "REQ-CONTEXT-002",
    "D8": "REQ-CONTRACT-004",
}

CONTRACT_APPROVAL_DECISIONS = ("approved", "rejected")
CONTRACT_APPROVAL_DECISION_CLASS = "contract_definition_approval"
HUMAN_DECISION_OWNER = "human_decision_owner"


def build_definition_challenge_material_set(
    *, project_root, contract, material_paths, material_records=(), record_id=None
):
    """材料のpathとDigestを固定する。Contractへは`record_ref`で結ぶ。

    `material_records`は上流recordへの参照を入れる口である。ここへcompile後または
    成果側のrecordが入っていないかは、Challenge側のD8が判定する。
    """

    root = Path(project_root)
    files = []
    for relative in sorted(set(material_paths)):
        safe_relative_path(relative)
        path = root / relative
        if not path.is_file():
            raise ContractError("definition_material_missing", relative)
        files.append({"relative_path": relative, "sha256": file_sha256(path)})
    if not files:
        raise ContractError("definition_material_missing", "material set is empty")

    return seal(
        {
            "record_kind": "definition_challenge_material_set",
            "record_id": record_id or f"DCM-{contract['record_id']}",
            "record_version": 1,
            "digest_algorithm": DIGEST_ALGORITHM,
            "contract_ref": record_ref(contract),
            "files": files,
            "records": [dict(item) for item in material_records],
        }
    )


def _finding(index, check_id, *, contract, description, requirement_id=None):
    return {
        "finding_id": f"DF-{index:03d}-{check_id}",
        "check_id": check_id,
        "severity": "blocking",
        "stop_code": CHECK_STOP_CODES[check_id],
        "target_ref": record_ref(contract),
        "requirement_ref": requirement_id or CHECK_REQUIREMENTS[check_id],
        "description": description,
    }


def _verify_materials(*, project_root, material_set):
    """D7の前半。材料が一件でも欠ける、Digestが違えばverdictを発行せず停止する。

    設計§2.2の「`definition_material_missing`で停止し、verdictを発行しない」に従う。
    """

    root = Path(project_root)
    listed = set()
    for item in material_set["files"]:
        relative = item["relative_path"]
        listed.add(relative)
        path = root / relative
        if not path.is_file():
            raise ContractError("definition_material_missing", relative)
        if file_sha256(path) != item["sha256"]:
            raise ContractError("definition_material_missing", relative)
    for requirement_id in BOUND_REQUIREMENT_IDS:
        relative = (
            f"records/requirements/definitions/{requirement_id.lower()}--v1.json"
        )
        if relative not in listed:
            raise ContractError("definition_material_missing", relative)
    return True


def _check_requirement_receivers(contract):
    """D1：束縛16 Requirementのすべてに、実在する非空の受け先がある。"""

    receivers = contract.get("requirement_receivers")
    if not isinstance(receivers, dict):
        return [(requirement_id, "受け先の宣言自体が無い。")
                for requirement_id in BOUND_REQUIREMENT_IDS]
    problems = []
    for requirement_id in BOUND_REQUIREMENT_IDS:
        section = receivers.get(requirement_id)
        if not section:
            problems.append(
                (requirement_id, "束縛RequirementにContract側の受け先が無い。")
            )
        elif section not in CONTRACT_SECTIONS:
            problems.append(
                (requirement_id, f"受け先`{section}`はContractの10節に無い。")
            )
        elif not contract.get(section):
            problems.append((requirement_id, f"受け先`{section}`が空である。"))
    for requirement_id in sorted(set(receivers) - set(BOUND_REQUIREMENT_IDS)):
        problems.append(
            (requirement_id, "束縛16件に無いRequirementの受け先が宣言されている。")
        )
    return problems


def _check_sections(contract):
    """D2：10節が非空で、AcceptanceとProvenanceがDefinition Challengeを必須にする。"""

    problems = [
        f"節`{section}`が空である。"
        for section in CONTRACT_SECTIONS
        if not contract.get(section)
    ]
    acceptance = contract.get("acceptance") or []
    if not any("definition_challenge" in str(item) for item in acceptance):
        problems.append("AcceptanceがDefinition Challengeの通過を要求していない。")
    required_edges = (contract.get("provenance_obligations") or {}).get(
        "required_edges"
    ) or []
    if "definition_challenge_verdict" not in required_edges:
        problems.append("Provenance obligationsがDefinition Challengeを含まない。")
    return problems


def _check_scope(contract):
    """D3：対象は`docs/`配下の一文書だけである。"""

    targets = (contract.get("boundary") or {}).get("target_paths") or []
    if len(targets) != 1:
        return [f"対象文書が{len(targets)}件である。一件だけを対象にする。"]
    if not str(targets[0]).startswith("docs/"):
        return [f"対象`{targets[0]}`が`docs/`配下でない。"]
    return []


def _check_forbidden_capabilities(contract):
    """D4：禁止能力が明示的に偽である。"""

    capabilities = contract.get("allowed_capabilities") or {}
    return [
        f"禁止能力`{name}`が偽で固定されていない。"
        for name in FORBIDDEN_CAPABILITIES
        if capabilities.get(name) is not False
    ]


def _check_owner_separation(contract):
    """D5：review判断のownerがcompile前に固定され、pairwise distinctである。"""

    owners = contract.get("review_owners")
    if not isinstance(owners, dict):
        return ["review ownerの宣言自体が無い。"]
    problems = [
        f"`{role}`のownerが空である。"
        for role in SEPARATED_REVIEW_ROLES
        if not owners.get(role)
    ]
    assigned = {}
    for role, owner in sorted(owners.items()):
        if not owner:
            continue
        if owner in assigned:
            problems.append(
                f"`{assigned[owner]}`と`{role}`が同じowner`{owner}`である。"
            )
        else:
            assigned[owner] = role
    return problems


def _check_deferred_requirements(contract):
    """D6：deferred Requirementを黙って受理していない。"""

    declared = sorted(contract.get("requirement_ids") or [])
    if declared == sorted(BOUND_REQUIREMENT_IDS):
        return []
    extra = sorted(set(declared) - set(BOUND_REQUIREMENT_IDS))
    missing = sorted(set(BOUND_REQUIREMENT_IDS) - set(declared))
    problems = []
    if extra:
        problems.append(f"束縛16件の外のRequirementを受理している：{','.join(extra)}")
    if missing:
        problems.append(f"束縛Requirementが宣言から欠けている：{','.join(missing)}")
    return problems


def _check_material_binding(contract, material_set):
    """D7の後半：material setが検査対象のContractへ結ばれている。"""

    if material_set.get("contract_ref") != record_ref(contract):
        return ["material setが別のContractへ結ばれている。"]
    return []


def _check_stage_confusion(material_set):
    """D8：compile後または成果側のrecordを入力にしていない。"""

    problems = []
    for item in material_set.get("records") or []:
        kind = item.get("record_kind") if isinstance(item, dict) else None
        if kind in STAGE_CONFUSION_KINDS:
            problems.append(
                f"compile後または成果側のrecord`{kind}`をDefinition Challengeの材料にしている。"
            )
    return problems


def run_definition_challenge(
    *,
    project_root,
    contract,
    requirement_binding,
    material_set,
    owner=DEFINITION_CHALLENGE_OWNER,
):
    """D1〜D8を決定的に実行し、`definition_challenge_verdict`を返す。

    材料の欠落とDigest不一致だけは、verdictを発行せずに停止する（設計§2.2）。
    """

    if not isinstance(material_set, dict) or material_set.get(
        "record_kind"
    ) != "definition_challenge_material_set":
        raise ContractError("definition_material_missing", "material set required")
    _verify_materials(project_root=project_root, material_set=material_set)

    findings = []

    def add(check_id, problems, requirement_ids=None):
        for offset, description in enumerate(problems):
            requirement_id = None
            if requirement_ids is not None:
                requirement_id = requirement_ids[offset]
            findings.append(
                _finding(
                    len(findings) + 1, check_id,
                    contract=contract,
                    description=description,
                    requirement_id=requirement_id,
                )
            )

    receiver_problems = _check_requirement_receivers(contract)
    add(
        "D1",
        [description for _identifier, description in receiver_problems],
        [identifier for identifier, _description in receiver_problems],
    )
    add("D2", _check_sections(contract))
    add("D3", _check_scope(contract))
    add("D4", _check_forbidden_capabilities(contract))
    add("D5", _check_owner_separation(contract))
    add("D6", _check_deferred_requirements(contract))
    add("D7", _check_material_binding(contract, material_set))
    add("D8", _check_stage_confusion(material_set))

    blocking_count = len(
        [item for item in findings if item["severity"] == "blocking"]
    )
    return seal(
        {
            "record_kind": "definition_challenge_verdict",
            "record_id": f"DCV-{contract['record_id']}",
            "record_version": 1,
            "owner": owner,
            "status": "failed" if blocking_count else "passed",
            "contract_ref": record_ref(contract),
            "material_set_ref": record_ref(material_set),
            "requirement_binding_ref": record_ref(requirement_binding),
            "checks": list(DEFINITION_CHECKS),
            "findings": findings,
            "blocking_count": blocking_count,
        }
    )


def build_contract_approval(
    *,
    contract,
    definition_challenge_verdict,
    decision,
    human_id,
    decided_at,
    owner=CONTRACT_APPROVAL_OWNER,
):
    """HumanのContract approvalを耐久recordにする（Amendment§2）。

    会話文、TODO、単なるbooleanでは代用しない。`passed`なverdictへだけ結ぶ。
    このrecordを作るのはHumanの判断であり、機械が代行して`approved`を作らない。
    """

    if decision not in CONTRACT_APPROVAL_DECISIONS:
        raise ContractError("schema_violation", str(decision))
    if not human_id:
        raise ContractError("schema_violation", "human_id")
    if not decided_at:
        raise ContractError("schema_violation", "decided_at")
    if (
        not isinstance(definition_challenge_verdict, dict)
        or definition_challenge_verdict.get("record_kind")
        != "definition_challenge_verdict"
    ):
        raise ContractError("contract_approval_invalid", "definition_challenge_ref")
    if definition_challenge_verdict.get("status") != "passed":
        raise ContractError(
            "contract_approval_invalid", definition_challenge_verdict.get("status")
        )
    if definition_challenge_verdict.get("contract_ref") != record_ref(contract):
        raise ContractError("contract_approval_invalid", "contract_ref")
    if owner in (definition_challenge_verdict.get("owner"), HUMAN_DECISION_OWNER):
        raise ContractError("owner_separation_violated", owner)

    return seal(
        {
            "record_kind": "contract_approval",
            "record_id": f"CA-{contract['record_id']}",
            "record_version": 1,
            "owner": owner,
            "decision_class": CONTRACT_APPROVAL_DECISION_CLASS,
            "decision": decision,
            "human_id": human_id,
            "decided_at": decided_at,
            "contract_ref": record_ref(contract),
            "definition_challenge_ref": record_ref(definition_challenge_verdict),
        }
    )
