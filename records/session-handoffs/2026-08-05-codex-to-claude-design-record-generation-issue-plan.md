# Codex → Claude：定型記録生成 Issue のPlan提案作成指示

## 誰が何をするか

- **Human**は、`ISSUE-HTC-66C3E6CA`の「定型記録を機械生成する計画を作る」を選択した。
- **Codex**は、提案の目的、境界、停止条件をこの指示書へ固定する。
- **Claude**は、Human承認待ちのPlan提案、検証receipt、TODO更新だけを作成してcommitする。

これは正式Issue Resolution Plan、Decision、Task Contractではない。`ISSUE-HTC-66C3E6CA`のstateは
`registered`のままにする。実装、RED test、既存recordの書換え、外部操作は行わない。

## 対象Issueと観測

- Issue：`.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json`
- Human triage decision：`.reviewcompass/workflow/triage-decisions-v4/dec-htc-66c3e6ca--v1.json`
- 現行TODO手順：`docs/development/prompts/todo-handoff-update.md`
- 現行TODO renderer：`tools/development/todo_handoff_projection.py`
- 現行TODO validator：`tools/development/todo_handoff.py`
- 現行公式Test receipt生成器：`tools/development/policy_test_runner.py`

問題は、LLMがEvidence・TODO等の定型欄について、receiptの件数や実行条件、file digest、見出しの
挿入位置、完了時刻、監査内訳を手入力または都度推測していることである。その結果、receiptとTODOの数値が
ずれる、正しい見出しを見つけられない、検証前に時刻が確定する、監査の内訳が人に読み取りにくい、といった
手戻りが起きる。直近にも、TODOの全Test件数が`829 passed`のまま、実績`852 passed`へ訂正された。

LLMによる説明文・判断理由の記述は禁止しない。ただし、正本から決定できる定型値、位置、順序、件数、
digest、時刻、集計は機械処理に移す。

## 作成するPlan提案

次を新規作成する。

`docs/design/2026-08-05-record-generation-issue-plan-proposal.md`

状態は`awaiting_human_approval`とする。正式Planではないことを冒頭で明記する。対象Issue、decision、
上記5入力のpathとSHA-256を、作成時の実値で固定する。

提案は、少なくとも以下を平易に記述する。

### 1. 解くことと解かないこと

- **解くこと**：公式Test receipt、対象file、構造化入力から、定型欄を決定的に収集・検証・描画する。
  初期対象は、TODOの関連Test／全Test表示、参照pathとSHA-256、固定見出しの位置、完了後の記録時刻、
  cohort別監査内訳である。
- **解かないこと**：LLMが書く説明・要約・人の判断、Human承認、Issue／Decision／Task Contractの自動作成、
  既存recordの一括修復、Git操作、外部送信。
- TODOは引き続き人向けprojectionであり、stateまたは完了Evidenceの正本にしない。

### 2. 正本と生成経路

「どの値を、どこから、いつ取得し、どこへ出すか」を表にする。少なくとも次を分離する。

- 公式Test receiptから得る結果、suite、Python／pytest版、fallback、実行時刻
- 対象fileのバイト列から再計算するSHA-256
- templateの一意な見出しidentityから得る挿入位置
- 検証完了後にだけ確定する生成・完了時刻
- 構造化監査結果から決定的に集計するcohort内訳
- LLMが書く自由文（非権威の入力として、機械値と混ぜない）

入力の欠落、digest不一致、同一見出しの重複、未知field、receipt失敗、書込み後の再読込不一致では、
出力を更新せず停止する方針を提案する。Test結果のstdout文字列を脆く解析して件数を推測する方式は、
代替案として比較しても、初期実装の正本には採用しない。

### 3. 最小縦切りの比較と推奨

少なくとも次の2案を比較し、最小で再発防止に効く推奨案を示す。推奨はHuman承認まで確定しない。

- **案A**：TODOだけを対象にし、既存の公式Test receiptと参照fileから、構造化projectionを組み立て、
  TODO本文を決定的に描画・検証する。
- **案B**：TODOに加え、Evidence／Decisionの定型欄にも同時に一般化する。

案Aが推奨なら、後で案Bへ進むために必要な境界（共通入力model、version、record種別ごとのrenderer、
authorityを勝手に変更しない規則）を明記する。ただし、汎用frameworkを先行実装する提案にしない。

### 4. 受入条件と検証方針

正常・負例・境界例を具体的に提案する。少なくとも次を含める。

- receiptの件数・version・fallbackがTODO表示へ正しく反映され、手入力差が起きない
- 参照対象を改竄したとき、digest不一致で停止しTODOを変えない
- 見出しが欠落または重複すると停止し、位置推測で書き込まない
- failed receiptまたは未完了verificationから完了表示・完了時刻を生成しない
- cohort集計は入力順に依存せず再現する
- 描画後に再読込、TODO validator、参照整合、byte上限を検証する
- 同じ固定入力から同じ出力が得られる

各条件で、将来どのTest、fault injection、独立照合が必要かを示す。実際のtestは作らない。

### 5. 依存・移行・停止境界

- 現行`todo_handoff_projection.py`、`todo_handoff.py`、`todo_compaction.py`との役割分担
- 既存TODOの手更新から、最小縦切りへ移す順番
- C9のoperation routingとの境界：本Issueは記録内容を決定する。実際のGit／shell等の実行経路は扱わない
- 意味的な文章の書き換えや、authorityの変更が必要になったときの停止・Human判断

### 6. Human判断が必要な点

少なくとも、最初の対象を案Aに限定する可否、何を「公式Test receipt」として受け付けるか、
生成済みTODOの更新をどのcommitへ含めるか、将来Evidence／Decisionへ拡張する条件、実装開始可否を
明示する。

## 必須の確認

1. 対象Issue、decision、現行TODO手順、3つのTODO tool、公式Test runnerを読んでから、提案へ
   pathとSHA-256を固定する。
2. 提案作成後、参照pathとSHA-256を機械再計算して照合する。
3. 公式runnerで全Testを実行し、次のreceiptを作る。

   `records/development/2026-08-05-record-generation-issue-plan-proposal-test-receipt-v1.json`

4. TODOを現在位置だけに更新する。`ISSUE-HTC-66C3E6CA`は`registered`／nonblockingで、Plan提案が
   Human承認待ちであることを示す。3 Issueのstateは変更しない。

## 禁止事項

- 正式Plan、Decision、Task Contract、code、test、config、policyを作成・変更しない。
- 定型記録生成、TODO renderer、receipt parser、監査集計を実装しない。
- 既存TODO以外の既存Evidence、Decision、Issue、receiptを変更しない。
- push、PR、外部送信、hook、watcher、scheduler、background serviceを開始しない。

## コミットと完了報告

- Plan提案、TODO更新、test receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

  `records/session-handoffs/2026-08-05-claude-to-codex-design-record-generation-issue-plan.md`

報告には、commit SHA、提案path・Digest、比較した最小縦切り案、推奨、Human判断点、全Test結果、
未実施事項を記す。
