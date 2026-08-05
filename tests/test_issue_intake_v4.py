"""Issue Intake V4の受入test（設計§5 I1〜I9、J1〜J16）。

正本設計：docs/design/2026-08-05-historical-todo-issue-intake-proposal.md
登録済みIssue数に上限を置かず、`in_progress`だけを最大1件に制限する。
`blocks`の循環は正本へ保存せず、根拠を持つroot cause candidateとして記録する。
"""

import hashlib
import importlib
import json
import shutil
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = "records/session-handoffs/2026-08-04-todo-before-compaction-001.md"
SNAPSHOT_SHA = "16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1"
CONFIG_V4 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v4.json"
CONFIG_V2 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v2.json"
CONFIG_V3 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v3.json"
EXISTING_ISSUE = (
    PROJECT_ROOT / ".reviewcompass/workflow/issues/issue-pilot-todo-growth-001--v1.json"
)


@pytest.fixture
def intake():
    return importlib.import_module("tools.development.issue_intake_v4")


@pytest.fixture
def config(intake):
    return intake.load_config(CONFIG_V4)


def _issue(issue_id, state):
    return {
        "record_kind": "issue_record",
        "schema_version": 2,
        "issue_id": issue_id,
        "issue_version": 1,
        "state": state,
        "problem": f"{issue_id}の問題",
    }


# ------------------------------------------------------------------ 正常例 I1〜I9


def test_i1_intake_extraction_is_deterministic(intake, config):
    first = intake.extract_intake_candidates(
        project_root=PROJECT_ROOT, config=config,
        source_path=SNAPSHOT, expected_sha256=SNAPSHOT_SHA,
    )
    second = intake.extract_intake_candidates(
        project_root=PROJECT_ROOT, config=config,
        source_path=SNAPSHOT, expected_sha256=SNAPSHOT_SHA,
    )
    assert len(first) >= 2
    assert [item["candidate_id"] for item in first] == [
        item["candidate_id"] for item in second
    ]
    assert [item["content_digest"] for item in first] == [
        item["content_digest"] for item in second
    ]
    for item in first:
        assert item["record_kind"] == "historical_todo_intake_candidate"
        assert item["source"]["sha256"] == SNAPSHOT_SHA
        assert item["source"]["start_line"] >= 1
        assert item["quotation"].strip()
        assert item["human_fields"] == {
            "unresolved": None, "recurrence": None, "impact": None,
            "priority": None, "promote_to_issue": None,
        }


def test_i2_existing_resolved_issue_coexists_unchanged(intake, config):
    before = EXISTING_ISSUE.read_bytes()
    candidates = intake.extract_intake_candidates(
        project_root=PROJECT_ROOT, config=config,
        source_path=SNAPSHOT, expected_sha256=SNAPSHOT_SHA,
    )
    assert candidates
    assert EXISTING_ISSUE.read_bytes() == before
    existing = json.loads(before.decode("utf-8"))
    assert existing["schema_version"] == 1
    assert "state" not in existing


def test_i3_registration_has_no_upper_limit(intake, config):
    assert "maximum_registered_issues" not in config
    assert "maximum_issue_subjects" not in config
    issues = []
    for index in range(1, 51):
        issues = intake.register_issue(
            issues=issues, issue=_issue(f"ISSUE-{index:03d}", "registered"), config=config
        )
    assert len(issues) == 50
    assert intake.count_active_issues(issues) == 0


def test_i4_many_non_active_states_with_one_in_progress(intake, config):
    issues = [
        _issue("ISSUE-001", "registered"),
        _issue("ISSUE-002", "untriaged"),
        _issue("ISSUE-003", "deferred"),
        _issue("ISSUE-004", "suspended"),
        _issue("ISSUE-005", "resolved"),
        _issue("ISSUE-006", "rejected"),
        _issue("ISSUE-007", "in_progress"),
    ]
    assert intake.count_active_issues(issues) == 1
    assert intake.validate_issue_set(issues=issues, config=config) is True


def test_i5_registering_non_blocking_issue_does_not_suspend(intake, config):
    issues = [_issue("ISSUE-001", "in_progress")]
    issues = intake.register_issue(
        issues=issues, issue=_issue("ISSUE-002", "registered"), config=config
    )
    states = {item["issue_id"]: item["state"] for item in issues}
    assert states["ISSUE-001"] == "in_progress"
    assert states["ISSUE-002"] == "registered"
    assert intake.count_active_issues(issues) == 1


def test_i6_blocking_switch_suspends_previous(intake, config):
    issues = [_issue("ISSUE-001", "in_progress"), _issue("ISSUE-002", "registered")]
    relations, issues = intake.declare_blocks(
        relations=[], issues=issues,
        blocker_issue_id="ISSUE-002", blocked_issue_id="ISSUE-001",
        human_ruling="ISSUE-002を先に解く", config=config,
    )
    issues = intake.start_issue(issues=issues, issue_id="ISSUE-002", config=config)
    states = {item["issue_id"]: item["state"] for item in issues}
    assert states["ISSUE-001"] == "suspended"
    assert states["ISSUE-002"] == "in_progress"
    assert intake.count_active_issues(issues) == 1
    assert len(relations) == 1


