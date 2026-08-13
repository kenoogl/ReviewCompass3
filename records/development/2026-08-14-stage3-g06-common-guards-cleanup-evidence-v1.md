# 第3段 G06共通処理試験整理 Evidence v1

- 記録日：2026-08-14
- 状態：`implemented_pending_independent_review`
- 作業票：`docs/development/2026-08-14-stage3-g06-common-guards-cleanup-bootstrap-work-ticket-v1.md`
- 作業票commit：`f9073e5`
- 基準commit：`f879af5`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- Human承認：G06案Bを承認済み

## 1. 実施

【実測】`tests/test_common_digests.py`一件だけで次を実施した。

- 入れ子tuple入力をlist内tuple入力`{"items": [(1, 2)]}`へ置換した。
- 通常経路では比較へ到達しない衝突確認の引数別二件を削除した。
- 名前順先頭200 fileだけを走査する実在記録試験一件を削除した。

変更後試験file SHA-256は`8a2c2cae53cf65bf8b18459785ed40d5de2087dafd7e6edec95dbce9fc07bf23`である。
製品コード、経路五件、非文字列key、tuple、非有限数、set、bytes、Task Contract三境界、正常文書三件は変更していない。

## 2. 関連試験と欠陥投入

【実測】G06対象は21件成功、終了コード0だった。関連四fileは84件成功、終了コード0だった。

【実測】今回の変更後試験fileは、先行再評価で作成したリポジトリ外の正常複製とlist再帰欠陥複製の双方にある
試験fileとSHA-256が一致した。正常複製ではG06 21件・関連84件が成功した。list要素の再帰検査だけを外した複製では、
置換したlist内tuple一件だけが失敗し、20件成功・1件失敗・終了コード1だった。

【判断】新しい試験数を増やさず、既知のlist再帰の見逃しを閉じた。削除した三件は固有保証を持たず、残した条件は
現在の共通内容識別値と経路境界を直接守る。

## 3. 正規全試験

【実測】正規入口を単独実行した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-g06-cleanup-full-receipt.json
```

- 結果：`passed`
- 終了コード：`0`
- 成功：`1,728`
- 失敗・エラー・除外：`0`
- Python：`3.13.14`
- pytest：`8.4.2`
- 代替実行：`false`
- 受領記録SHA-256：`b7014f402c7432c0d4ba7155d103ba98fdf72766f1299ee2fcfdd6b8379b001f`
- 状態識別値：`853918c2997843b6e4de8c407e03d87a1fe76cff9430076fad09ee6d5f46fa10`

【実測】Work 5B整理後の1,731件から三件減の1,728件で、作業票の期待と一致した。受領記録は本Evidence追加前の
試験整理状態に対応する。独立完了レビューは結果commit全体を再確認する。

## 4. 変更範囲と未実施

【実測】成果の変更範囲は`tests/test_common_digests.py`一件と本Evidence一件だけである。
`git diff --check`は指摘0件だった。

【未実施】製品コード、他試験、設定、正本、台帳、既存record、TODO、G06外の変更、新しい試験・検査器・台帳、
外部送信、履歴書換え、第3段完了判断は行っていない。
