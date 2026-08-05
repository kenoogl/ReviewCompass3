# Codex → Claude：定型記録生成のTODO最小縦切り 実装指示

## 誰が何をするか

- **Human**は、`ISSUE-HTC-66C3E6CA`のPlan提案について、次の5点を一括で承諾した。
  1. 最初の対象はTODOだけに限定する。
  2. Test件数はstdoutを正規表現で読むのではなく、公式Test receiptの構造化集計から得る。
  3. 自動生成したTODOは、作業本体と同じ意味単位commitへ含め、TODOだけの追加commitを作らない。
  4. Evidence／Decisionへの拡張は、TODOで複数回の実運用が手入力訂正なしで通ってからHumanが判断する。
  5. 実装はTest先行で、受領証の集計、TODO用材料の収集、更新経路の切替の順に分ける。
- **Codex**は、承認内容、実装順序、禁止事項、停止条件をこの指示書へ固定する。
- **Claude**は、承認記録を作成した後、下記の3段階をTest先行で実装し、各段階を緑の意味単位commitとして確定する。

正式Issueのstateは`registered`のままにする。V4の正式Issue Resolution Plan、Task Contract、Workflow permitを
作らない。

## 固定入力

- Plan提案：`docs/design/2026-08-05-record-generation-issue-plan-proposal.md`
- 対象Issue：`.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json`
- Human triage decision：`.reviewcompass/workflow/triage-decisions-v4/dec-htc-66c3e6ca--v1.json`
- TODO手順：`docs/development/prompts/todo-handoff-update.md`
- Test runner：`tools/development/policy_test_runner.py`
- TODO renderer：`tools/development/todo_handoff_projection.py`
- TODO validator：`tools/development/todo_handoff.py`
- TODO compaction validator：`tools/development/todo_compaction.py`

作業開始時にこれらを読み、Planの固定input SHA-256が現状と一致することを機械確認する。不一致なら、
局所修正せず停止して報告する。

## 0. 承認記録（最初のcommit）

最初に、次を同じcommitへ入れる。

- `records/development/2026-08-05-record-generation-issue-plan-approval-decision-v1.md`を新規作成する。
  `DEC-RECORD-GENERATION-PLAN-001`として、Humanの上記5承諾をそのまま記録する。
- Plan提案の状態を`approved_for_development_implementation`へ更新する。
- TODOを、当該Planが承認済みで、以下のTODO最小縦切りを実装中である現在位置へ更新する。

このcommitは文書・Decision・TODOだけである。`ISSUE-HTC-66C3E6CA`、他のIssue、既存receiptは変更しない。
TODO validator、TODO compaction validator、参照digest照合、`git diff --check`を通してからcommitする。

## 1. 公式Test receiptの構造化集計（Test先行・第2 commit）

### 目的

`policy_test_runner`が出す**新しい**receiptへ、stdoutを解析せずに読める構造化`test_summary`を追加する。
この値がTODOの全Test表示の唯一の数値sourceになる。

### 必須の振る舞い

- `test_summary`には少なくとも`passed`、`failed`、`skipped`、`xfailed`、`xpassed`、`errors`、
  `total`を整数で持たせる。値の定義をmodule docstringまたは同等の機械近接文書へ明記する。
- 集計はpytestのmachine API（hook／pluginまたは同等の構造化結果）から得る。`stdout`／`stderr`を
  正規表現・文字列分割で解析してはならない。
- Test実行に失敗してもreceiptは残し、summaryと`status`が矛盾しない。plugin summaryが得られない場合は、
  `test_summary_unavailable`として通常の成功を装わず停止する。
- 既存receiptは履歴として変更しない。新fieldが無い旧receiptを今回のTODO自動更新入力として受理しない。
- runnerの既存identity、configured Python、fallback禁止、source-state digestの自己参照除外を壊さない。

### Test

実装より先に`tests/test_policy_test_runner.py`または同じ責務の新規Testへ、正常・失敗・summary欠落の
Testを追加する。REDを確認してから実装する。GREENでは対象Testと公式全Testを実行する。

この段階のcommitは、Test、receipt集計に必要なmodule、`policy_test_runner.py`だけに限定する。
TODOを実際に機械更新しない。

## 2. TODO用材料の収集・検証（Test先行・第3 commit）

### 目的

構造化`test_summary`を持つ公式receiptと、既存TODO内の参照pathから、TODOの機械管理部分を
決定的に作る入力収集器を実装する。

### 境界

- LLM／Humanが書いた全体説明、判断理由、次作業などの自由文は再解釈・再生成しない。既存bytesを保持する。
- 機械が更新する対象は、`## Git・Test`の「直近の全Test」行と、`## 最新のauthority／Evidence`にある
  Markdown linkのSHA-256値だけである。関連Testの意味的な選定、link label、link path、行の並びは
  自動で決めない。既存の値をそのまま保つ。
