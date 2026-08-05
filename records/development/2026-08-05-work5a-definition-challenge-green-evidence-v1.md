# Work 5A Definition Challenge GREEN Evidence v1

- 対象：後継draft Review Task Contract version 2（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`）
- 承認：`DEC-WORK5A-DEFINITION-CHALLENGE-001`、`DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`
- RED Evidence：`records/development/2026-08-05-work5a-definition-challenge-red-evidence-v1.md`
- RED commit：`927183bf25d7782f4a84fdbe45eb9e1357c89b91`
- 公式receipt：`records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md`

## 1. 変更したmodule

| module | 変更 |
| --- | --- |
| `tools/task_contract/definition_challenge.py` | **新設**。material set、D1〜D8、verdict、Contract approval |
| `tools/task_contract/identity.py` | record kind 3件とstop code 14件を登録 |
| `tools/task_contract/contract.py` | version 2の宣言（§6.1の差分だけ）と、compile事前gate |
| `tools/task_contract/execution.py` | Contract versionに応じた来歴の期待node／edgeと、封の再確認 |
| `tools/task_contract/__init__.py` | public APIの明示export |

未定義の汎用framework、plugin、policy、拡張pointは作っていない。

## 2. 追加したpublic API

```python
build_definition_challenge_material_set(project_root, contract, material_paths,
                                        material_records=(), record_id=None)
run_definition_challenge(project_root, contract, requirement_binding, material_set,
                         owner=DEFINITION_CHALLENGE_OWNER)
build_contract_approval(contract, definition_challenge_verdict, decision,
                        human_id, decided_at, owner=CONTRACT_APPROVAL_OWNER)
