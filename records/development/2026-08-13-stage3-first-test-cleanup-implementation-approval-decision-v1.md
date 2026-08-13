# 第3段 最初の試験整理 実施承認判断 v1

- 判断日：2026-08-13
- 判断者：利用者
- 対象計画：`docs/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2.md`
- 対象計画SHA-256：`c470da1e4ed3b19c548b64db0d817bdec2d1236b747d3388f50eeccf8c6d1147`
- 独立修正後確認：`records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-one-time-correction-review-v1.md`
- 独立修正後確認SHA-256：`0afc66a36878dc431d7a3e9105b82b2e49c7c0886b8129211460d4c73cf09c45`
- Claude確認結果：`records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-claude-delta-review-result-v1.md`
- Claude確認結果SHA-256：`d2ea0a5ccde1981f2732e5b9f134b1ef3271e9ec0cd22d147a494aee7356c4dd`

## 1. 利用者判断

利用者は本会話で「承認」と明示し、次の三点を承認した。

1. 案Bを採用し、G04の役割終了二試験を削除する。
2. 未承認だった`test_declaration_map_keys_equal_scope_requirement_ids`の保証廃止を承認する。
3. 変更範囲を`tests/test_claude_bootstrap_entrypoints.py`一件、次の二試験、専用定数二件に限定する。
   - `test_declaration_map_keys_equal_scope_requirement_ids`
   - `test_red_evidence_keeps_green_fields_explicitly_unimplemented`
   - `MAP_PATH`
   - `REQUIREMENT_IDS`

## 2. 変更しない範囲

G11三試験、G11専用補助処理、現行`TRACEABILITY`、製品コード、設定、正規入口、履歴資料、対応表は
変更しない。

## 3. この承認に含まれないもの

本判断は第3段完了の承認ではない。他の意味群の削除・統合、製品コード整理、G11要求証拠の廃止・置換、
外部送信、履歴書換えは承認しない。
