# 運用集計v2（H5束縛表・承認点定義）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「運用集計v2（H5束縛表など）に進んでください」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。既存集計装置への読み取り専用の集計追加のみ（既存挙動・
  判定・安全境界の変更なし。出力schemaは`schema_version` 2へ更新）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-operational-metrics-v2-prescan-v1.md`

## 1. 目的

H5（digest束縛の追跡可能率）を機械集計へ加える。recordに書かれたpath＋SHA-256の組を実fileと
照合し、証拠へ機械でたどれる割合を出す。あわせて承認点の欄形式計数（`field_count`）を併記する。

## 2. 正本範囲（成果物）

1. **`tools/evaluation/operational_metrics.py`の拡張**：
   - 集計3（H5束縛照合）`collect_binding_metrics`：書式A（shasum行）と書式B（同一行に
     backtick付きpathを持つ`SHA-256 \`hex\``）から（path, digest）組を抽出し、
     `resolved_match`／`digest_differs`／`file_missing`へ分類。相対pathは`roots.repo_root()`
     基準、絶対pathはそのまま。組の閉じない出現は`unpaired_count`、全hex出現は
     `total_hex_count`として採点せず報告（fail-closed）。
   - 集計2の併記：行頭が`承認文言`で始まる行を持つrecord数を`field_count`へ追加
     （v1の`record_count`定義は不変）。
   - 出力`schema_version`を2へ。既存欄の意味は変えない。
2. **試験の追加（RED先行）**：`tests/test_operational_metrics.py`へ、(a) 書式A・Bの抽出と
   3分類、(b) unpaired・total_hexの計上、(c) `field_count`、(d) `schema_version` 2、の4本を
   追加（既存5本は変更しない）。
3. **dataset v2固定**：実データ実行出力を
   `records/development/2026-08-18-operational-metrics-dataset-v2.json`へ固定（v1は不変）。
   `digest_differs`は「版の前進でも起きるため破損と断定しない」定義を実行Evidenceに明記。

## 3. 範囲外（v3へ明示繰り越し）

- 書式C（表cell）の照合（表ごとのpath列schema対応が先）。
- H4手動記入（母集団＝request-builder資材の特定が先）。
- コスト・H4 assemble/check近似（セッションログ時系列parserの新設が先）。
- git履歴を遡るdigest照合（`digest_differs`の来歴判定）。既存recordの改変。

## 4. 受入条件

1. RED：追加試験が実装前に失敗（単独終了コード非0）・既存5本は緑のまま。
2. GREEN：新旧9本＋`tests/test_common_roots.py`＋`tests/test_rq2_paired_trial.py`が
   各単独終了コード0。
3. 実データ実行：終了コード0。書式A・Bの採点対象組数と`total_hex_count`（事前走査実測2,386）
   の整合が出力から機械確認できる。
4. dataset v2固定・digest機械転記。v1不変（digest再計算一致）。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. `digest_differs`の扱い（v2は分類報告のみ。「破損」判定や履歴照合はv3判断）。
2. 書式Cの1,048件を照合対象に含める時機（v3）。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査と同一commit。
2. 正式再利用検索→証明書commit。
3. RED→GREEN→実データ実行→dataset v2・Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