def test_i7_resume_after_blocker_resolved_or_human_ruling(intake, config):
    issues = [_issue("ISSUE-001", "suspended"), _issue("ISSUE-002", "resolved")]
    relations = [
        {"relation_id": "REL-001", "blocker_issue_id": "ISSUE-002",
         "blocked_issue_id": "ISSUE-001"}
    ]
    resumed = intake.resume_issue(
        issues=issues, relations=relations, issue_id="ISSUE-001", config=config
    )
    assert {item["issue_id"]: item["state"] for item in resumed}["ISSUE-001"] == "in_progress"

    blocked = [_issue("ISSUE-003", "suspended"), _issue("ISSUE-004", "in_progress")]
    other = [
        {"relation_id": "REL-002", "blocker_issue_id": "ISSUE-004",
         "blocked_issue_id": "ISSUE-003"}
    ]
    with pytest.raises(intake.IntakeError):
        intake.resume_issue(
            issues=blocked, relations=other, issue_id="ISSUE-003", config=config
        )
    ruled = intake.resume_issue(
        issues=[_issue("ISSUE-003", "suspended")], relations=other,
        issue_id="ISSUE-003", human_ruling="Humanが再開を裁定", config=config,
    )
    assert {item["issue_id"]: item["state"] for item in ruled}["ISSUE-003"] == "in_progress"


def test_i8_todo_projection_fits_limits_without_registered_count(intake, config):
    issues = [_issue(f"ISSUE-{i:03d}", "registered") for i in range(1, 31)]
    issues.append(_issue("ISSUE-099", "in_progress"))
    section = intake.build_todo_projection(issues=issues, config=config)
    assert "ISSUE-099" in section
    assert len(section.encode("utf-8")) <= config["todo_projection"]["maximum_section_bytes"]
    entries = [line for line in section.splitlines() if line.startswith("- ")]
    assert len(entries) <= config["todo_projection"]["maximum_entries"]
    assert intake.validate_todo_projection(section=section, config=config) is True


def test_i9_previous_versions_still_validate(intake):
    pilot = importlib.import_module("tools.development.issue_resolution_pilot")
    for path in (CONFIG_V2, CONFIG_V3):
        legacy = pilot.load_config(path)
        assert legacy["maximum_issue_subjects"] == 1
    existing = json.loads(EXISTING_ISSUE.read_text(encoding="utf-8"))
    assert existing["schema_version"] == 1
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_issue_record(existing, config=intake.load_config(CONFIG_V4))
    assert error.value.code == "issue_schema_version_unsupported"


# ------------------------------------------------------------------ 負例 J1〜J16


def test_j1_completed_claim_heading_is_excluded(intake, config):
    with pytest.raises(intake.IntakeError) as error:
        intake.build_intake_candidate(
            config=config, heading_path=["実施報告照合", "verified"],
            quotation="- Claim `EC-019`：固定fixtureへ固定した。",
            source_path=SNAPSHOT, sha256=SNAPSHOT_SHA, start_line=63, end_line=63,
        )
    assert error.value.code == "intake_rule_excluded"
    assert "X1" in error.value.detail


def test_j2_evidence_only_line_is_excluded(intake, config):
    with pytest.raises(intake.IntakeError) as error:
        intake.build_intake_candidate(
            config=config, heading_path=["実施報告照合", "未実施"],
            quotation="  - Evidence：`tests/test_session_log_bootstrap.py`",
            source_path=SNAPSHOT, sha256=SNAPSHOT_SHA, start_line=66, end_line=66,
        )
    assert error.value.code == "intake_rule_excluded"
    assert "X2" in error.value.detail


def test_j3_resolved_history_line_is_excluded(intake, config):
    with pytest.raises(intake.IntakeError) as error:
        intake.build_intake_candidate(
            config=config, heading_path=["実施報告照合", "手戻り・機械化候補"],
            quotation="- 既知候補：routeは恒久対策commit `f9adef4`で実装済み。",
            source_path=SNAPSHOT, sha256=SNAPSHOT_SHA, start_line=735, end_line=735,
        )
    assert error.value.code == "intake_rule_excluded"
    assert "X3" in error.value.detail


def test_j4_source_digest_mismatch_stops(intake, config):
    with pytest.raises(intake.IntakeError) as error:
        intake.extract_intake_candidates(
            project_root=PROJECT_ROOT, config=config,
            source_path=SNAPSHOT, expected_sha256="0" * 64,
        )
    assert error.value.code == "intake_source_digest_mismatch"


def test_j5_duplicate_without_suspect_flag_is_rejected(intake, config):
    existing = json.loads(EXISTING_ISSUE.read_text(encoding="utf-8"))
    candidate = intake.build_intake_candidate(
        config=config, heading_path=["実施報告照合", "未実施"],
        quotation="- " + existing["problem"][:60],
        source_path=SNAPSHOT, sha256=SNAPSHOT_SHA, start_line=800, end_line=800,
    )
    candidate["duplicate_suspect"] = {
        "suspected": False, "matched_record_ids": [], "basis": "未判定",
    }
    with pytest.raises(intake.IntakeError) as error:
        intake.register_intake_candidate(
            candidate=candidate, existing_records=[existing], config=config
        )
    assert error.value.code == "duplicate_suspect_not_flagged"


def test_j6_promotion_without_human_ruling_is_rejected(intake, config):
    candidate = intake.build_intake_candidate(
        config=config, heading_path=["実施報告照合", "未実施"],
        quotation="- Project Bindingのdurable保存",
        source_path=SNAPSHOT, sha256=SNAPSHOT_SHA, start_line=803, end_line=803,
    )
    assert candidate["human_fields"]["promote_to_issue"] is None
    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_to_issue(candidate=candidate, config=config)
    assert error.value.code == "human_ruling_required"


def test_j7_second_in_progress_is_rejected(intake, config):
    issues = [_issue("ISSUE-001", "in_progress"), _issue("ISSUE-002", "registered")]
    with pytest.raises(intake.IntakeError) as error:
        intake.start_issue(issues=issues, issue_id="ISSUE-002", config=config)
    assert error.value.code == "active_issue_limit_exceeded"


