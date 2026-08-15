# 一件レビュー 境界2 RED証拠 v1

- Evidence ID：`EVD-ONE-ITEM-REVIEW-BOUNDARY2-RED-2026-08-15-V1`
- 実施日：2026-08-15
- 基準commit：`03a3808`
- 対象：`tests/test_one_item_review.py`
- 状態：`red_confirmed`

## 結果

【実測】`.venv/bin/python3 -m pytest --collect-only -q tests/test_one_item_review.py`は85件収集、終了コード0である。

【実測】`.venv/bin/python3 -m pytest -q --tb=no tests/test_one_item_review.py`は、境界1の29件が成功し、
境界2の56件だけが失敗、終了コード1である。

【実測】正常材料一件の単独実行は1 failed、終了コード1、主要理由は
`AttributeError: module 'tools.reviews.one_item_review' has no attribute 'prepare_material'`である。

【判断】製品関数不在という期待した一理由によるREDである。正常schemaとSHA、決定性、schema不正14種、
既定5秘密patternと高乱雑性、絶対path停止6例・非停止3例、環境値非解決を固定し、結果集合・整理・CLIは含めない。

【未実施】製品核、入口、`pyproject.toml`は変更していない。材料作成、安全停止、関連・全試験は未実施である。
