# 測定ブロック：read_only_entry終了コード統合 受入確認の実測

- captured_at：2026-08-19T00:16:50+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-read-only-entry-exit-code-unification-evidence-commands-v1.json`（SHA-256 `b73cf446c86efa0bed687c950d7e37dd241c09330fbc868da8281aa0467497b4`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## session系全試験の機械列挙実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nfrom pathlib import Path\nfiles = sorted(\n    str(path)\n    for pattern in (\n        'test_session_log*.py',\n        'test_session_artifact*.py',\n        'test_redaction*.py',\n        'test_session_bootstrap_e2e.py',\n    )\n    for path in Path('tests').glob(pattern)\n)\nprint('files', len(files))\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q', *files],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：3.08s
- 完全性：二重実行一致

- stdout：

```text
files 53
exit 0
348 passed

```

## 統合後の3入口の終了コード定数行（語彙一致の機械転記）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\ntargets = (\n    'tools/session_logs/cli.py',\n    'tools/session_logs/read_only_entry.py',\n    'tools/session_logs/eventual_preservation.py',\n)\nfor target in targets:\n    print(target)\n    for number, line in enumerate(\n        Path(target).read_text(encoding='utf-8').splitlines(), start=1\n    ):\n        stripped = line.strip()\n        if stripped.startswith('EXIT_') and '=' in stripped:\n            print(' ', number, stripped)\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.018s
- 完全性：二重実行一致

- stdout：

```text
tools/session_logs/cli.py
  39 EXIT_OK = 0
  40 EXIT_SENSITIVE_DATA = 2
  41 EXIT_NO_TARGETS = 3
  42 EXIT_UNSUPPORTED = 4
  43 EXIT_FAILED = 5
  44 EXIT_PRESERVATION_FAILED = 6
  45 EXIT_VERIFICATION_MISMATCH = 7
  46 EXIT_REGENERATION_FAILED = 8
  47 EXIT_RESTORE_PRESERVED = 9
  48 EXIT_RESTORE_INTEGRITY_FAILED = 10
tools/session_logs/read_only_entry.py
  24 EXIT_OK = 0
  25 EXIT_UNSUPPORTED = 4
  26 EXIT_FAILED = 5
tools/session_logs/eventual_preservation.py
  34 EXIT_OK = 0
  35 EXIT_UNSUPPORTED = 4
  36 EXIT_FAILED = 5

```

## 変更fileと消費側のdigest固定

- argv：`["shasum", "-a", "256", "tools/session_logs/read_only_entry.py", "tools/session_logs/safe_storage_entry.py", "tests/test_session_log_read_only_entry.py", "tests/test_session_artifact_safe_storage_entry.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.013s
- 完全性：二重実行一致

- stdout：

```text
6e3fffb0c5c7254ef773997860941d820bfad92180c195a1e5a74b9b3f99948f  tools/session_logs/read_only_entry.py
a67a36927ab751616437c2cf5d5abd50436026490fdc2a3e08c93abf53ee66ce  tools/session_logs/safe_storage_entry.py
6659793b9274a6d63e5f42fb6b23953991b8ade6d6c54ed5f698da062b2ae292  tests/test_session_log_read_only_entry.py
20bf269a751aa624cd2cd9dd3629c418f4275c8f20aab8b2107bb8a4471a1247  tests/test_session_artifact_safe_storage_entry.py

```

## RQ2封緘材料の無変更（tracked差分なし＝出力空が合格）

- argv：`["git", "diff", "--name-only", "--", "docs/evaluation/rq2-cases", "records/development/2026-08-17-rq2-case-answer-key-v2.md"]`
- 実行体：/usr/bin/git
- exit：0・elapsed：0.009s
- 完全性：二重実行一致
