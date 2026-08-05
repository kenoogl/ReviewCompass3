# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 4Aのv1 patch群は可逆revert済み。
- 現在の工程：Work 4／最初のReview Task Contract設計提案を作成済み、Human承認待ち。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4 最初のReview Task Contract設計提案。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4 最初のReview Task Contract設計提案](docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md) — SHA-256 `b5ca289307ba053fbdbf4a78facac4ff7112bef16ce83d692a6d46fa50138194`
- [Work 4A Rebuild Design v3](docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md) — SHA-256 `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37`
- [Work 4A Rebuild v3 Approval](records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md) — SHA-256 `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1`
- [Work 4A v3 Actual Observation](records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md) — SHA-256 `75e0eb3d30c4ec559b33e3f9678ff8bbf1752d3a20f6b6a1f5ec4631d9cf25b1`
- [Work 4A Rebuild Design v3.1](docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md) — SHA-256 `5839e37467aaa7d06ee2e9bde477e6c6a76da57e6f4b8a9653e1c9551cea5e40`
- [Work 4A v3.3 Comparison Discovery](records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md) — SHA-256 `2cbefe548462d5c05a4cdba263decc074739d0933e4fe8fa688b219e92fd5d02`
- [Work 4A Rebuild Design v3.2 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md) — SHA-256 `b157640f940c12d733d237921cad664dbebc4925c592796394f29da1155f5e48`
- [Work 4A Rebuild Design v3.3 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md) — SHA-256 `b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- [Work 4A Early Exit / Work 4B Decision](records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md) — SHA-256 `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `fe26afde36acd46b8485a25eccd2c5cc36a44a0546ca00f1af129ac8a4edd52b`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `b63e6e059fefc9511ed9409b7286efa41a607c95882a53776716625ffcd924a7`

## 次に行う一作業

Work 4設計提案のHuman承認を得る。

開始条件：

- 設計提案commit後のclean transition。

完了条件：

- 対象scenario、Contract構造、record順序、負例、Work 5A範囲、Requirement対応をHumanが承認または差し戻す。
- §9の五点と§11.3の後続評価三点を判断する。
- 承認された場合にだけDecision Recordを作成する。

後続作業：Work 5AのRED受入固定と最小componentの実装。E2以降の後続評価は別作業単位とする。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：Work 4設計提案の承認と§9の五点。Work 4Aの実データは提示済み。
- 再開条件：設計提案commit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。全routineの意味的分類・全件台帳化をWork 4A完了条件とする旧計画。v1／v2試作moduleとE2E testはworking treeから撤去済み。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 4A v3.3 acceptance `15 passed`、v3.2 `11 passed`、v3.1 `21 passed`、v3 `22 passed`
- 直近の全Test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
