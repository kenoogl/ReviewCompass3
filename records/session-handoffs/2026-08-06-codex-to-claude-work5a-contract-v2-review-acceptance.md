# Codex → Claude：Work 5A Contract version 2 Review結果受理指示

## 1. Human承認と目的

Humanは、Contract version 2のReview結果を受理した。承認Decisionは次である。

`records/development/2026-08-06-work5a-contract-v2-review-acceptance-decision-v1.md`

Claudeは、この承認を根拠に`human_decision`を作成し、循環のないProvenanceを検証して、成立する場合だけ
`accepted_artifact`を作成する。これは最小Review経路の実行結果の受理であり、review対象文書の内容の
完全性または一般的な品質保証を意味しない。

## 2. 固定入力

作業前に次を全文読み、SHA-256を機械照合する。

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-decision-v1.md` | `a1f09018348ca21997dc9103e3996317197f85d3b311bc266b6fc0a9ef0bfc8b` |
| `records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json` | `51f93bc14e47a3fe2e78eec8daa875930153ecb9d0c1031c12af800eeb723979` |
| `records/development/2026-08-06-work5a-contract-v2-review-run-evidence-v1.md` | `49d2df92e02c21491b0bf57c6bf31bd77b3beff1c41757863dcec9fa62af735b` |
| `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054` |

開始基準commitは`88a68ae6119c3c7d6bcd3d50814bca790ded9fa3`である。

Human decisionの固定値：

- decision：`approved`
- human_id：`kenoogl`
- decided_at：`2026-08-06T06:37:41+09:00`
- target digest：Context Manifestのcontent digest
  `149ae4a5f28d9ccd0378d31312b2b3965ed1d3aaa31599ed98b249f080348354`

## 3. 事前照合

Run bundleを再読込みし、次を機械照合する。

1. bundle内12 recordと、`compile_verdict.plan_bundle`のcontent digest。
2. Definition ChallengeからFinal Challengeまでの上流参照。
3. `finding_set`が0件、ConformanceとFinal Challengeが`passed`であること。
4. Definition Challenge、Contract approval、Conformance、Final Challengeのowner分離。
5. Source Snapshot内のtarget textとSHA-256が現在のtarget fileと一致すること。
6. `human_decision`、`provenance_verdict`、`accepted_artifact`がRun bundleに存在しないこと。

いずれかが不一致なら`stale`または該当する停止理由として扱い、三recordを作らず報告して停止する。

## 4. 実施内容

`tools.task_contract`の既存public APIだけを使用し、次の順序で実行する。

1. `record_human_decision()`
   - 上記固定値を使用する。
   - Finding set、Conformance verdict、Final Challenge verdictへ束縛する。
   - `target_digest`がContext Manifestのcontent digestと一致することを確認する。
2. `verify_provenance()`
   - Contract version 2の経路として、Definition Challenge verdictとContract approvalを含める。
   - Human decisionを終端とする11 node・10 edgeを検証する。
   - `provenance_verdict`自身をnodeまたはedge端点へ含めない。
   - `verified_nodes`、`verified_edges`、`closure`を持つ循環のない現行形式を使用する。
   - statusが`verified`であることを確認する。
3. `accept_artifact()`
   - Human decisionが`approved`、Provenanceが`verified`、target digestが一致する場合だけ実行する。

新しいContract identityの初回recordなので、三recordはいずれも`record_version: 1`とする。既存recordを
上書き、削除、無効化、stale化しない。

保存先：

- `records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json`
- `records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md`

Evidenceには「受理したのは最小Review経路の実行結果であり、対象文書の品質保証ではない」と明記する。

## 5. TODO、検証、commit

`docs/development/prompts/todo-handoff-update.md`を全文読み、その共通手順だけを使って
`TODO_NEXT_SESSION.md`を更新する。

- 現在位置は「Contract version 2のReview経路がaccepted artifactまで完了」。
- 次の一作業は「CodexがClaudeの受理recordを独立検証する」。
- Codexの独立検証前に後続Workを選択または開始しない。

保存後に次を実行する。

- 三recordのcontent digest再計算。
- Provenanceの11 node・10 edge、全node identity／version／Digest、自己参照なしの照合。
- accepted artifactからProvenanceとHuman decisionへの参照、target pathの照合。
- `tests/test_work5a_definition_challenge.py`と`tests/test_first_review_task_contract_e2e.py`。
- 公式venv runnerの全Test。
- TODO構造・参照Digest検査。
- `git diff --check`。

受理records、Evidence、機械生成済みTODOだけを一つの意味的commitにする。

## 6. 禁止事項と停止条件

- `tools/task_contract/`、`tests/`、review対象文書、Contract、Requirement、Current Plan、checklistを変更しない。
- 既存recordを削除、上書き、無効化、stale化しない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CIを使わない。
- Work 4B、Work 6A、後続評価E2以降を開始しない。
- 固定入力、target、上流参照、Digest、owner分離、Provenance、Testのいずれかが不成立なら、
  accepted artifactを作らず、理由とEvidenceを報告して停止する。

## 7. 完了報告

Git管理外の次へ保存して停止する。

`records/session-handoffs/2026-08-06-claude-to-codex-work5a-contract-v2-review-acceptance.md`

commit SHA、固定入力照合、三recordのID／version／Digest、Provenanceのnode／edge数、accepted artifactの有無、
対象Testと全Test、変更していない範囲を報告する。Codexの独立確認前に次へ進まない。
