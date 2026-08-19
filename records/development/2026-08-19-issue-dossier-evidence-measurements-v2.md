# 測定ブロック：issue実態調書tool 受入確認の実測

- captured_at：2026-08-19T12:03:12+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-issue-dossier-evidence-commands-v1.json`（SHA-256 `d836bf7f0e1322ee8c6fc81cbd2067ecdce578e974851ae6dfee36eae0f927f6`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## lane系試験26本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_reconciliation_dossier.py',\n     'tests/test_triage_decision_writer.py',\n     'tests/test_issue_record_writer.py',\n     'tests/test_issue_state_transition.py',\n     'tests/test_workflow_ledger_verify.py',\n     'tests/test_improvement_candidate_writer.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.731s
- 完全性：二重実行一致

- stdout：

```text
exit 0
26 passed

```

## 台帳関連試験群の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py',\n     'tests/test_issue_intake_v4.py',\n     'tests/test_issue_resolution_pilot.py',\n     'tests/test_agents_lane_guidance.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.328s
- 完全性：二重実行一致

- stdout：

```text
exit 0
68 passed

```

## 実repoでの調書生成（8件・拘束flag検出・exit 0が合格）

- argv：`[".venv/bin/python3", "-m", "tools.development.issue_reconciliation_dossier"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.313s
- 完全性：二重実行一致

- stdout：

```text
{"issue_total":8,"issues":[{"activity":{"git_mention_count":2,"records_latest":"2026-08-19-issue-dossier-evidence-measurements-v1.md","records_mention_count":20},"candidate_id":"IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001","created_at":"2026-08-06T14:39:40+09:00","issue_id":"ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001","issue_version":1,"referenced_paths":{"missing":[],"total":1},"state":"registered","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":4,"records_latest":"2026-08-19-issue-ledger-reconciliation-decision-v1.md","records_mention_count":14},"candidate_id":"HTC-66C3E6CA","created_at":"2026-08-05T14:02:25+09:00","issue_id":"ISSUE-HTC-66C3E6CA","issue_version":2,"referenced_paths":{"missing":[],"total":0},"state":"resolved","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":3,"records_latest":"2026-08-19-issue-ledger-reconciliation-decision-v1.md","records_mention_count":6},"candidate_id":"HTC-BEB5E0BD","created_at":"2026-08-05T13:17:35+09:00","issue_id":"ISSUE-HTC-BEB5E0BD","issue_version":1,"referenced_paths":{"missing":[],"total":0},"state":"registered","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":7,"records_latest":"2026-08-19-issue-ledger-reconciliation-decision-v1.md","records_mention_count":29},"candidate_id":"HTC-C9F6C917","created_at":"2026-08-05T13:40:55+09:00","issue_id":"ISSUE-HTC-C9F6C917","issue_version":2,"referenced_paths":{"missing":[],"total":0},"state":"resolved","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":0,"records_latest":"2026-08-19-state-pinning-limited-reopen-test-l6-decision-v1.md","records_mention_count":47},"candidate_id":"IC-TEST-GROWTH-STATE-PINNING-001","created_at":"2026-08-06T15:38:38+09:00","issue_id":"ISSUE-TEST-GROWTH-STATE-PINNING-001","issue_version":1,"referenced_paths":{"missing":[],"total":2},"state":"registered","todo_active":true,"todo_line":"- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する"},{"activity":{"git_mention_count":0,"records_latest":"2026-08-19-issue-dossier-evidence-measurements-v1.md","records_mention_count":2},"candidate_id":"IC-TEST-SHA256-FIXTURE-DUPLICATION-001","created_at":"2026-08-08T08:06:16+09:00","issue_id":"ISSUE-TEST-SHA256-FIXTURE-DUPLICATION-001","issue_version":1,"referenced_paths":{"missing":[],"total":0},"state":"registered","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":0,"records_latest":"2026-08-19-issue-ledger-reconciliation-decision-v1.md","records_mention_count":4},"candidate_id":"IC-TODO-HANDOFF-VERIFICATION-GAP-001","created_at":"2026-08-07T09:12:27+09:00","issue_id":"ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001","issue_version":2,"referenced_paths":{"missing":[],"total":0},"state":"resolved","todo_active":false,"todo_line":null},{"activity":{"git_mention_count":1,"records_latest":"2026-08-19-issue-dossier-evidence-measurements-v1.md","records_mention_count":7},"candidate_id":"IC-UNREVIEWED-WORK-REVIEW-BACKLOG-001","created_at":"2026-08-07T08:21:45+09:00","issue_id":"ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001","issue_version":1,"referenced_paths":{"missing":[],"total":1},"state":"registered","todo_active":false,"todo_line":null}],"status":"ok"}

```

## 新設module・試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/issue_reconciliation_dossier.py", "tests/test_issue_reconciliation_dossier.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.017s
- 完全性：二重実行一致

- stdout：

```text
451c9871d891f09cf9d6c62c546db1492a6eff56ec2aa3209d305fe84fd3cac9  tools/development/issue_reconciliation_dossier.py
bd990f342e08a635aff93084ff1baa3c3d3df469282ed72258be0e44590bc263  tests/test_issue_reconciliation_dossier.py

```
