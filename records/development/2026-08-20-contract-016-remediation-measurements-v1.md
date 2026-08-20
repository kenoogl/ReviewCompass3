# 測定ブロック：契約016 terra E2E所見是正のGREEN固定（単独実行の終了コード・件数・digest）

- captured_at：2026-08-20T21:37:17+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-contract-016-remediation-commands-v1.json`（SHA-256 `1ced689075f20e34b88f20ac46cf373c8ea50365d01daadda2ebb7ff3755d303`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## reviewer_launch試験の単独実行（entry exitがpytest自身の終了コード）

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：5.677s
- 完全性：二重実行一致

## request_builder試験の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_request_builder.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：5.12s
- 完全性：二重実行一致

## 運用集計試験（保護対象の互換確認）の単独実行

- argv：`["sh", "-c", "exec .venv/bin/python3 -m pytest tests/test_operational_metrics.py -q -p no:cacheprovider >/dev/null 2>&1"]`
- 実行体：/bin/sh
- exit：0・elapsed：28.963s
- 完全性：二重実行一致

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.114s
- 完全性：二重実行一致

- stdout：

```text
106

```

## 是正成果物・E2E材料のdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/core.py", "docs/development/prompts/reviewer-launch-run.md", "tests/test_reviewer_launch.py", "tools/request_builder/core.py", "records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-request-v1.md", "records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md", "records/development/2026-08-20-contract-016-full-test-receipt-v1.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
04a25bd07c43364dbe6282545e86007c4e22e7c9305ce15c1559104266eeb69c  tools/reviewer_launch/core.py
3acaed33ae9b916f4ca1d15b7c686ae9e089300f21bb8814b320b2f192a9ae8d  docs/development/prompts/reviewer-launch-run.md
690cf31f41b8301419b55955a194375582e53acc86e3704b5461f42ed481f138  tests/test_reviewer_launch.py
ef2d6efcea54aa2bdc2c9e5a3cf9d48e9410747252916afeddae97bfc889a72d  tools/request_builder/core.py
41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc  records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-request-v1.md
ca8c8b5a2404ac0b5760a650f6b04ee7c37a535bb98f955a857498733310132f  records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md
33d68be720f19c2f5c75187e787acdf64da77e37dc6d7a4b54f562fb744d9581  records/development/2026-08-20-contract-016-full-test-receipt-v1.json

```
