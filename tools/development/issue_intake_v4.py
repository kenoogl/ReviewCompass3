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

_DECISION_ID = re.compile(r"DEC-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_ISSUE_ID = re.compile(r"ISSUE-[A-Z0-9]+(?:-[A-Z0-9]+)+")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
)

STOP_CODES = (
    "config_invalid",
    "intake_source_digest_mismatch",
    "intake_rule_excluded",
    "duplicate_suspect_not_flagged",
    "human_ruling_required",
    "human_triage_decision_required",
    "human_triage_decision_field_unknown",
    "human_triage_decision_field_invalid",
    "human_triage_decision_identity_invalid",
    "human_triage_decision_schema_version_unsupported",
    "human_triage_decision_path_invalid",
    "human_triage_decision_path_mismatch",
    "human_triage_decision_disposition_invalid",
    "human_triage_decision_promotion_inconsistent",
    "human_triage_decision_digest_mismatch",
    "human_triage_decision_conflict",
    "candidate_bundle_unavailable",
    "candidate_bundle_digest_mismatch",
    "candidate_bundle_schema_version_mismatch",
    "candidate_record_unavailable",
    "candidate_record_digest_mismatch",
    "candidate_not_found",
    "candidate_digest_mismatch",
    "v4_issue_field_unknown",
    "v4_issue_field_invalid",
    "v4_issue_schema_version_unsupported",
    "v4_issue_identity_invalid",
    "v4_issue_path_invalid",
    "v4_issue_path_mismatch",
    "v4_issue_digest_mismatch",
    "v4_issue_decision_reference_stale",
    "v4_issue_decision_mismatch",
    "v4_issue_duplicate_for_candidate",
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


def canonical_digest(document):
    """`content_digest`を除いた正準表現のSHA-256を返す。"""

    return _canonical_digest(document)


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
        "human_triage_decision_v2", "issue_record_v2",
    ):
        if required not in config:
            raise IntakeError("config_invalid", required)
    if config["maximum_active_issues"] != 1 or config["maximum_active_leaves"] != 1:
        raise IntakeError("config_invalid", "active limits must be 1")
    decision = config["human_triage_decision_v2"]
    for required in (
        "schema_version", "decision_id_prefix", "dispositions", "human_field_names",
        "impact_values", "priority_values", "promotion_disposition", "record_fields",
    ):
        if required not in decision:
            raise IntakeError("config_invalid", f"human_triage_decision_v2.{required}")
    if decision["schema_version"] != 2:
        raise IntakeError("config_invalid", "human triage decision schema must be 2")
    if decision["promotion_disposition"] not in decision["dispositions"]:
        raise IntakeError("config_invalid", "promotion disposition is not in vocabulary")
    if "human_triage_decision_v2" not in config["directories"]:
        raise IntakeError("config_invalid", "directories.human_triage_decision_v2")
    if (
        config["directories"]["human_triage_decision_v2"]
        == config["directories"]["human_triage_decision"]
    ):
        # V1 decision directoryはV1規則のまま保つ。V4 schema 2は別directoryへ置く。
        raise IntakeError("config_invalid", "v4 decisions must not share the v1 directory")
    issue = config["issue_record_v2"]
    for required in ("schema_version", "issue_id_prefix", "initial_state", "record_fields"):
        if required not in issue:
            raise IntakeError("config_invalid", f"issue_record_v2.{required}")
    if issue["schema_version"] != config["issue_schema_version"]:
        raise IntakeError("config_invalid", "v4 issue schema version is inconsistent")
    if issue["initial_state"] not in config["issue_states"]:
        raise IntakeError("config_invalid", "v4 issue initial state is unknown")
    if issue["initial_state"] in config["active_issue_states"]:
        raise IntakeError("config_invalid", "v4 issue must not start as active")
    if "issue_record_v2" not in config["directories"]:
        raise IntakeError("config_invalid", "directories.issue_record_v2")
    if (
        config["directories"]["issue_record_v2"]
        == config["directories"]["issue_record"]
    ):
        # 旧Issue directoryは「Pilot subjectが1件」の検査を持つ。V4 Issueは別directoryへ置く。
        raise IntakeError("config_invalid", "v4 issues must not share the legacy directory")
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


