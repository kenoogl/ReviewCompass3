# 一件レビュー 境界1 RED証拠 v1

- Evidence ID：`EVD-ONE-ITEM-REVIEW-BOUNDARY1-RED-2026-08-15-V1`
- 実施日：2026-08-15
- 基準commit：`edf00bd5720fcfb73759dd852677aecca241e6a6`
- 作業票：`docs/development/2026-08-15-one-item-review-implementation-work-ticket-v2.md`
- 対象：`tests/test_one_item_review.py`
- 状態：`red_confirmed`

## 1. 目的

【判断】境界1の安全な一件読取りについて、製品実装が無ければ失敗し、後続のschema、機微情報、整理、CLIを
先取りしない試験境界を固定する。

## 2. 試験範囲

【実測】対象試験は29件で、次を固定した。

- `prepare`用2 fileと`organize`用3 fileの明示読取り
- directory探索禁止
- 相対path、root外、root・途中・file symlink、通常file以外
- 同一pathとhard linkによる同一file指定、欠落file
- 空、NUL、UTF-8不正
- 資料262,144 bytes、条件65,536 bytes、結果1,048,576 bytesの上限一致と上限+1

## 3. RED command

【実測】収集確認を単独実行した。

```text
.venv/bin/python3 -m pytest --collect-only -q tests/test_one_item_review.py
```

- 終了コード：0
- 収集：29件

【実測】正常読取り一件を単独実行した。

```text
.venv/bin/python3 -m pytest -q 'tests/test_one_item_review.py::test_reads_only_the_explicit_regular_input_files[False]'
```

- 終了コード：1
- 結果：1 failed
- 主要失敗理由：`ModuleNotFoundError: No module named 'tools.reviews'`

【判断】製品核不在という期待した一理由で失敗した。fixture、収集、import名の誤記、環境依存、後続境界の期待による失敗はない。

## 4. 次と未実施

【提案】対象試験を変更せず、`tools/reviews/one_item_review.py`へ境界1の安全読取りだけを最小実装し、29件をGREENにする。

【未実施】製品code、入口、`pyproject.toml`、schema検査、機微情報検査、材料作成、結果整理、CLI、関連・全試験は変更・実行していない。
