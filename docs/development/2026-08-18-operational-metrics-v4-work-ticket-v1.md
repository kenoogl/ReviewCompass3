# 運用集計v4（基点別解決・履歴照合）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v4へ」（2026-08-18 chat）
- 種別：範囲固定文書（軽量作業票）。読み取り専用の集計拡張のみ。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-18-operational-metrics-v4-prescan-v1.md`

## 1. 正本範囲

1. `tools/evaluation/operational_metrics.py`：事前走査§1の2機能（基点別解決・履歴照合）を追加。
   `schema_version` 4。既存欄の意味不変（`digest_differs`は`history_match`＋`true_mismatch`＋
   `history_capped`へ内訳が付く）。
2. 試験の追加（RED先行）3本：(a) 代替基点で一致するpathが`external_match`になる、(b) 過去版と
   一致する不一致が`history_match`になる（一時git repo fixture）、(c) どの版とも一致しない
   不一致が`true_mismatch`になる。既存12本は無変更（schema固定は意図保存で4へ更新）。
3. dataset v4の実データ固定＋Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外（v5へ繰り越し）

H4手動記入率・コスト（セッションログ時系列parser）。

## 3. 受入条件

1 RED：追加3本のみ失敗／2 GREEN：15本単独0／3 実データ0・dataset v4固定・v1〜v3不変／
4 計画writer仕上げ・証明書start_allowed: true／5 diff・意味単位commit・transition合格。

## 4. Humanの確認が要る点（覆せる形）

履歴照合の上限200版（超過はhistory_cappedへ明示）。代替基点を1系統（work4a/b実基点）に限る範囲。
