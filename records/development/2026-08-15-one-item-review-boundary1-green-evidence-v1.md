# 一件レビュー 境界1 GREEN証拠 v1

- Evidence ID：`EVD-ONE-ITEM-REVIEW-BOUNDARY1-GREEN-2026-08-15-V1`
- 実施日：2026-08-15
- RED commit：`1594356`
- 作業票：`docs/development/2026-08-15-one-item-review-implementation-work-ticket-v2.md`
- 製品核：`tools/reviews/one_item_review.py`
- 製品核SHA-256：`39e8fd3cf8f9563caacaea52ee9b7171d09c8390439da68d51e405fa1978d182`
- 対象試験SHA-256：`a2acca491a23826482beca1b566ecf3a4740872ebe95e07387f495f63ce4bab0`
- 状態：`boundary_1_green`

## 1. 実施

【実測】RED試験を変更せず、製品核へ次だけを実装した。

- 明示された絶対root内の資料、条件、任意の結果fileだけを読む。
- rootからfileまでfile descriptorで辿り、各構成要素をsymlink非追跡で開く。
- 通常file、読取り前後のsize、同一inode、UTF-8、空、NULを検査する。
- 資料262,144 bytes、条件65,536 bytes、結果1,048,576 bytesを上限とする。
- 停止は契約の固定理由を持つ`ReviewStop`として返す。

【実測】`git diff --quiet HEAD -- tests/test_one_item_review.py`は終了コード0で、RED commit後に試験変更はない。

## 2. GREEN command

```text
.venv/bin/python3 -m pytest -q tests/test_one_item_review.py
```

【実測】29 passed、失敗・error・skip 0、終了コード0である。

## 3. 禁止した先取り

【実測】製品核にJSON解析、schema検査、機微情報・高乱雑性検査、正準JSON、CLI引数処理、network、外部process、
環境値解決、file書込み、directory作成、削除はない。静的検索は該当0件、終了コード1である。

【判断】境界1の利用者意味と拒否境界だけがGREENになった。境界2以降の合格を主張しない。

## 4. 次と未実施

【提案】境界1を意味単位commitへ固定後、境界2の固定材料作成、条件schema、機微情報・絶対path安全停止について、
失敗試験を先に追加する。

【未実施】製品入口、`pyproject.toml`、材料作成、結果集合検査、整理、CLI、関連・全試験、独立完了レビューは未実施である。
