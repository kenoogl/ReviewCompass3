"""Work 1B Session Log Bootstrapの受入テスト。"""

import hashlib
import importlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
FIXTURE_ROOT = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "development"
    / "session-log-bootstrap"
)
BASELINE_RECORD = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-03-layout-baseline-v1.json"
)


def _bootstrap():
    return importlib.import_module(
        "tools.development.session_log_bootstrap"
    )


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path):
    return tuple(
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    )


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _layout_resolution(tmp_path):
    layout = importlib.import_module("tools.layout.baseline")
    baseline = layout.load_layout_baseline(BASELINE_RECORD)
    project = tmp_path / "project"
    project.mkdir()
    defaults = {
        name: tmp_path / "external" / name
        for name in (
            "code_root",
            "config_root",
            "data_root",
            "state_root",
            "log_root",
            "cache_root",
            "sensitive_root",
            "evaluation_root",
        )
    }
    return layout.resolve_layout(
        baseline,
        environment_role="development",
        project_root=project,
        defaults=defaults,
    )


def test_capture_profile_records_identity_range_policy_and_separated_roots(
    tmp_path,
):
    bootstrap = _bootstrap()
    profile = _json(FIXTURE_ROOT / "capture-profile.json")
    raw_bytes = (FIXTURE_ROOT / "raw" / "session.jsonl").read_bytes()
    resolution = _layout_resolution(tmp_path)

    plan = bootstrap.plan_session_capture(
        profile,
        raw_bytes=raw_bytes,
        layout=resolution,
    )

    assert plan.session_id == "session-work1b-fixture"
    assert plan.source_identity == "codex-thread:fixture-001"
    assert plan.event_range == ("evt-001", "evt-003", 3)
    assert plan.raw_path == (
        resolution.roots["sensitive_root"]
        / "sessions"
        / "session-work1b-fixture"
        / "raw"
        / "session.jsonl"
    )
    assert plan.derived_paths == {
        "index": (
            resolution.roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "index.json"
        ),
        "summary": (
            resolution.roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "summary.json"
        ),
        "transcript": (
            resolution.roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "transcript.md"
        ),
    }
    assert plan.confidentiality == "restricted"
    assert plan.access == (
        "authorized_human",
        "session_capture_runtime",
    )
    assert plan.retention == {
        "derived": "project_policy",
        "raw": "30_days",
    }
    assert plan.capture_deadline == "2026-08-03T09:05:00+09:00"
    assert plan.completeness == "complete"
    assert plan.mutation == "append_only"
    assert plan.source_availability == "available"


def test_source_availability_distinguishes_normal_empty_from_failures():
    bootstrap = _bootstrap()
    cases = _json(FIXTURE_ROOT / "source-availability-cases.json")

    actual = [
        bootstrap.assess_source_availability(case["observation"])
        for case in cases
    ]

    assert actual == [case["expected"] for case in cases]
    assert {item["status"] for item in actual} == {
        "available",
        "source_missing",
        "source_expired",
        "non_reconstructable",
    }


def test_restore_rebuilds_derived_artifacts_and_matches_fixed_digests():
    bootstrap = _bootstrap()
    profile = _json(FIXTURE_ROOT / "capture-profile.json")
    raw_bytes = (FIXTURE_ROOT / "raw" / "session.jsonl").read_bytes()
    expected = {
        name: (FIXTURE_ROOT / "expected" / filename).read_bytes()
        for name, filename in {
            "index": "index.json",
            "summary": "summary.json",
            "transcript": "transcript.md",
        }.items()
    }

    restored = bootstrap.restore_derived_artifacts(
        raw_bytes,
        profile=profile,
    )

    assert restored.artifacts == expected
    assert restored.digests == {
        name: _sha256(content)
        for name, content in expected.items()
    }
    assert restored.source_digest == _sha256(raw_bytes)
    assert restored.matches_profile is True


def test_projection_reduces_major_state_events_deterministically():
    bootstrap = _bootstrap()
    events = _jsonl(FIXTURE_ROOT / "workflow-events.jsonl")
    inputs = _json(FIXTURE_ROOT / "projection-inputs.json")
    expected = _json(FIXTURE_ROOT / "expected" / "projection.json")

    first = bootstrap.project_current_work(events, inputs=inputs)
    second = bootstrap.project_current_work(events, inputs=inputs)

    assert first == second == expected
    assert first["diagnostics"] == {
        "conflicts": [],
        "missing": [],
        "status": "complete",
    }
    assert first["blockers"] == []
    assert first["human_decisions"] == []
    assert first["stale"] == []
    assert first["deferred"] == [
        {"summary": "future UI", "work_id": "DEFERRED-UI"}
    ]
    assert first["canceled"] == [
        {
            "summary": "obsolete experiment",
            "work_id": "CANCELED-EXPERIMENT",
        }
    ]


def test_projection_renders_fixed_short_and_detailed_text():
    bootstrap = _bootstrap()
    projection = _json(FIXTURE_ROOT / "expected" / "projection.json")

    short = bootstrap.render_current_work(projection, mode="short")
    detailed = bootstrap.render_current_work(
        projection,
        mode="detailed",
    )

    assert short == (
        FIXTURE_ROOT / "expected" / "current-work-short.txt"
    ).read_text(encoding="utf-8")
    assert detailed == (
        FIXTURE_ROOT / "expected" / "current-work-detailed.txt"
    ).read_text(encoding="utf-8")


def test_projection_reports_missing_authority_without_guessing():
    bootstrap = _bootstrap()
    events = _jsonl(FIXTURE_ROOT / "workflow-events.jsonl")
    inputs = _json(FIXTURE_ROOT / "projection-incomplete-inputs.json")

    projection = bootstrap.project_current_work(events, inputs=inputs)

    assert projection["diagnostics"] == {
        "conflicts": [],
        "missing": [
            "fixed Plan identity and Digest",
            "workflow event stream identity and Digest",
        ],
        "status": "incomplete",
    }
    assert projection["next"] == "Repair missing projection inputs"
    detailed = bootstrap.render_current_work(
        projection,
        mode="detailed",
    )
    assert "STATUS: INCOMPLETE" in detailed
    assert "fixed Plan identity and Digest" in detailed


def test_projection_reports_conflicting_active_work_as_inconsistent():
    bootstrap = _bootstrap()
    events = _jsonl(
        FIXTURE_ROOT / "workflow-events-conflict.jsonl"
    )
    inputs = _json(FIXTURE_ROOT / "projection-inputs.json")

    projection = bootstrap.project_current_work(events, inputs=inputs)

    assert projection["diagnostics"] == {
        "conflicts": [
            "concurrent work_started events have different work_item_id"
        ],
        "missing": [],
        "status": "inconsistent",
    }
    assert projection["current_activity"] == {
        "contract_id": None,
        "tdd_state": "red",
        "work_item_id": None,
    }
    assert projection["next"] == "Resolve conflicting active work"
    detailed = bootstrap.render_current_work(
        projection,
        mode="detailed",
    )
    assert "STATUS: INCONSISTENT" in detailed
