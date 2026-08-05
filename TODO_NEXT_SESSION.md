# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。過去sessionの詳細はここへ累積しない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 4Aのv1 patch群は可逆revert済み。
- 現在の工程：過去TODO候補41件のHuman triageは完了し、Issue Intake V4の限定拡張はHuman承認のうえ検証を閉じた。未判断は0件である。
- 正式Issue：3件、いずれも`registered`かつnonblockingで未着手。active Issueは0件。`ISSUE-HTC-C9F6C917`はPlan提案v2の§3最小縦切り（operation inventory、permission preflight、execution receipt）だけをHuman承認のうえ実装済みで、receipt改竄検出の訂正も完了している（execution receipt schema v2）。Issue全体はcloseしていない。旧v1提案は履歴として保持する。
- 各Issueの対象：`ISSUE-HTC-BEB5E0BD`は会話記録の保存方針が未決定であること、`ISSUE-HTC-C9F6C917`はLLMが機械操作の実行手順を都度組み立てていること、`ISSUE-HTC-66C3E6CA`は記録の定型欄の生成が未機械化であることを追跡する。`ISSUE-HTC-66C3E6CA`は`registered`かつnonblockingのままで、Plan提案はHuman承認済みである。TODO最小縦切り（受領証の集計、TODO用材料の収集、更新経路の切替）は実装済みで、参照範囲とactive IDの正本に関する境界訂正も完了している。初回のGREEN Evidenceとreceiptは境界不足があった初回根拠としてstaleのまま履歴に残し、有効な完了根拠は境界訂正GREEN Evidenceと訂正最終receiptである。
- 通常commitの運用：意味単位commitを最小ガード付きで自律化した。push、tag、amend、rebase、reset、force push、履歴書換え、方針変更、段完了、意味的裁定、不可逆操作、外部送信、権限の迂回はHuman明示承認のままである。
- Task Contract固定sourceの状態解決：歴史状態は受理時点のGit blob、現在有効状態はworking tree、`active_stale`は停止のまま、という三状態をv1／v2共通のresolverで扱う。
- activeなTask Contract／Work Item：なし。
- 製品実装code：`tools/task_contract/`の最小Runtime packageのみ。
- 当面の進行入口：Work 5A 最小Review Task Contract。
- Evidence参照：`## 最新のauthority／Evidence`節の参照は機械計測で28件である。件数の訂正記録は`records/development/2026-08-05-todo-evidence-reference-count-correction-v1.md`。

## 現在作業に影響する改善候補／Issue

- `ISSUE-PILOT-TODO-GROWTH-001`：resolved。現行Workへの影響なし。TODOは現在の入口だけを表示し、詳細は正本recordを参照する。

## 最新のauthority／Evidence

