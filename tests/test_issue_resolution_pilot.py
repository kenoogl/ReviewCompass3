"""ReviewCompass Issue Resolution早期Pilot bootstrapのAcceptance Test。"""

import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config/development-issue-resolution-pilot.json"
TASK_CONTRACT_PATH = (
    PROJECT_ROOT
    / "records/task-contract/issue-resolution-early-pilot-v1.json"
)
CANDIDATE_PATH = (
    PROJECT_ROOT
    / ".reviewcompass/workflow/improvement-candidates"
    / "ic-pilot-todo-growth-001--v1.json"
)


def _module():
    return importlib.import_module(
        "tools.development.issue_resolution_pilot"
    )


def _canonical_digest(record):
    payload = {
        key: value
        for key, value in record.items()
        if key != "content_digest"
    }
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate(project_root):
    source_path = project_root / "records/development/observation-v1.json"
    _write_json(
        source_path,
        {
            "observation_id": "OBS-PILOT-TODO-GROWTH-001",
            "status": "fixed_pilot_source",
        },
    )
    relative_source = source_path.relative_to(project_root).as_posix()
    record = {
        "record_kind": "improvement_candidate",
        "schema_version": 1,
        "candidate_id": "IC-PILOT-TODO-GROWTH-001",
        "candidate_version": 1,
        "created_at": "2026-08-04T08:30:00+09:00",
        "source_work": "inter-work/issue-resolution-early-pilot",
        "source_identity": {
            "kind": "observation",
            "source_id": "OBS-PILOT-TODO-GROWTH-001",
            "source_version": 1,
            "path": relative_source,
            "sha256": _sha256(source_path),
        },
        "problem": "TODO contains accumulated historical claims.",
        "impact": ["current handoff is difficult to scan"],
        "scope": ["one development-only Pilot subject"],
        "non_scope": ["formal product Issue schema"],
        "classification_candidates": ["process_improvement"],
        "route_candidates": ["issue_resolution"],
        "consumer_candidates": ["reviewcompass3-development"],
        "evidence_refs": [
            {
                "path": relative_source,
                "sha256": _sha256(source_path),
            }
        ],
        "proposed_action": "Obtain a Human Triage Decision.",
        "content_digest": "",
    }
    record["content_digest"] = _canonical_digest(record)
    path = (
        ".reviewcompass/workflow/improvement-candidates/"
        "ic-pilot-todo-growth-001--v1.json"
    )
    return record, path


def _write_candidate(project_root, record, relative_path):
    path = project_root / relative_path
    _write_json(path, record)
    return path


def _decision(project_root, candidate, candidate_path, *, disposition):
    candidate_file = project_root / candidate_path
    promotion = disposition == "issue_resolution"
    record = {
        "record_kind": "human_triage_decision",
        "schema_version": 1,
        "decision_id": "DEC-PILOT-TODO-GROWTH-001",
        "decision_version": 1,
        "decided_at": "2026-08-04T08:35:00+09:00",
        "decision_maker": "human",
        "candidate_ref": {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["candidate_version"],
            "path": candidate_path,
            "sha256": _sha256(candidate_file),
            "content_digest": candidate["content_digest"],
        },
        "disposition": disposition,
        "blocking": False,
        "rationale": "The Pilot subject requires durable independent tracking.",
        "selected_consumer": "reviewcompass3-development",
        "next_action": "Create the one approved Issue Record.",
        "issue_promotion": {
            "approved": promotion,
            "issue_id": "ISSUE-PILOT-TODO-GROWTH-001" if promotion else None,
        },
        "content_digest": "",
    }
    record["content_digest"] = _canonical_digest(record)
    path = (
        ".reviewcompass/workflow/triage-decisions/"
        "dec-pilot-todo-growth-001--v1.json"
    )
    return record, path


def test_repository_config_and_task_contract_fix_the_limited_pilot():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)

    assert config["pilot_mode"] == "development_only_provisional"
    assert config["maximum_issue_subjects"] == 1
    assert config["directories"] == {
        "improvement_candidate": (
            ".reviewcompass/workflow/improvement-candidates"
        ),
        "human_triage_decision": (
            ".reviewcompass/workflow/triage-decisions"
        ),
    }
    assert pilot.validate_task_contract_sources(
        TASK_CONTRACT_PATH,
        project_root=PROJECT_ROOT,
    ) == 9
    for relative_path in config["directories"].values():
        assert (PROJECT_ROOT / relative_path).is_dir()


def test_repository_contains_only_the_single_valid_pilot_subject():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    candidate_files = sorted(CANDIDATE_PATH.parent.glob("*.json"))
    decision_files = sorted(
        (
            PROJECT_ROOT
            / config["directories"]["human_triage_decision"]
        ).glob("*.json")
    )

    assert candidate_files == [CANDIDATE_PATH]
    assert len(decision_files) <= 1
    result = pilot.validate_record_file(
        CANDIDATE_PATH,
        project_root=PROJECT_ROOT,
        config=config,
    )
    assert result.record_id == "IC-PILOT-TODO-GROWTH-001"
    for decision_file in decision_files:
        pilot.validate_record_file(
            decision_file,
            project_root=PROJECT_ROOT,
            config=config,
        )


