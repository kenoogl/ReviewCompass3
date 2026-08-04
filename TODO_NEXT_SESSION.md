# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baselineが完了。Human判断によりWork 4AをWork 4より先行する。
- 現在作業：Work 4A Source Symbol Index generator GREEN completed_uncommitted / actual baseline capture not_started
- Task Contract：activeなし

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：`resolved`、現行Workへの影響なし。次：actual Source SnapshotとSource Symbol Index baseline

## 最新のauthority／Evidence

- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development venv Baseline Evidence](records/development/2026-08-04-development-venv-baseline-completion-evidence-v1.md) — SHA-256 `896c827068417d0bed3154b1651f517f50d054d4c3b32a63e19b18f77306be93`
- [Work 4A Sequence Decision](records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json) — SHA-256 `4a10d09c12f227e67399aad1dc9c1ca8a6c664edcc6bc7f99385edafa7f48f0f`
- [Work 4A Start Boundary Evidence](records/development/2026-08-04-work-4a-start-boundary-evidence-v1.md) — SHA-256 `65d47954cf8f71b02444b334df8598912c31d19183d70ccec59bc083b1ed7159`
- [Work 4A Source Symbol Index RED Evidence](records/development/2026-08-04-work-4a-source-symbol-index-red-evidence-v1.md) — SHA-256 `f8cf312392897cb9b5da030ffae15432e0d2a77a58ca8e158d786b66221454d3`
- [Work 4A Source Symbol Index GREEN Evidence](records/development/2026-08-04-work-4a-source-symbol-index-green-evidence-v1.md) — SHA-256 `d0cb960280a9411b5358d9d21ee3fc2fc8829bf12ddf0a6f9e7d6180ef56a871`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `b6eb1dc55235520e8ce90e99b940f5520c101f0b31ea342dcec4ed8b36ff0231`

## 次に行う一作業

clean containing commitからactual Source SnapshotとSource Symbol Index baselineを機械生成する。

開始条件：

- Source Symbol Index GREEN containing commitとclean transition
- venv bootstrapがPython 3.9.6、pytest 8.4.2でverified

完了条件：

- Snapshot ID、primary／Test-reference manifest、全function／method Indexを実source treeから保存する
- coverage、freshness、再生成一致を機械確認する

後続作業：public、shared、high-risk、重複候補、retiredの機械抽出を追加する。

## blocker・Human判断待ち

- blocker：`completed_work_unit_uncommitted`。GREEN generatorのcommit完了までactual baseline captureへ移らない。
- Human判断待ち：なし。Work 4A先行と最小identity境界は承認済み。

## stale・deferred

- stale：開始前commit `0880b54`の観測はStart Boundary Evidenceを含むcommit後に再利用しない。実source treeのIndex観測はGREEN containing commitまで未採取。Current Plan 17節の初期実装順6・7はSequence Decisionの範囲だけsuperseded。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Source Symbol Index Acceptance `5 passed`
- 直近の全Test：venv公式runner 657 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
