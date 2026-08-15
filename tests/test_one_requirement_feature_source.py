"""一件の要求候補整合検査に関する製品試験。"""

import copy
import hashlib
import importlib
import io
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest


_REDACTION_PATH = Path("tools/session_logs/redaction.py")
_REDACTION_SHA256 = (
    "aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd"
)
_SEVEN_LISTS = (
    "inputs",
    "outputs",
    "stop_conditions",
    "recovery_conditions",
    "preserved_artifacts",
    "acceptance_criteria",
    "non_goals",
)
_LIMITATIONS = [
    "source_status_not_verified",
    "semantic_correctness_not_verified",
    "multi_requirement_partition_not_verified",
    "authority_not_changed",
    "sensitive_detection_not_exhaustive",
]

_SRC_A_SHA = hashlib.sha256(b"source-a").hexdigest()
_SRC_B_SHA = hashlib.sha256(b"source-b").hexdigest()
_SRC_C_SHA = hashlib.sha256(b"source-c").hexdigest()
_AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"


def _core():
    return importlib.import_module(
        "tools.requirements.one_requirement_feature_source"
    )


def _entry():
    return importlib.import_module(
        "tools.requirements.one_requirement_feature_source_entry"
    )


def _input_bytes(value):
    return json.dumps(value).encode("utf-8")


def _canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _catalog(sources=None, **overrides):
    value = {
        "schema_version": 1,
        "catalog_identifier": "CAT-G24-ONE",
        "sources": sources if sources is not None else [
            {
                "source_id": "SRC-B",
                "sha256": _SRC_B_SHA,
                "declared_status": "candidate",
            },
            {
                "source_id": "SRC-A",
                "sha256": _SRC_A_SHA,
                "declared_status": "effective",
            },
            {
                "source_id": "SRC-C",
                "sha256": _SRC_C_SHA,
                "declared_status": "historical",
            },
        ],
    }
    value.update(overrides)
    return value


def _obligation_ids(requirement_id="REQ-CHECK-001", lists=None):
    identifiers = [f"{requirement_id}#statement"]
    for field in _SEVEN_LISTS:
        count = 1 if lists is None else lists[field]
        for index in range(1, count + 1):
            identifiers.append(f"{requirement_id}#{field}.{index:03d}")
    return identifiers


def _candidate(**overrides):
    value = {
        "schema_version": 1,
        "candidate_identifier": "RC-CAND-001",
        "feature": {
            "feature_id": "FEAT-REQCHECK",
            "name": "整合検査",
            "responsibility": "候補一件の整合を検査する",
            "non_goals": ["要求文の作成"],
        },
        "requirement": {
            "requirement_id": "REQ-CHECK-001",
            "feature_id": "FEAT-REQCHECK",
            "statement": "候補一件を決定的に検査する。",
            "inputs": ["出典一覧一件"],
            "outputs": ["正準JSON一件"],
            "stop_conditions": ["機微情報候補の検出"],
            "recovery_conditions": ["入力の修正"],
            "preserved_artifacts": ["既存の成果物"],
            "acceptance_criteria": ["全出典に採否がある"],
            "non_goals": ["意味の推測"],
        },
        "source_dispositions": [
            {
                "source_id": "SRC-A",
                "disposition": "selected",
                "rationale": "根拠資料",
            },
            {
                "source_id": "SRC-B",
                "disposition": "not_selected",
                "rationale": "対象外",
            },
            {
                "source_id": "SRC-C",
                "disposition": "not_selected",
                "rationale": "履歴資料",
            },
        ],
        "obligation_sources": [
            {"obligation_id": identifier, "source_ids": ["SRC-A"]}
            for identifier in _obligation_ids()
        ],
    }
    value.update(overrides)
    return value


def _check(catalog=None, candidate=None):
    module = _core()
    return module.check_inputs(
        _input_bytes(_catalog() if catalog is None else catalog),
        _input_bytes(_candidate() if candidate is None else candidate),
    )


def _stop(catalog=None, candidate=None, catalog_bytes=None, candidate_bytes=None):
    module = _core()
    selected_catalog = (
        catalog_bytes
        if catalog_bytes is not None
        else _input_bytes(_catalog() if catalog is None else catalog)
    )
    selected_candidate = (
        candidate_bytes
        if candidate_bytes is not None
        else _input_bytes(_candidate() if candidate is None else candidate)
    )
    with pytest.raises(module.RequirementCandidateStop) as info:
        module.check_inputs(selected_catalog, selected_candidate)
    return info.value


def _normalized_dispositions(candidate):
    return sorted(
        (
            {
                "source_id": item["source_id"],
                "disposition": item["disposition"],
                "rationale": item["rationale"],
            }
            for item in candidate["source_dispositions"]
        ),
        key=lambda item: item["source_id"],
    )


