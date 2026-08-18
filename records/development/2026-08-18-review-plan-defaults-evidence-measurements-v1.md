# 測定ブロック：review-plan commit既定（対策3）受入確認の実測

- captured_at：2026-08-18T21:11:57+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-review-plan-defaults-evidence-commands-v1.json`（SHA-256 `3b033c8b54e0933832811803f5ed2d81ffc0fc9d7afb878be54444bba0b90782`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 保護試験11本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_review_plan.py', '-q'], capture_output=True, text=True)\nprint('exit', r.returncode)\nprint(r.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：1.495s
- 完全性：二重実行一致

- stdout：

```text
exit 0
11 passed

```

## 手順書のtarget-commit placeholder残存検索（該当なし＝exit 1が合格）

- argv：`["grep", "-n", "target-commit <", "docs/development/prompts/review-plan-run.md"]`
- 実行体：/usr/bin/grep
- exit：1・elapsed：0.002s
- 完全性：二重実行一致

## 変更fileのdigest固定

- argv：`["shasum", "-a", "256", "tools/development/review_plan_cli.py", "tests/test_review_plan.py", "docs/development/prompts/review-plan-run.md"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.008s
- 完全性：二重実行一致

- stdout：

```text
b0ddafc68e5bf7ff59a3b22a6a405abf8d6fe7970d13424e23bed7567f6a17e7  tools/development/review_plan_cli.py
983a839dea25ccc5a7bd1a594d84eef2fda60de5b5004cd31a61d104d7d67202  tests/test_review_plan.py
232154bc4a37e5672a0d3250b54bdb429aa98d3f78109a07e745f1159b28bde8  docs/development/prompts/review-plan-run.md

```
