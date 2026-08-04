# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aはv3設計を承認済みで、v1 patch群を可逆revert済み。
- 現在の工程：Work 4A rebuild v3／commit済みv2試作のrevert提示。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4A Rebuild Design v3。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4A Rebuild Design v3](docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md) — SHA-256 `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37`
- [Work 4A Rebuild v3 Approval](records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md) — SHA-256 `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `bf25291e574b659339048185b4313134eb6d20b690f314a6ba2b3401a946dec3`

## 次に行う一作業

commit済みv2試作のrevert対象を提示し、Humanのrevert承認を得る。

開始条件：

- `DEC-WORK4A-REBUILD-DESIGN-003`によるHuman承認。
- v3設計・Decision・本handoffを含む設計commit後のclean transition。

完了条件：

- revert対象commit、対象path、保持対象、影響を一度だけ提示する。
- Humanのrevert承認後、別作業単位でrevertし、revert mapをnew-only保存する。

後続作業：v3設計§17 A〜HのRED testを固定し、GREEN、全test、commitまで進める。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：commit済みv2試作のrevert承認。actual artifactの対象routine選定とdispositionは後続。
- 再開条件：設計commit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、v1／v2 E2E test、`c4bfb57`と`33218e0`の試作module、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。v3 E2EがGREENになるまで再利用しない。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：v3設計commitではTestを実行していない（設計・記録のみの変更）
- 直近の全Test：venv公式runner `667 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