# --------------------------------------------------- V4 Human triage decision v2
#
# 候補bundleは機械抽出時のimmutableな観測である。Humanの判断はbundleへ書き戻さず、
# 一候補につき一件の`human_triage_decision` schema version 2として保存する。
# V1のdecision directoryと規則は変更しない。V4はV4 configのdirectoryを使う。


def _decision_settings(config):
    return config["human_triage_decision_v2"]


def _safe_relative_path(value, code="human_triage_decision_path_invalid"):
    if not isinstance(value, str) or not value:
        raise IntakeError(code, str(value))
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise IntakeError(code, value)
    return path


def _require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise IntakeError("human_triage_decision_field_invalid", label)


def _require_text_field(value, label, code="v4_issue_field_invalid"):
    if not isinstance(value, str) or not value.strip():
        raise IntakeError(code, label)


# candidate_refの2形式（N1）。key集合で形式を判別し、過不足・混在は拒否する。
_BUNDLE_CANDIDATE_REF_FIELDS = frozenset(
    (
        "bundle_path", "bundle_sha256", "bundle_schema_version", "candidate_id",
        "candidate_content_digest",
    )
)
_SINGLE_CANDIDATE_REF_FIELDS = frozenset(
    ("record_path", "record_sha256", "candidate_id", "candidate_content_digest")
)


def _candidate_ref_form(candidate_ref, *, code):
    """candidate_refの形式をkey集合で判別する。過不足・混在は拒否する（N1）。"""

    if isinstance(candidate_ref, dict):
        fields = frozenset(candidate_ref)
        if fields == _BUNDLE_CANDIDATE_REF_FIELDS:
            return "bundle"
        if fields == _SINGLE_CANDIDATE_REF_FIELDS:
            return "single"
    raise IntakeError(code, "candidate_ref")


def _load_candidate_record(*, project_root, candidate_ref):
    """単体候補recordを開き、指紋がすべて一致する場合だけ返す（N2）。

    fileの実在、実bytesのSHA-256一致、record内`candidate_id`一致、
    record内`content_digest`一致を、fail-closedで検証する。
    """

    relative = _safe_relative_path(candidate_ref["record_path"])
    path = Path(project_root) / relative
    if not path.is_file():
        raise IntakeError("candidate_record_unavailable", candidate_ref["record_path"])
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != candidate_ref["record_sha256"]:
        raise IntakeError("candidate_record_digest_mismatch", actual)
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise IntakeError("candidate_record_unavailable", str(error)) from error
    if not isinstance(record, dict) or (
        record.get("candidate_id") != candidate_ref["candidate_id"]
    ):
        raise IntakeError("candidate_not_found", candidate_ref["candidate_id"])
    if record.get("content_digest") != candidate_ref["candidate_content_digest"]:
        raise IntakeError("candidate_digest_mismatch", candidate_ref["candidate_id"])
    return record


def _load_referenced_candidate(*, project_root, candidate_ref, code):
    """candidate_refの形式を判別し、対応する検証読み込みへ振り分ける。"""

    form = _candidate_ref_form(candidate_ref, code=code)
    if form == "bundle":
        _bundle, candidate = _load_candidate_bundle(
            project_root=project_root, candidate_ref=candidate_ref
        )
        return form, candidate
    return form, _load_candidate_record(
        project_root=project_root, candidate_ref=candidate_ref
    )


