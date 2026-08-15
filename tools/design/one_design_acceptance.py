"""一件の設計と受入条件を決定的に照合する。"""

import hashlib
import json
import re


_SAFE_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_OPERATORS = frozenset(("equals", "not_equals", "contains_all", "contains_none"))
_QUEUE_ORDER = ("contradicted", "missing", "satisfied", "unreferenced_fact")
_INTEGER_LIMIT = 9007199254740991


class DesignAcceptanceStop(Exception):
    """入力を安全に照合できないため処理を停止する。"""

    def __init__(self, reason, source):
        super().__init__(reason)
        self.reason = reason
        self.source = source


class _DuplicateMember(ValueError):
    """復号後のJSON項目名が重複している。"""


def canonical_json_bytes(value):
    """値を内容識別値用の正準JSON bytesへ変換する。"""

    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateMember
        value[key] = item
    return value


def _decode_input(raw, source):
    if not isinstance(raw, bytes):
        raise DesignAcceptanceStop("invalid_schema", source)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise DesignAcceptanceStop("invalid_utf8", source) from error
    try:
        return json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, _DuplicateMember, RecursionError) as error:
        raise DesignAcceptanceStop("invalid_schema", source) from error


def _is_safe_identifier(value):
    return isinstance(value, str) and _SAFE_IDENTIFIER.fullmatch(value) is not None


