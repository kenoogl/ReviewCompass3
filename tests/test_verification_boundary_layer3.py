"""層3（機械は保証しない）：検証していない箇所を機械可読に明示する。

承認：DEC-VERIFICATION-BOUNDARY-001（層3）
所見：反証O-2・O-3（host権限の自己申告）、O-4（実行結果の説明文）、
I-1（Human裁定文）、P-1（候補の提案文）、C-2（説明の意味的妥当性）
"""

import json
from pathlib import Path

import pytest

from tools.development import verification_boundary as vb


def test_z1_declaration_lists_every_unverified_field():
    """層3の全件が宣言に載っていること。"""

    declaration = vb.unverified_fields()
    identifiers = {entry["finding_id"] for entry in declaration["fields"]}
    assert identifiers == {"O-2", "O-3", "O-4", "I-1", "I-2-text", "P-1", "C-2-meaning"}


def test_z2_each_entry_states_who_carries_it():
    """各項目に、機械が保証しない理由と担い手が書かれていること。"""

    for entry in vb.unverified_fields()["fields"]:
        assert entry["carried_by"] in ("human", "host")
        assert entry["reason"].strip()
        assert entry["record_kind"].strip()
        assert entry["field"].strip()


def test_z3_declared_targets_exist_in_the_repository():
    """宣言が指すrecord種別とfieldが、実在の形式と対応していること。"""

    unresolved = vb.verify_declaration_targets(project_root=Path("."))
    assert unresolved == []


def test_z4_host_boundary_is_declared_as_design_not_defect():
    """host権限の自己申告は欠陥ではなく設計どおりの境界であると明示する。"""

    entries = {
        entry["finding_id"]: entry for entry in vb.unverified_fields()["fields"]
    }
    for finding_id in ("O-2", "O-3"):
        assert entries[finding_id]["carried_by"] == "host"
        assert entries[finding_id]["classification"] == "designed_boundary"
        assert entries[finding_id]["authority_decision"] == (
            "DEC-MACHINE-OPERATION-ROUTING-001"
        )


def test_z5_free_text_entries_are_marked_as_unverifiable_prose():
    """自由文の項目は、機械では真偽を判定できないと明示する。"""

    entries = {
        entry["finding_id"]: entry for entry in vb.unverified_fields()["fields"]
    }
    for finding_id in ("O-4", "I-1", "I-2-text", "P-1", "C-2-meaning"):
        assert entries[finding_id]["classification"] == "unverifiable_prose"
        assert entries[finding_id]["carried_by"] == "human"


def test_z6_declaration_is_reachable_from_the_review_protocol():
    """レビュー手順書から宣言へ辿れること（人が確認すべき対象として見える）。"""

    protocol = Path("docs/development/work-review-protocol.md").read_text(
        encoding="utf-8"
    )
    assert "verification_boundary" in protocol or "検証していない" in protocol
