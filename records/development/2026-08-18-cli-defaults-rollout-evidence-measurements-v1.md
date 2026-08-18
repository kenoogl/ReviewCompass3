# 測定ブロック：既定値化の横展開 受入確認の実測（GREEN・既定値・placeholder残存・digest）

- captured_at：2026-08-18T19:53:18+09:00
- 宣言file：`records/development/2026-08-18-cli-defaults-rollout-evidence-commands-v1.json`（SHA-256 `2a700bc224cef78afc96aef196d821ffcbe03756989205e8906e4096696059a7`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止）

## reviewer_launch試験の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_reviewer_launch.py", "-q"]`
- exit：0・elapsed：4.287s

- stdout：

```text
......................................................................   [100%]
70 passed in 4.02s

```

## request_builder試験の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_request_builder.py", "-q"]`
- exit：0・elapsed：4.59s

- stdout：

```text
..........................................                               [100%]
42 passed in 4.38s

```

## reviewer_bridge試験の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_reviewer_bridge.py", "-q"]`
- exit：0・elapsed：0.504s

- stdout：

```text
....                                                                     [100%]
4 passed in 0.39s

```

## 既定private_rootの実機値

- argv：`[".venv/bin/python3", "-c", "from tools.reviewer_launch import entry; print(entry.default_private_root())"]`
- exit：0・elapsed：0.035s

- stdout：

```text
/Users/keno/.reviewcompass3-private/reviewer-launch

```

## 廃止placeholderの残存検索（該当なし＝exit 1が合格）

- argv：`["grep", "-n", "repo外私有領域の絶対パス\\|<YYYY-MM-DD>", "docs/development/prompts/reviewer-launch-run.md", "docs/development/prompts/request-builder-run.md"]`
- exit：1・elapsed：0.003s

## 変更4fileのdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/entry.py", "tools/request_builder/entry.py", "docs/development/prompts/reviewer-launch-run.md", "docs/development/prompts/request-builder-run.md"]`
- exit：0・elapsed：0.013s

- stdout：

```text
b8b33d9229b1f48258ab7c26475e5593093eb78799bc261db3f28aa316ec6fe1  tools/reviewer_launch/entry.py
2873e17b5e94ab1fb7f353b747a5098f1b29174a457dfc23f531034344ea0d1c  tools/request_builder/entry.py
59d71bcfa7a3502f44475f6b52a996aed6b5ae5ba045a19e9dc33a3abde3bcc5  docs/development/prompts/reviewer-launch-run.md
6b2f3493ffec7cd7674dfbaf79fa8ad3f893a81c0675ef4896117867117b474f  docs/development/prompts/request-builder-run.md

```
