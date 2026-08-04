# Work 4A Routine Classification Candidate Extractor GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-ROUTINE-CLASSIFICATION-GREEN-2026-08-04-V1`
- status：`verified / extractor_green / actual_candidate_list_not_yet_captured`
- scope：承認済み分類規則から、Human確定前のroutine候補とsource evidenceを抽出する最小tool。

## Fixed inputs

- Approval Decision：`records/development/2026-08-04-work-4a-routine-classification-approval-decision-v1.json`
- RED Evidence：`records/development/2026-08-04-work-4a-routine-classification-red-evidence-v1.md`
- implementation：`tools/development/source_symbol_index.py`、SHA-256
  `581d2ec9f47448ccdc52b6dcd1d0f74ef96a4ac0bd93ad952239b489fb7885ac`
- Acceptance Test：`tests/test_routine_classification_candidates.py`、SHA-256
  `47c9625ba4654c787979f465d0c0c2893a927f0a0a8ccd672566038ca5b81361`

## Implemented boundary

- `extract_routine_classification_candidates`は、固定Snapshot／Indexのidentity一致を確認した後、
  static importからpublic／shared候補、filesystem writeまたはsubprocessからhigh-risk候補、deprecation markerかつ
  静的参照なしからretired候補、同一normalized bodyかつsignatureからduplicate candidateを出力する。
- 各出力はSnapshot ID、symbol ID、rule ID、definitionとrule hitのsource evidence、`candidate` statusを持つ。
- dynamic attribute lookupは解決済み参照と偽装せず、`unresolved_reference_forms`へ明示する。
- terminal nameだけの一致、静的参照なしだけのroutineは候補にしない。final Verdict、Ledger登録、routine変更、
  近似duplicateの意味判断は未実装である。

## GREEN verification

```text
.venv/bin/python3 -m pytest tests/test_source_symbol_index.py tests/test_source_symbol_index_persistence.py tests/test_routine_classification_candidates.py -q
```

結果：`14 passed`。

```text
.venv/bin/python3 -m pytest -q
```

結果：`673 passed in 5.20s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

## Deferred actual candidate capture

extractor自身が未コミットの間は`capture_source_snapshot`がdirty worktreeを拒否する。したがってactual candidate listは
このGREEN containing commitのclean transition後、latest Snapshot／Indexをnew IDとして保存してから生成する。
候補はHuman確認前にLedgerまたはreuse dispositionへ昇格しない。
