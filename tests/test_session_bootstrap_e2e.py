"""Work 1B session開始／終了bootstrap E2Eの受入テスト。"""

import copy
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
    / "session-bootstrap-e2e"
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


def _e2e_inputs(tmp_path):
    return {
        "layout": _layout_resolution(tmp_path),
        "profile": _json(FIXTURE_ROOT / "capture-profile.json"),
        "projection_inputs": _json(
            FIXTURE_ROOT / "projection-inputs.json"
        ),
        "raw_bytes": (FIXTURE_ROOT / "raw" / "session.jsonl").read_bytes(),
    }


def test_captures_session_lifecycle_and_renders_current_work_e2e(tmp_path):
    bootstrap = _bootstrap()
    inputs = _e2e_inputs(tmp_path)

    result = bootstrap.run_session_bootstrap(**inputs)

    assert result.session_lifecycle == {
        "ended": True,
        "event_count": 3,
        "started": True,
    }
    assert result.capture.raw_path.read_bytes() == inputs["raw_bytes"]
    assert result.capture.evidence_path.read_bytes() == (
        FIXTURE_ROOT / "expected" / "session-evidence.json"
    ).read_bytes()
    assert result.projection == _json(
        FIXTURE_ROOT / "expected" / "projection.json"
    )
    assert result.short_text == (
        FIXTURE_ROOT / "expected" / "current-work-short.txt"
    ).read_text(encoding="utf-8")
    assert result.detailed_text == (
        FIXTURE_ROOT / "expected" / "current-work-detailed.txt"
    ).read_text(encoding="utf-8")
    assert result.authority_status == "valid"
    assert result.display_status == "rendered"
    assert result.display_error is None


def test_rereads_saved_event_identity_digests_and_derived_artifacts(
    tmp_path,
):
    bootstrap = _bootstrap()
    inputs = _e2e_inputs(tmp_path)

    result = bootstrap.run_session_bootstrap(**inputs)

    saved_events = tuple(
        json.loads(line)
        for line in result.capture.raw_path.read_text(
            encoding="utf-8"
        ).splitlines()
    )
    assert [event["event_type"] for event in saved_events] == [
        "session_started",
        "work_started",
        "session_ended",
    ]
    raw_digest = hashlib.sha256(
        result.capture.raw_path.read_bytes()
    ).hexdigest()
    assert raw_digest == result.capture.evidence["digests"]["raw_sha256"]
    assert raw_digest == result.projection["inputs"][1]["digest"]
    assert result.projection["generated_at"] == "2026-08-03T10:00:04+09:00"
    assert result.projection["freshness"] == "current"
    for name, path in result.capture.derived_paths.items():
        assert path.read_bytes() == (
            FIXTURE_ROOT / "expected" / {
                "index": "index.json",
                "summary": "summary.json",
                "transcript": "transcript.md",
            }[name]
        ).read_bytes()


def test_display_failure_does_not_discard_valid_capture_or_authority(
    tmp_path,
):
    bootstrap = _bootstrap()
    inputs = _e2e_inputs(tmp_path)

    def failing_renderer(_projection, *, mode):
        raise RuntimeError(f"fixture {mode} display failure")

    result = bootstrap.run_session_bootstrap(
        **inputs,
        renderer=failing_renderer,
    )

    assert result.capture.raw_path.is_file()
    assert result.capture.evidence_path.is_file()
    assert result.projection["diagnostics"]["status"] == "complete"
    assert result.authority_status == "valid"
    assert result.display_status == "failed"
    assert result.display_error == "renderer_failed"
    assert result.short_text is None
    assert result.detailed_text is None


def test_missing_authority_is_incomplete_not_a_display_failure(tmp_path):
    bootstrap = _bootstrap()
    inputs = _e2e_inputs(tmp_path)
    inputs["projection_inputs"] = copy.deepcopy(
        inputs["projection_inputs"]
    )
    inputs["projection_inputs"]["fixed_inputs"] = []

    result = bootstrap.run_session_bootstrap(**inputs)

    assert result.capture.raw_path.is_file()
    assert result.projection["diagnostics"]["status"] == "incomplete"
    assert result.authority_status == "incomplete"
    assert result.display_status == "rendered"
    assert result.display_error is None
    assert "STATUS: INCOMPLETE" in result.detailed_text