def test_j8_second_active_leaf_is_rejected(intake, config):
    state = intake.new_work_state()
    intake.start_work_item(work_state=state, work_item_id="WI-001", config=config)
    with pytest.raises(intake.IntakeError) as error:
        intake.start_work_item(work_state=state, work_item_id="WI-002", config=config)
    assert error.value.code == "active_leaf_limit_exceeded"


def test_j9_registration_cannot_suspend_current(intake, config):
    issues = [_issue("ISSUE-001", "in_progress")]
    with pytest.raises(intake.IntakeError) as error:
        intake.register_issue(
            issues=issues, issue=_issue("ISSUE-002", "registered"),
            config=config, suspend_issue_ids=["ISSUE-001"],
        )
    assert error.value.code == "suspend_requires_blocks_and_ruling"
    assert issues[0]["state"] == "in_progress"


def test_j10_self_cycle_is_rejected_and_not_persisted(intake, config):
    issues = [_issue("ISSUE-001", "in_progress")]
    relations, updated, candidate = intake.propose_blocks(
        relations=[], issues=issues,
        blocker_issue_id="ISSUE-001", blocked_issue_id="ISSUE-001", config=config,
    )
    assert relations == []
    assert candidate is not None
    assert candidate["detection_reason"] == "blocks_cycle_detected"
    assert intake.count_active_issues(updated) == 0


def test_j11_two_issue_cycle_is_rejected_and_suspends_all(intake, config):
    issues = [_issue("ISSUE-001", "in_progress"), _issue("ISSUE-002", "registered")]
    relations, issues = intake.declare_blocks(
        relations=[], issues=issues,
        blocker_issue_id="ISSUE-001", blocked_issue_id="ISSUE-002",
        human_ruling=None, config=config,
    )
    assert len(relations) == 1
    persisted, updated, candidate = intake.propose_blocks(
        relations=relations, issues=issues,
        blocker_issue_id="ISSUE-002", blocked_issue_id="ISSUE-001", config=config,
    )
    assert persisted == relations
    assert len(persisted) == 1
    assert candidate is not None
    assert sorted(candidate["affected_issue_ids"]) == ["ISSUE-001", "ISSUE-002"]
    assert intake.count_active_issues(updated) == 0
    assert all(item["state"] == "suspended" for item in updated)


def test_j12_candidate_missing_required_evidence_is_rejected(intake, config):
    required = (
        "proposed_blocker_issue_id", "proposed_blocked_issue_id", "cycle_path_issue_ids",
        "cycle_path_relation_ids", "affected_issue_ids", "detection_reason",
        "input_digest", "content_digest",
    )
    issues = [_issue("ISSUE-001", "in_progress"), _issue("ISSUE-002", "registered")]
    relations, issues = intake.declare_blocks(
        relations=[], issues=issues, blocker_issue_id="ISSUE-001",
        blocked_issue_id="ISSUE-002", human_ruling=None, config=config,
    )
    _persisted, _updated, candidate = intake.propose_blocks(
        relations=relations, issues=issues,
        blocker_issue_id="ISSUE-002", blocked_issue_id="ISSUE-001", config=config,
    )
    for field in required:
        assert field in candidate
        broken = {k: v for k, v in candidate.items() if k != field}
        with pytest.raises(intake.IntakeError) as error:
            intake.validate_root_cause_candidate(broken, config=config)
        assert error.value.code == "root_cause_candidate_incomplete"


def test_j13_partial_write_is_rejected(intake, config):
    issues = [_issue("ISSUE-001", "in_progress"), _issue("ISSUE-002", "registered")]
    relations, issues = intake.declare_blocks(
        relations=[], issues=issues, blocker_issue_id="ISSUE-001",
        blocked_issue_id="ISSUE-002", human_ruling=None, config=config,
    )
    with pytest.raises(intake.IntakeError) as error:
        intake.propose_blocks(
            relations=relations, issues=issues,
            blocker_issue_id="ISSUE-002", blocked_issue_id="ISSUE-001",
            config=config, simulate_partial_write=True,
        )
    assert error.value.code == "cycle_detection_partial_write"
    assert {item["issue_id"]: item["state"] for item in issues}["ISSUE-001"] == "in_progress"


def test_j14_candidate_alone_grants_no_authority(intake, config):
    issues = [_issue("ISSUE-001", "suspended"), _issue("ISSUE-002", "suspended")]
    relations, issues = intake.declare_blocks(
        relations=[], issues=[_issue("ISSUE-001", "in_progress"),
                              _issue("ISSUE-002", "registered")],
        blocker_issue_id="ISSUE-001", blocked_issue_id="ISSUE-002",
        human_ruling=None, config=config,
    )
    _persisted, updated, candidate = intake.propose_blocks(
        relations=relations, issues=issues,
        blocker_issue_id="ISSUE-002", blocked_issue_id="ISSUE-001", config=config,
    )
    for action in ("create_issue", "create_plan", "start_work", "resume_issue"):
        with pytest.raises(intake.IntakeError) as error:
            intake.authorize_from_root_cause_candidate(
                candidate=candidate, action=action, human_ruling=None, config=config
            )
        assert error.value.code == "human_ruling_required"


def test_j15_resume_within_cycle_requires_resolution_or_ruling(intake, config):
    issues = [_issue("ISSUE-001", "suspended"), _issue("ISSUE-002", "suspended")]
    relations = [
        {"relation_id": "REL-001", "blocker_issue_id": "ISSUE-002",
         "blocked_issue_id": "ISSUE-001"}
    ]
    with pytest.raises(intake.IntakeError) as error:
        intake.resume_issue(
            issues=issues, relations=relations, issue_id="ISSUE-001", config=config
        )
    assert error.value.code == "resume_requires_resolution_or_ruling"


