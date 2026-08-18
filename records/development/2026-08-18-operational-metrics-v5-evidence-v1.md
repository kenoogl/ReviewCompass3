# 運用集計v5（H4手動記入・コスト第一段）実行Evidence v1

- 記録日：2026-08-18。指示者：利用者（Human）「運用集計v5（H4手動記入・コスト）へ」→
  「v5の実装を続行してください（REDから）」（chat）
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v5-work-ticket-v1.md`／
  事前走査同prescan v1。基準`9bdbc0f`→事前走査`a71cf0b`→文書・計画（writer）`52af362`→
  証明書`2ced695`→実装は本record同一commit

## 1. 成果物

装置へ2集計を追加——H4自動導出率（builder雛形`_render`（純関数）を類型別にin-memory生成し
`<<記入:`欄数÷非空行数から機械算出。手数えゼロ）・コスト第一段（保全先の区画別file数・byte・
日付範囲。内容不読・区画名のみ出力）。`--preservation-root`任意引数（既定＝正準path）。
schema 5。試験18本（追加3・schema固定は意図保存で5へ）。dataset v5を機械固定（v1〜v4不変）。

## 2. RED→GREEN（正直な記載）

RED＝追加3本のみ失敗（terminal転記）。実装初回に`datetime`のimport漏れで5本失敗させ、
即修正した（過程の記録）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-18-operational-metrics-v5-evidence-measurements-v1.md`参照**
（18本exit 0・dataset v1〜v4の既知digest一致・v5に絶対path無し＝grep該当なし・全entry二重実行
一致）。`git diff --check`合格。

## 3. dataset v5の要旨

- **H4自動導出率＝93.9%**（3類型とも記入欄2・非空行33。雛形構造が共通のため同値——依頼record
  の33行中、LLMが書くのは2欄だけで残りは機械欄）。
- **コスト第一段**：raw 1,731 file・約2.94GB（2026-08-10〜08-18）・verbatim 1,724 file・
  約614MB・cursors／provenance各1,724 file・state 3 file。**8日間で約3.5GBの全量保全**が
  機械集計で固定された。

## 4. v6へ繰り越し

道具呼び出し数・時間の時系列復元（rawの全文解析・別設計）・欠落34の由来特定。

## 5. 未実施

TODO・見取り図反映とcommit。push（利用者の運用に従う）。
