# Codex → Claude：機械操作routing後続範囲のPlan提案作成指示

## 誰が何をするか

- **Human**は、`ISSUE-HTC-C9F6C917`の後続範囲を実施するよう選択した。
- **Codex**は、今回の範囲を「後続実装のPlan提案」に限定して固定する。
- **Claude**は、Human承認待ちのPlan提案、検証receipt、TODOの現在位置だけを作成し、1つの意味的commitにする。

今回の選択は、後続範囲の**実装承認ではない**。正式Decision、Task Contract、Issue stateの変更でもない。

## 対象と現在の境界

- 対象Issue：`.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`
- 主triage decision：`.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json`
- 既存の正本設計：`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`
- 完了済み最小縦切りの承認：`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`
- 現在の実装：`tools/development/operation_routing.py`

完了済みなのは、operation inventory、permission preflight、execution receiptの3部だけである。
次の後続項目は未承認・未実装である。

1. shellを経由しない構造化argv executor
2. task専用Python cache rootの決定的な固定
3. 既存の直接shell／Git操作を安全に移す順序
4. host側tool構文と外部送信をproject内の解決済みと誤報しない境界

## Claudeが作成するもの

次のPlan提案を新規作成する。

`docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`

状態は`awaiting_human_approval`とする。冒頭で、実装許可・正式Decision・Task Contractではないことを明記する。

### Planに必ず含める内容

1. **現状と目的**
   - 最小縦切りが何を解決済みで、何を未解決として残しているかを平易に区別する。
   - 5観測（Git metadata、Python cache、shell引用、shell特殊変数、host tool構文）との対応を再確認する。

2. **後続3部の責任境界**
   - argv executorは、`argv`を文字列shellへ再結合せず、各要素の型・空値・cwd・許可対象をどう検証するかを提案する。
   - executorがprocessを起動する責任と、既存`operation_routing.py`が権限種別を計算するだけの責任を混同しない。
   - cache rootは、project成果物・任意の外部root・利用者の通常cacheを汚さない配置候補、作成権限、cleanup／保持、Windows・Linux・macOSを含む境界を比較する。
   - 既存直接操作は、機械抽出した移行inventoryを作ってから、一種類ずつ移す。全面置換を一括実行しない。

3. **安全な段階と各段階の停止条件**
   - 少なくとも「設計固定 → RED test → argv executor最小slice → cache root最小slice → 移行inventory → 操作種別ごとの段階移行」の順を比較し、推奨順を示す。
   - 各段階で、何を実装しないか、Human承認が必要になる条件、既存の動作を変更しない確認を明示する。
   - `unknown`分類、未取得権限、scope外host操作、external操作、identity／receipt不一致では停止する既存原則を維持する。

4. **移行対象の調査方法**
   - 現在の`tools/`および関連testから、直接shell実行、Git書込み、Python cache設定を**機械検索で列挙する方法**を示す。
   - ただし今回、移行inventory・code・testを新規作成しない。Plan内に、次段階で作る成果物と選定規則を提案するだけに留める。

5. **受入条件・検証方針**
   - argvに空白、引用符、backtick、shell特殊文字を含んでもshell解釈に渡らないこと。
   - 不正argv、unsafe cwd、未取得権限ではprocessが一度も起動しないこと。
   - cache rootがproject内や意図しないrootへ書かれないこと。
   - 移行前後の操作分類、権限preflight、receipt identityを比較して、挙動の後退を検出すること。
   - Windows・Linux・macOSの差を、何を共通仕様、何をplatform adapterとして扱うか。
   - それぞれに正常例・負例・境界例・必要な独立確認を提案する。Testは作成しない。

6. **Human判断点**
   - argv executorの許容操作種別と実行責任の境界。
   - cache rootの配置・削除／保持方針。
   - 移行対象の優先順と、最初の実装sliceの承認可否。
   - project外であるhost tool構文・外部送信を本Issueで扱わないことの確認。

## 必須の確認と更新

1. 上記の対象Issue・decision・既存設計・既存承認・実装を読み、提案にpathと作成時点のSHA-256を固定する。
2. 実装の現状をread-onlyで調べ、Planの「現状」主張を根拠付きにする。推測で直接操作の件数を書かない。
3. 提案作成後に再読込し、参照pathとDigestを機械照合する。
4. 公式policy runnerで全Testを実行し、次のreceiptを作成する。

`records/development/2026-08-05-machine-operation-routing-follow-on-plan-test-receipt-v1.json`

5. `TODO_NEXT_SESSION.md`を共通手順に従って現在位置だけ更新する。`ISSUE-HTC-C9F6C917`は`registered`かつnonblockingのままとし、後続PlanがHuman承認待ちであることを示す。他のIssue stateは変えない。
6. TODO validator、compaction validator、参照整合、`python3 tools/development/work_unit_transition.py --work-status completed`を実行する。

## 禁止事項

- code、test、config、policy、既存Plan、既存Decision、Task Contract、Issue recordを変更しない。
- argv executor、cache root、移行inventory、Git／shell操作の置換を実装しない。
- Git／shell／Python cacheの実行自動化、push、外部送信、hook、watcher、schedulerを開始しない。
- host側tool構文、sandbox／host権限承認、外部tool APIをproject内で解決したと書かない。
- RED testを作らない。今回の成果は文書提案である。

## commitと完了報告

- 次の3種だけを明示pathでstageし、1つの意味的commitにする：新規Plan提案、test receipt、TODO更新。
- commit前に`git diff --check`、該当validator、全Testを確認し、commit後にread-only照合する。
- 完了報告はcommitに混ぜず、Git管理外の次のpathへ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-plan-machine-operation-routing-follow-on.md`

報告には、commit SHA、Plan pathとDigest、推奨した段階順、Human判断点、全Test結果、未実施事項を記す。