def _normalized_obligations(candidate):
    return sorted(
        (
            {
                "obligation_id": item["obligation_id"],
                "source_ids": sorted(item["source_ids"]),
            }
            for item in candidate["obligation_sources"]
        ),
        key=lambda item: item["obligation_id"],
    )


def _expected_result(catalog=None, candidate=None):
    catalog = _catalog() if catalog is None else catalog
    candidate = _candidate() if candidate is None else candidate
    sources = sorted(catalog["sources"], key=lambda item: item["source_id"])
    normalized_catalog = {
        "schema_version": 1,
        "catalog_identifier": catalog["catalog_identifier"],
        "sources": sources,
    }
    dispositions = _normalized_dispositions(candidate)
    obligations = _normalized_obligations(candidate)
    normalized_candidate = {
        "schema_version": 1,
        "candidate_identifier": candidate["candidate_identifier"],
        "feature": candidate["feature"],
        "requirement": candidate["requirement"],
        "source_dispositions": dispositions,
        "obligation_sources": obligations,
    }
    trace = {
        "schema_version": 1,
        "source_dispositions": dispositions,
        "obligation_sources": obligations,
    }
    status_by_source = {
        item["source_id"]: item["declared_status"] for item in sources
    }
    disposition_by_source = {
        item["source_id"]: item["disposition"] for item in dispositions
    }
    counts = {
        "approved_context_sources": sum(
            1 for item in sources if item["declared_status"] == "approved_context"
        ),
        "candidate_sources": sum(
            1 for item in sources if item["declared_status"] == "candidate"
        ),
        "effective_sources": sum(
            1 for item in sources if item["declared_status"] == "effective"
        ),
        "historical_sources": sum(
            1 for item in sources if item["declared_status"] == "historical"
        ),
        "not_selected_sources": sum(
            1
            for item in dispositions
            if item["disposition"] == "not_selected"
        ),
        "selected_sources": sum(
            1 for item in dispositions if item["disposition"] == "selected"
        ),
        "traced_obligations": len(obligations),
    }
    selected_candidates = sorted(
        item["source_id"]
        for item in dispositions
        if item["disposition"] == "selected"
        and status_by_source[item["source_id"]] == "candidate"
    )
    selected_historicals = sorted(
        item["source_id"]
        for item in dispositions
        if item["disposition"] == "selected"
        and status_by_source[item["source_id"]] == "historical"
    )
    queue = [
        {
            "identifiers": [candidate["candidate_identifier"]],
            "kind": "requirement_candidate",
        },
    ]
    if selected_candidates:
        queue.append(
            {
                "identifiers": selected_candidates,
                "kind": "candidate_source_selection",
            },
        )
    if selected_historicals:
        queue.append(
            {
                "identifiers": selected_historicals,
                "kind": "historical_source_selection",
            },
        )
    result = {
        "status": "requirement_candidate_checked",
        "schema_version": 1,
        "decision_status": "pending_human_decision",
        "promotion_status": "not_promoted",
        "verdict": (
            "review_required_pending_human_decision"
            if selected_candidates or selected_historicals
            else "trace_complete_pending_human_decision"
        ),
        "catalog": {
            "identifier": catalog["catalog_identifier"],
            "sha256": _sha(normalized_catalog),
            "source_count": len(sources),
        },
        "candidate": {
            "identifier": candidate["candidate_identifier"],
            "sha256": _sha(normalized_candidate),
        },
        "feature": {
            "identifier": candidate["feature"]["feature_id"],
            "sha256": _sha(candidate["feature"]),
        },
        "requirement": {
            "identifier": candidate["requirement"]["requirement_id"],
            "sha256": _sha(candidate["requirement"]),
            "obligation_count": len(obligations),
        },
        "counts": counts,
        "source_dispositions": [
            {
                "source_id": item["source_id"],
                "declared_status": status_by_source[item["source_id"]],
                "disposition": disposition_by_source[item["source_id"]],
            }
            for item in dispositions
        ],
        "obligation_sources": obligations,
        "trace_sha256": _sha(trace),
        "human_decision_queue": queue,
        "limitations": list(_LIMITATIONS),
        "external_send_approved": False,
    }
    result["result_sha256"] = _sha(result)
    return result


# ---------------------------------------------------------------------------
# 受入条件1・7・22：正例の完全一致
# ---------------------------------------------------------------------------


def test_positive_example_returns_exact_full_result():
    assert _check() == _expected_result()


def test_positive_example_counts_and_verdict():
    result = _check()

    assert result["counts"] == {
        "approved_context_sources": 0,
        "candidate_sources": 1,
        "effective_sources": 1,
        "historical_sources": 1,
        "not_selected_sources": 2,
        "selected_sources": 1,
        "traced_obligations": 8,
    }
    assert result["verdict"] == "trace_complete_pending_human_decision"
    assert result["requirement"]["obligation_count"] == 8
    assert result["catalog"]["source_count"] == 3


