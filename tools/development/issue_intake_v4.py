"""Issue Intake V4の決定的validator。

正本設計：docs/design/2026-08-05-historical-todo-issue-intake-proposal.md
登録済みIssue数に上限を置かず、`in_progress`だけを最大1件に制限する。
`blocks`の循環は正本へ保存せず、根拠を持つroot cause candidateとして記録する。
既存のV1〜V3のconfigとrecordは変更しない。
"""

import hashlib
import json
import re
from pathlib import Path


DIGEST_ALGORITHM = "sha256"
_HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
_TOP_LEVEL_ITEM = re.compile(r"^- \S")
_COMMIT_SHA = re.compile(r"`[0-9a-f]{7,40}`")
_EVIDENCE_PATH = re.compile(r"`[^`]+\.(?:py|md|json)`")

STOP_CODES = (
    "config_invalid",
    "intake_source_digest_mismatch",
    "intake_rule_excluded",
    "duplicate_suspect_not_flagged",
    "human_ruling_required",
    "active_issue_limit_exceeded",
    "active_leaf_limit_exceeded",
    "suspend_requires_blocks_and_ruling",
    "root_cause_candidate_incomplete",
    "cycle_detection_partial_write",
    "resume_requires_resolution_or_ruling",
    "todo_forbidden_marker",
    "todo_projection_too_large",
    "issue_schema_version_unsupported",
    "issue_state_unknown",
)


class IntakeError(Exception):
    """Issue Intake V4のfail-closed条件に触れた。"""

    def __init__(self, code, detail=None):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _canonical_digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()


