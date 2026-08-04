# Work 4A Baseline Persistence GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-BASELINE-PERSISTENCE-GREEN-2026-08-04-V1`
- status：`verified / tool_green / current_baseline_not_yet_captured`
- scope：Source SnapshotとSource Symbol Indexをexternal `DATA_ROOT`へnew-only保存するversioned persistence tool。

## Fixed inputs

- Triage Decision：`records/development/2026-08-04-work-4a-baseline-persistence-triage-decision-v1.json`
- RED Evidence：`records/development/2026-08-04-work-4a-baseline-persistence-red-evidence-v1.md`
- implementation：`tools/development/source_symbol_index.py`、SHA-256
  `e2704661819f88ef68d4526f85c11dcc179994e43485249ce6592f43cf022d1d`
- Acceptance Test：`tests/test_source_symbol_index_persistence.py`、SHA-256
  `dc64be4bf6a4bbe8ae0cf6dc02bba893f6f0ea9e8c575570f8961f5b3306f4f1`

## Implemented boundary

- `persist_source_symbol_index_baseline`はabsolute `DATA_ROOT`、明示project ID、`development`または`runtime`
  profileを検査し、Snapshot／Indexをsnapshot ID別JSONとしてnew-only保存する。
- 保存物はterminal project pathを含まず、Snapshot／Index identity不一致、既存出力、relative root、不正ID／profileを
  拒否する。
- `verify_persisted_source_symbol_index_baseline`は保存Digestと再読込内容を固定Snapshot／Indexへ照合する。
- `classify_persisted_source_symbol_index_baseline`は指定current Snapshotと同一なら`current`、異なれば
  `historical`を返す。既存Snapshot identity規則、Layout resolver、既存external outputは変更しない。

## GREEN verification

```text
.venv/bin/python3 -m pytest tests/test_source_symbol_index_persistence.py -q
```

結果：`7 passed`。

```text
.venv/bin/python3 -m pytest tests/test_source_symbol_index.py -q
```

結果：`5 passed`。既存generatorとの互換を確認した。

```text
.venv/bin/python3 -m pytest -q
```

結果：`671 passed in 5.23s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

## Deferred current baseline capture

このtool自身が未コミットの間は`capture_source_snapshot`がdirty worktreeを拒否する。したがって、
current external baselineはこのGREEN containing commitのclean transition後に、toolを使ってnew IDとして生成する。
保存済みHEAD `6258aaf`のoutputはhistoricalとして保持し、上書きしない。
