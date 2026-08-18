# 測定ブロック：計画JSON writer（対策2）事前走査の実測

- captured_at：2026-08-18T20:49:47+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-plan-writer-prescan-commands-v1.json`（SHA-256 `c474a3882c479e78bd33790c4dab3652608c08893dd12cda070538a9b68a6aa5`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 既存の正規writer（universe・policy）の所在

- argv：`["grep", "-rln", "write_source_universe\\|write_freshness_policy", "tools/"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.062s
- 完全性：二重実行一致

- stdout：

```text
tools/development/work4a_rebuild_v3.py
tools/development/__pycache__/work4a_rebuild_v3.cpython-313.pyc

```

## 検索側の計画検証の実装点

- argv：`["grep", "-n", "_PLAN_FIELDS\\|_SEARCH_FIELDS_V2\\|content_digest\\|def _load_plan\\|def _validate", "tools/development/formal_code_reuse_search.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.003s
- 完全性：二重実行一致

- stdout：

```text
14:_PLAN_FIELDS = {
19:    "content_digest",
27:_SEARCH_FIELDS_V2 = {
77:def _validate_plan(document, project_root):
78:    if not isinstance(document, dict) or set(document) != _PLAN_FIELDS:
85:        or document.get("content_digest") != work4a._content_digest(document)
99:            else _SEARCH_FIELDS_V2
167:            document["content_digest"],
188:        document["content_digest"],
325:                "search_content_digest": record["content_digest"],

```

## 正準digest関数の所在

- argv：`["grep", "-n", "def canonical_content_digest", "tools/common/digests.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.002s
- 完全性：二重実行一致

- stdout：

```text
73:def canonical_content_digest(document):

```

## 既存の計画record数（手書きheredocの実例母数）

- argv：`["grep", "-rln", "formal_code_reuse_search_plan", "records/development/"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.052s
- 完全性：二重実行一致

- stdout：

```text
records/development/2026-08-18-operational-metrics-reuse-search-plan-v1.json
records/development/2026-08-17-reviewer-bridge-reuse-search-plan-v1.json
records/development/2026-08-18-plan-writer-prescan-commands-v1.json
records/development/2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json
records/development/2026-08-18-session-log-exit-code-reuse-search-plan-v1.json
records/development/2026-08-18-measurement-block-plan-v1.json
records/development/2026-08-17-launch-metrics-reuse-search-plan-v1.json
records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json
records/development/2026-08-17-session-log-record-run-reuse-search-plan-v1.json
records/development/2026-08-18-measurement-block-nondeterminism-observation-v1.md
records/development/2026-08-18-operational-metrics-v2-reuse-search-plan-v1.json
records/development/2026-08-17-rq1-apparatus-reuse-search-plan-v1.json
records/development/2026-08-18-placement-root-resolution-reuse-search-plan-v1.json
records/development/2026-08-17-rq2-apparatus-reuse-search-plan-v1.json
records/development/2026-08-17-free-text-request-type-reuse-search-plan-v1.json
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v4.json
records/development/2026-08-17-vertical-a-request-builder-reuse-search-plan-v1.json
records/development/2026-08-18-measurement-block-integrity-guard-plan-v1.json
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v3.json
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v2.json
records/development/2026-08-18-cli-defaults-rollout-plan-v1.json
records/development/2026-08-15-safe-storage-formal-code-reuse-search-plan-v1.json
records/development/2026-08-18-reuse-search-cli-defaults-plan-v1.json

```
