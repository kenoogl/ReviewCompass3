# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：セッションログ書庫のLayout v3移行が完了した（12検査全合格、冪等unchanged、旧書庫はrollback保持）。HumanがWork 4B最小試行（Current Plan §17実装順12）への前進を選定した。着手前の範囲確定が次である。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提

## 最新のauthority／Evidence

- [書庫移行 Receipt](records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json) — SHA-256 `29a3af432c408e8f479a747706cc8ce406c9c7d123c95d02cbb4f02719235914`
- [書庫移行 Evidence](records/development/2026-08-07-preservation-layout-v3-migration-evidence-v1.md) — SHA-256 `7e5f8b3701d9df8498d972f42a528552ee96d88eca92845f197ad86df812653f`
- [書庫移行 承認Decision](records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md) — SHA-256 `b9aa5bc3bc2f6324e42032d3537e3b96f48a63e44c19f530dddafbcf0054843e`
- [意図毀損検出 設計提案（承認済み）](docs/design/2026-08-06-final-challenge-intent-damage-proposal.md) — SHA-256 `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6`
- [テスト増加の課題record](.reviewcompass/workflow/issues-v4/issue-test-growth-state-pinning-001--v1.json) — SHA-256 `13f4c9a68d90105e66f3e3b5fb2df36b334f7921ee69430b82e85cf40b6f8194`
- [本日の問題一覧（14件）](records/development/2026-08-06-encountered-problem-inventory-v1.md) — SHA-256 `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `a089ffdf5e538e28457894fb6a120ef065d2b8a0acb3c392d4dedaeacdecbd9d`
- [CL-6A-10完了Decision](records/development/2026-08-06-work6a-cl-6a-10-completion-decision-v1.md) — SHA-256 `efd3a577129a1b12c264a300f6743b9d149bd00f002cefac84fe1d433f9ce42a`

## 次に行う一作業

Work 4B最小試行の範囲提案を作り、Human承認を得る。承認後にREDへ進む。

開始条件：

- Work 4Bの承認済み境界（Current Plan §12 Work 4B、DEC-WORK4A-EARLY-EXIT-001）を照合すること
- 対象routineの選定基準と記録方法を提案で固定すること

完了条件：

- 範囲提案がHuman承認され、宣言→RED対応表の関門を経てREDが固定されること

後続作業：Work 4B最小試行の後、Work 5B（内部Implementation Task Contract Pilot）でgateを実証する。全routineの一括分類は行わない。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：Work 4B最小試行の範囲提案の承認（提案提示後）。旧書庫の削除可否は別途判断。

## stale・deferred

- stale：「次の一作業の選定待ち」はHumanのA選定により解消した。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、登録済み5課題の着手、旧書庫の削除判断、Current Work Projection正式写像、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：書庫移行 7 passed、Intake V4単体候補11 passed
- 直近の全Test：venv公式runner 1047 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
