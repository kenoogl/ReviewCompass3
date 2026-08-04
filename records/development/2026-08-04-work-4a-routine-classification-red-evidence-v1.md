# Work 4A Routine Classification Candidate Extractor RED Evidence v1

- Evidence ID：`RC3-WORK4A-ROUTINE-CLASSIFICATION-RED-2026-08-04-V1`
- status：`active / red`
- scope：承認済みの分類規則から、public、shared、high-risk、duplicate、retiredの機械候補とsource evidenceを
  生成する最小extractor。

## Fixed inputs

- Approval Decision：`records/development/2026-08-04-work-4a-routine-classification-approval-decision-v1.json`
- Acceptance Test：`tests/test_routine_classification_candidates.py`、SHA-256
  `47c9625ba4654c787979f465d0c0c2893a927f0a0a8ccd672566038ca5b81361`
- Test environment：`.venv/bin/python3`、Python `3.9.6`、pytest `8.4.2`

## Expected behavior

1. 固定Snapshot／Indexからpublic、shared、high-risk、duplicate candidate、retired candidateを安定して出力する。
2. 各candidateをSnapshot ID、symbol ID、rule ID、source evidenceへ結線し、statusを`candidate`に留める。
3. terminal nameだけの一致、参照なしだけのroutineをduplicate／retiredとして誤分類しない。
4. dynamic attribute lookupを参照不明として明示する。
5. Indexが別Snapshotを指す場合を拒否する。

## RED execution

```text
.venv/bin/python3 -m pytest tests/test_routine_classification_candidates.py -q
```

結果：`2 failed`。直接原因は、`tools.development.source_symbol_index`に
`extract_routine_classification_candidates`が存在しない`AttributeError`である。必要なextractorが未実装であるための
期待どおりのREDであり、Acceptance Testは変更しない。

## Next implementation boundary

`tools/development/source_symbol_index.py`へ、ASTによるstatic import、filesystem write、deprecation marker、
normalized function body、dynamic attribute lookupの最小解析を追加する。final Verdict、Ledger登録、routine変更、
近似duplicateの意味判断は対象外である。
