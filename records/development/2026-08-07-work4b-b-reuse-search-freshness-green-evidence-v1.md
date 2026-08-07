# 構成B 再利用検索の鮮度判定 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001` §3
- RED Evidence：`records/development/2026-08-07-work4b-b-reuse-search-freshness-red-evidence-v1.md`

## 1. 実装

`tools/development/reuse_search_record.py`を変更した（本設計束で最初の既存module変更。変更前に
実装前検索gateを通過済み）。

- `search_existing_routines`へ`observation_document`・`project_root`を追加。観測を渡すと
  schema 2となり、観測recordの`files`欄（path＋SHA-256）と現状を突き合わせた`freshness`欄
  （変更・新規・欠落fileとstale判定）を機械計測して持つ。
- `gate_check`は、schema 2 recordに対して**gate時点で乖離を再計測**し、承認済み閾値
  （対象範囲の変更1件で停止）に従い`profile_stale`と対象file一覧を返す。
- schema 1の既存recordは版固定のまま検証・gate通過を維持し、gate結果に
  `freshness: not_assessed`を明示する（黙って素通りさせない）。

## 2. Test結果（機械実行、終了コード直接判定）

- targeted：freshness 4件＋既存R系8件 `12 passed`、exit `0`。固定testは変更していない。
- 公式全Test：`1075 passed`、exit `0`。
- 既存の実record 4件（schema 1）のgate通過を個別再確認した：全件`start_allowed: true`かつ
  `freshness: not_assessed`表示【実測】。

## 3. 残余と限界

- 観測を渡さない生成はschema 1のままであり、鮮度は計測されない。実運用の検索が観測を渡すことは
  運用規約であり、機械強制ではない（RED Evidence §3に記録した既知の緩さ。順位表（A-2）実装時に
  「順位表生成はschema 2 recordだけを入力にする」形で締める案を宣言に含める）。
- 鮮度の基準は観測recordの`files`欄の範囲に限る。範囲外の変更（例：test）は対象外。
- 本変更は守り役codeの変更であり、validator変更に相当する。旧合格のstale閉包について：
  schema 1 recordの合格は版固定の原則（統合除外宣言E2と同じ）により有効のまま維持し、
  stale化しない。正例・負例・境界例はF1〜F4とR1〜R7で再実行済み。
