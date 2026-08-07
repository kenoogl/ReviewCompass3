"""機械操作routing v2の最小縦切り。

正本設計：docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md の§3
承認：`DEC-MACHINE-OPERATION-ROUTING-001`（§3だけ）

扱うのは次の3部だけである。

1. versioned operation inventory：作業単位で行う操作を分類付きで並べる。
2. permission preflight：実行前にinventory全体を一度走査し、必要な権限種別を一回で出す。
3. execution receipt：inventory、preflight verdict、実行結果を結ぶ。

このmoduleは決定的なlibraryであり、shellも外部processも一切起動しない。
権限の`host attestation`はcallerが渡す入力である。ここでOS、sandbox、hostの権限を
検査・付与・迂回することはない。承認と取得済み確認はhost側の責任である。

policy runnerへのimport依存を持たない。
"""

import hashlib
import json
from pathlib import Path


DIGEST_ALGORITHM = "sha256"

#: inventoryとpreflightのschema version。
SCHEMA_VERSION = 1

#: execution receiptのschema version。完全なpreflight recordを持つ形へ変えたため2である。
#: version 1のreceiptは抜粋しか持たず改竄を検出できないため、明示的に拒否する。
RECEIPT_SCHEMA_VERSION = 2

CLASSIFICATIONS = (
    "read_only",
    "project_artifact_write",
    "git_metadata_write",
    "external",
    "unknown",
)

#: host attestationで受理できる権限種別。
PERMISSIONS = ("git_metadata_write", "project_artifact_write")

#: 分類から必要権限種別を決める規則。`read_only`と`unknown`は権限を必要としない。
#: `external`はこのrunnerで実行できないため、preflightが停止する。
_REQUIRED_PERMISSION = {
    "read_only": None,
    "project_artifact_write": "project_artifact_write",
    "git_metadata_write": "git_metadata_write",
    "external": "external",
    "unknown": None,
}

# 分類の下限規則（層2）は外部configで宣言する。moduleは特定toolの知識を持たず、
# 規則を読んで適用するだけである（既存の境界設計を保つため）。
_MINIMUM_RULES_PATH = "config/development-classification-minimums.json"

_OPERATION_FIELDS = (
    "operation_id",
    "operation_version",
    "classification",
    "required_permission",
    "argv",
    "summary",
)
_INVENTORY_FIELDS = (
    "record_kind",
    "schema_version",
    "digest_algorithm",
    "inventory_id",
    "inventory_version",
    "operations",
    "content_digest",
)
_PREFLIGHT_FIELDS = (
    "record_kind",
    "schema_version",
    "digest_algorithm",
    "inventory_ref",
    "required_permissions",
    "granted_permissions",
    "missing_permissions",
    "verdict",
    "attestation_source",
    "content_digest",
)
_RECEIPT_FIELDS = (
    "record_kind",
    "schema_version",
    "digest_algorithm",
    "inventory_ref",
    "preflight_ref",
    "results",
    "content_digest",
)
_INVENTORY_REF_FIELDS = ("inventory_id", "inventory_version", "content_digest")
_RESULT_FIELDS = ("operation_id", "status", "detail")
_RESULT_STATUSES = ("completed", "failed")

STOP_CODES = (
    "inventory_invalid",
    "inventory_field_unknown",
    "inventory_schema_version_unsupported",
    "inventory_digest_mismatch",
    "operation_id_invalid",
    "operation_id_duplicated",
    "operation_classification_unknown",
    "permission_requirement_mismatch",
    "unknown_classification_not_executable",
    "external_operation_not_supported",
    "host_attestation_invalid",
    "approval_required",
    "preflight_invalid",
    "preflight_field_unknown",
    "preflight_digest_mismatch",
    "preflight_identity_mismatch",
    "preflight_requirement_mismatch",
    "preflight_verdict_mismatch",
    "preflight_not_passed",
    "receipt_invalid",
    "receipt_field_unknown",
    "receipt_schema_version_unsupported",
    "receipt_identity_mismatch",
    "receipt_digest_mismatch",
    "execution_result_invalid",
)