def test_positive_example_lists_every_disposition_and_obligation():
    result = _check()

    assert [item["source_id"] for item in result["source_dispositions"]] == [
        "SRC-A",
        "SRC-B",
        "SRC-C",
    ]
    assert [item["obligation_id"] for item in result["obligation_sources"]] == (
        sorted(_obligation_ids())
    )
    assert all(
        item["source_ids"] == ["SRC-A"]
        for item in result["obligation_sources"]
    )


def test_positive_example_excludes_free_text_and_source_sha256():
    result = _check()
    rendered = _canonical(result).decode("utf-8")

    assert "根拠資料" not in rendered
    assert "候補一件を決定的に検査する。" not in rendered
    assert _SRC_A_SHA not in rendered


# ---------------------------------------------------------------------------
# 受入条件5・6：未昇格と人の判断一覧
# ---------------------------------------------------------------------------


def test_full_trace_does_not_promote():
    result = _check()

    assert result["decision_status"] == "pending_human_decision"
    assert result["promotion_status"] == "not_promoted"
    assert result["limitations"] == _LIMITATIONS
    assert result["external_send_approved"] is False
    assert result["human_decision_queue"] == [
        {"identifiers": ["RC-CAND-001"], "kind": "requirement_candidate"},
    ]


def test_selected_candidate_and_historical_enter_queue_in_fixed_order():
    candidate = _candidate()
    for item in candidate["source_dispositions"]:
        item["disposition"] = "selected"
    obligations = candidate["obligation_sources"]
    obligations[0]["source_ids"] = ["SRC-C", "SRC-B", "SRC-A"]

    result = _check(candidate=candidate)

    assert [item["kind"] for item in result["human_decision_queue"]] == [
        "requirement_candidate",
        "candidate_source_selection",
        "historical_source_selection",
    ]
    assert result["human_decision_queue"][1]["identifiers"] == ["SRC-B"]
    assert result["human_decision_queue"][2]["identifiers"] == ["SRC-C"]
    assert result["verdict"] == "review_required_pending_human_decision"
    assert result["obligation_sources"][0]["source_ids"] == [
        "SRC-A",
        "SRC-B",
        "SRC-C",
    ]
    assert result["promotion_status"] == "not_promoted"


# ---------------------------------------------------------------------------
# 受入条件2・3：採否と義務対応の停止
# ---------------------------------------------------------------------------


def test_missing_disposition_stops_incomplete_coverage():
    candidate = _candidate()
    del candidate["source_dispositions"][2]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("incomplete_coverage", "candidate")


def test_duplicate_disposition_stops_incomplete_coverage():
    candidate = _candidate()
    candidate["source_dispositions"][1] = {
        "source_id": "SRC-A",
        "disposition": "selected",
        "rationale": "重複",
    }

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("incomplete_coverage", "candidate")


