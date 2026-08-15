# One-design acceptance boundary 2 RED evidence v1

## Purpose

G08 の第2境界について、安全読込の実装前に、path・symlink・通常file・size・読取り前後整合・副作用の要求を固定した試験が未実装を検出することを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md` §4
- Boundary 1 GREEN commit: `e200310`
- Test target: `tests/test_one_design_acceptance.py`

## Execution

【実測】次のcommandを単独で実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py
```

- exit code: `1`
- result: `24 failed, 43 passed in 0.14s`
- common failure: `AttributeError: module 'tools.design.one_design_acceptance' has no attribute 'read_input_pair'`

## Fixed failure examples

【実測】追加24件は、正常な二file読込、相対・root外・`.`・`..`・空構成要素・同一path、rootまでとfileまでの各層symlink、directory・FIFO・socket、262,144 bytes超過、読取り後のsize・機器番号・inode変更、短い実読取り、全構成要素のopen flag、必須非追跡flag不在、入力tree不変を対象とする。

## Judgment

【判断】第2境界のREDは成立した。境界1の固定43件は成功を維持し、追加24件だけが安全読込公開関数の不在で失敗した。

## Scope observation

【実測】RED確認時点で製品コード、CLI entry、`pyproject.toml`、既存G08保護対象4fileに追加差分はない。第2境界の差分は `tests/test_one_design_acceptance.py` だけである。

## Next boundary

試験を変更せず、比較核と同じmoduleへ安全読込だけを追加する。CLIとcommand登録は後続境界に残す。
