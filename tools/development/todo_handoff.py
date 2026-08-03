"""Commitと循環しないTODO Git欄を決定的に検査する。"""

import argparse
import dataclasses
import json
import re
from pathlib import Path


_GIT_HEADING = "## Git・Test"
_COMMIT_BOUNDARY = (
    "commit境界：本handoffを含むcommit完了時点"
)
_GIT_STATE_AUTHORITY = (
    "Git状態：HEAD、upstream、ahead／behind、push状態は"
    "Gitから機械取得する"
)
_WORKTREE_BOUNDARY = (
    "worktree：本handoffを含むcommit完了時点でclean"
)
_COMMIT_SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])")


@dataclasses.dataclass(frozen=True)
class HandoffValidation:
    status: str
    findings: tuple

    def report(self):
        return {
            "findings": list(self.findings),
            "status": self.status,
        }


def _git_sections(document):
    lines = document.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line == _GIT_HEADING
    ]
    sections = []
    for start in starts:
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        sections.append("\n".join(lines[start:end]))
    return tuple(sections)


def _has_numbered_git_state(line):
    return (
        ("ahead" in line or "behind" in line)
        and any(character.isdigit() for character in line)
    )


def validate_commit_stable_git_section(document):
    if not isinstance(document, str):
        raise TypeError("document must be text")
    sections = _git_sections(document)
    if not sections:
        return HandoffValidation(
            status="failed",
            findings=("git_section_missing",),
        )
    if len(sections) != 1:
        return HandoffValidation(
            status="failed",
            findings=("git_section_duplicated",),
        )

    section = sections[0]
    lines = section.splitlines()
    findings = []
    if _COMMIT_BOUNDARY not in section:
        findings.append("commit_boundary_missing")
    if _GIT_STATE_AUTHORITY not in section:
        findings.append("git_state_authority_missing")
    if _WORKTREE_BOUNDARY not in section:
        findings.append("worktree_commit_boundary_missing")
    if any(
        line.startswith("- HEAD：") or _COMMIT_SHA.search(line)
        for line in lines
    ):
        findings.append("self_commit_sha_snapshot")
    if any(
        "push済み" in line
        or "push未実施" in line
        or _has_numbered_git_state(line)
        for line in lines
    ):
        findings.append("mutable_remote_snapshot")
    if "未コミット" in section:
        findings.append("uncommitted_worktree_snapshot")
    return HandoffValidation(
        status="failed" if findings else "passed",
        findings=tuple(findings),
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args(argv)
    try:
        document = Path(args.path).read_text(encoding="utf-8")
    except OSError:
        result = HandoffValidation(
            status="failed",
            findings=("todo_read_failed",),
        )
    else:
        result = validate_commit_stable_git_section(document)
    print(json.dumps(result.report(), ensure_ascii=False, sort_keys=True))
    return 0 if result.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
