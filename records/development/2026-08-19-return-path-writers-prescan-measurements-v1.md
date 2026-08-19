# 測定ブロック：復路writer（決定・issue・状態遷移）事前走査の実測

- captured_at：2026-08-19T11:20:26+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-return-path-writers-prescan-commands-v1.json`（SHA-256 `4da54542daac8670063d9ef269aa8b38f805621e02752adf6f0c970eca471be4`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## intake既存API（build・validate関数の機械列挙）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\ntext = Path('tools/development/issue_intake_v4.py').read_text(encoding='utf-8')\nfor line in text.splitlines():\n    if line.startswith('def build_') or line.startswith('def validate_'):\n        print(line.split('(')[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.019s
- 完全性：二重実行一致

- stdout：

```text
def validate_issue_record
def validate_issue_set
def build_root_cause_candidate
def validate_root_cause_candidate
def build_intake_candidate
def build_human_triage_decision
def validate_human_triage_decision
def validate_triage_decision_repository
def build_v4_issue_record
def validate_v4_issue_record
def validate_v4_issue_repository
def build_todo_projection
def validate_todo_projection

```

## v4のissue状態語彙・欄・置き場

- argv：`[".venv/bin/python3", "-c", "import json\nconfig = json.load(open('config/development-issue-resolution-pilot-v4.json', encoding='utf-8'))\nprint('issue_states', config['issue_states'])\nprint('active', config['active_issue_states'], 'terminal', config['terminal_issue_states'])\nprint('maximum_active_issues', config['maximum_active_issues'])\nprint('issue_record_v2_fields', config['issue_record_v2']['record_fields'])\nprint('issue_dir', config['directories']['issue_record_v2'])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.017s
- 完全性：二重実行一致

- stdout：

```text
issue_states ['registered', 'untriaged', 'deferred', 'in_progress', 'suspended', 'resolved', 'rejected']
active ['in_progress'] terminal ['resolved', 'rejected']
maximum_active_issues 1
issue_record_v2_fields ['record_kind', 'schema_version', 'issue_id', 'issue_version', 'created_at', 'state', 'problem', 'candidate_ref', 'triage_decision_ref', 'content_digest']
issue_dir .reviewcompass/workflow/issues-v4

```

## verdict検証器の不在の機械確認

- argv：`[".venv/bin/python3", "-c", "import json\nfrom pathlib import Path\nfor name in ('config/development-issue-resolution-pilot-v2.json', 'config/development-issue-resolution-pilot-v3.json', 'config/development-issue-resolution-pilot-v4.json'):\n    config = json.loads(Path(name).read_text(encoding='utf-8'))\n    fields = config.get('record_fields', {}) or {}\n    print(name.rsplit('-', 1)[-1], 'verdict_fields', fields.get('issue_resolution_verdict'), '| resolution_verdict' in json.dumps(config))\ntext = Path('tools/development/issue_resolution_pilot.py').read_text(encoding='utf-8')\nprint('dispatch_has_resolution_verdict', 'resolution_verdict' in text)\nold = json.loads(Path('.reviewcompass/workflow/resolution-verdicts/verdict-pilot-todo-growth-001--v1.json').read_text(encoding='utf-8'))\nprint('old_verdict_record_kind', old['record_kind'])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.018s
- 完全性：二重実行一致

- stdout：

```text
v2.json verdict_fields None False
v3.json verdict_fields None False
v4.json verdict_fields None False
dispatch_has_resolution_verdict False
old_verdict_record_kind resolution_verdict

```

## 新設名の衝突なしの機械確認

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfor candidate in (\n    'tools/development/triage_decision_writer.py',\n    'tools/development/issue_record_writer.py',\n    'tools/development/issue_state_transition.py',\n    'tests/test_triage_decision_writer.py',\n    'tests/test_issue_record_writer.py',\n    'tests/test_issue_state_transition.py',\n):\n    print(candidate, 'exists', Path(candidate).exists())\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.017s
- 完全性：二重実行一致

- stdout：

```text
tools/development/triage_decision_writer.py exists False
tools/development/issue_record_writer.py exists False
tools/development/issue_state_transition.py exists False
tests/test_triage_decision_writer.py exists False
tests/test_issue_record_writer.py exists False
tests/test_issue_state_transition.py exists False

```

## 流用部品のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/issue_intake_v4.py", "tools/development/issue_resolution_pilot.py", "tools/development/improvement_candidate_writer.py", "tools/development/workflow_ledger_verify.py", "config/development-issue-resolution-pilot-v4.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
42b797ad9e1aef81620a94a08c279a99c8daa7924329b44a54da1024cc9f4fde  tools/development/issue_intake_v4.py
71e8daebe1a991bde307b0ab9498082218cfef9a6cab6661fa43cb093821f6ef  tools/development/issue_resolution_pilot.py
18cf2f9580613c114fe58294f9d1d2533a01926a8a7baf004d39ae71da479324  tools/development/improvement_candidate_writer.py
efe6f31f6b52691fd54d7906b9714616b660ae0d9915e7bfb697150f6fee549a  tools/development/workflow_ledger_verify.py
ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e  config/development-issue-resolution-pilot-v4.json

```
