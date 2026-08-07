# 層3（機械は保証しない）GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層3）
- RED Evidence：`records/development/2026-08-07-verification-boundary-layer3-red-evidence-v1.md`

## 1. 実装

`tools/development/verification_boundary.py`を新設し、機械が保証しない7項目を機械可読な宣言と
して固定した。

| 項目 | 対象 | 区分 | 担い手 |
| --- | --- | --- | --- |
| O-2、O-3 | host申告の取得済み権限と判定 | `designed_boundary` | host |
| O-4 | 実行結果の説明文 | `unverifiable_prose` | Human |
| I-1 | Human裁定文 | `unverifiable_prose` | Human |
| I-2-text | 決定時刻の文面（単調性は層1で機械化済み） | `unverifiable_prose` | Human |
| P-1 | 候補の提案文 | `unverifiable_prose` | Human |
| C-2-meaning | 宣言説明の意味的妥当性（空文字拒否は層1で機械化済み） | `unverifiable_prose` | Human |

宣言には**「合格表示は『検証した』ではなく『検証対象外』を意味する」**と明記した。
O-2・O-3は欠陥ではなく設計どおりの境界であり、根拠Decision（`DEC-MACHINE-OPERATION-ROUTING-001`）
を持たせた。`verify_declaration_targets`で宣言が指すmoduleの実在を確認し、解決できない参照が
0件であることをtestで固定した。

**レビュー手順書へ導線を追加**し、reviewerがこの一覧を「Humanが確認すべき対象」として扱えるように
した（Z6で固定）。

- targeted：`tests/test_verification_boundary_layer3.py` 6 test。RED 6 → GREEN 6。
- 公式全Test：`1131 passed`、exit `0`。

## 2. A案の効果が確認された（記録）

手順書を再び改定したが、**Work 5B Contractのtestは壊れなかった**。`DEC-FIXED-SOURCE-KIND-001`で
導入した`pinned_at_start`（上流の可変文書は開始時点のpinであり、改定による不一致は正常）が
意図どおり機能した。同じ改定が前回はContract testを壊して作業を止めていたことと対照的である。
**設計判断の効果が2回目の改定で実証された。**

TODO側の参照Digestは機械更新で解消した（可変文書を指す参照の宿命であり、
`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の領域）。

## 3. 検証境界の全11件が完了

| 層 | 件数 | 状態 |
| --- | --- | --- |
| 層1（機械が保証する） | 5 | 完了（C-4、C-1 scope欄、R-3、C-2空文字、I-2単調性） |
| 層2（機械が支援する） | 3 | 完了（O-1、A-1、X-2。誤記検出であることを宣言） |
| 層3（機械は保証しない） | 7項目 | 完了（明示。うちO-2・O-3は設計どおりの境界） |

反証レビュー第1束で成立した21件は、9件を第1次修正、8件を層1・層2で機械化、残りを層3で明示、
という形ですべて処置された。

## 4. 残余

- 反証レビュー第2束（stage期module群、`tools/session_logs/`の伏字化系ほか）は未着手。
- 合意順序④（RC2資産の取り込み、外部APIによる独立レビュー）も未着手。層3の項目は
  「Humanが担う」と宣言したが、その確認をどう設計するかはWork 8の評価対象である。
