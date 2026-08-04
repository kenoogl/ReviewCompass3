# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3完了。Work 4前のIssue Resolution早期Pilotを実施中。
- 現在作業：WI-004 common TODO prompt completed / commit pending
- Task Contract：`TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V2`

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：`implementation_in_progress`、影響：root TODO handoffとPilot完了境界、次：WI-005

## 最新のauthority／Evidence

- [Task Contract v2](records/task-contract/issue-resolution-todo-compaction-implementation-v2.json) — SHA-256 `1fb3608e0aa0daabec3680f8913bb28a3ea5ade87acb1d9402d75174098a67a6`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Pre-compaction Snapshot Manifest](records/session-handoffs/2026-08-04-todo-before-compaction-001.manifest.json) — SHA-256 `395337e57cd73ccb16bec4e009761f780f4631444e12f081b55e1d7c6ed40963`
- [WI-003 Completion Evidence](records/development/2026-08-04-issue-resolution-pilot-wi-003-completion-evidence-v1.md) — SHA-256 `9b0c9e62d353edf54fec82419d2e2adc8188ef0493e31792ea81d6adb05c614c`

## 次に行う一作業

WI-005のpost-write検証、restore rehearsal、Pilot測定、Resolution Verdict候補をtest-firstで実施する。

開始条件：

- WI-004 containing commitとclean transition
- WI-003とWI-004のcompleted／committed確認

完了条件：

- post-write再読込、validator、参照、restore rehearsal、公式全Testの合格
- 未処理と残余riskを記録したResolution Verdict候補

後続作業：Resolution VerdictのHuman判断。承認後に早期Pilotを閉じる。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：現在なし。Resolution VerdictでHuman判断が必要。

## stale・deferred

- stale：Plan v1-v3とTask Contract v1はPlan v4／Task Contract v2へsuperseded。
- deferred：正式Issue Resolution automation、画面UI、Work 4以降の製品工程。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：共通prompt／入口3 passed、TODO projection 6 passed
- 直近の全Test：634 passed（WI-004 TODO更新前）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
