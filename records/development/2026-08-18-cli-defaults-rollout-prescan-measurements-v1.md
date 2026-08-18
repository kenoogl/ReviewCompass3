# 測定ブロック：既定値化の横展開（reviewer-launch・request-builder）事前走査の実測

- captured_at：2026-08-18T19:46:13+09:00
- 宣言file：`records/development/2026-08-18-cli-defaults-rollout-prescan-commands-v1.json`（SHA-256 `422c224f0619b692d673892835f4215fdf3914fb3303833c3203532a49470fb6`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止）

## reviewer_launchの引数定義の所在

- argv：`["grep", "-rn", "add_argument", "tools/reviewer_launch/"]`
- exit：1・elapsed：0.004s

## request_builderの引数定義の所在

- argv：`["grep", "-rn", "add_argument", "tools/request_builder/"]`
- exit：1・elapsed：0.003s

## reviewer_launchのprivate_root既定の現状

- argv：`["grep", "-rn", "private_root", "tools/reviewer_launch/entry.py"]`
- exit：0・elapsed：0.003s

- stdout：

```text
tools/reviewer_launch/entry.py:134:        private_root=values["--private-root"],

```

## request_builderのdate・repository受け取りの現状

- argv：`["grep", "-rn", "date\\|repository", "tools/request_builder/entry.py"]`
- exit：0・elapsed：0.002s

- stdout：

```text
tools/request_builder/entry.py:42:    values.update(lists)
tools/request_builder/entry.py:64:            repository=values["--input-root"],
tools/request_builder/entry.py:89:            ("--repository", "--type", "--date", "--slug", "--title"),
tools/request_builder/entry.py:97:                repository=values["--repository"],
tools/request_builder/entry.py:99:                record_date=values["--date"],
tools/request_builder/entry.py:114:            selected_arguments[1:], ("--repository", "--request")
tools/request_builder/entry.py:121:                repository=values["--repository"],

```

## 両CLIの保護試験fileの一覧

- argv：`["grep", "-rln", "reviewer_launch\\|request_builder", "tests/"]`
- exit：0・elapsed：0.123s

- stdout：

```text
tests/test_reviewer_launch.py
tests/__pycache__/test_request_builder.cpython-313-pytest-8.4.2.pyc
tests/__pycache__/test_rq2_paired_trial.cpython-313-pytest-8.4.2.pyc
tests/__pycache__/test_reviewer_bridge.cpython-313-pytest-8.4.2.pyc
tests/__pycache__/test_reviewer_launch.cpython-313-pytest-8.4.2.pyc
tests/test_reviewer_bridge.py
tests/test_request_builder.py
tests/test_rq2_paired_trial.py

```

## 私有領域の実run-id命名の実態

- argv：`["ls", "/Users/keno/.reviewcompass3-private/reviewer-launch"]`
- exit：0・elapsed：0.003s

- stdout：

```text
cr-011-001
cr-012-001
cr-012-002
cr-013-001
cr-013-002
cr-014-001
e2e-010-001
e2e-010-002
e2e-010-003
e2e-010-004
e2e-010-005
e2e-010-006
e2e-010-007
e2e-011-001
e2e-011-002
e2e-012-001
e2e-012-002
e2e-013-001
rq2-case-008-b
rq2b2-case-001-a1
rq2b2-case-001-a2
rq2b2-case-001-b
rq2b2-case-001-c
rq2b2-case-001-d
rq2b2-case-002-b
rq2b2-case-002-c
rq2b2-case-003-b
rq2b2-case-003-c
rq2b2-case-004-a1
rq2b2-case-004-a2
rq2b2-case-004-b
rq2b2-case-004-c
rq2b2-case-005-b
rq2b2-case-005-c
rq2b2-case-006-b
rq2b2-case-006-c
rq2b2-case-007-b
rq2b2-case-007-c
rq2b2-case-008-a1
rq2b2-case-008-a2
rq2b2-case-008-b
rq2b2-case-008-c
rq2b2-case-009-b
rq2b2-case-009-c
rq2b2-case-010-b
rq2b2-case-010-c
rq2b2r-case-002-c
rq2b2r-case-009-b

```
