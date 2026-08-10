"""完了作業単位から次作業へ進む前のcommit関門。"""

import argparse
import dataclasses
import json
import subprocess
from pathlib import Path


class WorkUnitTransitionError(Exception):
    """遷移関門の機械入力を取得できない。"""


@dataclasses.dataclass(frozen=True)
class TransitionResult:
    status: str
    next_work_allowed: object
    findings: tuple
    reminder: object


def evaluate_transition(*, work_status, porcelain, head_difference=""):
    """完了作業単位の未コミットを判定する。

    `porcelain`はGitの表示、`head_difference`はHEADとのbytes差である。
    `skip-worktree`等でindex表示を消しても、bytes差が残れば停止する。
    """

    if work_status != "completed":
        return TransitionResult(
            status="not_applicable",
            next_work_allowed=None,
            findings=(),
            reminder=None,
        )
    if porcelain.strip() or (head_difference or "").strip():
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


def _git(run, arguments, project_root, failure):
    result = run(
        ("git", *arguments),
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise WorkUnitTransitionError(failure)
    return result.stdout


def preflight_next_work(
    *,
    work_status,
    project_root=".",
    run=subprocess.run,
):
    """要求されたrootのGit状態だけを見る。

    別のclean Git rootへ差し替えて合格させられないよう、Gitが答えたtop levelが
    要求rootと同一実体であることを束縛する。
    """

    top_level = _git(
        run,
        ("rev-parse", "--show-toplevel"),
        project_root,
        "cannot resolve the Git repository root",
    ).strip()
    requested = Path(project_root).resolve()
    if not top_level or Path(top_level).resolve() != requested:
        raise WorkUnitTransitionError(
            "requested project root is not the Git repository root"
        )
    porcelain = _git(
        run,
        ("status", "--porcelain=v1", "--untracked-files=all"),
        project_root,
        "cannot inspect Git worktree state",
    )
    head_difference = _git(
        run,
        ("diff", "--name-only", "HEAD", "--"),
        project_root,
        "cannot inspect differences against HEAD",
    )
    return evaluate_transition(
        work_status=work_status,
        porcelain=porcelain,
        head_difference=head_difference,
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
