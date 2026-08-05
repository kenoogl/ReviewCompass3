# Work 5A Contract version 2 Review Run Evidence v1

- 対象Contract：`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`（version 2）
- 承認：`DEC-WORK5A-CONTRACT-V2-APPROVAL-001`
  （`records/development/2026-08-06-work5a-contract-v2-approval-decision-v1.md`）
- Run records：`records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json`
- 指示：`records/session-handoffs/2026-08-06-codex-to-claude-work5a-contract-v2-review-run.md`
- 実行時刻：2026-08-06T06:23:29+0900
- 開始基準commit：`44af24c959f0251e080db0c5ae3f575fb728b833`（HEADの祖先であることを確認）

**Final Challengeの結果を保存した時点で停止した。Human review acceptanceは作っていない。**

## 1. 固定入力の照合

指示§2の4件を全文読み、SHA-256を機械照合した。**4件すべて一致**である。

| path | 判定 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-approval-decision-v1.md` | 一致 |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | 一致 |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | 一致 |
| `records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json` | 一致 |

初回Run bundleから取り出した4 recordは、いずれも封をしたときのcontent digestと一致した。
`definition_challenge_verdict`は`passed`、`blocking_count`は0である。

## 2. 実行command

```text
.venv/bin/python3 <scratchpad>/review_run.py
```

`tools.task_contract`のpublic APIだけを指示§3の順で呼ぶ。

```python
approval        = build_contract_approval(contract, definition_challenge_verdict=challenge,
                                          decision="approved", human_id="kenoogl",
                                          decided_at="2026-08-06T06:20:15+09:00")
compile_verdict = compile_contract(contract, requirement_binding=binding,
                                   definition_challenge_verdict=challenge,
                                   contract_approval=approval)
snapshot        = read_source_snapshot(project_root=ROOT, target_paths=(TARGET,),
                                       base_commit=..., head_commit=...)
context         = build_context_manifest(contract, plan_bundle, snapshot)
permit          = acquire_permit(workflow_state=new_workflow_state(), context_manifest=context)
finding_set     = run_stub_reviewer(contract, context_manifest=context, permit=permit)
conformance     = evaluate_conformance(contract, plan_bundle, finding_set)
final_challenge = evaluate_final_challenge(contract, conformance_verdict=conformance,
                                           finding_set=finding_set)
```

`record_human_decision`、`verify_provenance`、`accept_artifact`は**一度も呼んでいない**。

## 3. 結果

| 段 | 結果 |
| --- | --- |
| `contract_approval` | `approved`、`contract_approval_owner`、`human_id: kenoogl`、`decided_at: 2026-08-06T06:20:15+09:00` |
| compile | **`compiled`**。Plan bundleは6 view（context_acquisition、review_execution、harness_and_capability、verification、provenance_capture、human_interaction） |
| Finding | **0件**（error 0、warning 0、info 0） |
| Conformance | **`passed`**（`conformance_owner`） |
| Final Challenge | **`passed`**（`final_challenge_owner`、`human_decision_required: true`） |

`error` Findingは無く、ConformanceもFinal Challengeも`failed`ではないため、
指示§4の停止条件には該当しない。

対象文書はContract version 2が束縛する
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`の1件である。
change setは`base_commit: 44af24c9…`、`head_commit: 8767f260…`である。

## 4. 作成したrecordのidentity、version、content digest

| record | record_id | version | content digest |
| --- | --- | --- | --- |
| `contract_approval` | `CA-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `af4209029b2d11f53d9abf0e3ed67dd8d182c1177dfe1625507f03bcb2095b25` |
| `compile_verdict` | `CV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `ad45ebba3659d5ea34751d103bd1fde96b075162bc00a6cabc2aa5b85b8ac332` |
| `source_snapshot` | `SS-FIRST-REVIEW-CONTRACT` | 1 | `90f50d3a5eb744a9c0ab13997dd22d014333f785dbc5b01b26b1bbac90f026e0` |
| `context_manifest` | `CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `149ae4a5f28d9ccd0378d31312b2b3965ed1d3aaa31599ed98b249f080348354` |
| `workflow_permit` | `WP-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `03b8b0d4c691db8f0f4b4f72c5bde7f0de0a9b31814dd85e2e143c90c57a72b5` |
| `finding_set` | `FS-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `59788c36ae787e014a2d360adfde84b67da0c7bae028bbc5144452a70bb51054` |
| `conformance_verdict` | `CFV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `fb6ddb28d4e499d837aab4aaba903bcb1ecad68aed31230c3719374b385e5f46` |
| `final_challenge_verdict` | `FCV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `a3e7887474142b6024484f14553ebfb6b13cede5295d10e6e5c644abd436d3e6` |

すべてnew-onlyで作成した。Run bundleには上流の`requirement_binding`、draft Contract v2、
`definition_challenge_material_set`、`definition_challenge_verdict`も、初回Runの値のまま同梱している。

## 5. 再読込みによる独立照合

保存したbundleを読み直して機械照合した結果は次である。

| 検証 | 結果 |
| --- | --- |
| 12 recordのcontent digest再計算 | **全件一致** |
| `approval.contract_ref` == Contract v2 | 一致 |
| `approval.definition_challenge_ref` == Challenge verdict | 一致 |
| `compile.definition_challenge_ref` / `compile.contract_approval_ref` / `compile.contract_ref` | いずれも一致 |
| `context.plan_bundle_ref` == Plan bundle | 一致 |
| `permit.context_ref` == Context Manifest | 一致 |
| `finding_set.permit_ref` == Workflow permit | 一致 |
| `conformance.finding_set_ref` == Finding set | 一致 |
| `final.conformance_ref` == Conformance verdict | 一致 |
| `verdict.material_set_ref` == material set | 一致 |
| owner分離（Definition Challenge／Contract approval／Conformance／Final Challenge） | 4件すべて別の論理owner |
| bundle内のrecord種別 | 12種。`human_decision`、`provenance_verdict`、`accepted_artifact`は**不在** |

recordは省略せずそのまま保存しているため、content digestを外部から独立に再計算できる。

## 6. Test

| 対象 | 結果 |
| --- | --- |
| `tests/test_work5a_definition_challenge.py` | `45 passed` |
| `tests/test_first_review_task_contract_e2e.py` | `38 passed` |
| 公式全Test | **`1007 passed`** |

`tools/task_contract/`と既存Testは1文字も変更していない（`git status`で確認）。
実行時の不具合は見つかっていない。

## 7. 作っていないもの（停止境界）

Run bundleの`not_executed_steps`へ機械可読で記録した。

- Review結果に対する`human_decision`
- `provenance_verdict`
- `accepted_artifact`

Contract version 1、その既存accepted artifact、既存Provenance recordは変更・無効化・stale化していない。
Human review acceptanceは代行しない。次に進むには、Review結果に対する別のHuman判断が要る。
