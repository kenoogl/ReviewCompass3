# Work 4A v3.1 Acceptance RED Evidence v1

## 対象

- Test：`tests/test_work4a_rebuild_v3_1_e2e.py`
- 正本設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md`（§13 I1〜I21）
- 承認：`DEC-WORK4A-REBUILD-DESIGN-004`

## RED結果

```text
21 failed in 0.15s
E   AttributeError: module 'tools.development.work4a_rebuild_v3' has no attribute 'write_freshness_policy_v2'
```

v3.1の実装が存在しないため、21件すべてが失敗する。期待を緩めた通過は一件もない。
v3の受入22件は影響を受けず、引き続きGREENである。

## 受入項目とtestの対応

| 設計§13 | test |
| --- | --- |
| I1 抽出対象を漏れなく収録、除外は件数と理由を記録 | `test_i1_routine_profile_covers_all_declared_constructs` |
| I2 `absence_does_not_imply_no_effect`必須 | `test_i2_marker_detection_flag_must_be_true` |
| I3 痕跡語彙外を拒否 | `test_i3_unknown_effect_marker_is_rejected` |
| I4 Routine ProfileへのLLM由来fieldを拒否 | `test_i4_llm_field_in_routine_profile_is_rejected` |
| I5 非advisoryのProposalを拒否 | `test_i5_non_advisory_proposal_is_rejected` |
| I6 生成元fieldの必須と対象Profile Digestの一致 | `test_i6_provenance_fields_are_required_and_bound` |
| I7 根拠不足の提案は`null`＋`human_review_required`で受理 | `test_i7_unresolved_proposal_is_accepted_when_marked` |
| I8 ProposalをEntryのdisposition根拠にできない | `test_i8_proposal_cannot_authorize_entry_disposition` |
| I9 snapshot不一致で停止 | `test_i9_snapshot_mismatch_stops` |
| I10 外部record不在でもcurrent検証成功 | `test_i10_missing_external_records_do_not_block_current` |
| I11 group未該当が残れば停止 | `test_i11_uncovered_routine_stops_expansion` |
| I12 展開結果が`applied_group_rule_id`を持つ | `test_i12_expansion_records_group_rule_id` |
| I13 機械初期値よりHuman値が優先 | `test_i13_human_value_overrides_machine_proposal` |
| I14 抽出規則v2で新しいCandidate Run | `test_i14_rule_v2_creates_new_candidate_run` |
| I15 schema_version 1のAttestationを読める | `test_i15_schema_version_one_attestation_is_readable` |
| I16 同一構造Digestが同一group | `test_i16_structural_match_group_is_shared_by_identical_structure` |
| I17 symbol_id重複で停止 | `test_i17_symbol_id_collision_stops` |
| I18 参照範囲外と自己参照で停止 | `test_i18_out_of_scope_reference_stops` |
| I19 根拠不在と語彙外`kind`で停止 | `test_i19_missing_evidence_stops` |
| I20 `code_reference`不一致で停止 | `test_i20_code_reference_mismatch_stops` |
| I21 正しい`code_reference`根拠は受理 | `test_i21_valid_code_reference_evidence_is_accepted` |

## 規律

実装中にこのtestの期待を緩めない。v3の22件も同時にGREENを保つ。
LLMによるDisposition Proposalの実生成は本作業に含めない。testはschemaと検証のみを対象とする。
