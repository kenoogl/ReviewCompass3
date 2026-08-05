# Codex → Claude：機械操作の根本原因Issue登録指示

## 誰が何をするか

- **Human**は、候補5件を別々に修正せず、LLMが機械操作の実行手順をその場で文字列として組み立てることを
  共通原因と判断した。この共通原因を、nonblockingの正式Issueとして1件登録することを承認した。
- **Codex**は、この承認をV4 Human triage decisionとV4 Issueに保存するよう指示する。
- **Claude**は、以下のdecision record、正式Issue、test receipt、TODO更新だけを作成してcommitする。

LLMは「何を確認・変更するか」の意味的な判断を行ってよい。しかし、コマンドの引用、shell変数、
ツール呼出構文、権限経路、Python cache書込み先のような決定的な実行手順を、都度手書きしてはならない。
その実行手順は機械側の定型処理が扱う、というHuman方針である。

## 対象候補

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

| candidate ID | content digest | Human判断 |
| --- | --- | --- |
| `HTC-C9F6C917` | `380fb83e6bf42b5e7e6a82ae14d3fb6026342eec3bddf9d71d1da0fed9ea8fe0` | 主候補。正式Issueへ昇格する。 |
| `HTC-477EA1A4` | `331ae2c6bdc46b3d7e50de65c7efa273a5818dbace62006921ab8eb8c058246a` | 同じ根本原因Issueで扱う。個別Issueにはしない。 |
| `HTC-186E9B83` | `2aa672216ac89be2b6fcfded754d837cd04146b8ee0bbe5296e5a37ab69f5de2` | 同じ根本原因Issueで扱う。個別Issueにはしない。 |
| `HTC-9DCE8503` | `11a630f39c3855fd458f35c3b136f2dd518e505c488c34212ce85f03b3e04f09` | 同じ根本原因Issueで扱う。個別Issueにはしない。 |
| `HTC-A5D1BCCA` | `27e0319409fa360dcfc1be6291e29cd3fd5fc5a0d34df206ac299035cdad7532` | 同じ根本原因Issueで扱う。個別Issueにはしない。 |

候補bundleのpath、SHA-256、schema version（1）は既存V4 decisionと同じ値を使う。
候補bundle自体、特に`human_fields`は変更しない。

## 作成するV4 Human triage decision

`HTC-C9F6C917`には次を作る。

- `decision_id: DEC-HTC-C9F6C917`
- `unresolved: true`、`recurrence: true`、`impact: high`、`priority: high`、`promote_to_issue: true`
- `disposition: issue_resolution`、`blocking: false`
- `issue_promotion: {"approved": true, "issue_id": "ISSUE-HTC-C9F6C917"}`
- `supersedes: null`

残る4候補には、それぞれ次を作る。

- `decision_id: DEC-<candidate ID>`
- `unresolved: true`、`recurrence: true`、`impact: high`、`priority: high`、`promote_to_issue: false`
- `disposition: defer`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

5件の`rationale`には、単発の操作ミスとして処置するのではなく、
`ISSUE-HTC-C9F6C917`で共通原因を扱うことを平易に記す。`defer`は問題を放置する意味ではなく、
同じ根本原因を別Issueに重複登録しない意味であることを明記する。

## 作成する正式Issue

V4 API `build_v4_issue_record`を使い、主候補の承認済みdecisionから次を作る。

- path：`.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`
- `issue_id: ISSUE-HTC-C9F6C917`
- `state: registered`。`in_progress`にしない。
- `problem`：

  `LLMがGit書込み、shell実行、ツール呼出、Python cacheの決定的な実行手順を都度文字列として組み立てている。そのため権限選択、引用、shell特殊変数、構文、書込み先で手戻りが再発する。`

Issueの`problem`または主decisionの`rationale`で、残る4候補を同じ根本原因の観測として明記する。
このIssueはsandboxの承認そのものを迂回・無効化するためのものではない。
必要な権限を最初の実行前に決め、定型手順として実行するための追跡である。

## 実施範囲

1. 上記5件のschema version 2 V4 Human triage decisionを作る。
2. 主decisionからV4 Issueを作る。既存`ISSUE-HTC-BEB5E0BD`は変更しない。
3. 各record、decision集合、V4 Issue集合、候補bundleの不変性をV4 validatorで確認する。
4. 全testを公式runner `.venv/bin/python3 -m pytest`で実行する。
5. test receiptを`records/development/2026-08-05-triage-machine-operation-root-issue-test-receipt-v1.json`に作る。
6. TODOを現在位置だけに更新する。判断済みは17件、残りは24件、正式Issueは2件、active Issueは0件とする。
   次の一作業は残り24候補のHuman triageとし、両Issueはregistered／nonblockingのままと書く。

## 禁止事項

- IssueのPlan化、実装、runner・config・policy・testの変更をしない。
- Git／shell／Python cacheの自動化を実装しない。
- 既存12 decision、既存Issue、候補bundle、Plan、Decision、Evidence、code、test、configを変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- 5 decision record、正式Issue、TODO更新、test receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-machine-operation-root-issue.md`

報告にはcommit SHA、5 decision ID、正式Issue ID、候補bundle不変確認、V4 Issue数、active Issue数、
全test結果、未実施事項を記す。
