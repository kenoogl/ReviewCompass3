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


#: `git ls-files -v`が隠蔽指定を表す状態letter。小文字はassume-unchanged、
#: `S`はskip-worktreeである。
_HIDDEN_LETTERS = frozenset("hsmrckS")


def _hidden_entries(listing):
    """索引で表示を抑えられている追跡fileのpathを返す。"""

    hidden = []
    for line in listing.splitlines():
        if len(line) < 3 or line[1] != " ":
            continue
        letter, path = line[0], line[2:]
        if letter in _HIDDEN_LETTERS and path:
            hidden.append(path)
    return hidden


def _hidden_entry_difference(run, project_root):
    """隠蔽指定された追跡fileについて、HEADと作業bytesの差を返す。

    索引の表示に依存せず、blob idを直接比べる。取得できない場合は
    差があるものとして扱う（fail-closed）。
    """

    listing = _git(
        run,
        ("ls-files", "-v"),
        project_root,
        "cannot inspect Git index visibility",
    )
    difference = []
    for path in _hidden_entries(listing):
        try:
            committed = _git(
                run,
                ("rev-parse", f"HEAD:{path}"),
                project_root,
                "cannot resolve the committed blob",
            ).strip()
            actual = _git(
                run,
                ("hash-object", "--", path),
                project_root,
                "cannot hash the working tree file",
            ).strip()
        except WorkUnitTransitionError:
            difference.append(path)
            continue
        if not committed or not actual or committed != actual:
            difference.append(path)
    return "".join(f"{path}\n" for path in difference)


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
    # 索引の隠蔽指定（skip-worktree・assume-unchanged）は`status`も`diff`も
    # 黙らせる。索引の表示に頼らず、HEADのblob idと作業fileのblob idを直接比べる。
    hidden_difference = _hidden_entry_difference(run, project_root)
    return evaluate_transition(
        work_status=work_status,
        porcelain=porcelain,
        head_difference=head_difference + hidden_difference,
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
