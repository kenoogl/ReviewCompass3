# 構成B 再利用検索の鮮度判定 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §3（構成B。閾値「対象範囲のfileに観測後の変更が
  1件でもあれば停止」は承認済み初版値）
- 実装前検索record（gate通過済み）：
  `records/development/2026-08-07-reuse-search-freshness-reuse-search-v1.json`
  （該当38 routine、hit 194件。snapshot・observation取り扱いの既存部品を捕捉）

## 1. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work4b-b-reuse-search-freshness-declaration-red-map-v1.json`
（`RC3-WORK4B-B-REUSE-SEARCH-FRESHNESS-DECLARATION-RED-MAP-001`）。照合は恒久検査器で`passed`、
宣言4件（F1〜F4）、testの無い宣言0件。

## 2. RED結果（機械実行、終了コード直接判定）

- 対象test：`tests/test_reuse_search_freshness.py` 4 test、exit `1`
  （`search_existing_routines`が`observation_document`・`project_root`を受け取らず、
  freshness機能が未実装のため。期待どおりのRED）
- 既存全Test（対象fileを除外）：exit `0`

## 3. 設計上の決定（記録）

- 鮮度の機械的基準は観測recordの`files`欄（path＋file SHA-256、v3.3実観測は101 file）とする。
- 検索recordはschema_version 2へ進め、`freshness`欄を必須とする。**schema 1の既存record 4件は
  版固定のまま検証・gate通過を維持する**（統合除外宣言E2と同じ原則。旧recordを新規則で
  再判定しない）。
- 観測を渡さない生成はschema 1のまま（freshness無し）とし、gateは`freshness: not_assessed`を
  明示して通す。既定でstaleにしない理由：既存の固定test（R4・R7）が観測なしfixtureでの
  gate通過を固定しており、これを弱めないため。実運用の検索は観測を渡す。この緩さは
  black hole候補として次のHuman判断材料に含める。
