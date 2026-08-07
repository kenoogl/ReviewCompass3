# 構成A-1 統合除外宣言 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`（設計束）、`DEC-INTEGRATION-EXCLUSION-ENTRIES-001`
  （entry 3件）
- 実装前検索record（gate通過済み）：
  `records/development/2026-08-07-integration-exclusions-helper-reuse-search-v1.json`
  （該当31 routine、hit 310件。歴史allowlist系——機械可読な免除宣言の先例——を捕捉）

## 1. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work4b-a1-integration-exclusions-declaration-red-map-v1.json`
（`RC3-WORK4B-A1-INTEGRATION-EXCLUSIONS-DECLARATION-RED-MAP-001`）。
**照合は恒久検査器`tools/development/declaration_red_map_check.py`で実施**（新規mapへの最初の適用）：
`passed`、宣言4件（X1〜X4）、testの無い宣言0件、実在しない列挙0件、結ばれないtest 0件。

## 2. RED結果（機械実行、終了コード直接判定）

- 対象test：`tests/test_integration_exclusions.py` 5 test、exit `2`
  （`tools.development.integration_exclusions`未実装によるImportError。期待どおりのRED）
- 既存全Test（対象fileを除外）：exit `0`。既存Testは弱めていない。

## 3. 状態と次

本RED作業単位のcommit後、固定testを変更せずGREEN実装し、承認済み3 entry（E1関数単位・
E2経路単位・E3 file単位）で実record
`.reviewcompass/workflow/integration-exclusions/integration-exclusions-001--v1.json`を作成する。
本helperは順位表の候補脱落を決める守り役codeであり既定`high`
（`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の反証レビュー対象に含める）。