def _load_candidate_bundle(*, project_root, candidate_ref):
    """bundleを開き、指紋が一致する候補だけを返す。"""

    relative = _safe_relative_path(candidate_ref["bundle_path"])
    path = Path(project_root) / relative
    if not path.is_file():
        raise IntakeError("candidate_bundle_unavailable", candidate_ref["bundle_path"])
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != candidate_ref["bundle_sha256"]:
        raise IntakeError("candidate_bundle_digest_mismatch", actual)
    try:
        bundle = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise IntakeError("candidate_bundle_unavailable", str(error)) from error
    if bundle.get("schema_version") != candidate_ref["bundle_schema_version"]:
        raise IntakeError(
            "candidate_bundle_schema_version_mismatch", str(bundle.get("schema_version"))
        )
    for item in bundle.get("candidates", []):
        if item.get("candidate_id") == candidate_ref["candidate_id"]:
            if item.get("content_digest") != candidate_ref["candidate_content_digest"]:
                raise IntakeError(
                    "candidate_digest_mismatch", candidate_ref["candidate_id"]
                )
            return bundle, item
    raise IntakeError("candidate_not_found", candidate_ref["candidate_id"])


def human_triage_decision_path(decision, *, config):
    """decision IDとversionからV4のrecord pathを決める。"""

    directory = config["directories"]["human_triage_decision_v2"]
    return f"{directory}/{decision['decision_id'].lower()}--v{decision['decision_version']}.json"


def build_human_triage_decision(
    *, project_root, bundle_path=None, candidate_id, decided_at, human_fields,
    disposition, blocking, rationale, next_action, config, decision_version=1,
    supersedes=None, issue_id=None, decision_suffix=None, candidate_record_path=None
):
    """候補を指紋付きで参照するHuman triage decisionを決定的に組み立てる。

    `bundle_path`はbundle形式、`candidate_record_path`は単体形式（N1）の
    candidate_refを作る。どちらか一方だけを指定する。
    """

    settings = _decision_settings(config)
    if (bundle_path is None) == (candidate_record_path is None):
        raise IntakeError(
            "human_triage_decision_field_invalid",
            "exactly one of bundle_path and candidate_record_path is required",
        )
    if candidate_record_path is not None:
        relative = _safe_relative_path(candidate_record_path)
        path = Path(project_root) / relative
        if not path.is_file():
            raise IntakeError("candidate_record_unavailable", candidate_record_path)
        payload = path.read_bytes()
        try:
            candidate = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            raise IntakeError("candidate_record_unavailable", str(error)) from error
        if not isinstance(candidate, dict) or (
            candidate.get("candidate_id") != candidate_id
        ):
            raise IntakeError("candidate_not_found", candidate_id)
        candidate_ref = {
            "record_path": candidate_record_path,
            "record_sha256": hashlib.sha256(payload).hexdigest(),
            "candidate_id": candidate_id,
            "candidate_content_digest": candidate.get("content_digest"),
        }
    else:
        relative = _safe_relative_path(bundle_path)
        path = Path(project_root) / relative
        if not path.is_file():
            raise IntakeError("candidate_bundle_unavailable", bundle_path)
        bundle = json.loads(path.read_text(encoding="utf-8"))
        candidate_ref = {
            "bundle_path": bundle_path,
            "bundle_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bundle_schema_version": bundle.get("schema_version"),
            "candidate_id": candidate_id,
            "candidate_content_digest": None,
        }
        for item in bundle.get("candidates", []):
            if item.get("candidate_id") == candidate_id:
                candidate_ref["candidate_content_digest"] = item.get("content_digest")
                break
        else:
            raise IntakeError("candidate_not_found", candidate_id)

    decision_id = f"{settings['decision_id_prefix']}-{candidate_id}"
    if decision_suffix:
        decision_id = f"{decision_id}-{decision_suffix}"
    promoted = (
        human_fields.get("promote_to_issue") is True
        and disposition == settings["promotion_disposition"]
    )
    promotion = {
        "approved": bool(promoted),
        "issue_id": (issue_id or f"ISSUE-{candidate_id}") if promoted else None,
    }
    if supersedes is not None and "record_kind" in supersedes:
        supersedes = {
            "decision_id": supersedes["decision_id"],
            "decision_version": supersedes["decision_version"],
            "content_digest": supersedes["content_digest"],
        }
    document = {
        "record_kind": "human_triage_decision",
        "schema_version": settings["schema_version"],
        "decision_id": decision_id,
        "decision_version": decision_version,
        "decided_at": decided_at,
        "decision_maker": "human",
        "candidate_ref": candidate_ref,
        "human_fields": {
            name: human_fields[name] for name in settings["human_field_names"]
        },
        "disposition": disposition,
        "blocking": blocking,
        "rationale": rationale,
        "next_action": next_action,
        "supersedes": supersedes,
        "issue_promotion": promotion,
    }
    document["content_digest"] = _canonical_digest(document)
    return document


