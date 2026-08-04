# Work 4A Source Symbol Index GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-SOURCE-SYMBOL-INDEX-GREEN-2026-08-04-V1`
- status：`verified / generator_green / baseline_not_yet_captured`
- scope：SourceUniverse、clean Source Snapshot capture／validation、function／method AST Indexの最小bootstrap generator。

## Fixed inputs

- RED Evidence：`records/development/2026-08-04-work-4a-source-symbol-index-red-evidence-v1.md`
- generator：`tools/development/source_symbol_index.py`、SHA-256
  `a6d67cbf5f3d0493c813f0d6e4e629c8f933be42ef9268c4555b514dd23bada0`
- Acceptance Test：`tests/test_source_symbol_index.py`、SHA-256
  `46411f490db361060df858966fd543f4c02c6bc49dfa2ffbd38fdd1e05ff58cf`

## Implemented boundary

- `capture_source_snapshot`はGit worktree全体がcleanでなければ`source_snapshot_dirty`で停止する。
- Git追跡済みの`tools/**/*.py`と`tests/**/*.py`を別populationとして、path順とfile bytesのSHA-256で
  manifest化する。Snapshot IDはHEAD、SourceUniverse、両manifestのcanonical JSON SHA-256である。
- `validate_source_snapshot`はHEAD、clean状態、file存在、file Digest、Snapshot IDを再照合する。
- `generate_source_symbol_index`は一次populationだけをAST解析し、function、async function、method、
  async method、nested functionを、固定したpath／qualified name／kindのsymbol IDへ収録する。
- Ledger、visibility、参照関係、Test参照抽出、Human意味確認、製品Runtime流用は未実装である。

## GREEN verification

```text
.venv/bin/python3 -m pytest -q tests/test_source_symbol_index.py
```

結果：`5 passed`。RED Testを変更せず、clean再生成、dirty拒否、ignored path、欠落Digest、symbol identity、
content変更検出を確認した。

公式全Testは
`records/development/2026-08-04-work-4a-source-symbol-index-green-test-receipt-v1.json`で`657 passed`、
Python `3.9.6`、pytest `8.4.2`、fallback `false`である。

## Deferred actual baseline capture

このgenerator自身が未コミットである間は、実リポジトリのcaptureは意図どおりdirty拒否となる。
したがって実source treeのSnapshot、100 files／631 functions・methodsの実Index、coverage、freshness、
再生成一致は、このGREEN containing commitのclean transition後の次作業で採取・確認する。
