# Work 4A v3 Acceptance RED Evidence v1

## 対象

- Test：`tests/test_work4a_rebuild_v3_e2e.py`
- 正本設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`（§17 A〜H）
- 承認：`DEC-WORK4A-REBUILD-DESIGN-003`

## RED結果

```text
22 errors in 0.13s
E   ModuleNotFoundError: No module named 'tools.development.work4a_rebuild_v3'
```

実装moduleが存在しないため、22件すべてがcollection errorで停止する。
期待を緩めた通過は一件もない。

## 受入項目とtestの対応

| 設計§17 | test |
| --- | --- |
| A1 project refだけで連鎖が閉じる | `test_a1_chain_closes_with_project_refs_only` |
| A2 外部refのfieldを拒否 | `test_a2_decision_schema_rejects_external_reference_field` |
| B1 `DATA_ROOT`削除でもcurrent検証成功 | `test_b1_current_is_validated_without_data_root` |
| B2 異profileのlocatorは照合しない | `test_b2_locator_of_other_profile_is_not_collated` |
| C1 外部candidate改竄で停止 | `test_c1_tampered_candidate_stops` |
| C2 別projectのdataを拒否 | `test_c2_foreign_project_data_stops` |
| C3 data root脱出を拒否 | `test_c3_data_root_escape_stops` |
| D1 traversal／絶対path／symlinkを拒否 | `test_d1_project_ref_rejects_traversal_absolute_and_symlink` |
| D2 root重なりはPolicyより前に停止 | `test_d2_root_overlap_stops_before_policy` |
| E1 古い観測の流用を拒否 | `test_e1_stale_observation_reuse_stops` |
| E2 HEAD差だけならfresh | `test_e2_head_only_change_is_continuous_fresh` |
| E3 内容差・universe差は昇格不可 | `test_e3_content_and_universe_divergence_block_advance` |
| E4 Attestation内部の同一性不整合 | `test_e4_attestation_content_identity_mismatch` |
| E5 Decisionとの相互検査 | `test_e5_decision_candidate_mismatch` |
| F1 new-onlyで既存を書換えない | `test_f1_new_only_keeps_existing_records` |
| F2 Baseline欠番を拒否 | `test_f2_missing_baseline_version_stops` |
| F3 書込み失敗で部分生成なし | `test_f3_failed_write_leaves_nothing` |
| G1 Policy／Decision不在を拒否 | `test_g1_missing_policy_or_decision_stops` |
| G2 security変更は再検証必須 | `test_g2_security_policy_change_requires_revalidation` |
| G3 legacy Contractの根拠不足 | `test_g3_legacy_contract_requires_full_evidence` |
| H1 要約語彙違反を拒否 | `test_h1_summary_vocabulary_violation` |
| H2 symbol ID一覧Digestの再計算 | `test_h2_symbol_id_list_digest_is_recomputable` |

## 規律

実装中にこのtestの期待を緩めない。moduleを実装してGREENにする。
v1／v2試作を参照・import・復元しない。
