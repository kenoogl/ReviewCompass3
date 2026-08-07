# 統合除外宣言 初版entry 承認Decision v1

- decision ID：`DEC-INTEGRATION-EXCLUSION-ENTRIES-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「承認」（2026-08-07。初版entry候補3件の提示後）

## 1. Humanの決定

初版entry候補一覧（`records/development/2026-08-07-integration-exclusion-entries-candidate-v1.md`、
SHA-256 `4e248b680f894c93dfe75ad954c3f5f658e9f99d652614048567b1aa5e67cb8d`）の3件を、
提示どおりの粒度で承認した。

- **E1**（`frozen_lane`）：旧Pilot subject固定の検証器群（関数単位3件）
- **E2**（`version_pinned`）：Intake v2版のrecord検証経路（config＋経路単位）
- **E3**（`historical_retained`）：旧37要件の決定的移行器（file単位）

## 2. 承認により許可されること

- 承認済み3 entryを内容とする除外宣言record・schema・検証器・除外判定helperの、
  test-first実装（`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`構成A-1の実装単位）
- 実装は確立済みの関門（実装前再利用検索gate、宣言→RED対応表——照合は恒久検査器、RED固定）を通す

## 3. この決定が承認していないこと

- entryの追加・削除（後継versionの候補提示とHuman裁定を経る）
- 除外対象codeの削除・変更・レビュー免除（除外は「統合しない」の宣言のみ）
- 構成A-2（順位表）以降の実装
