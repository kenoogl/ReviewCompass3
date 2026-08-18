# 運用集計v5（H4手動記入・コスト第一段）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v5（H4手動記入・コスト）へ」（2026-08-18 chat）
- 種別：範囲固定文書（軽量作業票）。読み取り専用の集計拡張のみ。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-18-operational-metrics-v5-prescan-v1.md`

## 1. 正本範囲

1. `tools/evaluation/operational_metrics.py`：事前走査§2の2集計を追加——
   (a) H4自動導出率＝request_builderの3類型の雛形をin-memory生成し`<<記入:`欄数と機械欄数から
   機械算出、(b) コスト第一段＝保全先の区画別file数・総byte・日付範囲の流し読み集計
   （内容不読・絶対path非出力）。`--preservation-root`は任意引数（既定＝保全先の正準path）。
   `schema_version` 5。
2. 試験の追加（RED先行）3本：(a) 3類型の自動導出率が算出される、(b) 保全先集計が区画別に
   件数・byteを返す、(c) 保全先出力へ絶対pathが含まれない。既存15本は無変更
   （schema固定は意図保存で5へ）。
3. dataset v5の実データ固定＋Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外（v6へ繰り越し）

道具呼び出し数・時間の時系列復元（rawの全文解析）・欠落34の由来特定。

## 3. 受入条件

1 RED：追加3本のみ失敗／2 GREEN：18本単独0／3 実データ0・dataset v5固定・v1〜v4不変／
4 計画writer仕上げ・証明書start_allowed: true／5 diff・意味単位commit・transition合格。

## 4. Humanの確認が要る点（覆せる形）

コスト第一段を規模集計に絞る裁定（時系列parserはv6）。
