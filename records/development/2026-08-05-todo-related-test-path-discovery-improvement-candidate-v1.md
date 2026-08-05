---
candidate_id: IC-TODO-RELATED-TEST-PATH-DISCOVERY-001
observed_at: 2026-08-05
origin_stage: initial-development
origin_work: Work 5A Claude handoff TODO update verification
candidate_kind: improvement_candidate
classification: manual_operation_candidate
priority: P3
status: routed
blocking: false
suggested_route: ISSUE-HTC-C9F6C917
confidentiality_class: project-internal
---

# TODO関連Testのpathを実在確認せず指定した

## 1. 対象操作と期待／実executor

- 対象操作：`TODO_NEXT_SESSION.md`更新後の関連Test選択と実行。
- 期待executor：`rg --files tests`の機械列挙から実在する関連Testだけを選ぶ処理。
- 実executor：LLMが記憶に基づいてTest pathを直接組み立てた。
- 手作業理由：既存Test名を確認する検索をTest実行より先に行わなかった。

## 2. 手戻り事象とEvidence

最初の補助Test commandへ、実在しない`tests/test_todo_handoff.py`を含めた。

```text
ERROR: file or directory not found: tests/test_todo_handoff.py
no tests ran in 0.00s
```

成果物生成と`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`は先に合格しており、
TODO内容への影響は無い。`rg --files tests | rg 'todo_(handoff|compaction|projection)'`で実在pathを列挙し、
関連6 fileを再実行した結果は`31 passed in 0.09s`、TODO validatorも再度`passed`である。

## 3. 機械処理候補とroute

- 機械処理候補：Test pathを固定文字列で推測せず、repository inventoryから解決してからrunnerへ渡す。
- route：決定的操作の手組みによる手戻りを扱う既存`ISSUE-HTC-C9F6C917`へnonblockingでrouteする。
- 現行Work：停止しない。Claude handoffとTODO更新の検証結果は有効である。
