# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aは再設計済みで、旧patch群を可逆revertした。
- 現在の工程：Work 4A rebuild v2／最小identity chain GREEN。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4A Rebuild Design v2。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4A Rebuild Design v2](docs/design/2026-08-04-work-4a-rebuild-design-v2-proposal.md) — SHA-256 `dfe045f6da57c13f6b42ac41ad18a8c477be07e5eb26eb721cfab88912a7429a`
- [Work 4A Rebuild v2 Approval](records/development/2026-08-04-work-4a-rebuild-design-v2-approval-decision-v1.md) — SHA-256 `fc2fcc232aba35f660c80afb6fc6b437ef0d4f48a1829d1061df53a0f3d5be2a`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `bf25291e574b659339048185b4313134eb6d20b690f314a6ba2b3401a946dec3`

## 次に行う一作業

v2最小identity chainを独立に確認し、actual artifactへ進む前の不足範囲を分類する。

開始条件：

- `DEC-WORK4A-REBUILD-DESIGN-002`によるHuman承認。
- v2 identity chain GREEN containing commit後のclean transition。

完了条件：

- source universe、Policy artifact、Operational Decision、new-only Entry／Relation／Baselineを同じidentity chainで独立照合する。
- actual artifact、既存patchの部分復元を含めない。

後続作業：actual artifact候補をHuman判断用に提示する。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：なし。v2設計承認済み。
- 再開条件：v2 RED acceptance containing commit後のclean transition。

## stale・deferred

- stale：v1設計、v1 E2E test、`c4bfb57`試作module、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。v2 E2EがGREENになるまで再利用しない。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 4A rebuild v2 E2E `4 passed`
- 直近の全Test：venv公式runner `667 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
