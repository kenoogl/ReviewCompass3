# 層2（機械が支援する）RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層2）、`DEC-RED-VERIFICATION-ADOPTION-001`（手順）
- 実装前検索：`records/development/2026-08-07-layer2-reuse-search-attestation-v1.json`
  （gate `assessed_fresh`、該当43 routine）

## 1. 対象と固定する拒否

| 反証 | 固定する内容 |
| --- | --- |
| O-1 | 既知の破壊的argv（`rm -rf`、`git push`など）を`read_only`と申告するinventoryを拒否する |
| A-1 | pathspec位置のoption形・絶対path・親escapeを拒否し、拒否時は何も実行しない |
| X-2 | 除外指定が落とす件数をentry別に報告する（拒否ではなく表示） |

**層2の要件**（安全保証ではなく誤記検出であること）を、Y4・Y11で**機械可読な宣言として固定**する。
規則の網羅は不可能であり、正常な操作を誤って止めないこと（Y3・Y8の境界例）も同時に固定する。

## 2. 宣言→RED対応表

`records/development/2026-08-07-verification-boundary-layer2-declaration-red-map-v1.json`
（`scope: complete`）。静的検査`passed`、宣言11件（Y1〜Y11）。

## 3. 実行照合（`DEC-RED-VERIFICATION-ADOPTION-001`）

RED固定commit前に照合した【実測】：

    checked=11  verified=11  mismatched=0  unknown=0  → passed

内訳はRED 9件（未実装により失敗）と境界例2件（Y3・Y8。正常な操作が通ることを実装前から確認）。

## 4. 状態と次

本RED作業単位のcommit後、固定testを変更せずGREEN実装へ進む。