def validate_human_triage_decision(record, *, path, project_root, config):
    """未知field、bundle path脱出、指紋不一致、schema不一致をfail-closedで拒否する。"""

    settings = _decision_settings(config)
    if not isinstance(record, dict):
        raise IntakeError("human_triage_decision_field_invalid", str(type(record)))
    if record.get("record_kind") != "human_triage_decision":
        raise IntakeError(
            "human_triage_decision_field_invalid", str(record.get("record_kind"))
        )
    # 旧schemaのdecisionはV4規則で再判定しない。schema版の不一致として停止する。
    if record.get("schema_version") != settings["schema_version"]:
        raise IntakeError(
            "human_triage_decision_schema_version_unsupported",
            str(record.get("schema_version")),
        )
    expected_fields = set(settings["record_fields"])
    unknown = sorted(set(record) - expected_fields)
    if unknown:
        raise IntakeError("human_triage_decision_field_unknown", ",".join(unknown))
    missing = sorted(expected_fields - set(record))
    if missing:
        raise IntakeError("human_triage_decision_field_invalid", ",".join(missing))
    if record["decision_maker"] != "human":
        raise IntakeError(
            "human_triage_decision_identity_invalid", str(record["decision_maker"])
        )
    if (
        not isinstance(record["decision_id"], str)
        or not _DECISION_ID.fullmatch(record["decision_id"])
        or not isinstance(record["decision_version"], int)
        or isinstance(record["decision_version"], bool)
        or record["decision_version"] < 1
        or not isinstance(record["decided_at"], str)
        or not _TIMESTAMP.fullmatch(record["decided_at"])
    ):
        raise IntakeError(
            "human_triage_decision_identity_invalid", str(record["decision_id"])
        )

    candidate_ref = record["candidate_ref"]
    form = _candidate_ref_form(
        candidate_ref, code="human_triage_decision_field_unknown"
    )
    digest_fields = (
        ("bundle_sha256", "candidate_content_digest")
        if form == "bundle"
        else ("record_sha256", "candidate_content_digest")
    )
    for field in digest_fields:
        if not isinstance(candidate_ref[field], str) or not _SHA256.fullmatch(
            candidate_ref[field]
        ):
            raise IntakeError("human_triage_decision_field_invalid", field)

    prefix = f"{settings['decision_id_prefix']}-{candidate_ref['candidate_id']}"
    if record["decision_id"] != prefix and not record["decision_id"].startswith(
        f"{prefix}-"
    ):
        raise IntakeError(
            "human_triage_decision_identity_invalid",
            "decision id is not bound to the candidate",
        )
    expected_path = human_triage_decision_path(record, config=config)
    if path != expected_path:
        raise IntakeError("human_triage_decision_path_mismatch", str(path))

    _load_referenced_candidate(
        project_root=project_root, candidate_ref=candidate_ref,
        code="human_triage_decision_field_unknown",
    )

    human_fields = record["human_fields"]
    if not isinstance(human_fields, dict) or set(human_fields) != set(
        settings["human_field_names"]
    ):
        raise IntakeError("human_triage_decision_field_unknown", "human_fields")
    for field in ("unresolved", "recurrence", "promote_to_issue"):
        if not isinstance(human_fields[field], bool):
            raise IntakeError("human_triage_decision_field_invalid", field)
    if human_fields["impact"] not in settings["impact_values"]:
        raise IntakeError("human_triage_decision_field_invalid", "impact")
    if human_fields["priority"] not in settings["priority_values"]:
        raise IntakeError("human_triage_decision_field_invalid", "priority")

    if record["disposition"] not in settings["dispositions"]:
        raise IntakeError(
            "human_triage_decision_disposition_invalid", str(record["disposition"])
        )
    if not isinstance(record["blocking"], bool):
        raise IntakeError("human_triage_decision_field_invalid", "blocking")
    _require_text(record["rationale"], "rationale")
    _require_text(record["next_action"], "next_action")

    supersedes = record["supersedes"]
    if supersedes is not None:
        if not isinstance(supersedes, dict) or set(supersedes) != {
            "decision_id", "decision_version", "content_digest",
        }:
            raise IntakeError("human_triage_decision_field_unknown", "supersedes")
        if (
            not isinstance(supersedes["decision_id"], str)
            or not _DECISION_ID.fullmatch(supersedes["decision_id"])
            or not isinstance(supersedes["decision_version"], int)
            or isinstance(supersedes["decision_version"], bool)
            or supersedes["decision_version"] < 1
            or supersedes["decision_version"] >= record["decision_version"]
            or not isinstance(supersedes["content_digest"], str)
            or not _SHA256.fullmatch(supersedes["content_digest"])
        ):
            raise IntakeError("human_triage_decision_field_invalid", "supersedes")

    promotion = record["issue_promotion"]
    if not isinstance(promotion, dict) or set(promotion) != {"approved", "issue_id"}:
        raise IntakeError("human_triage_decision_field_unknown", "issue_promotion")
    promotable = (
        human_fields["promote_to_issue"] is True
        and record["disposition"] == settings["promotion_disposition"]
    )
    if promotable:
        if promotion["approved"] is not True or not isinstance(
            promotion["issue_id"], str
        ) or not _ISSUE_ID.fullmatch(promotion["issue_id"]):
            raise IntakeError(
                "human_triage_decision_promotion_inconsistent", record["decision_id"]
            )
    elif promotion != {"approved": False, "issue_id": None}:
        raise IntakeError(
            "human_triage_decision_promotion_inconsistent", record["decision_id"]
        )

    if record["content_digest"] != _canonical_digest(record):
        raise IntakeError(
            "human_triage_decision_digest_mismatch", str(record["content_digest"])
        )
    return True


