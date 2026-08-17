# セッションログ前置record解釈（契約014候補） 作業契約候補 v1

- 作成日：2026-08-17
- 起草者：Claude
- 指示：利用者「Aで採用。仕分けrecordを作成し、事前走査から着手して」→事前走査固定後
  「契約候補v1を起草して。論点の推奨込みで提示まで」（いずれも2026-08-17 chat）
- 種別：Task Contract候補（採用判断待ち。採用判断まで実装に着手しない）
- 主題：デスクトップ起点セッションのJSONL先頭に付く前置record（`queue-operation`・`mode`・
  `custom-title`・`started`）を既知の正準列として読み飛ばし、実会話を含むfileを解釈対象へ
  戻す。過去の解釈非対応分は判定拡張後の通常実行で自然遡及させる

## 1. 位置と縮小境界

- 位置：改善候補`IC-SESSION-LOG-PREFIX-INTERPRETATION-001`の採用（2026-08-17仕分けrecord）を
  実装する契約。session log系の独立作業であり、レビュー基盤module（休止中）の再開ではない。
- 縮小境界：変更は判定器`source_kind.py`・解釈器`parse_claude.py`（限定1点・§7.3）・試験・
  手順書1段落に限る。振り分け（`source_adapter.py`）・保全機構・転写再生成・record-run wrapper
  は変更しない。

## 2. Human承認境界

- 本候補の採用判断（残余risk§7.6の受容を含む）。
- **既存試験の書換え範囲**（§5.1-3の5 file一覧）の承認（本候補の採用に含めて諮る）。
- 遡及の受入実測（実環境での`record-run`実行）は利用者の実行指示ごと。
- 段完了・製品受入の判断。

## 3. 権威、証拠

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 仕分けDecision | `records/development/2026-08-17-session-log-prefix-interpretation-triage-decision-v1.md` | `baf2bfa9a8ac2c91cf03b81410b5806e8c23d450fa6b287e7d8a031e6f95bffb` |
| 事前走査record（digest表23行を含む） | `records/development/2026-08-17-session-log-prefix-interpretation-prescan-v1.md` | `53cfdcd39904d4ceb43e4d8e8e991c8a4201430d2ea47fb2af8d6fc0ecf03055` |
| 正式検索計画 | `records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json` | `e9680cf17eec303303673e6ddcb7b1206260d596179c675659ba3e488e47a96e` |
| 正式検索証明書（`start_allowed: true`） | `records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-attestation-v1.json` | `f17f9a951e99d4fe4d583b02389ba9c2d9370585631139c0379d89d64acc9eae` |

基準commit：`cce8092`。対象fileの個別digestは事前走査record §5の表を正とする。

## 4. 実装方法の3案

- **案A（推奨）**：`source_kind.py`へ前置スキップの正準列判定を追加し、前置種別の定義を共有定数
  として`parse_claude.py`が参照（前置4種を無issueでスキップ）。既存構造の拡張のみ・新module
  なし。
- 案B：`source_kind.py`だけ変更し解釈器は不変。前置recordが毎回`unsupported_event` issueに計上
  され、遡及後はclaude系ほぼ全fileが「issueあり成功（parse_issues）」になる。本物の異常（壊れた
  行）がissueの中に埋もれ、正直な申告の原則に反するため不採用。
- 案C：前置除去の前処理moduleを新設し判定・解釈の前段に置く。新部品・新接続点が増え、byte原本と
  解釈対象がずれる（運搬層の複雑化）ため不採用。

## 5. 範囲

### 5.1 範囲内

1. `tools/session_logs/source_kind.py`：前置4種の正準列定義（§7.1の必須欄）・前置スキップ判定
   （上限16・超過/未知/判定可能record不在は非対応）・`identify_source_kind_bytes`／
   `identify_source_kind`の拡張・補助分類の意味の明文化（§7.4）。
2. `tools/session_logs/parse_claude.py`：前置4種recordの無issueスキップ（§7.3。共有定義の参照
   のみ・解釈規則は不変）。
3. 試験：新設試験（新仕様＋敵対fixture§7.5）のRED先行と、既存試験の期待値修正——対象は次の
   **5 file**に限る：`tests/test_session_log_source_kind.py`・`tests/test_session_log_parse_claude.py`・
   `tests/test_session_log_eventual_preservation.py`・`tests/test_session_log_cli.py`・
   `tests/test_session_log_private_validation.py`。修正原則＝試験の意図を保存し、fixture（前置
   前提→本文なし補助・未知種別前提）と期待値のみ新仕様へ差し替える。
   ※`tests/test_session_log_record_run.py`の1試験（queue開始fileでpartialを固定）も同原則の
   対象に含む（計6 file）。
4. 手順書`docs/development/prompts/session-log-record-run.md` §2の非対応説明の改定（1段落）。
5. 遡及の受入実測（§7.5-2。実環境`record-run`の前後比較。実施は利用者指示）。

