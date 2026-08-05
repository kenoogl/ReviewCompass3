---
candidate_id: IC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001
observed_at: 2026-08-05
origin_stage: initial-development
origin_work: Work 5A Definition Challenge TDD preflight
origin_commit: 01f2fcf5a09302cb57de700d2b374cddd11f5105
candidate_kind: improvement_candidate
classification: Task Contract不良
priority: P0
status: awaiting_human_triage
blocking: true
suggested_route: upstream_revision
related_requirement: REQ-CONTRACT-004
confidentiality_class: project-internal
---

# Human Contract approvalをcompile前に検証する機械gateが未定義である

## 1. 発生元と固定source

| identity | path | SHA-256 |
| --- | --- | --- |
| 承認Decision | `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d` |
| 承認済み設計 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| 現在のcompile実装 | `tools/task_contract/contract.py` | `be7ec9d314492c529ae0fa962458e35777d400586f8ca461dd5ccbe2c88c74cd` |
| Requirement | `records/requirements/definitions/req-contract-004--v1.json` | `5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf` |
| Development Policy | `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |

## 2. 観測した事象

承認済み設計の正常経路は次の順序を要求する。

```text
draft Contract v2 → Definition Challenge verdict → Human Contract approval
→ compile / Plan bundle
```

しかし、設計とDecisionは次を定義していない。

- Human Contract approvalのrecord kind、identity、version、必須field、content digest。
- approvalがdraft Contract v2とDefinition Challenge verdictの両方へ束縛される方法。
- `compile_contract`がapprovalの実在、Digest、decision、owner、対象Contract versionを検証する方法。
- approval欠落、拒否、改竄、別Contractへの差し替えに対するstop code。

現行の`compile_contract`の入力はContractとRequirement bindingだけである。設計どおりに
Definition Challenge verdictを追加しても、Human Contract approvalを検証する入力と規則が無い。

## 3. 原因

設計訂正は、compile後の`plan_bundle`をDefinition Challenge入力にする循環を解消したが、
新しく挿入したHuman Contract approvalを、耐久recordと機械gateに接続していない。
順序を文章で追加した一方、その順序を強制する入出力境界が欠落した。

## 4. 影響と停止判定

- Challengeが`passed`であるだけでcompileへ進めるなら、Human Contract approvalは宣言だけになる。
- 拒否されたContract、別versionへのapproval、改竄されたapprovalをfail-closedで拒否できない。
- `REQ-CONTRACT-004`のHuman gate、Acceptanceの真偽、必須Provenanceに影響する。

Development Policyの`pause_and_triage`条件のうち、許可の妥当性、Acceptanceの真偽、必須Provenance、
開始permitに影響する。そのため現行Workを停止し、Testと実装は作成しない。

## 5. route提案

`upstream_revision`を提案する。Humanが採用した場合だけ、承認済み設計を新versionへ改定する。
最小訂正案は次である。

1. `contract_approval`recordはContract v2 ref、Definition Challenge verdict ref、Human identity、
   `approved | rejected`、decided at、content digestを持つ。
2. `compile_contract`はContract v2に対し、`passed`なDefinition Challenge verdictと`approved`な
   `contract_approval`の両方を必須入力とする。
3. Contract ref、Challenge ref、Digest、owner、decisionの欠落または不一致で`not_compilable`とし、
   Plan bundleを作らない。
4. `contract_approval`をProvenanceのDefinition Challengeとcompile verdictの間に追加する。

この訂正はHuman gateとProvenanceの意味を変えるため、Humanの明示判断なしに設計、Decision、
Task Contract、Testを書き換えない。

## 6. consumerとOutcome

- consumer候補：Work 5A Definition Challenge設計とTDD。
- Outcome候補：Human承認済みの版付きUpstream Revision、RED Test、GREEN Evidence。
- 現在のOutcome：未作成。本候補はopenである。

## 7. この候補が許可しないこと

- 現行の承認済み設計、Decision、Task Contract、Test、Requirementの自動変更。
- Human Contract approvalを会話文またはTODOの記載だけで代用すること。
- approval欠落または不一致をwarningとして通過させること。
- Contract version 1と既存accepted artifactの上書き、無効化、stale化。
- Work 6A、汎用Challenge framework、LLM、外部送信、push、PR、CI。
