"""一件レビュー材料作成・結果整理の製品契約試験。"""

import importlib
import os
from pathlib import Path

import pytest


MATERIAL_LIMIT = 262_144
REVIEW_SPEC_LIMIT = 65_536
RESULTS_LIMIT = 1_048_576


def _review():
    return importlib.import_module("tools.reviews.one_item_review")


def _inputs(tmp_path, *, with_results=True):
    input_root = tmp_path / "input"
    input_root.mkdir()
    material = input_root / "material.txt"
    review_spec = input_root / "review-spec.json"
    results = input_root / "results.json"
    material.write_bytes(b"synthetic material\n")
    review_spec.write_bytes(b'{"schema_version":1}\n')
    if with_results:
        results.write_bytes(b'{"schema_version":1,"reviews":[]}\n')
    return {
        "input_root": input_root.absolute(),
        "material": material.absolute(),
        "review_spec": review_spec.absolute(),
        "results": results.absolute() if with_results else None,
    }


def _read(review, paths):
    return review.read_input_files(
        input_root=paths["input_root"],
        material=paths["material"],
        review_spec=paths["review_spec"],
        results=paths["results"],
    )


@pytest.mark.parametrize("with_results", (False, True))
def test_reads_only_the_explicit_regular_input_files(tmp_path, monkeypatch, with_results):
    review = _review()
    paths = _inputs(tmp_path, with_results=with_results)

    def fail_discovery(*args, **kwargs):
        raise AssertionError("input directory discovery is forbidden")

    monkeypatch.setattr(os, "scandir", fail_discovery)
    monkeypatch.setattr(Path, "iterdir", fail_discovery)
    monkeypatch.setattr(Path, "glob", fail_discovery)
    monkeypatch.setattr(Path, "rglob", fail_discovery)

    actual = _read(review, paths)

    expected = {
        "material": b"synthetic material\n",
        "review_spec": b'{"schema_version":1}\n',
    }
    if with_results:
        expected["results"] = b'{"schema_version":1,"reviews":[]}\n'
    assert actual == expected


@pytest.mark.parametrize(
    "path_name",
    ("input_root", "material", "review_spec", "results"),
)
def test_rejects_relative_paths(tmp_path, path_name):
    review = _review()
    paths = _inputs(tmp_path)
    paths[path_name] = Path("relative") / path_name

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "invalid_path"


def test_rejects_file_outside_the_explicit_root(tmp_path):
    review = _review()
    paths = _inputs(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"outside\n")
    paths["material"] = outside.absolute()

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "invalid_path"


@pytest.mark.parametrize("placement", ("root", "intermediate", "file"))
def test_rejects_symlink_in_the_path_without_reading_its_target(tmp_path, placement):
    review = _review()
    paths = _inputs(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    secret = outside / "secret.txt"
    secret.write_bytes(b"must-not-be-read\n")

    if placement == "root":
        linked_root = tmp_path / "linked-root"
        linked_root.symlink_to(paths["input_root"], target_is_directory=True)
        paths["input_root"] = linked_root.absolute()
        paths["material"] = linked_root / "material.txt"
        paths["review_spec"] = linked_root / "review-spec.json"
        paths["results"] = linked_root / "results.json"
    elif placement == "intermediate":
        linked_directory = paths["input_root"] / "linked"
        linked_directory.symlink_to(outside, target_is_directory=True)
        paths["material"] = linked_directory / "secret.txt"
    else:
        linked_file = paths["input_root"] / "linked.txt"
        linked_file.symlink_to(secret)
        paths["material"] = linked_file

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "invalid_path"


def test_rejects_non_regular_input(tmp_path):
    review = _review()
    paths = _inputs(tmp_path)
    directory = paths["input_root"] / "directory"
    directory.mkdir()
    paths["material"] = directory

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "invalid_path"


@pytest.mark.parametrize("identity_kind", ("same_path", "hard_link"))
def test_rejects_inputs_that_are_the_same_file(tmp_path, identity_kind):
    review = _review()
    paths = _inputs(tmp_path)
    if identity_kind == "same_path":
        paths["review_spec"] = paths["material"]
    else:
        hard_link = paths["input_root"] / "same-file.json"
        os.link(paths["material"], hard_link)
        paths["review_spec"] = hard_link

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "invalid_arguments"


def test_rejects_missing_input(tmp_path):
    review = _review()
    paths = _inputs(tmp_path)
    paths["material"].unlink()

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "unreadable_input"


@pytest.mark.parametrize("path_name", ("material", "review_spec", "results"))
@pytest.mark.parametrize(
    ("content", "reason"),
    ((b"", "invalid_schema"), (b"contains\x00nul", "invalid_schema"), (b"\xff", "invalid_utf8")),
)
def test_rejects_empty_nul_or_non_utf8_input(tmp_path, path_name, content, reason):
    review = _review()
    paths = _inputs(tmp_path)
    paths[path_name].write_bytes(content)

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == reason


@pytest.mark.parametrize(
    ("path_name", "limit"),
    (
        ("material", MATERIAL_LIMIT),
        ("review_spec", REVIEW_SPEC_LIMIT),
        ("results", RESULTS_LIMIT),
    ),
)
def test_accepts_each_exact_size_limit(tmp_path, path_name, limit):
    review = _review()
    paths = _inputs(tmp_path)
    paths[path_name].write_bytes(b"x" * limit)

    actual = _read(review, paths)

    assert actual[path_name] == b"x" * limit


@pytest.mark.parametrize(
    ("path_name", "limit"),
    (
        ("material", MATERIAL_LIMIT),
        ("review_spec", REVIEW_SPEC_LIMIT),
        ("results", RESULTS_LIMIT),
    ),
)
def test_rejects_each_size_limit_plus_one(tmp_path, path_name, limit):
    review = _review()
    paths = _inputs(tmp_path)
    paths[path_name].write_bytes(b"x" * (limit + 1))

    with pytest.raises(review.ReviewStop) as caught:
        _read(review, paths)

    assert caught.value.reason == "size_limit_exceeded"
