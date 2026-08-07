# 構成C 検索recordの外部化 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §4
- 実装前検索record（schema 2、gate `assessed_fresh`）：
  `records/development/2026-08-07-reuse-search-externalization-reuse-search-v1.json`
  （該当140 routine。Work 4Aのlocator・attestation機構ほか外部参照系の既存部品を捕捉）

## 1. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work4b-c-externalization-declaration-red-map-v1.json`。
照合は恒久検査器で`passed`、宣言4件（H1〜H4）、testの無い宣言0件。

## 2. RED結果（機械実行、終了コード直接判定）

- 対象test：`tests/test_reuse_search_externalization.py` 4 test、exit `1`
  （外部化・証明書gate・移行の各関数が未実装のため。期待どおりのRED）
- 既存全Test（対象fileを除外）：exit `0`

## 3. 設計上の決定（記録）

- 証明書（`reuse_search_attestation`）はWork 4Aの証明書方式を踏襲し、外部相対path・
  content digest・**byte SHA-256**・source identity・hit件数を持つ。gateはbyte一致まで確認する。
- 外部rootの解決はcaller渡し（`data_root`引数）とし、test可能性を保つ。実運用の解決は
  Layout v3の既存規則（`resolve_data_root`）を使う。
- 移行（H4）は既存6件を対象に、byte一致検証・旧位置保持で行う。旧位置の削除は別途Human判断
  （書庫移行と同じ扱い）。
