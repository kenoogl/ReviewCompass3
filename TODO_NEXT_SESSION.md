# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：**Work 4B本体設計束の4構成すべてが完了した**（A-1除外宣言、B鮮度gate、A-2順位表、D台帳=既存経路再利用、C外部化）。Cでは検索record 7件を全件byte一致で外部化し証明書をproject内へ作成（旧位置は保持）。universe v2も作成したが、`validate_current`の停止原因は**freshness policy v4自身の開発方針参照**と再特定され（診断訂正Evidence参照）、policy v5の作成がHuman判断待ち。参照Digest drift類型は4例目となった。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断

## 最新のauthority／Evidence

- [構成C GREEN Evidence](records/development/2026-08-07-work4b-c-externalization-green-evidence-v1.md) — SHA-256 `a6ee5742a9bc9174db60304a9d6d7767a6ecc9d7159f276336896d33815543b4`
- [universe v2結果・診断訂正Evidence](records/development/2026-08-07-universe-v2-outcome-evidence-v1.md) — SHA-256 `0a06cb014652efedbd1c52139d9448c6a31506cad02eab8ad93a8b9f1100b7c8`
- [構成D 初回実運用Evidence](records/development/2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md) — SHA-256 `f416a360bd9cd09f2646db4f5089fc0805624e26e44c6b8bffeb2b56297628a0`
- [構成A-2 GREEN Evidence](records/development/2026-08-07-work4b-a2-candidate-ranking-green-evidence-v1.md) — SHA-256 `7ce86a44e5ef270875135ce8d9c82017152db82302d76e29db750a5cb2bd96eb`
- [実順位表v1](records/development/2026-08-07-candidate-ranking-v1.json) — SHA-256 `7b02535390547f169b1643f2314979ca9bc5dfb7df8e59a9a99a942f3c09cfee`
- [構成B GREEN Evidence](records/development/2026-08-07-work4b-b-reuse-search-freshness-green-evidence-v1.md) — SHA-256 `cbf5a22317c8aa622a3bdd462ee521f93ba0ab5e662df57135c0287114de9877`
- [構成A-1 GREEN Evidence](records/development/2026-08-07-work4b-a1-integration-exclusions-green-evidence-v1.md) — SHA-256 `91910e837710140a43e0b060832b3726a1b11a5348a7ee4b59cc95b19467a153`
- [統合除外宣言record](.reviewcompass/workflow/integration-exclusions/integration-exclusions-001--v1.json) — SHA-256 `f482bf3d6200e1c2a4fc17233d4e87ed098f04d053dc1fa56e69e481a4b090fd`
- [設計束 承認Decision](records/development/2026-08-07-work4b-main-design-bundle-approval-decision-v1.md) — SHA-256 `6bbaea795f7280f006dce2834b0286bb7df0b1cdb05b12918d2ce7574c27bf5e`
- [設計束提案（承認済み）](docs/design/2026-08-07-work-4b-main-design-bundle-proposal.md) — SHA-256 `14c629d2f45a1dd36cbb3ed60b311ead2898c1e07fe71ffc8e5d2c6365234b5b`
- [設計議論の証跡Decision](records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md) — SHA-256 `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d`
- [Work 5B検査器 GREEN Evidence](records/development/2026-08-07-work5b-checker-green-evidence-v1.md) — SHA-256 `020db589b586e6db741e0d5d347d31c30c89a077c390ebd2232c42dfccbb7d2c`
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `fb48732e7445ef4d28fdca0a44691eceb31f39760099d2426014220267e5883d`

## 次に行う一作業

合意順序（DEC-WORK5B-DISCUSSION-OUTCOMES-001 §2）の③：レビューbacklog上位2系統（operation_routing系、Issue・候補の合否を決める検証器群）への先行反証レビュー。着手には`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の`in_progress`化が必要で、これはHuman判断である（同Decision §3）。

開始条件：

- Humanがbacklog Issueの`in_progress`化と上位2系統の着手を承認すること
- 反証レビューはwork-review-protocol §4.4（fixtureに無い反証の新作）・§5（上流からの独立oracle導出）に従う

完了条件：

- 上位2系統それぞれについて、反証レビューの結果record（見つかった欠陥または反証不成立の記録）が固定されること。欠陥の修正はレビューと分離する

後続作業：合意順序の③レビューbacklog上位2系統の先行反証レビュー、④残りのbacklogとRC2取り込み・外部APIレビュー（台帳整備後）。全routineの一括分類は行わない。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：(1) freshness policy v5の作成可否（validate_current停止の残余処置。参照現行化のみ、語彙・閾値変更なし）。(2) レビューbacklog Issueの`in_progress`化と上位2系統着手（次の一作業の開始条件）。(3) Work 5Bの段完了（全6項目がEvidence接続済み）。(4) 外部化済み旧record 7件と旧書庫の削除可否（削除でrepositoryが約2.3MB軽くなる）。

## stale・deferred

- stale：なし。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、登録済み7課題の着手、旧書庫の削除判断、Current Work Projection正式写像、Entry・Relation・Baseline台帳、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：外部化 4 passed（宣言H1〜H4対応）＋検索系既存 12 passed
- 直近の全Test：venv pytest 1084 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
