"""構造化projectionから短いTODO handoffを決定的に生成する。"""

import hashlib
import re
from pathlib import Path


_SHA256 = re.compile(r"[0-9a-f]{64}")
_REQUIRED_HEADINGS = (
    "## 現在位置",
    "## 現在作業に影響する改善候補／Issue",
    "## 最新のauthority／Evidence",
    "## 次に行う一作業",
    "## blocker・Human判断待ち",
    "## stale・deferred",
    "## Git・Test",
    "## 更新規則",
)
_REQUIRED_FIELDS = {
    "updated_on",
    "overall",
    "current_work",
    "task_contract_id",
    "active_issue",
    "references",
    "next_work",
    "blocker",
    "human_decision",
    "stale",
    "deferred",
    "branch",
    "related_test",
    "full_test",
}


class TodoHandoffProjectionError(Exception):
    """短いhandoffを固定入力から安全に生成できない。"""


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise TodoHandoffProjectionError(f"{label} is invalid")
    return value.strip()


def _project_path(project_root, relative_path):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute() or not path.parts:
        raise TodoHandoffProjectionError(
            "projection reference is stale or unresolved"
        )
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise TodoHandoffProjectionError(
            "projection reference is stale or unresolved"
        ) from error
    return resolved


def _validate_template(project_root, template_path):
    path = _project_path(project_root, template_path)
    try:
        template = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise TodoHandoffProjectionError("TODO template is unavailable") from error
    if any(template.count(heading) != 1 for heading in _REQUIRED_HEADINGS):
        raise TodoHandoffProjectionError(
            "TODO template headings are incomplete"
        )


def _validate_references(project_root, references):
    if not isinstance(references, list) or not references:
        raise TodoHandoffProjectionError(
            "projection reference is stale or unresolved"
        )
    validated = []
    for reference in references:
        if not isinstance(reference, dict) or set(reference) != {
            "label",
            "path",
            "sha256",
        }:
            raise TodoHandoffProjectionError(
                "projection reference is stale or unresolved"
            )
        label = _text(reference["label"], "reference label")
        relative_path = _text(reference["path"], "reference path")
        digest = reference["sha256"]
        path = _project_path(project_root, relative_path)
        if (
            not isinstance(digest, str)
            or not _SHA256.fullmatch(digest)
            or not path.is_file()
            or hashlib.sha256(path.read_bytes()).hexdigest() != digest
        ):
            raise TodoHandoffProjectionError(
                "projection reference is stale or unresolved"
            )
        validated.append((label, relative_path, digest))
    return tuple(validated)


def render_todo_handoff(projection, *, project_root, template_path):
    """templateの固定headingへ構造化current projectionを描画する。"""

    if not isinstance(projection, dict) or set(projection) != _REQUIRED_FIELDS:
        raise TodoHandoffProjectionError("projection fields are invalid")
    _validate_template(project_root, template_path)
    active = projection["active_issue"]
    if not isinstance(active, dict) or set(active) != {
        "issue_id",
        "state",
        "impact",
        "next_action",
    }:
        raise TodoHandoffProjectionError(
            "exactly one active issue is required"
        )
    next_work = projection["next_work"]
    if not isinstance(next_work, dict) or set(next_work) != {
        "action",
        "start_conditions",
        "completion_conditions",
        "following",
    }:
        raise TodoHandoffProjectionError("next work is invalid")
    for field in ("start_conditions", "completion_conditions"):
        if (
            not isinstance(next_work[field], list)
            or not next_work[field]
            or any(not isinstance(value, str) or not value.strip() for value in next_work[field])
        ):
            raise TodoHandoffProjectionError("next work is invalid")
    references = _validate_references(project_root, projection["references"])
    reference_lines = "\n".join(
        f"- [{label}]({path}) — SHA-256 `{digest}`"
        for label, path, digest in references
    )
    start_lines = "\n".join(
        f"- {value.strip()}" for value in next_work["start_conditions"]
    )
    completion_lines = "\n".join(
        f"- {value.strip()}" for value in next_work["completion_conditions"]
    )
    document = f"""# TODO_NEXT_SESSION

更新日：{_text(projection['updated_on'], 'updated_on')}

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：{_text(projection['overall'], 'overall')}
- 現在作業：{_text(projection['current_work'], 'current_work')}
- Task Contract：`{_text(projection['task_contract_id'], 'task_contract_id')}`

## 現在作業に影響する改善候補／Issue

- `{_text(active['issue_id'], 'issue_id')}`：`{_text(active['state'], 'state')}`、影響：{_text(active['impact'], 'impact')}、次：{_text(active['next_action'], 'next_action')}

## 最新のauthority／Evidence

{reference_lines}

## 次に行う一作業

{_text(next_work['action'], 'next action')}

開始条件：

{start_lines}

完了条件：

{completion_lines}

後続作業：{_text(next_work['following'], 'following work')}

## blocker・Human判断待ち

- blocker：{_text(projection['blocker'], 'blocker')}
- Human判断待ち：{_text(projection['human_decision'], 'human_decision')}

## stale・deferred

- stale：{_text(projection['stale'], 'stale')}
- deferred：{_text(projection['deferred'], 'deferred')}

## Git・Test

- branch：`{_text(projection['branch'], 'branch')}`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：{_text(projection['related_test'], 'related_test')}
- 直近の全Test：{_text(projection['full_test'], 'full_test')}
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
"""
    return document.encode("utf-8")