def resolve_effective_triage_decisions(decisions):
    """candidateごとに有効decisionを一つだけ決める。競合は拒否する。"""

    groups = {}
    for decision in decisions:
        candidate_id = decision["candidate_ref"]["candidate_id"]
        groups.setdefault(candidate_id, []).append(decision)

    effective = {}
    for candidate_id, group in groups.items():
        keys = [(item["decision_id"], item["decision_version"]) for item in group]
        if len(set(keys)) != len(keys):
            raise IntakeError("human_triage_decision_conflict", candidate_id)
        by_key = dict(zip(keys, group))
        roots = [item for item in group if item["supersedes"] is None]
        if len(roots) != 1:
            raise IntakeError(
                "human_triage_decision_conflict",
                f"{candidate_id}: {len(roots)} decisions without supersedes",
            )
        superseded = set()
        for item in group:
            reference = item["supersedes"]
            if reference is None:
                continue
            key = (reference["decision_id"], reference["decision_version"])
            target = by_key.get(key)
            if target is None:
                raise IntakeError(
                    "human_triage_decision_conflict",
                    f"{candidate_id}: superseded record is absent",
                )
            if target["content_digest"] != reference["content_digest"]:
                raise IntakeError(
                    "human_triage_decision_conflict",
                    f"{candidate_id}: supersedes digest is stale",
                )
            if item["decision_version"] <= target["decision_version"]:
                raise IntakeError(
                    "human_triage_decision_conflict",
                    f"{candidate_id}: revision version is not increasing",
                )
            if key in superseded:
                raise IntakeError(
                    "human_triage_decision_conflict",
                    f"{candidate_id}: one record is superseded twice",
                )
            superseded.add(key)
        latest = [item for item, key in zip(group, keys) if key not in superseded]
        if len(latest) != 1:
            raise IntakeError("human_triage_decision_conflict", candidate_id)
        effective[candidate_id] = latest[0]
    return effective


