# 測定ブロック：review-plan commit既定（対策3）事前走査の実測

- captured_at：2026-08-18T21:09:11+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-review-plan-defaults-prescan-commands-v1.json`（SHA-256 `8696d362450b78e3b5d416fdc64e6d8ccbd438b1c18dac314e965c0d8ef36aa6`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## CLIの引数固定の現状

- argv：`["grep", "-n", "_FLAGS\\|len(_FLAGS)", "tools/development/review_plan_cli.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.002s
- 完全性：二重実行一致

- stdout：

```text
10:_FLAGS = ("base-commit", "target-commit", "risk", "stage", "classification")
14:    if len(arguments) != len(_FLAGS) * 2:
22:        if name not in _FLAGS or name in values:
25:    if set(values) != set(_FLAGS):

```

## commit解決（rev-parse）の実装点

- argv：`["grep", "-n", "rev-parse\\|def _commit", "tools/development/review_plan.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.002s
- 完全性：二重実行一致

- stdout：

```text
58:def _commit(repository, value):
63:        "rev-parse",

```

## 保護試験の基線（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_review_plan.py', '-q'], capture_output=True, text=True)\nprint('exit', r.returncode)\nprint(r.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：1.255s
- 完全性：二重実行一致

- stdout：

```text
exit 0
9 passed

```

## 対象fileのdigest固定

- argv：`["shasum", "-a", "256", "tools/development/review_plan_cli.py", "tests/test_review_plan.py", "docs/development/prompts/review-plan-run.md"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
f9877687c46f1294d5d3f3a4e5e73211b5a4acf2c86c1f91b85276f2138525d0  tools/development/review_plan_cli.py
7bb8ca17506e35d93e3fb41855ef7c6836e401c53ef703265073ab81b389173d  tests/test_review_plan.py
5712357ba17086055a0808a48d9259229cdee0764e4d75e0ff656856709cb0cb  docs/development/prompts/review-plan-run.md

```
