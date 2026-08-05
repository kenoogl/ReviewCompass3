"""機械操作routing v2 最小縦切りのAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-machine-operation-routing-v2-slice.md
承認：DEC-MACHINE-OPERATION-ROUTING-001（v2提案§3だけ）

対象は次の3部だけである。
  1. versioned operation inventory
  2. permission preflight
  3. execution receipt

このmoduleはshell、subprocess、Gitを実行しない。host attestationはcallerが渡す入力であり、
project側がsandbox権限を検査・付与・迂回することはない。
"""

import hashlib
import importlib
import json

import pytest


CLASSIFICATIONS = (
    "read_only",
    "project_artifact_write",
    "git_metadata_write",
    "external",
    "unknown",
)


@pytest.fixture
def routing():
    return importlib.import_module("tools.development.operation_routing")


def _digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    ).hexdigest()


def _operation(operation_id, classification, argv, summary):
    return {
        "operation_id": operation_id,
        "classification": classification,
        "argv": list(argv),
        "summary": summary,
    }


def _read_only_operations():
    return [
        _operation("OP-001", "read_only", ["git", "status", "--porcelain"], "作業状態を読む"),
        _operation("OP-002", "read_only", ["git", "diff", "--check"], "空白の混入を読む"),
    ]


def _mixed_operations():
    return [
        _operation("OP-001", "read_only", ["git", "status", "--porcelain"], "作業状態を読む"),
        _operation(
            "OP-002", "project_artifact_write", ["write", "records/development/x.md"],
            "成果物fileを書く",
        ),
        _operation("OP-003", "git_metadata_write", ["git", "add", "records/development/x.md"], "stageする"),
        _operation("OP-004", "git_metadata_write", ["git", "commit", "-m", "x"], "commitする"),
    ]


def _inventory(routing, operations, inventory_id="OPINV-FIXTURE-001", inventory_version=1):
    return routing.build_operation_inventory(
        inventory_id=inventory_id,
        inventory_version=inventory_version,
        operations=operations,
    )


class _Recorder:
    """callbackが呼ばれたかどうかを独立に記録する。報告文を根拠にしない。"""

    def __init__(self, status="completed"):
        self.calls = []
        self.status = status

    def __call__(self, operation):
        self.calls.append(operation["operation_id"])
        return {"status": self.status, "detail": f"{operation['operation_id']}を実行した"}


# ------------------------------------------------------------------ 1. inventory


def test_inventory_carries_identity_classification_permission_and_digest(routing):
    inventory = _inventory(routing, _mixed_operations())

    assert inventory["record_kind"] == "operation_inventory"
    assert inventory["schema_version"] == 1
    assert inventory["inventory_id"] == "OPINV-FIXTURE-001"
    assert inventory["inventory_version"] == 1
    assert inventory["digest_algorithm"] == "sha256"
    assert inventory["content_digest"] == _digest(inventory)
    assert routing.validate_operation_inventory(inventory) is True

    permissions = [item["required_permission"] for item in inventory["operations"]]
    assert permissions == [None, "project_artifact_write", "git_metadata_write", "git_metadata_write"]
    for item in inventory["operations"]:
        assert item["operation_version"] == 1
        assert set(item) == {
            "operation_id", "operation_version", "classification",
            "required_permission", "argv", "summary",
        }

    # 同じ入力からは同じinventoryとDigestが再生成できる。
    again = _inventory(routing, _mixed_operations())
    assert again == inventory


