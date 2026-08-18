# 運用集計v7（系統意味づけ・道具正規化・活動時間）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v7に着手してください。作業票と事前走査から入ってください」（2026-08-18 chat）
- 種別：範囲固定文書（軽量作業票）。読み取り専用の集計拡張のみ。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-18-operational-metrics-v7-prescan-v1.md`

## 1. 正本範囲

1. `tools/evaluation/operational_metrics.py`：事前走査§2の3追加——
   (a) 系統意味づけ`collect_system_identity`＝保全設定のnamespace導出でdir↔labelを機械照合
   （label・hash・dir有無・未対応dir数のみ出力）、(b) `collect_cost_metrics`の追加欄＝正規化
   道具計数（Claude＝`message.content[].type == "tool_use"`の構造計数／Codex＝`response_item`×
   `payload.type ∈ {function_call, custom_tool_call}`。未同定dirはnull）と活動時間（隣接
   timestamp間隔の固定bucket件数・秒和＋窓600秒既定の`activity_seconds`。負間隔・時刻なし行は
   明示計上）、(c) schema 7。既存欄の意味とdataset v1〜v6を変えない。
2. 試験の追加（RED先行）4本：(a) 系統照合（未対応dir含む）、(b) Codex正規化（`*_output`・
   event系を数えない）、(c) Claude正規化の敵対fixture（本文中の偽`"type":"tool_use"`文字列を
   構造計数が数えない＝byte計数との差を固定）、(d) 活動時間（窓内和・bucket・負間隔・時刻なし行）。
   既存21本無変更（schema固定は意図保存で7へ）。
3. dataset v7の実データ固定＋Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外（v8候補）

日別の時系列展開・複数会話の重複窓統合・rawの意味解析・会話単位の系列出力。

## 3. 受入条件

1 RED：追加4本のみ失敗／2 GREEN：25本単独0／3 実データ0・dataset v7固定・v1〜v6不変・
絶対path出力なし（grep該当なし）／4 計画writer仕上げ・証明書start_allowed: true／
5 diff・意味単位commit・transition合格。

## 4. Humanの確認が要る点（覆せる形）

1. 活動時間の窓＝600秒既定（保全の活動窓`RECENT_ACTIVITY_WINDOW_SECONDS`と同値）。固定bucketを
   併載するため、窓の再選択は再集計だけで可能。
2. namespace導出の再利用方法＝`_namespace`の直接import（案A採用）。代替：式の複製（案B。将来の
   乖離risk）／保全moduleへ公開wrapper追加（案C。正規moduleの変更が必要で変更範囲が大きい）。
   単純さ・正本一元・変更範囲の小ささで案A。
3. Codex規則集合＝呼び出し2種のみ（`mcp_tool_call_end`等のevent系は数えない＝二重計上回避）。
