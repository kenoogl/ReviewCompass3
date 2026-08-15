"""一件レビュー材料作成・結果整理の製品契約試験。"""

import importlib
import hashlib
import json
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


def _valid_spec():
    return {
        "schema_version": 1,
        "material_identifier": "SYNTHETIC-1",
        "goal": "Review the synthetic material.",
        "criteria": [
            {"id": "C-2", "text": "Second criterion."},
            {"id": "C-1", "text": "First criterion."},
        ],
        "constraints": ["Do not send externally.", "Keep every finding."],
    }


def _canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _prepare(review, material=b"first line\nsecond line\n", spec=None):
    selected = _valid_spec() if spec is None else spec
    return review.prepare_material(material, _canonical(selected))


def test_prepares_the_exact_deterministic_material_package():
    review = _review()
    spec = _valid_spec()
    material = b"first line\nsecond line\n"
    normalized_spec = {
        **spec,
        "criteria": sorted(spec["criteria"], key=lambda item: item["id"]),
    }
    expected = {
        "external_send_approved": False,
        "material": {
            "content": material.decode("utf-8"),
            "content_sha256": hashlib.sha256(material).hexdigest(),
            "identifier": "SYNTHETIC-1",
            "line_count": 2,
        },
        "result_schema": {
            "grouping_basis": "supplied_issue_key",
            "schema_version": 1,
            "semantic_deduplication_performed": False,
        },
        "review_spec": {
            "constraints": spec["constraints"],
            "criteria": normalized_spec["criteria"],
            "goal": spec["goal"],
            "sha256": hashlib.sha256(_canonical(normalized_spec)).hexdigest(),
        },
        "schema_version": 1,
        "status": "material_prepared",
    }
    expected["material_package_sha256"] = hashlib.sha256(
        _canonical(expected)
    ).hexdigest()

    actual = review.prepare_material(material, _canonical(spec))

    assert actual == expected


def test_prepare_is_independent_of_spec_object_key_and_criteria_input_order():
    review = _review()
    first = _valid_spec()
    second = {
        "constraints": first["constraints"],
        "criteria": list(reversed(first["criteria"])),
        "goal": first["goal"],
        "material_identifier": first["material_identifier"],
        "schema_version": first["schema_version"],
    }

    first_result = review.prepare_material(b"material\n", _canonical(first))
    second_result = review.prepare_material(
        b"material\n",
        json.dumps(second, ensure_ascii=False, indent=2).encode("utf-8"),
    )

    assert first_result == second_result


@pytest.mark.parametrize(
    "change",
    (
        "invalid_json",
        "unknown_root_key",
        "missing_goal",
        "wrong_schema_version",
        "invalid_identifier",
        "empty_goal",
        "too_long_goal",
        "empty_criteria",
        "too_many_criteria",
        "duplicate_criterion",
        "unknown_criterion_key",
        "empty_criterion_text",
        "too_many_constraints",
        "non_string_constraint",
    ),
)
def test_rejects_invalid_review_spec_schema(change):
    review = _review()
    spec = _valid_spec()
    if change == "invalid_json":
        encoded = b"{"
    else:
        if change == "unknown_root_key":
            spec["extra"] = True
        elif change == "missing_goal":
            del spec["goal"]
        elif change == "wrong_schema_version":
            spec["schema_version"] = 2
        elif change == "invalid_identifier":
            spec["material_identifier"] = "invalid identifier"
        elif change == "empty_goal":
            spec["goal"] = ""
        elif change == "too_long_goal":
            spec["goal"] = "x" * 2_001
        elif change == "empty_criteria":
            spec["criteria"] = []
        elif change == "too_many_criteria":
            spec["criteria"] = [
                {"id": f"C-{index}", "text": "criterion"}
                for index in range(17)
            ]
        elif change == "duplicate_criterion":
            spec["criteria"][1]["id"] = spec["criteria"][0]["id"]
        elif change == "unknown_criterion_key":
            spec["criteria"][0]["extra"] = True
        elif change == "empty_criterion_text":
            spec["criteria"][0]["text"] = ""
        elif change == "too_many_constraints":
            spec["constraints"] = ["constraint"] * 17
        else:
            spec["constraints"] = [1]
        encoded = _canonical(spec)

    with pytest.raises(review.ReviewStop) as caught:
        review.prepare_material(b"material\n", encoded)

    assert caught.value.reason == "invalid_schema"


