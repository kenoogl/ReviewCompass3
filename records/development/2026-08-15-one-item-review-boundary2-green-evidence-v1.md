# 一件レビュー 境界2 GREEN証拠 v1

- Evidence ID：`EVD-ONE-ITEM-REVIEW-BOUNDARY2-GREEN-2026-08-15-V1`
- 実施日：2026-08-15
- RED commit：`55eefd4`
- 製品核SHA-256：`9b9f8fede1ad2816680c9f12f69922284ec76575e543c2770d0bc1cac79677a2`
- 対象試験SHA-256：`d7f5a4c5e3f0e739281213df3056d2818e6840239dfb6cd3ac88e09e02ac75c7`
- 状態：`boundary_2_green`

## 実施と結果

【実測】RED試験を変更せず、条件JSONの完全一致schema、基準ID順正規化、条件・資料・材料のSHA-256、
契約§8.2の材料schema、G25の`default_pattern_rules`と`find_high_entropy`、契約固定4絶対path patternだけを実装した。

【実測】`git diff --quiet HEAD -- tests/test_one_item_review.py`は終了コード0で、RED commit後の試験変更はない。

【実測】`.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`は85 passed、失敗・error・skip 0、終了コード0である。

【判断】境界1の29件を維持し、境界2の56件をGREENにした。入力のkey順・基準順へ依存せず、秘密候補・高乱雑性・
絶対pathの停止例では検出値を`ReviewStop`へ含めない。環境依存規則を解決しない。

## 未実施

【未実施】結果集合schema、SHA欄の参照検査、結果集合の安全検査、整理、入口、`pyproject.toml`、関連・全試験、
独立完了レビューは未実施である。次は境界3のREDを先に固定する。
