# 一件レビュー作業契約候補v3 変更点確認

- 記録ID：`REV-TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003-CORRECTION-2026-08-15-V2`
- 実施日：2026-08-15
- 対象commit：`6535dcd6c044626422b784a3fb55237fc161027c`
- 対象契約：`records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v3.md`
- 対象SHA-256：`a52cd717f6709c5ca01a1e339385272abfe976a0b9ce176e857b427778cf07d6`
- 先行確認：`records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v1.md`
- 先行確認SHA-256：`8544484e25c7af07743002793c63a591aa3ad63c2dd09ce74f512fead4899a1f`
- 担当：先行レビューと同じ独立実行単位
- 判定：`ready_for_human_contract_and_implementation_decision`

## 1. 判定

【判断】**開始可**である。候補v2に残った2原因は候補v3で解消した。止める指摘は0件である。
ここでの開始可は、利用者の契約採用と案Cの実装開始判断へ渡せる意味であり、自動承認ではない。

## 2. 位置指定引数と内容検査

【実測】位置指定の絶対path引数はroot内束縛と安全な読取りだけに使い、内容検査、内容識別値、成功・停止出力から
除外された。内容検査は資料本文と、復号済みの条件JSON・結果集合JSONにある全ての文字列key・値へ固定された。

【実測】契約に固定した4 patternを`.venv/bin/python3`で実行し、終了コード0で次を確認した。

| 入力例 | 結果 |
| --- | --- |
| `work=/Users/example/project` | 検出 |
| `path:/Users/example/project` | 検出 |
| `path=C:\Users\example` | 検出 |
| `\\server\share\item` | 検出 |
| `//server/share/item` | 検出 |
| `file:///tmp/item` | 検出 |
| `https://example.test/item` | 非検出 |
| `relative/path` | 非検出 |
| `/` | 非検出 |

【判断】正常な位置指定引数を拒否せず、内容中の4形式を停止する規則は一意になった。

## 3. 配列順、内容識別値、指摘署名

【実測】基準ID、報告者、群内指摘、複製review候補、重複key候補、証拠不足一覧、未解決一覧、
人の判断一覧とその識別子に順序規則が追加された。

【実測】指摘署名はseverity、title、description、ID順の基準ID、開始行、終了行だけを持つ正準JSONへ固定された。
reviewの二つのSHA-256を計算する前にも、指摘と基準IDを同じ順へ正規化する。

【判断】基準IDの順だけを変えて複製review検出を逃れる反例は閉じた。

## 4. 退行確認

【実測】v2、v3、先行確認のSHA-256は一致した。固定参照9文書と機微情報検査codeも全件一致した。
G02既存14 fileは基準commitから差分0だった。複製review検出、全群を残す人の判断一覧、案Cの変更上限は維持された。

【実測】対象commitの変更は候補v3、v2確認記録、TODOだけである。レビュー終了時の`git status --short`は出力なしだった。
レビュー担当は成果を変更していない。

## 5. 利用者へ残す判断

1. 候補v3を作業契約として採用するか。
2. 一件、外部送信なし、書込みなし、共通問題keyによる結果整理という責務を採用するか。
3. 案Cの新しい製品核1、入口1、実行名1、対象試験1という上限で実装を開始するか。

## 6. 未実施

【未実施】契約採用、実装開始、製品code・試験・入口・実行名の変更、実利用者資料、外部送信、外部処理、保存、
正規全試験、push、tag、履歴書換えは行っていない。
