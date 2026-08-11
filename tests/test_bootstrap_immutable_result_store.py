"""Bootstrap とpilotが共有する不変JSON保存境界の受入テスト。"""

import dataclasses
import importlib
import json

import pytest


def _canonical_file_bytes(value):
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        + b"\n"
    )


def test_common_store_writes_canonical_json_once_and_rereads_it(tmp_path):
    store = importlib.import_module("tools.bootstrap.immutable_result_store")
    document = {"z": "日本語", "a": [2, 1]}

    store.store_immutable_json(
        tmp_path,
        "raw/attempt-001.json",
        document,
    )

    path = tmp_path / "raw/attempt-001.json"
    expected = _canonical_file_bytes(document)
    assert path.read_bytes() == expected


def test_common_store_rejects_overwrite_without_changing_original(tmp_path):
    store = importlib.import_module("tools.bootstrap.immutable_result_store")
    original = {"value": "first"}
    store.store_immutable_json(tmp_path, "raw/result.json", original)
    original_bytes = (tmp_path / "raw/result.json").read_bytes()

    with pytest.raises(store.ImmutableResultStoreError):
        store.store_immutable_json(tmp_path, "raw/result.json", {"value": "second"})

    assert (tmp_path / "raw/result.json").read_bytes() == original_bytes


@pytest.mark.parametrize(
    "relative_path",
    ("", ".", "../escape.json", "/absolute.json", "raw/../escape.json", "a\x00b"),
)
def test_common_store_rejects_unsafe_relative_paths(tmp_path, relative_path):
    store = importlib.import_module("tools.bootstrap.immutable_result_store")

    with pytest.raises(store.ImmutableResultStoreError):
        store.store_immutable_json(tmp_path, relative_path, {"value": True})


def test_common_store_rejects_symlinked_parent(tmp_path):
    store = importlib.import_module("tools.bootstrap.immutable_result_store")
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "linked").symlink_to(outside, target_is_directory=True)

    with pytest.raises(store.ImmutableResultStoreError):
        store.store_immutable_json(tmp_path, "linked/result.json", {"value": True})

    assert not (outside / "result.json").exists()


def test_existing_raw_review_store_calls_common_immutable_boundary(
    tmp_path,
    monkeypatch,
):
    common_store = importlib.import_module("tools.bootstrap.immutable_result_store")
    raw_store = importlib.import_module("tools.bootstrap.raw_review_store")
    review_execution = importlib.import_module("tools.bootstrap.review_execution")
    original_store = common_store.store_immutable_json
    observed_paths = []

    def observing_store(storage_root, relative_path, document):
        observed_paths.append(relative_path)
        return original_store(storage_root, relative_path, document)

    monkeypatch.setattr(common_store, "store_immutable_json", observing_store)
    raw_store = importlib.reload(raw_store)
    assignments = (
        review_execution.ReviewAssignment(
            name="main",
            provider="provider-a",
            model="model-a",
            route="main",
        ),
        review_execution.ReviewAssignment(
            name="independent",
            provider="provider-b",
            model="model-b",
            route="independent",
        ),
    )
    executions = tuple(
        review_execution.ReviewExecution(
            assignment=assignment,
            status="succeeded",
            raw_response=f'{{"assignment":"{assignment.name}"}}',
            error=None,
            contracted_payload_digest="a" * 64,
        )
        for assignment in assignments
    )

    try:
        records = raw_store.store_raw_executions(
            tmp_path,
            "attempt-001",
            executions,
        )
    finally:
        monkeypatch.setattr(common_store, "store_immutable_json", original_store)
        importlib.reload(raw_store)

    assert tuple(record.assignment_name for record in records) == (
        "independent",
        "main",
    )
    assert observed_paths == [
        "attempt-001/independent.raw.json",
        "attempt-001/main.raw.json",
    ]


def test_existing_raw_review_store_public_contract_is_unchanged():
    raw_store = importlib.import_module("tools.bootstrap.raw_review_store")

    assert issubclass(raw_store.RawReviewStoreError, Exception)
    assert tuple(field.name for field in dataclasses.fields(raw_store.RawReviewRecord)) == (
        "attempt_id",
        "assignment_name",
        "route",
        "status",
        "contracted_payload_digest",
        "raw_digest",
        "relative_path",
    )
