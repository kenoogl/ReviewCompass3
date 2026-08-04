# Issue Resolution Pilot Task Contract v2 Completion Evidence v1

## 成果物

- Task Contract：`records/task-contract/issue-resolution-todo-compaction-implementation-v2.json`
- file SHA-256：`1fb3608e0aa0daabec3680f8913bb28a3ea5ade87acb1d9402d75174098a67a6`
- content Digest：`248f3f8604d4451e4c2c73d3083ca78bc787c2cf1337ae2194d2aea3b9df163f`
- validator：`tools/development/issue_resolution_pilot.py`
- validator SHA-256：`031fcf2a17e751a111a0e7cace2b8d26ed90656adcacaba8b9c9bca755d51563`
- Test：`tests/test_issue_resolution_pilot_implementation_task_contract_v2.py`
- Test SHA-256：`0adc3c55e2ba745194a416d39eda02f60981faa002203d7b59e273889de6d8e5`

## 固定した実行境界

- Plan v4、Challenge v4、Approval Decision、Task Contract v1、固定sourceをfile SHAとcontent Digestで検査する。
- WI-001はcommit `64782ec4e94422462e093f7492d9f87197b37a6d`の完了を繰り越し、実snapshot未作成を固定する。
- Work Item順を`WI-001, WI-002, WI-006, WI-007, WI-003, WI-004, WI-005`へ固定する。
- WI-007 containing commitではTODOを書き換えずsource identityを固定し、WI-003はそのcommit、source identity再読込一致、
  clean worktreeの確認後だけ開始できる。
- Task Contract v2 containing commit前のWI-002、WI-002／WI-006 commit前の実snapshot、green TestだけでのIssue解決を
  禁止する。

## Test補正

最初のGREEN後の意味照合で、v1から複製した`goal`だけが「承認済みPlan v3」を参照していることを検出した。
Plan v4を正本とする承認内容との矛盾であるため、開発方針の要求誤解時のTest修正规則に従い、期待値をPlan v4へ補正し、
旧Plan表記を拒否する負例を追加した。補正後の実装前確認は`2 failed, 7 passed`で、失敗は旧goalを持つ契約実体と
旧表記を拒否しないvalidatorの二点だけだった。Testを削除または緩和していない。

## 検証結果

- targeted：`python3 -m pytest -q tests/test_issue_resolution_pilot_implementation_task_contract_v2.py`
- 結果：`9 passed in 0.03s`
- 公式runner receipt：
  `records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-green-test-receipt-v1.json`
- receipt SHA-256：`b4c14ee9b3d99822f5059b22fe6b53c4c83e914e74685d42a60d80e880fc1cba`
- 全体結果：`590 passed in 2.51s`、`fallback_used: false`
- `git diff --check`：合格

## 判定

Task Contract v2はGREENで、containing commit確認後に`implementation_in_progress`を導出できる。実snapshot、WI-002、
TODO compaction、Resolution Verdict、Issue解決は未実施であり、次の独立作業単位はWI-002 REDである。
