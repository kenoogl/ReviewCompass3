# Codex → Claude：authority境界4候補のHuman triage記録指示

## 誰が何をするか

- **Human**は、次の4候補を「独立して解決する問題ではなく、承認範囲を誤らないための方針上の境界」と判断し、
  正式Issueにしないことを承認した。
- **Codex**は、承認内容をV4 Human triage decisionとして保存するよう指示する。
- **Claude**は、4件のdecision recordと必要なTODO更新だけを作成する。

## 対象候補とHuman判断

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

| candidate ID | Human判断 |
| --- | --- |
| `HTC-8AEF6A5F` | Layout validatorは初期規則を測る定規であり、製品Runtimeではない。この区別は現在も守られている。 |
| `HTC-152E0FB3` | Planやbaseline確認は正式承認の代わりではない。承認はDecisionと承認対象Digestで行う。 |
| `HTC-7DDF463E` | 数値閾値、Architecture Policy、shared／distributed環境は未承認であり、根拠なしに実装しない。 |
| `HTC-B53A2670` | 先送りした13機能は初期releaseのnonblockingであり、別Task ContractとHuman判断まで実装しない。 |

4件すべてを、次のV4 Human triage decisionとして作成する。

- `unresolved: false`
- `recurrence: false`
- `impact: not_applicable`
- `priority: not_applicable`
- `promote_to_issue: false`
- `disposition: reject`
- `blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

`rationale`には、「reject」は方針・Evidenceを捨てる意味ではなく、**この候補を独立したIssueとして
追跡しない**意味であることを平易に記す。各candidateの元のPlan／Decision／Evidenceは変更しない。

## 実施範囲

1. V4 decision directoryに、4candidateのschema version 2 decision recordを各一件作る。
2. 各recordのbundle path／SHA-256、candidate ID／content digest、decision path／content digestを
   V4 validatorで検証する。
3. V4 decision集合に競合が無いことを検証する。
4. 候補bundleが不変であること、V4 Issueが`ISSUE-HTC-BEB5E0BD`の一件だけであること、全testが
   通ることを確認する。
5. TODOを現在位置に更新する。詳細を再累積せず、判断済み候補数を12件、残りを29件として記す。
   次の一作業は残り29候補のHuman triageとする。`ISSUE-HTC-BEB5E0BD`はregistered／nonblockingのままとする。

## 禁止事項

- 4候補を正式Issue、Plan、Workへ昇格しない。
- 残る29候補、既存8 decision、既存V4 Issue、候補bundle、Plan、Decision、Evidence、code、test、configを
  変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- decision record、TODO更新、作成後のtest receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-authority-boundary-candidates.md`

報告にはcommit SHA、4 decision ID、候補bundle不変確認、V4 Issue数、全test結果、未実施事項を記す。