def test_j16_forbidden_todo_marker_is_rejected(intake, config):
    section = (
        config["todo_projection"]["heading"]
        + "\n\n- `ISSUE-099`：in_progress\n- problem: 詳細を書いてしまった\n"
    )
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_todo_projection(section=section, config=config)
    assert error.value.code == "todo_forbidden_marker"


# ------------------------------------------- V4 Human triage永続化 K1〜K7
#
# 指示：records/session-handoffs/2026-08-05-codex-to-claude-v4-human-triage-persistence.md
# 候補bundleは機械抽出時のimmutableな観測として保持し、Humanの判断正本は
# 一候補につき一件のhuman_triage_decision schema version 2とする。

BUNDLE = "records/development/2026-08-05-historical-todo-intake-candidates-v1.json"
BUNDLE_SHA = "e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e"
APPROVED_CANDIDATE_IDS = (
    "HTC-14D810C7",
    "HTC-1AB699F7",
    "HTC-21C3CE46",
    "HTC-6ABDDC35",
)
HISTORICAL_HUMAN_FIELDS = {
    "unresolved": False,
    "recurrence": False,
    "impact": "not_applicable",
    "priority": "not_applicable",
    "promote_to_issue": False,
}
DECIDED_AT = "2026-08-05T21:00:00+09:00"
V1_DECISION = (
    PROJECT_ROOT
    / ".reviewcompass/workflow/triage-decisions/dec-pilot-todo-growth-001--v1.json"
)


@pytest.fixture
def bundle():
    return json.loads((PROJECT_ROOT / BUNDLE).read_text(encoding="utf-8"))


def _bundle_candidate(bundle_document, candidate_id):
    for item in bundle_document["candidates"]:
        if item["candidate_id"] == candidate_id:
            return item
    raise AssertionError(f"{candidate_id} is absent from the bundle")


def _historical_decision(intake, config, candidate_id, **overrides):
    parameters = {
        "project_root": PROJECT_ROOT,
        "bundle_path": BUNDLE,
        "candidate_id": candidate_id,
        "decided_at": DECIDED_AT,
        "human_fields": dict(HISTORICAL_HUMAN_FIELDS),
        "disposition": "historical_completed",
        "blocking": False,
        "rationale": "当時の完了済み手順であり、現在解くIssueではない。",
        "next_action": "候補bundleを変更せず、この判断recordだけを保持する。",
        "config": config,
    }
    parameters.update(overrides)
    return intake.build_human_triage_decision(**parameters)


def _rehashed(intake, decision, **changes):
    updated = dict(decision)
    updated.update(changes)
    updated["content_digest"] = intake.canonical_digest(updated)
    return updated


def test_k1_decision_references_bundle_candidate_by_fingerprint(intake, config, bundle):
    decision = _historical_decision(intake, config, "HTC-14D810C7")
    candidate = _bundle_candidate(bundle, "HTC-14D810C7")

    assert decision["record_kind"] == "human_triage_decision"
    assert decision["schema_version"] == 2
    assert decision["decision_maker"] == "human"
    assert decision["decision_version"] == 1
    assert decision["supersedes"] is None
    assert decision["candidate_ref"] == {
        "bundle_path": BUNDLE,
        "bundle_sha256": BUNDLE_SHA,
        "bundle_schema_version": bundle["schema_version"],
        "candidate_id": "HTC-14D810C7",
        "candidate_content_digest": candidate["content_digest"],
    }
    assert decision["human_fields"] == HISTORICAL_HUMAN_FIELDS
    assert decision["issue_promotion"] == {"approved": False, "issue_id": None}

    path = intake.human_triage_decision_path(decision, config=config)
    assert path == (
        config["directories"]["human_triage_decision_v2"]
        + "/dec-htc-14d810c7--v1.json"
    )
    assert (
        intake.validate_human_triage_decision(
            decision, path=path, project_root=PROJECT_ROOT, config=config
        )
        is True
    )


def test_k2_broken_candidate_references_are_rejected(intake, config, bundle):
    decision = _historical_decision(intake, config, "HTC-14D810C7")
    path = intake.human_triage_decision_path(decision, config=config)

    def _reject(record, record_path=None):
        with pytest.raises(intake.IntakeError) as error:
            intake.validate_human_triage_decision(
                record,
                path=record_path or path,
                project_root=PROJECT_ROOT,
                config=config,
            )
        return error.value.code

    stale_bundle = _rehashed(
        intake,
        decision,
        candidate_ref=dict(decision["candidate_ref"], bundle_sha256="0" * 64),
    )
    assert _reject(stale_bundle) == "candidate_bundle_digest_mismatch"

    unknown_candidate = _rehashed(
        intake,
        decision,
        decision_id="DEC-HTC-00000000",
        candidate_ref=dict(decision["candidate_ref"], candidate_id="HTC-00000000"),
    )
    assert _reject(
        unknown_candidate,
        config["directories"]["human_triage_decision_v2"]
        + "/dec-htc-00000000--v1.json",
    ) == "candidate_not_found"

    stale_candidate = _rehashed(
        intake,
        decision,
        candidate_ref=dict(decision["candidate_ref"], candidate_content_digest="0" * 64),
    )
    assert _reject(stale_candidate) == "candidate_digest_mismatch"

    wrong_bundle_schema = _rehashed(
        intake,
        decision,
        candidate_ref=dict(decision["candidate_ref"], bundle_schema_version=99),
    )
    assert _reject(wrong_bundle_schema) == "candidate_bundle_schema_version_mismatch"

    unknown_field = _rehashed(intake, decision, reviewer="claude")
    assert _reject(unknown_field) == "human_triage_decision_field_unknown"

    for escape in ("../../etc/passwd", "/etc/passwd", "records/../../outside.json"):
        traversal = _rehashed(
            intake,
            decision,
            candidate_ref=dict(decision["candidate_ref"], bundle_path=escape),
        )
        assert _reject(traversal) == "human_triage_decision_path_invalid"

    wrong_path = _rehashed(intake, decision)
    assert _reject(
        wrong_path,
        config["directories"]["human_triage_decision_v2"] + "/dec-other--v1.json",
    ) == "human_triage_decision_path_mismatch"

    unknown_disposition = _rehashed(intake, decision, disposition="unknown_route")
    assert _reject(unknown_disposition) == "human_triage_decision_disposition_invalid"

    broken_digest = dict(decision, content_digest="0" * 64)
    assert _reject(broken_digest) == "human_triage_decision_digest_mismatch"

    old_schema = json.loads(V1_DECISION.read_text(encoding="utf-8"))
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_human_triage_decision(
            old_schema,
            path=".reviewcompass/workflow/triage-decisions/"
            "dec-pilot-todo-growth-001--v1.json",
            project_root=PROJECT_ROOT,
            config=config,
        )
    assert error.value.code == "human_triage_decision_schema_version_unsupported"


