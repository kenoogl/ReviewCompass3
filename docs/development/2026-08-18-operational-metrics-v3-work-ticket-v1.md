# 運用集計v3（書式C照合）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「候補1」（2026-08-18 chat）
- 種別：範囲固定文書（軽量作業票）。既存集計装置への読み取り専用の集計拡張のみ。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-operational-metrics-v3-prescan-v1.md`

## 1. 正本範囲

1. `tools/evaluation/operational_metrics.py`：書式C（表cell束縛）の組抽出を事前走査§2-1の
   fail-closed規則で追加。`schema_version`を3へ。既存欄の意味不変。
2. 試験の追加（RED先行）：`tests/test_operational_metrics.py`へ3本——(a) 2列・3列の表行の組が
   採点される、(b) **hexがfile名の一部の行を採点しない**（偽装fixture）、(c) pathの無いhex行は
   unpairedへ。既存9本は無変更。
3. dataset v3の実データ固定＋実行Evidence（guard付き測定ブロック）。

## 2. 範囲外（v4へ繰り越し）

H4手動記入率・コスト（セッションログ時系列parser）・`digest_differs`のgit履歴照合。

## 3. 受入条件

1. RED：追加3本のみ失敗。2. GREEN：12本単独0（決定的射影で固定）。3. 実データ実行0・
dataset v3固定（v1・v2不変）。4. 検索計画はwriter仕上げ・証明書`start_allowed: true`。
5. diff・意味単位commit・transition合格。

## 4. Humanの確認が要る点（覆せる形）

書式Cの組定義（1 hex-cell×1 path-cellの行のみ採点）の採否。