@pytest.mark.parametrize(
    "candidate",
    (
        "person@example.test",
        "Bearer ABCDEFGHIJKLMNOPQRSTUVWX",
        "api_key=abcdefghijklmnop",
        "-----BEGIN PRIVATE KEY-----\nvalue\n-----END PRIVATE KEY-----",
        "AKIAABCDEFGHIJKLMNOP",
        "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6",
    ),
)
@pytest.mark.parametrize("location", ("material", "goal", "json_key"))
def test_stops_without_exposing_sensitive_candidates(candidate, location):
    review = _review()
    spec = _valid_spec()
    material = b"material\n"
    if location == "material":
        material = candidate.encode("utf-8")
    elif location == "goal":
        spec["goal"] = candidate
    else:
        spec[candidate] = "value"

    with pytest.raises(review.ReviewStop) as caught:
        review.prepare_material(material, _canonical(spec))

    assert caught.value.reason == "sensitive_data_remaining"
    assert candidate not in str(caught.value)


@pytest.mark.parametrize(
    "candidate",
    (
        "work=/Users/example/project",
        "path:/Users/example/project",
        "path=C:\\Users\\example",
        "\\\\server\\share\\item",
        "//server/share/item",
        "file:///tmp/item",
    ),
)
@pytest.mark.parametrize("location", ("material", "goal", "json_key"))
def test_stops_without_exposing_absolute_paths(candidate, location):
    review = _review()
    spec = _valid_spec()
    material = b"material\n"
    if location == "material":
        material = candidate.encode("utf-8")
    elif location == "goal":
        spec["goal"] = candidate
    else:
        spec[candidate] = "value"

    with pytest.raises(review.ReviewStop) as caught:
        review.prepare_material(material, _canonical(spec))

    assert caught.value.reason == "absolute_path_remaining"
    assert candidate not in str(caught.value)


@pytest.mark.parametrize(
    "safe_text",
    ("https://example.test/item", "relative/path", "/"),
)
def test_does_not_stop_for_contract_absolute_path_non_examples(safe_text):
    review = _review()
    spec = _valid_spec()
    spec["goal"] = safe_text

    actual = review.prepare_material(b"material\n", _canonical(spec))

    assert actual["status"] == "material_prepared"


def test_prepare_does_not_resolve_environment_sensitive_rules(monkeypatch):
    review = _review()
    redaction = importlib.import_module("tools.session_logs.redaction")

    def fail_environment_resolution(*args, **kwargs):
        raise AssertionError("environment-sensitive rules must not be resolved")

    monkeypatch.setattr(redaction, "environment_reference_rules", fail_environment_resolution)
    monkeypatch.setattr(redaction, "resolve_environment_rules", fail_environment_resolution)

    assert _prepare(review)["status"] == "material_prepared"


def _valid_results(material_package_sha256):
    return {
        "schema_version": 1,
        "material_package_sha256": material_package_sha256,
        "reviews": [
            {
                "reviewer_id": "REVIEWER-2",
                "verdict": "findings_present",
                "summary": "Two synthetic findings.",
                "findings": [
                    {
                        "finding_id": "F-2",
                        "issue_key": "ISSUE-2",
                        "severity": "warning",
                        "title": "Second issue",
                        "description": "Second description.",
                        "criterion_ids": ["C-2", "C-1"],
                        "start_line": 2,
                        "end_line": 2,
                    },
                    {
                        "finding_id": "F-1",
                        "issue_key": "ISSUE-1",
                        "severity": "error",
                        "title": "First issue",
                        "description": "First description.",
                        "criterion_ids": ["C-1"],
                        "start_line": 1,
                        "end_line": 1,
                    },
                ],
            },
            {
                "reviewer_id": "REVIEWER-1",
                "verdict": "no_findings",
                "summary": "No findings.",
                "findings": [],
            },
        ],
    }


def _validate_results(review, results=None):
    material = _prepare(review)
    selected = (
        _valid_results(material["material_package_sha256"])
        if results is None
        else results
    )
    return material, review.validate_results(material, _canonical(selected))


