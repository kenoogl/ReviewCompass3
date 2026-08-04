# TODO_NEXT_SESSION

更新日：2026-08-04

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3が完了。Work 4Aはv3設計を承認済みで、v1 patch群を可逆revert済み。
- 現在の工程：Work 4A rebuild v3.1／設計提案を作成済み、Human承認待ち。Observationと初回Candidate Runは完了済み。v3.1のRoutine ProfileとDisposition Proposalは未着手。
- activeなTask Contract／Work Item：なし。
- 製品実装code：未着手。
- 当面の進行入口：Work 4A Rebuild Design v3.1 Amendment。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [Work 4A Rebuild Design v3](docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md) — SHA-256 `a9e0419dcac556789e82f6f51292dd70399000f988e0720d240286c9a05c2b37`
- [Work 4A Rebuild v3 Approval](records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md) — SHA-256 `c358f730c84d2cdc3d981c7668d21f1898a12eadd04e9af04800b9c5f26900a1`
- [Work 4A v3 Actual Observation](records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md) — SHA-256 `75e0eb3d30c4ec559b33e3f9678ff8bbf1752d3a20f6b6a1f5ec4631d9cf25b1`
- [Work 4A Rebuild Design v3.1 提案](docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md) — SHA-256 `5056e9d2eb04f53d4f09c69eb93a11998309c45787f0c7b0632f841fe8cf8b12`
- [conformance-evaluation緩和提案](docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md) — SHA-256 `67b1bc3b95dd573065367a9f08d13803fe3cdfb5d4f4b6cb9fc110e43aee8416`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `9bd03b0fa801fd08335ebb0772de13cd29bffff71ba790053aac96f53f3108ef`

## 次に行う一作業

v3.1設計とconformance-evaluation利用範囲のHuman承認を得る。

開始条件：

- 提案文書commit後のclean transition。

完了条件：

- v3.1改訂案と緩和提案をHumanが承認または差し戻す。
- 未決五点（lambda、group条件記法、例外class既定、Proposal生成単位、nested function既定）を判断する。
- 承認された場合にだけDecision recordを作成する。

後続作業：Policy v2固定、受入test I1〜I21のRED、Routine Profile実装。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：v3.1設計およびconformance-evaluation利用範囲のHuman承認。未決五点の判断。
- 再開条件：提案文書commit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。v1／v2試作moduleとE2E testはworking treeから撤去済み。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 4A v3 acceptance `22 passed`
- 直近の全Test：venv公式runner `681 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
