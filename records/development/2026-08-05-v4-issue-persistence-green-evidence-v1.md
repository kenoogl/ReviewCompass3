# V4 Issue永続化：GREEN Evidence v1（実装）

## 対象

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-issue-persistence-and-session-policy-triage.md`
RED Evidence：`records/development/2026-08-05-v4-issue-persistence-red-evidence-v1.md`

この記録は**実装だけ**の作業単位を対象とする。承認済み4件のHuman triage decisionと
正式Issue recordは、別の作業単位で作る。

## 実装したもの

### 1. V4専用Issue directoryと永続schema

`config/development-issue-resolution-pilot-v4.json`へ次を追加した。

- `directories.issue_record_v2`：`.reviewcompass/workflow/issues-v4`
- `issue_record_v2`：`schema_version: 2`、`issue_id_prefix: ISSUE`、
  `initial_state: registered`、`record_fields`（10個）

`load_config()`は次をfail-closedで拒否する。

| 条件 | 停止code |
| --- | --- |
| `directories.issue_record_v2`が無い | `config_invalid` |
| V4 Issue directoryが旧Issue directoryと同一 | `config_invalid` |
| `issue_record_v2.schema_version`が`issue_schema_version`と食い違う | `config_invalid` |
| 初期stateが未知、または作業中stateである | `config_invalid` |

V4 Issue recordのfieldは次の10個で固定し、これ以外は拒否する。

`record_kind`、`schema_version`、`issue_id`、`issue_version`、`created_at`、`state`、
`problem`、`candidate_ref`、`triage_decision_ref`、`content_digest`

- file名は`{issue_id小文字}--v{issue_version}.json`として決定的に導出する。
- `candidate_ref`は候補bundleのpath・SHA-256・schema version・candidate ID・candidate content digestを持ち、
  検証時に実fileから再確認する。
- `triage_decision_ref`はdecisionのID・version・path・file SHA-256・content digestを持ち、
  検証時にdecision fileを読み直して再確認する。参照先decisionは
  `validate_human_triage_decision()`で単体検証したうえで、candidate参照の一致、昇格承認、
  issue IDの一致まで確認する。
- `content_digest`は`content_digest`を除いた正準JSONのSHA-256とする。

拒否する条件と停止codeは次のとおり。

| 条件 | 停止code |
| --- | --- |
| 未知field、field欠落 | `v4_issue_field_unknown`／`v4_issue_field_invalid` |
| schema version不一致（旧Issueを含む） | `v4_issue_schema_version_unsupported` |
| issue ID・version・作成時刻の形式不正 | `v4_issue_identity_invalid` |
| 未知state | `issue_state_unknown` |
| record pathがID規則と不一致 | `v4_issue_path_mismatch` |
| decision pathの絶対path・`..`脱出 | `v4_issue_path_invalid` |
| decision fileが無い、file SHA不一致 | `v4_issue_decision_reference_stale` |
| decisionのID・version・content digest・candidate参照・昇格承認・issue ID不一致 | `v4_issue_decision_mismatch` |
| bundle SHA不一致、candidate不存在、candidate digest不一致 | `candidate_bundle_digest_mismatch`／`candidate_not_found`／`candidate_digest_mismatch` |
| content digest不一致 | `v4_issue_digest_mismatch` |

`validate_v4_issue_repository()`はV4 Issue directoryだけを走査し、record単体検証に加えて
issue IDの重複と、同一candidateに有効Issueが二件以上ある状態
（`v4_issue_duplicate_for_candidate`）を拒否する。旧Issue directoryは読まない。

### 2. Issue作成関数

`build_v4_issue_record()`は、既存の`promote_candidate_from_decision()`を権限判定の関門として
呼び、そのうえで永続recordを組み立てる。したがってHuman decisionが
`decision_maker: human`、`promote_to_issue: true`、`disposition: issue_resolution`、
candidate参照の完全一致、競合なしを満たさない限りrecordを作れない。

候補bundleは読むだけで書き換えない。初期stateは`registered`であり、`in_progress`へは進めない。
`count_active_issues()`で0件のままである。

## RED→GREEN

| 段階 | receipt | status | 結果 |
| --- | --- | --- | --- |
| RED | `records/development/2026-08-05-v4-issue-persistence-red-test-receipt-v1.json` | `failed`／exit 1 | `3 failed, 809 passed, 3 errors` |
| GREEN | `records/development/2026-08-05-v4-issue-persistence-green-test-receipt-v1.json` | `passed`／exit 0 | `815 passed` |

いずれも公式Test runner（`tools/development/policy_test_runner.py`、suite `full`、
Python 3.9.6、pytest 8.4.2、fallback false）で実行した。RED時に追加したL1〜L6は
実装中に一度も変更していない。既存809testも変更していない。

## 旧Pilotへの影響

- 旧Issue directory`.reviewcompass/workflow/issues/`は1件のままである。
- 旧PilotのvalidatorはそのIssueを従来どおり通す。
- V4 validatorは旧Issueを`v4_issue_schema_version_unsupported`として扱い、V4語彙で再判定しない。
- 旧Pilotのconfig、V1 decision、V1 Issue、旧testは変更していない。

## 変更したfile（この作業単位）

- `config/development-issue-resolution-pilot-v4.json`
- `tools/development/issue_intake_v4.py`
- `tests/test_issue_intake_v4.py`
- `.reviewcompass/workflow/issues-v4/.gitkeep`（新規directory）
- 本Evidenceと二つのreceipt、RED Evidence

候補bundle`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`は
変更していない（SHA-256 `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`）。