def _normalize_value(value, source):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if -_INTEGER_LIMIT <= value <= _INTEGER_LIMIT:
            return value
        raise DesignAcceptanceStop("invalid_schema", source)
    if isinstance(value, str):
        if 1 <= len(value) <= 2000 and "\x00" not in value:
            return value
        raise DesignAcceptanceStop("invalid_schema", source)
    if isinstance(value, list):
        if not 1 <= len(value) <= 32:
            raise DesignAcceptanceStop("invalid_schema", source)
        if any(
            not isinstance(item, str)
            or not 1 <= len(item) <= 256
            or "\x00" in item
            for item in value
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        if len(set(value)) != len(value):
            raise DesignAcceptanceStop("invalid_schema", source)
        return sorted(value)
    raise DesignAcceptanceStop("invalid_schema", source)


def _normalize_design(value):
    source = "design"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "design_identifier",
        "facts",
    }:
        raise DesignAcceptanceStop("invalid_schema", source)
    if value["schema_version"] != 1 or not _is_safe_identifier(
        value["design_identifier"]
    ):
        raise DesignAcceptanceStop("invalid_schema", source)
    facts = value["facts"]
    if not isinstance(facts, list) or not 1 <= len(facts) <= 256:
        raise DesignAcceptanceStop("invalid_schema", source)

    normalized_facts = []
    fact_ids = set()
    subjects = set()
    for fact in facts:
        if not isinstance(fact, dict) or set(fact) != {
            "fact_id",
            "subject",
            "value",
        }:
            raise DesignAcceptanceStop("invalid_schema", source)
        fact_id = fact["fact_id"]
        subject = fact["subject"]
        if (
            not _is_safe_identifier(fact_id)
            or not _is_safe_identifier(subject)
            or fact_id in fact_ids
            or subject in subjects
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        fact_ids.add(fact_id)
        subjects.add(subject)
        normalized_facts.append(
            {
                "fact_id": fact_id,
                "subject": subject,
                "value": _normalize_value(fact["value"], source),
            }
        )

    normalized_facts.sort(key=lambda fact: (fact["subject"], fact["fact_id"]))
    return {
        "schema_version": 1,
        "design_identifier": value["design_identifier"],
        "facts": normalized_facts,
    }


def _normalize_acceptance(value):
    source = "acceptance"
    if not isinstance(value, dict) or set(value) != {
        "schema_version",
        "acceptance_identifier",
        "conditions",
    }:
        raise DesignAcceptanceStop("invalid_schema", source)
    if value["schema_version"] != 1 or not _is_safe_identifier(
        value["acceptance_identifier"]
    ):
        raise DesignAcceptanceStop("invalid_schema", source)
    conditions = value["conditions"]
    if not isinstance(conditions, list) or not 1 <= len(conditions) <= 256:
        raise DesignAcceptanceStop("invalid_schema", source)

    normalized_conditions = []
    condition_ids = set()
    subjects = set()
    for condition in conditions:
        if not isinstance(condition, dict) or set(condition) != {
            "condition_id",
            "subject",
            "operator",
            "expected",
        }:
            raise DesignAcceptanceStop("invalid_schema", source)
        condition_id = condition["condition_id"]
        subject = condition["subject"]
        operator = condition["operator"]
        if (
            not _is_safe_identifier(condition_id)
            or not _is_safe_identifier(subject)
            or condition_id in condition_ids
            or subject in subjects
            or operator not in _OPERATORS
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        expected = _normalize_value(condition["expected"], source)
        if operator in ("contains_all", "contains_none") and not isinstance(
            expected,
            list,
        ):
            raise DesignAcceptanceStop("invalid_schema", source)
        condition_ids.add(condition_id)
        subjects.add(subject)
        normalized_conditions.append(
            {
                "condition_id": condition_id,
                "subject": subject,
                "operator": operator,
                "expected": expected,
            }
        )

    normalized_conditions.sort(key=lambda condition: condition["condition_id"])
    return {
        "schema_version": 1,
        "acceptance_identifier": value["acceptance_identifier"],
        "conditions": normalized_conditions,
    }


def _typed_equal(actual, expected):
    return type(actual) is type(expected) and actual == expected


def _is_satisfied(operator, actual, expected):
    if operator == "equals":
        return _typed_equal(actual, expected)
    if operator == "not_equals":
        return not _typed_equal(actual, expected)
    if not isinstance(actual, list):
        return False
    actual_values = set(actual)
    expected_values = set(expected)
    if operator == "contains_all":
        return expected_values.issubset(actual_values)
    return actual_values.isdisjoint(expected_values)


def _build_result(design, acceptance):
    facts_by_subject = {fact["subject"]: fact for fact in design["facts"]}
    used_fact_ids = set()
    results = []
    identifiers_by_kind = {kind: [] for kind in _QUEUE_ORDER}

    for condition in acceptance["conditions"]:
        fact = facts_by_subject.get(condition["subject"])
        if fact is None:
            disposition = "missing"
            fact_id = None
            actual_sha256 = None
        else:
            fact_id = fact["fact_id"]
            used_fact_ids.add(fact_id)
            actual_sha256 = _sha256(fact["value"])
            disposition = (
                "satisfied"
                if _is_satisfied(
                    condition["operator"],
                    fact["value"],
                    condition["expected"],
                )
                else "contradicted"
            )
        identifiers_by_kind[disposition].append(condition["condition_id"])
        results.append(
            {
                "condition_id": condition["condition_id"],
                "subject": condition["subject"],
                "disposition": disposition,
                "fact_id": fact_id,
                "operator": condition["operator"],
                "expected_value_sha256": _sha256(condition["expected"]),
                "actual_value_sha256": actual_sha256,
            }
        )

    unreferenced = sorted(
        fact["fact_id"]
        for fact in design["facts"]
        if fact["fact_id"] not in used_fact_ids
    )
    identifiers_by_kind["unreferenced_fact"] = unreferenced
    counts = {
        "contradicted": len(identifiers_by_kind["contradicted"]),
        "missing": len(identifiers_by_kind["missing"]),
        "satisfied": len(identifiers_by_kind["satisfied"]),
        "unreferenced_fact": len(unreferenced),
    }
    queue = [
        {"identifiers": sorted(identifiers_by_kind[kind]), "kind": kind}
        for kind in _QUEUE_ORDER
        if identifiers_by_kind[kind]
    ]
    result = {
        "acceptance": {
            "condition_count": len(acceptance["conditions"]),
            "identifier": acceptance["acceptance_identifier"],
            "sha256": _sha256(acceptance),
        },
        "counts": counts,
        "decision_status": "pending_human_decision",
        "design": {
            "fact_count": len(design["facts"]),
            "identifier": design["design_identifier"],
            "sha256": _sha256(design),
        },
        "external_send_approved": False,
        "human_decision_queue": queue,
        "results": results,
        "schema_version": 1,
        "status": "comparison_completed",
        "unreferenced_fact_ids": unreferenced,
        "verdict": (
            "review_required"
            if counts["missing"] or counts["contradicted"]
            else "conditions_met_pending_human_decision"
        ),
    }
    result["comparison_sha256"] = _sha256(result)
    return result


def compare_inputs(design_bytes, acceptance_bytes):
    """検査・正規化した設計と受入条件を照合する。"""

    design = _normalize_design(_decode_input(design_bytes, "design"))
    acceptance = _normalize_acceptance(
        _decode_input(acceptance_bytes, "acceptance")
    )
    return _build_result(design, acceptance)
