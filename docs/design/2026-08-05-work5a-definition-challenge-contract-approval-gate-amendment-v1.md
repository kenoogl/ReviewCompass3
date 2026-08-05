# Work 5A Definition Challenge Human Contract approval gate Amendment v1

状態：`approved`
対象設計：`docs/design/2026-08-05-work5a-definition-challenge-proposal.md`
対象候補：`IC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`
承認Decision：`DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`

## 1. 目的

承認済みDefinition Challenge設計は、次の順序を要求する。

```text
draft Contract v2 → Definition Challenge verdict → Human Contract approval
→ compile / Plan bundle
```

本Amendmentは、Human Contract approvalを耐久recordとcompile事前gateに接続し、
会話文またはTODOの宣言だけでcompileへ進む経路を拒否する。

## 2. `contract_approval` record

`contract_approval`recordは次の必須fieldを持つ。

```json
{
  "record_kind": "contract_approval",
  "record_id": "CA-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2",
  "record_version": 1,
  "owner": "contract_approval_owner",
  "decision_class": "contract_definition_approval",
  "decision": "approved",
  "human_id": "<non-empty human identity>",
  "decided_at": "<timestamp>",
  "contract_ref": { "...": "draft Contract v2 record_ref" },
  "definition_challenge_ref": { "...": "passed verdict record_ref" },
  "content_digest": "..."
}
```

- `decision`は`approved | rejected`の二値である。
- `owner`は`contract_approval_owner`に固定する。Definition Challenge ownerと、成果受理時の
  `human_decision_owner`のどちらとも別の論理ownerである。同じHuman個人が実施することは禁止しない。
- `contract_ref`はChallenge対象のdraft Contract v2とidentity、version、Digestが完全一致する。
- `definition_challenge_ref`は実際の`passed` verdictとidentity、version、Digestが完全一致する。
- recordはnew-onlyで保存し、decision変更は既存recordの上書きではなく新versionと関係で行う。

## 3. compile事前gate

Contract version 1の既存compile経路は履歴再読込みのため維持する。Contract version 2以降では
`compile_contract`に次の二recordを必須入力とする。

1. `definition_challenge_verdict`：`status == passed`
2. `contract_approval`：`decision == approved`

gateはPlan bundleを生成する前に、次をすべて検証する。

- 両recordの必須fieldとcontent digest。
- ChallengeのContract refとcompile対象Contractの完全一致。
- ApprovalのContract refとcompile対象Contractの完全一致。
- ApprovalのChallenge refと入力Challenge verdictの完全一致。
- Definition Challenge owner、Contract approval owner、後続のHuman review acceptance ownerの論理分離。

一件でも満たさない場合、`compile_verdict.status`を`not_compilable`とし、
`plan_bundle`を含めない。理由は次の閉じた語彙とする。

| reason | 条件 |
| --- | --- |
| `definition_challenge_missing` | Challenge verdict欠落 |
| `definition_challenge_failed` | Challenge verdictが`passed`でない |
| `definition_challenge_invalid` | ChallengeのDigest改竄、schema不正、Contract ref不一致 |
| `contract_approval_missing` | Approval欠落 |
| `contract_approval_rejected` | Approvalが`approved`でない |
| `contract_approval_invalid` | ApprovalのDigest改竄、schema不正、Contract／Challenge ref不一致 |

## 4. Provenance

Contract version 2のProvenanceは`contract_approval`をDefinition Challengeとcompileの間に持つ。

```text
requirement_binding → review_task_contract → definition_challenge_verdict
→ contract_approval → compile_verdict → context_manifest → workflow_permit
→ finding_set → conformance_verdict → final_challenge_verdict → human_decision
```

- Contract version 2は11 node、10 edgeとし、自己辺を持たない。
- `contract_approval`欠落、重複、identity不一致、Digest不一致のProvenanceは拒否する。
- Contract version 1の既存9 node、8 edge recordは読取り可能な履歴として維持し、
  version 2の拒否fixtureに使わない。

## 5. TDD追加受入条件

元設計のG1〜G4、H1〜H11に次を追加する。

### 正常例

- G5：`passed` Challengeとそれへ束縛した`approved` Contract approvalがある場合だけ、
  Contract version 2のcompileが`compiled`を返す。
- G6：Contract approvalはContract v2とChallenge verdictのidentity、version、Digestを保持する。
- G7：Contract version 2のProvenanceが11 node、10 edgeで、`contract_approval`が正しい位置にある。
- G8：Contract version 1の既存compileと9 node Provenanceはそのまま有効である。

### 負例

- H12：Contract approval欠落 → `contract_approval_missing`。
- H13：Contract approval拒否 → `contract_approval_rejected`。
- H14：Contract approvalのcontent digest改竄 → `contract_approval_invalid`。
- H15：別Contractまたは別ChallengeへのApproval差し替え → `contract_approval_invalid`。
- H16：Contract approvalを欠くversion 2 Provenance → `provenance_node_missing`。
- H17：`rejected`または改竄Approvalからaccepted artifactへ到達できない。

## 6. 固定入力

| 種別 | path | SHA-256 |
| --- | --- | --- |
| blocking候補 | `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md` | `96ee100a0633be4525e59f27d090e6460657e26352416e88d0261172845ff18d` |
| 元の承認Decision | `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d` |
| 元の承認済み設計 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| Requirement | `records/requirements/definitions/req-contract-004--v1.json` | `5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Development Policy | `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |

## 7. 実施境界

- 本Amendmentのcommitとclean transition後にだけRED Testへ進む。
- 既存Testを弱めず、Contract version 1の履歴互換性を保持する。
- 初回Definition Challenge実Runが`passed`でも、新しい`contract_approval`がHumanにより作成されるまで
  compile、Review Run、accepted artifact作成へ進まない。
