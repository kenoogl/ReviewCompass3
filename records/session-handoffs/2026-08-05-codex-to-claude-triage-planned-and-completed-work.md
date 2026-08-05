# Codex → Claude：完了済み2件と計画どおり保留4件のHuman triage記録指示

## 誰が何をするか

- **Human**は、次の6候補を新たな障害ではなく、既に完了した作業または現行Plan／既存Issueにより
  意図的に保留されている作業と判断した。新しい正式Issueを作らないことを承認した。
- **Codex**は、承認内容をV4 Human triage decisionとして保存するよう指示する。
- **Claude**は、6件のdecision record、test receipt、TODO更新だけを作成してcommitする。

## 対象候補とHuman判断

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

### 解決済み（2件）

| candidate ID | Human判断 |
| --- | --- |
| `HTC-1D5B5102` | WI-006、実snapshot／manifest、TODO compaction、Resolution Verdictは完了済みである。 |
| `HTC-BE5E1F67` | Work 4のDesign差分、代表scenario、最初のvertical sliceの選定は完了し、Work 5Aへ進んでいる。 |

この2件は`historical_completed`とする。

- `unresolved: false`、`recurrence: false`
- `impact: not_applicable`、`priority: not_applicable`
- `promote_to_issue: false`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`、`supersedes: null`

### 現行Planにより保留（3件）

| candidate ID | Human判断 |
| --- | --- |
| `HTC-328144E4` | Deployment Manifest、package builder、原子的切替、rollbackはWork 7の計画済み作業である。 |
| `HTC-45B611EF` | durable Project BindingはWork 7の計画済み作業である。 |
| `HTC-D7E1F8C3` | 実施報告照合の自動Claim抽出、Provenance、完了state結線は、現在は手作業を維持し将来の製品工程へ先送りしている。 |

この3件は`defer`とする。

- `unresolved: true`、`recurrence: false`
- `impact: medium`、`priority: low`
- `promote_to_issue: false`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`、`supersedes: null`

`rationale`には、未実施であることは忘却・障害ではなく、現行Planが意図的に先送りしている範囲であることを記す。

### 既存Issueに依存して保留（1件）

| candidate ID | Human判断 |
| --- | --- |
| `HTC-243BE1FF` | session hook、Desktop監視、Claude hook、scheduler、background serviceの有効化は、会話記録の保存方針が決まるまで開始しない。`ISSUE-HTC-BEB5E0BD`に依存する。 |

この1件は`dependency`とする。

- `unresolved: true`、`recurrence: true`
- `impact: high`、`priority: low`
- `promote_to_issue: false`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`、`supersedes: null`

`rationale`と`next_action`には、`ISSUE-HTC-BEB5E0BD`の方針決定前にhook、watcher、scheduler、
background serviceを有効化しないことを明記する。

候補bundle自体、特に`human_fields`は変更しない。各candidateの元のPlan、Decision、Evidence、code、testも変更しない。

## 実施範囲

1. V4 decision directoryに、6candidateのschema version 2 decision recordを各一件作る。
2. 各record、decision集合、V4 Issue集合をV4 validatorで検証する。
3. 候補bundleのSHA-256が`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま、
   `human_fields`が全件`null`のままであることを確認する。
4. `.venv/bin/python3 -m pytest -q`を実行し、test receiptを
   `records/development/2026-08-05-triage-planned-and-completed-work-test-receipt-v1.json`へ作る。
5. TODOを現在位置だけに更新する。判断済み32件、残り9件、正式Issue 3件、active Issue 0件とし、
   次の一作業を残り9候補のHuman triageとする。3 Issueはregistered／nonblockingのままと書く。

## 禁止事項

- Work 7、hook、watcher、scheduler、background service、自動Claim抽出、Project Bindingを実装または有効化しない。
- 正式Issue、Plan、Workを作らない。
- 残る9候補、既存26 decision、既存3 Issue、候補bundle、Plan、Decision、Evidence、code、test、configを変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- 6 decision record、TODO更新、作成後のtest receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-planned-and-completed-work.md`

報告にはcommit SHA、6 decision ID、候補bundle不変確認、V4 Issue数、active Issue数、全test結果、未実施事項を記す。