def test_unknown_disposition_source_stops_unresolved_reference():
    candidate = _candidate()
    candidate["source_dispositions"].append(
        {
            "source_id": "SRC-X",
            "disposition": "not_selected",
            "rationale": "未知",
        },
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


def test_empty_rationale_stops_invalid_schema():
    candidate = _candidate()
    candidate["source_dispositions"][0]["rationale"] = ""

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_missing_obligation_stops_incomplete_coverage():
    candidate = _candidate()
    del candidate["obligation_sources"][0]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("incomplete_coverage", "candidate")


def test_duplicate_obligation_stops_incomplete_coverage():
    candidate = _candidate()
    candidate["obligation_sources"].append(
        copy.deepcopy(candidate["obligation_sources"][0]),
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("incomplete_coverage", "candidate")


def test_unknown_obligation_stops_unresolved_reference():
    candidate = _candidate()
    candidate["obligation_sources"][0]["obligation_id"] = (
        "REQ-CHECK-001#bogus.001"
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


def test_empty_source_ids_stops_invalid_schema():
    candidate = _candidate()
    candidate["obligation_sources"][0]["source_ids"] = []

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_duplicate_source_ids_stop_invalid_schema():
    candidate = _candidate()
    candidate["obligation_sources"][0]["source_ids"] = ["SRC-A", "SRC-A"]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_not_selected_reference_stops_unresolved_reference():
    candidate = _candidate()
    candidate["obligation_sources"][0]["source_ids"] = ["SRC-B"]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


def test_unknown_obligation_source_stops_unresolved_reference():
    candidate = _candidate()
    candidate["obligation_sources"][0]["source_ids"] = ["SRC-X"]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


def test_unconsumed_selected_source_stops_incomplete_coverage():
    candidate = _candidate()
    candidate["source_dispositions"][1]["disposition"] = "selected"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("incomplete_coverage", "candidate")


def test_feature_id_mismatch_stops_unresolved_reference():
    candidate = _candidate()
    candidate["requirement"]["feature_id"] = "FEAT-OTHER"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


def test_reference_stage_precedes_coverage_stage():
    candidate = _candidate()
    candidate["obligation_sources"][0]["source_ids"] = ["SRC-X"]
    del candidate["obligation_sources"][1]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("unresolved_reference", "candidate")


# ---------------------------------------------------------------------------
# 受入条件4：一覧と件数境界
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("field", _SEVEN_LISTS)
def test_missing_list_stops_invalid_schema(field):
    candidate = _candidate()
    del candidate["requirement"][field]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


@pytest.mark.parametrize("field", _SEVEN_LISTS)
def test_empty_list_stops_invalid_schema(field):
    candidate = _candidate()
    candidate["requirement"][field] = []

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_duplicate_list_item_stops_invalid_schema():
    candidate = _candidate()
    candidate["requirement"]["inputs"] = ["同じ値", "同じ値"]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_oversized_list_stops_invalid_schema():
    candidate = _candidate()
    candidate["requirement"]["inputs"] = [
        f"入力項目{index}" for index in range(33)
    ]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_maximum_obligations_pass():
    candidate = _candidate()
    lists = {field: 32 for field in _SEVEN_LISTS}
    candidate["feature"]["non_goals"] = [f"目的外{index}" for index in range(32)]
    for field in _SEVEN_LISTS:
        candidate["requirement"][field] = [
            f"{field}項目{index}" for index in range(32)
        ]
    candidate["obligation_sources"] = [
        {"obligation_id": identifier, "source_ids": ["SRC-A"]}
        for identifier in _obligation_ids(lists=lists)
    ]

    result = _check(candidate=candidate)

    assert result["requirement"]["obligation_count"] == 225
    assert result["counts"]["traced_obligations"] == 225


def test_source_count_boundaries():
    sources = [
        {
            "source_id": f"SRC-{index:03d}",
            "sha256": hashlib.sha256(f"source-{index}".encode()).hexdigest(),
            "declared_status": "effective",
        }
        for index in range(256)
    ]
    catalog = _catalog(sources=sources)
    candidate = _candidate()
    candidate["source_dispositions"] = [
        {
            "source_id": f"SRC-{index:03d}",
            "disposition": "selected" if index == 0 else "not_selected",
            "rationale": f"理由{index}",
        }
        for index in range(256)
    ]
    for item in candidate["obligation_sources"]:
        item["source_ids"] = ["SRC-000"]

    result = _check(catalog=catalog, candidate=candidate)

    assert result["catalog"]["source_count"] == 256
    assert result["counts"]["effective_sources"] == 256

    oversized = _catalog(sources=sources + [
        {
            "source_id": "SRC-256",
            "sha256": hashlib.sha256(b"source-256").hexdigest(),
            "declared_status": "effective",
        },
    ])
    stop = _stop(catalog=oversized, candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_empty_sources_stop_invalid_schema():
    stop = _stop(catalog=_catalog(sources=[]))

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


# ---------------------------------------------------------------------------
# 受入条件8：表現順だけの差は結果を変えない
# ---------------------------------------------------------------------------


def test_object_member_order_does_not_change_bytes():
    module = _core()
    catalog = _catalog()
    reordered = {key: catalog[key] for key in reversed(list(catalog))}
    baseline = module.check_inputs(
        _input_bytes(catalog),
        _input_bytes(_candidate()),
    )
    variant = module.check_inputs(
        _input_bytes(reordered),
        _input_bytes(_candidate()),
    )

    assert _canonical(baseline) == _canonical(variant)


def test_source_and_mapping_order_does_not_change_result():
    catalog = _catalog()
    catalog["sources"].reverse()
    candidate = _candidate()
    candidate["source_dispositions"].reverse()
    candidate["obligation_sources"].reverse()

    assert _check(catalog=catalog, candidate=candidate) == _expected_result()


def test_source_ids_order_does_not_change_result():
    candidate = _candidate()
    for item in candidate["source_dispositions"]:
        item["disposition"] = "selected"
    candidate["obligation_sources"][0]["source_ids"] = [
        "SRC-C",
        "SRC-B",
        "SRC-A",
    ]
    baseline = _check(candidate=candidate)

    variant_candidate = copy.deepcopy(candidate)
    variant_candidate["obligation_sources"][0]["source_ids"] = [
        "SRC-A",
        "SRC-C",
        "SRC-B",
    ]
    variant = _check(candidate=variant_candidate)

    assert baseline == variant


def test_list_reorder_changes_requirement_sha256():
    candidate = _candidate()
    candidate["requirement"]["inputs"] = ["入力一", "入力二"]
    candidate["obligation_sources"] = [
        {"obligation_id": identifier, "source_ids": ["SRC-A"]}
        for identifier in _obligation_ids(
            lists={
                field: (2 if field == "inputs" else 1)
                for field in _SEVEN_LISTS
            },
        )
    ]
    baseline = _check(candidate=candidate)

    variant_candidate = copy.deepcopy(candidate)
    variant_candidate["requirement"]["inputs"] = ["入力二", "入力一"]
    variant = _check(candidate=variant_candidate)

    assert (
        baseline["requirement"]["sha256"]
        != variant["requirement"]["sha256"]
    )
    assert baseline["candidate"]["sha256"] != variant["candidate"]["sha256"]


# ---------------------------------------------------------------------------
# 受入条件9・10：内容識別値の対応と独立oracle
# ---------------------------------------------------------------------------


def test_digests_match_independent_oracle():
    result = _check()
    expected = _expected_result()

    assert result["catalog"]["sha256"] == expected["catalog"]["sha256"]
    assert result["candidate"]["sha256"] == expected["candidate"]["sha256"]
    assert result["feature"]["sha256"] == expected["feature"]["sha256"]
    assert (
        result["requirement"]["sha256"] == expected["requirement"]["sha256"]
    )
    assert result["trace_sha256"] == expected["trace_sha256"]
    without_result = dict(result)
    del without_result["result_sha256"]
    assert result["result_sha256"] == _sha(without_result)


def test_statement_change_moves_requirement_digests_only():
    baseline = _check()
    candidate = _candidate()
    candidate["requirement"]["statement"] = "別の本文で検査する。"

    variant = _check(candidate=candidate)

    assert (
        variant["requirement"]["sha256"] != baseline["requirement"]["sha256"]
    )
    assert variant["candidate"]["sha256"] != baseline["candidate"]["sha256"]
    assert variant["result_sha256"] != baseline["result_sha256"]
    assert variant["catalog"]["sha256"] == baseline["catalog"]["sha256"]
    assert variant["feature"]["sha256"] == baseline["feature"]["sha256"]
    assert variant["trace_sha256"] == baseline["trace_sha256"]


def test_rationale_change_moves_trace_digest_only():
    baseline = _check()
    candidate = _candidate()
    candidate["source_dispositions"][0]["rationale"] = "別の根拠"

    variant = _check(candidate=candidate)

    assert variant["trace_sha256"] != baseline["trace_sha256"]
    assert variant["candidate"]["sha256"] != baseline["candidate"]["sha256"]
    assert variant["result_sha256"] != baseline["result_sha256"]
    assert variant["catalog"]["sha256"] == baseline["catalog"]["sha256"]
    assert variant["feature"]["sha256"] == baseline["feature"]["sha256"]
    assert (
        variant["requirement"]["sha256"] == baseline["requirement"]["sha256"]
    )


def test_source_sha256_change_moves_catalog_digest():
    baseline = _check()
    catalog = _catalog()
    catalog["sources"][0]["sha256"] = hashlib.sha256(b"changed").hexdigest()

    variant = _check(catalog=catalog)

    assert variant["catalog"]["sha256"] != baseline["catalog"]["sha256"]
    assert variant["candidate"]["sha256"] == baseline["candidate"]["sha256"]
    assert variant["trace_sha256"] == baseline["trace_sha256"]


def test_feature_name_change_moves_feature_digest():
    baseline = _check()
    candidate = _candidate()
    candidate["feature"]["name"] = "別名の機能"

    variant = _check(candidate=candidate)

    assert variant["feature"]["sha256"] != baseline["feature"]["sha256"]
    assert variant["candidate"]["sha256"] != baseline["candidate"]["sha256"]
    assert (
        variant["requirement"]["sha256"] == baseline["requirement"]["sha256"]
    )


def test_list_item_change_moves_requirement_digest():
    baseline = _check()
    candidate = _candidate()
    candidate["requirement"]["acceptance_criteria"] = ["別の受入条件"]

    variant = _check(candidate=candidate)

    assert (
        variant["requirement"]["sha256"] != baseline["requirement"]["sha256"]
    )


# ---------------------------------------------------------------------------
# 受入条件11：構文・型・文字の防御
# ---------------------------------------------------------------------------


def test_duplicate_member_stops_invalid_schema():
    raw = (
        b'{"schema_version":1,"schema_version":1,'
        b'"catalog_identifier":"CAT-G24-ONE","sources":[]}'
    )

    stop = _stop(catalog_bytes=raw)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_escaped_duplicate_member_stops_invalid_schema():
    raw = (
        '{"schema_version":1,"catalog_identifier":"CAT-G24-ONE",'
        '"sources":[],"a":1,"\\u0061":2}'
    ).encode("utf-8")

    stop = _stop(catalog_bytes=raw)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_json_syntax_error_stops_invalid_schema():
    stop = _stop(candidate_bytes=b"{not json")

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


@pytest.mark.parametrize("version", (True, 2, 1.0, "1"))
def test_schema_version_variants_stop_invalid_schema(version):
    catalog = _catalog()
    catalog["schema_version"] = version

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_unknown_root_member_stops_invalid_schema():
    catalog = _catalog()
    catalog["extra_member"] = "harmless"

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_null_value_stops_invalid_schema():
    candidate = _candidate()
    candidate["feature"]["name"] = None

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_nested_array_stops_invalid_schema():
    candidate = _candidate()
    candidate["requirement"]["inputs"] = [["入れ子"]]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_lone_surrogate_stops_invalid_schema():
    candidate = _candidate()
    candidate["requirement"]["statement"] = "\ud800不正な文字"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


@pytest.mark.parametrize(
    "identifier",
    ("FEAT-lower", "REQ-CHECK-01", "白い空白 id", "-lead", ""),
)
def test_invalid_identifiers_stop_invalid_schema(identifier):
    candidate = _candidate()
    candidate["feature"]["feature_id"] = identifier
    candidate["requirement"]["feature_id"] = identifier

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_requirement_id_needs_three_digit_suffix():
    candidate = _candidate()
    candidate["requirement"]["requirement_id"] = "REQ-CHECK-01"
    candidate["obligation_sources"] = [
        {"obligation_id": identifier, "source_ids": ["SRC-A"]}
        for identifier in _obligation_ids(requirement_id="REQ-CHECK-01")
    ]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


@pytest.mark.parametrize(
    "digest",
    (
        "A" * 64,
        "a" * 63,
        "a" * 65,
        "not-a-digest",
    ),
)
def test_invalid_source_sha256_stops_invalid_schema(digest):
    catalog = _catalog()
    catalog["sources"][0]["sha256"] = digest

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_invalid_declared_status_stops_invalid_schema():
    catalog = _catalog()
    catalog["sources"][0]["declared_status"] = "unknown"

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")


def test_invalid_disposition_stops_invalid_schema():
    candidate = _candidate()
    candidate["source_dispositions"][0]["disposition"] = "maybe"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_free_text_length_limits():
    candidate = _candidate()
    candidate["requirement"]["statement"] = "あ" * 2001

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")

    candidate = _candidate()
    candidate["requirement"]["inputs"] = ["い" * 501]
    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


def test_nul_character_stops_invalid_schema():
    candidate = _candidate()
    candidate["requirement"]["statement"] = "前\x00後"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "candidate")


# ---------------------------------------------------------------------------
# 受入条件12：機微情報候補の停止
# ---------------------------------------------------------------------------


def test_aws_key_in_source_id_stops_sensitive():
    catalog = _catalog()
    catalog["sources"][0]["source_id"] = _AWS_KEY

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "catalog",
    )


def test_email_in_rationale_stops_sensitive():
    candidate = _candidate()
    candidate["source_dispositions"][0]["rationale"] = (
        "user@example.com に確認した"
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_bearer_token_in_statement_stops_sensitive():
    candidate = _candidate()
    candidate["requirement"]["statement"] = (
        "Bearer abcdefabcdef012345 を使う"
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_api_key_assignment_in_list_stops_sensitive():
    candidate = _candidate()
    candidate["requirement"]["non_goals"] = [
        "api_key = abcdef123456789012",
    ]

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_private_key_block_stops_sensitive():
    candidate = _candidate()
    candidate["feature"]["responsibility"] = (
        "-----BEGIN PRIVATE KEY-----\nZm9v\n-----END PRIVATE KEY-----"
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_high_entropy_identifier_stops_sensitive():
    candidate = _candidate()
    candidate["candidate_identifier"] = hashlib.sha256(b"secret").hexdigest()

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_hex_digest_outside_sha256_member_stops_sensitive():
    candidate = _candidate()
    candidate["source_dispositions"][0]["rationale"] = (
        hashlib.sha256(b"leak").hexdigest()
    )

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_sensitive_value_under_unknown_member_stops_before_schema():
    catalog = _catalog()
    catalog["unknown_member"] = "user@example.com"

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "catalog",
    )


def test_sensitive_member_name_stops_sensitive():
    candidate = _candidate()
    candidate[_AWS_KEY] = "値"

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_catalog_checked_before_candidate():
    catalog = _catalog()
    catalog["sources"][0]["source_id"] = _AWS_KEY
    candidate = _candidate()
    candidate["candidate_identifier"] = _AWS_KEY

    stop = _stop(catalog=catalog, candidate=candidate)

    assert stop.source == "catalog"


def test_correct_sha256_member_is_not_flagged():
    result = _check()

    assert result["status"] == "requirement_candidate_checked"


def test_aws_key_in_sha256_member_still_stops():
    catalog = _catalog()
    catalog["sources"][0]["sha256"] = _AWS_KEY + "a" * 44

    stop = _stop(catalog=catalog)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "catalog",
    )


def test_stop_output_hides_sensitive_value():
    module = _core()
    catalog = _catalog()
    catalog["sources"][0]["source_id"] = _AWS_KEY

    with pytest.raises(module.RequirementCandidateStop) as info:
        module.check_inputs(_input_bytes(catalog), _input_bytes(_candidate()))

    assert _AWS_KEY not in str(info.value)
    assert _AWS_KEY not in repr(info.value.__dict__)


# ---------------------------------------------------------------------------
# 受入条件13：機微情報規則の照合
# ---------------------------------------------------------------------------


def test_redaction_module_is_pinned_before_and_after_run():
    def current_digest():
        return hashlib.sha256(_REDACTION_PATH.read_bytes()).hexdigest()

    assert current_digest() == _REDACTION_SHA256
    redaction = importlib.import_module("tools.session_logs.redaction")
    assert callable(redaction.default_pattern_rules)
    assert callable(redaction.find_high_entropy)
    assert len(redaction.default_pattern_rules()) == 5

    _check()

    assert current_digest() == _REDACTION_SHA256


def test_core_does_not_resolve_environment_rules():
    source = Path(
        "tools/requirements/one_requirement_feature_source.py"
    ).read_text(encoding="utf-8")

    assert "environment_reference_rules" not in source
    assert "resolve_environment_rules" not in source
    assert "redact_text" not in source


# ---------------------------------------------------------------------------
# 受入条件14・15・17：入口・path・停止形式
# ---------------------------------------------------------------------------


def _write_inputs(root, catalog=None, candidate=None):
    catalog_path = root / "catalog.json"
    candidate_path = root / "candidate.json"
    catalog_path.write_bytes(
        _input_bytes(_catalog() if catalog is None else catalog),
    )
    candidate_path.write_bytes(
        _input_bytes(_candidate() if candidate is None else candidate),
    )
    return catalog_path, candidate_path


def _run_entry(arguments):
    output = io.BytesIO()
    code = _entry().main(arguments, output=output)
    return code, output.getvalue()


def _entry_arguments(root, catalog_path, candidate_path):
    return [
        "check",
        "--input-root",
        str(root),
        "--catalog",
        str(catalog_path),
        "--candidate",
        str(candidate_path),
    ]


def test_entry_returns_canonical_result_bytes(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )

    assert code == 0
    assert payload == _canonical(_expected_result()) + b"\n"


def test_entry_stop_payload_is_fixed_shape(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, tmp_path / "missing.json"),
    )

    assert code == 2
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "unreadable_input",
            "source": "candidate",
            "status": "stopped",
        },
    ) + b"\n"
    assert str(tmp_path).encode() not in payload


