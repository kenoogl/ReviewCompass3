# Work 4B本体 設計束 承認Decision v1

- decision ID：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「承認」（2026-08-07。平易説明の提示後）

## 1. Humanの決定

Work 4B本体 設計束提案v1（`docs/design/2026-08-07-work-4b-main-design-bundle-proposal.md`、
SHA-256 `14c629d2f45a1dd36cbb3ed60b311ead2898c1e07fe71ffc8e5d2c6365234b5b`）を承認した。
承認は4構成すべてと、推奨実装順（A-1除外宣言→B再観測→A-2順位表→D台帳→C外部化）、
初版の閾値（Bの鮮度判定「対象範囲に観測後の変更1件で停止」、Cのbyte一致移行・旧位置保持）に及ぶ。

## 2. 承認により許可されること

- A-1：統合除外宣言の初版entry候補一覧の作成とHuman裁定の要求
- 各構成の実装単位ごとの、規範宣言の展開、宣言→RED対応表（照合は恒久検査器）、
  再利用検索gate、RED固定、実装
- D完了後のWork 5B defer項目の完了戻し（`DEC-WORK5B-LEDGER-ITEM-DEFER-001`の再開条件）

## 3. この決定が承認していないこと

- 除外宣言の初版entryの内容（候補一覧の提示後に別途Human裁定）
- LLM意味判断の実行、レビューbacklog着手、RC2取り込み、外部APIレビュー（合意順序③④のまま）
- 全routineの一括分類・一括台帳化
- 順位重みの変更（初版は固定の辞書式順）
