# 運用集計v2（H5束縛表・承認点定義）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「運用集計v2（H5束縛表など）に進んでください」（2026-08-18 chat）
- 記録者：Claude
- 上位：運用集計Evidence v1 §6の繰り越し一覧（`records/development/2026-08-18-operational-metrics-evidence-v1.md`・
  SHA-256 `e7a46f56ee3fcfc573e0947ac1845e5f2a9e916399976800b6c132225fc4d4de`）。
  H5の定義は復元可能性表§3（digest束縛の追跡可能率）
- 基準commit：`e69a322`（作業tree clean・push済み）

## 1. 手順1〜3：束縛書式の機械調査【実測・grep出力の転記】

`records/development/*.md`内の64桁hex出現は**2,386**。書式別の内訳：

| 書式 | 件数 | 機械照合の可否 |
| --- | --- | --- |
| A：shasum形式（`^hex␣␣path$`。機械出力の転記） | **205** | **可**（行内で組が閉じる） |
| B：同一行inline（`` `path`…SHA-256 `hex` ``） | **163**（うち同一行にpathが無い継続行あり） | 同一行にbacktick付きpathがある場合のみ**可**。無い場合は**採点不能**（unpaired計上） |
| C：表cell（`| \`hex\` |`） | **1,048** | **不可**（表ごとにpath列の位置が違う。v3の論点） |

現行成果物のdigest：

```text
ff5b26e3ab3c6fa7ead6214d302b7cd500e7bfbd2a456c0c0bcc45897c38511c  tools/evaluation/operational_metrics.py
1efd0c8f09df8e18d77dcb69c48ce85e97324e6846c84df109334968f8e29c0e  tests/test_operational_metrics.py
```

## 2. 手順4：接続点と設計

- **既存装置の拡張**（新設せず`operational_metrics.py`へ集計3を追加。schema_version 2）。
- H5照合の分類：`resolved_match`（fileが在りdigest一致）／`digest_differs`（fileは在るが不一致。
  版の前進でも起きるため「破損」とは断定しない定義を dataset に明記）／`file_missing`。
  path解決は相対＝repo root基準（`roots.repo_root()`）・絶対＝そのまま（私有領域対応）。
- 承認点定義の精緻化（Evidence v1 §4-2の論点）：v1の「文字列を含むrecord数」に加え、
  行頭欄形式（`承認文言`で始まる行を持つrecord数）を`field_count`として併記。v1定義は不変。
- fail-closed：書式C・組の閉じないBは採点せず件数のみ報告（`unpaired_count`・`total_hex_count`）。

## 3. 手順5：正式再利用検索

作業別計画の先行commit後に実行し、証明書を
`records/development/2026-08-18-operational-metrics-v2-reuse-search-attestation-v1.json`へ固定する。

## 4. 範囲の判断（作業票へ渡す論点）

v2＝**H5（書式A・Bの照合）＋承認点field_count**。繰り越し（v3）＝書式Cの表schema対応・
H4手動記入（母集団特定が先）・コストと assemble/check 近似（セッションログ時系列parser）。

## 5. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、dataset v2固定、Evidence、TODO反映。
