# Work 5A Current Work Projection後続route提案

状態：`human_decision_candidate`

## 1. 結論

Work 5Aの`bootstrap Current Work Projectionを正式recordへ写像する`項目は、現時点で部分実装せず、
必要な正式recordが揃うまで`deferred`に維持することを推奨する。

次の実行工程は、Current Plan §17の初期実装順11に従い、Work 6Aの中核negative pathとする。
Work 6AではCurrent Work Projectionについて、正式入力欠落、第二正本化、欠測推測、stale／競合の
誤表示をnegative fixtureとして先に固定する。正式projection本体を同時に発明しない。

## 2. 固定した現在地

- Contract version 2のReview経路はaccepted artifactまで完了した。
- `human_decision`は`approved`、Provenanceは11 node・10 edgeで`verified`である。
- Codexの独立再実行は関連83件、全1007件とも合格した。
- Definition Challengeは`passed`、blocking Finding 0件であり、チェックリストの同項目は完了Evidenceへ
  接続できる。

固定Evidence：

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json` | `151c63c838850a3da319b5f1eaa8cf0d02379aed85b0a592f124e3624c275354` |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md` | `3edf6f88bd85619c9e75868f066ddc1d0b66c41e842d27cd05abffac64d9bed5` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | `aace8f35b79cbe4e3113433b55e903e86e0171f04738b180e1728eb83bd93ca6` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | `ad7b82ae74cec8655c205191feb4bf89801353eb8c7838f239f8b1c7da4c6658` |

## 3. 今すぐ正式写像できない理由

既存のbootstrap projectionは、Plan参照とworkflow event streamから次を導出する。

- Stage、Work、Work Item、TDD状態
- 次の実行可能作業
- blocker、Human判断待ち、stale、deferred、cancel
- 欠測と競合の診断

一方、現在の`tools.task_contract`が持つ正式recordは、最初のReview Task Contractの実行経路に限定される。
Contract version 2の11 nodeは次である。

```text
requirement_binding → review_task_contract → definition_challenge_verdict
→ contract_approval → compile_verdict → context_manifest → workflow_permit
→ finding_set → conformance_verdict → final_challenge_verdict → human_decision
```

この経路には、Portfolio、開発Work Item、Stage、dependency／cycle、pause／resume、session lifecycle、
次作業を権威的に表す正式recordがない。Review Task Contract自身も一文書のreviewを対象にしており、
ReviewCompass3開発全体の現在位置authorityではない。

したがって現時点で写像を実装すると、次のいずれかになる。

1. bootstrap eventまたはTODOの値を「正式record」と呼び替える。
2. 未承認のPortfolio／Work Item／Workflow state schemaをWork 5Aへ追加する。
3. 欠けたStage、Work、next actionを推測する。

いずれも、第二正本の禁止、小さなE2E縦切り、欠測時fail-closedの方針に反する。

## 4. 選択肢

### 案A：正式入力が揃うまでdeferし、Work 6Aへ進む（推奨）

- Definition Challenge項目を完了Evidenceへ接続する。
- Current Work Projection正式写像とrefactor後再確認は未完了のまま保持する。
- defer理由、必要入力、再開条件をチェックリストとTODOへ記録する。
- Work 6Aで、正式入力欠落や第二正本化をnegative fixtureとして先に固定する。
- Portfolio／Work Item／Workflow stateの承認済み最小recordが揃った時点で写像を再開する。

利点は、未承認schemaを増やさず、Current Planの次工程へ進めることである。欠点は、Work 5Aの二項目が
未完了のまま残ることである。

### 案B：bootstrap eventを部分的に包むadapterを今作る

形式上はTask Contractの参照を追加できるが、Stage、Work、next actionのauthorityはbootstrapのままである。
「正式recordへの写像が完了した」と誤表示しやすいため採用しない。

### 案C：正式Portfolio／Work Item／Workflow stateを今実装する

Current Work Projectionを完全に導出できるが、Work 5Aの一Contract typeという承認scopeを超え、Work 4の
残設計とWork 6Aのnegative fixtureより先に大きな基盤を作ることになるため採用しない。

## 5. 案Aの再開条件

正式写像は、少なくとも次が固定された後に再開する。

- Stage／Work／Work Item identityとstate owner
- Plan、Portfolio、Work Item、Task Contractの型付きrelation
- dependency、cycle、pause／resume、termination、Human decision、staleの正式record
- 次の実行可能作業を導出するWorkflow規則
- 欠測、競合、stale、表示器failureを区別するnegative test

再開時もprojectionは派生viewとし、手編集可能な状態正本、独立status database、UI固有authorityを作らない。

## 6. Human判断

Humanが案Aを承認する場合、次を許可する。

1. Definition Challenge完了Evidenceのチェックリスト反映。
2. Current Work Projection正式写像とrefactor後再確認のdefer理由・再開条件の記録。
3. TODOをWork 6Aの中核negative path開始待ちへ更新。
4. Work 6Aの既存negative test inventoryと、未被覆項目のRED test作成をClaudeへ委譲する指示書の作成。

この承認は、Work 6AのGREEN実装、Work 4B、Work 5B、正式projection schema、UI、automation、外部送信を
承認しない。RED testの独立確認後に、GREEN実装範囲を別途確定する。