@pytest.mark.parametrize(
    "mutate",
    (
        lambda arguments: arguments[:-1],
        lambda arguments: arguments + ["--extra", "x"],
        lambda arguments: ["verify"] + arguments[1:],
        lambda arguments: arguments[:1]
        + ["--catalog", arguments[4], "--catalog", arguments[4]]
        + arguments[5:],
    ),
)
def test_entry_rejects_malformed_arguments(tmp_path, mutate):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    arguments = mutate(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )

    code, payload = _run_entry(arguments)

    assert code == 2
    assert b'"invalid_arguments"' in payload
    assert b'"arguments"' in payload


def test_entry_rejects_relative_and_escaping_paths(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)

    code, payload = _run_entry(
        [
            "check",
            "--input-root",
            str(tmp_path),
            "--catalog",
            "catalog.json",
            "--candidate",
            str(candidate_path),
        ],
    )
    assert code == 2
    assert b'"invalid_path"' in payload

    outside = tmp_path.parent / "outside.json"
    code, payload = _run_entry(
        [
            "check",
            "--input-root",
            str(tmp_path),
            "--catalog",
            str(outside),
            "--candidate",
            str(candidate_path),
        ],
    )
    assert code == 2
    assert b'"invalid_path"' in payload

    code, payload = _run_entry(
        [
            "check",
            "--input-root",
            str(tmp_path) + "/../" + tmp_path.name,
            "--catalog",
            str(catalog_path),
            "--candidate",
            str(candidate_path),
        ],
    )
    assert code == 2
    assert b'"invalid_path"' in payload


