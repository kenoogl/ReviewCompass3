# セッションログ前置record解釈（契約014候補） 作業契約候補 v2

- 作成日：2026-08-17
- 起草者：Claude
- v2改定：利用者「Aで承認。§7.4を改定した候補v2を固定してからREDへ着手して」（2026-08-17
  chat）。改定理由＝補助分類の利用2箇所（`cli.py` 360行・`private_validation.py` 145行）は
  「補助と判定したfileの**転写・機微削除済み派生物の生成をスキップ**する」意味であり、v1
  §7.4（判定不変）のままでは本文ありの前置開始fileが派生物経路で無視され続け、契約目的の
  半分が未達になると判明したため。v1＝`…-candidate-v1.md`（commit `3c9b1b9`・本v2で置換）
- 採用：v1は2026-08-17に採用済み（採用判断record
  `records/development/2026-08-17-session-log-prefix-interpretation-contract-adoption-decision-v1.md`・
  残余risk4点受容）。本v2は§7.4改定＋整合箇所のみの差分であり、v2固定の承認は冒頭の指示文言
  を根拠とする
- 種別：Task Contract（契約014）。RED着手可
- 主題：デスクトップ起点セッションのJSONL先頭に付く前置record（`queue-operation`・`mode`・
  `custom-title`・`started`）を既知の正準列として読み飛ばし、実会話を含むfileを解釈・転写の
  対象へ戻す。過去の解釈非対応分は判定拡張後の通常実行で自然遡及させる

## 1. 位置と縮小境界

- 位置：改善候補`IC-SESSION-LOG-PREFIX-INTERPRETATION-001`の採用（2026-08-17仕分けrecord）を
  実装する契約。session log系の独立作業であり、レビュー基盤module（休止中）の再開ではない。
- 縮小境界：変更は判定器`source_kind.py`（種別判定＋補助分類）・解釈器`parse_claude.py`
  （限定1点・§7.3）・試験・手順書1段落に限る。振り分け（`source_adapter.py`）・保全機構・
  転写再生成・record-run wrapperは変更しない。

## 2. Human承認境界

- 候補の採用と残余risk受容（v1採用済み・§7.4改定はv2冒頭の文言で承認済み）。
- **既存試験の書換え範囲**（§5.1-3の6 file一覧）の承認（v1採用に含めて承認済み）。
- 遡及の受入実測（実環境での`record-run`実行）は利用者の実行指示ごと。
- 段完了・製品受入の判断。

## 3. 権威、証拠

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 仕分けDecision | `records/development/2026-08-17-session-log-prefix-interpretation-triage-decision-v1.md` | `baf2bfa9a8ac2c91cf03b81410b5806e8c23d450fa6b287e7d8a031e6f95bffb` |
| 事前走査record（digest表23行を含む） | `records/development/2026-08-17-session-log-prefix-interpretation-prescan-v1.md` | `53cfdcd39904d4ceb43e4d8e8e991c8a4201430d2ea47fb2af8d6fc0ecf03055` |
| 正式検索計画 | `records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json` | `e9680cf17eec303303673e6ddcb7b1206260d596179c675659ba3e488e47a96e` |
| 正式検索証明書（`start_allowed: true`） | `records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-attestation-v1.json` | `f17f9a951e99d4fe4d583b02389ba9c2d9370585631139c0379d89d64acc9eae` |
| 採用判断record（v1採用・残余risk受容） | `records/development/2026-08-17-session-log-prefix-interpretation-contract-adoption-decision-v1.md` | （commit `a8219f3`） |

基準commit：`a8219f3`。対象fileの個別digestは事前走査record §5の表を正とする。

## 4. 実装方法の3案

- **案A（採用）**：`source_kind.py`へ前置スキップの正準列判定を追加し、前置種別の定義を共有
  して種別判定・補助分類・解釈器（`parse_claude.py`の無issueスキップ）が同じ規則を参照する。
  既存構造の拡張のみ・新moduleなし。
- 案B：`source_kind.py`の種別判定だけ変更し解釈器・補助分類は不変。前置recordのissue計上で
  「issueあり成功」が常態化し、補助分類経由の転写スキップで派生物の取りこぼしが残るため不採用。
- 案C：前置除去の前処理moduleを新設。新部品・新接続点が増え、byte原本と解釈対象がずれるため
  不採用。

## 5. 範囲

### 5.1 範囲内

