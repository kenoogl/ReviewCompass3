"""Work 1B durable capture境界の受入テスト。"""

import copy
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BOOTSTRAP_FIXTURE = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "development"
    / "session-log-bootstrap"
)
DURABLE_FIXTURE = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "development"
    / "session-log-durable-capture"
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


def _capture_inputs(tmp_path):
    return {
        "layout": _layout_resolution(tmp_path),
        "profile": _json(BOOTSTRAP_FIXTURE / "capture-profile.json"),
        "raw_bytes": (
            BOOTSTRAP_FIXTURE / "raw" / "session.jsonl"
        ).read_bytes(),
    }


def test_persists_and_rereads_raw_derived_artifacts_and_session_evidence(
    tmp_path,
):
    bootstrap = _bootstrap()
    inputs = _capture_inputs(tmp_path)
    expected_evidence_path = (
        DURABLE_FIXTURE / "expected-session-evidence.json"
    )
    expected_evidence = _json(expected_evidence_path)

    result = bootstrap.persist_session_capture(**inputs)

    assert result.raw_path.read_bytes() == inputs["raw_bytes"]
    assert result.evidence_path.read_bytes() == (
        expected_evidence_path.read_bytes()
    )
    assert result.evidence == expected_evidence
    assert result.derived_paths == {
        "index": (
            inputs["layout"].roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "index.json"
        ),
        "summary": (
            inputs["layout"].roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "summary.json"
        ),
        "transcript": (
            inputs["layout"].roots["data_root"]
            / "sessions"
            / "session-work1b-fixture"
            / "transcript.md"
        ),
    }
    for name, path in result.derived_paths.items():
        assert path.read_bytes() == (
            BOOTSTRAP_FIXTURE / "expected" / {
                "index": "index.json",
                "summary": "summary.json",
                "transcript": "transcript.md",
            }[name]
        ).read_bytes()
    assert list(inputs["layout"].roots["project_root"].iterdir()) == []


def test_rejects_digest_mismatch_before_creating_capture_files(tmp_path):
    bootstrap = _bootstrap()
    inputs = _capture_inputs(tmp_path)
    inputs["profile"] = copy.deepcopy(inputs["profile"])
    inputs["profile"]["digests"]["transcript_sha256"] = "0" * 64

    with pytest.raises(
        bootstrap.SessionLogBootstrapError,
        match="Digest",
    ):
        bootstrap.persist_session_capture(**inputs)

    assert not (
        inputs["layout"].roots["sensitive_root"] / "sessions"
    ).exists()
    assert not (
        inputs["layout"].roots["data_root"] / "sessions"
    ).exists()


def test_preserves_existing_file_and_writes_no_other_capture_artifacts(
    tmp_path,
):
    bootstrap = _bootstrap()
    inputs = _capture_inputs(tmp_path)
    raw_path = (
        inputs["layout"].roots["sensitive_root"]
        / "sessions"
        / "session-work1b-fixture"
        / "raw"
        / "session.jsonl"
    )
    raw_path.parent.mkdir(parents=True)
    raw_path.write_bytes(b"preserve-existing\n")

    with pytest.raises(
        bootstrap.SessionLogBootstrapError,
        match="already exists",
    ):
        bootstrap.persist_session_capture(**inputs)

    assert raw_path.read_bytes() == b"preserve-existing\n"
    assert not (
        inputs["layout"].roots["data_root"] / "sessions"
    ).exists()


def test_rolls_back_files_when_durable_write_fails_partway(tmp_path):
    bootstrap = _bootstrap()
    inputs = _capture_inputs(tmp_path)
    write_count = 0

    def fail_on_third_write(path, content):
        nonlocal write_count
        write_count += 1
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if write_count == 3:
            raise OSError("fixture partial write failure")
        path.write_bytes(content)

    with pytest.raises(
        bootstrap.SessionLogBootstrapError,
        match="partial capture",
    ):
        bootstrap.persist_session_capture(
            **inputs,
            write_bytes=fail_on_third_write,
        )

    assert write_count == 3
    assert not (
        inputs["layout"].roots["sensitive_root"] / "sessions"
    ).exists()
    assert not (
        inputs["layout"].roots["data_root"] / "sessions"
    ).exists()
