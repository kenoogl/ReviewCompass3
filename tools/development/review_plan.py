"""Git差分と開発方針から、レビュー計画を決定的に生成する。"""

import hashlib
import json
from pathlib import Path

from tools.development import policy as development_policy
from tools.development import pilot_collaboration


_RISKS = {"low", "medium", "high"}
_STAGES = {"scope", "completion"}
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


def build_review_plan(
    repository,
    *,
    base_commit,
    target_commit,
    risk,
    stage,
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
    policy_path = repository / "config/development-policy.json"
    try:
        policy_bytes = policy_path.read_bytes()
        loaded_policy = development_policy.load_policy(policy_path)
        evaluated = development_policy.evaluate_change(
            loaded_policy,
            change_kind="behavior",
            risk=risk,
        )
    except (OSError, development_policy.DevelopmentPolicyError) as error:
        raise ReviewPlanStop("policy_invalid") from error
    assignments = []
    if "independent_review" in evaluated.verification_requirements:
        assignments.append(
            {"round": 1, "role": "independent_reviewer", "sequence": 1}
        )
    plan = {
        "base_commit": base,
        "blocking_classes": list(_BLOCKING_CLASSES),
        "changed_paths": paths,
        "policy_id": loaded_policy.policy_id,
        "policy_sha256": hashlib.sha256(policy_bytes).hexdigest(),
        "record_kind": "mechanical_review_plan",
        "result": "completed",
        "risk": risk,
        "round_limit": 1 if assignments else 0,
        "schema_version": 1,
        "scope_expansion": "forbidden",
        "semantic_assignments": assignments,
        "semantic_call_count": len(assignments),
        "stage": stage,
        "target_commit": target,
        "verification_requirements": list(
            evaluated.verification_requirements
        ),
    }
    plan["plan_sha256"] = hashlib.sha256(_canonical_bytes(plan)).hexdigest()
    return plan
