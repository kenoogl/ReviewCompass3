# 運用集計v6（時系列復元・欠落由来）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「運用集計v6（時系列復元）へ」（2026-08-18 chat）
- 記録者：Claude
- 上位：v5 Evidence §4の繰り越し
- 基準commit：`dfa373a`（作業tree clean）
- 実測：測定ブロック
  `records/development/2026-08-18-operational-metrics-v6-prescan-measurements-v1.md`
  （guard付き・全entry二重実行一致。**内容は読まず件数のみ**の探針で行形を調査）

## 1. 実測から確定した事実

1. raw区画は**3系統dir**（hash名）：1,152 file／19 file／560 file。
2. 行形は系統ごとに異なる——`"type":"tool_use"`の厳密一致が数えられるのは1系統のみ
   （見本fileで73件）。他系統は`"timestamp"`主体で道具呼び出しの表現が別形。
3. よって**単一の解釈を全系統へ当てない**：厳密一致計数（保守値）と緩い部分一致計数（上限値）を
   **別掲**し、時刻を解釈できないfileは`duration_unrecognized`へ明示計上する（fail-closed）。

## 2. 設計（作業票へ渡す論点）

1. **コスト時系列（第一次）**`collect_cost_metrics(raw_root)`：系統dir別に
   file数・行数・`"type":"tool_use"`厳密数・`tool_use`部分一致数・先頭行と末尾行のtimestamp差の
   合計（解釈可能fileのみ。不能は件数計上）。出力は系統dir名（hash）のみ・絶対path出力なし・
   **内容の転記なし（数と時刻だけ）**。
2. **欠落34の由来分類**`collect_missing_origin(...)`：束縛照合のfile_missingを
   `missing_deleted`（git履歴に存在＝削除・改名）／`missing_never`（履歴に無い）／
   `missing_absolute`（絶対path束縛）へ分類（counts のみ・path一覧は出力しない）。
3. dataset v6（schema_version 6）。v1〜v5不変。`--raw-root`任意引数（既定＝保全先raw）。
4. v7へ繰り越し得るもの：系統別の意味づけ（どのhashがどの系統か＝保全設定との突き合わせ）・
   道具呼び出しの系統横断正規化。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-18-operational-metrics-v6-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、dataset v6固定、Evidence、TODO・見取り図反映。