def _normalized_review(review_value):
    normalized = json.loads(json.dumps(review_value))
    normalized["findings"] = sorted(
        normalized["findings"],
        key=lambda item: (item["issue_key"], item["finding_id"]),
    )
    for finding in normalized["findings"]:
        finding["criterion_ids"] = sorted(finding["criterion_ids"])
    return normalized


def test_validates_and_normalizes_the_result_set_with_exact_hashes():
    review = _review()
    material = _prepare(review)
    supplied = _valid_results(material["material_package_sha256"])
    normalized_reviews = sorted(
        (_normalized_review(item) for item in supplied["reviews"]),
        key=lambda item: item["reviewer_id"],
    )
    normalized_root = {
        "material_package_sha256": material["material_package_sha256"],
        "reviews": normalized_reviews,
        "schema_version": 1,
    }
    expected_reviews = []
    for item in normalized_reviews:
        without_reviewer = {
            key: value for key, value in item.items() if key != "reviewer_id"
        }
        expected_reviews.append({
            "review": item,
            "review_content_sha256": hashlib.sha256(
                _canonical(without_reviewer)
            ).hexdigest(),
            "review_sha256": hashlib.sha256(_canonical(item)).hexdigest(),
        })

    actual = review.validate_results(material, _canonical(supplied))

    assert actual == {
        "material_package_sha256": material["material_package_sha256"],
        "result_set_sha256": hashlib.sha256(_canonical(normalized_root)).hexdigest(),
        "reviews": expected_reviews,
    }


def test_result_hashes_ignore_set_like_input_order_only():
    review = _review()
    material = _prepare(review)
    first = _valid_results(material["material_package_sha256"])
    second = json.loads(json.dumps(first))
    second["reviews"].reverse()
    second["reviews"][1]["findings"].reverse()
    second["reviews"][1]["findings"][1]["criterion_ids"].reverse()

    first_value = review.validate_results(material, _canonical(first))
    second_value = review.validate_results(material, _canonical(second))

    assert first_value == second_value


@pytest.mark.parametrize(
    "change",
    (
        "invalid_json",
        "unknown_root_key",
        "wrong_schema_version",
        "empty_reviews",
        "too_many_reviews",
        "unknown_review_key",
        "duplicate_reviewer",
        "invalid_reviewer",
        "invalid_verdict",
        "verdict_count_mismatch",
        "unknown_finding_key",
        "duplicate_finding",
        "duplicate_issue_key",
        "invalid_severity",
        "unknown_criterion",
        "duplicate_criterion",
        "invalid_line_order",
        "line_out_of_range",
        "too_many_findings",
    ),
)
def test_rejects_invalid_result_set_schema(change):
    review = _review()
    material = _prepare(review)
    results = _valid_results(material["material_package_sha256"])
    if change == "invalid_json":
        encoded = b"{"
    else:
        first_review = results["reviews"][0]
        first_finding = first_review["findings"][0]
        if change == "unknown_root_key":
            results["extra"] = True
        elif change == "wrong_schema_version":
            results["schema_version"] = 2
        elif change == "empty_reviews":
            results["reviews"] = []
        elif change == "too_many_reviews":
            template = results["reviews"][1]
            results["reviews"] = [
                {**template, "reviewer_id": f"REVIEWER-{index}"}
                for index in range(9)
            ]
        elif change == "unknown_review_key":
            first_review["extra"] = True
        elif change == "duplicate_reviewer":
            results["reviews"][1]["reviewer_id"] = first_review["reviewer_id"]
        elif change == "invalid_reviewer":
            first_review["reviewer_id"] = "invalid reviewer"
        elif change == "invalid_verdict":
            first_review["verdict"] = "approved"
        elif change == "verdict_count_mismatch":
            first_review["verdict"] = "no_findings"
        elif change == "unknown_finding_key":
            first_finding["extra"] = True
        elif change == "duplicate_finding":
            first_review["findings"][1]["finding_id"] = first_finding["finding_id"]
        elif change == "duplicate_issue_key":
            first_review["findings"][1]["issue_key"] = first_finding["issue_key"]
        elif change == "invalid_severity":
            first_finding["severity"] = "critical"
        elif change == "unknown_criterion":
            first_finding["criterion_ids"] = ["C-UNKNOWN"]
        elif change == "duplicate_criterion":
            first_finding["criterion_ids"] = ["C-1", "C-1"]
        elif change == "invalid_line_order":
            first_finding["start_line"] = 2
            first_finding["end_line"] = 1
        elif change == "line_out_of_range":
            first_finding["end_line"] = 3
        else:
            first_review["findings"] = [
                {
                    **first_finding,
                    "finding_id": f"F-{index}",
                    "issue_key": f"ISSUE-{index}",
                }
                for index in range(101)
            ]
        encoded = _canonical(results)

    with pytest.raises(review.ReviewStop) as caught:
        review.validate_results(material, encoded)

    assert caught.value.reason == "invalid_schema"


