# 一件レビュー作業契約候補v2 変更点確認

- 記録ID：`REV-TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003-CORRECTION-2026-08-15-V1`
- 実施日：2026-08-15
- 対象commit：`39bc84b778debd7e03002370e0c1981daa2a3833`
- 対象契約：`records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v2.md`
- 対象SHA-256：`60b8703e5a361eb7f509ecdb7532c1b928450bf55aea5c2eb9814020046d3e37`
- 先行レビュー：`records/development/2026-08-15-one-item-review-task-contract-definition-challenge-v1.md`
- 先行レビューSHA-256：`c1ec9fc3dc033c1dbf14c5201966497b1e2c8eae18cd38ededce5e8637ebd4b3`
- 担当：先行レビューと同じ独立実行単位
- 判定：`correction_required`

## 1. 判定

【判断】**修正要**であり、実装開始を止める。先行3原因のうち、複製reviewと人の判断一覧は解消した。
全入力文字列の安全検査と、出力・並び・内容識別値・絶対path規則は一部未解消である。

## 2. 解消した原因

【実測】`reviewer_id`だけを除く`review_content_sha256`が追加され、同じ内容は`possible_duplicate_reviews`へ入り、
独立した根拠として数えない。`matching_reports`は独立性も正しさも表さず、全ての群が人の判断一覧へ残る。

【判断】先行原因2は解消した。v3で再設計しない。

## 3. 残る原因1：検査対象と必須path引数が衝突する

【反証】v2は入力位置を絶対pathで指定させる一方、SHA-256欄以外の全利用者入力文字列に絶対pathがあれば停止する。
実行引数を除く記述がなく、正常な必須引数自身を拒否する。

【反証】`work=/Users/example/project`と`path:/Users/example/project`は、v2のPOSIX規則が直前文字に`=`と`:`を
含めないため検出を逃れる。Windows drive規則も開始位置境界がなく、`https://`中の`s:/`を誤検出する読み方と、
`path=C:\Users\...`を見逃す読み方の両方が成立する。

【提案】検査対象を、資料本文、条件JSON、結果集合JSONを復号した後の全ての文字列値とkeyに限定する。
位置指定引数はroot束縛だけに使い、内容検査・出力の対象外にする。停止例と非停止例を契約へ固定する。

## 4. 残る原因3：配列順と指摘署名が未固定

【実測】正常出力のkey集合、追加key禁止、UTF-8、key順、区切り、末尾LF、空の標準エラーは固定された。

【反証】`criterion_ids`、`reporters`、群内findings、重複候補と各ID、証拠不足一覧、未解決一覧、
人の判断一覧の同一区分内と`identifiers`の順が未固定である。基準IDの逆順だけで別の
`review_content_sha256`になり、複製検出を回避できる。

【反証】指摘署名SHA-256の正確な項目と入れ子構造も未固定である。

【提案】全配列の順をIDまたは内容識別値で固定し、指摘署名の正準JSON構造を列挙する。

## 5. 退行なし

【実測】対象commit、v1、v2、先行レビューのSHA-256は一致した。固定参照9文書と機微情報検査codeも一致した。
G02既存14 fileは基準commitから差分0で、案Cの変更上限は不変、製品codeと試験の変更は0だった。
レビュー終了時の`git status --short`は出力なしで、レビュー担当は成果を変更していない。

## 6. 次の処理

【提案】原因1と3の未解消部分だけを候補v3へ限定訂正し、変更点を一回確認する。開始可になるまで実装へ進まない。

## 7. 未実施

【未実施】契約採用、実装開始、製品code・試験・入口・実行名の変更、実利用者資料、外部送信、外部処理、保存、
正規全試験、push、tag、履歴書換えは行っていない。
