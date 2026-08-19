# 候補writer・台帳一括検証入口 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-19
- 指示者：利用者（Human）。文言「current_workで採用。候補writerと一括検証入口だけ先に作って」
  （2026-08-19 chat）
- 種別：範囲固定文書（軽量作業票）。開発基盤の新設2 module＋試験。台帳recordのschema・
  既存検証器・保護試験N7は不変。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-19-ledger-writer-prescan-v1.md`
- 対象候補：`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`（current_work・先行2部品）

## 1. 正本範囲

1. `tools/development/improvement_candidate_writer.py`【新設】：草稿→機械埋め込み
   （出所SHA-256・時刻・正準digest）→置き場解決→**v3検証器合格時のみ書き出し**（new-only）。
   一行JSON・exit 0／1。
2. `tools/development/workflow_ledger_verify.py`【新設】：候補置き場のN7同型勘定
   （validator／allowlist／V4決定指紋の3分岐）＋V4決定台帳の全件検証を一操作で。
   `{findings, status, counts}`一行JSON・exit 0／1。既定＝実repo・`--project-root`任意。
3. 試験（RED先行）8〜9本：writer＝合格書き出し・無効語彙の拒否（書き出さない）・上書き拒否・
   `-m`疎通／verify＝fixture緑・破損候補の失敗列挙・allowlist分岐・実repo緑・`-m`疎通。
4. Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外

仕分け決定・issue登録のwriter入口／verdict writerと状態遷移／record schema・検証器・N7試験の
変更／既存台帳recordの改変。残scopeは突合checkpoint枠で再仕分け（決定record §3）。

## 3. 受入条件

1 RED：新設試験のみ失敗／2 GREEN：新設試験単独0＋台帳関連試験群（intake単体・intake v4・
pilot・lane guidance）単独0／3 実repoで`workflow_ledger_verify`単独exit 0（現況＝候補20勘定・
決定52全件合格が期待値）／4 計画writer仕上げ・証明書`start_allowed: true`／5 `git diff --check`・
意味単位commit・`work_unit_transition`合格。

## 4. Humanの確認が要る点（覆せる形）

1. verify出力の形式＝`todo_handoff`型（findings＋status・exit 0／1）。
2. writerはnew-only（既存fileの更新modeは残scope側で判断）。
3. module名2件（`improvement_candidate_writer`・`workflow_ledger_verify`）。
