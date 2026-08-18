# 運用集計v4（基点別解決・履歴照合）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v4へ」（2026-08-18 chat）
- 記録者：Claude
- 上位：v3 Evidence §5の繰り越し
- 基準commit：`8b01b58`（作業tree clean・push済み）
- 実測の入力：dataset v3（SHA-256 `ef79c8e506cd0e276a80a1bb0a8ed17d2d337ce89925ec8c25b107001859ffbb`）
  ——欠落34・不一致311はv3の機械集計値を固定入力とする（再測定はv4実行時に装置が行う）

## 1. 設計（作業票へ渡す論点）

1. **基点別解決**：repo rootで解決できない相対pathを、機械導出の代替基点
   （`formal_code_reuse_search.default_runtime_root()`配下の
   `projects/reviewcompass3/development/data`＝work4a/work4b記録の実基点）で再解決し、
   `external_match`／`external_differs`へ分類。どこにも無いものだけを`file_missing`に残す。
2. **履歴照合**：repo相対の`digest_differs`について、`git rev-list HEAD -- <path>`の各版の内容
   SHA-256を照合し、一致が見つかれば`history_match`（**版の前進＝追跡可能**）、無ければ
   `true_mismatch`。1 pathあたり照合上限200版（超過は`history_capped`へ明示計上——黙って
   打ち切らない）。gitからの取得は読み取り専用。
3. dataset v4（schema_version 4）として新版固定。v1〜v3不変。
4. v5へ明示繰り越し：H4手動記入率・コスト（セッションログ時系列）。

## 2. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-18-operational-metrics-v4-attestation-v1.json`。

## 3. 未実施

手順5、作業票の適用、RED、GREEN、dataset v4固定、Evidence、TODO・見取り図反映。