def test_inventory_rejects_broken_shapes(routing):
    inventory = _inventory(routing, _mixed_operations())

    def _reject(document):
        with pytest.raises(routing.OperationRoutingError) as error:
            routing.validate_operation_inventory(document)
        return error.value.code

    assert _reject("not a mapping") == "inventory_invalid"
    assert _reject([1, 2, 3]) == "inventory_invalid"

    unknown_field = dict(inventory, reviewer="claude")
    unknown_field["content_digest"] = _digest(unknown_field)
    assert _reject(unknown_field) == "inventory_field_unknown"

    wrong_schema = dict(inventory, schema_version=99)
    wrong_schema["content_digest"] = _digest(wrong_schema)
    assert _reject(wrong_schema) == "inventory_schema_version_unsupported"

    empty_id = json.loads(json.dumps(inventory))
    empty_id["operations"][0]["operation_id"] = ""
    empty_id["content_digest"] = _digest(empty_id)
    assert _reject(empty_id) == "operation_id_invalid"

    duplicated = json.loads(json.dumps(inventory))
    duplicated["operations"][1]["operation_id"] = duplicated["operations"][0]["operation_id"]
    duplicated["content_digest"] = _digest(duplicated)
    assert _reject(duplicated) == "operation_id_duplicated"

    broken_digest = dict(inventory, content_digest="0" * 64)
    assert _reject(broken_digest) == "inventory_digest_mismatch"

    no_operations = dict(inventory, operations=[])
    no_operations["content_digest"] = _digest(no_operations)
    assert _reject(no_operations) == "inventory_invalid"

    unknown_operation_field = json.loads(json.dumps(inventory))
    unknown_operation_field["operations"][0]["note"] = "x"
    unknown_operation_field["content_digest"] = _digest(unknown_operation_field)
    assert _reject(unknown_operation_field) == "inventory_field_unknown"

    bad_argv = json.loads(json.dumps(inventory))
    bad_argv["operations"][0]["argv"] = "git status"
    bad_argv["content_digest"] = _digest(bad_argv)
    assert _reject(bad_argv) == "inventory_invalid"


# ------------------------------------------------------------------ 2. 分類語彙


def test_only_the_five_classifications_are_accepted(routing):
    assert routing.CLASSIFICATIONS == CLASSIFICATIONS

    for classification in CLASSIFICATIONS:
        inventory = _inventory(
            routing, [_operation("OP-001", classification, ["noop"], "分類の確認")]
        )
        assert routing.validate_operation_inventory(inventory) is True

    with pytest.raises(routing.OperationRoutingError) as error:
        _inventory(routing, [_operation("OP-001", "maybe_safe", ["noop"], "未定義")])
    assert error.value.code == "operation_classification_unknown"

    inventory = _inventory(routing, _read_only_operations())
    tampered = json.loads(json.dumps(inventory))
    tampered["operations"][0]["classification"] = "maybe_safe"
    tampered["content_digest"] = _digest(tampered)
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_operation_inventory(tampered)
    assert error.value.code == "operation_classification_unknown"


def test_unknown_classification_is_fail_closed(routing):
    inventory = _inventory(
        routing,
        [
            _operation("OP-001", "read_only", ["git", "status"], "読む"),
            _operation("OP-002", "unknown", ["git", "frobnicate"], "判定できない"),
        ],
    )
    recorder = _Recorder()

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.run_permission_preflight(
            inventory=inventory, host_attestation={"granted_permissions": []}
        )
    assert error.value.code == "unknown_classification_not_executable"

    with pytest.raises(routing.OperationRoutingError):
        routing.execute_with_preflight(
            inventory=inventory,
            host_attestation={"granted_permissions": ["git_metadata_write"]},
            execute=recorder,
        )
    assert recorder.calls == []


# ------------------------------------------------------------------ 3. preflight