def test_k3_conflicting_decisions_are_rejected_and_revisions_are_allowed(
    intake, config
):
    first = _historical_decision(intake, config, "HTC-1AB699F7")
    rival = _historical_decision(
        intake,
        config,
        "HTC-1AB699F7",
        decision_suffix="ALT",
        human_fields=dict(HISTORICAL_HUMAN_FIELDS, unresolved=True),
        disposition="defer",
    )
    assert rival["decision_id"] == "DEC-HTC-1AB699F7-ALT"
    assert rival["supersedes"] is None

    with pytest.raises(intake.IntakeError) as error:
        intake.resolve_effective_triage_decisions([first, rival])
    assert error.value.code == "human_triage_decision_conflict"

    revision = _historical_decision(
        intake,
        config,
        "HTC-1AB699F7",
        decision_version=2,
        supersedes=first,
        human_fields=dict(HISTORICAL_HUMAN_FIELDS, unresolved=True),
        disposition="defer",
    )
    assert revision["supersedes"] == {
        "decision_id": first["decision_id"],
        "decision_version": 1,
        "content_digest": first["content_digest"],
    }
    effective = intake.resolve_effective_triage_decisions([first, revision])
    assert effective["HTC-1AB699F7"]["decision_version"] == 2
    assert intake.validate_human_triage_decision(
        revision,
        path=intake.human_triage_decision_path(revision, config=config),
        project_root=PROJECT_ROOT,
        config=config,
    ) is True

    stale_supersedes = _rehashed(
        intake,
        revision,
        supersedes=dict(revision["supersedes"], content_digest="0" * 64),
    )
    with pytest.raises(intake.IntakeError) as error:
        intake.resolve_effective_triage_decisions([first, stale_supersedes])
    assert error.value.code == "human_triage_decision_conflict"


def test_k4_promotion_requires_a_matching_human_decision(intake, config, bundle):
    candidate = _bundle_candidate(bundle, "HTC-14D810C7")
    rejecting = _historical_decision(intake, config, "HTC-14D810C7")

    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=candidate, decision=None,
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "human_triage_decision_required"

    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=candidate, decision=rejecting,
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "human_triage_decision_required"

    wrong_disposition = _historical_decision(
        intake,
        config,
        "HTC-14D810C7",
        human_fields=dict(HISTORICAL_HUMAN_FIELDS, promote_to_issue=True),
        disposition="defer",
    )
    assert wrong_disposition["issue_promotion"] == {"approved": False, "issue_id": None}
    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=candidate, decision=wrong_disposition,
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "human_triage_decision_required"

    approving = _historical_decision(
        intake,
        config,
        "HTC-14D810C7",
        human_fields=dict(HISTORICAL_HUMAN_FIELDS, promote_to_issue=True),
        disposition="issue_resolution",
        issue_id="ISSUE-HTC-14D810C7",
    )
    assert approving["issue_promotion"] == {
        "approved": True, "issue_id": "ISSUE-HTC-14D810C7",
    }

    other_candidate = _bundle_candidate(bundle, "HTC-1AB699F7")
    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=other_candidate, decision=approving,
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "candidate_not_found"

    detached = dict(candidate, content_digest="0" * 64)
    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=detached, decision=approving,
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "candidate_digest_mismatch"

    rival = _historical_decision(
        intake, config, "HTC-14D810C7", decision_suffix="ALT",
    )
    with pytest.raises(intake.IntakeError) as error:
        intake.promote_candidate_from_decision(
            candidate=candidate, decision=approving, decisions=[approving, rival],
            project_root=PROJECT_ROOT, config=config,
        )
    assert error.value.code == "human_triage_decision_conflict"

    issue = intake.promote_candidate_from_decision(
        candidate=candidate, decision=approving, decisions=[approving],
        project_root=PROJECT_ROOT, config=config,
    )
    assert issue["issue_id"] == "ISSUE-HTC-14D810C7"
    assert issue["state"] == "registered"
    assert issue["triage_decision_ref"]["decision_id"] == approving["decision_id"]
    assert intake.validate_issue_record(issue, config=config) is True
    assert candidate["human_fields"] == {
        "unresolved": None, "recurrence": None, "impact": None,
        "priority": None, "promote_to_issue": None,
    }


