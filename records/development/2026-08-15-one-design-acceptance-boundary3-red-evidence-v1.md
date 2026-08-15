# One-design acceptance boundary 3 RED evidence v1

## Purpose

G08 の第3境界について、正式命令入口の実装前に、引数、安全表示、停止元、終了コード、禁止作用の要求を固定した試験が未実装を検出することを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md` §5
- Overlay: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md` §2
- Boundary 2 GREEN commit: `9028a67`
- Test target: `tests/test_one_design_acceptance.py`

## Execution

【実測】次のcommandを単独で実行した。

```text
.venv/bin/python3 -m pytest -q --tb=short tests/test_one_design_acceptance.py
```

- exit code: `1`
- result: `18 failed, 70 passed in 0.24s`
- common failure: `ModuleNotFoundError: No module named 'tools.design.one_design_acceptance_entry'`

## Fixed failure examples

【実測】追加18件は、正常結果の核との完全一致、引数不足・未知操作・未知引数・重複引数・相対pathの読取り前停止、設計側と受入条件側それぞれのsize・UTF-8・schema・open失敗、入力owner不明の読取り失敗、秘密候補を含む内部例外、安全表示、空stderr、入力tree不変を対象とする。

【実測】巨大入力をparameter IDへ展開しない固定IDを付け、失敗表示自体に入力内容を出さないよう試験表示を訂正した。検査内容と期待結果は変更していない。

## Judgment

【判断】第3境界のREDは成立した。境界1・2の固定70件は成功を維持し、追加18件だけが入口module不在で失敗した。

## Scope observation

【実測】RED確認時点で製品コード、`pyproject.toml`、既存G08保護対象4fileに追加差分はない。第3境界の差分は `tests/test_one_design_acceptance.py` だけである。

## Next boundary

試験を変更せず、`tools/design/one_design_acceptance_entry.py` の薄い入口だけを実装する。command登録は境界4に残す。
