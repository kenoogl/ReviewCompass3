# Codex → Claude：正本・履歴・検証手順9候補のHuman triage記録指示

## 誰が何をするか

- **Human**は、次の9候補を、現行の正本規則、旧版の履歴保持規則、または検証・報告手順の説明と判断した。
  新しい障害や独立した正式Issueにはしないことを承認した。
- **Codex**は、承認内容をV4 Human triage decisionとして保存するよう指示する。
- **Claude**は、9件のdecision record、test receipt、TODO更新だけを作成してcommitする。

## 対象候補とHuman判断

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

### 現行の正本と履歴保持（7件）

| candidate ID | Human判断 |
| --- | --- |
| `HTC-C05BE65C` | digest-onlyの改定履歴は保持し、現行固定入力とWork 1A EvidenceはGitから再構築する。 |
| `HTC-C3193ABF` | Intent／用語集候補はpromotion前snapshotであり、外部Approval Decisionと承認対象Digestを第二正本化しない。 |
| `HTC-ECE89CA2` | session `001`と旧candidate Digestは問題発生Evidenceとして保持し、current判断関門には使わない。 |
| `HTC-49795CC0` | coverage matrixの現行authorityは外部Approval Decisionであり、候補fileを第二正本にしない。 |
| `HTC-094589CA` | identity／stale規則とRequirements配置規則の現行authorityは外部Decisionと承認対象Digestである。CI adapter、Build Artifact実装、provider操作は引き続き対象外である。 |
| `HTC-876989C2` | 現行effective authority chainは50 definitionであり、legacy bindingとauthority v1はsuperseded履歴として保持する。 |
| `HTC-ABE70CFC` | 旧37 Requirementは移行済みで、現行effective authority v2は50 definition、legacy binding 0件である。旧版は削除・上書きしない。 |

### 検証と報告の現行手順（2件）

| candidate ID | Human判断 |
| --- | --- |
| `HTC-7071DD99` | 公式Testはpolicy runnerが起動し、receiptを機械生成する。`.venv/bin/python3 -m pytest -q`はrunner内部の実行commandである。 |
| `HTC-62719E1C` | 作業後報告には手戻りと手作業の因果、期待／実executor、Evidence、機械処理候補、routeを含める。決定的処理をLLMが行った場合は、手戻りがなくても改善候補として扱う。 |

上記9件すべてに、次のschema version 2 V4 Human triage decisionを作成する。

- `unresolved: false`
- `recurrence: false`
- `impact: not_applicable`
- `priority: not_applicable`
- `promote_to_issue: false`
- `disposition: reject`
- `blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

`rationale`には、`reject`は正本規則・履歴・検証手順を捨てる意味ではなく、
この候補を独立したIssueとして追跡しない意味であることを平易に記す。
各candidateの元のPlan、Decision、Evidence、code、test、configを変更しない。

## 実施範囲

1. V4 decision directoryに、9candidateのschema version 2 decision recordを各一件作る。
2. 各record、decision集合、V4 Issue集合をV4 validatorで検証する。
3. 候補bundleのSHA-256が`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま、
   `human_fields`が全件`null`のままであることを確認する。
4. `.venv/bin/python3 -m pytest -q`を実行し、test receiptを
   `records/development/2026-08-05-triage-authority-history-and-procedure-test-receipt-v1.json`へ作る。
5. TODOを現在位置だけに更新する。判断済み41件、残り0件、正式Issue 3件、active Issue 0件とする。
   Human triageは完了したと書き、次の一作業を「3正式IssueのPlan化順序、またはIssue Intake V4 Pilotを
   閉じるかのHuman判断」とする。3 Issueはregistered／nonblockingのままと書く。

## 禁止事項

- IssueのPlan化、Issue Intake V4 Pilotの閉鎖、実装、既存文書の一括書換えをしない。
- 既存32 decision、既存3 Issue、候補bundle、Plan、Decision、Evidence、code、test、configを変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- 9 decision record、TODO更新、作成後のtest receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-authority-history-and-procedure.md`

報告にはcommit SHA、9 decision ID、候補bundle不変確認、V4 Issue数、active Issue数、全test結果、未実施事項を記す。
