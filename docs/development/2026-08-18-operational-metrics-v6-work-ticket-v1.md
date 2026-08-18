# 運用集計v6（時系列復元・欠落由来）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v6（時系列復元）へ」（2026-08-18 chat）
- 種別：範囲固定文書（軽量作業票）。読み取り専用の集計拡張のみ。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-18-operational-metrics-v6-prescan-v1.md`

## 1. 正本範囲

1. `tools/evaluation/operational_metrics.py`：事前走査§2の2集計を追加——
   (a) コスト時系列＝系統dir別のfile数・行数・厳密／緩いtool_use計数・先頭末尾timestamp差の合計
   （解釈不能はduration_unrecognizedへ）、(b) 欠落由来＝missing_deleted／missing_never／
   missing_absoluteのcounts。内容の転記・絶対path出力なし。schema 6。
2. 試験の追加（RED先行）3本：(a) 系統別のtool_use計数と行数、(b) timestamp解釈不能fileの明示
   計上、(c) 欠落由来の3分類（git fixture）。既存18本無変更（schema固定は意図保存で6へ）。
3. dataset v6の実データ固定＋Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外（v7候補）

系統hashの意味づけ・道具呼び出しの系統横断正規化・rawの意味解析。

## 3. 受入条件

1 RED：追加3本のみ失敗／2 GREEN：21本単独0／3 実データ0・dataset v6固定・v1〜v5不変・
絶対path出力なし（grep該当なし）／4 計画writer仕上げ・証明書start_allowed: true／
5 diff・意味単位commit・transition合格。

## 4. Humanの確認が要る点（覆せる形）

厳密／緩い二本立て計数の採否（単一解釈を全系統へ当てない設計）。
