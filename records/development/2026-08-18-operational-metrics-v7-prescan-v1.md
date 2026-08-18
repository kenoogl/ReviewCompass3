# 運用集計v7（系統意味づけ・道具正規化・活動時間）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v7に着手してください。作業票と事前走査から入ってください」（2026-08-18 chat）
- 記録者：Claude
- 上位：v6 Evidence §4の候補（`records/development/2026-08-18-operational-metrics-v6-evidence-v1.md`）
- 基準commit：`c0d2582`（作業treeは本走査の生成物2件を除きclean）
- 実測：測定ブロック
  `records/development/2026-08-18-operational-metrics-v7-prescan-measurements-v1.md`
  （guard付き・全5entry二重実行一致。**内容は読まず、正準位置のtype語彙と件数のみ**の探針）

## 1. 実測から確定した事実

1. **系統dirは保全設定から機械同定できる**：raw配下のdir名は取得元rootの`_namespace`
   （絶対path文字列のSHA-256先頭16桁。`tools/session_logs/eventual_preservation.py`）であり、
   `record_run.DEFAULT_SYSTEMS`の3系統がdir 3つと過不足なく一致——claude=`d48f07ecdd30cb6f`・
   codex現行=`b12edc2408fa1263`・codex保管=`c5ae2c27e5f07634`。未対応dir 0。
2. **道具呼び出しの正準位置**：Codex 2系統はtop-level `type`が7語彙（`event_msg`・`response_item`等）で、
   道具呼び出しは`payload.type`の`function_call`（57,846／90）と`custom_tool_call`（45,841／653）。
   対応する`*_output`が同数で並ぶ（呼び出しと結果の対）。Claude系統は`message.content[].type`の
   `tool_use`＝28,760で、byte一致計数（`"type":"tool_use"`）28,760と全件一致（現corpusでは本文偽装の
   混入0の傍証。ただし正とするのは構造計数のみ）。
3. **時刻**：3系統とも、JSON解釈できた行のtimestampは全件ISO・時刻帯つき（naive 0）。Claude系統は
   timestampを持つ行が111,154／130,943行で、**逆行する隣接対3,567**がある（並びが時刻順でない）。
   負間隔は数えて除外するfail-closed処理が要る。Codex系統は全行にtimestampがあり逆行0。
4. **間隔分布が機械算出できる**：隣接timestamp対の間隔bucket（≤60／≤600／≤3600／>3600秒）の
   件数と秒和が3系統とも取得済み（測定ブロック参照）。600秒は保全の活動窓
   （`RECENT_ACTIVITY_WINDOW_SECONDS`）と同値の既定候補。
5. **変更面は装置と試験に閉じる**：`operational_metrics`の参照元（Python）は
   `tests/test_operational_metrics.py`の1件のみ。既存試験はキー単位の検証（追加キーで壊れない）。
   schema固定試験のみ意図保存の更新対象。
6. **自己言及の明記**：corpusは本日実行のセッションログ記録（record-run）時点までを含み、
   本セッション自身の保全prefixも母集団に入る。v6 dataset固定時点からfile・行が増えている
   （例：claude系統560→562 file）。v7は新snapshotであり、v1〜v6は不変のまま。

## 2. 設計（作業票へ渡す論点）

1. **系統意味づけ**`collect_system_identity(raw_root, systems=保全設定既定)`：namespace導出で
   dir↔labelを照合し、label・hash・dir有無・未対応dir数だけを出力（絶対path・内容なし）。
   導出は`_namespace`の再利用（式の複製をしない）。
2. **道具呼び出しの正規化**：系統labelごとの正準規則で構造計数——Claude＝`message.content[].type
   == "tool_use"`、Codex＝top-level `response_item`かつ`payload.type ∈ {function_call,
   custom_tool_call}`（呼び出しのみ。`*_output`・event系は数えず二重計上を避ける）。labelを
   同定できないdirへは規則を当てず`null`（fail-closed）。既存の`tool_use_typed`／`tool_use_loose`
   欄は不変のまま併載。
3. **活動時間の精緻化**：file内の隣接する解釈可能timestamp対の間隔を、固定bucket（≤60／≤600／
   ≤3600／>3600秒）の件数・秒和で出力し、窓（既定600秒）以下の和を`activity_seconds`とする。
   負間隔・時刻なし行は明示計上。経過幅`duration_seconds`（v6定義）は不変のまま併載。
4. schema_version 7（追加のみ）。dataset v7固定。`--activity-window-seconds`任意引数（既定600）。
5. v8候補：日別の時系列展開・複数会話の重複窓統合・rawの意味解析。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-18-operational-metrics-v7-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、dataset v7固定、Evidence、TODO・見取り図反映。
