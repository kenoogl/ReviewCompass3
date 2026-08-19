# 測定ブロック：候補writer・台帳一括検証入口 受入確認の実測

- captured_at：2026-08-19T11:02:00+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-ledger-writer-evidence-commands-v1.json`（SHA-256 `deda9afa3649985345b2c390b00a0ee2e818727ad0aca8b113bbc49382515974`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 新設試験9本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_improvement_candidate_writer.py',\n     'tests/test_workflow_ledger_verify.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.24s
- 完全性：二重実行一致

- stdout：

```text
exit 0
9 passed

```

## 台帳関連試験群の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py',\n     'tests/test_issue_intake_v4.py',\n     'tests/test_issue_resolution_pilot.py',\n     'tests/test_agents_lane_guidance.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.375s
- 完全性：二重実行一致

- stdout：

```text
exit 0
68 passed

```

## 実repoでの一括検証入口の単独実行（exit 0が合格）

- argv：`[".venv/bin/python3", "-m", "tools.development.workflow_ledger_verify"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.046s
- 完全性：二重実行一致

- stdout：

```text
{"accounted":{"allowlist":1,"decision":6,"validator":13},"candidate_total":20,"decision_total":52,"findings":[],"status":"passed"}

```

## 新設module・試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/improvement_candidate_writer.py", "tools/development/workflow_ledger_verify.py", "tests/test_improvement_candidate_writer.py", "tests/test_workflow_ledger_verify.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
18cf2f9580613c114fe58294f9d1d2533a01926a8a7baf004d39ae71da479324  tools/development/improvement_candidate_writer.py
efe6f31f6b52691fd54d7906b9714616b660ae0d9915e7bfb697150f6fee549a  tools/development/workflow_ledger_verify.py
c12664e65106a44f62ec8957a969734e7acc44334250d0ea9c2558f79da5661e  tests/test_improvement_candidate_writer.py
efabb75b7058284ffc78abd014a4adc6db463ed3d1e8256c29c9175c56bb5fdb  tests/test_workflow_ledger_verify.py

```