def test_entry_rejects_same_file(tmp_path):
    catalog_path, _ = _write_inputs(tmp_path)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, catalog_path),
    )

    assert code == 2
    assert b'"invalid_path"' in payload


def test_entry_stops_on_symlink(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    link_path = tmp_path / "link.json"
    link_path.symlink_to(catalog_path)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, link_path, candidate_path),
    )

    assert code == 2
    assert b'"unreadable_input"' in payload
    assert b'"catalog"' in payload


def test_entry_stops_on_directory_input(tmp_path):
    catalog_path, _ = _write_inputs(tmp_path)
    directory = tmp_path / "not-a-file"
    directory.mkdir()

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, directory),
    )

    assert code == 2
    assert b'"unreadable_input"' in payload
    assert b'"candidate"' in payload


def test_entry_stops_on_missing_root(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)

    code, payload = _run_entry(
        [
            "check",
            "--input-root",
            str(tmp_path / "absent"),
            "--catalog",
            str(catalog_path),
            "--candidate",
            str(candidate_path),
        ],
    )

    assert code == 2
    assert b'"invalid_path"' in payload


def test_entry_stops_on_size_limit(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    catalog_path.write_bytes(b"x" * 262145)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )

    assert code == 2
    assert b'"size_limit_exceeded"' in payload
    assert b'"catalog"' in payload


