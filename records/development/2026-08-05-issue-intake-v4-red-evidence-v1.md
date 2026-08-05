# Issue Intake V4 RED Evidence v1

## 対象

- Test：`tests/test_issue_intake_v4.py`（25件）
- 正本設計：`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`（§5 I1〜I9、J1〜J16）
- 固定source：`records/session-handoffs/2026-08-04-todo-before-compaction-001.md`
  （SHA-256 `16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`）

## RED結果

```text
25 errors in 0.15s
E   ModuleNotFoundError: No module named 'tools.development.issue_intake_v4'
```

V4のconfig、schema V2、validatorが存在しないため、25件すべてがcollection errorで停止する。
期待を緩めた通過は一件もない。

## 受入項目とtestの対応

| 設計§5 | test |
| --- | --- |
| I1 抽出の決定性 | `test_i1_intake_extraction_is_deterministic` |
| I2 既存解決済みIssueとの共存 | `test_i2_existing_resolved_issue_coexists_unchanged` |
| I3 登録数に上限なし | `test_i3_registration_has_no_upper_limit` |
| I4 非active状態が複数でもactive 1件で有効 | `test_i4_many_non_active_states_with_one_in_progress` |
| I5 非阻害の登録で中断しない | `test_i5_registering_non_blocking_issue_does_not_suspend` |
| I6 阻害切替でsuspendedとin_progress | `test_i6_blocking_switch_suspends_previous` |
| I7 resolvedまたはHuman裁定後の再開 | `test_i7_resume_after_blocker_resolved_or_human_ruling` |
| I8 TODO projectionの上限 | `test_i8_todo_projection_fits_limits_without_registered_count` |
| I9 旧versionの検証継続とstate非適用 | `test_i9_previous_versions_still_validate` |
| J1 X1（完了Claim見出し） | `test_j1_completed_claim_heading_is_excluded` |
| J2 X2（Evidence行） | `test_j2_evidence_only_line_is_excluded` |
| J3 X3（commit付き実装済み） | `test_j3_resolved_history_line_is_excluded` |
| J4 source Digest不一致 | `test_j4_source_digest_mismatch_stops` |
| J5 重複疑い未立て | `test_j5_duplicate_without_suspect_flag_is_rejected` |
| J6 Human裁定なしの昇格 | `test_j6_promotion_without_human_ruling_is_rejected` |
| J7 二件目のin_progress | `test_j7_second_in_progress_is_rejected` |
| J8 二件目のactive leaf | `test_j8_second_active_leaf_is_rejected` |
| J9 登録だけの中断 | `test_j9_registration_cannot_suspend_current` |
| J10 自己循環 | `test_j10_self_cycle_is_rejected_and_not_persisted` |
| J11 二Issue循環 | `test_j11_two_issue_cycle_is_rejected_and_suspends_all` |
| J12 candidate証跡欠落 | `test_j12_candidate_missing_required_evidence_is_rejected` |
| J13 部分書込み | `test_j13_partial_write_is_rejected` |
| J14 candidateの無権限 | `test_j14_candidate_alone_grants_no_authority` |
| J15 循環中Issueの再開 | `test_j15_resume_within_cycle_requires_resolution_or_ruling` |
| J16 TODO禁止marker | `test_j16_forbidden_todo_marker_is_rejected` |

## 規律

実装中にこのtestの期待を緩めない。既存V1〜V3のconfigとrecordを変更しない。
候補を自動でIssueへ昇格しない。優先順位、統合、根本原因Issue化、再開をHumanの代わりに決めない。