def load_triage_decisions(*, project_root, config):
    """V4 decision directoryのrecordだけを読む。V1 directoryは触らない。"""

    directory = Path(project_root) / config["directories"]["human_triage_decision_v2"]
    if not directory.is_dir():
        return []
    decisions = []
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise IntakeError("human_triage_decision_field_invalid", str(path)) from error
        relative = path.relative_to(Path(project_root)).as_posix()
        validate_human_triage_decision(
            record, path=relative, project_root=project_root, config=config
        )
        decisions.append(record)
    return decisions


def validate_triage_decision_repository(*, project_root, config):
    """decision単体だけでなく、集合の競合も確認する。"""

    decisions = load_triage_decisions(project_root=project_root, config=config)
    return resolve_effective_triage_decisions(decisions)


def promote_candidate_from_decision(
    *, candidate, decision, project_root, config, decisions=()
):
    """検証済みHuman decisionが昇格を承認した場合だけIssueを作る。

    候補bundleの`human_fields`は読まず、変更もしない。
    """

    settings = _decision_settings(config)
    if decision is None:
        raise IntakeError(
            "human_triage_decision_required", str(candidate.get("candidate_id"))
        )
    path = human_triage_decision_path(decision, config=config)
    validate_human_triage_decision(
        decision, path=path, project_root=project_root, config=config
    )
    candidate_ref = decision["candidate_ref"]
    if candidate.get("candidate_id") != candidate_ref["candidate_id"]:
        raise IntakeError("candidate_not_found", str(candidate.get("candidate_id")))
    if candidate.get("content_digest") != candidate_ref["candidate_content_digest"]:
        raise IntakeError("candidate_digest_mismatch", candidate_ref["candidate_id"])
    if decision["human_fields"]["promote_to_issue"] is not True:
        raise IntakeError("human_triage_decision_required", candidate_ref["candidate_id"])
    if decision["disposition"] != settings["promotion_disposition"]:
        raise IntakeError("human_triage_decision_required", decision["disposition"])
    promotion = decision["issue_promotion"]
    if promotion["approved"] is not True:
        raise IntakeError(
            "human_triage_decision_promotion_inconsistent", decision["decision_id"]
        )
    if decisions:
        effective = resolve_effective_triage_decisions(decisions)
        chosen = effective.get(candidate_ref["candidate_id"])
        if chosen is None or (
            chosen["decision_id"],
            chosen["decision_version"],
        ) != (decision["decision_id"], decision["decision_version"]):
            raise IntakeError(
                "human_triage_decision_conflict", candidate_ref["candidate_id"]
            )
    return {
        "record_kind": "issue_record",
        "schema_version": config["issue_schema_version"],
        "issue_id": promotion["issue_id"],
        "issue_version": 1,
        "state": "registered",
        "problem": candidate["quotation"],
        "candidate_ref": dict(candidate_ref),
        "triage_decision_ref": {
            "decision_id": decision["decision_id"],
            "decision_version": decision["decision_version"],
            "path": path,
            "content_digest": decision["content_digest"],
        },
    }


