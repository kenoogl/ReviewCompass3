# Work 4A Reusable Routine Ledger GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-REUSABLE-ROUTINE-LEDGER-GREEN-2026-08-04-V1`
- status：`verified / entry_baseline_green / relation_not_implemented / actual_entry_not_yet_created`
- Decision：`DEC-WORK4A-REUSABLE-ROUTINE-LEDGER-STRUCTURE-001`

最小schemaは`.reviewcompass/reuse/reusable-routine-ledger/`へentryとDigest付きbaseline manifestをnew-only保存する。
baselineだけがcurrent entryをDigest付きで束縛し、terminal pathは保存しない。Snapshot不一致、reuse root escape、
entry Digest不一致を拒否する。relationの実装とactual Ledger entryの作成は対象外である。

```text
.venv/bin/python3 -m pytest tests/test_reusable_routine_ledger.py -q
```

結果：`2 passed`。REDではmodule未実装により`2 failed`。

```text
.venv/bin/python3 -m pytest -q
```

結果：`677 passed in 4.46s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

- implementation SHA-256：`5e8b3b600ebdd73523aa69957ea93f9b767ff0ca975e9b5f79bb276889cc7332`
- Acceptance Test SHA-256：`9f71df2a371999753b9b907bf68ec47a53fbbd4598f0a2c35f04876c7bc4099a`
