"""Work 5A 最小Review Task ContractのRuntime package。

正本設計：docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md
承認：DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001

一Contract type、一Compiler version、`new_development / fresh`だけを扱う。
LLM、外部送信、Git write、CIを使わない。`tools/bootstrap/`は参照せず、昇格もしない。
"""

from tools.task_contract.contract import (
    CONTINUATION_CLASSES,
    ORIGIN_CLASSES,
    PLAN_VIEWS,
    REQUIREMENT_OBLIGATIONS,
    SEVERITY_CLASSES,
    bind_requirements,
    build_review_task_contract,
    check_requirement_coverage,
    compile_contract,
)
from tools.task_contract.execution import (
    accept_artifact,
    acquire_permit,
    active_leaf_count,
    assert_context_fresh,
    build_context_manifest,
    evaluate_conformance,
    evaluate_final_challenge,
    new_workflow_state,
    read_source_snapshot,
    record_human_decision,
    release_permit,
    run_stub_reviewer,
    verify_provenance,
)
from tools.task_contract.identity import (
    CONTRACT_SECTIONS,
    RECORD_KINDS,
    STOP_CODES,
    ContractError,
    record_ref,
    validate_record,
)

__all__ = [
    "CONTINUATION_CLASSES",
    "CONTRACT_SECTIONS",
    "ContractError",
    "ORIGIN_CLASSES",
    "PLAN_VIEWS",
    "RECORD_KINDS",
    "REQUIREMENT_OBLIGATIONS",
    "SEVERITY_CLASSES",
    "STOP_CODES",
    "accept_artifact",
    "acquire_permit",
    "active_leaf_count",
    "assert_context_fresh",
    "bind_requirements",
    "build_context_manifest",
    "build_review_task_contract",
    "check_requirement_coverage",
    "compile_contract",
    "evaluate_conformance",
    "evaluate_final_challenge",
    "new_workflow_state",
    "read_source_snapshot",
    "record_human_decision",
    "record_ref",
    "release_permit",
    "run_stub_reviewer",
    "validate_record",
    "verify_provenance",
]