- [読み取り専用argv executor 承認Decision](records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md) — SHA-256 `2982646b43a74d856d9b18af527b743b10ac3d8874f03ee39afba825752a8864`
- [機械操作routing 後続Plan提案（§2.1／§3.2のみ承認済み）](docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md) — SHA-256 `d5877f9668cc75a00a25b79d0fad9050c7ae3dd243047a4c61ba6e776fceb571`
- [承認記録時点の全test receipt](records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-test-receipt-v1.json) — SHA-256 `85f411ad3083ee7580e140dce3d0c858bebf4ad1e3ae3a2c032ce9122f5d0d39`
- [V4 Issue永続化 GREEN](records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md) — SHA-256 `3ae17b4b5828429ee8c7f1b6dfbc3b80d9439da4bace685542cee3845640b731`
- [正式Issue record 会話記録方針](.reviewcompass/workflow/issues-v4/issue-htc-beb5e0bd--v1.json) — SHA-256 `a4a1511e609005193a3d127080a3eabf4f56a67529c5bd9b4e0f55b467422d62`
- [正式Issue record 機械操作の根本原因](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`
- [正式Issue record 記録生成の根本原因](.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json) — SHA-256 `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732`
- [意味単位commit最小ガード Decision](records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md) — SHA-256 `07eb9cbcd1e4e1b33aff787f597a45db1be6913a0685d76f8db1169adf965d23`
- [機械操作routing v2 承認Decision](records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md) — SHA-256 `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`
- [receipt整合性 訂正Decision](records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md) — SHA-256 `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b`
- [receipt整合性 訂正GREEN Evidence（有効な完了根拠）](records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md) — SHA-256 `b6255b0a7de3bcd90b62745ff934a957dba94b3870bc847517f1dbde36a430ea`
- [機械操作routing Plan提案 v2（§3のみ承認済み）](docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md) — SHA-256 `e01c3aaf8039377da2b43dab7f735d28a2f86bf10aa83f5bb22e5dd1eefa8572`
- [Issue Intake V4 承認Decision](records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md) — SHA-256 `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c`
- [Issue Intake V4 閉鎖Evidence](records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md) — SHA-256 `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e`
- [定型記録生成 境界訂正GREEN Evidence（有効な完了根拠）](records/development/2026-08-05-record-generation-todo-boundary-repair-green-evidence-v1.md) — SHA-256 `0f4e4031b541a06e431c56de2e1d19c0626aeadb1068a66ee9f392bb9e749634`
- [境界訂正後の全test receipt](records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json) — SHA-256 `ad0f191e0af53a21ab130d9346743d0b214ac56ad6cf958b64ae175535df98df`
- [定型記録生成 Plan提案（承認済み）](docs/design/2026-08-05-record-generation-issue-plan-proposal.md) — SHA-256 `79ed49831ebd9b69c9713fcd71becfaa1d85f7fd97759e5fff373f99126a2a7c`
- [Plan提案作成後の全test receipt](records/development/2026-08-05-record-generation-issue-plan-proposal-test-receipt-v1.json) — SHA-256 `d2320449185d783860312a3cc4b5b232a60d861bf5bf123f4794aaefc9927b92`
- [過去TODO候補一覧](records/development/2026-08-05-historical-todo-intake-candidates-v1.json) — SHA-256 `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`
- [Work 5A 最初の実Review Run](records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md) — SHA-256 `cdc4c4d8ad08a6f0d8373ea56d46018e070618ba2152ade7ac4dd09d72808b50`
- [Work 5A GREEN Evidence](records/development/2026-08-05-work-5a-first-review-contract-green-evidence-v1.md) — SHA-256 `57feb4e7fa08924c00307dec997f2b12285641b168925825225e6a596b63fbae`
- [Work 4 最初のslice設計承認](records/development/2026-08-05-work4-first-review-contract-design-approval-decision-v1.md) — SHA-256 `3048a52ccab59815f92b6fc3d1bd88b0ca8bd5d7a5117ad223d7139dab287675`
- [Work 4 最初のReview Task Contract設計提案](docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md) — SHA-256 `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054`
- [Work 4A Rebuild Design v3.3 Proposal](docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md) — SHA-256 `b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- [Work 4A Early Exit / Work 4B Decision](records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md) — SHA-256 `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `ca1e62f8b43f9bf26ce7fd250a8daad90af82ec699a1bd0124096c786e50da0d`

## 次に行う一作業

`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`で承認された読み取り専用argv executor
最小sliceを、Test先行で実装する。

開始条件：

- 本handoffを含むcommit後のclean transition。
- 承認範囲を超えないこと。cache root、移行、書込み、externalは対象外のままとする。

未承認のまま残るHuman判断点：

- cache rootの配置と、削除するか保持するかの方針。
- 移行対象の優先順。
- host側tool構文と外部送信を本Issueで扱わないことの確認。

完了データ：

- 過去TODO候補41件は全件triage済み。正式Issueは3件で、正本は`.reviewcompass/workflow/issues-v4/`である。
- `ISSUE-HTC-C9F6C917`は§3最小縦切りが承認・実装済みで、`registered`かつnonblockingのままである。後続Plan全体は`awaiting_human_approval`のままだが、読み取り専用argv executor最小sliceだけは`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`で実装承認された。実行templateは`git status --porcelain`だけで、cache root、既存操作の移行、書込み、externalは対象外である。
- `ISSUE-HTC-66C3E6CA`はTODO最小縦切りだけ承認・実装済み。案Bは未承認である。
- `DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`は通常commitの運用だけを確定したものである。

後続作業：後続範囲の個別Plan。着手が承認されるまで、argv executor、cache root固定、既存直接操作の置換、host側tool構文、外部送信は行わない。

## blocker・Human判断待ち

- blocker：なし。
- Human判断待ち：`ISSUE-HTC-C9F6C917`の後続範囲に着手するかどうかの判断。`ISSUE-HTC-66C3E6CA`はPlan承認済みで、Evidence／Decisionへの拡張はTODOでの実運用が手入力訂正なしで複数回通ってから判断する。§3最小縦切りは承認・実装済みで、Issue全体はcloseしていない。過去TODO候補41件のHuman triageとV4検証閉鎖は完了している。`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`はいずれも`registered`かつnonblockingのままで、作業を開始していない。
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
- 直近の全Test：venv公式runner `892 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
