# 運用集計v3（書式C＝表cell束縛の照合）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「候補1」（＝運用集計v3。2026-08-18 chat）
- 記録者：Claude
- 上位：運用集計v2 Evidence §6の繰り越し
- 基準commit：`0dc25e1`（作業tree clean）
- 実測：測定ブロック
  `records/development/2026-08-18-operational-metrics-v3-prescan-measurements-v1.md`
  （guard付き・全entry二重実行一致）

## 1. 実測から確定した事実

1. 書式C（表cell）の実形は主に2種——`| 見出し | `path` | `hex` |`（3列）と
   `| `path` | `hex` |`（2列）。
2. **採点してはならない偽装が実在**する——(a) hexがfile名の一部（`work4a/observations/<hex>.json`）、
   (b) pathの無いhex行（`| 修正実装 | `hex` |`）。行単位のfail-closed組定義が必須。

## 2. 設計（作業票へ渡す論点）

1. `collect_binding_metrics`へ**書式C**を追加：行を`|`でcell分割し、「backtick付きの**裸hexだけ**の
   cellがちょうど1つ」かつ「path様token（`/`か`.`を含み純hexでない）を含むcellがちょうど1つ」の
   行だけを組として採点。それ以外（0個・複数・hexがtoken内）は`unpaired_count`へ（fail-closed）。
   書式Bが同一行で一致した場合はCを適用しない（二重計上防止）。
2. dataset出力は`schema_version` 3・`…-dataset-v3.json`として新版固定（v1・v2不変）。
3. **v4へ明示繰り越し**：H4手動記入率・コスト（セッションログ時系列）・`digest_differs`の
   git履歴照合。見取り図は引き続き一部完了。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみで実行。証明書は
`records/development/2026-08-18-operational-metrics-v3-attestation-v1.json`。

## 4. 未実施

- 手順5、作業票の適用、RED、GREEN、dataset v3固定、Evidence、TODO・見取り図反映。