def test_k5_four_approved_decisions_validate_without_touching_the_bundle(
    intake, config, bundle
):
    before = (PROJECT_ROOT / BUNDLE).read_bytes()
    directory = PROJECT_ROOT / config["directories"]["human_triage_decision_v2"]

    for candidate_id in APPROVED_CANDIDATE_IDS:
        decision = _historical_decision(intake, config, candidate_id)
        path = intake.human_triage_decision_path(decision, config=config)
        assert decision["human_fields"] == HISTORICAL_HUMAN_FIELDS
        assert decision["disposition"] == "historical_completed"
        assert decision["blocking"] is False
        assert decision["issue_promotion"] == {"approved": False, "issue_id": None}
        assert intake.validate_human_triage_decision(
            decision, path=path, project_root=PROJECT_ROOT, config=config
        ) is True

        stored_path = directory / f"dec-{candidate_id.lower()}--v1.json"
        if stored_path.is_file():
            stored = json.loads(stored_path.read_text(encoding="utf-8"))
            assert intake.validate_human_triage_decision(
                stored,
                path=intake.human_triage_decision_path(stored, config=config),
                project_root=PROJECT_ROOT,
                config=config,
            ) is True
            expected = _historical_decision(
                intake, config, candidate_id,
                decided_at=stored["decided_at"],
                rationale=stored["rationale"],
                next_action=stored["next_action"],
            )
            assert stored == expected
            assert "6b68c25" in stored["rationale"]
            assert "b10cd09" in stored["rationale"]
            assert "416e4e1" in stored["rationale"]

    assert (PROJECT_ROOT / BUNDLE).read_bytes() == before
    assert hashlib.sha256(before).hexdigest() == BUNDLE_SHA
    for candidate in bundle["candidates"]:
        assert candidate["human_fields"] == {
            "unresolved": None, "recurrence": None, "impact": None,
            "priority": None, "promote_to_issue": None,
        }


def test_k6_legacy_v1_decision_and_pilot_validation_keep_passing(intake, config):
    pilot = importlib.import_module("tools.development.issue_resolution_pilot")
    legacy_config = pilot.load_config(CONFIG_V2)
    result = pilot.validate_record_file(
        V1_DECISION, project_root=PROJECT_ROOT, config=legacy_config
    )
    assert result.record_id == "DEC-PILOT-TODO-GROWTH-001"

    legacy = json.loads(V1_DECISION.read_text(encoding="utf-8"))
    assert legacy["schema_version"] == 1
    assert legacy["issue_promotion"]["approved"] is True

    v1_directory = PROJECT_ROOT / config["directories"]["human_triage_decision"]
    v4_directory = PROJECT_ROOT / config["directories"]["human_triage_decision_v2"]
    assert v1_directory != v4_directory
    assert sorted(path.name for path in v1_directory.glob("*.json")) == [
        "dec-pilot-todo-growth-001--v1.json"
    ]


def test_k7_repository_decision_set_has_no_conflict(intake, config):
    effective = intake.validate_triage_decision_repository(
        project_root=PROJECT_ROOT, config=config
    )
    assert isinstance(effective, dict)
    for candidate_id, decision in effective.items():
        assert decision["candidate_ref"]["candidate_id"] == candidate_id
        assert decision["candidate_ref"]["bundle_sha256"] == BUNDLE_SHA
        assert decision["decision_maker"] == "human"

    stored = sorted(
        (PROJECT_ROOT / config["directories"]["human_triage_decision_v2"]).glob(
            "*.json"
        )
    )
    assert len(effective) == len({
        json.loads(path.read_text(encoding="utf-8"))["candidate_ref"]["candidate_id"]
        for path in stored
    })


# ---------------------------------------------- V4 Issue永続化 L1〜L6
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-v4-issue-persistence-and-session-policy-triage.md
# 旧PilotのIssue directoryは「Pilot subjectが1件」の検査を持つため、V4 Issueは
# V4専用directoryへ永続保存する。旧IssueをV4語彙で再判定しない。

SESSION_POLICY_CANDIDATE = "HTC-BEB5E0BD"
SESSION_POLICY_ISSUE_ID = "ISSUE-HTC-BEB5E0BD"
SESSION_POLICY_PROBLEM = (
    "生会話記録の保存期間、削除、application-layer暗号化、backupの方針が未決定である。"
)
CREATED_AT = "2026-08-05T22:00:00+09:00"
LEGACY_ISSUE_DIRECTORY = ".reviewcompass/workflow/issues"


def _write_json(root, relative, document):
    path = Path(root) / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


@pytest.fixture
def workspace(tmp_path, config):
    """候補bundleだけを写した作業用project rootを作る。実repositoryは触らない。"""

    root = tmp_path / "project"
    (root / BUNDLE).parent.mkdir(parents=True)
    shutil.copy2(PROJECT_ROOT / BUNDLE, root / BUNDLE)
    for key in ("human_triage_decision_v2", "issue_record_v2"):
        (root / config["directories"][key]).mkdir(parents=True)
    return root


def _approving_decision(intake, config, root, **overrides):
    parameters = {
        "project_root": root,
        "bundle_path": BUNDLE,
        "candidate_id": SESSION_POLICY_CANDIDATE,
        "decided_at": DECIDED_AT,
        "human_fields": {
            "unresolved": True,
            "recurrence": True,
            "impact": "high",
            "priority": "high",
            "promote_to_issue": True,
        },
        "disposition": "issue_resolution",
        "blocking": False,
        "rationale": "生会話記録の保存方針が未決定であり、正式Issueとして追跡する。",
        "next_action": "Plan化するかどうかをHumanが判断する。",
        "issue_id": SESSION_POLICY_ISSUE_ID,
        "config": config,
    }
    parameters.update(overrides)
    decision = intake.build_human_triage_decision(**parameters)
    _write_json(
        root, intake.human_triage_decision_path(decision, config=config), decision
    )
    return decision


