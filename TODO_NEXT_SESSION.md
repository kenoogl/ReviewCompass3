# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了し、deferred #7、#5、#1に加えて、deferred #6は第1単位、第2単位（高19件の独立レビュー実施）、守り役後追い修正第1単位（group E）、第2単位（group A）、第3単位（group B）まで完了した。
- 現在作業：守り役後追い修正第3単位（group B、公式検証oracleのF-B1〜F-B5）はEvidence commit 33dfa38と完了レビューv2 commit c656859により完了し、判定はverified、blocking 0件となった。group C 5件・D 7件の計12件は未修正のまま各判定recordに保持する。次はgroup Cのblocking 5件の修正単位であり、包括承認commit 271826aによりrisk `high`確定・着手・RED開始は事前承認済みである。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [守り役後追い修正順序 Human裁定 v1](records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md) — SHA-256 `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997`
- [group B 公式検証oracle修正 Evidence v1](records/development/2026-08-10-official-oracle-fix-evidence-v1.md) — SHA-256 `f38e9e59396954e75b73768e7328e355aa2ad93c38fcb841f36998fd200e1444`
- [group B 公式検証oracle修正 完了レビュー結果 v2](records/session-handoffs/2026-08-10-codex-review-result-official-oracle-fix-v2.md) — SHA-256 `e6c402146110d1dc80a90924348c8a8c2e7fc87231f91d1c7b2f6f862c083d0b`
- [group B〜D 自律実行 包括承認 v1](records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md) — SHA-256 `3c0a0fb8f02ebead2694c1ae0568e536f9a8fbf99ba65c7050116744f18ab8c9`
- [守り役後追い独立レビュー group C 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-c-v1.md) — SHA-256 `d7b52bd131cbae3e559643c66e229c52084710586171cd3b4644e61bb5540b0d`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

守り役後追い修正第4単位として、group C（現在地正本の`tools/development/todo_handoff.py`・`tools/development/todo_update_path.py`）のblocking 5件を修正する。

開始条件：

- 包括承認commit 271826aにより、group C修正単位のrisk `high`確定・着手・RED開始は事前承認済み。包括承認§2の停止条件に触れない限り追加承認を待たず開始すること
- 修正順序の裁定recordとgroup C判定recordを固定入力とし、group Dの7件を先取り修正しないこと

完了条件：

- 裁定済み手順に従い、F-C1〜F-C5の反証Test、実装、完了レビュー、Closer処理をgroup Cだけの修正単位として完了すること
- 完了レビューがverifiedとなり、group Cのblocking 5件が解消したことを固定Evidenceで確認できること

後続作業：group Cの完了後、包括承認の範囲内でgroup Dのblocking 7件の修正単位へ進む。

## blocker・Human判断待ち

- blocker：技術上のblockerはなし。group C修正単位は包括承認により着手可能。包括承認§2の停止条件に触れた場合は停止する
- Human判断待ち：開始前の判断待ちはなし。変更可能path外、上流設計・config・schema変更、既存台帳・recordの再計算や移行、RED後のtest変更、完了レビューのblocking修正、その他の意味的裁定が必要になった場合だけ判断を求める

## stale・deferred

- stale：group Bを未修正とする旧projectionは、group B修正Evidenceと完了レビューv2により置換済み。完了レビューv1のF-C1・F-C2は解消済みとして履歴保持する。既知のnon-blocking N-C1（公式receiptの`source_state_digest`再生成不一致）は本修正対象外のまま保持する。
- deferred：group C 5件・D 7件の計12件は未修正のまま各判定recordに保持する。#2 C／Dの扱い、#3既存保全データへの遡及適用、#4原子的filesystem競合防止、守り役後追いレビューの中51・低17、Work 7A第2項の後続slice、authority参照Digest検査器の実docsへの適用・修復、既存Issueのresolveも保留継続

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：group B完了レビューv2で`tests/test_work_unit_transition.py` 13 passed。F-C1修正Testは修正前実装で1 failed、現行実装で1 passed
- 直近の全Test：group B完了レビューv2で公式runner 1469 passed、failed 0、errors 0、skipped 0、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
