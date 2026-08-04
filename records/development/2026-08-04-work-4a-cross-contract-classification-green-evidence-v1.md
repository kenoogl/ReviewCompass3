# Work 4A Cross-contract Classification GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-CROSS-CONTRACT-CLASSIFICATION-GREEN-2026-08-04-V1`
- status：`verified / extractor_green / actual_candidate_list_not_yet_recaptured`
- scope：異なる`tools.<domain>`間のstatic importをcross-contract candidateとして抽出する最小規則。

## Fixed inputs

- Gap Candidate：`records/development/2026-08-04-work-4a-cross-contract-classification-gap-candidate-v1.json`
- Approval Decision：`records/development/2026-08-04-work-4a-cross-contract-classification-approval-decision-v1.json`
- implementation：`tools/development/source_symbol_index.py`、SHA-256
  `bff79e8cf2627a3b3e79348ac049759bf5d63562ec74a2af57c5e95c47fff5eb`
- Acceptance Test：`tests/test_routine_classification_candidates.py`、SHA-256
  `34da5e9ef0519573be658832186ca46cc523d4ee65e18e54c50b5a8e2fcf3a7e`

## Implemented boundary

- `tools/<domain>/...`で定義されたroutineを、異なる`<domain>`に属するprimary source moduleがstatic importした場合だけ
  `cross_contract` candidateを出す。definition pathとcross-domain import pathをEvidenceにする。
- 同一domainのstatic import、Test referenceだけのimport、dynamic attribute lookup、domainを持たない`tools/<module>.py`は
  この候補にしない。これはcall graph、動的import解決、semantic verdictを実装しない最小境界である。

## RED / GREEN verification

RED command：

```text
.venv/bin/python3 -m pytest tests/test_routine_classification_candidates.py -q
```

結果：`1 failed, 3 passed`。`cross_contract` candidate未実装による`KeyError`を確認した。

GREEN command：

```text
.venv/bin/python3 -m pytest tests/test_routine_classification_candidates.py tests/test_source_symbol_index.py tests/test_source_symbol_index_persistence.py -q
```

結果：`16 passed in 2.25s`。

```text
.venv/bin/python3 -m pytest -q
```

結果：`675 passed in 5.36s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

## Deferred actual candidate capture

cross-contract candidateはこのGREEN containing commitのclean transition後に、latest Snapshot／Indexと同じSnapshot IDで
new-only保存する。既存144件のcandidate listはhistoricalとして保存し、上書きしない。再生成後もcandidateはHumanの
final VerdictまたはLedger登録ではない。
