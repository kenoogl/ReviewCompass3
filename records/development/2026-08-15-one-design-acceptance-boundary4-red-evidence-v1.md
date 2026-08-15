# One-design acceptance boundary 4 RED evidence v1

## Purpose

G08 の第4境界について、配布設定の追加前に、正式実行名とrepository外の配置後実行を固定した試験が未登録を検出することを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md` §6
- Boundary 3 GREEN commit: `b62539e`
- Test target: `tests/test_one_design_acceptance.py`

## Execution

【実測】次のcommandを単独で実行した。

```text
.venv/bin/python3 -m pytest -q --tb=short tests/test_one_design_acceptance.py
```

- exit code: `1`
- result: `3 failed, 88 passed in 0.16s`
- failure 1: `pyproject.toml`に`reviewcompass3-design-acceptance-check`がなく`KeyError`
- failure 2・3: `.venv/bin/reviewcompass3-design-acceptance-check`がなく`FileNotFoundError`

## Fixed failure examples

【実測】追加3件は、正式実行名が固定入口を指し依存一覧を変えないこと、核・repository module・配置後正式名が同じ正常bytesを返すこと、repository外の現在位置から配置後正式名が固定停止bytesを返すことを対象とする。

## Judgment

【判断】第4境界のREDは成立した。境界1〜3の固定88件は成功を維持し、追加3件だけが実行名未登録と配置後command不在で失敗した。repository module入口の正常実行は追加試験内で終了コード0となり、失敗原因を配布境界へ限定できる。

## Scope observation

【実測】RED確認時点で`pyproject.toml`、製品コード、既存G08保護対象4fileに追加差分はない。第4境界の差分は `tests/test_one_design_acceptance.py` だけである。

## Next boundary

試験を変更せず、`pyproject.toml`へ正式実行名一件だけを追加する。その後、`.venv/bin/python3 -m pip install --no-deps --no-build-isolation -e .`でnetworkと依存追加なしに配置する。