def test_l1_issue_is_persisted_and_reloaded_with_deterministic_path_and_digest(
    intake, config, workspace
):
    before = (workspace / BUNDLE).read_bytes()
    decision = _approving_decision(intake, config, workspace)
    candidate = _bundle_candidate(
        json.loads((workspace / BUNDLE).read_text(encoding="utf-8")),
        SESSION_POLICY_CANDIDATE,
    )

    issue = intake.build_v4_issue_record(
        candidate=candidate, decision=decision, project_root=workspace,
        config=config, created_at=CREATED_AT, problem=SESSION_POLICY_PROBLEM,
        decisions=[decision],
    )
    assert issue["record_kind"] == "issue_record"
    assert issue["schema_version"] == 2
    assert issue["issue_id"] == SESSION_POLICY_ISSUE_ID
    assert issue["issue_version"] == 1
    assert issue["state"] == "registered"
    assert issue["problem"] == SESSION_POLICY_PROBLEM
    assert issue["candidate_ref"] == decision["candidate_ref"]
    assert issue["content_digest"] == intake.canonical_digest(issue)
    assert intake.count_active_issues([issue]) == 0

    path = intake.v4_issue_path(issue, config=config)
    assert path == (
        config["directories"]["issue_record_v2"] + "/issue-htc-beb5e0bd--v1.json"
    )
    stored = _write_json(workspace, path, issue)
    reloaded = json.loads(stored.read_text(encoding="utf-8"))
    assert reloaded == issue
    assert intake.validate_v4_issue_record(
        reloaded, path=path, project_root=workspace, config=config
    ) is True

    decision_reference = issue["triage_decision_ref"]
    decision_path = intake.human_triage_decision_path(decision, config=config)
    assert decision_reference == {
        "decision_id": decision["decision_id"],
        "decision_version": decision["decision_version"],
        "path": decision_path,
        "sha256": hashlib.sha256((workspace / decision_path).read_bytes()).hexdigest(),
        "content_digest": decision["content_digest"],
    }

    effective = intake.validate_v4_issue_repository(
        project_root=workspace, config=config
    )
    assert list(effective) == [SESSION_POLICY_CANDIDATE]
    assert effective[SESSION_POLICY_CANDIDATE]["issue_id"] == SESSION_POLICY_ISSUE_ID
    assert (workspace / BUNDLE).read_bytes() == before


