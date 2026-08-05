# Work 5A 初回Definition Challenge Run Evidence v1

- 対象：draft Review Task Contract version 2（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`）
- Run records：`records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json`
- 承認：`DEC-WORK5A-DEFINITION-CHALLENGE-001`、`DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`
- GREEN Evidence：`records/development/2026-08-05-work5a-definition-challenge-green-evidence-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md`
- 実行時刻：2026-08-06T06:12:09+0900

## 1. 実行したcommand

```text
.venv/bin/python3 <scratchpad>/first_run.py
```

このscriptは`tools.task_contract`のpublic APIだけを順に呼ぶ。

```python
binding       = bind_requirements(project_root=ROOT, requirement_ids=BOUND_REQUIREMENT_IDS)
contract      = build_review_task_contract(contract_id=..., contract_version=2,
                                           requirement_binding=binding,
                                           target_paths=(TARGET,), supersedes=<v1 ref>)
material_set  = build_definition_challenge_material_set(project_root=ROOT, contract=contract,
                                                        material_paths=<19件>)
verdict       = run_definition_challenge(project_root=ROOT, contract=contract,
                                         requirement_binding=binding, material_set=material_set)
```

`compile_contract`、`build_contract_approval`、下流のいずれの関数も**呼んでいない**。

## 2. 結果

| 項目 | 値 |
| --- | --- |
| verdict status | **`passed`** |
| `blocking_count` | **0** |
| Finding件数 | **0件** |
| 実行した検査 | D1、D2、D3、D4、D5、D6、D7、D8 |

`nonblocking` Findingも0件である。現時点でD1〜D8はすべて`blocking`分類であり、
`nonblocking`の実例は作っていない（設計§4.1）。

## 3. 作ったrecordのidentityとDigest

| record | record_id | version | content digest |
| --- | --- | --- | --- |
| `requirement_binding` | `RB-FIRST-REVIEW-CONTRACT` | 1 | `831217a7c3850fb711427ddc2c6aaf686b9155338e34dfa406a6fbc9f7af68de` |
| `review_task_contract`（draft v2） | `TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 2 | `cfa129d3afce155a683fed7e7da07c3272fb89922264edf79c239b6d3846cfb4` |
| `definition_challenge_material_set` | `DCM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `d90b9f5efb12bd8bc3b58174f8c323017356194133481bfa9e2f2fe30a778816` |
| `definition_challenge_verdict` | `DCV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `d951862f9ab8b760afe796a4356a1a89cc6dd8053bb597768b4916b7cde4a967` |

すべてnew-onlyで作成した。既存recordの上書きはしていない。

## 4. draft Contract version 2の内容

version 1から変えたのは設計§6.1が列挙した差分だけである。

- `requirement_receivers`：束縛16 Requirementの受け先を、Contractの10節の実在するfield名で明示した（16件）。
- `review_owners`：`definition_challenge_owner`、`contract_approval_owner`、`conformance_owner`、
  `final_challenge_owner`、`human_decision_owner`。5件すべて異なる論理ownerである。
- `acceptance`：version 1の5件へ`definition_challenge_passed`と`contract_approval_recorded`を追加した。
- `provenance_obligations.required_edges`：`contract_approval`を含む11 stepにした。
- `escalation`：`definition_challenge_failed`、`contract_approval_missing`、`contract_approval_rejected`を追加した。
- `supersedes`：Contract version 1（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`、version 1、
  digest `e67dc0d1…`）を指す。この参照はversion 1を無効にもstaleにもしない。

対象文書はversion 1と同じ
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`の1件である。

## 5. 固定した材料（19件）

| 種別 | 件数 | 内容 |
| --- | --- | --- |
| Requirement definition | 16 | `records/requirements/definitions/`の束縛16件 |
| 対象文書 | 1 | Work 4設計提案（§2、§7、§8） |
| 開発方針 | 1 | `docs/development/2026-08-02-development-policy.md` |
| Current Plan | 1 | `docs/current/reviewcompass3-plan-current.md` |

各fileのpathとSHA-256をmaterial setへ固定し、Run後に全19件を再計算して一致を確認した
（`digest_verification.material_files_reverified` が真）。

Architecture Policy、risk catalog、同じ運用面の隣接Contract、Challenge Policyは実在しないため、
材料に含めていない。推測で新設もしていない。これらを要する検査は行っていない（設計§2.2、§7）。

## 6. 決定性の確認

同じ固定材料で再度組み立てた結果、3 recordのcontent digestがいずれも一致した。

| record | 再現一致 |
| --- | --- |
| draft Contract v2 | 一致 |
| material set | 一致 |
| verdict | 一致 |

LLMは使っていない。判定は固定入力から同じ結果を再生成できる。

## 7. 作っていないもの（段の混同を避けるため）

Run bundleの`not_executed_steps`に機械可読で記録した。bundle内のrecord種別は
`requirement_binding`、`review_task_contract`、`definition_challenge_material_set`、
`definition_challenge_verdict`の4種だけであり、次はいずれも存在しない。

`contract_approval`、`compile_verdict`、`plan_bundle`、`context_manifest`、`workflow_permit`、
`finding_set`、`conformance_verdict`、`final_challenge_verdict`、`human_decision`、
`provenance_verdict`、`accepted_artifact`。

- Definition ChallengeはContract定義だけを検査した。対象文書の再Reviewはしていない。
- verdictが`passed`でも、`contract_approval`は作っていない。
  Contract version 2の承認はHumanの判断であり、代行しない。
- Contract version 1、その既存accepted artifact、既存Provenance recordは変更していない。

## 8. 次に必要なHuman判断

Contract version 2を承認するかどうかである。承認する場合は`contract_approval` record
（`decision: approved`、`human_id`、`decided_at`、上のContract v2とverdictへの参照）が必要になる。
それが作られるまで、compile、Review Run、accepted artifactへ進まない。