def test_preflight_collects_required_permissions_once_without_duplicates(routing):
    inventory = _inventory(routing, _mixed_operations())
    verdict = routing.run_permission_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["project_artifact_write", "git_metadata_write"]
        },
    )

    assert verdict["record_kind"] == "operation_permission_preflight"
    assert verdict["required_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]
    assert verdict["missing_permissions"] == []
    assert verdict["verdict"] == "granted"
    assert verdict["attestation_source"] == "host"
    assert verdict["inventory_ref"] == {
        "inventory_id": inventory["inventory_id"],
        "inventory_version": inventory["inventory_version"],
        "content_digest": inventory["content_digest"],
    }
    assert verdict["content_digest"] == _digest(verdict)
    assert routing.validate_permission_preflight(verdict, inventory=inventory) is True


def test_read_only_inventory_requires_no_permission(routing):
    inventory = _inventory(routing, _read_only_operations())
    verdict = routing.run_permission_preflight(
        inventory=inventory, host_attestation={"granted_permissions": []}
    )

    assert verdict["required_permissions"] == []
    assert verdict["missing_permissions"] == []
    assert verdict["verdict"] == "granted"

    recorder = _Recorder()
    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={"granted_permissions": []},
        execute=recorder,
    )
    assert recorder.calls == ["OP-001", "OP-002"]
    assert receipt["preflight_ref"]["verdict"] == "granted"


# ------------------------------------------------------------------ 4. 権限不足


def test_missing_permission_stops_before_any_callback(routing):
    inventory = _inventory(routing, _mixed_operations())
    recorder = _Recorder()

    verdict = routing.run_permission_preflight(
        inventory=inventory,
        host_attestation={"granted_permissions": ["project_artifact_write"]},
    )
    assert verdict["verdict"] == "approval_required"
    assert verdict["required_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]
    assert verdict["missing_permissions"] == ["git_metadata_write"]

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.execute_with_preflight(
            inventory=inventory,
            host_attestation={"granted_permissions": ["project_artifact_write"]},
            execute=recorder,
        )
    assert error.value.code == "approval_required"
    assert error.value.required_permissions == (
        "git_metadata_write", "project_artifact_write",
    )
    assert error.value.missing_permissions == ("git_metadata_write",)
    assert recorder.calls == []


def test_empty_attestation_requests_every_permission_in_one_set(routing):
    inventory = _inventory(routing, _mixed_operations())
    verdict = routing.run_permission_preflight(
        inventory=inventory, host_attestation={"granted_permissions": []}
    )
    assert verdict["verdict"] == "approval_required"
    assert verdict["missing_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]


# ------------------------------------------------------------------ 5. host attestation


def test_execution_runs_only_when_attestation_covers_every_permission(routing):
    inventory = _inventory(routing, _mixed_operations())
    recorder = _Recorder()

    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
        execute=recorder,
    )
    assert recorder.calls == ["OP-001", "OP-002", "OP-003", "OP-004"]
    assert receipt["preflight_ref"]["attestation_source"] == "host"
    assert [item["operation_id"] for item in receipt["results"]] == recorder.calls
    assert all(item["status"] == "completed" for item in receipt["results"])


def test_host_attestation_is_an_input_not_a_permission_check(routing):
    """project側はsandbox権限を検査・付与しない。attestationはcallerの申告である。"""

    source = (
        importlib.import_module("tools.development.operation_routing").__file__
    )
    with open(source, encoding="utf-8") as handle:
        text = handle.read()
    for forbidden in ("subprocess", "import os", "os.system", "shell=True", "Popen"):
        assert forbidden not in text
    assert "git" not in text.replace("git_metadata_write", "")

    inventory = _inventory(routing, _mixed_operations())
    verdict = routing.run_permission_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
    )
    assert verdict["attestation_source"] == "host"
    assert verdict["granted_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.run_permission_preflight(
            inventory=inventory, host_attestation={"granted_permissions": "everything"}
        )
    assert error.value.code == "host_attestation_invalid"

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.run_permission_preflight(
            inventory=inventory,
            host_attestation={"granted_permissions": ["superuser"]},
        )
    assert error.value.code == "host_attestation_invalid"


# ------------------------------------------------------------------ 6. external


def test_external_operations_are_not_supported_by_this_runner(routing):
    inventory = _inventory(
        routing,
        [
            _operation("OP-001", "read_only", ["git", "status"], "読む"),
            _operation("OP-002", "external", ["send", "https://example.invalid"], "外部送信"),
        ],
    )
    recorder = _Recorder()

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.run_permission_preflight(
            inventory=inventory, host_attestation={"granted_permissions": []}
        )
    assert error.value.code == "external_operation_not_supported"

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.execute_with_preflight(
            inventory=inventory,
            host_attestation={
                "granted_permissions": ["git_metadata_write", "project_artifact_write"]
            },
            execute=recorder,
        )
    assert error.value.code == "external_operation_not_supported"
    assert recorder.calls == []


