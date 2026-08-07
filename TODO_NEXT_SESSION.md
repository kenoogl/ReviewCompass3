# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 5Bの対象helper（宣言→RED対応表検査器）がGREENと第一実運用まで完了した。検査gateの実証（実装前検索record→gate→Contract→red→implementation_ready→green）を一周し、恒久tool化が成立。第一実運用は4枚中3枚passed（自己検査passed）、Intake V4対応表に実在所見2件——処置はHuman判断待ち。設計議論の合意はDEC-WORK5B-DISCUSSION-OUTCOMES-001へ証跡化済み。台帳更新の項目だけ台帳未整備のため残る。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断

## 最新のauthority／Evidence

- [Work 5B検査器 GREEN Evidence](records/development/2026-08-07-work5b-checker-green-evidence-v1.md) — SHA-256 `020db589b586e6db741e0d5d347d31c30c89a077c390ebd2232c42dfccbb7d2c`
- [検査器 第一実運用record](records/development/2026-08-07-work5b-checker-first-run-v1.json) — SHA-256 `e2c4fb658c289340f2d0ac3c27a7cb3bce8168b3dcccd6926de30c5e21aca20c`
- [設計議論の証跡Decision](records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md) — SHA-256 `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d`
- [implementation_ready Decision](records/development/2026-08-07-work5b-implementation-ready-decision-v1.md) — SHA-256 `ad81728241f849b605954c6aa597215fed2811f5dbc1e6a21aafc5b508552554`
- [Work 5B Contract](records/development/2026-08-07-work5b-implementation-task-contract-v1.json) — SHA-256 `89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387`
- [Work 4B最小試行 GREEN Evidence](records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md) — SHA-256 `3284f77507a2ad09992404cae1ced846a6fe5ccdd564af8c8c0e8772e0588e0c`
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `387907b9e4abc513b1c367daa57d8f6e48227b0c43b5c2f16b747523c37111e1`

## 次に行う一作業

合意順序（DEC-WORK5B-DISCUSSION-OUTCOMES-001）の②：Work 4B本体の設計束を一枚の提案にまとめ、Human承認を得る。内容は、Profile再観測の検索への組み込み、検索recordの外部化（DATA_ROOT＋証明書方式）、絞り込み順位表と除外宣言（「すぐ対処」指定。除外宣言の承認が先行）、Entry・Relation・Baseline台帳。

開始条件：

- なし（Intake V4対応表の所見はA案でv2作成済み、Work 5B残項目はア案でdefer済み。DEC-INTAKE-V4-RED-MAP-SUPERSEDE-001、DEC-WORK5B-LEDGER-ITEM-DEFER-001）

完了条件：

- 設計束提案がHuman承認されること。実装はその後の作業単位

後続作業：合意順序の③レビューbacklog上位2系統の先行反証レビュー、④残りのbacklogとRC2取り込み・外部APIレビュー（台帳整備後）。全routineの一括分類は行わない。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：旧書庫の削除可否（別途判断）。所見処置と段完了扱いは2026-08-07に裁定済み（A案・ア案）。

## stale・deferred

- stale：なし。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、登録済み7課題の着手、旧書庫の削除判断、Current Work Projection正式写像、Entry・Relation・Baseline台帳、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：検査器 6 passed（宣言C1〜C4対応）、Contract結線 5 passed
- 直近の全Test：venv pytest 1066 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