1. `tools/session_logs/source_kind.py`：前置4種の正準列定義（§7.1の必須欄）・前置スキップ判定
   （上限16・超過/未知/判定可能record不在は非対応）・`identify_source_kind_bytes`／
   `identify_source_kind`の拡張・**補助分類`identify_auxiliary_kind`の判定変更（§7.4：本文
   recordを持たないfileのみ補助）**。
2. `tools/session_logs/parse_claude.py`：前置4種recordの無issueスキップ（§7.3。共有定義の参照
   のみ・解釈規則は不変）。
3. 試験：新設試験（新仕様＋敵対fixture§7.5）のRED先行と、既存試験の期待値修正——対象は次の
   **6 file**に限る：`tests/test_session_log_source_kind.py`・`tests/test_session_log_parse_claude.py`・
   `tests/test_session_log_eventual_preservation.py`・`tests/test_session_log_cli.py`・
   `tests/test_session_log_private_validation.py`・`tests/test_session_log_record_run.py`
   （queue開始fileでpartialを固定する1試験）。修正原則＝試験の意図を保存し、fixture（前置前提
   →本文なし補助・未知種別前提）と期待値のみ新仕様へ差し替える。
4. 手順書`docs/development/prompts/session-log-record-run.md` §2の非対応説明の改定（1段落）。
5. 遡及の受入実測（§7.5-2。実環境`record-run`の前後比較。実施は利用者指示）。

### 5.2 範囲外

- `source_adapter.py`・`eventual_preservation.py`・`regeneration.py`・`record_run.py`・保全機構
  （raw先行保存）・一件用安全保存の変更。
- 未知前置種別の推測解釈（fail-closed維持）。`mode`の補助分類への登録（補助分類は§7.4の
  本文有無規則で扱い、種別の追加登録はしない）。
- Codex 2形式の判定変更。過去分rawの書換え（遡及は解釈のやり直しのみ）。
- レビュー基盤moduleのpending残件。

## 6. 固定再利用部品と保護基準

- 流用元（正式検索の直接一致より）：`_identify_first_event`・`_first_record`（拡張対象）、
  `identify_auxiliary_kind`（判定変更対象）、`_parse_lines`（限定変更）、
  `reconcile_source_root`・`regenerate_transcript`（無変更のまま遡及・確認に利用）。
- 保護基準：session_logs系試験全域（2026-08-17実測215本＋record-run 10本、書換え後の新期待で）
  の単独終了コード0。保全（raw）・cursor・台帳の形式は不変。

## 7. 中心的な取り決め

### 7.1 正準列の定義（論点1）

先頭から連続する**既知前置record**だけを読み飛ばし、最初の判定可能recordで従来判定
（Claude本文形式・Codex 2形式）を行う。既知前置の必須欄（実物基準・事前走査record §1）：

| 種別 | 必須欄 |
| --- | --- |
| `queue-operation` | `operation`∈{enqueue, dequeue}・`sessionId`（str非空）・`content`存在 |
| `mode` | `mode`（str）・`sessionId`（str非空） |
| `custom-title` | `customTitle`（str）・`sessionId`（str非空） |
| `started` | `agentId`（str非空）・`key`（str非空） |

- `type`が上記4種のrecordは、他の欄（`uuid`等）を持っていても本文形式と判定しない（前置経路で
  必須欄を検査する）。
- スキップ上限は**16 record**（実測の連続数3〜4個の4倍）。超過は非対応。
- 必須欄に合致しないrecord（偽装・未知種別）が現れた時点で打ち切り、その位置で従来判定に
  合致しなければ非対応（fail-closed）。

### 7.2 判定の互換（論点2）

先頭が本文形式・Codex 2形式のfileは従来どおりの判定。既存の判定試験のうち互換部分の検査は
無修正のまま通す。

### 7.3 issue計上の扱い（論点8・(b)採用）

`parse_claude._parse_lines`は既知前置4種（§7.1と同一の共有定義を参照）を**無issueで**読み
飛ばす。それ以外の非会話recordは従来どおり`unsupported_event` issueに計上する（本物の異常が
issueに残る）。解釈規則（会話recordの処理）は不変。

### 7.4 補助分類の変更（論点6・v2改定）

`identify_auxiliary_kind`を「**本文recordを持たないfileだけが補助**」へ変更する。判定手順：
§7.1と同一の正準列規則で最初の判定可能recordを探し、

- 本文形式recordへ到達できるfileは**補助でない**（`None`を返す。転写・派生物経路の処理対象に
  なる）。