class OperationRoutingError(Exception):
    """機械操作routingのfail-closed条件に触れた。"""

    def __init__(self, code, detail=None, *, required_permissions=(), missing_permissions=()):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail
        self.required_permissions = tuple(required_permissions)
        self.missing_permissions = tuple(missing_permissions)


def canonical_digest(document):
    """`content_digest`を除いた正準表現のSHA-256を返す。"""

    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()


def _require_text(value):
    return isinstance(value, str) and bool(value.strip())


def _require_exact(document, fields, *, unknown_code, missing_code, label):
    if not isinstance(document, dict):
        raise OperationRoutingError(missing_code, label)
    expected = set(fields)
    unknown = sorted(set(document) - expected)
    if unknown:
        raise OperationRoutingError(unknown_code, f"{label}: {','.join(unknown)}")
    missing = sorted(expected - set(document))
    if missing:
        raise OperationRoutingError(missing_code, f"{label}: {','.join(missing)}")


# ------------------------------------------------------------------ 1. inventory


def classification_minimum_rules(*, project_root="."):
    """分類の下限規則を宣言として読む（層2の位置づけを含む）。

    規則の実体は外部configにあり、moduleは特定toolの知識を持たない。
    """

    path = Path(project_root) / _MINIMUM_RULES_PATH
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise OperationRoutingError(
            "classification_minimum_rules_unavailable", str(error)
        ) from error
    return document


def _check_classification_minimum(operation, *, rules_document):
    """argvの先頭が宣言済みの危険操作なら、軽すぎる分類を拒否する（層2）。"""

    argv = [item for item in operation.get("argv", []) if isinstance(item, str)]
    rank = rules_document["classification_rank"]
    actual = rank.get(operation["classification"], 0)
    for rule in rules_document["rules"]:
        head = tuple(rule["argv_head"])
        if tuple(argv[: len(head)]) != head:
            continue
        if actual < rank[rule["minimum"]]:
            raise OperationRoutingError(
                "classification_below_minimum",
                "%s: declared as %s, minimum %s (%s)" % (
                    operation.get("operation_id"), operation["classification"],
                    rule["minimum"], rule["note"],
                ),
            )
    return True


def build_operation_inventory(
    *, inventory_id, inventory_version=1, operations, project_root="."
):
    """分類と必要権限を確定した版付きinventoryを決定的に組み立てる。"""

    rules_document = classification_minimum_rules(project_root=project_root)
    if not _require_text(inventory_id):
        raise OperationRoutingError("inventory_invalid", "inventory_id")
    if not isinstance(inventory_version, int) or isinstance(inventory_version, bool):
        raise OperationRoutingError("inventory_invalid", "inventory_version")
    if not isinstance(operations, list) or not operations:
        raise OperationRoutingError("inventory_invalid", "operations")

    built = []
    for operation in operations:
        if not isinstance(operation, dict):
            raise OperationRoutingError("inventory_invalid", "operation")
        classification = operation.get("classification")
        if classification not in CLASSIFICATIONS:
            raise OperationRoutingError(
                "operation_classification_unknown", str(classification)
            )
        entry = {
            "operation_id": operation.get("operation_id"),
            "operation_version": operation.get("operation_version", 1),
            "classification": classification,
            "required_permission": _REQUIRED_PERMISSION[classification],
            "argv": list(operation.get("argv", [])),
            "summary": operation.get("summary"),
        }
        _check_classification_minimum(entry, rules_document=rules_document)
        built.append(entry)

    document = {
        "record_kind": "operation_inventory",
        "schema_version": SCHEMA_VERSION,
        "digest_algorithm": DIGEST_ALGORITHM,
        "inventory_id": inventory_id,
        "inventory_version": inventory_version,
        "operations": built,
    }
    document["content_digest"] = canonical_digest(document)
    validate_operation_inventory(document)
    return document