def test_validates_candidate_identity_digest_path_and_fixed_sources(
    tmp_path,
):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record, path = _candidate(tmp_path)

    result = pilot.validate_candidate(
        record,
        path=path,
        project_root=tmp_path,
        config=config,
    )

    assert result.record_kind == "improvement_candidate"
    assert result.record_id == "IC-PILOT-TODO-GROWTH-001"
    assert result.content_digest == record["content_digest"]


@pytest.mark.parametrize(
    ("mutation", "path_change", "message"),
    [
        (lambda record: record.update(problem=""), None, "text field"),
        (
            lambda record: record.update(content_digest="0" * 64),
            None,
            "content digest",
        ),
        (
            lambda record: record["source_identity"].update(
                sha256="0" * 64
            ),
            None,
            "source reference",
        ),
        (
            lambda record: None,
            ".reviewcompass/workflow/issues/wrong.json",
            "record path",
        ),
    ],
)
def test_rejects_invalid_candidate(
    tmp_path,
    mutation,
    path_change,
    message,
):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    record, path = _candidate(tmp_path)
    mutation(record)

    with pytest.raises(pilot.PilotValidationError, match=message):
        pilot.validate_candidate(
            record,
            path=path_change or path,
            project_root=tmp_path,
            config=config,
        )


def test_validates_human_triage_and_issue_promotion_binding(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    candidate, candidate_path = _candidate(tmp_path)
    _write_candidate(tmp_path, candidate, candidate_path)
    decision, decision_path = _decision(
        tmp_path,
        candidate,
        candidate_path,
        disposition="issue_resolution",
    )

    result = pilot.validate_triage_decision(
        decision,
        path=decision_path,
        project_root=tmp_path,
        config=config,
    )

    assert result.record_kind == "human_triage_decision"
    assert result.record_id == "DEC-PILOT-TODO-GROWTH-001"
    assert result.content_digest == decision["content_digest"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda record: record.update(decision_maker="machine"),
            "Human decision",
        ),
        (
            lambda record: record["issue_promotion"].update(
                approved=False,
                issue_id=None,
            ),
            "Issue promotion",
        ),
        (
            lambda record: record["candidate_ref"].update(
                sha256="0" * 64
            ),
            "candidate reference",
        ),
    ],
)
def test_rejects_non_human_or_stale_issue_promotion(
    tmp_path,
    mutation,
    message,
):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    candidate, candidate_path = _candidate(tmp_path)
    _write_candidate(tmp_path, candidate, candidate_path)
    decision, decision_path = _decision(
        tmp_path,
        candidate,
        candidate_path,
        disposition="issue_resolution",
    )
    mutation(decision)
    decision["content_digest"] = _canonical_digest(decision)

    with pytest.raises(pilot.PilotValidationError, match=message):
        pilot.validate_triage_decision(
            decision,
            path=decision_path,
            project_root=tmp_path,
            config=config,
        )


def test_allows_non_issue_disposition_without_issue_identity(tmp_path):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    candidate, candidate_path = _candidate(tmp_path)
    _write_candidate(tmp_path, candidate, candidate_path)
    decision, decision_path = _decision(
        tmp_path,
        candidate,
        candidate_path,
        disposition="checkpoint",
    )

    result = pilot.validate_triage_decision(
        decision,
        path=decision_path,
        project_root=tmp_path,
        config=config,
    )

    assert result.record_kind == "human_triage_decision"


def test_todo_projection_accepts_only_active_known_ids():
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)
    document = """# TODO_NEXT_SESSION

## 現在作業に影響する改善候補／Issue

- `IC-PILOT-TODO-GROWTH-001`：`triage_pending`、影響：現行handoff、次：Human Triage

## 次に行う一作業
"""

    result = pilot.validate_todo_projection(
        document,
        known_ids={"IC-PILOT-TODO-GROWTH-001"},
        config=config,
    )

    assert result == ("IC-PILOT-TODO-GROWTH-001",)


@pytest.mark.parametrize(
    ("document", "message"),
    [
        (
            """# TODO_NEXT_SESSION

## 現在作業に影響する改善候補／Issue

- `IC-UNKNOWN-001`：`open`、影響：handoff、次：triage
""",
            "unknown active ID",
        ),
        (
            """# TODO_NEXT_SESSION

### 手戻り・機械化候補

- 期待executor、実executor、Evidence、詳細な履歴

## 現在作業に影響する改善候補／Issue

- なし
""",
            "detailed rework history",
        ),
        (
            """# TODO_NEXT_SESSION

## 現在作業に影響する改善候補／Issue

- `IC-PILOT-TODO-GROWTH-001`：problem: full candidate text
""",
            "active ID projection",
        ),
    ],
)
def test_todo_projection_rejects_unknown_or_detailed_history(
    document,
    message,
):
    pilot = _module()
    config = pilot.load_config(CONFIG_PATH)

    with pytest.raises(pilot.PilotValidationError, match=message):
        pilot.validate_todo_projection(
            document,
            known_ids={"IC-PILOT-TODO-GROWTH-001"},
            config=config,
        )
