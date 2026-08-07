"""層2（機械が支援する）：分類の下限規則、pathspec形式検査、除外の影響件数表示。

承認：DEC-VERIFICATION-BOUNDARY-001（層2。安全保証ではなく誤記検出であることの明示を要件とする）
所見：反証O-1、A-1、X-2
"""

import json
from pathlib import Path

import pytest

from tools.development import integration_exclusions as ix
from tools.development import operation_routing as orouting
from tools.development import structured_argv_executor as argvx


# ---------------------------------------------------------------- O-1：分類の下限


def _inventory(argv, classification="read_only", operation_id="OP-1"):
    return orouting.build_operation_inventory(
        inventory_id="INV-LAYER2",
        operations=[{
            "operation_id": operation_id,
            "classification": classification,
            "argv": argv,
            "summary": "fixture",
        }],
    )


def test_o1_destructive_argv_cannot_claim_read_only():
    """反証O-1：`rm -rf /`を読み取り専用と申告できてはならない。"""

    with pytest.raises(orouting.OperationRoutingError) as error:
        _inventory(["rm", "-rf", "/"])
    assert "classification_below_minimum" in str(error.value)


def test_o1_push_cannot_claim_read_only():
    with pytest.raises(orouting.OperationRoutingError):
        _inventory(["git", "push", "origin", "main"])


def test_o1_read_only_command_is_accepted():
    """正例：実際に読み取り専用の操作は通る。"""

    inventory = _inventory(["git", "status", "--porcelain"])
    assert orouting.required_permissions(inventory) == []


def test_o1_minimum_rule_declares_it_is_not_a_safety_guarantee():
    """層2の要件：誤記検出であって安全保証ではないことを機械可読に宣言する。"""

    declaration = orouting.classification_minimum_rules()
    assert declaration["guarantee"] == "typo_detection_not_safety"
    assert declaration["coverage"] == "known_cases_only"
    assert any("rm" in entry["argv_head"] for entry in declaration["rules"])


# ---------------------------------------------------------------- A-1：pathspec


def _read_only_inventory(argv):
    return orouting.build_operation_inventory(
        inventory_id="INV-ARGV",
        operations=[{
            "operation_id": "OP-GIT",
            "classification": "read_only",
            "argv": argv,
            "summary": "fixture",
        }],
    )


def _runner(recorded):
    def run(argv, *, cwd):
        recorded.append(list(argv))

        class Result:
            returncode = 0
            stdout = ""
            stderr = ""

        return Result()

    return run


def test_a1_option_shaped_pathspec_is_rejected(tmp_path):
    """反証A-1：区切りの後ろにoptionを紛れ込ませられてはならない。"""

    inventory = _read_only_inventory(
        ["git", "status", "--porcelain", "--", "--output=/tmp/pwned"]
    )
    recorded = []
    with pytest.raises(argvx.StructuredArgvExecutorError) as error:
        argvx.run_read_only_operations(
            inventory=inventory, host_attestation={"granted_permissions": []},
            project_root=tmp_path, cwd=".", runner=_runner(recorded),
        )
    assert "pathspec_invalid" in str(error.value)
    assert recorded == [], "nothing may be executed when the pathspec is rejected"


def test_a1_absolute_pathspec_is_rejected(tmp_path):
    inventory = _read_only_inventory(
        ["git", "status", "--porcelain", "--", "/etc/passwd"]
    )
    with pytest.raises(argvx.StructuredArgvExecutorError):
        argvx.run_read_only_operations(
            inventory=inventory, host_attestation={"granted_permissions": []},
            project_root=tmp_path, cwd=".", runner=_runner([]),
        )


def test_a1_parent_escape_pathspec_is_rejected(tmp_path):
    inventory = _read_only_inventory(
        ["git", "status", "--porcelain", "--", "../outside"]
    )
    with pytest.raises(argvx.StructuredArgvExecutorError):
        argvx.run_read_only_operations(
            inventory=inventory, host_attestation={"granted_permissions": []},
            project_root=tmp_path, cwd=".", runner=_runner([]),
        )


def test_a1_ordinary_pathspec_is_accepted(tmp_path):
    """正例：普通のpathspecは通り、そのまま実行される。"""

    inventory = _read_only_inventory(
        ["git", "status", "--porcelain", "--", "tools/development"]
    )
    recorded = []
    argvx.run_read_only_operations(
        inventory=inventory, host_attestation={"granted_permissions": []},
        project_root=tmp_path, cwd=".", runner=_runner(recorded),
    )
    assert recorded and recorded[0][-1] == "tools/development"


# ---------------------------------------------------------------- X-2：影響件数


def _exclusions(tmp_path, targets):
    approval = tmp_path / "records" / "approval.md"
    approval.parent.mkdir(parents=True, exist_ok=True)
    approval.write_text("# approval\n", encoding="utf-8")
    record = {
        "record_kind": "integration_exclusions", "schema_version": 1,
        "exclusion_id": "X", "exclusion_version": 1,
        "created_at": "2026-08-07T00:00:00+09:00",
        "approval": {"decision_id": "DEC-X", "path": "records/approval.md",
                     "sha256": ix.file_sha256(approval)},
        "entries": [{
            "entry_id": "E1", "reason_kind": "frozen_lane", "targets": targets,
            "rationale": "fixture",
            "authority_refs": [{"decision_id": "DEC-X", "path": "records/approval.md"}],
        }],
    }
    record["content_digest"] = ix.content_digest(record)
    return record


_SYMBOLS = (
    "tools/development/a.py:one",
    "tools/development/a.py:two",
    "tools/development/b.py:three",
    "tools/session_logs/c.py:four",
)


def test_x2_broad_prefix_reports_its_impact(tmp_path):
    """反証X-2：広範囲の除外は、何件を落とすかを見えるようにする。"""

    record = _exclusions(tmp_path, [{"kind": "symbol_prefix", "value": "tools/"}])
    impact = ix.exclusion_impact(record=record, symbol_ids=_SYMBOLS)
    assert impact["total_symbols"] == 4
    assert impact["excluded_symbols"] == 4
    assert impact["by_entry"]["E1"] == 4


def test_x2_narrow_target_reports_a_small_impact(tmp_path):
    record = _exclusions(
        tmp_path, [{"kind": "module_path", "value": "tools/development/b.py"}]
    )
    impact = ix.exclusion_impact(record=record, symbol_ids=_SYMBOLS)
    assert impact["excluded_symbols"] == 1
    assert impact["by_entry"]["E1"] == 1


def test_x2_impact_is_reported_not_enforced(tmp_path):
    """層2の要件：拒否ではなく表示であることを宣言する。"""

    record = _exclusions(tmp_path, [{"kind": "symbol_prefix", "value": "tools/"}])
    impact = ix.exclusion_impact(record=record, symbol_ids=_SYMBOLS)
    assert impact["enforcement"] == "reported_for_human_review"
