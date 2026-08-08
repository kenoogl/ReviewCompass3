"""統合除外宣言（構成A-1）：統合してはいけない対象の機械可読宣言。

承認：DEC-WORK4B-MAIN-DESIGN-BUNDLE-001（構成A-1）、DEC-INTEGRATION-EXCLUSION-ENTRIES-001

除外宣言recordはHuman承認Decisionへの参照なしには成立しない。絞り込み順位表（構成A-2）は
本宣言を機械参照し、該当groupを候補から落とし、落とした件数を表示する。除外は「統合しない」の
宣言であって、codeの削除・変更・レビュー免除を意味しない。
"""

import hashlib
import json
from pathlib import Path


class IntegrationExclusionError(Exception):
    """除外宣言recordの検証・保存・読み込みの失敗。"""


_RECORD_FIELDS = (
    "record_kind", "schema_version", "exclusion_id", "exclusion_version",
    "created_at", "approval", "entries", "content_digest",
)
_APPROVAL_FIELDS = ("decision_id", "path", "sha256")
_ENTRY_FIELDS = ("entry_id", "reason_kind", "targets", "rationale", "authority_refs")
_TARGET_FIELDS = ("kind", "value")
_REASON_KINDS = (
    "version_pinned", "frozen_lane", "historical_retained", "superseded_kept",
)
_TARGET_KINDS = ("symbol_prefix", "module_path", "config_lane")


from tools.common.digests import file_sha256 as file_sha256


from tools.common.digests import canonical_content_digest as content_digest


def _require_exact_fields(document, fields, label):
    if not isinstance(document, dict):
        raise IntegrationExclusionError(f"{label} is not a mapping")
    unknown = sorted(set(document) - set(fields))
    if unknown:
        raise IntegrationExclusionError(f"{label} has unknown fields: {','.join(unknown)}")
    missing = sorted(set(fields) - set(document))
    if missing:
        raise IntegrationExclusionError(f"{label} misses fields: {','.join(missing)}")


def validate_integration_exclusions(record, *, project_root="."):
    """必須field、理由種別語彙、承認参照、digestをfail-closedで検証する。"""

    _require_exact_fields(record, _RECORD_FIELDS, "integration exclusions record")
    if record["record_kind"] != "integration_exclusions":
        raise IntegrationExclusionError("record kind is invalid")
    if record["schema_version"] != 1:
        raise IntegrationExclusionError("schema version is invalid")

    approval = record["approval"]
    _require_exact_fields(approval, _APPROVAL_FIELDS, "approval reference")
    approval_file = Path(project_root) / approval["path"]
    if not approval_file.is_file():
        raise IntegrationExclusionError(
            f"approval decision is missing: {approval['path']}"
        )
    if file_sha256(approval_file) != approval["sha256"]:
        raise IntegrationExclusionError(
            f"approval decision digest mismatch: {approval['path']}"
        )

    entries = record["entries"]
    if not isinstance(entries, list) or not entries:
        raise IntegrationExclusionError("entries are missing")
    seen_ids = set()
    for entry in entries:
        _require_exact_fields(entry, _ENTRY_FIELDS, "exclusion entry")
        if entry["entry_id"] in seen_ids:
            raise IntegrationExclusionError(
                f"duplicate entry id: {entry['entry_id']}"
            )
        seen_ids.add(entry["entry_id"])
        if entry["reason_kind"] not in _REASON_KINDS:
            raise IntegrationExclusionError(
                f"reason kind is invalid: {entry['reason_kind']}"
            )
        if not isinstance(entry["targets"], list) or not entry["targets"]:
            raise IntegrationExclusionError(
                f"entry targets are missing: {entry['entry_id']}"
            )
        for target in entry["targets"]:
            _require_exact_fields(target, _TARGET_FIELDS, "exclusion target")
            if target["kind"] not in _TARGET_KINDS:
                raise IntegrationExclusionError(
                    f"target kind is invalid: {target['kind']}"
                )
            if not isinstance(target["value"], str) or not target["value"]:
                raise IntegrationExclusionError(
                    f"target value is invalid: {entry['entry_id']}"
                )
        if not isinstance(entry["rationale"], str) or not entry["rationale"]:
            raise IntegrationExclusionError(
                f"entry rationale is missing: {entry['entry_id']}"
            )
        if not isinstance(entry["authority_refs"], list) or not entry["authority_refs"]:
            raise IntegrationExclusionError(
                f"entry authority refs are missing: {entry['entry_id']}"
            )
        # 根拠は解決できなければ根拠ではない。ID文字列だけでは、実在しない
        # Decisionを名乗って除外を通せてしまう。
        for reference in entry["authority_refs"]:
            if not isinstance(reference, dict) or not reference.get("path"):
                raise IntegrationExclusionError(
                    f"authority reference has no path: {entry['entry_id']}"
                )
            target = Path(project_root) / reference["path"]
            if not target.is_file():
                raise IntegrationExclusionError(
                    f"authority reference is unresolvable: {reference['path']}"
                )

    if record["content_digest"] != content_digest(record):
        raise IntegrationExclusionError("content digest mismatch")
    return True


def write_integration_exclusions(*, path, record):
    """new-onlyで保存する。既存fileの上書きを拒否する。"""

    target = Path(path)
    if target.exists():
        raise IntegrationExclusionError("integration exclusions record already exists")
    target.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def excluded_entry_ids(symbol_id, *, record):
    """symbol_idに該当する除外entryのIDを決定的に返す。非該当は空list。"""

    module_part = symbol_id.split(":", 1)[0]
    matched = []
    for entry in record["entries"]:
        for target in entry["targets"]:
            if target["kind"] == "symbol_prefix" and symbol_id.startswith(
                target["value"]
            ):
                matched.append(entry["entry_id"])
                break
            if target["kind"] == "module_path" and module_part == target["value"]:
                matched.append(entry["entry_id"])
                break
    return sorted(matched)


def exclusion_impact(*, record, symbol_ids):
    """除外指定が落とすsymbolの件数をentry別に報告する（層2）。

    拒否はしない。広範囲の指定が何を落とすかをHumanが承認時に見えるようにする。
    """

    by_entry = {entry["entry_id"]: 0 for entry in record["entries"]}
    excluded = 0
    for symbol_id in symbol_ids:
        matched = excluded_entry_ids(symbol_id, record=record)
        if matched:
            excluded += 1
        for entry_id in matched:
            by_entry[entry_id] += 1
    return {
        "enforcement": "reported_for_human_review",
        "total_symbols": len(tuple(symbol_ids)),
        "excluded_symbols": excluded,
        "by_entry": by_entry,
    }


def load_integration_exclusions(*, path, project_root="."):
    """読み込みと検証。欠落・解析不能はfail-closedでerrorにする。"""

    target = Path(path)
    try:
        record = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise IntegrationExclusionError(
            f"integration exclusions record unavailable: {target} "
            f"({type(error).__name__})"
        ) from error
    validate_integration_exclusions(record, project_root=project_root)
    return record
