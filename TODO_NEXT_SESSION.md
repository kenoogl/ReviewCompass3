# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 4Aのv1 patch群は可逆revert済み。
- 現在の工程：Work 5A／最小Review Task Contractの実装。Work 4の最初のslice設計は承認済み。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 5A 最小Review Task Contract。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4 最初のslice設計承認](records/development/2026-08-05-work4-first-review-contract-design-approval-decision-v1.md) — SHA-256 `3048a52ccab59815f92b6fc3d1bd88b0ca8bd5d7a5117ad223d7139dab287675`
- [Work 4 最初のReview Task Contract設計提案](docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md) — SHA-256 `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054`
- [Work 4A Rebuild Design v3](docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md) — SHA-256 `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37`
- [Work 4A Rebuild v3 Approval](records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md) — SHA-256 `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1`
- [Work 4A v3 Actual Observation](records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md) — SHA-256 `75e0eb3d30c4ec559b33e3f9678ff8bbf1752d3a20f6b6a1f5ec4631d9cf25b1`
- [Work 4A Rebuild Design v3.1](docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md) — SHA-256 `5839e37467aaa7d06ee2e9bde477e6c6a76da57e6f4b8a9653e1c9551cea5e40`
- [Work 4A v3.3 Comparison Discovery](records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md) — SHA-256 `2cbefe548462d5c05a4cdba263decc074739d0933e4fe8fa688b219e92fd5d02`
- [Work 4A Rebuild Design v3.2 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md) — SHA-256 `b157640f940c12d733d237921cad664dbebc4925c592796394f29da1155f5e48`
- [Work 4A Rebuild Design v3.3 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md) — SHA-256 `b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- [Work 4A Early Exit / Work 4B Decision](records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md) — SHA-256 `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `df5590903bd0a77cde65450b506843cc19ccb05538c4c59e15cd8ac1463db983`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `c986951795330931842f01173cf3919e09da37900d4b34adfd006cfdde8337a7`

## 次に行う一作業

A1〜A11、B1〜B10、C1〜C4をREDで固定し、`tools/task_contract/`の最小Runtime実装でGREENにする。

開始条件：

- `DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`によるHuman承認。
- 設計確定commit後のclean transition。

完了条件：

- 受入25件をREDで固定し、期待を緩めずGREENにする。
- Requirement binding からaccepted artifactまでのrecordを、identity・version・Digest・上流参照付きで作る。
- 実文書へのreview run、Human decision、accepted artifactを作らない。

後続作業：実review runの承認、後続評価E2以降の別承認。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：実review runの実施承認。後続評価E2、E4、E5の開始承認。
- 再開条件：設計確定commit後のclean transition。

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