def validate_operation_inventory(inventory):
    """未知field、重複ID、空ID、未知分類、権限規則違反、Digest不一致を拒否する。"""

    if not isinstance(inventory, dict):
        raise OperationRoutingError("inventory_invalid", str(type(inventory)))
    if inventory.get("record_kind") != "operation_inventory":
        raise OperationRoutingError("inventory_invalid", str(inventory.get("record_kind")))
    if inventory.get("schema_version") != SCHEMA_VERSION:
        raise OperationRoutingError(
            "inventory_schema_version_unsupported", str(inventory.get("schema_version"))
        )
    _require_exact(
        inventory,
        _INVENTORY_FIELDS,
        unknown_code="inventory_field_unknown",
        missing_code="inventory_invalid",
        label="inventory",
    )
    if inventory["digest_algorithm"] != DIGEST_ALGORITHM:
        raise OperationRoutingError("inventory_invalid", "digest_algorithm")
    if not _require_text(inventory["inventory_id"]):
        raise OperationRoutingError("inventory_invalid", "inventory_id")
    if (
        not isinstance(inventory["inventory_version"], int)
        or isinstance(inventory["inventory_version"], bool)
        or inventory["inventory_version"] < 1
    ):
        raise OperationRoutingError("inventory_invalid", "inventory_version")
    operations = inventory["operations"]
    if not isinstance(operations, list) or not operations:
        raise OperationRoutingError("inventory_invalid", "operations")

    seen = set()
    for operation in operations:
        _require_exact(
            operation,
            _OPERATION_FIELDS,
            unknown_code="inventory_field_unknown",
            missing_code="inventory_invalid",
            label="operation",
        )
        if not _require_text(operation["operation_id"]):
            raise OperationRoutingError("operation_id_invalid", str(operation["operation_id"]))
        if operation["operation_id"] in seen:
            raise OperationRoutingError("operation_id_duplicated", operation["operation_id"])
        seen.add(operation["operation_id"])
        if (
            not isinstance(operation["operation_version"], int)
            or isinstance(operation["operation_version"], bool)
            or operation["operation_version"] < 1
        ):
            raise OperationRoutingError("inventory_invalid", "operation_version")
        if operation["classification"] not in CLASSIFICATIONS:
            raise OperationRoutingError(
                "operation_classification_unknown", str(operation["classification"])
            )
        if operation["required_permission"] != _REQUIRED_PERMISSION[
            operation["classification"]
        ]:
            raise OperationRoutingError(
                "permission_requirement_mismatch", operation["operation_id"]
            )
        argv = operation["argv"]
        if not isinstance(argv, list) or not argv or not all(
            isinstance(item, str) for item in argv
        ):
            raise OperationRoutingError("inventory_invalid", "argv")
        if not _require_text(operation["summary"]):
            raise OperationRoutingError("inventory_invalid", "summary")

    if inventory["content_digest"] != canonical_digest(inventory):
        raise OperationRoutingError(
            "inventory_digest_mismatch", str(inventory["content_digest"])
        )
    return True


def _inventory_reference(inventory):
    return {
        "inventory_id": inventory["inventory_id"],
        "inventory_version": inventory["inventory_version"],
        "content_digest": inventory["content_digest"],
    }


# ------------------------------------------------------------------ 2. preflight


def _validate_host_attestation(host_attestation):
    """callerが申告した取得済み権限を読む。ここで権限を検査・付与しない。"""

    _require_exact(
        host_attestation,
        ("granted_permissions",),
        unknown_code="host_attestation_invalid",
        missing_code="host_attestation_invalid",
        label="host attestation",
    )
    granted = host_attestation["granted_permissions"]
    if not isinstance(granted, list) or not all(isinstance(item, str) for item in granted):
        raise OperationRoutingError("host_attestation_invalid", "granted_permissions")
    unknown = sorted(set(granted) - set(PERMISSIONS))
    if unknown:
        raise OperationRoutingError("host_attestation_invalid", ",".join(unknown))
    return sorted(set(granted))


def required_permissions(inventory):
    """inventory全体から必要権限種別を重複なく一回で得る。"""

    validate_operation_inventory(inventory)
    for operation in inventory["operations"]:
        if operation["classification"] == "unknown":
            raise OperationRoutingError(
                "unknown_classification_not_executable", operation["operation_id"]
            )
    for operation in inventory["operations"]:
        if operation["classification"] == "external":
            raise OperationRoutingError(
                "external_operation_not_supported", operation["operation_id"]
            )
    needed = {
        operation["required_permission"]
        for operation in inventory["operations"]
        if operation["required_permission"] is not None
    }
    return sorted(needed)


