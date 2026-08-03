"""完了作業単位から次作業へ進む前のcommit関門。"""

import argparse
import dataclasses
import json
import subprocess


class WorkUnitTransitionError(Exception):
    """遷移関門の機械入力を取得できない。"""


@dataclasses.dataclass(frozen=True)
class TransitionResult:
    status: str
    next_work_allowed: object
    findings: tuple
    reminder: object


def evaluate_transition(*, work_status, porcelain):
    if work_status != "completed":
        return TransitionResult(
            status="not_applicable",
            next_work_allowed=None,
            findings=(),
            reminder=None,
        )
    if porcelain.strip():
        return TransitionResult(
            status="blocked",
            next_work_allowed=False,
            findings=("completed_work_unit_uncommitted",),
            reminder=(
                "作業単位は完了していますが、未コミットです。"
                "コミットされるまで次の作業を開始できません。"
            ),
        )
    return TransitionResult(
        status="passed",
        next_work_allowed=True,
        findings=(),
        reminder=None,
    )


def preflight_next_work(
    *,
    work_status,
    project_root=".",
    run=subprocess.run,
):
    result = run(
        ("git", "status", "--porcelain=v1", "--untracked-files=all"),
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise WorkUnitTransitionError(
            "cannot inspect Git worktree state"
        )
    return evaluate_transition(
        work_status=work_status,
        porcelain=result.stdout,
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--work-status",
        choices=("in_progress", "completed"),
        required=True,
    )
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args(argv)
    result = preflight_next_work(
        work_status=args.work_status,
        project_root=args.project_root,
    )
    print(
        json.dumps(
            dataclasses.asdict(result),
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 1 if result.status == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