def test_rejects_result_set_bound_to_another_material():
    review = _review()
    material = _prepare(review)
    results = _valid_results("0" * 64)

    with pytest.raises(review.ReviewStop) as caught:
        review.validate_results(material, _canonical(results))

    assert caught.value.reason == "stale_material"


@pytest.mark.parametrize(
    ("candidate", "reason"),
    (
        ("person@example.test", "sensitive_data_remaining"),
        ("A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6", "sensitive_data_remaining"),
        ("work=/Users/example/project", "absolute_path_remaining"),
        ("path=C:\\Users\\example", "absolute_path_remaining"),
        ("\\\\server\\share\\item", "absolute_path_remaining"),
        ("//server/share/item", "absolute_path_remaining"),
        ("file:///tmp/item", "absolute_path_remaining"),
    ),
)
@pytest.mark.parametrize(
    "location",
    ("summary", "title", "description", "reviewer_id", "json_key"),
)
def test_rejects_unsafe_result_strings_without_exposing_them(
    candidate,
    reason,
    location,
):
    review = _review()
    material = _prepare(review)
    results = _valid_results(material["material_package_sha256"])
    if location == "summary":
        results["reviews"][0]["summary"] = candidate
    elif location == "title":
        results["reviews"][0]["findings"][0]["title"] = candidate
    elif location == "description":
        results["reviews"][0]["findings"][0]["description"] = candidate
    elif location == "reviewer_id":
        results["reviews"][0]["reviewer_id"] = candidate
    else:
        results["reviews"][0][candidate] = "value"

    with pytest.raises(review.ReviewStop) as caught:
        review.validate_results(material, _canonical(results))

    assert caught.value.reason == reason
    assert candidate not in str(caught.value)


def _finding(finding_id, issue_key, *, severity="warning", title="Issue", description="Description."):
    return {
        "finding_id": finding_id,
        "issue_key": issue_key,
        "severity": severity,
        "title": title,
        "description": description,
        "criterion_ids": ["C-1"],
        "start_line": 1,
        "end_line": 1,
    }


def _organization_results(material_sha256):
    duplicate_finding = _finding(
        "F-DUP",
        "ISSUE-DUP",
        title="Duplicated review issue",
    )
    return {
        "schema_version": 1,
        "material_package_sha256": material_sha256,
        "reviews": [
            {
                "reviewer_id": "R-B",
                "verdict": "findings_present",
                "summary": "Second report.",
                "findings": [
                    _finding("F-M2", "ISSUE-MATCH", title="Matching issue"),
                    _finding(
                        "F-C2",
                        "ISSUE-CONFLICT",
                        severity="info",
                        title="Different conflict wording",
                    ),
                    _finding("F-K2", "ISSUE-KEY-2", title="Same signature"),
                ],
            },
            {
                "reviewer_id": "R-A",
                "verdict": "findings_present",
                "summary": "First report.",
                "findings": [
                    _finding("F-S", "ISSUE-SINGLE", title="Single issue"),
                    _finding("F-M1", "ISSUE-MATCH", title="Matching issue"),
                    _finding("F-C1", "ISSUE-CONFLICT", title="Conflict wording"),
                    _finding("F-K1", "ISSUE-KEY-1", title="Same signature"),
                ],
            },
            {
                "reviewer_id": "R-C",
                "verdict": "insufficient_evidence",
                "summary": "Evidence is insufficient.",
                "findings": [],
            },
            {
                "reviewer_id": "R-E",
                "verdict": "findings_present",
                "summary": "Duplicated report.",
                "findings": [duplicate_finding],
            },
            {
                "reviewer_id": "R-D",
                "verdict": "findings_present",
                "summary": "Duplicated report.",
                "findings": [duplicate_finding],
            },
        ],
    }


