# Codex → Claude：Work 5A Contract version 2 Review Run指示

## 1. Human承認と目的

HumanはContract version 2を承認した。承認Decisionは次である。

`records/development/2026-08-06-work5a-contract-v2-approval-decision-v1.md`

Claudeは、承認対象へ束縛した`contract_approval`をnew-onlyで作成し、Contract version 2のcompileから
Final Challengeまでを実行する。Human review acceptanceの直前で停止する。

## 2. 固定入力

作業前に次を全文読み、SHA-256を機械照合する。

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-approval-decision-v1.md` | `58063dbb46794a87a4d93f490706e93e366b68ffb029d4ea019f29d20f559c16` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | `aace8f35b79cbe4e3113433b55e903e86e0171f04738b180e1728eb83bd93ca6` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | `ad7b82ae74cec8655c205191feb4bf89801353eb8c7838f239f8b1c7da4c6658` |
| `records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json` | `626e38a76f456b6714dff5d167bcbbf4c75422559d442c40147064c4e5671468` |

開始基準commitは`44af24c959f0251e080db0c5ae3f575fb728b833`である。

## 3. 実施内容

初回Run bundleにある次のrecordを固定入力として使う。

- `requirement_binding`
- draft `review_task_contract` version 2
- `definition_challenge_material_set`
- `definition_challenge_verdict`（`passed`、blocking Finding 0件）

次の順序でpublic APIを実行する。

1. `build_contract_approval()`
   - `decision: approved`
   - `human_id: kenoogl`
   - `decided_at: 2026-08-06T06:20:15+09:00`
   - Contract v2とDefinition Challenge verdictのidentity、version、Digestへ束縛する。
2. `compile_contract()`。`compiled`とPlan bundleを確認する。
3. Source SnapshotとContext Manifestを新規作成する。
4. Workflow permitを取得し、deterministic stub reviewerを実行する。
5. Finding set、Conformance verdict、Final Challenge verdictを新規作成する。
6. 結果と全recordのidentity、version、Digestを保存する。

保存先：

- `records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json`
- `records/development/2026-08-06-work5a-contract-v2-review-run-evidence-v1.md`

## 4. 停止境界

Final Challengeの結果を保存した時点で停止する。

次は作成・実行しない。

- Review結果に対する`human_decision`
- `provenance_verdict`
- `accepted_artifact`
- Contract version 1または既存recordの変更、無効化、stale化

Findingに`error`がある、ConformanceまたはFinal Challengeが`failed`、固定入力不一致、Test不合格の場合も、
範囲を広げず停止して報告する。

## 5. 検証とcommit

- `tools/task_contract/`と既存Testは変更しない。実行時の不具合が見つかった場合は修正せず停止する。
- Definition Challenge 45件、既存Work 5A 38件、公式全Testを実行する。
- recordを再読込みし、content digest、上流参照、未実行stepを照合する。
- TODOは共通手順で「Review Run完了、Human review acceptance待ち」へ更新する。
- Run records、Evidence、機械生成済みTODOだけを一つの意味的commitにする。
- push、PR、CI、外部送信を行わない。

## 6. 完了報告

Git管理外の次へ保存して停止する。

`records/session-handoffs/2026-08-06-claude-to-codex-work5a-contract-v2-review-run.md`

commit SHA、`contract_approval`、compile、Finding、Conformance、Final Challenge、全Test、作成していない
`human_decision`／Provenance／accepted artifactを報告する。Codexの独立確認前に次へ進まない。