def test_entry_stops_on_invalid_utf8(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    candidate_path.write_bytes(b"\xff\xfe\x00broken")

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )

    assert code == 2
    assert b'"invalid_utf8"' in payload
    assert b'"candidate"' in payload


def test_entry_returns_three_for_sensitive_stop(tmp_path):
    catalog = _catalog()
    catalog["sources"][0]["source_id"] = _AWS_KEY
    catalog_path, candidate_path = _write_inputs(tmp_path, catalog=catalog)

    code, payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )

    assert code == 3
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "sensitive_data_remaining",
            "source": "catalog",
            "status": "stopped",
        },
    ) + b"\n"
    assert _AWS_KEY.encode() not in payload


def test_entry_does_not_write_files(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    before = sorted(path.name for path in tmp_path.iterdir())

    _run_entry(_entry_arguments(tmp_path, catalog_path, candidate_path))

    assert sorted(path.name for path in tmp_path.iterdir()) == before


def test_module_execution_from_other_directory_matches_bytes(tmp_path):
    catalog_path, candidate_path = _write_inputs(tmp_path)
    _, direct_payload = _run_entry(
        _entry_arguments(tmp_path, catalog_path, candidate_path),
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(Path.cwd())

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.requirements.one_requirement_feature_source_entry",
        ]
        + _entry_arguments(tmp_path, catalog_path, candidate_path),
        capture_output=True,
        cwd=tmp_path,
        env=environment,
    )

    assert completed.returncode == 0
    assert completed.stdout == direct_payload
    assert completed.stderr == b""


