# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aは再設計済みで、旧patch群を可逆revertした。
- 現在の工程：Work 4A rebuild／E2E acceptance RED。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4A Rebuild Design。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4A Rebuild Design](docs/design/2026-08-04-work-4a-rebuild-design-proposal.md) — SHA-256 `233ac821e6f55b34ab31219e55bf9f23b19f2e97d2884e34be6fa191b87dda2a`
- [Work 4A Rebuild Approval](records/development/2026-08-04-work-4a-rebuild-design-approval-decision-v1.md) — SHA-256 `dfa69cabf35cf5e1c40b26eab6044250b270fcdc9fc8e45b9c9b5e71ffdcdf59`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `7535f96513fdc618a9836ebbe04e3ffd6d93023ca77b09e5b1fe995be93d4e8e`

## 次に行う一作業

Work 4A再設計の七項目を、一つのE2E acceptance test群としてREDで固定する。

開始条件：

- `DEC-WORK4A-REBUILD-DESIGN-001`によるHuman承認。
- revert commit後のclean transition。

完了条件：

- new-only Entry／Relation／Baseline、content-based freshness、Historical Contract Status、負例を含む受入testが意図どおりREDになる。
- production implementation、actual artifact、既存patchの部分復元を含めない。

後続作業：RED testを変更せず、最小のidentity chain実装をGREENにする。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：なし。設計承認済み。
- 再開条件：RED acceptance containing commit後のclean transition。

## stale・deferred

- stale：旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。rebuild E2EがGREENになるまで再利用しない。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：TODO handoff validation、post-write verification／restore rehearsal合格
- 直近の全Test：venv公式runner `659 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
