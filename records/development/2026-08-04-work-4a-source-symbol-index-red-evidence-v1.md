# Work 4A Source Symbol Index RED Evidence v1

- Evidence ID：`RC3-WORK4A-SOURCE-SYMBOL-INDEX-RED-2026-08-04-V1`
- status：`active / red`
- scope：Source Snapshot captureとSource Symbol Indexの最小bootstrap generatorのAcceptance Test。実装は未着手。

## Fixed inputs

- Start Boundary Evidence：`records/development/2026-08-04-work-4a-start-boundary-evidence-v1.md`、SHA-256
  `65d47954cf8f71b02444b334df8598912c31d19183d70ccec59bc083b1ed7159`
- Acceptance Test：`tests/test_source_symbol_index.py`、SHA-256
  `46411f490db361060df858966fd543f4c02c6bc49dfa2ffbd38fdd1e05ff58cf`
- Test environment：`.venv/bin/python3`、Python `3.9.6`、pytest `8.4.2`

## Expected behavior

1. clean Git fixtureからordered primary／Test-reference manifestと同一Snapshot IDを再生成する。
2. dirtyまたはuntracked sourceを`source_snapshot_dirty`として停止する。
3. ignored pathを収録せず、欠落したfile Digestを`source_snapshot_file_digest_missing`として拒否する。
4. `FunctionDef`と`AsyncFunctionDef`を一意なsymbol IDへ収録し、同名別path、class method、nested functionを区別する。
5. content変更後はSnapshot IDとsymbol content Digestが変わり、symbol IDは維持する。

## RED execution

```text
.venv/bin/python3 -m pytest -q tests/test_source_symbol_index.py
```

結果：`5 failed`。全件の直接原因は
`ModuleNotFoundError: No module named 'tools.development.source_symbol_index'`である。
これは期待どおり、必要なgenerator moduleが存在しないためのREDであり、Testの期待を変更しない。

## Next implementation boundary

次作業で`tools/development/source_symbol_index.py`だけを追加し、RED Testを変更せずに
SourceUniverse、Snapshot capture／validation、AST Index generationの最小実装を行う。Ledger、参照関係、
visibility、Human意味確認、製品Runtimeへの流用は対象外である。
