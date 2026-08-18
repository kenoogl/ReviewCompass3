# read_only_entry終了コード統合 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-19
- 指示者：利用者（Human）。文言「read_only_entry独自語彙の統合」（2026-08-19 chat）
- 種別：範囲固定文書（軽量作業票）。**終了コードの値2つを共通語彙へ揃える。判定の意味・JSON出力・
  安全境界は不変**。消費側のgateは0／非0のみを見るため挙動不変（事前走査§1-3の実測）。契約は
  立てない
- 固定入力：事前走査record
  `records/development/2026-08-19-read-only-entry-exit-code-unification-prescan-v1.md`
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`（仕分け＝採用）の残件

## 1. 正本範囲

1. `tools/session_logs/read_only_entry.py`：定数を共通語彙へ（事前走査§2案A）——
   `EXIT_OK=0`不変・partial→`EXIT_UNSUPPORTED=4`・stopped→`EXIT_FAILED=5`（独自名
   `EXIT_PARTIAL`・`EXIT_STOPPED`は廃止）。JSON出力（`status`・`error`欄）は不変。
2. 試験（RED先行）：新設1本＝`cli.py`との値一致pin。意図保存の期待値更新＝
   `tests/test_session_log_read_only_entry.py`（parametrize 3→4・4→5、直接assert 4箇所）・
   `tests/test_session_artifact_safe_storage_entry.py`（模擬値を(4,"partial")・(5,"stopped")へ
   現行化。gate検査の意図＝0以外は転送せず停止、は不変）。
3. Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外

- `safe_storage_entry.py`自身の語彙（0・生の数字3・stopped=4）——storage系の外向き取り決めで
  消費側分析が別途要る。観測記録→改善候補routeへ（登録はHuman仕分け）。
- `cli.py`の語彙定義そのもの。包み役（`record_run.py`）。
- RQ2ケース材料`docs/evaluation/rq2-cases/`（封緘済み複製）と正解表。

## 3. 受入条件

1. RED：新設pin試験＋期待値更新済み試験が実装前に失敗（単独終了コード非0）。
2. GREEN：session_log系・session_artifact系・redaction系の全試験が単独終了コード0
   （本数は実行時に機械計数して記録）。
3. safe_storage gate（0以外は転送せず停止）の意図不変を試験で機械確認。
4. 計画writer仕上げ・証明書`start_allowed: true`。
5. RQ2封緘材料の無変更（tracked差分なしの機械確認）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 4. Humanの確認が要る点（覆せる形）

1. 対応表＝partial→4・stopped→5（停止理由別の細分は採らない。詳細はJSONの`error`欄が運ぶ）。
2. 独自定数名の廃止（共通語彙名への改名。外部参照なしは実測済み）。
3. safe_storage_entry語彙の扱い＝範囲外・観測記録→改善候補route。
