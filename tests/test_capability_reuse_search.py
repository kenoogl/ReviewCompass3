"""作業ごとの必要な働きから全コードの再利用候補を導く試験。"""

import json
from pathlib import Path

import pytest

from tools.development import reuse_search_record as reuse


PROFILE_ID = "a" * 64
DISCOVERY_ID = "b" * 64
SOURCE_ID = "c" * 64


def _routine(symbol_id, *, markers=(), callees=(), callers=()):
    relative = symbol_id.split(":", 1)[0]
    return {
        "symbol_id": symbol_id,
        "code_reference": {
            "relative_path": relative,
            "start_line": 1,
            "end_line": 2,
        },
        "signature": {"parameters": [], "returns_annotation": None},
        "structure_digest": symbol_id,
        "syntactic_effect_markers": list(markers),
        "direct_callee_symbol_ids": list(callees),
        "direct_caller_symbol_ids": list(callers),
        "raised_exception_names": [],
        "caught_exception_names": [],
    }


def _profile():
    atomic = "tools/common/atomic.py:atomic_replace"
    anchor = "tools/feature/save.py:save_record"
    risky = "tools/other/upload.py:write_and_send"
    unrelated = "tools/other/display.py:show_status"
    return {
        "profile_run_id": PROFILE_ID,
        "source_content_id": SOURCE_ID,
        "schema_version": 3,
        "extraction_rule_version": 4,
        "routines": [
            _routine(anchor, markers=("file_write",), callees=(atomic,)),
            _routine(atomic, markers=("file_write",), callers=(anchor,)),
            _routine(risky, markers=("file_write", "network")),
            _routine(unrelated),
        ],
    }


def _discovery():
    return {
        "discovery_run_id": DISCOVERY_ID,
        "source_content_id": SOURCE_ID,
        "schema_version": 1,
        "grouping_rule_version": 1,
        "groups": [
            {
                "group_id": "CG-STRUCT-0001",
                "basis_kind": "structural_exact_match",
                "presentation_class": "focused",
                "member_symbol_ids": [
                    "tools/common/atomic.py:atomic_replace",
                    "tools/feature/save.py:save_record",
                ],
            },
            {
                "group_id": "CG-IFACE-0001",
                "basis_kind": "interface_shape_match",
                "presentation_class": "focused",
                "member_symbol_ids": [
                    "tools/feature/save.py:save_record",
                    "tools/other/display.py:show_status",
                ],
            }
        ],
    }


def _write_source(root, relative, lifecycle):
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        '"""fixture\n\nlifecycle: ' + lifecycle + '\n"""\n',
        encoding="utf-8",
    )


def _capability(**overrides):
    document = {
        "capability_id": "safe_atomic_write",
        "responsibility": "途中状態を正式データにせず保存する",
        "inputs": ["保存内容", "保存先"],
        "outputs": ["確定済みfile"],
        "failure_behavior": ["途中状態を正式データとして扱わない"],
        "required_properties": ["一時fileから確定する"],
        "reference_paths": ["tools/feature/save.py"],
        "reference_symbols": [],
        "symbol_terms": [],
        "required_effect_markers": ["file_write"],
        "forbidden_effect_markers": ["network"],
    }
    document.update(overrides)
    return document


def test_capability_search_expands_from_anchor_to_full_repository_candidates(tmp_path):
    _write_source(tmp_path, "tools/feature/save.py", "stable")
    _write_source(tmp_path, "tools/common/atomic.py", "provisional")
    _write_source(tmp_path, "tools/other/upload.py", "provisional")
    observation = {
        "snapshot_id": "d" * 64,
        "files": [
            {
                "path": path.relative_to(tmp_path).as_posix(),
                "file_sha256": reuse.file_sha256(path),
            }
            for path in sorted((tmp_path / "tools").rglob("*.py"))
        ],
    }

    record = reuse.search_required_capabilities(
        profile_document=_profile(),
        discovery_document=_discovery(),
        declaration={
            "subject": "safe_storage",
            "source_scope_paths": ["tools"],
            "capabilities": [_capability()],
        },
        observation_document=observation,
        project_root=tmp_path,
    )

    result = record["capability_results"][0]
    by_id = {item["symbol_id"]: item for item in result["candidates"]}
    assert result["coverage_status"] == "candidates_found"
    assert "tools/common/atomic.py:atomic_replace" in by_id
    assert "comparison_group_member" in by_id[
        "tools/common/atomic.py:atomic_replace"
    ]["match_reasons"]
    assert by_id["tools/common/atomic.py:atomic_replace"]["declared_lifecycle"] == (
        "provisional"
    )
    assert by_id["tools/feature/save.py:save_record"]["declared_lifecycle"] == "stable"
    assert "tools/other/display.py:show_status" not in by_id
    assert by_id["tools/other/upload.py:write_and_send"][
        "conflicting_effect_markers"
    ] == ["network"]
    assert record["human_adjudication_required"] is True


def test_capability_search_reports_uncovered_work_without_fixed_path(tmp_path):
    _write_source(tmp_path, "tools/feature/save.py", "stable")
    observation = {
        "snapshot_id": "d" * 64,
        "files": [
            {
                "path": "tools/feature/save.py",
                "file_sha256": reuse.file_sha256(tmp_path / "tools/feature/save.py"),
            }
        ],
    }
    capability = _capability(
        capability_id="content_digest",
        reference_paths=[],
        symbol_terms=["content_digest"],
        required_effect_markers=[],
        forbidden_effect_markers=[],
    )

    record = reuse.search_required_capabilities(
        profile_document=_profile(),
        discovery_document=_discovery(),
        declaration={
            "subject": "digest_work",
            "source_scope_paths": ["tools"],
            "capabilities": [capability],
        },
        observation_document=observation,
        project_root=tmp_path,
    )

    assert record["uncovered_capability_ids"] == ["content_digest"]
    assert record["capability_results"][0]["coverage_status"] == "no_candidates"


def test_capability_search_never_emits_reuse_disposition(tmp_path):
    _write_source(tmp_path, "tools/feature/save.py", "stable")
    observation = {
        "snapshot_id": "d" * 64,
        "files": [
            {
                "path": "tools/feature/save.py",
                "file_sha256": reuse.file_sha256(tmp_path / "tools/feature/save.py"),
            }
        ],
    }

    record = reuse.search_required_capabilities(
        profile_document=_profile(),
        discovery_document=_discovery(),
        declaration={
            "subject": "safe_storage",
            "source_scope_paths": ["tools"],
            "capabilities": [_capability()],
        },
        observation_document=observation,
        project_root=tmp_path,
    )

    serialized = json.dumps(record, ensure_ascii=False, sort_keys=True)
    assert "recommended_disposition" not in serialized
    assert '"disposition"' not in serialized


def test_capability_rejects_effect_that_is_both_required_and_forbidden(tmp_path):
    capability = _capability(
        required_effect_markers=["file_write"],
        forbidden_effect_markers=["file_write"],
    )

    with pytest.raises(reuse.ReuseSearchError):
        reuse.search_required_capabilities(
            profile_document=_profile(),
            discovery_document=_discovery(),
            declaration={
                "subject": "invalid",
                "source_scope_paths": ["tools"],
                "capabilities": [capability],
            },
            observation_document={"snapshot_id": "d" * 64, "files": []},
            project_root=tmp_path,
        )
