# 測定ブロック：既定値化の横展開 事前走査の補助実測（digest・既存試験の固定点）

- captured_at：2026-08-18T19:48:06+09:00
- 宣言file：`records/development/2026-08-18-cli-defaults-rollout-prescan-commands-v2.json`（SHA-256 `d38a90266d156dad9fc4225cf9db8cf29901ad145bab5dfb62d89d569558f151`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止）

## 対象2fileのdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/entry.py", "tools/request_builder/entry.py", "docs/development/prompts/reviewer-launch-run.md", "docs/development/prompts/request-builder-run.md"]`
- exit：0・elapsed：0.015s

- stdout：

```text
0b7f569aae8f8b7f1b0668fcab3f9024ed3571d131e5cbb7fe3dc89bb61ff1db  tools/reviewer_launch/entry.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
e348964e16cd839ba795801e057f386dec0107cd727326a8c4a818fc79b65cbb  docs/development/prompts/reviewer-launch-run.md
f24ee5d47dfe6a4ccfe0d6323adbc0115227265dc5f67962ba693b08dd03ed11  docs/development/prompts/request-builder-run.md

```

## reviewer_launch試験の引数欠落固定点

- argv：`["grep", "-n", "invalid_arguments\\|private-root\\|--repository", "tests/test_reviewer_launch.py"]`
- exit：0・elapsed：0.003s

- stdout：

```text
1371:            "--repository",
1377:            "--private-root",

```

## request_builder試験の引数欠落固定点

- argv：`["grep", "-n", "invalid_arguments\\|--date\\|--repository", "tests/test_request_builder.py"]`
- exit：0・elapsed：0.002s

- stdout：

```text
595:            "--repository",
599:            "--date",
619:            "--repository",

```
