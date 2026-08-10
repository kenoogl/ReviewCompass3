# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了し、deferred #7、#5、#1に加えて、deferred #6第1単位の守り役後追いレビュー対象一覧も独立レビュー済みで完了した。
- 現在作業：deferred #6第1単位は、一覧record commit 68a659dと完了レビューv2 commit 0768a9fによりverified / completed。全133 moduleを網羅し、後追い対象84件（高19・中50・低15）と要Human判定6件を固定した。次はHuman裁定待ちで、個別後追いレビューは未着手。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [守り役後追いレビュー対象一覧 完了レビューv2](records/session-handoffs/2026-08-10-codex-review-result-guard-backfill-inventory-v2.md) — SHA-256 `bc6359f81c5e5522cb3a5bc36f8a8c48166d8f7ca0ebdba87df501fc3bb46ed4`
- [守り役code後追いレビュー対象一覧 v1](records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md) — SHA-256 `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e`
- [deferred #6第1単位 範囲固定 v1](records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-scope-v1.md) — SHA-256 `b81ecaacfbe866719e25cb35764cd4754092d72ad55af63c83b7c429b6567204`
- [Deferred項目の仕分け裁定 v1](records/development/2026-08-09-deferred-items-triage-decision-v1.md) — SHA-256 `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

deferred #6の後続方針について、Humanが一覧recordの提案を裁定する。

開始条件：

- 一覧record commit 68a659d、完了レビューv2 commit 0768a9f、範囲固定 commit b1f96dcを固定入力として参照すること
- 裁定が固定されるまで、個別moduleの後追いレビュー、code・test・既存recordの変更を開始しないこと

完了条件：

- 後追い対象84件の優先度を確定すること
- 実施対象を選定すること
- 要Human判定6件を判定すること

後続作業：Humanが選定した実施対象について、別の範囲固定と着手指示を得て後追いレビューへ進む。

## blocker・Human判断待ち

- blocker：技術上のblockerはなし。後続の個別レビューはHuman裁定まで開始しない
- Human判断待ち：後追い対象84件の優先度確定、実施対象の選定、要Human判定6件の判定

## stale・deferred

- stale：Work 7A第2項を単一sliceで完了する旧projectionは、Human裁定「分割案1」と前駆sliceのverified Completion Evidenceにより置換済み。
- deferred：#2 C／Dの扱い、#3既存保全データへの遡及適用、#4原子的filesystem競合防止は保留継続。Work 7A第2項の後続slice、authority参照Digest検査器の実docsへの適用・修復、既存IssueのresolveもHuman判断待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：完了レビューv2でF1負例14件がpassed。全133件、後追い84件、要Human判定6件の再集計が一覧recordと一致
- 直近の全Test：直近のReviewer独立実行では公式runner 1381 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
