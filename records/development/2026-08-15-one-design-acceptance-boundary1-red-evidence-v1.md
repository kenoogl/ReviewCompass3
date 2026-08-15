# One-design acceptance boundary 1 RED evidence v1

## Purpose

G08 の第1境界について、実装前に要求を固定したテストが失敗し、未実装の振る舞いを検出できることを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket overlay: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md`
- Work ticket SHA-256: `a733a57203a0148c52d722713be4b3948134192da6f5bceef8ab5eb92e9a58ec`
- Test target: `tests/test_one_design_acceptance.py`

## Execution

【実測】次の command を単独で実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py
```

- exit code: `1`
- result: `43 failed in 0.20s`
- common failure: `ModuleNotFoundError: No module named 'tools.design.one_design_acceptance'`

## Judgment

【判断】第1境界の RED は成立した。43件はすべて、まだ作成していない中核モジュールの import で停止しており、既存実装の偶然の不合格や環境不良を合格根拠にしていない。

## Scope observation

【実測】RED確認時点では、製品コード、CLI entry、`pyproject.toml`、既存G08保護対象4ファイルに差分はない。作業treeの差分は未追跡の `tests/test_one_design_acceptance.py` だけである。

## Next boundary

テストを変更せずに `tools/design/one_design_acceptance.py` の中核比較処理だけを実装し、同じ43件がすべて合格することを確認する。CLI、安全読込、command登録は後続境界に残す。