def test_l2_v4_issue_directory_must_differ_from_the_legacy_one(
    intake, config, tmp_path
):
    assert config["directories"]["issue_record"] == LEGACY_ISSUE_DIRECTORY
    assert config["directories"]["issue_record_v2"] != LEGACY_ISSUE_DIRECTORY

    document = json.loads(CONFIG_V4.read_text(encoding="utf-8"))
    document["directories"]["issue_record_v2"] = document["directories"]["issue_record"]
    collided = tmp_path / "collided.json"
    collided.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(intake.IntakeError) as error:
        intake.load_config(collided)
    assert error.value.code == "config_invalid"

    missing = json.loads(CONFIG_V4.read_text(encoding="utf-8"))
    del missing["directories"]["issue_record_v2"]
    absent = tmp_path / "absent.json"
    absent.write_text(json.dumps(missing, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(intake.IntakeError) as error:
        intake.load_config(absent)
    assert error.value.code == "config_invalid"


def test_l3_tampered_references_are_rejected(intake, config, workspace):
    decision = _approving_decision(intake, config, workspace)
    candidate = _bundle_candidate(
        json.loads((workspace / BUNDLE).read_text(encoding="utf-8")),
        SESSION_POLICY_CANDIDATE,
    )
    issue = intake.build_v4_issue_record(
        candidate=candidate, decision=decision, project_root=workspace,
        config=config, created_at=CREATED_AT, problem=SESSION_POLICY_PROBLEM,
    )
    path = intake.v4_issue_path(issue, config=config)

    def _reject(record, record_path=None):
        with pytest.raises(intake.IntakeError) as error:
            intake.validate_v4_issue_record(
                record,
                path=record_path or path,
                project_root=workspace,
                config=config,
            )
        return error.value.code

    assert _reject(
        _rehashed(
            intake, issue,
            candidate_ref=dict(issue["candidate_ref"], bundle_sha256="0" * 64),
        )
    ) == "candidate_bundle_digest_mismatch"

    assert _reject(
        _rehashed(
            intake, issue,
            candidate_ref=dict(
                issue["candidate_ref"], candidate_content_digest="0" * 64
            ),
        )
    ) == "candidate_digest_mismatch"

    assert _reject(
        _rehashed(
            intake, issue,
            triage_decision_ref=dict(issue["triage_decision_ref"], sha256="0" * 64),
        )
    ) == "v4_issue_decision_reference_stale"

    assert _reject(
        _rehashed(
            intake, issue,
            triage_decision_ref=dict(
                issue["triage_decision_ref"], content_digest="0" * 64
            ),
        )
    ) == "v4_issue_decision_mismatch"

    for escape in ("../../etc/passwd", "/etc/passwd"):
        assert _reject(
            _rehashed(
                intake, issue,
                triage_decision_ref=dict(issue["triage_decision_ref"], path=escape),
            )
        ) == "v4_issue_path_invalid"

    assert _reject(
        _rehashed(
            intake, issue,
            triage_decision_ref=dict(
                issue["triage_decision_ref"],
                path=config["directories"]["human_triage_decision_v2"]
                + "/dec-htc-00000000--v1.json",
            ),
        )
    ) == "v4_issue_decision_reference_stale"

    assert _reject(_rehashed(intake, issue, reviewer="claude")) == "v4_issue_field_unknown"
    assert _reject(dict(issue, content_digest="0" * 64)) == "v4_issue_digest_mismatch"
    assert _reject(issue, path + ".other") == "v4_issue_path_mismatch"

    # decision fileを後から書き換えると、保存済みIssueの参照は成立しない。
    tampered = dict(decision, rationale=decision["rationale"] + "追記")
    tampered["content_digest"] = intake.canonical_digest(tampered)
    _write_json(
        workspace, intake.human_triage_decision_path(decision, config=config), tampered
    )
    assert _reject(issue) == "v4_issue_decision_reference_stale"


def test_l4_issue_creation_requires_an_approving_decision(intake, config, workspace):
    bundle_document = json.loads((workspace / BUNDLE).read_text(encoding="utf-8"))
    candidate = _bundle_candidate(bundle_document, SESSION_POLICY_CANDIDATE)

    def _refuse(**overrides):
        parameters = {
            "candidate": candidate, "project_root": workspace, "config": config,
            "created_at": CREATED_AT, "problem": SESSION_POLICY_PROBLEM,
        }
        parameters.update(overrides)
        with pytest.raises(intake.IntakeError) as error:
            intake.build_v4_issue_record(**parameters)
        return error.value.code

    assert _refuse(decision=None) == "human_triage_decision_required"

    rejecting = _approving_decision(
        intake, config, workspace,
        human_fields={
            "unresolved": True, "recurrence": True, "impact": "high",
            "priority": "high", "promote_to_issue": False,
        },
        disposition="dependency", issue_id=None, decision_suffix="NO",
    )
    assert _refuse(decision=rejecting) == "human_triage_decision_required"

    mismatched = _approving_decision(
        intake, config, workspace,
        human_fields={
            "unresolved": True, "recurrence": True, "impact": "high",
            "priority": "high", "promote_to_issue": True,
        },
        disposition="dependency", issue_id=None, decision_suffix="DEP",
    )
    assert _refuse(decision=mismatched) == "human_triage_decision_required"

    approving = _approving_decision(intake, config, workspace)
    issue = intake.build_v4_issue_record(
        candidate=candidate, decision=approving, project_root=workspace,
        config=config, created_at=CREATED_AT, problem=SESSION_POLICY_PROBLEM,
    )
    _write_json(workspace, intake.v4_issue_path(issue, config=config), issue)

    renamed = _rehashed(intake, issue, issue_id="ISSUE-HTC-BEB5E0BD-OTHER")
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_v4_issue_record(
            renamed,
            path=intake.v4_issue_path(renamed, config=config),
            project_root=workspace,
            config=config,
        )
    assert error.value.code == "v4_issue_decision_mismatch"

    revision = _approving_decision(
        intake, config, workspace,
        decision_version=2, supersedes=approving,
        issue_id="ISSUE-HTC-BEB5E0BD-B",
    )
    duplicate = intake.build_v4_issue_record(
        candidate=candidate, decision=revision, project_root=workspace,
        config=config, created_at=CREATED_AT, problem=SESSION_POLICY_PROBLEM,
    )
    _write_json(workspace, intake.v4_issue_path(duplicate, config=config), duplicate)
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_v4_issue_repository(project_root=workspace, config=config)
    assert error.value.code == "v4_issue_duplicate_for_candidate"


def test_l5_legacy_issue_directory_stays_single_and_unjudged_by_v4(intake, config):
    legacy_files = sorted((PROJECT_ROOT / LEGACY_ISSUE_DIRECTORY).glob("*.json"))
    assert [path.name for path in legacy_files] == [
        "issue-pilot-todo-growth-001--v1.json"
    ]
    legacy = json.loads(legacy_files[0].read_text(encoding="utf-8"))
    assert legacy["schema_version"] == 1

    with pytest.raises(intake.IntakeError) as error:
        intake.validate_v4_issue_record(
            legacy,
            path=f"{LEGACY_ISSUE_DIRECTORY}/{legacy_files[0].name}",
            project_root=PROJECT_ROOT,
            config=config,
        )
    assert error.value.code == "v4_issue_schema_version_unsupported"

    pilot = importlib.import_module("tools.development.issue_resolution_pilot")
    legacy_config = pilot.load_config(CONFIG_V2)
    assert pilot.validate_record_file(
        legacy_files[0], project_root=PROJECT_ROOT, config=legacy_config
    ).record_id == "ISSUE-PILOT-TODO-GROWTH-001"


def test_l6_repository_issue_set_is_consistent(intake, config):
    effective = intake.validate_v4_issue_repository(
        project_root=PROJECT_ROOT, config=config
    )
    assert isinstance(effective, dict)
    decisions = intake.validate_triage_decision_repository(
        project_root=PROJECT_ROOT, config=config
    )

    for candidate_id, issue in effective.items():
        assert issue["candidate_ref"]["candidate_id"] == candidate_id
        assert issue["candidate_ref"]["bundle_sha256"] == BUNDLE_SHA
        assert issue["state"] == "registered"
        decision = decisions[candidate_id]
        assert decision["issue_promotion"] == {
            "approved": True, "issue_id": issue["issue_id"],
        }
        assert decision["blocking"] is False
    assert intake.count_active_issues(list(effective.values())) == 0

    stored = sorted(
        (PROJECT_ROOT / config["directories"]["issue_record_v2"]).glob("*.json")
    )
    assert len(stored) == len(effective)
    if stored:
        assert list(effective) == [SESSION_POLICY_CANDIDATE]
        issue = effective[SESSION_POLICY_CANDIDATE]
        assert issue["issue_id"] == SESSION_POLICY_ISSUE_ID
        assert issue["problem"] == SESSION_POLICY_PROBLEM