compile_gate_reason(contract, definition_challenge_verdict, contract_approval)
provenance_node_roles(contract_version)
```

既存関数の追加引数は次である。version 1の呼出しは引数なしでそのまま動く。

- `build_review_task_contract(..., supersedes=None, requirement_receivers=None, review_owners=None)`
- `compile_contract(..., definition_challenge_verdict=None, contract_approval=None)`
- `verify_provenance(..., definition_challenge_verdict=None, contract_approval=None)`

定数も明示exportした。`DEFINITION_CHECKS`、`DEFINITION_SEVERITY_CLASSES`、
`DEFINITION_VERDICT_STATUSES`、`FORBIDDEN_CAPABILITIES`、`STAGE_CONFUSION_KINDS`、
`BOUND_REQUIREMENT_IDS`、`REQUIREMENT_RECEIVERS`、`DEFAULT_REVIEW_OWNERS`、
`DEFINITION_CHALLENGE_OWNER`、`CONTRACT_APPROVAL_OWNER`、`CONTRACT_APPROVAL_DECISIONS`、
`COMPILE_GATE_REASONS`、`CONTRACT_V2_REQUIRED_EDGES`、`CONTRACT_V2_EDGE_ORDER`、
`PROVENANCE_EDGE_ORDER`。

## 3. 追加したrecord kindとstop code

record kindは3件で、いずれも版付き、Digest付き、上流`record_ref`付きの閉じたrecordである。

| record kind | identity | 上流参照 |
| --- | --- | --- |
| `definition_challenge_material_set` | `DCM-<contract id>` v1 | `contract_ref` |
| `definition_challenge_verdict` | `DCV-<contract id>` v1 | `contract_ref`、`material_set_ref`、`requirement_binding_ref` |
| `contract_approval` | `CA-<contract id>` v1 | `contract_ref`、`definition_challenge_ref` |

stop codeは14件を`STOP_CODES`へ登録した。D1〜D8の8件と、Amendment§3の閉じたreason 6件である。

## 4. D1〜D8の実装

すべてLLMを使わない決定的検査である。Findingは`blocking | nonblocking`、verdictは
`passed | failed`だけを使い、既存の`error / warning / info`と語彙を分けている。
現時点でD1〜D8はすべて`blocking`で、`nonblocking`の実例は作っていない（設計§4.1）。

| 検査 | 実装した判定 |
| --- | --- |
| D1 | `requirement_receivers`が束縛16 IDと完全一致し、各値が10節の実在する非空fieldを指す |
| D2 | 10節が非空で、AcceptanceがDefinition Challengeの通過を要求し、Provenance obligationsが`definition_challenge_verdict`を含む |
| D3 | `boundary.target_paths`が1件かつ`docs/`始まり |
| D4 | `call_llm`、`external_transmission`、`write_artifact`、`git_write`がすべて明示的に偽 |
| D5 | `review_owners`のDefinition Challenge、Conformance、Final Challenge、Human decisionが非空でpairwise distinct（Amendment§2のContract approval ownerも同じ集合で重複を見る） |
| D6 | `requirement_ids`が束縛16件と完全一致 |
| D7 | material setが検査対象Contractへ結ばれ、各fileが実在しDigestが一致する |
| D8 | material setに`plan_bundle`、`compile_verdict`、`finding_set`、`conformance_verdict`、`final_challenge_verdict`が無い |

D7だけは扱いを二つに分けた。**材料の欠落とDigest不一致は`definition_material_missing`で停止し、
verdictを発行しない**（設計§2.2の明文）。material setが別Contractへ結ばれている場合は
検査対象が読み取れる状態なので、D7のblocking Findingとして`failed` verdictを出す。

Architecture Policy、risk catalog、同じ運用面の隣接Contract、Challenge Policyは実在しないため
検査していない（設計§2.2、§7）。推測で新設していない。

## 5. compile事前gate（Amendment§3）

`compile_gate_reason()`が、Plan bundleを作る前に次の順で検査する。返すreasonは閉じた6語彙だけである。

1. Challenge欠落 → `definition_challenge_missing`
2. Challengeのschema不正またはDigest改竄 → `definition_challenge_invalid`
3. Challengeが`passed`でない → `definition_challenge_failed`
4. ChallengeのContract refが不一致 → `definition_challenge_invalid`
5. Approval欠落 → `contract_approval_missing`
6. Approvalのschema不正またはDigest改竄 → `contract_approval_invalid`
7. Approvalが`approved`でない → `contract_approval_rejected`
8. ApprovalのContract refが不一致 → `contract_approval_invalid`
9. ApprovalのChallenge refが入力Challengeと不一致 → `contract_approval_invalid`
10. Definition Challenge owner、Contract approval owner、Human review acceptance ownerが分離していない → `contract_approval_invalid`

一件でも満たさない場合、`compile_verdict.status`は`not_compilable`で、`plan_bundle`を**含めない**。
Contract version 1はこのgateを通さない（履歴再読込みの互換性）。

Contract approvalは、会話文、TODO、単なるbooleanでは代用できない。必須fieldは
`owner`、`decision_class`、`decision`、`human_id`、`decided_at`、`contract_ref`、
`definition_challenge_ref`、`content_digest`である。`passed`でないverdictへは束縛できない。

## 6. Provenance

期待node列はContract versionから決める。辺数だけでは通さず、各nodeのkind、identity、version、
Digestとedge順序を照合する。

| Contract version | node | edge |
| --- | --- | --- |
| 1 | 9 | 8 |
| 2 | 11 | 10 |

version 2は`requirement_binding → review_task_contract → definition_challenge_verdict
→ contract_approval → compile_verdict → …`の順で、`contract_approval`がChallengeとcompileの間にある。

来歴が主張するContract versionは、来歴自身の`review_task_contract` nodeの`record_version`から読む。
version 2を名乗るnodeがある限り、Definition Challengeとcontract approvalのnodeを必ず要求するため、
node列だけを削って version 1として通すことはできない。

`validate_provenance_verdict()`の末尾へ、封をしたあとの改竄を見る自己Digest照合を足した。
node、edge、closureの構造検査を**先に**通すので、既存の停止codeは変わっていない。

`verify_provenance()`はversion 2で、compileと同じgate判定を再確認し、
Definition Challenge owner、Contract approval owner、Conformance、Final Challenge、
Human decisionのownerが互いに異なることを確かめる。同じHuman個人が別decision classを担うこと自体は
禁止していない。

## 7. RED→GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_work5a_definition_challenge.py` | `44 failed, 1 passed` | `45 passed` |
| `tests/test_first_review_task_contract_e2e.py`（既存38件） | `38 passed` | `38 passed` |
| 公式policy runner suite `full` | 実施不能（着手前から1件失敗） | **`1007 passed`** |

公式receiptの集計は
`{"errors": 0, "failed": 0, "passed": 1007, "skipped": 0, "total": 1007, "xfailed": 0, "xpassed": 0}`、
Python 3.9.6、pytest 8.4.2、fallbackなしである。

### 7.1 RED Testのfixtureを1点だけ直した

「別Contractへのapproval差し替え」を確かめる2件（H15と、material setの結び先違い）で、
比較対象の「別Contract」を同じ`contract_id`・同じ内容で作っていた。record identityも内容も同じなので、
実際には**同一record**であり、負例になっていなかった。`contract_id`を別にして、真に別のContractを
比較するよう直した。

- 直したのはfixtureだけである。assertionは1件も変えていない（`not_compilable`、
  `contract_approval_invalid`、`failed`、`D7`の期待はそのまま）。
- 期待を実装へ合わせて緩めてはいない。むしろ、それまで実質的に何も検査していなかった負例が、
  実際に別Contractのapprovalを拒否することを検査するようになった。
- 他の43件のTestは変更していない。

## 8. 変更していないもの

- Contract version 1の出力。version 2専用fieldはversion 1のrecordへ足していない。
  version 1でこれらの引数を渡すと`schema_violation`で止める。
- 既存accepted artifact、既存Provenance record、`records/`配下の既存record。
- 承認済み設計、Amendment、Decision、Requirement、Current Plan、checklist、Development Policy。
- 既存Test。`tests/test_first_review_task_contract_e2e.py`は1文字も変えていない。
- `contract_approval`の実recordは作っていない。Humanの承認を代行しない。
