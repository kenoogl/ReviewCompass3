# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baselineが完了。Human判断によりWork 4AをWork 4より先行する。
- 現在作業：Work 4A start boundary completed_uncommitted / Source Symbol Index RED not_started
- Task Contract：activeなし

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：`resolved`、現行Workへの影響なし。次：Source Symbol IndexのRED Acceptance Test

## 最新のauthority／Evidence

- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development venv Baseline Evidence](records/development/2026-08-04-development-venv-baseline-completion-evidence-v1.md) — SHA-256 `896c827068417d0bed3154b1651f517f50d054d4c3b32a63e19b18f77306be93`
- [Work 4A Sequence Decision](records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json) — SHA-256 `4a10d09c12f227e67399aad1dc9c1ca8a6c664edcc6bc7f99385edafa7f48f0f`
- [Work 4A Start Boundary Evidence](records/development/2026-08-04-work-4a-start-boundary-evidence-v1.md) — SHA-256 `65d47954cf8f71b02444b334df8598912c31d19183d70ccec59bc083b1ed7159`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `43a414b041486b3e4446c3b15a631ceb94127cd25f386dedef9588d4d2f8a013`

## 次に行う一作業

Source Symbol IndexのAcceptance Testを作成し、bootstrap generator未実装のREDを確認する。

開始条件：

- Work 4A Start Boundary Evidence containing commitとclean transition
- venv bootstrapがPython 3.9.6、pytest 8.4.2でverified

完了条件：

- clean／dirty、対象／除外、欠落Digest、再生成一致、symbol identity衝突のAcceptance Test
- generator未実装による期待理由のRED

後続作業：RED Testを変更せず、最小bootstrap generatorを実装する。

## blocker・Human判断待ち

- blocker：`completed_work_unit_uncommitted`。Start Boundary Evidenceのcommit完了までRED Testへ移らない。
- Human判断待ち：なし。Work 4A先行と最小identity境界は承認済み。

## stale・deferred

- stale：開始前commit `0880b54`の観測はStart Boundary Evidenceを含むcommit後に再利用しない。Current Plan 17節の初期実装順6・7はSequence Decisionの範囲だけsuperseded。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Sequence Decision、TODO参照、restore rehearsal targeted 5 passed
- 直近の全Test：venv公式runner 652 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
