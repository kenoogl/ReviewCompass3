# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Issue Intake V4の最小修正が完了した。単体候補参照、候補全件検証、歴史allowlistを実装し、検査器の課題ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001をregistered（未着手）で登録した。同じTestを弱めていない。問題一覧の#8と#14は解消した。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則（対象keyのallowlist宣言）の承認が実装の前提

## 最新のauthority／Evidence

- [Intake V4修正 設計提案（承認済み）](docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md) — SHA-256 `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358`
- [Intake V4修正 GREEN Evidence](records/development/2026-08-06-intake-v4-single-candidate-green-evidence-v1.md) — SHA-256 `d63bb9330bbed22f1346618e01ed1710884e55a9e5b3d58686962140b7e7629c`
- [宣言→RED対応表](records/development/2026-08-06-intake-v4-declaration-red-map-v1.json) — SHA-256 `c24ebaf58eee3ce2d318084697051d41c9669e30aa756086706f9f110117ce40`
- [Intake V4 Evidence訂正record](records/development/2026-08-06-intake-v4-evidence-correction-v1.md) — SHA-256 `27db1856b650b23458df49c195544fbfb1f9df5112e3bf85ce16ac670e05df9a`
- [登録した課題record](.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json) — SHA-256 `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`
- [本日の問題一覧（14件）](records/development/2026-08-06-encountered-problem-inventory-v1.md) — SHA-256 `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `53226e7c7c743e145af6fa313e42c2fccdd66f5f41917399b445d8587f022676`
- [深掘りの停止規則Decision](records/development/2026-08-06-deep-dive-stop-rule-decision-v1.md) — SHA-256 `b28e5b2de79f6ccb6df413f4ecc33c64fc29ab55f7f44f944460bba1e4c82401`

## 次に行う一作業

Humanが本線Work 6Aの残り10項目へ戻るか、問題一覧の未解決分のrouteを先に決めるかを判断する。

開始条件：

- Intake V4修正と訂正recordを含むcommitがcleanであること

完了条件：

- 次の一作業がHuman判断として示されること

後続作業：本線へ戻る場合、Work 6A残り10項目の次のRED対象を選定して提示する。

## blocker・Human判断待ち

- blocker：なし。登録した課題の着手、V1凍結レーンの解除、深さ・派生元field追加、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：次の一作業（本線Work 6Aへ戻るか、未解決問題のroute決めか）。

## stale・deferred

- stale：問題一覧の#8（仕分け判断を置けない）と#14（候補が検証されない）は解消した。#9はGREEN Evidence記述の訂正と処置確定により、実装漏れ分（§3.1/§3.2延期など）を残して閉じた。
- deferred：Work 6Aの残り10項目、登録済み4課題の着手・解決計画、深さ・派生元field、Current Work Projection正式写像、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Intake V4単体候補11 passed、Intake関連54 passed
- 直近の全Test：venv公式runner 1031 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
