"""一件の設計・受入条件照合に関する製品試験。"""

import copy
import hashlib
import importlib
import json

import pytest


def _module():
    return importlib.import_module("tools.design.one_design_acceptance")


def _json_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _design(facts=None, **overrides):
    value = {
        "schema_version": 1,
        "design_identifier": "DESIGN-ONE",
        "facts": facts if facts is not None else [
            {"fact_id": "F-MODE", "subject": "mode", "value": "safe"},
        ],
    }
    value.update(overrides)
    return value


def _acceptance(conditions=None, **overrides):
    value = {
        "schema_version": 1,
        "acceptance_identifier": "ACCEPTANCE-ONE",
        "conditions": conditions if conditions is not None else [
            {
                "condition_id": "C-MODE",
                "subject": "mode",
                "operator": "equals",
                "expected": "safe",
            },
        ],
    }
    value.update(overrides)
    return value


def _compare(design=None, acceptance=None):
    module = _module()
    return module.compare_inputs(
        _json_bytes(_design() if design is None else design),
        _json_bytes(_acceptance() if acceptance is None else acceptance),
    )


@pytest.mark.parametrize(
    ("operator", "actual", "expected", "disposition"),
    (
        ("equals", "safe", "safe", "satisfied"),
        ("equals", "fast", "safe", "contradicted"),
        ("equals", 1, True, "contradicted"),
        ("not_equals", "fast", "safe", "satisfied"),
        ("not_equals", "safe", "safe", "contradicted"),
        ("contains_all", ["a", "b"], ["b"], "satisfied"),
        ("contains_all", ["a"], ["a", "b"], "contradicted"),
        ("contains_all", "a", ["a"], "contradicted"),
        ("contains_none", ["a"], ["b"], "satisfied"),
        ("contains_none", ["a", "b"], ["b"], "contradicted"),
        ("contains_none", "a", ["b"], "contradicted"),
    ),
)
def test_applies_each_fixed_comparison(
    operator,
    actual,
    expected,
    disposition,
):
    result = _compare(
        _design([{"fact_id": "F-X", "subject": "x", "value": actual}]),
        _acceptance([
            {
                "condition_id": "C-X",
                "subject": "x",
                "operator": operator,
                "expected": expected,
            },
        ]),
    )

    assert result["results"][0]["disposition"] == disposition


def test_distinguishes_missing_and_unreferenced_facts():
    result = _compare(
        _design([
            {"fact_id": "F-USED", "subject": "used", "value": True},
            {"fact_id": "F-EXTRA", "subject": "extra", "value": 3},
        ]),
        _acceptance([
            {
                "condition_id": "C-MISSING",
                "subject": "missing",
                "operator": "equals",
                "expected": True,
            },
            {
                "condition_id": "C-USED",
                "subject": "used",
                "operator": "equals",
                "expected": True,
            },
        ]),
    )

    by_id = {item["condition_id"]: item for item in result["results"]}
    assert by_id["C-MISSING"]["disposition"] == "missing"
    assert by_id["C-MISSING"]["fact_id"] is None
    assert by_id["C-MISSING"]["actual_value_sha256"] is None
    assert result["unreferenced_fact_ids"] == ["F-EXTRA"]
    assert result["counts"] == {
        "contradicted": 0,
        "missing": 1,
        "satisfied": 1,
        "unreferenced_fact": 1,
    }


def test_keeps_all_conditions_for_human_when_everything_matches():
    result = _compare()

    assert result["verdict"] == "conditions_met_pending_human_decision"
    assert result["decision_status"] == "pending_human_decision"
    assert result["human_decision_queue"] == [
        {"identifiers": ["C-MODE"], "kind": "satisfied"},
    ]
    assert result["external_send_approved"] is False


