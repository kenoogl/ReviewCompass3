# read_only_entry終了コード統合 実行Evidence v1

- 記録日：2026-08-19。指示者：利用者（Human）「read_only_entry独自語彙の統合」（chat）
- 範囲固定：作業票
  `docs/development/2026-08-19-read-only-entry-exit-code-unification-work-ticket-v1.md`／
  事前走査同prescan v1。基準`48ba5d3`→文書・計画（writer）`fec768e`→証明書`b706c7e`→
  実装は本record同一commit
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`（仕分け＝採用）の残件。本作業で同候補の
  scope（partialの値決定・語彙統一の判断・消費側と保護試験の機械確認）は全消化

## 1. 成果物

`tools/session_logs/read_only_entry.py`の終了コードを部分系共通の語彙へ統合——ok=0不変・
partial=3→**4**（`EXIT_UNSUPPORTED`）・stopped=4→**5**（`EXIT_FAILED`）。独自定数名
（`EXIT_PARTIAL`・`EXIT_STOPPED`）は廃止し共通語彙名へ改名（外部参照なしは事前走査で実測済み）。
JSON出力（`status`・`error`欄）・安全境界は不変。試験は新設1本＝`cli.py`との値一致pin、
意図保存更新＝direct試験の期待値（parametrize 2箇所・直接assert 4箇所）と
safe_storage_entry試験の模擬値現行化（gate検査の意図＝0以外は転送せず停止、は不変）。

## 2. RED→GREEN

RED＝意図した11件のみ失敗（`11 failed, 13 passed`・terminal転記。期待値更新済み試験＋pin試験。
safe_storage側のgate検査は模擬値更新後も**実装前に合格**＝gateが値非依存（0／非0のみ）である
ことの傍証）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-19-read-only-entry-exit-code-unification-evidence-measurements-v1.md`
参照**（session系53file・348本exit 0・統合後3入口の定数行の機械転記・`safe_storage_entry.py`の
digest不変＝消費側無変更の機械証明・RQ2封緘材料のtracked差分なし・全entry二重実行一致）。
`git diff --check`合格。

## 3. 統合後の姿

- 部分系の実行入口3つ（`cli.py`・`read_only_entry.py`・`eventual_preservation.py`）の終了コードが
  同値同義——**0=ok・4=非対応（partial）・5=失敗（fail-closed停止）**。同じ数字が入口によって
  逆の意味になる並存（partial=3と対象なし=3、停止=4と非対応=4）は解消。
- 値一致はpin試験で機械固定（独自値の再導入をここで検出）。
- 消費側（`safe_storage_entry.py`のgate）は挙動・byteとも不変。

## 4. 観測（範囲外・改善候補routeへ）

`safe_storage_entry.py`自身の語彙は0・生の数字3（`StorageIncomplete`）・stopped=4のまま
（storage系の外向き取り決めで、消費側分析が別途要る）。本Evidenceを観測記録とし、改善候補への
登録要否はHuman仕分けへ委ねる。

## 5. 未実施

TODO・見取り図反映とcommit。push（利用者の運用に従う）。§4の改善候補登録の要否判断。
