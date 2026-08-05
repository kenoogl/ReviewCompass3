# Codex → Claude：記録生成の根本原因Issue登録指示

## 誰が何をするか

- **Human**は、次の4候補を「文書の内容」ではなく、Evidence・TODO等の定型欄を正しい入力から
  正しい位置・時点・内訳で生成する処理が未機械化である共通問題と判断した。
  `HTC-66C3E6CA`を主候補とするnonblocking正式Issue 1件の登録を承諾した。
- **Codex**は、承諾内容をV4 Human triage decisionとV4 Issueへ保存するよう指示する。
- **Claude**は、以下のdecision record、正式Issue、test receipt、TODO更新だけを作成してcommitする。

LLMは説明文の作成を行ってよい。しかし、固定receiptからの数値転記、構造見出しの位置特定、
必須検証終了後の時刻確定、機械監査結果のcohort別集計は、定型的な機械処理として扱う。

## 対象候補とHuman判断

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

| candidate ID | Human判断 |
| --- | --- |
| `HTC-66C3E6CA` | 主候補。receiptの全Test時間をTODOへ手入力して差が出た。正式Issueへ昇格する。 |
| `HTC-C2E642ED` | 同じIssueで扱う。構造見出しidentityから挿入位置を機械解決する必要がある。個別Issueにはしない。 |
| `HTC-D34A113E` | 同じIssueで扱う。必須verification完了後にCompletion Evidenceの時刻を機械確定する必要がある。個別Issueにはしない。 |
| `HTC-D65B4A8E` | 同じIssueで扱う。正しい監査結果をcohort別の内訳で機械表示する必要がある。個別Issueにはしない。 |

候補bundleのpath、SHA-256、schema version（1）は既存V4 decisionと同じ値を使う。
候補bundle自体、特に`human_fields`は変更しない。

## 作成するV4 Human triage decision

`HTC-66C3E6CA`には次を作る。

- `decision_id: DEC-HTC-66C3E6CA`
- `unresolved: true`、`recurrence: true`、`impact: high`、`priority: high`、`promote_to_issue: true`
- `disposition: issue_resolution`、`blocking: false`
- `issue_promotion: {"approved": true, "issue_id": "ISSUE-HTC-66C3E6CA"}`
- `supersedes: null`

残る3候補には、それぞれ次を作る。

- `decision_id: DEC-<candidate ID>`
- `unresolved: true`、`recurrence: true`、`impact: high`、`priority: high`、`promote_to_issue: false`
- `disposition: defer`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

4件の`rationale`には、単発の文書訂正として個別に処置するのではなく、
`ISSUE-HTC-66C3E6CA`で共通原因を扱うことを平易に記す。`defer`は問題を放置する意味ではなく、
同じ根本原因を別Issueに重複登録しない意味であることを明記する。

## 作成する正式Issue

V4 API `build_v4_issue_record`を使い、主候補の承認済みdecisionから次を作る。

- path：`.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json`
- `issue_id: ISSUE-HTC-66C3E6CA`
- `state: registered`。`in_progress`にしない。
- `problem`：

  `LLMがEvidence・TODO等の定型欄を手入力または都度の位置推測で作成している。そのため固定receiptとの転記差、見出し位置の不一致、検証完了前の時刻確定、監査内訳の分かりにくさが発生する。`

Issueの`problem`または主decisionの`rationale`で、残る3候補を同じ根本原因の観測として明記する。
今回のIssue登録は、既存文書の一括書換え、既存receiptの改竄、またはLLMによる説明文作成の禁止を意味しない。
定型値と構造操作を機械側へ移すための追跡である。

## 実施範囲

1. 上記4件のschema version 2 V4 Human triage decisionを作る。
2. 主decisionからV4 Issueを作る。既存2 Issueは変更しない。
3. 各record、decision集合、V4 Issue集合、候補bundleの不変性をV4 validatorで確認する。
4. 全testを公式runner `.venv/bin/python3 -m pytest -q`で実行する。
5. test receiptを`records/development/2026-08-05-triage-record-generation-root-issue-test-receipt-v1.json`に作る。
6. TODOを現在位置だけに更新する。判断済み26件、残り15件、正式Issueは3件、active Issueは0件とする。
   次の一作業は残り15候補のHuman triageとし、3 Issueはregistered／nonblockingのままと書く。

## 禁止事項

- IssueのPlan化、実装、文書一括書換え、runner・config・policy・testの変更をしない。
- 既存22 decision、既存2 Issue、候補bundle、Plan、Decision、Evidence、code、test、configを変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- 4 decision record、正式Issue、TODO更新、test receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-record-generation-root-issue.md`

報告にはcommit SHA、4 decision ID、正式Issue ID、候補bundle不変確認、V4 Issue数、active Issue数、
全test結果、未実施事項を記す。
