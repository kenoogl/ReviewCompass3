# 測定ブロック：復路writer（決定・issue登録・状態遷移）受入確認の実測

- captured_at：2026-08-19T11:26:20+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-return-path-writers-evidence-commands-v1.json`（SHA-256 `c9cba620f5dfdddc2a7999185e47ef61c27841b7872bbe984a464f19e7dd6407`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## writer系試験22本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_triage_decision_writer.py',\n     'tests/test_issue_record_writer.py',\n     'tests/test_issue_state_transition.py',\n     'tests/test_workflow_ledger_verify.py',\n     'tests/test_improvement_candidate_writer.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.384s
- 完全性：二重実行一致

- stdout：

```text
exit 0
22 passed

```

## 台帳関連試験群の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py',\n     'tests/test_issue_intake_v4.py',\n     'tests/test_issue_resolution_pilot.py',\n     'tests/test_agents_lane_guidance.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.337s
- 完全性：二重実行一致

- stdout：

```text
exit 0
68 passed

```

## 実repoでの一括検証（issue勘定を含む・exit 0が合格）

- argv：`[".venv/bin/python3", "-m", "tools.development.workflow_ledger_verify"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.053s
- 完全性：二重実行一致

- stdout：

```text
{"accounted":{"allowlist":1,"decision":6,"validator":13},"candidate_total":20,"decision_total":52,"findings":[],"issue_states":{"registered":8},"issue_total":8,"status":"passed"}

```

## 新設・拡張moduleと試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/triage_decision_writer.py", "tools/development/issue_record_writer.py", "tools/development/issue_state_transition.py", "tools/development/workflow_ledger_verify.py", "tests/test_triage_decision_writer.py", "tests/test_issue_record_writer.py", "tests/test_issue_state_transition.py", "tests/test_workflow_ledger_verify.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
f46b01da49bbbac2c80a4accb545237dc88c3c9bb8394da6961b6ace272a5e9a  tools/development/triage_decision_writer.py
a99ed107a9f90b6e4e9ddeeac7283211c43a372039efb3b394bb443da18ace83  tools/development/issue_record_writer.py
e2ec4c3a3c4d6926d55c30cdb14e62de4b0047abf30060be405aca52d5f66526  tools/development/issue_state_transition.py
81a8a72b56edaced0901c57263319c9dcac1bc2e581c0f6d9837cfa65b0b5174  tools/development/workflow_ledger_verify.py
6a20d008fcb12ada1307ca04f80e058d28c0c80a768bc2b768979276dbc51137  tests/test_triage_decision_writer.py
b2f18f3b2195b48ed439b91d5d73fb81dca13089d662f4927254ee1aa7d40605  tests/test_issue_record_writer.py
efba4e000798c968dbe85635dd132e46242c0ab65126f775f662440afce4cec1  tests/test_issue_state_transition.py
c194b23b52f7d6f85bf1337457dd7ac7361ee0ac221f5dfd2b2c36759227a2ae  tests/test_workflow_ledger_verify.py

```
