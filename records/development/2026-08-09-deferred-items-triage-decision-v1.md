# Deferred項目の仕分け裁定 v1

- 裁定日：2026-08-09
- 裁定者：Human
- 裁定文言（chatより転記）：「1，5，6，7を実施」
- 番号の対応：`TODO_NEXT_SESSION.md`のdeferred 7項目に対するClaude提示の一覧番号

## 裁定内容

| # | 項目 | 裁定 |
| --- | --- | --- |
| 1 | IC-V4 resolve tool不足（Issue正式解決の永続化） | **着手** |
| 2 | C／Dの扱い（内部未公開情報／混入外部データの方針） | 保留継続 |
| 3 | 既存保全データへの遡及適用 | 保留継続 |
| 4 | 原子的filesystem競合防止 | 保留継続 |
| 5 | 参照Digest恒久検査器 | **着手** |
| 6 | 守り役後追いレビュー | **着手** |
| 7 | テストfixture重複の共通化 | **着手** |

## 実施順（Pilot提案。Humanの変更指示があれば従う）

`#7`（最軽量。役割中立方式の`low`計測を兼ねる）→`#5`→`#1`→`#6`。
各項目は独立の作業単位とし、`single_active_leaf`（同時に1作業）で進める。
役割は現行のまま：pilot=claude、reviewer=codex、closer=codex。riskは項目ごとに
Pilotが提案しHumanが確定する。

## 保留継続分の扱い

`#2`・`#3`・`#4`はTODOのdeferred欄に残し、本裁定recordを参照点とする。
