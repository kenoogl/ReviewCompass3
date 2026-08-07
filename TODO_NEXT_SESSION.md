# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 4B最小試行の縦一周が完了した（範囲提案のHuman承認→宣言→RED対応表（R1〜R7、testの無い宣言0件）→RED→実装前の自己適用検索record→GREEN 8 passed→gate判定verified）。実装順12の後半（Work 5Bでのgate実証）が残る。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断

## 最新のauthority／Evidence

- [Work 4B最小試行 GREEN Evidence](records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md) — SHA-256 `3284f77507a2ad09992404cae1ced846a6fe5ccdd564af8c8c0e8772e0588e0c`
- [Work 4B最小試行 RED Evidence](records/development/2026-08-07-work4b-reuse-search-red-evidence-v1.md) — SHA-256 `2a03d414e34285dcd9fef2a10eea3f46ac63fb23e5e1c5ef3f1f9bf19e167054`
- [宣言→RED対応表（R1〜R7）](records/development/2026-08-07-work4b-reuse-search-declaration-red-map-v1.json) — SHA-256 `ba313d41f2b517e1923182215420f0b8e0ea13a8b6df30dd1b8372aa183707b7`
- [範囲提案 承認Decision](records/development/2026-08-07-work-4b-minimal-pilot-scope-approval-decision-v1.md) — SHA-256 `4db98a488c76a7d15c1ddffca5c8f94139c29eadcc985930f30af5636b59adfc`
- [実装前の自己適用検索record](records/development/2026-08-07-reuse-search-record-helper-reuse-search-v1.json) — SHA-256 `75cb79034e26e65b0aefff4525d4d134f5f3bcae3a34c88cb010edcb5fa6f58d`
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `a089ffdf5e538e28457894fb6a120ef065d2b8a0acb3c392d4dedaeacdecbd9d`
- [書庫移行 Receipt](records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json) — SHA-256 `29a3af432c408e8f479a747706cc8ce406c9c7d123c95d02cbb4f02719235914`

## 次に行う一作業

Work 5B（内部Implementation Task Contract Pilot）で、ReviewCompass3自身の小さなhelper一件を選定し、reuse search gate（検索record無しでは実装を開始しない関門、`tools/development/reuse_search_record.py`の`gate_check`）を実証する。

開始条件：

- HumanがWork 5Bの開始を承認し、対象helperを選定すること（`DEC-WORK4B-MINIMAL-PILOT-SCOPE-001`はWork 5B開始を承認していない）
- 宣言→RED対応表照合の恒久tool化の要否をHumanが判断すること（判断期限到来、下記参照）

完了条件：

- checklist §10 Work 5Bの項目（Contract、red、固定source、implementation_ready判断、green、post-write、Provenance、分割commit）に従う

後続作業：全routineの一括分類は行わない。Entry・Relation・Baselineの台帳形式はWork 4B本体の後続作業単位。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：(1) Work 5B開始の承認と対象helperの選定。(2) 宣言→RED対応表照合の恒久tool化の要否——リマインドの判断時点が到来した。3回目の対応表（Work 4B、R1〜R7）は確立済みのその場AST照合で作成済みであり、4回目以降をtool化するかの判断。(3) 旧書庫の削除可否は別途判断。

## stale・deferred

- stale：なし。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、登録済み7課題の着手、旧書庫の削除判断、Current Work Projection正式写像、Entry・Relation・Baseline台帳、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 4B reuse search 8 passed（宣言R1〜R7対応）
- 直近の全Test：venv pytest 1055 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
