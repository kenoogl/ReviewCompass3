# 測定ブロック：契約016 GREEN固定（単独実行の終了コード・収集件数・保護対象差分・成果物digest）

- captured_at：2026-08-20T21:14:22+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-contract-016-green-commands-v1.json`（SHA-256 `6c23587fd933c373b725dff8e9ed842af80259b92265ec8a0e57fef407ff17bf`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## reviewer_launch試験の単独実行（entry exitがpytest自身の終了コード）

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：5.805s
- 完全性：二重実行一致

## request_builder試験（契約011対象）の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_request_builder.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：5.074s
- 完全性：二重実行一致

## G30契約操作試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_operation_contract_run.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.236s
- 完全性：二重実行一致

## RQ2装置試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_rq2_paired_trial.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.777s
- 完全性：二重実行一致

## RQ2運搬部品試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_reviewer_bridge.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.612s
- 完全性：二重実行一致

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.108s
- 完全性：二重実行一致

- stdout：

```text
105

```

## request_builder試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.103s
- 完全性：二重実行一致

- stdout：

```text
51

```

## G30・RQ2装置・運搬部品の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_operation_contract_run.py tests/test_rq2_paired_trial.py tests/test_reviewer_bridge.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.12s
- 完全性：二重実行一致

- stdout：

```text
93

```

## 契約§6保護対象の基準commit（候補v2固定）からの差分file一覧（空が期待値）

- argv：`["git", "diff", "--name-only", "3eab124..HEAD", "--", "tools/reviewer_launch/record.py", "tools/bootstrap", "tools/session_logs", "tools/common/digests.py", "tools/development/claude_implementation_*", "tools/egress", "tools/external_review/send.py", "tools/operations/operation_contract_run.py", "tools/evaluation"]`
- 実行体：/usr/bin/git
- exit：0・elapsed：0.01s
- 完全性：二重実行一致

## 成果物・受入材料のdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py", "tools/request_builder/core.py", "tools/request_builder/entry.py", "tests/test_reviewer_launch.py", "tests/test_request_builder.py", "docs/development/prompts/request-builder-run.md", "docs/development/prompts/reviewer-launch-run.md", "records/development/2026-08-20-contract-016-red-replay-output.txt"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.013s
- 完全性：二重実行一致

- stdout：

```text
62babeef27dd9f634a7f35851bc32ff1c9596b42836b78a19227a2faa61f7b3a  tools/reviewer_launch/core.py
ccaa9b96f1e27d30e014b67cfefb3a17978c6c5c5106def82b95d2a4c438f151  tools/reviewer_launch/entry.py
31446cdc28e6193fd17663a98f04b588ef2d59841c2a99274f71441ba065e97e  tools/request_builder/core.py
b6eb4c86b61f82e989a0a308041270b749a41b4982a3347a7fc27268054035f7  tools/request_builder/entry.py
4906692f2f754df02f59402d98345c6fade1b26a80fc17fced6eccf2e5134c9a  tests/test_reviewer_launch.py
f1b199710ab389e74f95cf2355e72b3fad2c36d219a1af9e16783309e8c6f9d5  tests/test_request_builder.py
247ffdcbead83f428b5b8cd083c2fb79502dd3d620b2c6caba01d709698bbeec  docs/development/prompts/request-builder-run.md
1c80a85ec584453dbaa522704b870b615ad72e8b15f5e672fa8caafbbe5643fd  docs/development/prompts/reviewer-launch-run.md
fec327341cc852eae30b533ec5b8e9c1db9792d0dcb84f84ff9e149dc02ddc6b  records/development/2026-08-20-contract-016-red-replay-output.txt

```
