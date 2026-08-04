# Issue Resolution Pilot WI-007 Completion Evidence v1

## 固定source

- source：`TODO_NEXT_SESSION.md`
- source／snapshot SHA-256：`16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`
- bytes：`85219`
- lines：`900`
- Claim count：`123`

## 成果物

- snapshot：`records/session-handoffs/2026-08-04-todo-before-compaction-001.md`
- snapshot SHA-256：`16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`
- manifest：`records/session-handoffs/2026-08-04-todo-before-compaction-001.manifest.json`
- manifest file SHA-256：`395337e57cd73ccb16bec4e009761f780f4631444e12f081b55e1d7c6ed40963`
- manifest content Digest：`719b664d86922fdc69a5be27a128d2e952929585a6338d820008494d078e910c`

## 境界検証

- 既存9 snapshot Testを変更せず、source変更時に旧snapshotを上書きせず新versionへ作成するTestを追加した。
- 追加Test：`tests/test_todo_snapshot_versioned_recovery.py`、SHA-256
  `66ea2dea1a1da0858bf7cb793935f11b6696d4893d241e9e284aa10043e5ee95`
- snapshot関連：`10 passed in 0.04s`
- 作成後の機械再読込：`action=verified`、source／snapshot SHA、bytes、lines、Claim count一致。
- 公式receipt：`records/development/2026-08-04-issue-resolution-pilot-wi-007-test-receipt-v1.json`
- receipt SHA-256：`e058d1625ea34ec57b1500357ea902ae639236185f958e2eb95d1fc6d071797e`
- 全体：`625 passed in 2.77s`、fallback `false`

## commit安定境界

WI-007作業単位では`TODO_NEXT_SESSION.md`を変更していない。containing commit後、同じsource identityを再読込し、
clean transitionが合格した場合だけWI-003の最初のTODO書換えを許可する。不一致なら本snapshotを上書きせず新versionを
作成する。