- 到達できないfile（前置のみ・上限超過・未知種別で打ち切り）は従来どおり先頭recordで補助判定
  （`queue-operation`→`claude_queue`・`started`→`claude_agent`・それ以外は`None`＝非対応）。

利用2箇所（`cli.py`転写生成・`private_validation.py`検証）で、本文ありの前置開始fileが
スキップされず処理対象になることを試験で確認する（解釈できないfileのスキップは従来どおり）。

### 7.5 敵対fixtureと遡及の受入（論点3・5）

1. RED段に次の敵対fixtureを標準で含める：(a) 本文recordを装う前置（`uuid`・`sessionId`を持つ
   `queue-operation`風——本文と誤認しないこと）、(b) 前置を装う欠落record（必須欄不足の前置風
   record——打ち切り）、(c) 既知前置列の途中に未知種別が混入（打ち切り）、(d) 前置のみで本文が
   無いfile（非対応・補助分類は従来判定）、(e) 上限16超過（非対応）。期待はいずれも
   fail-closed側を固定する。
2. 遡及の受入実測：実環境`record-run`の前後比較で、claude系統の解釈非対応が68件（2026-08-16
   実測）から「本文recordを持たないfile・未知種別のみ」へ遷移することを要約JSONの機械転記で
   照合する。遷移しないfileが残る場合は内訳（種別・件数）を報告し成功として数えない。

### 7.6 残余risk（v1で受容済み・4点）

1. **前置種別の将来変化**：新しい前置種別が現れるとそのfileは再び非対応になる（既知4種限定の
   fail-closedの裏面）。緩和：`record-run`要約の非対応件数の急変で検知、同型の小改定で対応。
2. **スキップ上限16の恣意性**：超える正当なログは非対応側（安全側）に倒れる。緩和：定数1箇所・
   試験つき小改定で変更可能。
3. **既存試験書換えによる意図変質**：緩和：修正原則（意図保存・期待値のみ差し替え）を§5.1-3に
   固定し、完了レビューで書換え差分を対象にする。
4. **遡及の一斉遷移**：台帳・cursorに想定外があり得る。緩和：保全（raw）不変・原本無傷・
   再実行可能。遷移の照合は§7.5-2で機械化。

## 8. 変更上限

- 変更file：`source_kind.py`・`parse_claude.py`・試験7 file（新設1＋既存6）・手順書1——
  **計10 fileを上限**とし、超える変更が必要と判明したら停止して報告する。
- schema・保全形式・CLI引数・G30・外部送信への変更なし。

## 9. 受入条件

1. RED：新仕様試験＋敵対fixture 5形（§7.5-1）＋補助分類新仕様の試験が実装前に作成され、
   試験fileが失敗すること（単独終了コード非0。互換・fail-closed既定の検査が現仕様でも通るのは
   互換の証明として正）。
2. GREEN：新設試験全通過・session_logs系全域（書換え後の期待で）全通過——いずれも単独実行の
   終了コード0。
3. 既存試験の書換えが§5.1-3の一覧（6 file）の範囲内であること（`git diff`のfile一覧で機械確認）。
4. 手順書§2の改定済み。
5. 遡及の受入実測（§7.5-2）が完了し、前後比較の要約が転記されていること（実施は利用者指示。
   未実施の間は契約完了と区別して報告する）。
6. 意味単位commit・`work_unit_transition --work-status completed`合格。

## 10. 停止条件

- §5.1-3の一覧外の試験書換え、または§8の変更上限超過が必要と判明した時点。
- `source_adapter.py`等の範囲外fileへの変更が必要と判明した時点。
- 遡及実測で失敗・消失の増加など想定外遷移が出た時点（保全不変を確認して停止・報告）。

## 11. 影響、未実施、次作業

- 影響：完了後、当環境のClaude会話（前置開始）が解釈・転写の対象に戻り、過去の非対応68件も
  次回実行で遡及される。`record-run`要約の非対応は「本文なし補助・未知種別」だけに縮小する。
  **補助分類の縮小により、転写・検証経路（`cli.py`・`private_validation.py`）の処理対象が遡及
  初回に一時増加する**（これまでignoredだった本文ありfileが処理される。機微削除の検査対象が
  増えるのは意図どおりの効果）。
- 未実施：RED/GREEN、既存試験書換え、手順書改定、遡及実測。
- 次作業：RED着手（v2固定後、冒頭の指示文言により承認済み）。