def test_orders_the_human_queue_by_fixed_kind_order():
    result = _compare(
        _design([
            {"fact_id": "F-A", "subject": "a", "value": 1},
            {"fact_id": "F-B", "subject": "b", "value": 2},
            {"fact_id": "F-D", "subject": "d", "value": 4},
        ]),
        _acceptance([
            {
                "condition_id": "C-A",
                "subject": "a",
                "operator": "equals",
                "expected": 9,
            },
            {
                "condition_id": "C-B",
                "subject": "b",
                "operator": "equals",
                "expected": 2,
            },
            {
                "condition_id": "C-C",
                "subject": "c",
                "operator": "equals",
                "expected": 3,
            },
        ]),
    )

    assert [item["kind"] for item in result["human_decision_queue"]] == [
        "contradicted",
        "missing",
        "satisfied",
        "unreferenced_fact",
    ]


def test_returns_only_the_fixed_normal_result_shape():
    result = _compare()

    assert set(result) == {
        "acceptance",
        "comparison_sha256",
        "counts",
        "decision_status",
        "design",
        "external_send_approved",
        "human_decision_queue",
        "results",
        "schema_version",
        "status",
        "unreferenced_fact_ids",
        "verdict",
    }
    assert set(result["design"]) == {"fact_count", "identifier", "sha256"}
    assert set(result["acceptance"]) == {
        "condition_count",
        "identifier",
        "sha256",
    }
    assert set(result["results"][0]) == {
        "actual_value_sha256",
        "condition_id",
        "disposition",
        "expected_value_sha256",
        "fact_id",
        "operator",
        "subject",
    }
    assert result["status"] == "comparison_completed"
    assert result["schema_version"] == 1


def test_does_not_return_input_values():
    secret_actual = "private-design-value"
    secret_expected = "private-acceptance-value"
    result = _compare(
        _design([{"fact_id": "F-X", "subject": "x", "value": secret_actual}]),
        _acceptance([
            {
                "condition_id": "C-X",
                "subject": "x",
                "operator": "equals",
                "expected": secret_expected,
            },
        ]),
    )
    encoded = _json_bytes(result)

    assert secret_actual.encode() not in encoded
    assert secret_expected.encode() not in encoded


def test_hashes_match_the_normalized_documents_and_result():
    module = _module()
    result = _compare()
    without_self = dict(result)
    comparison_sha256 = without_self.pop("comparison_sha256")

    assert comparison_sha256 == hashlib.sha256(
        module.canonical_json_bytes(without_self)
    ).hexdigest()
    assert len(result["design"]["sha256"]) == 64
    assert len(result["acceptance"]["sha256"]) == 64
    assert len(result["results"][0]["actual_value_sha256"]) == 64
    assert len(result["results"][0]["expected_value_sha256"]) == 64


def test_ignores_object_array_and_string_set_order():
    module = _module()
    first_design = _design([
        {"fact_id": "F-B", "subject": "b", "value": ["z", "a"]},
        {"fact_id": "F-A", "subject": "a", "value": True},
    ])
    first_acceptance = _acceptance([
        {
            "condition_id": "C-B",
            "subject": "b",
            "operator": "contains_all",
            "expected": ["z", "a"],
        },
        {
            "condition_id": "C-A",
            "subject": "a",
            "operator": "equals",
            "expected": True,
        },
    ])
    second_design = copy.deepcopy(first_design)
    second_design["facts"].reverse()
    second_design["facts"][1]["value"].reverse()
    second_acceptance = copy.deepcopy(first_acceptance)
    second_acceptance["conditions"].reverse()
    second_acceptance["conditions"][1]["expected"].reverse()

    first = _compare(first_design, first_acceptance)
    second = _compare(second_design, second_acceptance)

    assert first == second
    assert module.canonical_json_bytes(first) == module.canonical_json_bytes(second)


def test_one_value_change_changes_all_dependent_hashes():
    first = _compare()
    second_design = _design()
    second_design["facts"][0]["value"] = "changed"
    second = _compare(second_design, _acceptance())

    assert first["design"]["sha256"] != second["design"]["sha256"]
    assert (
        first["results"][0]["actual_value_sha256"]
        != second["results"][0]["actual_value_sha256"]
    )
    assert first["comparison_sha256"] != second["comparison_sha256"]


