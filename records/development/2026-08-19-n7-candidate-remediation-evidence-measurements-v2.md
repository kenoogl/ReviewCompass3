# 測定ブロック：N7未充足候補4件の是正 受入確認の実測

- captured_at：2026-08-19T06:33:58+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-n7-candidate-remediation-evidence-commands-v1.json`（SHA-256 `43a493803a8c02f7695a05e42a0ba067b252d71bd9279cf33d50e306a5dac43c`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 再生成4件のv3検証器 単独合格

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfrom tools.development import issue_resolution_pilot as pilot\ntargets = [\".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json\"]\nconfig = pilot.load_config(Path('config/development-issue-resolution-pilot-v3.json'))\nfor target in targets:\n    pilot.validate_record_file(target, project_root=Path.cwd(), config=config)\n    print(Path(target).name, 'v3検証器合格')\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.033s
- 完全性：二重実行一致

- stdout：

```text
ic-contract-014-canonical-sequence-gaps-001--v1.json v3検証器合格
ic-launch-metrics-acceptance-title-001--v1.json v3検証器合格
ic-session-log-exit-code-doc-drift-001--v1.json v3検証器合格
ic-session-log-exit-code-vocabulary-001--v1.json v3検証器合格

```

## N7の是正後状態（GREEN・exit 0が合格）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py::test_n7_all_candidate_records_validate_or_are_allowlisted'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.154s
- 完全性：二重実行一致

- stdout：

```text
exit 0
1 passed

```

## 台帳関連試験群の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py',\n     'tests/test_issue_intake_v4.py',\n     'tests/test_issue_resolution_pilot.py',\n     'tests/test_agents_lane_guidance.py'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.335s
- 完全性：二重実行一致

- stdout：

```text
exit 0
68 passed

```

## 再生成4件のdigest固定

- argv：`["shasum", "-a", "256", ".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.013s
- 完全性：二重実行一致

- stdout：

```text
16f4848b34e2f71b685a4bdcb034c8347f5e0d8979f55cc653b87c5b3b5757e6  .reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json
6228350363549d0d6b1c003dcaa607b3515712bafcb3eb33e695519e8fe46b66  .reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json
e10fde4138d39f7470a22938954dd43197ea373e997bdf502f262546110855cd  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json
308578394f60f8e1d9c2669141584edf83b995e44e4351fc5d0a927431bd32e9  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json

```
