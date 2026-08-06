# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 6AはCL-6A-08・09・10の3項目が完了、部分被覆3項目は残余明記済み、基盤待ち4項目と関門1項目が残る。最終審査は意図毀損所見の検出とfail-closed停止を持ち、LLMレビュー実導入は別Task Contractである。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提

## 最新のauthority／Evidence

- [意図毀損検出 設計提案（承認済み）](docs/design/2026-08-06-final-challenge-intent-damage-proposal.md) — SHA-256 `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6`
- [CL-6A-10完了Decision](records/development/2026-08-06-work6a-cl-6a-10-completion-decision-v1.md) — SHA-256 `efd3a577129a1b12c264a300f6743b9d149bd00f002cefac84fe1d433f9ce42a`
- [意図毀損 GREEN Evidence](records/development/2026-08-06-intent-damage-green-evidence-v1.md) — SHA-256 `81ad5060eeb50c176e93cc5ee5a7df57d6085a53a3f1b7d70f6aa4adba91645c`
- [意図毀損 宣言→RED対応表](records/development/2026-08-06-intent-damage-declaration-red-map-v1.json) — SHA-256 `80decdaa37ac8a0f977128d7a7866c6e00c6defd58faacf32eceeeb2a90ae3d0`
- [意図毀損 RED Evidence](records/development/2026-08-06-intent-damage-red-evidence-v1.md) — SHA-256 `9950c141e5dcb6bd485857fcf3e34ae2372f61bee705a84cf92aa3fafedde047`
- [テスト増加の課題record](.reviewcompass/workflow/issues-v4/issue-test-growth-state-pinning-001--v1.json) — SHA-256 `13f4c9a68d90105e66f3e3b5fb2df36b334f7921ee69430b82e85cf40b6f8194`
- [本日の問題一覧（14件）](records/development/2026-08-06-encountered-problem-inventory-v1.md) — SHA-256 `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `0ad491a7177ade5983ca1a514f48a50a762d23f2bacf38c8b3c953a679040968`

## 次に行う一作業

Humanが次の一作業を判断する。候補は、Work 6A残り項目の扱いの再確認、登録済み5課題からの着手選定、または区切りである。

開始条件：

- CL-6A-10完了反映を含むcommitがcleanで全Testが緑であること

完了条件：

- 次の一作業がHuman判断として示されること

後続作業：Work 6Aの残りはCL-6A-01/02/03/05（残余明記済み）、CL-6A-04/06/07（基盤未整備）、CL-6A-11（段の関門）。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：次の一作業の選定。

## stale・deferred

- stale：CL-6A-10の完了印待ちは解消した。checklist参照digestは本commitの値へ更新済み。
- deferred：Work 6Aの残り9項目、登録済み5課題の着手、テスト整理のWork 8測定、Current Work Projection正式写像、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Intake V4単体候補11 passed、Work 6A境界例1 passed
- 直近の全Test：venv公式runner 1032 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
