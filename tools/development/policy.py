"""リスクベースの開発方針を決定的に評価する。"""

import dataclasses
import json
from pathlib import Path


class DevelopmentPolicyError(Exception):
    """開発方針または変更入力が不正である。"""


@dataclasses.dataclass(frozen=True)
class DevelopmentPolicy:
    policy_id: str
    change_kinds: dict
    risk_verification: dict
    human_approval_actions: tuple
    self_application_maturity: tuple
    commit_policy: str
    validator_assurance_requirements: dict
    post_write_verification_requirements: tuple


@dataclasses.dataclass(frozen=True)
class ChangeEvaluation:
    status: str
    test_timing: str
    commit_policy: str
    verification_requirements: tuple
    human_approval_actions: tuple
    unstable_self_application_capabilities: tuple
    prior_verdict_stale: bool


_POLICY_FIELDS = {
    "change_kinds",
    "commit_policy",
    "human_approval_actions",
    "policy_id",
    "post_write_verification_requirements",
    "record_version",
    "risk_verification",
    "self_application_maturity",
    "validator_assurance_requirements",
}
_CHANGE_KINDS = {
    "behavior",
    "documentation",
    "prototype",
    "research",
}
_CHANGE_KIND_FIELDS = {"base_verification", "test_timing"}
_TEST_TIMINGS = {"before_or_same_change", "not_required"}
_RISK_LEVELS = {"low", "medium", "high"}
_HUMAN_APPROVAL_ACTIONS = {
    "policy_change",
    "external_send",
    "irreversible_operation",
    "semantic_adjudication",
    "stage_completion",
}
_KNOWN_ACTIONS = _HUMAN_APPROVAL_ACTIONS | {"routine_implementation"}


def _text(value):
    return (
        isinstance(value, str)
        and bool(value)
        and "\x00" not in value
        and "\n" not in value
    )


def _texts(value, label, *, empty=False):
    if not isinstance(value, list):
        raise DevelopmentPolicyError(f"{label} must be a list")
    result = tuple(value)
    if (
        (not empty and not result)
        or len(set(result)) != len(result)
        or any(not _text(item) for item in result)
    ):
        raise DevelopmentPolicyError(
            f"{label} must contain unique text"
        )
    return result


def load_policy(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise DevelopmentPolicyError("cannot read development policy") from error
    if (
        not isinstance(data, dict)
        or set(data) != _POLICY_FIELDS
        or data["record_version"] != 2
        or not _text(data["policy_id"])
        or data["commit_policy"] != "integrated_commits_green"
        or not isinstance(data["change_kinds"], dict)
        or set(data["change_kinds"]) != _CHANGE_KINDS
        or not isinstance(data["risk_verification"], dict)
        or set(data["risk_verification"]) != _RISK_LEVELS
        or not isinstance(data["validator_assurance_requirements"], dict)
        or set(data["validator_assurance_requirements"]) != _RISK_LEVELS
    ):
        raise DevelopmentPolicyError("invalid development policy")

    change_kinds = {}
    for identifier, value in data["change_kinds"].items():
        if (
            not isinstance(value, dict)
            or set(value) != _CHANGE_KIND_FIELDS
            or value["test_timing"] not in _TEST_TIMINGS
        ):
            raise DevelopmentPolicyError("invalid change kind policy")
        change_kinds[identifier] = {
            "base_verification": _texts(
                value["base_verification"],
                "base verification",
            ),
            "test_timing": value["test_timing"],
        }

    risk_verification = {
        identifier: _texts(
            value,
            "risk verification",
            empty=True,
        )
        for identifier, value in data["risk_verification"].items()
    }
    validator_assurance = {
        identifier: _texts(
            value,
            "validator assurance requirement",
            empty=True,
        )
        for identifier, value in data[
            "validator_assurance_requirements"
        ].items()
    }
    post_write_verification = _texts(
        data["post_write_verification_requirements"],
        "post-write verification requirement",
    )
    human_actions = _texts(
        data["human_approval_actions"],
        "human approval actions",
    )
    if set(human_actions) != _HUMAN_APPROVAL_ACTIONS:
        raise DevelopmentPolicyError(
            "human approval actions must match the fixed material actions"
        )
    maturity = _texts(
        data["self_application_maturity"],
        "self application maturity",
    )
    if set(maturity) != {"stable"}:
        raise DevelopmentPolicyError(
            "self application must be restricted to stable capabilities"
        )
    return DevelopmentPolicy(
        policy_id=data["policy_id"],
        change_kinds=change_kinds,
        risk_verification=risk_verification,
        human_approval_actions=human_actions,
        self_application_maturity=maturity,
        commit_policy=data["commit_policy"],
        validator_assurance_requirements=validator_assurance,
        post_write_verification_requirements=post_write_verification,
    )


def _self_application_issues(capabilities, allowed_maturity):
    seen = set()
    unstable = []
    for value in capabilities:
        if (
            not isinstance(value, dict)
            or set(value) != {"name", "maturity"}
            or not _text(value["name"])
            or not _text(value["maturity"])
            or value["name"] in seen
        ):
            raise DevelopmentPolicyError(
                "self application capabilities must be unique named records"
            )
        seen.add(value["name"])
        if value["maturity"] not in allowed_maturity:
            unstable.append(value["name"])
    return tuple(unstable)


def evaluate_change(
    policy,
    *,
    change_kind,
    risk,
    actions=(),
    self_application_capabilities=(),
    changes_validator=False,
    changes_input_assumption=False,
    writes_artifact=False,
):
    if not isinstance(policy, DevelopmentPolicy):
        raise DevelopmentPolicyError("expected a loaded development policy")
    if change_kind not in policy.change_kinds or risk not in _RISK_LEVELS:
        raise DevelopmentPolicyError("unknown change kind or risk")
    if (
        not isinstance(actions, (list, tuple))
        or len(set(actions)) != len(actions)
        or any(action not in _KNOWN_ACTIONS for action in actions)
    ):
        raise DevelopmentPolicyError("unknown or duplicate action")
    if not isinstance(self_application_capabilities, (list, tuple)):
        raise DevelopmentPolicyError(
            "self application capabilities must be a sequence"
        )
    if any(
        not isinstance(value, bool)
        for value in (
            changes_validator,
            changes_input_assumption,
            writes_artifact,
        )
    ):
        raise DevelopmentPolicyError("change flags must be boolean")

    change_policy = policy.change_kinds[change_kind]
    verification = list(change_policy["base_verification"])
    if change_kind == "behavior":
        verification.extend(policy.risk_verification[risk])
    prior_verdict_stale = (
        changes_validator or changes_input_assumption
    )
    if prior_verdict_stale:
        verification.extend(
            policy.validator_assurance_requirements[risk]
        )
    if writes_artifact:
        verification.extend(
            policy.post_write_verification_requirements
        )
    approvals = tuple(
        action
        for action in actions
        if action in policy.human_approval_actions
    )
    unstable = _self_application_issues(
        self_application_capabilities,
        frozenset(policy.self_application_maturity),
    )
    if unstable:
        status = "blocked"
    elif approvals:
        status = "approval_required"
    else:
        status = "ready"
    return ChangeEvaluation(
        status=status,
        test_timing=change_policy["test_timing"],
        commit_policy=policy.commit_policy,
        verification_requirements=tuple(verification),
        human_approval_actions=approvals,
        unstable_self_application_capabilities=unstable,
        prior_verdict_stale=prior_verdict_stale,
    )