@pytest.mark.parametrize(
    ("raw", "source"),
    (
        (
            b'{"schema_version":999,"schema_version":1,'
            b'"design_identifier":"D","facts":[]}',
            "design",
        ),
        (
            b'{"schema_version":1,"design_identifier":"D","facts":['
            b'{"fact_id":"F","subject":"x","value":1,"value":2}]}',
            "design",
        ),
        (
            b'{"schema_version":1,"acceptance_identifier":"A",'
            b'"conditions":[{"condition_id":"C","subject":"x",'
            b'"\\u0073ubject":"y","operator":"equals","expected":1}]}',
            "acceptance",
        ),
    ),
)
def test_rejects_duplicate_json_members_before_normalization(raw, source):
    module = _module()
    design_bytes = _json_bytes(_design())
    acceptance_bytes = _json_bytes(_acceptance())
    if source == "design":
        design_bytes = raw
    else:
        acceptance_bytes = raw

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        module.compare_inputs(design_bytes, acceptance_bytes)

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == source


@pytest.mark.parametrize(
    ("design", "acceptance", "source"),
    (
        (_design(extra=True), _acceptance(), "design"),
        (_design(facts=[]), _acceptance(), "design"),
        (
            _design([
                {"fact_id": "F-1", "subject": "x", "value": 1},
                {"fact_id": "F-2", "subject": "x", "value": 2},
            ]),
            _acceptance(),
            "design",
        ),
        (
            _design([{"fact_id": "F-1", "subject": "x", "value": None}]),
            _acceptance(),
            "design",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "equals",
                    "expected": 1,
                },
                {
                    "condition_id": "C-2",
                    "subject": "x",
                    "operator": "equals",
                    "expected": 2,
                },
            ]),
            "acceptance",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "unknown",
                    "expected": 1,
                },
            ]),
            "acceptance",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "contains_all",
                    "expected": "not-an-array",
                },
            ]),
            "acceptance",
        ),
    ),
)
def test_rejects_invalid_closed_schemas(design, acceptance, source):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(design, acceptance)

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == source


@pytest.mark.parametrize(
    "bad_identifier",
    ("", "starts with space", "/absolute", "a" * 129),
)
def test_rejects_invalid_safe_identifiers(bad_identifier):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(_design(design_identifier=bad_identifier), _acceptance())

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == "design"


@pytest.mark.parametrize(
    "bad_value",
    (
        1.5,
        {},
        [["nested"]],
        [],
        ["duplicate", "duplicate"],
        9007199254740992,
        "",
        "nul\x00value",
    ),
)
def test_rejects_forbidden_value_types_and_bounds(bad_value):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(
            _design([{"fact_id": "F-X", "subject": "x", "value": bad_value}]),
            _acceptance(),
        )

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == "design"


def test_rejects_more_than_256_facts_or_conditions():
    module = _module()
    facts = [
        {"fact_id": f"F-{index}", "subject": f"s-{index}", "value": index}
        for index in range(257)
    ]
    conditions = [
        {
            "condition_id": f"C-{index}",
            "subject": f"s-{index}",
            "operator": "equals",
            "expected": index,
        }
        for index in range(257)
    ]

    with pytest.raises(module.DesignAcceptanceStop):
        _compare(_design(facts), _acceptance())
    with pytest.raises(module.DesignAcceptanceStop):
        _compare(_design(), _acceptance(conditions))


def test_rejects_non_bytes_and_invalid_utf8_inputs():
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as non_bytes:
        module.compare_inputs("not-bytes", _json_bytes(_acceptance()))
    assert non_bytes.value.reason == "invalid_schema"
    assert non_bytes.value.source == "design"

    with pytest.raises(module.DesignAcceptanceStop) as invalid_utf8:
        module.compare_inputs(b"\xff", _json_bytes(_acceptance()))
    assert invalid_utf8.value.reason == "invalid_utf8"
    assert invalid_utf8.value.source == "design"
