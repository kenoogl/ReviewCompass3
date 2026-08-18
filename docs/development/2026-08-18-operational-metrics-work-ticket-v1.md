# 運用集計コマンド（順序5）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「順序5（運用集計コマンド）に着手してください。まず範囲固定
  文書から」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。読み取り専用の集計装置の新設のみ（既存の挙動・判定・schema・
  安全境界の変更なし）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-operational-metrics-prescan-v1.md`

## 1. 目的

従軸（運用計測）の数値を、手集計せず装置で機械集計して新版recordに固定する（論文計画v2 §4）。
v1は今日の記録から形が一意に定まる2系統を確実に出す。

## 2. 正本範囲（成果物）

1. **`tools/evaluation/operational_metrics.py`の新設**：
   - 入力：`--launch-root`（launch計測メタの保存先）・`--records-root`（判断record群）。
   - 集計1（H4 launch実測）：各`<run>/launch.json`を読み、`elapsed_seconds`を持つ実行
     （instrumented）と持たない実行（legacy）を分計。instrumented の`elapsed_seconds`・
     `prompt_bytes`の件数・最小・中央値・平均・最大・合計。
   - 集計2（H7承認点）：`--records-root`直下の`*.md`のうち「承認文言」を含むfileを承認点として
     計数し、file名先頭の日付（YYYY-MM-DD）別分布を出す。
   - 出力：一行JSON（`schema_version`・両集計・入力母数・除外件数）。終了コード：0＝成功、
     2＝入力不備。未知形式のfileは数えず`skipped`へ計上（fail-closed）。
   - root解決は`tools/common/roots.py`を使い、遡りを複製しない。標準libraryのみ・2スペース。
2. **試験の新設（RED先行）**：`tests/test_operational_metrics.py`。一時fixtureで、(a) 分計と
   統計値、(b) 承認点の日付分布、(c) 一行JSONと終了コード0／2、(d) 未知形式のskip計上、
   (e) 実行入口（`-m`）の疎通、を固定する。
3. **dataset固定**：実データに対する実行出力を
   `records/development/2026-08-18-operational-metrics-dataset-v1.json`へ転記なしで固定し、
   実行Evidenceに実行コマンド・digest・件数を記録する。

## 3. 範囲外（v2へ明示繰り越し）

- **H4手動記入**（placeholder律）：母集団（request-builder資材）の特定が先。
- **H5**（digest束縛の追跡可能率）：束縛表の正準形の特定が先。
- **コスト・H4 assemble/check近似**：セッションログ時系列parserの新設が先（最重量）。
- 論文原稿への数値の取り込み（執筆スレッドの領分）。既存recordの改変・過去launchへのメタ遡及。

## 4. 受入条件

1. RED：新設試験が実装前に失敗（単独終了コード非0）。
2. GREEN：新設試験＋`tests/test_common_roots.py`＋evaluation系既存
   （`tests/test_rq2_paired_trial.py` 14件）が各単独終了コード0。
3. 実データ実行：終了コード0・launch母数49（31＋18）・承認点母数が§記録のgrep実測と一致。
4. dataset v1が固定され、出力JSONと `shasum` が Evidence に機械転記される。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. v1の2系統範囲の採否（残り3系統の繰り越し）。
2. 承認点の定義（「承認文言」欄を持つ判断record数）の採否——別定義（例：逐語欄のみ・chat行数）
   への変更はdataset v2で行う。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査と同一commit。
2. 正式再利用検索→証明書commit。
3. RED→GREEN→実データ実行→dataset・Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
