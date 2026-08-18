# 運用集計v5（H4手動記入・コスト）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v5（H4手動記入・コスト）へ」（2026-08-18 chat）
- 記録者：Claude
- 上位：v4 Evidence §4の繰り越し
- 基準commit：`9bdbc0f`（作業tree clean）
- 実測：測定ブロック
  `records/development/2026-08-18-operational-metrics-v5-prescan-measurements-v1.md`
  （guard付き・全entry二重実行一致）＋規模の追加実測（du：raw 2.7GB・verbatim 589MB。
  規律2の例外＝コマンド併記の転記）

## 1. 実測から確定した事実（設計を変える2点）

1. **commit済み依頼recordに`<<記入:`残存は0件**（grep全件0）。記入済みでcommitされる運用のため、
   H4手動記入率は「commit後recordの計数」では測れない。**雛形生成時の機械欄／LLM記入欄の比率を
   builder自身（`tools/request_builder/`の雛形定義）から機械算出**する設計に変える。
2. セッションログ保全先は5区画（cursors／provenance／raw／state／verbatim）で、
   **raw 2.7GB・verbatim 589MB**。コストの第一段は「file数・byte・期間の規模集計」に絞り、
   道具呼び出し数の時系列parserは**v6へ繰り越す**（全文解析は規模的に別設計が要る）。

## 2. 設計（作業票へ渡す論点）

1. H4：`request_builder`の3類型それぞれについて、雛形をin-memory生成して`<<記入:`欄数と
   機械欄数を数え、**自動導出率＝機械欄÷全欄**を機械算出する集計を装置へ追加。
2. コスト第一段：保全先の区画別file数・総byte・最古/最新の日付範囲を流し読みで集計
   （内容は読まない・読み取り専用・私有pathを出力に含めない既存規律を踏襲）。
3. dataset v5（schema_version 5）として新版固定。v1〜v4不変。
4. v6へ明示繰り越し：道具呼び出し数・時間の時系列復元・欠落34の由来特定。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-18-operational-metrics-v5-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、dataset v5固定、Evidence、TODO・見取り図反映。
