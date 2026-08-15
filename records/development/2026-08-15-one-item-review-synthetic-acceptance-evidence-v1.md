# 一件レビュー処理・合成受入例 Evidence v1

- 実施日：2026-08-15
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003`
- 対象commit：`741424b`（独立完了レビュー固定後）
- 実行環境：`.venv/bin/python3`
- 外部送信・外部処理・保存：なし

## 目的

実利用者資料を使わず、合成した一件を正式な核処理へ通し、利用者が資料本文を読まずに
件数、分類、人へ残る判断、安全表示を確認できることを実測する。

## 入力

- 資料識別子：`SYNTHETIC-ACCEPTANCE`
- 合成資料：2行（本文は証跡へ転記しない）
- レビュー：3件
  - 2件は同一論点を独立に報告
  - 1件は証拠不足
- 外部送信許可：与えない

## 実施

`tools.reviews.one_item_review`の`prepare_material`、`validate_results`、
`organize_results`を`.venv/bin/python3 -c`から順に呼び出し、利用者向け要約だけを標準出力した。

- 終了コード：0
- 資料内容識別値：`6bc225c3142cca76f9a2d23d7208a8423d8fc928d11ce4eb5892ab3369a91a2a`
- 材料一式識別値：`1efb5d9999399c723884f1da843f4d55296be80b9e3cf9ebe3b2b1e6cc2859e5`
- 結果集合識別値：`1f82aea53ffc004efe3d65a2252dc008cd84d96870433fdda8f84690c052ef87`

## 結果

| 項目 | 実測値 |
|---|---:|
| レビュー数 | 3 |
| 指摘数 | 2 |
| 論点数 | 1 |
| 一致した論点 | `ISSUE-1`（担当`R-A`、`R-B`） |
| 証拠不足 | 担当`R-C` |
| 人の判断一覧 | `insufficient_evidence: R-C`、`matching_reports: ISSUE-1` |
| 資料本文の出力 | false |
| 絶対pathの出力 | false |
| 外部送信許可 | false |
| 判断状態 | `pending_human_decision` |

## 判断

【実測】一致した報告も自動承認されず、証拠不足とともに人の判断一覧へ残った。
資料本文と絶対pathは要約へ出ず、外部送信も許可されなかった。

【未実施】製品処理としての受入はHuman承認境界であり、本証跡では代行しない。
