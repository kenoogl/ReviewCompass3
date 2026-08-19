# AGENTS §4 復路writer反映 Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：運用規範（AGENTS.md §4・改善候補経路の復路手順）の更新

## 1. 承認文言【記録】

> AGENTS §4へ復路writerも反映して、プッシュ

（2026-08-19 chat）

## 2. 変更内容【実測】

AGENTS.md §4の改善候補経路の規則へ、復路の正規手順を追記した：

1. トリアージ決定＝`triage_decision_writer --draft`（組み立て・検証・書き出しの一操作。
   組み立て正本は`build_human_triage_decision`のまま）。
2. Issue昇格＝`issue_record_writer --decision`。
3. issueの状態変更＝`issue_state_transition --issue-id --to-state`。
4. 判定の意味内容はDecision recordへ残し、**検証器のないverdict専用recordは作らない**
   （2026-08-19の設計判断＝案Aの規範化）。

既存の規則（候補writer・一括検証入口・仕分けのDecision record・N1形式・旧置き場凍結・
形式の作り直し禁止）は不変。

更新後のAGENTS.md SHA-256：
`1aabd8fb18fcc5d1b2fd10eee3c9ee2689328e1a23ab3363e9742f3b13a5c6e7`

## 3. 根拠

- 実装と受入：復路writer 3部品と一括検証拡張は試験22本・実repo一発合格で受入済み
  （`records/development/2026-08-19-return-path-writers-evidence-v1.md`）。
- verdict検証器の不在は事前走査で機械確認済み（同prescan §1-3）。
- 保護試験：AGENTS lane guidance系を含む14本が更新後も合格。

## 4. 未実施

なし（本recordとAGENTS.mdの同一commit、その後push）。
