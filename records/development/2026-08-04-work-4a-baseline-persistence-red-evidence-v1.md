# Work 4A Baseline Persistence RED Evidence v1

- Evidence ID：`RC3-WORK4A-BASELINE-PERSISTENCE-RED-2026-08-04-V1`
- status：`active / red`
- scope：Source SnapshotとSource Symbol Indexをexternal `DATA_ROOT`へnew-onlyで永続化する最小tool。

## Fixed inputs

- Triage Decision：`records/development/2026-08-04-work-4a-baseline-persistence-triage-decision-v1.json`
- Acceptance Test：`tests/test_source_symbol_index_persistence.py`、SHA-256
  `dc64be4bf6a4bbe8ae0cf6dc02bba893f6f0ea9e8c575570f8961f5b3306f4f1`
- Test environment：`.venv/bin/python3`、Python `3.9.6`、pytest `8.4.2`

## Expected behavior

1. SnapshotとIndexをsnapshot ID別のnew-only JSONとして保存し、terminal project pathを保存物へ入れない。
2. 同じ出力先の再保存とSnapshot／Index identity不一致を拒否する。
3. output Digestと再読込内容を照合し、改竄を検出する。
4. 現在のSnapshotと同じ出力を`current`、異なるものを`historical`として区別する。
5. relative data root、不正project ID、不正profileを拒否する。

## RED execution

```text
.venv/bin/python3 -m pytest tests/test_source_symbol_index_persistence.py -q
```

結果：`7 failed`。全件の直接原因は、`tools.development.source_symbol_index`に
`persist_source_symbol_index_baseline`が存在しない`AttributeError`である。必要な永続化toolが未実装であるための
期待どおりのREDであり、Acceptance Testの期待は変更しない。

## Next implementation boundary

`tools/development/source_symbol_index.py`へ、new-only write、SHA-256、再読込比較、current／historical分類の
最小APIだけを追加する。既存Snapshot identity規則、Layout resolver、external outputのmigration、実home directoryへの
書込みは対象外である。
