# 復路writer（決定・issue登録・状態遷移）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-19
- 指示者：利用者（Human）。文言「復路（決定・issue・verdictのwriterと状態遷移）の機械化をすぐに
  対応して」（2026-08-19 chat。`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`残scopeの前倒し）
- 種別：範囲固定文書（軽量作業票）。開発基盤の新設3 module＋既設1 moduleの拡張＋試験。
  record schema・検証器・保護試験は不変。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-19-return-path-writers-prescan-v1.md`

## 1. 正本範囲

1. `tools/development/triage_decision_writer.py`【新設】：仕分け決定の草稿→機械組み立て
   （時刻・指紋束縛）→単体検証→new-only書き出し。
2. `tools/development/issue_record_writer.py`【新設】：昇格決定（N1形式）→issue record組み立て→
   単体検証→new-only書き出し→repository検証（失敗時は自file除去で復元）。
3. `tools/development/issue_state_transition.py`【新設】：`--issue-id --to-state`で版遷移
   （state更新・版＋1・`created_at`保存・digest再計算・旧file置換・失敗時rollback）。
   状態語彙・active上限1・重複拒否は既存のrepository検証が機械強制。
4. `tools/development/workflow_ledger_verify.py`【拡張】：issues-v4のrepository検証と状態別
   countsを勘定へ追加（既存欄不変）。
5. 試験（RED先行）12本前後：決定writer 3・issue writer 3・遷移4・verify拡張2。
6. Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外

- **verdict schemaの新設**（事前走査§2案B。判定の意味内容は従来どおり`records/development/`の
  Decision recordが正本。閉じる操作は状態遷移＝案Aで実現）。
- record schema・既存検証器・保護試験・凍結置き場の変更。既存issue 8件の状態変更（突合作業の
  領分。本作業は道具を用意するまで）。

## 3. 受入条件

1 RED：新設試験のみ失敗／2 GREEN：新設試験単独0＋既設writer・verify試験9本単独0＋台帳関連
試験群単独0／3 実repoで拡張後`workflow_ledger_verify`単独exit 0（issue 8件の勘定を含む）／
4 計画writer仕上げ・証明書`start_allowed: true`／5 `git diff --check`・意味単位commit・
`work_unit_transition`合格。

## 4. Humanの確認が要る点（覆せる形）

1. **verdict＝案A**（状態遷移＋Decision record。schema新設なし）。需要が出たら案Bを別候補で起こす。
2. 版遷移は**置換方式**（新版書き出し＋旧版除去。repositoryの同一issue_id重複拒否に従う。
   履歴はgitが保持）。
3. `created_at`は初版の値を保存（遷移時刻はgit履歴とDecision recordが持つ）。
4. issue writerはN1形式のみ（bundle形式の決定は歴史扱い）。
