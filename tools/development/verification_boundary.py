"""検証境界の宣言（層3）：機械が保証しない箇所を明示する。

承認：DEC-VERIFICATION-BOUNDARY-001

反証レビュー第1束で、機械では真偽を判定できない箇所が特定された。文章の真偽は文章では
検証できず、host側の実際の権限はproject内からは確かめられない。これらを黙って通すのではなく、
**検証していないと表示する**ことが層3の役割である。

宣言と実装の対応が崩れたら検出できるよう、対象record種別とfieldを機械可読に持ち、
`verify_declaration_targets`で解決を確認する。
"""

import json
from pathlib import Path

_FIELDS = (
    {
        "finding_id": "O-2",
        "classification": "designed_boundary",
        "carried_by": "host",
        "record_kind": "operation_permission_preflight",
        "field": "host_attestation.granted_permissions",
        "reason": (
            "取得済み権限はcallerの申告である。承認と権限確認はhost側に置くと定めており、"
            "project内では検証しない。"
        ),
        "authority_decision": "DEC-MACHINE-OPERATION-ROUTING-001",
        "declared_in": "tools/development/operation_routing.py",
    },
    {
        "finding_id": "O-3",
        "classification": "designed_boundary",
        "carried_by": "host",
        "record_kind": "operation_permission_preflight",
        "field": "verdict",
        "reason": (
            "権限名を申告すればgrantedになる。実際に権限を持つかはhost側で検証される前提であり、"
            "project内の判定は必要権限の計算に留まる。"
        ),
        "authority_decision": "DEC-MACHINE-OPERATION-ROUTING-001",
        "declared_in": "tools/development/operation_routing.py",
    },
    {
        "finding_id": "O-4",
        "classification": "unverifiable_prose",
        "carried_by": "human",
        "record_kind": "operation_execution_receipt",
        "field": "results[].detail",
        "reason": (
            "実行内容の説明は自由文であり、実際に何が実行されたかを証明しない。"
            "証明が要る場合は外部receiptによる別設計を要する。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "declared_in": "tools/development/operation_routing.py",
    },
    {
        "finding_id": "I-1",
        "classification": "unverifiable_prose",
        "carried_by": "human",
        "record_kind": "human_triage_decision",
        "field": "rationale",
        "reason": (
            "Humanの裁定文は自由文であり、実際の発言との一致を機械では確かめられない。"
            "文面の正しさはHumanが確認する。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "declared_in": "tools/development/issue_intake_v4.py",
    },
    {
        "finding_id": "I-2-text",
        "classification": "unverifiable_prose",
        "carried_by": "human",
        "record_kind": "human_triage_decision",
        "field": "decided_at",
        "reason": (
            "決定時刻が実際の決定時点かは機械では確かめられない。版の前後と時刻の前後の"
            "矛盾（単調性）だけは機械化済みであり、それ以外はHumanが担う。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "declared_in": "tools/development/issue_intake_v4.py",
    },
    {
        "finding_id": "P-1",
        "classification": "unverifiable_prose",
        "carried_by": "human",
        "record_kind": "improvement_candidate",
        "field": "proposed_action",
        "reason": (
            "提案文は判断材料であり、実行権限を持たない。内容の妥当性は仕分けの際に"
            "Humanが判断する。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "declared_in": "tools/development/issue_resolution_pilot.py",
    },
    {
        "finding_id": "C-2-meaning",
        "classification": "unverifiable_prose",
        "carried_by": "human",
        "record_kind": "declaration_red_map",
        "field": "declarations[].summary",
        "reason": (
            "宣言の説明が意味を成すかは機械では判定できない。空文字の拒否は機械化済みであり、"
            "説明の質はレビューでHumanが確認する。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "declared_in": "tools/development/declaration_red_map_check.py",
    },
)


def unverified_fields():
    """機械が保証しない箇所の宣言を返す。"""

    return {
        "record_kind": "verification_boundary_declaration",
        "schema_version": 1,
        "layer": "layer3_not_machine_verified",
        "note": (
            "ここに載る箇所は機械が検証していない。合格表示は「検証した」ではなく"
            "「検証対象外」を意味する。確認はHumanまたはhostが担う。"
        ),
        "authority_decision": "DEC-VERIFICATION-BOUNDARY-001",
        "fields": [dict(entry) for entry in _FIELDS],
    }


def verify_declaration_targets(*, project_root="."):
    """宣言が指すmoduleが実在するかを確認し、解決できない参照を返す。"""

    root = Path(project_root)
    unresolved = []
    for entry in _FIELDS:
        if not (root / entry["declared_in"]).is_file():
            unresolved.append(
                {"finding_id": entry["finding_id"], "path": entry["declared_in"]}
            )
    return unresolved


def main(argv=None):
    """宣言をJSONで出力する（人が読む・記録へ写すための最小CLI）。"""

    print(json.dumps(unverified_fields(), ensure_ascii=False, indent=2))
    return 0
