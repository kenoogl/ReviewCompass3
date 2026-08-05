# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 4Aのv1 patch群は可逆revert済み。
- 現在の工程：過去TODO候補41件のHuman triageは完了し、Issue Intake V4の限定拡張はHuman承認のうえ検証を閉じた。未判断は0件である。
- 正式Issue：3件、いずれも`registered`かつnonblockingで未着手。active Issueは0件。`ISSUE-HTC-C9F6C917`はPlan提案v2の§3最小縦切り（operation inventory、permission preflight、execution receipt）だけをHuman承認のうえ実装済みで、receipt改竄検出の訂正も完了している（execution receipt schema v2）。Issue全体はcloseしていない。旧v1提案は履歴として保持する。
- 各Issueの対象：`ISSUE-HTC-BEB5E0BD`は会話記録の保存方針が未決定であること、`ISSUE-HTC-C9F6C917`はLLMが機械操作の実行手順を都度組み立てていること、`ISSUE-HTC-66C3E6CA`は記録の定型欄の生成が未機械化であることを追跡する。
- 通常commitの運用：意味単位commitを最小ガード付きで自律化した。push、tag、amend、rebase、reset、force push、履歴書換え、方針変更、段完了、意味的裁定、不可逆操作、外部送信、権限の迂回はHuman明示承認のままである。
- Task Contract固定sourceの状態解決：歴史状態は受理時点のGit blob、現在有効状態はworking tree、`active_stale`は停止のまま、という三状態をv1／v2共通のresolverで扱う。
- activeなTask Contract／Work Item：なし。
- 製品実装code：`tools/task_contract/`の最小Runtime packageのみ。
- 当面の進行入口：Work 5A 最小Review Task Contract。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [V4 Issue永続化 GREEN](records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md) — SHA-256 `3ae17b4b5828429ee8c7f1b6dfbc3b80d9439da4bace685542cee3845640b731`
- [正式Issue record 会話記録方針](.reviewcompass/workflow/issues-v4/issue-htc-beb5e0bd--v1.json) — SHA-256 `a4a1511e609005193a3d127080a3eabf4f56a67529c5bd9b4e0f55b467422d62`
- [正式Issue record 機械操作の根本原因](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`
- [正式Issue record 記録生成の根本原因](.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json) — SHA-256 `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732`
- [意味単位commit最小ガード Decision](records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md) — SHA-256 `07eb9cbcd1e4e1b33aff787f597a45db1be6913a0685d76f8db1169adf965d23`
- [機械操作routing v2 承認Decision](records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md) — SHA-256 `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`
- [receipt整合性 訂正Decision](records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md) — SHA-256 `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b`
- [receipt整合性 訂正GREEN Evidence（有効な完了根拠）](records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md) — SHA-256 `b6255b0a7de3bcd90b62745ff934a957dba94b3870bc847517f1dbde36a430ea`
- [機械操作routing v2 初回GREEN Evidence（stale、履歴）](records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md) — SHA-256 `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb`
- [機械操作routing Plan提案 v2（§3のみ承認済み）](docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md) — SHA-256 `e01c3aaf8039377da2b43dab7f735d28a2f86bf10aa83f5bb22e5dd1eefa8572`
- [機械操作routing Plan提案 v1（superseded、履歴）](docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md) — SHA-256 `722e9448971bcf3e97423ab1b9b137ca202f1f1c0ed7afdd92a619738e608bfa`
- [Issue Intake V4 承認Decision](records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md) — SHA-256 `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c`
- [Issue Intake V4 閉鎖Evidence](records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md) — SHA-256 `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e`
- [receipt整合性GREEN後の全test receipt](records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json) — SHA-256 `9be48428226a5c7d3e302b0ef68d8941cd21974a211892c66a7d8f3eaf8472bf`
- [過去TODO候補一覧](records/development/2026-08-05-historical-todo-intake-candidates-v1.json) — SHA-256 `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- [Work 5A 実Review受理 v2](records/development/2026-08-05-work5a-first-real-review-acceptance-v2-evidence.md) — SHA-256 `2e8335877202c8d5d1be07978b84ef6b3834ac5a207d5afa1184daddc719acdc`
- [Work 5A 受理record bundle v2](records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json) — SHA-256 `64d75f3568078ef419cf74c3b72632352d07e63449b98fdb1608b17257184e7b`
- [Provenance閉包 無効化record](records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json) — SHA-256 `f3ba011f5490059d96b8f21429cadc8016a9332415d79c59f546447a9c018a29`
- [Work 5A 最初の実Review Run](records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md) — SHA-256 `cdc4c4d8ad08a6f0d8373ea56d46018e070618ba2152ade7ac4dd09d72808b50`
- [Work 5A 実Review Run record bundle](records/development/2026-08-05-work5a-first-real-review-run-records-v1.json) — SHA-256 `658e5ba98d6023085709733f91130a8b64acd674b3c9ca497b3f23784d588447`
- [Work 5A GREEN Evidence](records/development/2026-08-05-work-5a-first-review-contract-green-evidence-v1.md) — SHA-256 `57feb4e7fa08924c00307dec997f2b12285641b168925825225e6a596b63fbae`
- [Work 4 最初のslice設計承認](records/development/2026-08-05-work4-first-review-contract-design-approval-decision-v1.md) — SHA-256 `3048a52ccab59815f92b6fc3d1bd88b0ca8bd5d7a5117ad223d7139dab287675`
- [Work 4 最初のReview Task Contract設計提案](docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md) — SHA-256 `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054`
- [Work 4A Rebuild Design v3.3 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md) — SHA-256 `b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- [Work 4A Early Exit / Work 4B Decision](records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md) — SHA-256 `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `ca1e62f8b43f9bf26ce7fd250a8daad90af82ec699a1bd0124096c786e50da0d`

## 次に行う一作業

後続範囲（構造化argv executor、cache root固定、既存直接操作の移行順）を扱うかどうかのHuman判断を受ける。

開始条件：

- 最小縦切りGREENのcommit後のclean transition。
- 後続範囲に着手するか、別Issueを先にするかのHuman判断。

完了データ：

- 候補一覧：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`（41件、重複疑い0件）
- 候補一覧の`human_fields`は生成時の未記入観測として全件`null`のまま保持する。判断正本は
  `.reviewcompass/workflow/triage-decisions-v4/`のV4 human triage decision（schema version 2）である。
- 判断済み41件（全件）。うち正式Issueへ昇格したのは`HTC-BEB5E0BD`、`HTC-C9F6C917`、`HTC-66C3E6CA`の3件である。
- Issue Intake V4は開発用・暫定の限定機能としてHuman承認済みで、実地検証は閉鎖済みである。
- `ISSUE-HTC-C9F6C917`のPlan提案v2は`approved_for_development_implementation`だが、承認範囲は§3だけである。旧v1提案は状態を変えずに履歴として残す。正式Issue Resolution PlanとTask Contractは作っていない。
- §3の実装（`tools/development/operation_routing.py`）は完了し、receipt改竄検出の訂正も適用済み。初回のGREEN Evidenceとreceiptはstaleとして履歴に残し、有効な完了根拠は訂正Decisionと訂正GREEN Evidenceである。構造化argv executor、cache root固定、既存直接操作の移行、host側tool構文、外部送信は未実施である。
- `DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`は通常commitの運用だけを確定したものであり、C9 Plan提案の承認ではない。
- 正式Issue正本：`.reviewcompass/workflow/issues-v4/`（V4 issue_record schema version 2）

後続作業：後続範囲の個別Plan。着手が承認されるまで、argv executor、cache root固定、既存直接操作の置換、host側tool構文、外部送信は行わない。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：`ISSUE-HTC-C9F6C917`の後続範囲に着手するかどうかの判断。§3最小縦切りは承認・実装済みで、Issue全体はcloseしていない。過去TODO候補41件のHuman triageとV4検証閉鎖は完了している。`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`はいずれも`registered`かつnonblockingのままで、作業を開始していない。
- 再開条件：判断recordのcommit後のclean transition。

## stale・deferred

- stale：v1設計、v2設計、旧Work 4AのSource Snapshot、Index、Candidate、Ledger、Policy状態を根拠にしたEvidence。全routineの意味的分類・全件台帳化をWork 4A完了条件とする旧計画。v1／v2試作moduleとE2E testはworking treeから撤去済み。
- deferred：正式Issue Resolution schema、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Issue Intake V4 `38 passed`
- 直近の全Test：venv公式runner `829 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
