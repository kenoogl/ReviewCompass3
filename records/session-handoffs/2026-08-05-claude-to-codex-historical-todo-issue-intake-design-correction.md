# Claude → Codex：Issue Intake V4 設計訂正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-historical-todo-issue-intake-design-correction.md`

## 1. commit SHA

`a1f53d8c7b8c9555bed69483f88238afb39e8902`（Correct issue intake v4 to unlimited registration）

設計提案一件だけのcommitである。config、schema、validator、code、test、既存Issue、TODO、Plan、
checklist、Decision recordを変更していない。既存commit `472c7ad`も変更していない。

| file | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `325f15838bc416a4321429b5e7ff4b47b5370890586bd548587c4456909e063d` |

状態は`awaiting_human_approval`のままである。

## 2. 登録上限の撤廃

`maximum_registered_issues`をV4設計から除いた。上限を置くのは同時に手を動かす数だけである。

| 設定 | 値 |
| --- | --- |
| 登録済みIssue数 | **上限なし** |
| `maximum_active_issues` | 1 |
| `maximum_active_leaves` | 1 |

登録数超過の拒否規則と旧受入条件J9を削除した。V4のconfigは
`maximum_issue_subjects`も`maximum_registered_issues`も持たない。

TODOは`in_progress`の入口だけを表示する。登録件数の表示は必須にせず、書く場合も一行に留める。

## 3. 変更した状態遷移

### 3.1 状態と作業中上限への算入

| 状態 | 算入 |
| --- | --- |
| `registered`／`untriaged` | 算入しない |
| `deferred` | 算入しない |
| `in_progress` | **算入する。常に最大1件** |
| `suspended` | 算入しない |
| `resolved`／`rejected` | 算入しない |

既存語彙との対応表を提案§1.4へ追加した。既存`issue_record`は`state`を持たず、進行は
`resolution_verdict.outcome`で表していた。`state`はV4で新設し、`issue_record`の
`schema_version` 2を必要とする。**名称だけを既存recordへ遡及適用しない。**
既存`ISSUE-PILOT-TODO-GROWTH-001`は version 1のまま保持する。

### 3.2 中断規則

1. 新しい問題は、`in_progress`があっても登録できる。登録に上限は無い。
2. 阻害要因でない限り、現行Issueを中断しない。新規Issueは`registered`のまま置く。
3. 阻害要因のときだけ、現行を`suspended`へ移し、新規を唯一の`in_progress`にできる。
4. **登録だけで現行Issueを自動中断してはならない。**中断は`blocks`関係とHumanの裁定を伴う。
5. 再開には、阻害Issueが`resolved`であること、またはHumanの明示的な再開裁定を必須とする。
   機械は自動再開しない。

## 4. 循環検出時の停止とHuman判断境界

`blocks`を有向関係として定義した。`A blocks B`は「Bを進めるにはAの解決が必要」を意味する。

| 事象 | 機械の動作 | Humanの判断 |
| --- | --- | --- |
| 関係追加 | 有向循環を毎回検出する | — |
| 自己循環（`A blocks A`） | 拒否する | — |
| 循環検出（`A → B → A`ほか） | 循環に含まれるIssueをすべて`suspended`にし、**作業中Issueを0件にする**。相互再開の往復をしない | — |
| 根本原因 | `root_cause_escalation_candidate`を作ってよい | **昇格、優先順位、統合、再開はHumanだけが決める** |
| 再開 | 根本原因Issueの`resolved`またはHuman裁定が無ければ拒否する | 再開裁定 |

循環は個別修正を増やす合図ではなく、依存関係・設計・方針を根本から見直す信号である旨を
提案§1.6へ平易に記した。

## 5. 受入条件の改訂

正常例をI1〜I9、負例をJ1〜J14へ改訂した。追加した主なものは次である。

| # | 内容 |
| --- | --- |
| I3 | 登録済みIssueが何件あっても登録が成功する。上限判定を行わない |
| I5 | 非阻害の新規Issue登録では現行の`in_progress`が中断されない |
| I6 | 阻害切替で旧Issueが`suspended`、新Issueだけが`in_progress`になる |
| I7 | `resolved`またはHuman裁定の後だけ`suspended`を再開できる |
| I9 | 既存記録が旧versionの規則で通り、V4のstateを書き込まない |
| J7 | 二件目の`in_progress`開始を拒否する |
| J9 | 登録だけで現行Issueを`suspended`にしようとすると拒否する |
| J10 | 自己循環を拒否する |
| J11 | 二Issue以上の`blocks`循環を拒否し、作業中Issueを0件にする |
| J12 | Human裁定なしのroot cause候補のIssue化を拒否する |
| J13 | 根本原因の`resolved`またはHuman裁定なしの再開を拒否する |

実施計画は「設計承認 → RED → 実装 → GREEN → 候補提示 → Human triage」の順序を保った。
循環検出時の根本原因Issue承認を段階9として追加し、Human承認が必要な箇所として明示した。

Human判断事項から登録上限を外し、残るのは候補IDの体系と、`issue_record`の`schema_version` 2化の
二点である（§0の失敗解消方針を含めて三点）。

## 6. 未実施事項

- config、schema、validator、code、test、既存Issue、TODO、Plan、checklist、Decision record：
  **変更していない**。
- 過去TODOからの候補・Issueの新規作成：**行っていない**。
- 失敗中のtestの局所修正：**行っていない**。§0の失敗はV4導入で解消する順序のままである。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。

検証は、訂正18項目の反映確認（登録上限の撤廃、旧J9の除去、状態5種、算入対象、既存語彙対応、
遡及適用の禁止、中断5規則、`blocks`定義、自己循環拒否、作業中0件、Human限定、平易な説明、
TODO表示の任意化、新受入条件、実施計画の段階追加）と`git diff --check`を実施し、いずれも合格した。

Human承認まで実装へ進まない。
