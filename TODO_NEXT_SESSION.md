# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 6Aは11項目中6件が完了した（欠落検出、区別、validator検査、第二正本化等の検出、表示器failure分離、意図毀損検出）。残り5件は基盤未整備4件（行き先明記済み：正式Workflow state、Work 4B、Work 7、Requirement差分）と段の関門1件で、対象能力がPortfolioへ入った時点で負例として有効化する。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提

## 最新のauthority／Evidence

- [意図毀損検出 設計提案（承認済み）](docs/design/2026-08-06-final-challenge-intent-damage-proposal.md) — SHA-256 `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6`
- [CL-6A-01/02/03完了Decision](records/development/2026-08-06-work6a-cl-6a-01-02-03-completion-decision-v1.md) — SHA-256 `87af326bb73b5af275a1a5896798c97782cbc29257f566b0a7e8611bc23ea7d9`
- [CL-6A-10完了Decision](records/development/2026-08-06-work6a-cl-6a-10-completion-decision-v1.md) — SHA-256 `efd3a577129a1b12c264a300f6743b9d149bd00f002cefac84fe1d433f9ce42a`
- [意図毀損 GREEN Evidence](records/development/2026-08-06-intent-damage-green-evidence-v1.md) — SHA-256 `81ad5060eeb50c176e93cc5ee5a7df57d6085a53a3f1b7d70f6aa4adba91645c`
- [意図毀損 宣言→RED対応表](records/development/2026-08-06-intent-damage-declaration-red-map-v1.json) — SHA-256 `80decdaa37ac8a0f977128d7a7866c6e00c6defd58faacf32eceeeb2a90ae3d0`
- [意図毀損 RED Evidence](records/development/2026-08-06-intent-damage-red-evidence-v1.md) — SHA-256 `9950c141e5dcb6bd485857fcf3e34ae2372f61bee705a84cf92aa3fafedde047`
- [テスト増加の課題record](.reviewcompass/workflow/issues-v4/issue-test-growth-state-pinning-001--v1.json) — SHA-256 `13f4c9a68d90105e66f3e3b5fb2df36b334f7921ee69430b82e85cf40b6f8194`
- [本日の問題一覧（14件）](records/development/2026-08-06-encountered-problem-inventory-v1.md) — SHA-256 `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b`

## 次に行う一作業

Humanが次の一作業を判断する。Work 6Aでいま届く範囲は出し切った。候補は、初期実装順12（Work 4B最小Pilot）への前進、登録済み5課題からの着手選定、または区切りである。

開始条件：

- 本完了反映commitがcleanで全Testが緑であること

完了条件：

- 次の一作業がHuman判断として示されること

後続作業：Work 4Bへ進む場合は対象routineの再利用検索と記録方法の確認から始める（Current Plan §17実装順12）。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：次の一作業の選定（Work 4B前進／課題着手／区切り）。

## stale・deferred

- stale：CL-6A-01/02/03の部分被覆表示は完了へ変わった。crash実地復旧はWork 7Aへ、誤停止測定はWork 8へ移管済み。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、登録済み5課題の着手、Current Work Projection正式写像、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

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
