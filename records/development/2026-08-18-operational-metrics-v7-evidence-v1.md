# 運用集計v7（系統意味づけ・道具正規化・活動時間）実行Evidence v1

- 記録日：2026-08-18。指示者：利用者（Human）「運用集計v7に着手してください。作業票と事前走査から
  入ってください」（chat）
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v7-work-ticket-v1.md`／
  事前走査同prescan v1。基準`c0d2582`→文書・計画（writer）`76fa3c4`→証明書`c8d2c52`→
  実装は本record同一commit

## 1. 成果物

装置へ3追加——系統意味づけ`collect_system_identity`（保全設定のnamespace導出でdir↔labelを機械照合。
label・hash・dir有無・未対応dir数のみ出力）、道具呼び出しの正規化（Claude＝`message.content[].type`
／Codex＝`response_item`×`payload.type` {`function_call`, `custom_tool_call`} の構造計数。未同定dirは
null）、活動時間（隣接timestamp間隔の固定bucket＋窓600秒既定の`activity_seconds`。負間隔・時刻帯なし
は明示計上）。`--activity-window-seconds`任意引数。schema 7。試験25本（追加4・schema固定は意図保存で
7へ）。dataset v7を機械固定（v1〜v6不変）。

## 2. RED→GREEN

RED＝追加4本のみ失敗（`4 failed, 21 passed`・terminal転記）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-18-operational-metrics-v7-evidence-measurements-v1.md`参照**
（25本exit 0・v1〜v6のtracked差分なし・v7に絶対path無し＝grep該当なし・全entry二重実行一致）。
`git diff --check`合格。実データ実行は装置全体で約60秒（raw約2.9GBの全行JSON解釈を含む）。

### 2.1 敵対fixtureの前提訂正（テスト修正の理由記録）

RED時の敵対fixtureは「文字列本文中の偽`"type":"tool_use"`がbyte計数を騙す」前提だったが、GREEN
1回目の失敗（assert 1 == 2）で前提の誤りが実測された——正しいJSONの文字列値では引用符が`\"`へ
必ずエスケープされるため、**文字列本文はbyte計数を騙せない**。騙せるのは**非正準位置の入れ子
object**である。fixtureを「正準位置の実呼び出し＋非正準位置objectの偽装＋文字列偽装（自壊の実証）」
の3行構成へ訂正した。実corpusでbyte計数と構造計数が一致（§3）した理由もこのエスケープ機構で
説明できる。

## 3. dataset v7の要旨（3論点の初数字）

- **系統意味づけ**：3系統とも照合一致——`d48f07ecdd30cb6f`=claude・`b12edc2408fa1263`=codex現行・
  `c5ae2c27e5f07634`=codex保管。未対応dir 0（raw dir名＝取得元rootのSHA-256先頭16桁、の機械導出）。
- **正規化道具計数**（呼び出しのみ・構造計数）：codex現行 **103,687**（`function_call` 57,846＋
  `custom_tool_call` 45,841）・claude **28,760**（byte計数28,760と一致）・codex保管 **743**。
  v6でCodex系が厳密計数0（行形が別）だった空白が埋まった。
- **活動時間**（600秒窓・全行timestamp使用）：codex現行 **2,161,626.702秒**・claude
  **1,381,871.866秒**・codex保管 **25,880.816秒**。bucket別（≤60／≤600／≤3600／>3600秒）の
  件数・秒和を併載——窓の再選択は再集計だけで可能。
- **fail-closed計上**：claudeの逆行対**3,567**（並びが時刻順でない）・timestampを持つ行111,154／
  全130,943行（差は前置record等）・時刻帯なし0。Codex 2系統は全行timestampあり・逆行0。
- **経過幅（v6定義・意味不変のまま併載）の脆さの観測**：corpus増（file 560→562・行128,150→
  130,943・厳密byte計数28,210→28,760）にもかかわらず、claudeの`duration_seconds`は
  354,453.59→194,845.506へ減、`duration_unrecognized`は78→83へ増【実測・固定dataset v6/v7の
  機械比較】。経過幅は先頭・末尾行だけに依存するため、末尾へ時刻なしrecordが追記されたfileが
  集計から抜けたと推測される【推測】。全行の時刻を使うv7活動時間はこの依存を持たない——
  精緻化の意義の実証。

## 4. v8候補

日別の時系列展開・複数会話の重複窓統合・rawの意味解析・会話単位の系列出力（作業票§2）。

## 5. 未実施

TODO・見取り図反映とcommit。push（利用者の運用に従う）。
