# 運用集計v4（基点別解決・履歴照合）実行Evidence v1

- 記録日：2026-08-18。指示者：利用者（Human）「運用集計v4へ」（chat）
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v4-work-ticket-v1.md`／
  事前走査同prescan v1。基準`8b01b58`→文書・計画（writer）`23bce58`→証明書`2f1ac0b`→実装は本record同一commit

## 1. 成果物

装置へ履歴照合（`git rev-list`＋各版内容SHA-256・上限200版超過は`history_capped`明示）と
基点別解決（work4a/b実基点）を追加。schema 4。試験15本（追加3・schema固定は意図保存で4へ）。
dataset v4を機械固定（v1〜v3不変＝受入測定ブロックでdigest固定）。

## 2. RED→GREEN

RED＝追加3本のみ失敗（terminal転記）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-18-operational-metrics-v4-evidence-measurements-v1.md`参照**
（15本exit 0・全entry二重実行一致）。`git diff --check`合格。

## 3. dataset v4の要旨（H5の確定形）

- **不一致313のうち298（95.2%）は`history_match`＝版の前進で追跡可能**。真の不一致は**13件**・
  照合上限到達2件。一致852と合わせ、**証拠へ機械でたどれる束縛＝1,150／1,199（95.9%）**。
- 正直な記載：external基点（work4a/b実基点1系統）での解決は**0件**——欠落34の基点仮説は
  この系統では当たらなかった。欠落34の個別由来はv5の論点として残る。

## 4. v5へ繰り越し

H4手動記入率・コスト（セッションログ時系列）・欠落34の由来特定。

## 5. 未実施

TODO・見取り図反映とcommit。push（利用者の運用に従う）。
