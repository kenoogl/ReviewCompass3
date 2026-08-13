"""Git差分と開発方針から、レビュー計画を決定的に生成する。"""

import hashlib
import json
from pathlib import Path

from tools.development import policy as development_policy
from tools.development import pilot_collaboration


_RISKS = {"low", "medium", "high"}
_STAGES = {"scope", "completion"}
_RISK_ORDER = {"low": 0, "medium": 1, "high": 2}
_TARGET_KINDS = (
    "documentation",
    "product_code",
    "test_code",
    "validator_code",
    "configuration",
    "structured_data",
)
_BLOCKING_CLASSES = (
    "authority_conflict",
    "human_boundary_missing",
    "demonstrable_false_verdict",
    "scope_or_schema_violation",
)


class ReviewPlanStop(Exception):
    """安全なレビュー計画を生成できない。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _run_git(repository, *arguments, text=True):
    try:
        return pilot_collaboration._run_git(
            repository,
            *arguments,
            binary=not text,
        )
    except Exception as error:
        raise ReviewPlanStop("git_unavailable") from error


def _commit(repository, value):
    if not isinstance(value, str) or not value:
        raise ReviewPlanStop("commit_invalid")
    completed = _run_git(
        repository,
        "rev-parse",
        "--verify",
        f"{value}^{{commit}}",
    )
    if completed.returncode != 0:
        raise ReviewPlanStop("commit_invalid")
    commit = completed.stdout.strip()
    if (
        len(commit) != 40
        or any(character not in "0123456789abcdef" for character in commit)
    ):
        raise ReviewPlanStop("commit_invalid")
    return commit


def _changed_paths(repository, base_commit, target_commit):
    ancestor = _run_git(
        repository,
        "merge-base",
        "--is-ancestor",
        base_commit,
        target_commit,
    )
    if ancestor.returncode != 0:
        raise ReviewPlanStop("commit_order_invalid")
    completed = _run_git(
        repository,
        "diff",
        "--name-only",
        "--diff-filter=ACDMRTUXB",
        "-z",
        base_commit,
        target_commit,
        text=False,
    )
    if completed.returncode != 0:
        raise ReviewPlanStop("diff_failed")
    try:
        paths = [
            item.decode("utf-8")
            for item in completed.stdout.split(b"\0")
            if item
        ]
    except UnicodeDecodeError as error:
        raise ReviewPlanStop("path_invalid") from error
    if not paths:
        raise ReviewPlanStop("change_empty")
    if len(set(paths)) != len(paths):
        raise ReviewPlanStop("path_invalid")
    for value in paths:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or "\x00" in value:
            raise ReviewPlanStop("path_invalid")
    return sorted(paths)


def _safe_relative_path(value):
    if (
        not isinstance(value, str)
        or not value
        or "\x00" in value
        or "\n" in value
    ):
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and bool(path.parts)
        and ".." not in path.parts
        and path.as_posix() == value
    )


def _load_classification(path):
    try:
        raw = Path(path).read_bytes()
        document = json.loads(raw)
    except (OSError, TypeError, ValueError) as error:
        raise ReviewPlanStop("classification_invalid") from error
    if (
        not isinstance(document, dict)
        or set(document) != {"schema_version", "targets", "actions"}
        or document["schema_version"] != 1
        or not isinstance(document["targets"], list)
        or not isinstance(document["actions"], list)
    ):
        raise ReviewPlanStop("classification_invalid")
    actions = document["actions"]
    if (
        any(
            not isinstance(action, str)
            or not action
            or "\x00" in action
            or "\n" in action
            for action in actions
        )
        or len(set(actions)) != len(actions)
    ):
        raise ReviewPlanStop("classification_invalid")
    targets = []
    seen = set()
    for item in document["targets"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "kind"}
            or not _safe_relative_path(item["path"])
            or not isinstance(item["kind"], str)
            or not item["kind"]
            or "\x00" in item["kind"]
            or "\n" in item["kind"]
            or item["path"] in seen
        ):
            raise ReviewPlanStop("classification_invalid")
        seen.add(item["path"])
        targets.append({"path": item["path"], "kind": item["kind"]})
    return raw, targets, tuple(actions)


def _effective_risk(requested, minimum=None):
    if minimum is None or _RISK_ORDER[requested] >= _RISK_ORDER[minimum]:
        return requested
    return minimum


def _group_evaluation(policy, target_kind, risk):
    arguments = {
        "change_kind": "behavior",
        "risk": risk,
    }
    extra_requirements = ()
    if target_kind == "documentation":
        arguments["change_kind"] = "documentation"
    elif target_kind == "validator_code":
        arguments["risk"] = _effective_risk(risk, "high")
        arguments["changes_validator"] = True
        extra_requirements = policy.validator_assurance_requirements[
            "medium"
        ]
    elif target_kind == "configuration":
        arguments["changes_input_assumption"] = True
        extra_requirements = (
            "configuration_impact_check",
            "default_behavior_check",
        )
    elif target_kind == "structured_data":
        arguments["change_kind"] = "documentation"
        arguments["writes_artifact"] = True
        extra_requirements = (
            "schema_identity_reference_check",
            "missing_duplicate_tamper_cases",
        )
    evaluated = development_policy.evaluate_change(policy, **arguments)
    requirements = list(evaluated.verification_requirements)
    for value in extra_requirements:
        if value not in requirements:
            requirements.append(value)
    return evaluated, arguments["risk"], requirements


def _extend_unique(values, additions):
    for value in additions:
        if value not in values:
            values.append(value)


def build_review_plan(
    repository,
    *,
    base_commit,
    target_commit,
    risk,
    stage,
    classification_path,
):
    """現在の承認済み方針から、変更できない一周の計画を作る。"""

    repository = Path(repository).resolve()
    if risk not in _RISKS:
        raise ReviewPlanStop("risk_invalid")
    if stage not in _STAGES:
        raise ReviewPlanStop("stage_invalid")
    base = _commit(repository, base_commit)
    target = _commit(repository, target_commit)
    paths = _changed_paths(repository, base, target)
    classification_bytes, targets, actions = _load_classification(
        classification_path
    )
    policy_path = repository / "config/development-policy.json"
    try:
        policy_bytes = policy_path.read_bytes()
        loaded_policy = development_policy.load_policy(policy_path)
    except (OSError, development_policy.DevelopmentPolicyError) as error:
        raise ReviewPlanStop("policy_invalid") from error
    try:
        action_evaluation = development_policy.evaluate_change(
            loaded_policy,
            change_kind="documentation",
            risk=risk,
            actions=actions,
        )
    except development_policy.DevelopmentPolicyError as error:
        raise ReviewPlanStop("classification_invalid") from error

    changed = set(paths)
    target_by_path = {item["path"]: item for item in targets}
    unclassified = sorted(changed - set(target_by_path))
    extra = sorted(set(target_by_path) - changed)
    unknown = sorted(
        (
            {"path": item["path"], "kind": item["kind"]}
            for item in targets
            if item["kind"] not in _TARGET_KINDS
        ),
        key=lambda item: (item["path"], item["kind"]),
    )
    groups = []
    requirements = []
    try:
        for target_kind in _TARGET_KINDS:
            group_paths = sorted(
                item["path"]
                for item in targets
                if item["path"] in changed and item["kind"] == target_kind
            )
            if not group_paths:
                continue
            evaluated, group_risk, group_requirements = _group_evaluation(
                loaded_policy,
                target_kind,
                risk,
            )
            groups.append(
                {
                    "effective_risk": group_risk,
                    "paths": group_paths,
                    "prior_verdict_stale": evaluated.prior_verdict_stale,
                    "target_kind": target_kind,
                    "test_timing": evaluated.test_timing,
                    "verification_requirements": group_requirements,
                }
            )
            _extend_unique(requirements, group_requirements)
    except development_policy.DevelopmentPolicyError as error:
        raise ReviewPlanStop("policy_invalid") from error

    warnings = []
    if unclassified:
        warnings.append("unclassified_paths")
    if extra:
        warnings.append("extra_paths")
    if unknown:
        warnings.append("unknown_target_kinds")
    assignments = []
    if "independent_review" in requirements:
        assignments.append(
            {"round": 1, "role": "independent_reviewer", "sequence": 1}
        )
    plan = {
        "approval_status": action_evaluation.status,
        "base_commit": base,
        "blocking_classes": list(_BLOCKING_CLASSES),
        "changed_paths": paths,
        "classification_sha256": hashlib.sha256(
            classification_bytes
        ).hexdigest(),
        "extra_paths": extra,
        "human_approval_actions": list(
            action_evaluation.human_approval_actions
        ),
        "policy_id": loaded_policy.policy_id,
        "policy_sha256": hashlib.sha256(policy_bytes).hexdigest(),
        "record_kind": "mechanical_review_plan",
        "result": "completed_with_warnings" if warnings else "completed",
        "review_groups": groups,
        "risk": risk,
        "round_limit": 1 if assignments else 0,
        "schema_version": 2,
        "scope_expansion": "forbidden",
        "semantic_assignments": assignments,
        "semantic_call_count": len(assignments),
        "stage": stage,
        "target_commit": target,
        "unclassified_paths": unclassified,
        "unknown_targets": unknown,
        "verification_requirements": requirements,
        "warnings": warnings,
    }
    plan["plan_sha256"] = hashlib.sha256(_canonical_bytes(plan)).hexdigest()
    return plan