- 見出しは完全一致でちょうど1回、対象行はちょうど1回でなければならない。近傍探索・行番号・位置推測で
  書き込まない。
- 各参照pathはproject root内の通常fileでなければならず、絶対path、`..`、symlink、欠落、digest不一致は
  `TODO_NEXT_SESSION.md`を変えずに停止する。
- `test_summary`が無い、`status != passed`、`fallback_used != false`、集計値が不正、未知field、
  receiptと表示に必要なPython／pytest versionが欠ける場合も、TODOを変えずに停止する。

既存の`render_todo_handoff()`は置き換えない。この最小sliceは、既存TODOの自由文を失わない**section内の
決定的更新器**である。全TODOを新しいschemaへ移すことは、Evidence／Decision拡張と同じく後続判断に送る。

### Test

実装より先に、次の正例・負例・境界例をTestへ固定する。

- 正常：receiptの構造化summary、version、fallbackが全Test行へ反映され、参照digestが再計算される。
- 改竄：参照fileを1 byte変えると停止し、TODO bytesが変わらない。
- receipt異常：summary欠落、`failed`、fallback、未知field、負数または`total`不整合で停止し、TODO bytesが変わらない。
- 構造異常：必須見出し／対象行の欠落・重複で停止し、TODO bytesが変わらない。
- path異常：絶対path、`..`、symlinkで停止する。
- 同じ固定入力から同じcandidate bytesが得られる。

GREENでは対象Testと公式全Testを実行する。commitには収集／更新moduleとTestだけを含め、root TODOは
まだ更新しない。

## 3. root TODOへの更新経路の切替（Test先行・第4 commit）

### 二段確認

receiptとTODOのsource-state identityを食い違わせないため、次の順序を固定する。

1. すべてのcode／Test変更後、公式全Testを一度実行して**一時receipt**を作る。
2. 一時receiptからroot `TODO_NEXT_SESSION.md`のcandidateを機械生成し、atomic writeする。
   自由文、link label、link path、順序は変えない。
3. TODO validator、TODO compaction validator、参照digest照合、read-back byte一致を通す。
4. 公式全Testを二度目に実行し、commitへ入れる**最終GREEN receipt**を作る。
5. 二つの`test_summary`、suite、Python版、pytest版、fallback、statusが完全一致することを機械照合する。
   不一致ならroot TODOを元bytesへ復元し、commitせず停止・報告する。

この手順により、TODOが示す数値は二度目の正式receiptの構造化値と一致し、最終receiptの
`source_state_digest`も更新済みTODOを含む状態を示す。

### Test

実装より先に、二段確認の正常例、二回の集計不一致、post-write read-back不一致、validator failureの
各Testを固定する。不一致／失敗ではroot TODOを変更前のbytesへ戻すことを確認する。RED確認後に実装する。

GREENで、最終receiptと最終GREEN Evidenceを次へ保存する。

- `records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json`
- `records/development/2026-08-05-record-generation-todo-green-evidence-v1.md`

Evidenceには、二段のreceiptのpath・SHA-256、summary一致、TODOの更新範囲、validator結果、全Test結果、
既存Issueが`registered`のままであること、未実施の拡張を記録する。

最終commitは、更新経路のmodule／Test、root TODO、最終GREEN receipt、GREEN Evidenceだけを含める。
TODOだけの追加commitは作らない。

## 共通の禁止事項

- Evidence／Decisionの自動生成、既存Evidence／Decision／receiptの一括書換え、Issue state変更、
  Task Contract、Workflow permit、UI、hook、watcher、scheduler、background serviceを作成・変更しない。
- Git／shell／外部toolの実行routingを実装しない。C9の範囲へ入らない。
- stdout／stderrの文字列からTest件数を抽出しない。
- `git add -A`または`git add .`を使わない。各commitは明示pathだけをstageする。
- push、PR、外部送信は行わない。

## 停止条件

次の場合だけ、局所patchで続けず、実装を止めてCodexへ報告する。

1. 固定input digestが開始時点で不一致。
2. machine APIを使って構造化summaryを得るために、上記範囲を超えるpolicy／config／外部依存の変更が必要。
3. root TODOを更新すると自由文、link label、link path、順序など非機械管理部分も変わる。
4. 二段確認で二つのsummaryが不一致、または更新失敗時に原状復帰できない。
5. 既存Task Contractまたはauthorityの固定source整合が崩れ、更新には新しいHuman判断が必要。

## 完了報告

上記4 commitを完了したら、commitに混ぜず次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-implement-record-generation-todo-slice.md`

報告には、各commit SHAと役割、RED／GREEN結果、最終receipt summary、二段確認の一致、TODOの実際の変更範囲、
未実施の範囲、停止なし／ありを明記する。