def _digest_of(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()


def load_config(path):
    """V4 configを読む。登録上限fieldを持たないことを要求する。"""

    try:
        config = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise IntakeError("config_invalid", str(path)) from error
    if config.get("pilot_version") != 4:
        raise IntakeError("config_invalid", "pilot_version must be 4")
    for forbidden in ("maximum_issue_subjects", "maximum_registered_issues"):
        if forbidden in config:
            raise IntakeError("config_invalid", f"{forbidden} must not exist in v4")
    for required in (
        "maximum_active_issues", "maximum_active_leaves", "issue_states",
        "active_issue_states", "intake", "root_cause_candidate", "todo_projection",
    ):
        if required not in config:
            raise IntakeError("config_invalid", required)
    if config["maximum_active_issues"] != 1 or config["maximum_active_leaves"] != 1:
        raise IntakeError("config_invalid", "active limits must be 1")
    return config


# ------------------------------------------------------------------ Issue state


def validate_issue_record(issue, *, config):
    """V4のissue_recordを検査する。旧schemaへV4のstateを求めない。"""

    if issue.get("record_kind") != "issue_record":
        raise IntakeError("issue_schema_version_unsupported", str(issue.get("record_kind")))
    if issue.get("schema_version") != config["issue_schema_version"]:
        raise IntakeError(
            "issue_schema_version_unsupported", str(issue.get("schema_version"))
        )
    if issue.get("state") not in config["issue_states"]:
        raise IntakeError("issue_state_unknown", str(issue.get("state")))
    return True


def count_active_issues(issues):
    return sum(1 for item in issues if item.get("state") == "in_progress")


def validate_issue_set(*, issues, config):
    """登録数は数えない。`in_progress`だけを上限判定する。"""

    for issue in issues:
        validate_issue_record(issue, config=config)
    if count_active_issues(issues) > config["maximum_active_issues"]:
        raise IntakeError("active_issue_limit_exceeded", str(count_active_issues(issues)))
    return True


def register_issue(*, issues, issue, config, suspend_issue_ids=()):
    """登録に上限を置かない。登録だけで既存Issueを中断しない。"""

    if suspend_issue_ids:
        raise IntakeError(
            "suspend_requires_blocks_and_ruling", ",".join(suspend_issue_ids)
        )
    validate_issue_record(issue, config=config)
    if issue["state"] == "in_progress":
        raise IntakeError("active_issue_limit_exceeded", "registration must not start work")
    updated = list(issues) + [dict(issue)]
    validate_issue_set(issues=updated, config=config)
    return updated


def start_issue(*, issues, issue_id, config):
    """`in_progress`を最大1件に保つ。二件目は拒否する。"""

    updated = [dict(item) for item in issues]
    if count_active_issues(updated) >= config["maximum_active_issues"]:
        raise IntakeError("active_issue_limit_exceeded", issue_id)
    for item in updated:
        if item["issue_id"] == issue_id:
            item["state"] = "in_progress"
            break
    else:
        raise IntakeError("issue_state_unknown", issue_id)
    validate_issue_set(issues=updated, config=config)
    return updated


def resume_issue(*, issues, relations, issue_id, config, human_ruling=None):
    """再開は阻害Issueの`resolved`かHumanの明示裁定がある場合だけ許す。"""

    states = {item["issue_id"]: item.get("state") for item in issues}
    blockers = [
        relation["blocker_issue_id"]
        for relation in relations
        if relation["blocked_issue_id"] == issue_id
    ]
    unresolved = [
        blocker for blocker in blockers if states.get(blocker) not in ("resolved", "rejected")
    ]
    if unresolved and not human_ruling:
        raise IntakeError("resume_requires_resolution_or_ruling", ",".join(unresolved))
    return start_issue(issues=issues, issue_id=issue_id, config=config)


def new_work_state():
    return {"active_work_items": []}


def start_work_item(*, work_state, work_item_id, config):
    if len(work_state["active_work_items"]) >= config["maximum_active_leaves"]:
        raise IntakeError("active_leaf_limit_exceeded", work_item_id)
    work_state["active_work_items"].append(work_item_id)
    return work_state


# ------------------------------------------------------------------ blocks関係


def _relation_id(index):
    return f"REL-{index:04d}"


def declare_blocks(
    *, relations, issues, blocker_issue_id, blocked_issue_id, config, human_ruling=None
):
    """循環にならない`blocks`だけを正本へ保存する。裁定があれば被阻害側を中断する。"""

    persisted, updated, candidate = propose_blocks(
        relations=relations, issues=issues, blocker_issue_id=blocker_issue_id,
        blocked_issue_id=blocked_issue_id, config=config,
    )
    if candidate is not None:
        return persisted, updated
    if human_ruling:
        updated = [
            dict(item, state="suspended")
            if item["issue_id"] == blocked_issue_id and item.get("state") == "in_progress"
            else dict(item)
            for item in updated
        ]
    return persisted, updated


def _cycle_path(relations, blocker_issue_id, blocked_issue_id):
    """提案関係を足すと循環になるか調べ、なる場合は既存経路を返す。"""

    if blocker_issue_id == blocked_issue_id:
        return [blocker_issue_id], []
    outgoing = {}
    for relation in relations:
        outgoing.setdefault(relation["blocker_issue_id"], []).append(relation)
    stack = [(blocked_issue_id, [blocked_issue_id], [])]
    seen = set()
    while stack:
        current, path, used = stack.pop()
        if current == blocker_issue_id:
            return path, used
        if current in seen:
            continue
        seen.add(current)
        for relation in outgoing.get(current, []):
            stack.append(
                (
                    relation["blocked_issue_id"],
                    path + [relation["blocked_issue_id"]],
                    used + [relation["relation_id"]],
                )
            )
    return None, None


def build_root_cause_candidate(
    *, blocker_issue_id, blocked_issue_id, cycle_path_issue_ids, cycle_path_relation_ids,
    affected_issue_ids, input_digest, config
):
    document = {
        "record_kind": "root_cause_escalation_candidate",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "candidate_id": f"RCC-{input_digest[:12].upper()}",
        "proposed_blocker_issue_id": blocker_issue_id,
        "proposed_blocked_issue_id": blocked_issue_id,
        "cycle_path_issue_ids": list(cycle_path_issue_ids),
        "cycle_path_relation_ids": list(cycle_path_relation_ids),
        "affected_issue_ids": sorted(affected_issue_ids),
        "detection_reason": config["root_cause_candidate"]["detection_reason"],
        "input_digest": input_digest,
        "grants_authority": False,
    }
    document["content_digest"] = _canonical_digest(document)
    validate_root_cause_candidate(document, config=config)
    return document


def validate_root_cause_candidate(candidate, *, config):
    """必須証跡が一つでも欠ければ拒否する。"""

    for field in config["root_cause_candidate"]["required_fields"]:
        if field not in candidate or candidate[field] in (None, ""):
            raise IntakeError("root_cause_candidate_incomplete", field)
    if candidate["detection_reason"] != config["root_cause_candidate"]["detection_reason"]:
        raise IntakeError("root_cause_candidate_incomplete", "detection_reason")
    return True


def propose_blocks(
    *, relations, issues, blocker_issue_id, blocked_issue_id, config,
    simulate_partial_write=False
):
    """提案関係をまず検査する。循環なら正本へ保存せずcandidateを返す。

    candidate作成と`suspended`化は一単位で行う。片方だけの書込みを検出したら
    `cycle_detection_partial_write`で停止し、いずれも書き込まない。
    """

    path, used = _cycle_path(relations, blocker_issue_id, blocked_issue_id)
    if path is None:
        persisted = list(relations) + [
            {
                "relation_id": _relation_id(len(relations) + 1),
                "blocker_issue_id": blocker_issue_id,
                "blocked_issue_id": blocked_issue_id,
            }
        ]
        return persisted, [dict(item) for item in issues], None

    input_digest = _digest_of(
        {
            "relations": [dict(item) for item in relations],
            "proposed": {
                "blocker_issue_id": blocker_issue_id,
                "blocked_issue_id": blocked_issue_id,
            },
        }
    )
    affected = sorted(set(path) | {blocker_issue_id, blocked_issue_id})
    candidate = build_root_cause_candidate(
        blocker_issue_id=blocker_issue_id, blocked_issue_id=blocked_issue_id,
        cycle_path_issue_ids=path, cycle_path_relation_ids=used or [],
        affected_issue_ids=affected, input_digest=input_digest, config=config,
    )
    suspended = [
        dict(item, state="suspended") if item["issue_id"] in affected else dict(item)
        for item in issues
    ]
    if simulate_partial_write:
        raise IntakeError("cycle_detection_partial_write", candidate["candidate_id"])
    if count_active_issues(suspended) != 0:
        raise IntakeError("cycle_detection_partial_write", "active issues remain")
    return list(relations), suspended, candidate


def authorize_from_root_cause_candidate(*, candidate, action, config, human_ruling=None):
    """candidateだけでは権限にならない。Humanの明示裁定を要求する。"""

    validate_root_cause_candidate(candidate, config=config)
    if action not in config["root_cause_candidate"]["authority_actions"]:
        raise IntakeError("human_ruling_required", str(action))
    if not human_ruling:
        raise IntakeError("human_ruling_required", action)
    return {"action": action, "human_ruling": human_ruling,
            "candidate_digest": candidate["content_digest"]}


# ------------------------------------------------------------------ 過去TODO intake


def _excluded_rule(*, config, heading_path, quotation):
    intake = config["intake"]
    leaf = heading_path[-1] if heading_path else ""
    if leaf in intake["excluded_headings"]:
        return "X1"
    if not any(heading in intake["included_headings"] for heading in heading_path):
        return "X1"
    stripped = quotation.strip()
    if not stripped or not _TOP_LEVEL_ITEM.match(quotation.lstrip("\n")):
        if quotation.startswith(" ") or quotation.lstrip().startswith("- Evidence"):
            return "X2"
    body = " ".join(
        segment.strip() for segment in stripped.splitlines()
    ).lstrip("- ").strip()
    if any(prefix in body[:24] for prefix in intake["explanation_prefixes"]):
        return "X2"
    if any(marker in body for marker in intake["resolution_markers"]) and (
        _COMMIT_SHA.search(body) or _EVIDENCE_PATH.search(body)
    ):
        return "X3"
    if not body:
        return "X5"
    return None


def build_intake_candidate(
    *, config, heading_path, quotation, source_path, sha256, start_line, end_line
):
    """除外規則を通った行だけを候補にする。`human_fields`は`null`のまま作る。"""

    rule = _excluded_rule(config=config, heading_path=heading_path, quotation=quotation)
    if rule is not None:
        raise IntakeError("intake_rule_excluded", f"{rule}: {quotation.strip()[:40]}")
    body = " ".join(
        segment.strip() for segment in quotation.strip().splitlines()
    ).lstrip("- ").strip()
    document = {
        "record_kind": "historical_todo_intake_candidate",
        "schema_version": 1,
        "digest_algorithm": DIGEST_ALGORITHM,
        "candidate_id": "",
        "source": {
            "relative_path": source_path,
            "sha256": sha256,
            "heading_path": list(heading_path),
            "start_line": start_line,
            "end_line": end_line,
        },
        "quotation": body,
        "applied_rules": ["X1:pass", "X2:pass", "X3:pass", "X5:pass"],
        "duplicate_suspect": {"suspected": False, "matched_record_ids": [], "basis": "未判定"},
        "human_fields": {
            "unresolved": None, "recurrence": None, "impact": None,
            "priority": None, "promote_to_issue": None,
        },
    }
    prefix = config["intake"]["candidate_id_prefix"]
    document["candidate_id"] = f"{prefix}-{_digest_of(document['source'])[:8].upper()}"
    document["content_digest"] = _canonical_digest(document)
    return document


def _normalize(text):
    return re.sub(r"[\s`、。．，．・:：]+", "", text)


def evaluate_duplicate_suspect(*, candidate, existing_records):
    """疑いまでを出す。重複と断定しない。"""

    matched = []
    body = _normalize(candidate["quotation"])
    for record in existing_records:
        problem = _normalize(str(record.get("problem", "")))
        if not problem:
            continue
        if body and (body in problem or problem in body):
            matched.append(record.get("issue_id") or record.get("candidate_id"))
    return {
        "suspected": bool(matched),
        "matched_record_ids": sorted(item for item in matched if item),
        "basis": "quotation正規化の包含一致",
    }


def register_intake_candidate(*, candidate, existing_records, config):
    """重複の疑いを立てずに登録することを拒否する。"""

    evaluated = evaluate_duplicate_suspect(
        candidate=candidate, existing_records=existing_records
    )
    if evaluated["suspected"] and not candidate["duplicate_suspect"]["suspected"]:
        raise IntakeError(
            "duplicate_suspect_not_flagged", ",".join(evaluated["matched_record_ids"])
        )
    updated = dict(candidate, duplicate_suspect=evaluated)
    updated["content_digest"] = _canonical_digest(updated)
    return updated


def promote_candidate_to_issue(*, candidate, config, human_ruling=None):
    """Humanが`promote_to_issue`を真にした場合だけIssueを作る。"""

    if candidate["human_fields"]["promote_to_issue"] is not True or not human_ruling:
        raise IntakeError("human_ruling_required", candidate["candidate_id"])
    return {
        "record_kind": "issue_record",
        "schema_version": config["issue_schema_version"],
        "issue_id": f"ISSUE-{candidate['candidate_id']}",
        "issue_version": 1,
        "state": "registered",
        "problem": candidate["quotation"],
        "candidate_ref": {
            "candidate_id": candidate["candidate_id"],
            "content_digest": candidate["content_digest"],
        },
        "human_ruling": human_ruling,
    }


def extract_intake_candidates(*, project_root, config, source_path, expected_sha256):
    """固定snapshotから決定的に候補を抽出する。Digest不一致では停止する。"""

    path = Path(project_root) / source_path
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected_sha256:
        raise IntakeError("intake_source_digest_mismatch", actual)

    lines = path.read_text(encoding="utf-8").splitlines()
    items = []
    heading_path = []
    current = None
    for number, line in enumerate(lines, start=1):
        matched = _HEADING.match(line)
        if matched:
            if current is not None:
                items.append(current)
                current = None
            level = len(matched.group(1))
            heading_path = heading_path[: level - 2] + [matched.group(2)]
            continue
        if _TOP_LEVEL_ITEM.match(line):
            if current is not None:
                items.append(current)
            current = {
                "heading_path": list(heading_path),
                "lines": [line],
                "start_line": number,
                "end_line": number,
            }
            continue
        if current is None:
            continue
        if line.strip() and line.startswith(" "):
            # 折返しまたは第2階層以下は同じ項目の続きとして畳む。
            current["lines"].append(line)
            current["end_line"] = number
            continue
        items.append(current)
        current = None
    if current is not None:
        items.append(current)

    candidates = []
    for item in items:
        if not any(
            heading in config["intake"]["included_headings"]
            for heading in item["heading_path"]
        ):
            continue
        quotation = "\n".join(item["lines"])
        try:
            candidates.append(
                build_intake_candidate(
                    config=config, heading_path=item["heading_path"], quotation=quotation,
                    source_path=source_path, sha256=expected_sha256,
                    start_line=item["start_line"], end_line=item["end_line"],
                )
            )
        except IntakeError as error:
            if error.code != "intake_rule_excluded":
                raise
    return candidates


# ------------------------------------------------------------------ TODO projection


def build_todo_projection(*, issues, config):
    """`in_progress`の入口だけを出す。登録件数の表示は必須にしない。"""

    projection = config["todo_projection"]
    lines = [projection["heading"], ""]
    active = [item for item in issues if item.get("state") == "in_progress"]
    for item in active[: projection["maximum_entries"]]:
        lines.append(f"- `{item['issue_id']}`：in_progress")
    if not active:
        lines.append("- active Issueなし")
    section = "\n".join(lines) + "\n"
    validate_todo_projection(section=section, config=config)
    return section


def validate_todo_projection(*, section, config):
    projection = config["todo_projection"]
    for marker in projection["forbidden_document_markers"] + projection[
        "forbidden_section_markers"
    ]:
        if marker in section:
            raise IntakeError("todo_forbidden_marker", marker)
    if len(section.encode("utf-8")) > projection["maximum_section_bytes"]:
        raise IntakeError("todo_projection_too_large", str(len(section.encode("utf-8"))))
    entries = [line for line in section.splitlines() if line.startswith("- ")]
    if len(entries) > projection["maximum_entries"]:
        raise IntakeError("todo_projection_too_large", str(len(entries)))
    return True
