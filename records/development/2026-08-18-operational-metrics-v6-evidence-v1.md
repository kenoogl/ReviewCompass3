# 運用集計v6（時系列復元・欠落由来）実行Evidence v1

- 記録日：2026-08-18。指示者：利用者（Human）「運用集計v6（時系列復元）へ」（chat）
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v6-work-ticket-v1.md`／
  事前走査同prescan v1。基準`dfa373a`→文書・計画（writer）`7b879b1`→証明書`b559fc9`→
  実装は本record同一commit

## 1. 成果物

装置へ2集計を追加——コスト時系列第一次（系統dir別のfile数・行数・tool_use厳密／緩い計数・
先頭末尾timestamp差の合計。解釈不能は`duration_unrecognized`明示・内容不転記・絶対path非出力）と
欠落由来分類（`missing_deleted`／`missing_never`／`missing_absolute`・countsのみ）。
`--raw-root`任意引数（既定＝保全先raw）。schema 6。試験21本（追加3・schema固定は意図保存で6へ）。
dataset v6を機械固定（v1〜v5不変）。

## 2. RED→GREEN

RED＝追加3本のみ失敗（terminal転記）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-18-operational-metrics-v6-evidence-measurements-v1.md`参照**
（21本exit 0・v1〜v5既知digest一致・v6に絶対path無し＝grep該当なし・全entry二重実行一致）。
`git diff --check`合格。実データ実行は28.7秒（raw約2.9GBの流し読み）。

## 3. dataset v6の要旨（コスト時系列の初数字・欠落34の由来確定）

- **Claude形式系統（d48f07…）**：560会話file・128,150行・**厳密tool_use 28,210回**
  （緩い計数152,299＝上限値）・経過幅合計 約354,454秒・解釈不能78 file。
- 他2系統は行形が異なり厳密計数0（b12edc…＝1,152 file・970,980行・緩い7,207／c5ae2c…＝
  19 file・11,898行）。**系統hashの意味づけはv7論点**のまま（単一解釈を当てない設計どおり）。
- 定義の明示：`duration_seconds`は**先頭行と末尾行のtimestamp差の合計＝経過幅**であり活動時間
  ではない（fileが日をまたいで追記される系統では大きく出る）。
- **欠落34の由来が確定**：削除・改名（git履歴あり）8＋履歴なし（私有領域相対等）23＋
  絶対path束縛3＝**34（v4のfile_missingと完全整合）**。

## 4. v7候補

系統hashの意味づけ（保全設定との突き合わせ）・道具呼び出しの系統横断正規化・活動時間の定義精緻化。

## 5. 未実施

TODO・見取り図反映とcommit。push（利用者の運用に従う）。
