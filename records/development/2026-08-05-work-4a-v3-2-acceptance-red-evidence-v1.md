# Work 4A v3.2 Acceptance RED Evidence v1

## 対象

- Test：`tests/test_work4a_rebuild_v3_2_e2e.py`（11件）
- 正本設計：`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`（§6 J1〜J10）
- 承認：`DEC-WORK4A-REBUILD-DESIGN-005`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-2-implementation.md`

## RED結果

```text
11 failed in 0.11s
E   AttributeError: module 'tools.development.work4a_rebuild_v3' has no attribute
    'write_freshness_policy_v3' ではなく 'build_routine_profile_v2'
```

Profile v2の実装（`build_routine_profile_v2`、`validate_routine_profile_v2_document`、
`build_decision_card`、`select_additional_context`）が存在しないため、11件すべてが失敗する。
期待を緩めた通過は一件もない。

本commitはRED test commitであり、固定したJ1〜J10が期待理由で失敗する状態を記録する。
既存のv3受入22件、v3.1受入21件、Task Contract固定入力11件は変更しておらず、GREENのままである。

## 受入項目とtestの対応

| 設計§6 | test |
| --- | --- |
| J1 同一universe内の直接caller/calleeを相互記録 | `test_j1_direct_caller_and_callee_are_mutually_recorded` |
| J1 Profile外のsymbol参照を拒否 | `test_j1_unknown_reference_is_rejected` |
| J2 alias・動的・reflectionを未解決として計上 | `test_j2_unresolved_calls_are_counted_not_faked` |
| J3 raise・catch・bare exceptの構文抽出 | `test_j3_exception_names_are_syntactic_only` |
| J4 分割度指標と`complexity_signal`の決定性 | `test_j4_complexity_signal_is_deterministic` |
| J5 `tests/`直下の直接参照のみ、範囲外を拒否 | `test_j5_test_references_are_limited_to_tests_tree` |
| J6 `__all__`・cross-package・CLIから公開API指標 | `test_j6_public_api_signal_is_derived_from_declared_inputs` |
| J7 構造一致だけで`merge`を確定しない | `test_j7_structural_match_group_is_not_a_merge_conclusion` |
| J8 意味的比較候補は同一Profile内・上限10件 | `test_j8_semantic_candidates_are_bounded_and_in_profile` |
| J9 Profile v1とv2の併存と非書換え | `test_j9_profile_v1_and_v2_coexist_without_rewrite` |
| J10 判断カードと限定した周辺code選択 | `test_j10_decision_card_selects_bounded_context` |

## 規律

実装中にこのtestの期待を緩めない。既存のv3／v3.1 testも弱めない。
LLMによるDisposition Proposalの生成、意味的重複判断、処置labelの提案は本作業に含めない。