# ------------------------------------------------------------------ 7. receipt


def test_receipt_binds_inventory_and_preflight_identity(routing):
    inventory = _inventory(routing, _mixed_operations())
    recorder = _Recorder()
    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
        execute=recorder,
    )

    assert receipt["record_kind"] == "operation_execution_receipt"
    # receiptは完全なpreflight recordを持つ形へ変わったためschema versionは2である。
    assert receipt["schema_version"] == 2
    assert receipt["inventory_ref"] == {
        "inventory_id": inventory["inventory_id"],
        "inventory_version": inventory["inventory_version"],
        "content_digest": inventory["content_digest"],
    }
    assert receipt["content_digest"] == _digest(receipt)
    assert routing.validate_execution_receipt(receipt, inventory=inventory) is True


def test_receipt_with_a_different_inventory_identity_is_rejected(routing):
    inventory = _inventory(routing, _mixed_operations())
    other = _inventory(routing, _mixed_operations(), inventory_id="OPINV-FIXTURE-002")
    recorder = _Recorder()
    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
        execute=recorder,
    )

    def _reject(document, target):
        with pytest.raises(routing.OperationRoutingError) as error:
            routing.validate_execution_receipt(document, inventory=target)
        return error.value.code

    assert _reject(receipt, other) == "receipt_identity_mismatch"

    wrong_version = json.loads(json.dumps(receipt))
    wrong_version["inventory_ref"]["inventory_version"] = 2
    wrong_version["content_digest"] = _digest(wrong_version)
    assert _reject(wrong_version, inventory) == "receipt_identity_mismatch"

    wrong_digest = json.loads(json.dumps(receipt))
    wrong_digest["inventory_ref"]["content_digest"] = "0" * 64
    wrong_digest["content_digest"] = _digest(wrong_digest)
    assert _reject(wrong_digest, inventory) == "receipt_identity_mismatch"

    broken = dict(receipt, content_digest="0" * 64)
    assert _reject(broken, inventory) == "receipt_digest_mismatch"

    unknown_field = dict(receipt, reviewer="claude")
    unknown_field["content_digest"] = _digest(unknown_field)
    assert _reject(unknown_field, inventory) == "receipt_field_unknown"


def test_receipt_without_a_granted_preflight_is_rejected(routing):
    inventory = _inventory(routing, _mixed_operations())
    recorder = _Recorder()
    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
        execute=recorder,
    )

    not_passed = json.loads(json.dumps(receipt))
    not_passed["preflight_ref"]["verdict"] = "approval_required"
    not_passed["content_digest"] = _digest(not_passed)
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_execution_receipt(not_passed, inventory=inventory)
    assert error.value.code == "preflight_not_passed"


# ------------------------------------------------------------------ 8. Git相当の分類


def test_git_argv_fixtures_show_the_expected_classification(routing):
    inventory = _inventory(
        routing,
        [
            _operation("OP-001", "read_only", ["git", "status", "--porcelain"], "読む"),
            _operation("OP-002", "read_only", ["git", "diff", "--check"], "読む"),
            _operation("OP-003", "git_metadata_write", ["git", "add", "AGENTS.md"], "stageする"),
            _operation("OP-004", "git_metadata_write", ["git", "commit", "-m", "x"], "commitする"),
        ],
    )
    classification = {
        item["operation_id"]: item["classification"] for item in inventory["operations"]
    }
    assert classification == {
        "OP-001": "read_only",
        "OP-002": "read_only",
        "OP-003": "git_metadata_write",
        "OP-004": "git_metadata_write",
    }

    verdict = routing.run_permission_preflight(
        inventory=inventory,
        host_attestation={"granted_permissions": ["git_metadata_write"]},
    )
    assert verdict["required_permissions"] == ["git_metadata_write"]
    assert verdict["verdict"] == "granted"

    recorder = _Recorder()
    routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={"granted_permissions": ["git_metadata_write"]},
        execute=recorder,
    )
    # moduleはGitを実行しない。実行したのはcallbackであり、記録は呼出しの記録だけである。
    assert recorder.calls == ["OP-001", "OP-002", "OP-003", "OP-004"]


