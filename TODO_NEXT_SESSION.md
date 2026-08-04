# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baselineが完了。Human判断によりWork 4AをWork 4より先行する。
- 現在作業：Work 4A actual Snapshot／Indexをclean HEAD `6258aaf`から生成・照合済み / operation observation・improvement candidate committed
- Task Contract：activeなし

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：`resolved`、現行Workへの影響なし。次：project-first runtime rootのLayout Baseline amendment
- `IC-WORK4A-BASELINE-PERSISTENCE-001`：`untriaged`。actual baselineはhistorical outputとして保存済み。versioned persistence toolとcapture／commit順序のrouteをHumanが後続checkpointで判断する。

## 最新のauthority／Evidence

- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development venv Baseline Evidence](records/development/2026-08-04-development-venv-baseline-completion-evidence-v1.md) — SHA-256 `896c827068417d0bed3154b1651f517f50d054d4c3b32a63e19b18f77306be93`
- [Work 4A Sequence Decision](records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json) — SHA-256 `4a10d09c12f227e67399aad1dc9c1ca8a6c664edcc6bc7f99385edafa7f48f0f`
- [Work 4A Start Boundary Evidence](records/development/2026-08-04-work-4a-start-boundary-evidence-v1.md) — SHA-256 `65d47954cf8f71b02444b334df8598912c31d19183d70ccec59bc083b1ed7159`
- [Work 4A Source Symbol Index RED Evidence](records/development/2026-08-04-work-4a-source-symbol-index-red-evidence-v1.md) — SHA-256 `f8cf312392897cb9b5da030ffae15432e0d2a77a58ca8e158d786b66221454d3`
- [Work 4A Source Symbol Index GREEN Evidence](records/development/2026-08-04-work-4a-source-symbol-index-green-evidence-v1.md) — SHA-256 `d0cb960280a9411b5358d9d21ee3fc2fc8829bf12ddf0a6f9e7d6180ef56a871`
- [Project-first Runtime Root Memo](docs/design/2026-08-04-project-first-runtime-root-memo.md) — SHA-256 `b1306fd2202b8562dae86acff0dd003ca2b9e9029dd5208e21e1e24e59d5e474`
- [Layout Baseline v3 Project-first Candidate](records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json) — SHA-256 `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38`
- [Layout Baseline v3 RED Evidence](records/development/2026-08-04-layout-baseline-v3-project-first-red-evidence-v1.md) — SHA-256 `278a4f4cd9de499702181104b9313b4cf895725f0039f10f2258390e3959f992`
- [Layout Baseline v3 GREEN Evidence](records/development/2026-08-04-layout-baseline-v3-project-first-green-evidence-v1.md) — SHA-256 `9522f2f26a3863b9ab20b428f7fe61d1bdd33a685a19cb289b43c814f3865284`
- [Layout Baseline v3 GREEN Test Receipt](records/development/2026-08-04-layout-baseline-v3-project-first-green-test-receipt-v1.json) — SHA-256 `f1da6b0909147f0c74ca07409a9bbfea7a2981e4476111b97ce73257d2728ecd`
- [Layout Baseline v3 Approval Decision](records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json) — SHA-256 `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275`
- [Work 4A Actual Baseline Operation Observation](records/development/2026-08-04-work-4a-actual-baseline-operation-observation-v1.json) — SHA-256 `1c82cbb33c6657e278bbcc63df9fc65b36670120310114c98f3bd42d5c908018`
- [Work 4A Baseline Persistence Improvement Candidate](records/development/2026-08-04-work-4a-baseline-persistence-improvement-candidate-v1.json) — SHA-256 `d7193d504860229f95de3f7c4f1e9e2515e401e7295c90e26669335c783bac99`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `dff6b6619da1f39401322e3f556d40c164e2619228d05f676c6fbcb2d9ccc73c`

## 次に行う一作業

actual baseline operation observationとmanual-operation improvement candidateをcommitし、clean containing commitから
current Source SnapshotとSource Symbol Indexを新規生成する。

開始条件：

- actual baseline operation observationとimprovement candidate containing commitとclean transition

完了条件：

- clean source treeからcurrent Source SnapshotとSource Symbol Indexを新規生成し、coverage、freshness、再生成一致を記録する

後続作業：承認後、clean containing commitからactual Source SnapshotとSource Symbol Index baselineを機械生成する。

## blocker・Human判断待ち

- blocker：なし。次のcurrent baseline再生成はこの記録commitのclean transitionを入力とする。
- Human判断待ち：なし。初回runtime directory作成は承認済みLayout内の明示操作として次の作業単位で行う。

## stale・deferred

- stale：開始前commit `0880b54`の観測はStart Boundary Evidenceを含むcommit後に再利用しない。actual Source Symbol Indexの保存先はLayout amendmentまで未確定。Current Plan 17節の初期実装順6・7はSequence Decisionの範囲だけsuperseded。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Project-first Runtime Layout v3 Acceptance `7 passed`、Layout Baseline互換 `12 passed`
- 直近の全Test：venv公式runner 664 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