def run_permission_preflight(*, inventory, host_attestation):
    """実行前に一度だけ走査し、必要権限を一回の集合で出す。

    未取得があれば`approval_required`のverdictを返す。この関数は何も実行しない。
    """

    validate_operation_inventory(inventory)
    granted = _validate_host_attestation(host_attestation)
    needed = required_permissions(inventory)
    missing = sorted(set(needed) - set(granted))
    document = {
        "record_kind": "operation_permission_preflight",
        "schema_version": SCHEMA_VERSION,
        "digest_algorithm": DIGEST_ALGORITHM,
        "inventory_ref": _inventory_reference(inventory),
        "required_permissions": needed,
        "granted_permissions": granted,
        "missing_permissions": missing,
        "verdict": "approval_required" if missing else "granted",
        "attestation_source": "host",
    }
    document["content_digest"] = canonical_digest(document)
    return document


def validate_permission_preflight(preflight, *, inventory):
    """preflightをinventoryから**再計算して**検証する。

    自己Digestを計算し直した改竄でも受理しない。必要権限はinventoryから導き直し、
    未取得集合とverdictも申告値ではなく再計算した値と一致しなければ拒否する。
    """

    if not isinstance(preflight, dict):
        raise OperationRoutingError("preflight_invalid", str(type(preflight)))
    if preflight.get("record_kind") != "operation_permission_preflight":
        raise OperationRoutingError("preflight_invalid", str(preflight.get("record_kind")))
    if preflight.get("schema_version") != SCHEMA_VERSION:
        raise OperationRoutingError("preflight_invalid", str(preflight.get("schema_version")))
    _require_exact(
        preflight,
        _PREFLIGHT_FIELDS,
        unknown_code="preflight_field_unknown",
        missing_code="preflight_invalid",
        label="preflight",
    )
    if preflight["attestation_source"] != "host":
        raise OperationRoutingError("preflight_invalid", "attestation_source")
    if preflight["verdict"] not in ("granted", "approval_required"):
        raise OperationRoutingError("preflight_invalid", str(preflight["verdict"]))
    if preflight["inventory_ref"] != _inventory_reference(inventory):
        raise OperationRoutingError("preflight_identity_mismatch", inventory["inventory_id"])

    granted = _validate_host_attestation(
        {"granted_permissions": preflight["granted_permissions"]}
    )
    if preflight["granted_permissions"] != granted:
        raise OperationRoutingError("host_attestation_invalid", "granted_permissions")

    needed = required_permissions(inventory)
    if preflight["required_permissions"] != needed:
        raise OperationRoutingError(
            "preflight_requirement_mismatch", ",".join(needed) or "(none)"
        )
    missing = sorted(set(needed) - set(granted))
    if preflight["missing_permissions"] != missing:
        raise OperationRoutingError(
            "preflight_requirement_mismatch", ",".join(missing) or "(none)"
        )
    expected_verdict = "approval_required" if missing else "granted"
    if preflight["verdict"] != expected_verdict:
        raise OperationRoutingError("preflight_verdict_mismatch", preflight["verdict"])

    if preflight["content_digest"] != canonical_digest(preflight):
        raise OperationRoutingError(
            "preflight_digest_mismatch", str(preflight["content_digest"])
        )
    return True


# ------------------------------------------------------------------ 3. receipt


def _validate_execution_result(result, operation_id):
    _require_exact(
        result,
        _RESULT_FIELDS,
        unknown_code="execution_result_invalid",
        missing_code="execution_result_invalid",
        label="execution result",
    )
    if result["operation_id"] != operation_id:
        raise OperationRoutingError("execution_result_invalid", operation_id)
    if result["status"] not in _RESULT_STATUSES:
        raise OperationRoutingError("execution_result_invalid", str(result["status"]))
    if not isinstance(result["detail"], str):
        raise OperationRoutingError("execution_result_invalid", "detail")