# ------------------------------------------------------------------ 9. 混在時の一回要求


def test_mixed_write_kinds_are_requested_once_without_later_additions(routing):
    inventory = _inventory(routing, _mixed_operations())

    attempts = []

    def _execute(operation):
        attempts.append(operation["operation_id"])
        return {"status": "completed", "detail": "ok"}

    verdict = routing.run_permission_preflight(
        inventory=inventory, host_attestation={"granted_permissions": []}
    )
    assert verdict["missing_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]
    assert attempts == []

    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation={
            "granted_permissions": ["git_metadata_write", "project_artifact_write"]
        },
        execute=_execute,
    )
    assert attempts == ["OP-001", "OP-002", "OP-003", "OP-004"]
    assert receipt["preflight_ref"]["required_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]
    assert receipt["preflight_ref"]["missing_permissions"] == []


# ---------------------------------------------- receipt整合性の修正（schema v2）
#
# 指示：records/session-handoffs/
#       2026-08-05-codex-to-claude-repair-operation-routing-receipt-integrity.md
#
# receiptは抜粋ではなく完全な検証済みpreflight recordを持ち、validatorはそれをinventoryに対して
# 再計算で検証する。自己Digestを合わせ直した改竄も受理しない。


def _granted_both():
    return {"granted_permissions": ["git_metadata_write", "project_artifact_write"]}


def _receipt_for(routing, operations, recorder=None):
    inventory = _inventory(routing, operations)
    receipt = routing.execute_with_preflight(
        inventory=inventory,
        host_attestation=_granted_both(),
        execute=recorder or _Recorder(),
    )
    return inventory, receipt


def _reseal(document):
    """改竄後に自己Digestを計算し直す。改竄をDigestで隠せないことを示すため。"""

    document["content_digest"] = _digest(document)
    return document


def test_receipt_with_emptied_preflight_requirements_is_rejected(routing):
    inventory, receipt = _receipt_for(routing, _mixed_operations())
    assert routing.validate_execution_receipt(receipt, inventory=inventory) is True

    tampered = json.loads(json.dumps(receipt))
    tampered["preflight_ref"]["required_permissions"] = []
    tampered["preflight_ref"]["missing_permissions"] = []
    _reseal(tampered["preflight_ref"])
    _reseal(tampered)

    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_execution_receipt(tampered, inventory=inventory)
    assert error.value.code in (
        "receipt_identity_mismatch", "preflight_requirement_mismatch",
    )


def test_receipt_carries_a_complete_revalidatable_preflight(routing):
    inventory, receipt = _receipt_for(routing, _mixed_operations())
    embedded = receipt["preflight_ref"]

    assert embedded["record_kind"] == "operation_permission_preflight"
    assert embedded["inventory_ref"] == {
        "inventory_id": inventory["inventory_id"],
        "inventory_version": inventory["inventory_version"],
        "content_digest": inventory["content_digest"],
    }
    assert routing.validate_permission_preflight(embedded, inventory=inventory) is True


def test_standalone_preflight_with_wrong_requirements_is_rejected(routing):
    inventory = _inventory(routing, _mixed_operations())
    preflight = routing.run_permission_preflight(
        inventory=inventory, host_attestation=_granted_both()
    )
    assert routing.validate_permission_preflight(preflight, inventory=inventory) is True

    emptied = _reseal(dict(preflight, required_permissions=[]))
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_permission_preflight(emptied, inventory=inventory)
    assert error.value.code == "preflight_requirement_mismatch"

    widened = _reseal(
        dict(
            preflight,
            required_permissions=[
                "git_metadata_write", "project_artifact_write", "project_artifact_write",
            ],
        )
    )
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_permission_preflight(widened, inventory=inventory)
    assert error.value.code == "preflight_requirement_mismatch"


def test_standalone_preflight_with_inconsistent_missing_or_verdict_is_rejected(routing):
    inventory = _inventory(routing, _mixed_operations())
    approval = routing.run_permission_preflight(
        inventory=inventory, host_attestation={"granted_permissions": []}
    )
    assert approval["verdict"] == "approval_required"
    assert routing.validate_permission_preflight(approval, inventory=inventory) is True

    # missingを空にしてverdictだけgrantedへ寄せる。grantedは空のままである。
    forged = _reseal(dict(approval, missing_permissions=[], verdict="granted"))
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_permission_preflight(forged, inventory=inventory)
    assert error.value.code == "preflight_requirement_mismatch"

    # missingは正しいのにverdictだけgrantedにする。
    verdict_only = _reseal(dict(approval, verdict="granted"))
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_permission_preflight(verdict_only, inventory=inventory)
    assert error.value.code == "preflight_verdict_mismatch"

    # 語彙外の取得済み権限を申告する。
    unknown_grant = _reseal(dict(approval, granted_permissions=["superuser"]))
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_permission_preflight(unknown_grant, inventory=inventory)
    assert error.value.code == "host_attestation_invalid"


def test_valid_read_only_and_mixed_receipts_stay_green(routing):
    read_only_inventory = _inventory(routing, _read_only_operations())
    read_only_receipt = routing.execute_with_preflight(
        inventory=read_only_inventory,
        host_attestation={"granted_permissions": []},
        execute=_Recorder(),
    )
    assert routing.validate_execution_receipt(
        read_only_receipt, inventory=read_only_inventory
    ) is True
    assert read_only_receipt["preflight_ref"]["required_permissions"] == []

    mixed_inventory, mixed_receipt = _receipt_for(routing, _mixed_operations())
    assert routing.validate_execution_receipt(
        mixed_receipt, inventory=mixed_inventory
    ) is True
    assert mixed_receipt["preflight_ref"]["required_permissions"] == [
        "git_metadata_write", "project_artifact_write",
    ]


def test_receipt_schema_version_two_is_required(routing):
    inventory, receipt = _receipt_for(routing, _mixed_operations())
    assert receipt["schema_version"] == 2
    assert routing.RECEIPT_SCHEMA_VERSION == 2
    assert routing.SCHEMA_VERSION == 1
    assert inventory["schema_version"] == 1
    assert receipt["preflight_ref"]["schema_version"] == 1

    legacy = _reseal(dict(receipt, schema_version=1))
    with pytest.raises(routing.OperationRoutingError) as error:
        routing.validate_execution_receipt(legacy, inventory=inventory)
    assert error.value.code == "receipt_schema_version_unsupported"


def test_no_callback_runs_for_any_stop_condition(routing):
    """unknown、external、権限不足のいずれでもcallbackは一度も呼ばれない。"""

    recorder = _Recorder()

    unknown_inventory = _inventory(
        routing, [_operation("OP-1", "unknown", ["x"], "判定不能")]
    )
    with pytest.raises(routing.OperationRoutingError):
        routing.execute_with_preflight(
            inventory=unknown_inventory, host_attestation=_granted_both(), execute=recorder
        )

    external_inventory = _inventory(
        routing, [_operation("OP-1", "external", ["send"], "外へ出す")]
    )
    with pytest.raises(routing.OperationRoutingError):
        routing.execute_with_preflight(
            inventory=external_inventory, host_attestation=_granted_both(), execute=recorder
        )

    write_inventory = _inventory(routing, _mixed_operations())
    with pytest.raises(routing.OperationRoutingError):
        routing.execute_with_preflight(
            inventory=write_inventory,
            host_attestation={"granted_permissions": []},
            execute=recorder,
        )

    assert recorder.calls == []