### 5.2 範囲外

- `source_adapter.py`・`eventual_preservation.py`・`regeneration.py`・`record_run.py`・保全機構
  （raw先行保存）・一件用安全保存の変更。
- 未知前置種別の推測解釈（fail-closed維持）。`mode`の補助分類への登録（実害が出てから）。
- Codex 2形式の判定変更。過去分rawの書換え（遡及は解釈のやり直しのみ）。
- レビュー基盤moduleのpending残件。

## 6. 固定再利用部品と保護基準

- 流用元（正式検索の直接一致より）：`_identify_first_event`・`_first_record`（拡張対象）、
  `_parse_lines`（限定変更）、`reconcile_source_root`・`regenerate_transcript`（無変更のまま
  遡及・確認に利用）。
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

- スキップ上限は**16 record**（実測の連続数3〜4個の4倍）。超過は非対応。
- 必須欄に合致しないrecord（偽装・未知種別）が現れた時点で打ち切り、その位置で従来判定に
  合致しなければ非対応（fail-closed）。

### 7.2 判定の互換（論点2）

先頭が本文形式・Codex 2形式のfileは従来どおりの判定。既存の判定試験は無修正で緑を維持する
（互換の証明として書換え対象から除外……ではなく、5.1-3の5 fileのうち互換部分の検査は無修正の
まま通す）。

### 7.3 issue計上の扱い（論点8・推奨(b)採用）

`parse_claude._parse_lines`は既知前置4種（§7.1と同一の共有定義を参照）を**無issueで**読み
飛ばす。それ以外の非会話recordは従来どおり`unsupported_event` issueに計上する（本物の異常が
issueに残る）。解釈規則（会話recordの処理）は不変。

### 7.4 補助分類の意味（論点6）

「**本文recordを持たないfileだけが補助（auxiliary）または非対応**」と明文化する
（docstringと試験で固定）。`identify_auxiliary_kind`の判定自体は不変（利用2箇所——私有領域
検証・転写生成のスキップ判定——の意味互換を試験で確認）。

### 7.5 敵対fixtureと遡及の受入（論点3・5）

1. RED段に次の敵対fixtureを標準で含める：(a) 本文recordを装う前置（uuid・sessionIdを持つ
   queue-operation風）、(b) 前置を装う本文の欠落（必須欄不足の前置風record）、(c) 既知前置列の
   途中に未知種別が混入、(d) 前置のみで本文が無いfile、(e) 上限16超過。それぞれ期待は
   fail-closed側（非対応・打ち切り）を固定する。
2. 遡及の受入実測：実環境`record-run`の前後比較で、claude系統の解釈非対応が68件（2026-08-16
   実測）から「本文recordを持たないfile・未知種別のみ」へ遷移することを要約JSONの機械転記で
   照合する。遷移しないfileが残る場合は内訳（種別・件数）を報告し成功として数えない。

### 7.6 残余risk（明示的に受容を諮る）

1. **前置種別の将来変化**：Claude Code側の更新で新しい前置種別が現れると、そのfileは再び
   非対応になる（既知4種限定のfail-closedの裏面）。緩和：`record-run`要約の非対応件数の急変で
   検知でき、種別追加は本契約と同型の小改定で対応可能。
2. **スキップ上限16の恣意性**：実測3〜4個の4倍で置いた値であり、将来それを超える正当なログが
   現れると非対応側（安全側）に倒れる。緩和：上限は定数1箇所で、変更は試験つき小改定。
3. **既存試験書換えによる意図変質**：5＋1 fileのfixture差し替えで試験の意図が変わるrisk。
   緩和：修正原則（意図保存・期待値のみ差し替え）を§5.1-3に固定し、完了レビューで書換え差分を
   対象にする。
4. **遡及の一斉遷移**：次回実行で68件が一斉に状態遷移し、台帳・cursorに想定外があり得る。
   緩和：保全（raw）は不変のため失敗しても原本無傷・再実行可能。遷移の照合は§7.5-2で機械化。

## 8. 変更上限

- 変更file：`source_kind.py`・`parse_claude.py`・試験7 file（新設1＋既存6）・手順書1——
  **計10 fileを上限**とし、超える変更が必要と判明したら停止して報告する。
- schema・保全形式・CLI引数・G30・外部送信への変更なし。

## 9. 受入条件

1. RED：新仕様試験＋敵対fixture 5形（§7.5-1）が実装前に失敗（単独終了コード非0の確認）。
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

- 影響：完了後、当環境のClaude会話（前置開始）が解釈対象に戻り、過去の非対応68件も次回実行で
  遡及される。`record-run`要約の非対応は「本文なし補助・未知種別」だけに縮小する。
- 未実施：採用判断、RED/GREEN、既存試験書換え、手順書改定、遡及実測。
- 次作業：採用判断（本候補の承認）→RED着手。