def _organize(review, results=None):
    material = _prepare(review)
    supplied = (
        _organization_results(material["material_package_sha256"])
        if results is None
        else results
    )
    validated = review.validate_results(material, _canonical(supplied))
    return material, review.organize_results(material, validated)


def test_organizes_every_issue_and_preserves_every_human_decision():
    review = _review()
    material, actual = _organize(review)

    assert set(actual) == {
        "status",
        "schema_version",
        "decision_status",
        "material",
        "result_set_sha256",
        "reviews",
        "counts",
        "issue_groups",
        "possible_duplicate_reviews",
        "possible_duplicate_keys",
        "insufficient_evidence_reviewers",
        "unresolved_issue_keys",
        "human_decision_queue",
        "grouping_basis",
        "semantic_deduplication_performed",
        "external_send_approved",
    }
    assert actual["status"] == "results_organized"
    assert actual["decision_status"] == "pending_human_decision"
    assert actual["external_send_approved"] is False
    assert actual["semantic_deduplication_performed"] is False
    assert actual["material"] == {
        "identifier": material["material"]["identifier"],
        "content_sha256": material["material"]["content_sha256"],
        "material_package_sha256": material["material_package_sha256"],
    }
    assert actual["counts"] == {
        "review_count": 5,
        "finding_count": 9,
        "issue_count": 6,
    }
    dispositions = {
        group["issue_key"]: group["disposition"]
        for group in actual["issue_groups"]
    }
    assert dispositions == {
        "ISSUE-CONFLICT": "conflict",
        "ISSUE-DUP": "single_report",
        "ISSUE-KEY-1": "single_report",
        "ISSUE-KEY-2": "single_report",
        "ISSUE-MATCH": "matching_reports",
        "ISSUE-SINGLE": "single_report",
    }
    assert actual["insufficient_evidence_reviewers"] == ["R-C"]
    assert actual["unresolved_issue_keys"] == [
        "ISSUE-CONFLICT",
        "ISSUE-DUP",
        "ISSUE-KEY-1",
        "ISSUE-KEY-2",
        "ISSUE-SINGLE",
    ]
    assert [item["reviewer_id"] for item in actual["reviews"]] == [
        "R-A", "R-B", "R-C", "R-D", "R-E",
    ]
    assert "content" not in actual["material"]


def test_duplicate_reviews_are_flagged_and_not_counted_as_matching_evidence():
    review = _review()
    _, actual = _organize(review)

    assert len(actual["possible_duplicate_reviews"]) == 1
    assert actual["possible_duplicate_reviews"][0]["reviewer_ids"] == ["R-D", "R-E"]
    duplicate_group = next(
        item for item in actual["issue_groups"] if item["issue_key"] == "ISSUE-DUP"
    )
    assert duplicate_group["reporters"] == ["R-D", "R-E"]
    assert duplicate_group["disposition"] == "single_report"


def test_matching_and_duplicate_candidates_all_remain_in_the_human_queue():
    review = _review()
    _, actual = _organize(review)

    kinds = [item["kind"] for item in actual["human_decision_queue"]]
    assert kinds == sorted(
        kinds,
        key=(
            "insufficient_evidence",
            "conflict",
            "possible_duplicate_review",
            "possible_duplicate_key",
            "single_report",
            "matching_reports",
        ).index,
    )
    assert set(kinds) == {
        "insufficient_evidence",
        "conflict",
        "possible_duplicate_review",
        "possible_duplicate_key",
        "single_report",
        "matching_reports",
    }
    assert any(
        item["kind"] == "matching_reports"
        and item["identifiers"] == ["ISSUE-MATCH"]
        for item in actual["human_decision_queue"]
    )


def test_organization_is_independent_of_all_set_like_input_order():
    review = _review()
    material = _prepare(review)
    first = _organization_results(material["material_package_sha256"])
    second = json.loads(json.dumps(first))
    second["reviews"].reverse()
    for item in second["reviews"]:
        item["findings"].reverse()
        for finding in item["findings"]:
            finding["criterion_ids"].reverse()

    first_validated = review.validate_results(material, _canonical(first))
    second_validated = review.validate_results(material, _canonical(second))

    assert review.organize_results(material, first_validated) == review.organize_results(
        material,
        second_validated,
    )
