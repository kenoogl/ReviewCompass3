# 測定ブロック：N7未充足候補4件の是正 受入確認の実測

- captured_at：2026-08-19T06:32:38+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-n7-candidate-remediation-evidence-commands-v1.json`（SHA-256 `43a493803a8c02f7695a05e42a0ba067b252d71bd9279cf33d50e306a5dac43c`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 再生成4件のv3検証器 単独合格

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfrom tools.development import issue_resolution_pilot as pilot\ntargets = [\".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json\"]\nconfig = pilot.load_config(Path('config/development-issue-resolution-pilot-v3.json'))\nfor target in targets:\n    pilot.validate_record_file(target, project_root=Path.cwd(), config=config)\n    print(Path(target).name, 'v3検証器合格')\n"]`
- 実行体：.venv/bin/python3
- exit：1・elapsed：0.033s
- 完全性：二重実行一致

- stderr：

```text
Traceback (most recent call last):
  File "<string>", line 6, in <module>
    pilot.validate_record_file(target, project_root=Path.cwd(), config=config)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/Daily/Development/ReviewCompass3/tools/development/issue_resolution_pilot.py", line 1610, in validate_record_file
    return validate_candidate(
        record,
    ...<2 lines>...
        config=config,
    )
  File "/Users/Daily/Development/ReviewCompass3/tools/development/issue_resolution_pilot.py", line 790, in validate_candidate
    raise PilotValidationError("source reference identity is invalid")
tools.development.issue_resolution_pilot.PilotValidationError: source reference identity is invalid

```

## N7の是正後状態（GREEN・exit 0が合格）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py::test_n7_all_candidate_records_validate_or_are_allowlisted'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.145s
- 完全性：二重実行一致

- stdout：

```text
exit 1
1 failed

```

## 台帳関連試験群の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py',\n     'tests/test_issue_intake_v4.py',\n     'tests/test_issue_resolution_pilot.py',\n     'tests/test_agents_lane_guidance.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.75s
- 完全性：二重実行一致

- stdout：

```text
exit 1
1 failed, 67 passed

```

## 再生成4件のdigest固定

- argv：`["shasum", "-a", "256", ".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
425e4d292f3dcba4df7c388b0c795010e368bcf2ba48f96db4173eefd671c02e  .reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json
dc70a7414f1aad8d5689b981f493b43d1ca3df988974308da65e723bbaa8933f  .reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json
a30f45226c6e3bfb53b614700ab9239039b88d058f90ec336679e558369f8287  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json
be636e417d8afcaadbe591635b0dd3db15fe34a18a950cfe3ae3e2470508e87e  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json

```
