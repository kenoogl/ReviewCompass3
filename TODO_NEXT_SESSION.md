# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 4Aのv1 patch群は可逆revert済み。
- 現在の工程：V4 Human triage永続化GREEN。過去TODO候補41件のうち4件をHuman判断済みrecordとして保存。残り37件はHuman triage待ち。
- activeなTask Contract／Work Item：なし。
- 製品実装code：`tools/task_contract/`の最小Runtime packageのみ。
- 当面の進行入口：Work 5A 最小Review Task Contract。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [V4 Human triage永続化 GREEN](records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md) — SHA-256 `41fcbbbd6acc278055dd3e43e64fcb0c603627319eae1fb13b853262bda305d7`
- [過去TODO候補 Human triage資料](records/development/2026-08-05-historical-todo-intake-triage-material-v1.md) — SHA-256 `b2ad5195ffd041a527b8d92f5847606bddcdb5876cacbca05a9a9c304b39efdb`
- [過去TODO候補一覧](records/development/2026-08-05-historical-todo-intake-candidates-v1.json) — SHA-256 `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- [Issue Intake V4 GREEN](records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md) — SHA-256 `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f`
- [Work 5A 実Review受理 v2](records/development/2026-08-05-work5a-first-real-review-acceptance-v2-evidence.md) — SHA-256 `2e8335877202c8d5d1be07978b84ef6b3834ac5a207d5afa1184daddc719acdc`
- [Work 5A 受理record bundle v2](records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json) — SHA-256 `64d75f3568078ef419cf74c3b72632352d07e63449b98fdb1608b17257184e7b`
- [Provenance閉包 無効化record](records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json) — SHA-256 `f3ba011f5490059d96b8f21429cadc8016a9332415d79c59f546447a9c018a29`
- [Work 5A 最初の実Review Run](records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md) — SHA-256 `cdc4c4d8ad08a6f0d8373ea56d46018e070618ba2152ade7ac4dd09d72808b50`
- [Work 5A 実Review Run record bundle](records/development/2026-08-05-work5a-first-real-review-run-records-v1.json) — SHA-256 `658e5ba98d6023085709733f91130a8b64acd674b3c9ca497b3f23784d588447`
- [Work 5A GREEN Evidence](records/development/2026-08-05-work-5a-first-review-contract-green-evidence-v1.md) — SHA-256 `57feb4e7fa08924c00307dec997f2b12285641b168925825225e6a596b63fbae`
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
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `c95ca09fe43a1c8d39f82426396f4cbac7645e18927e5d21e8d01887b2777fdf`

## 次に行う一作業

残り37候補に対するHuman triageを受ける。

開始条件：

- 判断recordのcommit後のclean transition。
- 未解決・再発性・影響・priority・Issue昇格のHuman判断。

完了データ：

- 候補一覧：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`
- 41件（未実施7、残余risk15、手戻り・機械化候補14、blocker・Human判断待ち5）。重複疑い0件。
- 候補一覧の`human_fields`は生成時の未記入観測として全件`null`のまま保持する。判断正本は
  `.reviewcompass/workflow/triage-decisions-v4/`のV4 human triage decision（schema version 2）である。
- 判断済み4件：`HTC-14D810C7`、`HTC-1AB699F7`、`HTC-21C3CE46`、`HTC-6ABDDC35`。いずれも
  `historical_completed`、`promote_to_issue: false`、`blocking: false`。正式Issueへ昇格していない。

後続作業：Humanが昇格を選んだ候補だけのIssue化、Plan化。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：過去TODO候補のうち残り37件のtriage。昇格、priority、統合、根本原因Issue化はHumanが決める。
- 再開条件：判断recordのcommit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。全routineの意味的分類・全件台帳化をWork 4A完了条件とする旧計画。v1／v2試作moduleとE2E testはworking treeから撤去済み。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Issue Intake V4 `32 passed`
- 直近の全Test：venv公式runner `809 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