def test_console_script_is_registered():
    with Path("pyproject.toml").open("rb") as stream:
        configuration = tomllib.load(stream)

    assert configuration["project"]["scripts"][
        "reviewcompass3-requirement-candidate-check"
    ] == "tools.requirements.one_requirement_feature_source_entry:main"


# ---------------------------------------------------------------------------
# 受入条件16：禁止作用の不在
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module_path",
    (
        "tools/requirements/one_requirement_feature_source.py",
        "tools/requirements/one_requirement_feature_source_entry.py",
    ),
)
def test_modules_avoid_forbidden_capabilities(module_path):
    source = Path(module_path).read_text(encoding="utf-8")

    for forbidden in (
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "environ",
        "getenv",
    ):
        assert forbidden not in source


# ---------------------------------------------------------------------------
# 停止段階の順序
# ---------------------------------------------------------------------------


def test_utf8_stop_precedes_candidate_sensitive():
    candidate = _candidate()
    candidate["candidate_identifier"] = _AWS_KEY

    stop = _stop(
        catalog_bytes=b"\xff\xff",
        candidate=candidate,
    )

    assert (stop.reason, stop.source) == ("invalid_utf8", "catalog")


def test_sensitive_stop_precedes_schema_stop():
    candidate = _candidate()
    candidate["unknown_member"] = _AWS_KEY

    stop = _stop(candidate=candidate)

    assert (stop.reason, stop.source) == (
        "sensitive_data_remaining",
        "candidate",
    )


def test_catalog_schema_precedes_candidate_schema():
    catalog = _catalog()
    catalog["sources"][0]["declared_status"] = "unknown"
    candidate = _candidate()
    candidate["feature"]["name"] = None

    stop = _stop(catalog=catalog, candidate=candidate)

    assert (stop.reason, stop.source) == ("invalid_schema", "catalog")
