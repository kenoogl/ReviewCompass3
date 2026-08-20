# 測定ブロック：契約015 GREEN固定（対象・関連試験の件数と終了コード・分岐消滅固定点・成果物digest）

- captured_at：2026-08-20T18:54:49+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-contract-015-green-commands-v1.json`（SHA-256 `20441bd6bdf6a30584afc5c5ff71a5b6000c7faa3ff78271ad1b7dde5e0b7bdd`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.111s
- 完全性：二重実行一致

- stdout：

```text
91

```

## reviewer_launch試験の単独終了コード射影

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q -p no:cacheprovider >/dev/null 2>&1; echo exit=$?"]`
- 実行体：/bin/sh
- exit：0・elapsed：4.801s
- 完全性：二重実行一致

- stdout：

```text
exit=0

```

## request_builder試験（契約011対象）の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.119s
- 完全性：二重実行一致

- stdout：

```text
42

```

## request_builder試験の単独終了コード射影

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py -q -p no:cacheprovider >/dev/null 2>&1; echo exit=$?"]`
- 実行体：/bin/sh
- exit：0・elapsed：4.241s
- 完全性：二重実行一致

- stdout：

```text
exit=0

```

## G30契約操作試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_operation_contract_run.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.14s
- 完全性：二重実行一致

- stdout：

```text
75

```

## G30契約操作試験の単独終了コード射影

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_operation_contract_run.py -q -p no:cacheprovider >/dev/null 2>&1; echo exit=$?"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.252s
- 完全性：二重実行一致

- stdout：

```text
exit=0

```

## RQ2装置試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_rq2_paired_trial.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.115s
- 完全性：二重実行一致

- stdout：

```text
14

```

## RQ2装置試験の単独終了コード射影

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_rq2_paired_trial.py -q -p no:cacheprovider >/dev/null 2>&1; echo exit=$?"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.848s
- 完全性：二重実行一致

- stdout：

```text
exit=0

```

## 起動核のname分岐消滅の固定点（0が期待値）

- argv：`["sh", "-c", "grep -c 'backend_name == ' tools/reviewer_launch/core.py || true"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.006s
- 完全性：二重実行一致

- stdout：

```text
0

```

## 生成promptのgolden digest再計算（改修後）

- argv：`[".venv/bin/python3", "-c", "from tools.reviewer_launch.core import build_prompt\nimport hashlib\nfor tool in ('view_file','Read'):\n    p=build_prompt('/repo-fixed','records/session-handoffs/fixed-request-v1.md','a'*64,read_tool_name=tool)\n    print(tool, len(p.encode('utf-8')), hashlib.sha256(p.encode('utf-8')).hexdigest())\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.034s
- 完全性：二重実行一致

- stdout：

```text
view_file 1528 79c2cdee58e9425d35704a770f730a7adf15c198d12693e5bf18c89ed9607845
Read 1523 40dd4f19c2c4e1ffec43bbed94c36e0a23c2704bdf56dbc94fc3c1df8a60c511

```

## 変更成果物のdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py", "tests/test_reviewer_launch.py", "docs/development/prompts/reviewer-launch-run.md"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.013s
- 完全性：二重実行一致

- stdout：

```text
88d3dab9bebafc87a7a3757c8216710f7517cffe4b6101fca6d4cb08b1ab2684  tools/reviewer_launch/core.py
946e5fc4291ee9cb8f6ae179a11017d87e7b95da5848f5e1a436b13b276f6f9d  tools/reviewer_launch/entry.py
0443c38e61880e6c330f7c38182390df900f53cea174a655132c6a3dee361866  tests/test_reviewer_launch.py
8cf52d9f7dc0d9f70d93b34035deeaad65a72ebe58372be037d906133ec65cd0  docs/development/prompts/reviewer-launch-run.md

```
