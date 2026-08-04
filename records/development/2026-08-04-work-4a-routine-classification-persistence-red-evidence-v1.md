# Work 4A Routine Classification Candidate Persistence RED Evidence v1

- Evidence ID：`RC3-WORK4A-ROUTINE-CLASSIFICATION-PERSISTENCE-RED-2026-08-04-V1`
- status：`active / red`
- scope：actual routine classification candidate listをexternal `DATA_ROOT`へnew-only保存し、Digestと再読込照合を行う
  最小persistence API。

## Fixed inputs

- Routine Classification Approval Decision：`records/development/2026-08-04-work-4a-routine-classification-approval-decision-v1.json`
- Extractor GREEN Evidence：`records/development/2026-08-04-work-4a-routine-classification-green-evidence-v1.md`
- Acceptance Test：`tests/test_routine_classification_candidates.py`、SHA-256
  `a00f969d02a739748075895ef812167b788b362d7c121899836beadffbfb086b`

## Expected behavior

1. candidate listとunresolved referenceをsnapshot ID別のnew-only JSONへ保存する。
2. outputにterminal project pathを入れず、project IDとprofileを保存する。
3. 同一出力の再保存を拒否し、Digestと再読込内容を照合する。
4. 改竄したcandidate listをDigest不一致として拒否する。

## RED execution

```text
.venv/bin/python3 -m pytest tests/test_routine_classification_candidates.py -q
```

結果：`2 passed, 2 failed`。失敗2件の直接原因は、
`persist_routine_classification_candidates`が未実装である`AttributeError`である。既存extractorのGREEN Testは維持し、
必要なpersistence API未実装を確認した。

## Next implementation boundary

`tools/development/source_symbol_index.py`へcandidate listのnew-only保存、SHA-256、再読込照合だけを追加する。
candidateの意味的確定、Ledger登録、routine disposition、実home directoryへの書込みは対象外である。
