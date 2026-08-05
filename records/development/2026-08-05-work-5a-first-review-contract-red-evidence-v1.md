# Work 5A First Review Task Contract RED Evidence v1

## 対象

- Test：`tests/test_first_review_task_contract_e2e.py`（25件）
- 正本設計：`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`（§8）
- 承認：`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-first-review-contract-implementation.md`

## RED結果

```text
25 errors in 0.18s
E   ModuleNotFoundError: No module named 'tools.task_contract'
```

Runtime package `tools/task_contract/`が存在しないため、25件すべてがcollection errorで停止する。
期待を緩めた通過は一件もない。既存testは変更しておらず、GREENのままである。

## 受入項目とtestの対応

### 正常例

| 設計§8.1 | test |
| --- | --- |
| A1 Contract schemaが全項目を要求 | `test_a1_contract_schema_requires_every_section` |
| A2 1 bundleと6 typed viewの決定的生成 | `test_a2_compile_produces_one_bundle_and_six_views` |
| A3 Requirementとの順逆被覆 | `test_a3_requirement_coverage_is_bidirectional` |
| A4 Context Manifestの7項目・材料束・Scope contract | `test_a4_context_manifest_fixes_materials_and_scope` |
| A5 permitされたRun一件だけ | `test_a5_permit_allows_a_single_active_leaf` |
| A6 ConformanceとFinal Challengeが別ownerで順に通過 | `test_a6_conformance_and_challenge_run_in_order_with_distinct_owners` |
| A7 Human decisionの対象Digest束縛 | `test_a7_human_decision_binds_target_digest` |
| A8 Capture Planの事前生成 | `test_a8_capture_plan_is_generated_before_execution` |
| A9 Provenance `verified`とaccepted artifact | `test_a9_provenance_verdict_and_accepted_artifact` |
| A10 `origin`と`continuation`の独立記録 | `test_a10_origin_and_continuation_are_independent` |
| A11 自己対象でも通常経路・関門を迂回しない | `test_a11_self_target_uses_the_same_gates` |

### 負例

| 設計§8.2 | test |
| --- | --- |
| B1 Contract項目欠落で`not_compilable` | `test_b1_missing_contract_section_is_not_compilable` |
| B2 義務の受け先欠落で停止 | `test_b2_unreceived_obligation_stops` |
| B3 Context項目欠落で停止 | `test_b3_missing_context_declaration_stops` |
| B4 入力変更後の再利用を`stale`で停止 | `test_b4_context_digest_change_makes_result_stale` |
| B5 owner兼務を拒否 | `test_b5_same_owner_for_conformance_and_challenge_is_rejected` |
| B6 暗黙資料の追加を拒否 | `test_b6_implicit_material_is_rejected` |
| B7 permit無しの開始を拒否 | `test_b7_run_without_permit_is_rejected` |
| B8 Provenanceの辺欠落で`verified`にしない | `test_b8_broken_provenance_edge_is_not_verified` |
| B9 Human決定のDigest不一致を拒否 | `test_b9_human_decision_digest_mismatch_is_rejected` |
| B10 `error` Findingと不承認でaccepted artifactを作らない | `test_b10_error_finding_and_rejection_block_accepted_artifact` |

### 境界例

| 設計§8.3 | test |
| --- | --- |
| C1 Finding 0件でも正常経路が完結 | `test_c1_zero_findings_completes_the_normal_path` |
| C2 `warning`のみでもHuman decisionが必須 | `test_c2_warning_only_still_requires_human_decision` |
| C3 最小Change Setで全段通過 | `test_c3_minimal_change_set_passes_every_stage` |
| C4 同時開始候補があってもactive leafは1件 | `test_c4_second_candidate_does_not_start_concurrently` |

## 規律

実装中にこのtestの期待を緩めない。既存testも弱めない。
実文書へのreview run、Human decision、accepted artifactの作成は本作業に含めない。
LLM、外部送信、外部`DATA_ROOT`、Git write／push／PR／CIを使わない。
