# 測定ブロック：契約015 GREEN固定v2（C15-REVIEW-001是正：合否は単独実行の終了コードで確定・連結なし）

- captured_at：2026-08-20T19:05:53+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-contract-015-green-commands-v2.json`（SHA-256 `709012b0be9a0cf09a0f039987c57df7f4689c7a23000c32988f82aefcc3e5a4`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## reviewer_launch試験の単独実行（entry exitがpytest自身の終了コード）

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：6.878s
- 完全性：二重実行一致

## request_builder試験（契約011対象）の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_request_builder.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：4.091s
- 完全性：二重実行一致

## G30契約操作試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_operation_contract_run.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.294s
- 完全性：二重実行一致

## RQ2装置試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_rq2_paired_trial.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.784s
- 完全性：二重実行一致

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.109s
- 完全性：二重実行一致

- stdout：

```text
94

```

## request_builder試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.107s
- 完全性：二重実行一致

- stdout：

```text
42

```

## G30契約操作試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_operation_contract_run.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.103s
- 完全性：二重実行一致

- stdout：

```text
75

```

## RQ2装置試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_rq2_paired_trial.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.098s
- 完全性：二重実行一致

- stdout：

```text
14

```

## 起動核のname分岐消滅の固定点（0が期待値・shell非経由）

- argv：`[".venv/bin/python3", "-c", "print(open('tools/reviewer_launch/core.py',encoding='utf-8').read().count('backend_name == '))"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.017s
- 完全性：二重実行一致

- stdout：

```text
0

```

## 生成promptのgolden digest再計算（是正後）

- argv：`[".venv/bin/python3", "-c", "from tools.reviewer_launch.core import build_prompt\nimport hashlib\nfor tool in ('view_file','Read'):\n    p=build_prompt('/repo-fixed','records/session-handoffs/fixed-request-v1.md','a'*64,read_tool_name=tool)\n    print(tool, len(p.encode('utf-8')), hashlib.sha256(p.encode('utf-8')).hexdigest())\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.033s
- 完全性：二重実行一致

- stdout：

```text
view_file 1528 79c2cdee58e9425d35704a770f730a7adf15c198d12693e5bf18c89ed9607845
Read 1523 40dd4f19c2c4e1ffec43bbed94c36e0a23c2704bdf56dbc94fc3c1df8a60c511

```

## 契約§6保護対象の基準commitからの差分file一覧（空が期待値）

- argv：`["git", "diff", "--name-only", "91e0dcd..HEAD", "--", "tools/request_builder", "tools/bootstrap", "tools/session_logs", "tools/common/digests.py", "tools/development/claude_implementation_*", "tools/egress", "tools/external_review/send.py", "tools/operations/operation_contract_run.py", "tools/evaluation/rq2_paired_trial.py", "tests/test_request_builder.py"]`
- 実行体：/usr/bin/git
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

## 成果物・受入材料のdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py", "tests/test_reviewer_launch.py", "docs/development/prompts/reviewer-launch-run.md", "records/development/2026-08-20-contract-015-red-replay-output.txt", "records/development/2026-08-20-contract-015-full-test-receipt-v1.json", "records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.014s
- 完全性：二重実行一致

- stdout：

```text
88d3dab9bebafc87a7a3757c8216710f7517cffe4b6101fca6d4cb08b1ab2684  tools/reviewer_launch/core.py
946e5fc4291ee9cb8f6ae179a11017d87e7b95da5848f5e1a436b13b276f6f9d  tools/reviewer_launch/entry.py
c7c5364ab72f5097557a00f086fdcc0cc5c555bb93bc1cfb5186645af8a04330  tests/test_reviewer_launch.py
8cf52d9f7dc0d9f70d93b34035deeaad65a72ebe58372be037d906133ec65cd0  docs/development/prompts/reviewer-launch-run.md
7171d84387ba763dc281fecf9de9798c114cbaffb35ae1b55a77dbbe35d167a1  records/development/2026-08-20-contract-015-red-replay-output.txt
65bca4012690d85beb84a260e91767ecc0cda4a8a171bfcb104a614d1d0e7446  records/development/2026-08-20-contract-015-full-test-receipt-v1.json
2880a7541502ead6d581205eb67d95a656e4d1487323819e98c497e3e7ddc6c8  records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md

```