def execute_with_preflight(*, inventory, host_attestation, execute):
    """preflightが通った場合だけcallbackを呼び、receiptを返す。

    停止条件に触れた場合、callbackは一度も呼ばれない。実行そのものはcallerのcallbackが行い、
    このmoduleはcommandを起動しない。
    """

    preflight = run_permission_preflight(
        inventory=inventory, host_attestation=host_attestation
    )
    if preflight["verdict"] != "granted":
        raise OperationRoutingError(
            "approval_required",
            ",".join(preflight["missing_permissions"]),
            required_permissions=preflight["required_permissions"],
            missing_permissions=preflight["missing_permissions"],
        )

    results = []
    for operation in inventory["operations"]:
        outcome = execute(dict(operation))
        if not isinstance(outcome, dict):
            raise OperationRoutingError(
                "execution_result_invalid", operation["operation_id"]
            )
        result = {
            "operation_id": operation["operation_id"],
            "status": outcome.get("status"),
            "detail": outcome.get("detail"),
        }
        _validate_execution_result(result, operation["operation_id"])
        results.append(result)

    document = {
        "record_kind": "operation_execution_receipt",
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "digest_algorithm": DIGEST_ALGORITHM,
        "inventory_ref": _inventory_reference(inventory),
        # 抜粋ではなく、完全な検証済みpreflight recordを保存する。
        # validatorはこれをinventoryに対して再計算で検証できる。
        "preflight_ref": preflight,
        "results": results,
    }
    document["content_digest"] = canonical_digest(document)
    validate_execution_receipt(document, inventory=inventory)
    return document


def validate_execution_receipt(receipt, *, inventory):
    """inventory identity、preflight verdict、未知field、Digestを検査する。"""

    if not isinstance(receipt, dict):
        raise OperationRoutingError("receipt_invalid", str(type(receipt)))
    if receipt.get("record_kind") != "operation_execution_receipt":
        raise OperationRoutingError("receipt_invalid", str(receipt.get("record_kind")))
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        raise OperationRoutingError(
            "receipt_schema_version_unsupported", str(receipt.get("schema_version"))
        )
    _require_exact(
        receipt,
        _RECEIPT_FIELDS,
        unknown_code="receipt_field_unknown",
        missing_code="receipt_invalid",
        label="receipt",
    )
    _require_exact(
        receipt["inventory_ref"],
        _INVENTORY_REF_FIELDS,
        unknown_code="receipt_field_unknown",
        missing_code="receipt_invalid",
        label="inventory reference",
    )
    if receipt["inventory_ref"] != _inventory_reference(inventory):
        raise OperationRoutingError("receipt_identity_mismatch", inventory["inventory_id"])

    preflight = receipt["preflight_ref"]
    if not isinstance(preflight, dict):
        raise OperationRoutingError("receipt_invalid", "preflight_ref")
    if preflight.get("verdict") != "granted":
        raise OperationRoutingError("preflight_not_passed", str(preflight.get("verdict")))
    # 完全なpreflight recordをinventoryに対して再計算で検証する。
    # 必要権限を空へ改竄してDigestを合わせ直しても、ここで拒否される。
    validate_permission_preflight(preflight, inventory=inventory)

    results = receipt["results"]
    if not isinstance(results, list) or len(results) != len(inventory["operations"]):
        raise OperationRoutingError("receipt_invalid", "results")
    for result, operation in zip(results, inventory["operations"]):
        _validate_execution_result(result, operation["operation_id"])

    if receipt["content_digest"] != canonical_digest(receipt):
        raise OperationRoutingError("receipt_digest_mismatch", str(receipt["content_digest"]))
    return True


# ------------------------------------------------------------------ 最小CLI


def main(argv=None):
    """inventoryを読み、preflightをJSONで出すだけのCLI。commandは実行しない。"""

    import argparse

    parser = argparse.ArgumentParser(
        description="operation inventoryを読み、必要権限種別を出す（実行はしない）"
    )
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--granted", action="append", default=[])
    arguments = parser.parse_args(argv)

    inventory = json.loads(Path(arguments.inventory).read_text(encoding="utf-8"))
    try:
        preflight = run_permission_preflight(
            inventory=inventory,
            host_attestation={"granted_permissions": list(arguments.granted)},
        )
    except OperationRoutingError as error:
        print(json.dumps({"status": "stopped", "code": error.code, "detail": error.detail},
                         ensure_ascii=False, sort_keys=True))
        return 1
    print(json.dumps(preflight, ensure_ascii=False, sort_keys=True))
    return 0 if preflight["verdict"] == "granted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