# ------------------------------------------------------- V4 Issue永続化（schema 2）
#
# 旧Issue directoryは「旧Pilot subjectが1件」の検査を持つため、V4 IssueはV4専用
# directoryへ永続保存する。旧IssueをV4語彙で再判定しない。


def _issue_settings(config):
    return config["issue_record_v2"]


def v4_issue_path(issue, *, config):
    """issue IDとversionからV4 Issueのrecord pathを決める。"""

    directory = config["directories"]["issue_record_v2"]
    return f"{directory}/{issue['issue_id'].lower()}--v{issue['issue_version']}.json"


def build_v4_issue_record(
    *, candidate, decision, project_root, config, created_at, problem=None,
    decisions=(), issue_version=1
):
    """検証済みHuman triage decisionから、永続保存できるV4 Issueを決定的に作る。

    候補bundleは読むだけで書き換えない。初期stateは`registered`であり、
    `in_progress`へは進めない。
    """

    settings = _issue_settings(config)
    if "quotation" not in candidate and "problem" in candidate:
        # 単体形式（N1）が指すimprovement_candidateは本文を`problem`に持つ。
        # 昇格整合検査には同じ内容を`quotation`として写した複製を渡し、
        # 候補record本体は変更しない。
        candidate = dict(candidate, quotation=candidate["problem"])
    draft = promote_candidate_from_decision(
        candidate=candidate, decision=decision, project_root=project_root,
        config=config, decisions=decisions,
    )
    decision_path = human_triage_decision_path(decision, config=config)
    decision_file = Path(project_root) / _safe_relative_path(
        decision_path, "v4_issue_path_invalid"
    )
    if not decision_file.is_file():
        raise IntakeError("v4_issue_decision_reference_stale", decision_path)
    document = {
        "record_kind": "issue_record",
        "schema_version": settings["schema_version"],
        "issue_id": draft["issue_id"],
        "issue_version": issue_version,
        "created_at": created_at,
        "state": settings["initial_state"],
        "problem": candidate["quotation"] if problem is None else problem,
        "candidate_ref": dict(decision["candidate_ref"]),
        "triage_decision_ref": {
            "decision_id": decision["decision_id"],
            "decision_version": decision["decision_version"],
            "path": decision_path,
            "sha256": hashlib.sha256(decision_file.read_bytes()).hexdigest(),
            "content_digest": decision["content_digest"],
        },
    }
    document["content_digest"] = _canonical_digest(document)
    return document


