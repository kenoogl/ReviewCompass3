# Work 4A Routine Classification Candidate Persistence GREEN Evidence v1

- Evidence ID：`RC3-WORK4A-ROUTINE-CLASSIFICATION-PERSISTENCE-GREEN-2026-08-04-V1`
- status：`verified / persistence_green / actual_candidate_list_not_yet_captured`
- scope：routine classification candidate listのexternal `DATA_ROOT`へのnew-only保存、Digest、再読込照合。

## Fixed inputs

- Routine Classification Approval Decision：`records/development/2026-08-04-work-4a-routine-classification-approval-decision-v1.json`
- Persistence RED Evidence：`records/development/2026-08-04-work-4a-routine-classification-persistence-red-evidence-v1.md`
- implementation：`tools/development/source_symbol_index.py`、SHA-256
  `ea8a07ad779b951724a4d26a9ed0752e8c73233b380de13ed7c6b867e7b24784`
- Acceptance Test：`tests/test_routine_classification_candidates.py`、SHA-256
  `a00f969d02a739748075895ef812167b788b362d7c121899836beadffbfb086b`

## Implemented boundary

- `persist_routine_classification_candidates`はcandidate listとunresolved reference formsを、Snapshot ID別の
  `routine-classification-candidates-v1.json`へnew-only保存する。保存recordにはproject IDとprofileを持たせ、
  terminal project pathは保存しない。
- 同一Snapshot IDの出力は明示的なerrorで拒否する。`verify_persisted_routine_classification_candidates`は
  保存Digestと再読込内容を固定reportへ照合する。
- final Verdict、Ledger登録、routine disposition、actual home directoryへの書込みは、この実装に含めない。

## GREEN verification

```text
.venv/bin/python3 -m pytest tests/test_routine_classification_candidates.py tests/test_source_symbol_index_persistence.py tests/test_source_symbol_index.py -q
```

結果：`16 passed in 2.02s`。

```text
.venv/bin/python3 -m pytest -q
```

結果：`675 passed in 4.86s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

## Deferred actual candidate capture

actual candidate listは、このGREEN containing commitのclean transition後に、latest Source Snapshot／Indexと
同じSnapshot IDへnew-only保存する。保存済みcandidateはHuman確認前にLedgerまたはreuse dispositionへ昇格しない。
