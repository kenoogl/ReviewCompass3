# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aはv3設計を承認済みで、v1 patch群を可逆revert済み。
- 現在の工程：Work 4A rebuild v3.3／設計確定。Comparison Discoveryの実装へ進む。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4A Rebuild Design v3.3。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4A Rebuild Design v3](docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md) — SHA-256 `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37`
- [Work 4A Rebuild v3 Approval](records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md) — SHA-256 `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1`
- [Work 4A v3 Actual Observation](records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md) — SHA-256 `75e0eb3d30c4ec559b33e3f9678ff8bbf1752d3a20f6b6a1f5ec4631d9cf25b1`
- [Work 4A Rebuild Design v3.1](docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md) — SHA-256 `5839e37467aaa7d06ee2e9bde477e6c6a76da57e6f4b8a9653e1c9551cea5e40`
- [Work 4A v3.2 Routine Profile v2](records/development/2026-08-05-work-4a-v3-2-actual-routine-profile-v2-evidence-v1.md) — SHA-256 `737ebf873fd2544a5a799f52339132241d79446019623d66398e471280a0ed35`
- [Work 4A Rebuild Design v3.2 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md) — SHA-256 `b157640f940c12d733d237921cad664dbebc4925c592796394f29da1155f5e48`
- [Work 4A Rebuild Design v3.3 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md) — SHA-256 `b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `b5a18fb4da194779c2a1bf8010e9d1418377d3b30bfc92d5d8336965eeab6d7c`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `6a68980e2e0817b9938c5730341660bcaabea4c73238ab280b47658d051d0557`

## 次に行う一作業

K1〜K12をREDで固定し、Profile v3とComparison Discoveryの実装でGREENにする。

開始条件：

- `DEC-WORK4A-REBUILD-DESIGN-006`によるHuman承認。
- 設計確定commit後のclean transition。

完了条件：

- Policy v4でgrouping ruleと表示classを固定する。
- K1〜K12と負例をREDで固定し、期待を緩めずGREENにする。
- 実sourceを再観測し、Profile v3とComparison Discoveryをnew-onlyで生成する。

後続作業：group統計の提示、LLMによるDisposition Proposal生成の別承認。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：LLMによるDisposition Proposal生成の承認。v3.3の実データ確認後とする。
- 再開条件：設計確定commit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。v1／v2試作moduleとE2E testはworking treeから撤去済み。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 4A v3.2 acceptance `11 passed`、v3.1 `21 passed`、v3 `22 passed`
- 直近の全Test：venv公式runner `724 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
