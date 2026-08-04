# Work 4A v3.3 Acceptance RED Evidence v1

## 対象

- Test：`tests/test_work4a_rebuild_v3_3_e2e.py`（15件）
- 正本設計：`docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md`（§9 K1〜K12）
- 承認：`DEC-WORK4A-REBUILD-DESIGN-006`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-3-implementation.md`

## RED結果

```text
15 failed in 0.15s
E   AttributeError: module 'tools.development.work4a_rebuild_v3' has no attribute
    'build_routine_profile_v3'
```

Profile v3とComparison Discoveryの実装（`build_routine_profile_v3`、
`build_comparison_discovery`、`validate_comparison_discovery_document`、
`validate_routine_profile_v3_document`、`reject_bounded_seed_basis`、
`build_llm_initial_input`、`record_additional_read`）が存在しないため、15件すべてが失敗する。
期待を緩めた通過は一件もない。

本commitはRED test commitであり、固定したK1〜K12と負例が期待理由で失敗する状態を記録する。
既存のv3受入22件、v3.1受入21件、v3.2受入11件、Task Contract固定入力11件は変更しておらず、
GREENのままである。

## 受入項目とtestの対応

| 設計§9 | test |
| --- | --- |
| K1 全memberを切り捨てず同一Profile内から収録 | `test_k1_groups_hold_all_members_from_the_same_profile` |
| K1 負例：Profile外のmemberを拒否 | `test_k1_member_outside_profile_is_rejected` |
| K2 代表は最大3件、memberは全件 | `test_k2_representatives_are_capped_without_truncating_members` |
| K3 一routineが複数根拠groupへ所属 | `test_k3_routine_can_belong_to_multiple_bases` |
| K4 package・引数個数だけでgroupを作らない | `test_k4_package_or_arity_alone_does_not_form_a_group` |
| K4 負例：語彙外basisを拒否 | `test_k4_unknown_basis_kind_is_rejected` |
| K5 根拠と限界の保持 | `test_k5_basis_evidence_and_limits_are_recorded` |
| K6 presentation classの決定性と語彙外拒否 | `test_k6_presentation_class_is_deterministic` |
| K7 Discoveryは`merge`を確定しない | `test_k7_discovery_never_concludes_merge` |
| K8 Profile digest・run ID・source content ID不一致を拒否 | `test_k8_profile_mismatch_is_rejected` |
| K9 bounded seedを根拠にできない | `test_k9_bounded_seed_cannot_be_a_basis` |
| K9 Profile v3はDiscoveryを参照しない | `test_k9_profile_v3_must_not_reference_discovery` |
| K10 初期入力に全source treeとsource本文を含めない | `test_k10_initial_llm_input_has_no_source_bodies` |
| K11 追加読込はgroup・理由・symbol IDをprovenanceへ残す | `test_k11_additional_read_requires_provenance` |
| K12 Profile v2／v3／Discoveryの併存と非書換え | `test_k12_profiles_and_discovery_coexist` |

## 規律

実装中にこのtestの期待を緩めない。既存のv3／v3.1／v3.2 testも弱めない。
期待を変える必要が生じた場合は設計矛盾として停止し、完了報告へ理由を記録する。
LLMによる説明生成、意味的比較、Disposition Proposal、処置labelの提案は本作業に含めない。
