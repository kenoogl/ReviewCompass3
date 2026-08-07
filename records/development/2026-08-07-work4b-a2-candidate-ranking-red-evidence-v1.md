# 構成A-2 絞り込み順位表 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §2 A-2
- 実装前検索record（**初のschema 2・鮮度判定付き**、gate `assessed_fresh`）：
  `records/development/2026-08-07-candidate-ranking-reuse-search-v1.json`
  （該当13 routine、hit 101件。除外宣言helper群と順位素材の既存部品を捕捉）

## 1. 再観測（構成Bの初回実運用）

実装前検索に先立ち、既存Work 4A経路で source universe を再観測した【実測】：

| 項目 | 値 |
| --- | --- |
| snapshot_id | `e349bb9c4c3e5d0531a8f889135f6c0e0f8a0cc905327cdd58df0ad07f3d76fa` |
| source_content_id | `82634be2f6437338c2542554dcafd8028a3ae68da676d722d6e4fa6df7a2d6bd` |
| profile_run_id | `079162d49b41c7e4703b4848dd3d3ee8ef892499ff34b0dce042320ada59448c`（routine 1239件、file 118） |
| discovery_run_id | `e7eb2eee5459ebace2d4e2c1116225dc0e5f0af0449718b80d248042296c048f`（group 804件） |
| head / captured_at | `46d5f9bdcca01b747c93f6c6e501fb682d60da50` / `2026-08-07T13:34:52+0900` |

旧identity（routine 1003・group 682、2026-08-05観測）はnew-onlyのまま保持。今週の新設module
（`reuse_search_record.py`等）が検索に映るようになり、鮮度問題の実例が解消された。

## 2. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work4b-a2-candidate-ranking-declaration-red-map-v1.json`。
照合は恒久検査器で`passed`、宣言5件（G1〜G5）、testの無い宣言0件。G4は構成B残余の締め
（staleなProfileからの順位表生成をfail-closedで拒否）を含む。

## 3. RED結果（機械実行、終了コード直接判定）

- 対象test：`tests/test_candidate_ranking.py` 5 test、exit `2`
  （`tools.development.candidate_ranking`未実装によるImportError。期待どおりのRED）
- 既存全Test（対象fileを除外）：exit `0`