def validate_v4_issue_record(record, *, path, project_root, config):
    """未知field、path脱出、digest不一致、参照decision不一致を拒否する。"""

    settings = _issue_settings(config)
    decision_settings = _decision_settings(config)
    if not isinstance(record, dict):
        raise IntakeError("v4_issue_field_invalid", str(type(record)))
    if record.get("record_kind") != "issue_record":
        raise IntakeError("v4_issue_field_invalid", str(record.get("record_kind")))
    # 旧schemaのIssueはV4語彙で再判定しない。schema版の不一致として停止する。
    if record.get("schema_version") != settings["schema_version"]:
        raise IntakeError(
            "v4_issue_schema_version_unsupported", str(record.get("schema_version"))
        )
    expected_fields = set(settings["record_fields"])
    unknown = sorted(set(record) - expected_fields)
    if unknown:
        raise IntakeError("v4_issue_field_unknown", ",".join(unknown))
    missing = sorted(expected_fields - set(record))
    if missing:
        raise IntakeError("v4_issue_field_invalid", ",".join(missing))
    if (
        not isinstance(record["issue_id"], str)
        or not _ISSUE_ID.fullmatch(record["issue_id"])
        or not record["issue_id"].startswith(f"{settings['issue_id_prefix']}-")
        or not isinstance(record["issue_version"], int)
        or isinstance(record["issue_version"], bool)
        or record["issue_version"] < 1
        or not isinstance(record["created_at"], str)
        or not _TIMESTAMP.fullmatch(record["created_at"])
    ):
        raise IntakeError("v4_issue_identity_invalid", str(record["issue_id"]))
    if record["state"] not in config["issue_states"]:
        raise IntakeError("issue_state_unknown", str(record["state"]))
    if path != v4_issue_path(record, config=config):
        raise IntakeError("v4_issue_path_mismatch", str(path))
    _require_text_field(record["problem"], "problem")

    candidate_ref = record["candidate_ref"]
    _load_referenced_candidate(
        project_root=project_root, candidate_ref=candidate_ref,
        code="v4_issue_field_unknown",
    )

    decision_ref = record["triage_decision_ref"]
    if not isinstance(decision_ref, dict) or set(decision_ref) != {
        "decision_id", "decision_version", "path", "sha256", "content_digest",
    }:
        raise IntakeError("v4_issue_field_unknown", "triage_decision_ref")
    relative = _safe_relative_path(decision_ref["path"], "v4_issue_path_invalid")
    decision_file = Path(project_root) / relative
    if not decision_file.is_file():
        raise IntakeError("v4_issue_decision_reference_stale", decision_ref["path"])
    if hashlib.sha256(decision_file.read_bytes()).hexdigest() != decision_ref["sha256"]:
        raise IntakeError("v4_issue_decision_reference_stale", decision_ref["path"])
    try:
        decision = json.loads(decision_file.read_text(encoding="utf-8"))
    except ValueError as error:
        raise IntakeError(
            "v4_issue_decision_reference_stale", decision_ref["path"]
        ) from error
    validate_human_triage_decision(
        decision, path=decision_ref["path"], project_root=project_root, config=config
    )
    if (
        decision["decision_id"] != decision_ref["decision_id"]
        or decision["decision_version"] != decision_ref["decision_version"]
        or decision["content_digest"] != decision_ref["content_digest"]
        or decision["candidate_ref"] != candidate_ref
    ):
        raise IntakeError("v4_issue_decision_mismatch", decision_ref["decision_id"])
    if (
        decision["human_fields"]["promote_to_issue"] is not True
        or decision["disposition"] != decision_settings["promotion_disposition"]
        or decision["issue_promotion"]["approved"] is not True
        or decision["issue_promotion"]["issue_id"] != record["issue_id"]
    ):
        raise IntakeError("v4_issue_decision_mismatch", record["issue_id"])

    if record["content_digest"] != _canonical_digest(record):
        raise IntakeError("v4_issue_digest_mismatch", str(record["content_digest"]))
    return True


def load_v4_issues(*, project_root, config):
    """V4 Issue directoryのrecordだけを読む。旧Issue directoryは触らない。"""

    directory = Path(project_root) / config["directories"]["issue_record_v2"]
    if not directory.is_dir():
        return []
    issues = []
    for path in sorted(directory.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise IntakeError("v4_issue_field_invalid", str(path)) from error
        relative = path.relative_to(Path(project_root)).as_posix()
        validate_v4_issue_record(
            record, path=relative, project_root=project_root, config=config
        )
        issues.append(record)
    return issues


def validate_v4_issue_repository(*, project_root, config):
    """record単体だけでなく、同一candidateへの有効Issue重複も拒否する。"""

    issues = load_v4_issues(project_root=project_root, config=config)
    seen_ids = set()
    effective = {}
    for issue in issues:
        if issue["issue_id"] in seen_ids:
            raise IntakeError("v4_issue_identity_invalid", issue["issue_id"])
        seen_ids.add(issue["issue_id"])
        if issue["state"] in config["terminal_issue_states"]:
            continue
        candidate_id = issue["candidate_ref"]["candidate_id"]
        if candidate_id in effective:
            raise IntakeError("v4_issue_duplicate_for_candidate", candidate_id)
        effective[candidate_id] = issue
    validate_issue_set(issues=list(effective.values()), config=config)
    return effective


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
