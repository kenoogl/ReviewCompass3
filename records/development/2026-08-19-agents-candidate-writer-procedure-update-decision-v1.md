# AGENTS §4 改善候補登録手順のwriter反映 Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：運用規範（AGENTS.md §4・改善候補の登録規則）の更新

## 1. 承認文言【記録】

> AGENTS §4の改善候補登録手順へ、writerと一括検証入口を反映して

（2026-08-19 chat）

## 2. 変更内容【実測】

AGENTS.md §4の改善候補登録の規則を次のとおり更新した：

1. 登録は**草稿（意味欄のみ）→候補writer**（`improvement_candidate_writer --draft`）による
   機械埋め込み・検証合格時のみの書き出しへ。置き場への雛形手書き・digest手計算を禁止として明文化。
2. **台帳一括検証の単一入口**（`workflow_ledger_verify`・単独終了コード0＝passed）を健全性確認
   の手段として追記。
3. 既存fileの検証（`issue_resolution_pilot … record <path>`）・仕分け判断のDecision record・
   N1形式・`build_human_triage_decision`・旧置き場凍結の各規則は不変。

更新後のAGENTS.md SHA-256：
`54a2f213f06c630ad234740d10f0977df02c0a0920ce184c0f6e9d4e1b41642e`

## 3. 根拠

- 実害：2026-08-18の検証器未通過4件登録（保護試験N7が3日間赤）と2026-08-19の形式不合格2回
  （`records/development/2026-08-19-n7-candidate-remediation-evidence-v1.md`・
  `records/development/2026-08-19-ledger-writer-evidence-v1.md`）。
- 実装と受入：writer・一括検証入口は新設試験9本と実repo一発合格で受入済み（同Evidence）。
- 保護試験：AGENTS lane guidance系を含む14本が更新後も合格（規範の行き止まり・凍結置き場の
  名指しなしを維持）。

## 4. 未実施

なし（本recordとAGENTS.mdの同一commitのみ）。残scope（決定・issue登録のwriter等）反映は
その実装時に改めて判断する。
