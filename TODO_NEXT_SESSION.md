# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：**検証境界の三層すべてが完了した**。反証レビュー第1束の21件は、9件を第1次修正、8件を層1（機械が保証する）・層2（機械が支援する）で機械化、7項目を層3（機械は保証しない）で明示、という形ですべて処置済み。層1にはC-4（関門が名のとおりREDを確認するようになった）を含む。層2は「安全保証ではなく誤記検出」を機械可読に宣言。層3は`tools/development/verification_boundary.py`で「合格＝検証対象外」を明示し、レビュー手順書から導線を張った。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断

## 最新のauthority／Evidence

- [層3 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer3-green-evidence-v1.md) — SHA-256 `4ed47b951ee9ccb8b28389a53ba91414cdf0d38f2eb9d4f3fb383118fc833722`
- [層2 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer2-green-evidence-v1.md) — SHA-256 `dc8a83595c67077460793eb435e8aa65b38623a237ea2d905310a7ed364f18cf`
- [層1 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer1-green-evidence-v1.md) — SHA-256 `baff96b87dd17f52da622f9d984b8836a3cb22922044c987a15ac9c56af71c65`
- [検証境界の設計提案（承認済み）](docs/design/2026-08-07-verification-boundary-proposal.md) — SHA-256 `f904e995003f30d9b7bf92555ac390649b4b084f232d9bc50fac341af6a4f4cb`
- [反証レビュー結果（新module 4件）](records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md) — SHA-256 `2558dd841712d24596ba79513b4e16da6edc0c236ca18d1537d660b72d6df94c`
- [反証レビュー結果（routing・Intake）](records/development/2026-08-07-adversarial-review-batch1-legacy-systems-v1.md) — SHA-256 `b6221cfbf2c1d8b220e0a0fe7087218551bbfed96303b777f3b461a9bcf0900d`
- [I-4処置 GREEN Evidence](records/development/2026-08-07-adversarial-remedy-i4-green-evidence-v1.md) — SHA-256 `fad332129fc7c2cbc84f7cacc1788ff1178ab9a3913e01fc3a461a4297fb7ec1`
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
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `a325a20814ad63131486570a94118b4d665dda88b952cd6fb8af476aec073942`

## 次に行う一作業

反証レビュー第2束：stage期module群（`tools/session_logs/`の伏字化・秘匿検出系ほか）への反証レビュー。トリアージメモ§6の優先度案では、守り役でありながら一度もレビューされていない最後の大きな塊である。まず対象moduleの絞り込み（伏字化・秘匿検出に該当する部分の特定）から始める。

開始条件：

- Humanの着手承認（`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の範囲内だが、第2束の着手は未承認）

完了条件：

- 対象ごとに反証レビューの結果record（欠陥または反証不成立）が固定されること。修正はレビューと分離する

後続作業：合意順序④（RC2資産の取り込み、外部APIによる独立レビュー）。層3で「Humanが担う」と宣言した項目の確認設計はWork 8の評価対象。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：反証レビュー第2束（stage期module群）の着手承認。

## stale・deferred

- stale：なし。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、backlog以外の登録済み課題の着手、Current Work Projection正式写像、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：層1 9 passed＋層2 11 passed＋層3 6 passed＋収集エラー補修 3 passed
- 直近の全Test：venv pytest 1131 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
