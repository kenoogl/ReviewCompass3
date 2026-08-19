# 測定ブロック：候補writer・台帳一括検証入口 事前走査の実測

- captured_at：2026-08-19T10:57:13+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-ledger-writer-prescan-commands-v1.json`（SHA-256 `58a8015ad471e40540a0c6b6a9e33ae026d3e0cfbf7567a4d9be7c138ad44386`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 台帳の現況（候補・決定・allowlistの件数）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\ncandidates = sorted(Path('.reviewcompass/workflow/improvement-candidates').glob('*.json'))\ndecisions = sorted(Path('.reviewcompass/workflow/triage-decisions-v4').glob('*.json'))\nprint('candidates_json', len(candidates), '(allowlist含む)')\nprint('decisions_v4', len(decisions))\nimport json\nallowlist = json.loads(Path('.reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json').read_text(encoding='utf-8'))\nprint('allowlist_entries', len(allowlist['entries']))\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.02s
- 完全性：二重実行一致

- stdout：

```text
candidates_json 21 (allowlist含む)
decisions_v4 52
allowlist_entries 1

```

## 新設名の衝突なしの機械確認

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfor candidate in (\n    'tools/development/improvement_candidate_writer.py',\n    'tools/development/workflow_ledger_verify.py',\n    'tests/test_improvement_candidate_writer.py',\n    'tests/test_workflow_ledger_verify.py',\n):\n    print(candidate, 'exists', Path(candidate).exists())\nhits = []\nfor base in ('tools', 'tests'):\n    for path in sorted(Path(base).rglob('*.py')):\n        try:\n            text = path.read_text(encoding='utf-8')\n        except (OSError, UnicodeDecodeError):\n            continue\n        if 'workflow_ledger' in text or 'improvement_candidate_writer' in text:\n            hits.append(path.as_posix())\nprint('name_hits', hits)\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.082s
- 完全性：二重実行一致

- stdout：

```text
tools/development/improvement_candidate_writer.py exists False
tools/development/workflow_ledger_verify.py exists False
tests/test_improvement_candidate_writer.py exists False
tests/test_workflow_ledger_verify.py exists False
name_hits ['tests/test_pilot_collaboration.py']

```

## 流用部品と接続先のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/issue_resolution_pilot.py", "tools/development/issue_intake_v4.py", "tools/development/reuse_search_plan.py", "tools/common/digests.py", "config/development-issue-resolution-pilot-v2.json", "config/development-issue-resolution-pilot-v3.json", "config/development-issue-resolution-pilot-v4.json", ".reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json", "tests/test_issue_intake_v4_single_candidate.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.026s
- 完全性：二重実行一致

- stdout：

```text
71e8daebe1a991bde307b0ab9498082218cfef9a6cab6661fa43cb093821f6ef  tools/development/issue_resolution_pilot.py
42b797ad9e1aef81620a94a08c279a99c8daa7924329b44a54da1024cc9f4fde  tools/development/issue_intake_v4.py
2708ad14318a2136c4f5bb5a0ca5e7b15b4f48bf663e0278cca8eb5286073b85  tools/development/reuse_search_plan.py
fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7  tools/common/digests.py
9af4837d968c4088f1ecbaffbf49fc7002667695cd067ee9d8ad33fceaeeb9ff  config/development-issue-resolution-pilot-v2.json
f3130d03805cd78e1622cc20f64df2062c21ba57ea460ef9f9766d132f92d7b9  config/development-issue-resolution-pilot-v3.json
ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e  config/development-issue-resolution-pilot-v4.json
25bf17ae9d53a5a01f370b477c001d6e040a7e1e645e00cb25dbd4caa0043c0a  .reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json
86f0b09864a0def0ed633aa444c1f5317df72d07734e6ac55289d5212bc258e2  tests/test_issue_intake_v4_single_candidate.py

```
