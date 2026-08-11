"""Bootstrap とpilotが共有する不変JSON保存境界の受入テスト。"""

import dataclasses
import importlib
import json
from pathlib import Path

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


def test_existing_raw_review_store_uses_common_immutable_boundary():
    raw_store_path = Path(__file__).resolve().parents[1] / "tools/bootstrap/raw_review_store.py"
    source = raw_store_path.read_text(encoding="utf-8")

    assert "tools.bootstrap.immutable_result_store" in source


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
