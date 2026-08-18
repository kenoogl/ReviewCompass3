# 測定ブロック：read_only_entry終了コード統合 事前走査の実測

- captured_at：2026-08-19T00:11:17+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-read-only-entry-exit-code-unification-prescan-commands-v1.json`（SHA-256 `ddfdaea83e7d7dfdcc960ac9d90f88741fb36e06f6a76e3f115e946295c49108`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 対象・消費側・保護試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/session_logs/read_only_entry.py", "tools/session_logs/safe_storage_entry.py", "tools/session_logs/cli.py", "tools/session_logs/eventual_preservation.py", "tests/test_session_log_read_only_entry.py", "tests/test_session_artifact_safe_storage_entry.py", "tests/test_session_log_record_run.py", "tests/test_session_log_eventual_preservation.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.01s
- 完全性：二重実行一致

- stdout：

```text
7d731d0c6304e4dc0e1d2a706adfabb757981822c1506914000736b99e1f7871  tools/session_logs/read_only_entry.py
a67a36927ab751616437c2cf5d5abd50436026490fdc2a3e08c93abf53ee66ce  tools/session_logs/safe_storage_entry.py
ff1f3ebdb829eff58b60c60194ac891786a433af7a4d3df3cca153b05a200443  tools/session_logs/cli.py
4fa0d87173c094a766c8d2f6021a5a9db17920b32dfdb7acb9b879601ceb5342  tools/session_logs/eventual_preservation.py
0dd4d70123deb0a8d12284d58fbe74d905d2e2d8e48c2032f55cec77d2d9e940  tests/test_session_log_read_only_entry.py
e7c8cc8295acdaff7ac58108a010b420d84ee6c4a26bfb51f5eb571cefcc2012  tests/test_session_artifact_safe_storage_entry.py
3a7ae96195de6466f4189c54cdcf8076e7bc495d30ca29c28953fee15792fa3d  tests/test_session_log_record_run.py
dd782bb3f02988f11e1b1abb1c963b7a2ccc6af908ceef324fd92ca3bbaaffef  tests/test_session_log_eventual_preservation.py

```

## 4入口の終了コード定数行（現状の語彙の機械転記）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\ntargets = (\n    'tools/session_logs/cli.py',\n    'tools/session_logs/read_only_entry.py',\n    'tools/session_logs/eventual_preservation.py',\n    'tools/session_logs/safe_storage_entry.py',\n)\nfor target in targets:\n    print(target)\n    for number, line in enumerate(\n        Path(target).read_text(encoding='utf-8').splitlines(), start=1\n    ):\n        stripped = line.strip()\n        if stripped.startswith('EXIT_') and '=' in stripped:\n            print(' ', number, stripped)\n"]`
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
  25 EXIT_PARTIAL = 3
  26 EXIT_STOPPED = 4
tools/session_logs/eventual_preservation.py
  34 EXIT_OK = 0
  35 EXIT_UNSUPPORTED = 4
  36 EXIT_FAILED = 5
tools/session_logs/safe_storage_entry.py
  18 EXIT_OK = 0
  19 EXIT_STOPPED = 4

```

## read_only_entryの参照元（Pythonのみ・機械列挙）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfor base in ('tools', 'tests'):\n    for path in sorted(Path(base).rglob('*.py')):\n        try:\n            text = path.read_text(encoding='utf-8')\n        except (OSError, UnicodeDecodeError):\n            continue\n        if 'read_only_entry' in text:\n            print(path.as_posix())\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.03s
- 完全性：二重実行一致

- stdout：

```text
tools/session_logs/safe_storage.py
tools/session_logs/safe_storage_entry.py
tests/test_session_artifact_safe_storage.py
tests/test_session_log_read_only_entry.py

```

## 終了コード値へ結合した箇所の機械計数

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\ntargets = {\n    'tests/test_session_log_read_only_entry.py': (\n        'expected_exit',\n        'exit_code == 3',\n        'exit_code == 4',\n        'exit_code == 5',\n    ),\n    'tests/test_session_artifact_safe_storage_entry.py': (\n        '(3, \\x22partial\\x22)',\n        '(4, \\x22stopped\\x22)',\n        'exit_code == 4',\n        'source_exit_code != ',\n    ),\n    'tools/session_logs/safe_storage_entry.py': (\n        'source_exit_code != EXIT_OK',\n        'exit_code = 3',\n        'EXIT_STOPPED = 4',\n    ),\n}\nfor target, patterns in targets.items():\n    text = Path(target).read_text(encoding='utf-8')\n    print(target)\n    for pattern in patterns:\n        print(' ', repr(pattern), text.count(pattern))\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.017s
- 完全性：二重実行一致

- stdout：

```text
tests/test_session_log_read_only_entry.py
  'expected_exit' 3
  'exit_code == 3' 1
  'exit_code == 4' 3
  'exit_code == 5' 0
tests/test_session_artifact_safe_storage_entry.py
  '(3, "partial")' 1
  '(4, "stopped")' 1
  'exit_code == 4' 2
  'source_exit_code != ' 0
tools/session_logs/safe_storage_entry.py
  'source_exit_code != EXIT_OK' 1
  'exit_code = 3' 1
  'EXIT_STOPPED = 4' 1

```
