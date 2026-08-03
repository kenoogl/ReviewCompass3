"""開発方針のリスクベース関門に関するテスト。"""

import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
POLICY_PATH = ROOT / "config" / "development-policy.json"


def _policy_module():
    return importlib.import_module("tools.development.policy")


def test_low_risk_behavior_change_uses_lightweight_test_first_gate():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="low",
    )

    assert result.status == "ready"
    assert result.test_timing == "before_or_same_change"
    assert result.commit_policy == "integrated_commits_green"
    assert result.verification_requirements == (
        "relevant_automated_tests",
    )


def test_high_risk_behavior_change_adds_strong_assurance():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="high",
    )

    assert result.status == "ready"
    assert result.verification_requirements == (
        "relevant_automated_tests",
        "full_test_suite",
        "mutation_or_equivalent_fault_injection",
        "representative_data_validation",
        "independent_review",
    )
    assert result.prior_verdict_stale is False


def test_validator_change_adds_assurance_and_stales_prior_verdict():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="medium",
        changes_validator=True,
    )

    assert result.prior_verdict_stale is True
    assert result.verification_requirements == (
        "relevant_automated_tests",
        "full_test_suite",
        "known_positive_fixture",
        "known_negative_fixture",
        "boundary_fixture",
    )


def test_high_risk_validator_change_adds_independent_assurance():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="high",
        changes_validator=True,
    )

    assert result.prior_verdict_stale is True
    assert result.verification_requirements[-3:] == (
        "validator_mutation_or_fault_injection",
        "independent_oracle",
        "representative_validator_data",
    )


def test_input_assumption_change_uses_validator_assurance():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="medium",
        changes_input_assumption=True,
    )

    assert result.prior_verdict_stale is True
    assert "known_negative_fixture" in result.verification_requirements


def test_artifact_write_requires_post_write_verification():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="documentation",
        risk="low",
        writes_artifact=True,
    )

    assert result.verification_requirements == (
        "document_consistency_check",
        "reread_written_artifact",
        "related_validator",
        "reference_integrity",
        "stale_closure_check",
    )


@pytest.mark.parametrize(
    "flag_name",
    ("changes_validator", "changes_input_assumption", "writes_artifact"),
)
def test_change_flags_must_be_boolean(flag_name):
    policy = _policy_module().load_policy(POLICY_PATH)
    arguments = {flag_name: "yes"}

    with pytest.raises(_policy_module().DevelopmentPolicyError):
        _policy_module().evaluate_change(
            policy,
            change_kind="behavior",
            risk="medium",
            **arguments,
        )


@pytest.mark.parametrize("change_kind", ("documentation", "prototype", "research"))
def test_non_product_changes_do_not_require_formal_red_green_cycle(
    change_kind,
):
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind=change_kind,
        risk="low",
    )

    assert result.test_timing == "not_required"
    assert "relevant_automated_tests" not in result.verification_requirements


@pytest.mark.parametrize(
    "action",
    (
        "policy_change",
        "external_send",
        "irreversible_operation",
        "semantic_adjudication",
        "stage_completion",
    ),
)
def test_material_actions_require_human_approval(action):
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="low",
        actions=(action,),
    )

    assert result.status == "approval_required"
    assert result.human_approval_actions == (action,)


def test_routine_implementation_does_not_require_human_approval():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="medium",
        actions=("routine_implementation",),
    )

    assert result.status == "ready"
    assert result.human_approval_actions == ()


def test_self_application_accepts_only_stable_capabilities():
    policy = _policy_module().load_policy(POLICY_PATH)

    stable = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="medium",
        self_application_capabilities=(
            {"name": "source_universe", "maturity": "stable"},
        ),
    )
    provisional = _policy_module().evaluate_change(
        policy,
        change_kind="behavior",
        risk="medium",
        self_application_capabilities=(
            {"name": "triage", "maturity": "provisional"},
        ),
    )

    assert stable.status == "ready"
    assert stable.unstable_self_application_capabilities == ()
    assert provisional.status == "blocked"
    assert provisional.unstable_self_application_capabilities == ("triage",)


def test_rejects_policy_with_unknown_approval_action(tmp_path):
    data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    data["human_approval_actions"].append("routine_implementation")
    invalid_path = tmp_path / "invalid-policy.json"
    invalid_path.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8",
    )

    with pytest.raises(_policy_module().DevelopmentPolicyError):
        _policy_module().load_policy(invalid_path)


@pytest.mark.parametrize(
    "operation_kind",
    ("text_editing", "semantic_analysis"),
)
def test_llm_is_limited_to_text_and_semantic_operations(operation_kind):
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_operation(
        policy,
        operation_kind=operation_kind,
        actual_executor="llm",
        rework_observed=False,
    )

    assert result.status == "ready"
    assert result.expected_executor == "llm"
    assert result.improvement_candidate is None


def test_deterministic_operation_requires_machine_execution():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_operation(
        policy,
        operation_kind="deterministic_operation",
        actual_executor="machine",
        rework_observed=False,
    )

    assert result.status == "ready"
    assert result.expected_executor == "machine"
    assert result.improvement_candidate is None


def test_llm_manual_rework_becomes_reportable_machine_candidate():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_operation(
        policy,
        operation_kind="deterministic_operation",
        actual_executor="llm",
        rework_observed=True,
    )

    assert result.status == "improvement_candidate_required"
    assert result.expected_executor == "machine"
    assert result.improvement_candidate == "manual_rework_candidate"
    assert result.report_fields == (
        "operation",
        "expected_executor",
        "actual_executor",
        "manual_reason",
        "rework_event",
        "rework_evidence",
        "machine_processing_candidate",
        "route",
    )


def test_llm_manual_operation_without_rework_is_still_a_candidate():
    policy = _policy_module().load_policy(POLICY_PATH)

    result = _policy_module().evaluate_operation(
        policy,
        operation_kind="deterministic_operation",
        actual_executor="llm",
        rework_observed=False,
    )

    assert result.status == "improvement_candidate_required"
    assert result.improvement_candidate == "manual_operation_candidate"
