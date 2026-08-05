# Codex → Claude：機械操作routing IssueのPlan提案作成指示

## 誰が何をするか

- **Human**は、承認済みV4 Issueの優先順に従い、`ISSUE-HTC-C9F6C917`のPlan提案を先に検討するよう指示した。
- **Codex**は、提案作成の範囲と停止境界をここに固定する。
- **Claude**は、Human承認待ちのPlan提案、test receipt、TODO更新だけを作成してcommitする。

これは正式Issue Resolution Planの作成・承認ではない。Issueのstateは`registered`のままにする。
実装、RED test、runner・config・policy変更、権限昇格、外部操作は行わない。

## 対象Issueと根本問題

- Issue：`.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`
- Human triage decision：`.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json`

問題は、LLMがGit書込み、shell実行、ツール呼出、Python cacheの決定的な実行手順をその場の文字列として
組み立て、権限選択・引用・shell特殊変数・構文・書込み先で手戻りを起こすことである。

関連する観測は、主候補`HTC-C9F6C917`に加え、`HTC-477EA1A4`、`HTC-186E9B83`、`HTC-9DCE8503`、
`HTC-A5D1BCCA`である。これらを個別の修正一覧にせず、共通原因から扱う。

## 作成するPlan提案

次を新規作成する。

`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md`

状態は`awaiting_human_approval`とする。正式Plan、Decision、Task Contractではないことを冒頭で明記する。

提案は、少なくとも次を平易に記述する。

### 1. 解きたいことと解かないこと

- LLMは目的、対象範囲、意味的な説明を出す。
- 機械は、決定的なcommand spec、argv、作業directory、書込み対象、必要な権限種別、cache先、receiptを扱う。
- sandboxの承認を迂回・無効化しない。Git metadata書込みが必要なら、最初の実行前に必要な権限として
  宣言・要求するだけである。
- Codex host側の`functions.exec` JavaScript構文や、外部toolのAPI schemaをリポジトリのrunnerが
  制御できるとは主張しない。これらはhost側の入力境界であり、project内の解決対象と混同しない。

### 2. 共通原因と5観測の対応

各観測が、どの層の不足かを表にする。

- Git metadata書込み：operation typeとpermission requirementの事前判定不足
- Python cache：machine environmentの書込み先固定不足
- shell引用：argvを構造化せずshell文字列へ埋込んだこと
- shell特殊変数：shell文法・予約名への依存
- tool-call JavaScript構文：host操作の文字列組立てであり、project runnerの直接対象外

### 3. 候補となる最小設計

project内で実現できるものと、host側でしか実現できないものを分ける。

project内候補には、少なくとも以下を検討する。

- versioned operation spec（operation kind、argv配列、cwd、書込み分類、cache policy、receipt要求）
- shellを経由しない構造化argv executor
- Git metadata書込みを通常read-only操作から区別するpreflight
- task専用Python cache rootの決定的設定
- post-write／receipt検証

しかし、すべてを一度に実装する前提にしない。最小の縦切り候補を2〜3案比較し、推奨案と理由を示す。
推奨案は、人が承認するまで確定しない。

### 4. 受入条件と検証方針

高riskのため、正常・負例・境界例を具体化する。

- Git read-onlyとGit metadata書込みを誤分類しない
- 権限が必要な操作は最初の実行前に停止・要求し、sandboxを迂回しない
- 引用符、backtick、shell特殊変数を含む入力がshell解釈へ流れない
- cache rootがproject成果物や意図しない外部rootを汚さない
- 構造化specと実行receiptのidentityが一致する
- host側のtool構文をproject runnerで解決したと誤報しない

各受入条件について、必要なTest、fault injection、独立確認を提案する。実際のTestは作らない。

### 5. 依存・移行・停止条件

- 既存の直接shell／Git操作を、どの範囲から置換するか。
- 既存のGit sandbox承認、`.venv`、policy runnerとの整合。
- scope外のhost操作に達した場合の停止・報告。
- 既存の`ISSUE-HTC-66C3E6CA`（記録生成）との境界。重複実装を避ける。

### 6. Human判断が必要な点

少なくとも、最初の縦切り、project内runnerの責任範囲、host側操作の扱い、既存直接操作の移行順、
実装着手可否を明示する。

## 必須の確認

1. 対象Issue、主decision、関連4 decision、Development Policy、V4承認・閉鎖recordを読み、pathとSHA-256を提案へ固定する。
2. 提案を作った後、再読込してreferenced pathとDigestを検証する。
3. policy runnerで全Testを実行し、次へreceiptを作る。

```text
records/development/2026-08-05-machine-operation-routing-issue-plan-proposal-test-receipt-v1.json
```

4. TODOを現在位置だけに更新する。`ISSUE-HTC-C9F6C917`はregistered／nonblockingで、
   Plan提案がHuman承認待ちであることを示す。3 Issueのstateは変更しない。

## 禁止事項

- 正式Plan、Decision、Task Contract、code、test、config、policyを作成・変更しない。
- Git／shell／Python cacheの自動化を実装しない。
- 既存3 Issue、41 decision、候補bundle、V4承認・閉鎖recordを変更しない。
- push、PR、外部送信、hook、watcher、scheduler、background serviceを開始しない。

## コミットと完了報告

- Plan提案、TODO更新、test receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-design-machine-operation-routing-plan.md`

報告にはcommit SHA、提案path・Digest、提案した最小縦切り案、Human判断点、全Test結果、未実施事項を記す。
