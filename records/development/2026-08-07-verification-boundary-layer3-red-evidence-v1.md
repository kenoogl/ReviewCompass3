# 層3（機械は保証しない）RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層3）、`DEC-RED-VERIFICATION-ADOPTION-001`（手順）
- 実装前検索：`records/development/2026-08-07-layer3-reuse-search-attestation-v1.json`
  （gate `assessed_fresh`、該当33 routine）

## 1. 対象

検証していない箇所を機械可読な宣言として固定し、宣言と実装の対応が崩れたら検出できるように
する。対象7項目：O-2・O-3（host権限の自己申告）、O-4（実行結果の説明文）、I-1（Human裁定文）、
I-2-text（決定時刻の文面。単調性は層1で機械化済み）、P-1（候補の提案文）、
C-2-meaning（説明の意味的妥当性。空文字拒否は層1で機械化済み）。

## 2. 実行照合中に判明した手順の不具合と補修（記録）

RED固定前の実行照合が、**6件すべて`unknown`**を返して手順が停止した。原因は、対象moduleが
未実装のとき`ImportError`で収集エラーになり、pytestがtest単位の結果行を出さないことだった。
**実装未着手という正常なREDの状態が、`unknown`と取り違えられていた。**

`DEC-RED-VERIFICATION-ADOPTION-001` §2-4（`unknown`が残る場合はcommitせず原因を解消する）に
従い、検査器を補修した：収集エラー行（`ERROR <file>`）を読み、そのfileに属するnode idを
すべて`error`として扱う。無関係なfileには波及しない。補修は
`tests/test_red_verification_collection_error.py` 3 testでtest-firstに固定した（RED 3→GREEN 3）。

補修後の照合：`checked=6 verified=6 mismatched=0 unknown=0` → `passed`。

**採用した手順が、その手順自身の不具合を2日目に露呈させた形**であり、記録に残す。

## 3. 宣言→RED対応表

`records/development/2026-08-07-verification-boundary-layer3-declaration-red-map-v1.json`
（`scope: complete`）。静的検査`passed`、宣言6件（Z1〜Z6）、実行照合`passed`。

## 4. 状態と次

本RED作業単位のcommit後、固定testを変更せずGREEN実装（宣言moduleの新設と手順書からの導線）へ
進む。
