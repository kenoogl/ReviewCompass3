"""record identityとDigestの共通規則。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md
承認：DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001
"""

import hashlib
import json
from pathlib import Path
from tools.common.errors import FailClosedError


DIGEST_ALGORITHM = "sha256"

RECORD_KINDS = (
    "requirement_binding",
    "source_snapshot",
    "review_task_contract",
    "definition_challenge_material_set",
    "definition_challenge_verdict",
    "contract_approval",
    "compile_verdict",
    "plan_bundle",
    "context_manifest",
    "workflow_permit",
    "finding_set",
    "conformance_verdict",
    "final_challenge_verdict",
    "human_decision",
    "provenance_verdict",
    "accepted_artifact",
)

STOP_CODES = (
    "schema_violation",
    "contract_section_missing",
    "not_compilable",
    "unreceived_obligation",
    "context_incomplete",
    "implicit_material_rejected",
    "path_out_of_scope",
    "stale",
    "not_permitted",
    "owner_separation_violated",
    "provenance_edge_missing",
    "provenance_edge_unexpected",
    "provenance_edge_endpoint_unresolved",
    "provenance_node_missing",
    "provenance_node_duplicated",
    "provenance_node_kind_mismatch",
    "provenance_node_identity_mismatch",
    "provenance_node_digest_mismatch",
    "provenance_self_reference",
    "decision_digest_mismatch",
    "human_decision_missing",
    "human_decision_not_approved",
    # Definition Challenge（設計§3のD1〜D8）
    "definition_requirement_unreceived",
    "definition_section_missing",
    "definition_scope_violation",
    "definition_forbidden_capability",
    "definition_owner_separation",
    "definition_deferred_requirement_accepted",
    "definition_material_missing",
    "definition_stage_confusion",
    # compile事前gate（Amendment§3の閉じたreason）
    "definition_challenge_missing",
    "definition_challenge_failed",
    "definition_challenge_invalid",
    "contract_approval_missing",
    "contract_approval_rejected",
    "contract_approval_invalid",
)


class ContractError(FailClosedError):
    """最小Review Task Contractのfail-closed条件に触れた。"""


def canonical_bytes(value):
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


from tools.common.digests import canonical_content_digest as content_digest


from tools.common.digests import file_sha256 as file_sha256


def seal(document):
    """recordへcontent_digestを与える。以後は書き換えない前提とする。"""

    if document.get("record_kind") not in RECORD_KINDS:
        raise ContractError("schema_violation", str(document.get("record_kind")))
    document["content_digest"] = content_digest(document)
    return document


def record_ref(document):
    """上流recordへの参照。identity、version、Digestを同時に持つ。"""

    return {
        "record_kind": document["record_kind"],
        "record_id": document["record_id"],
        "record_version": document["record_version"],
        "digest_algorithm": DIGEST_ALGORITHM,
        "content_digest": document["content_digest"],
    }


def safe_relative_path(value):
    """project相対pathだけを許す。脱出と絶対pathを拒否する。"""

    if not isinstance(value, str) or not value:
        raise ContractError("path_out_of_scope", "empty path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise ContractError("path_out_of_scope", value)
    return value


def validate_record(document):
    """recordの最小不変条件を検査する。"""

    if not isinstance(document, dict):
        raise ContractError("schema_violation", "record must be a mapping")
    kind = document.get("record_kind")
    if kind not in RECORD_KINDS:
        raise ContractError("schema_violation", str(kind))
    for field in ("record_id", "record_version", "content_digest"):
        if not document.get(field):
            raise ContractError("schema_violation", field)
    if kind == "review_task_contract":
        for section in CONTRACT_SECTIONS:
            if not document.get(section):
                raise ContractError("contract_section_missing", section)
    if content_digest(document) != document["content_digest"]:
        raise ContractError("schema_violation", "content_digest")
    return document


CONTRACT_SECTIONS = (
    "identity",
    "responsibility",
    "boundary",
    "preconditions",
    "context_obligations",
    "allowed_capabilities",
    "expected_output",
    "acceptance",
    "provenance_obligations",
    "escalation",
)
