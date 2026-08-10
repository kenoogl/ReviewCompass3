# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了し、deferred #7、#5、#1に加えて、deferred #6は第1単位、第2単位（高19件の独立レビュー実施）、守り役後追い修正第1単位（group E）まで完了した。
- 現在作業：守り役後追い修正第1単位（group E、外部送信・機微境界）はEvidence commit 2bd9d66と完了レビューcommit 6ece925により完了し、判定はverified、blocking 0件となった。group Eの7件は解消済みで、group A 2件・B 5件・C 5件・D 7件の計19件は未修正のまま各判定recordに保持する。次はgroup Aの修正単位であり、着手にはHumanのrisk確定と承認が必要である。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [守り役後追い修正順序 Human裁定 v1](records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md) — SHA-256 `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997`
- [group E 修正Evidence v1](records/development/2026-08-10-egress-guard-fix-evidence-v1.md) — SHA-256 `b3b78f98fb3ee8e035ddcf983f0e1c17c619deac1b949c127a6d98e78dfb6394`
- [group E 修正 完了レビュー結果 v1](records/session-handoffs/2026-08-10-codex-review-result-egress-guard-fix-v1.md) — SHA-256 `82e95646ab23dae68f488ed04fe0c96204d97321803c7ff6dd4671b86b3d090b`
- [守り役後追い独立レビュー group A 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-a-v1.md) — SHA-256 `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

守り役後追い修正第2単位として、group A（共通正本の`tools/common/digests.py`・`tools/common/paths.py`・`tools/task_contract/identity.py`）のblocking 2件を修正する。

開始条件：

- Humanがgroup A修正単位のriskを`high`と確定し、着手を承認すること
- 修正順序の裁定recordとgroup A判定recordを固定入力とし、group B〜Dの17件を先取り修正しないこと

完了条件：

- 裁定済み手順に従い、F-A1とF-A2の反証Test、実装、完了レビュー、Closer処理をgroup Aだけの修正単位として完了すること
- 完了レビューがverifiedとなり、group Aのblocking 2件が解消したことを固定Evidenceで確認できること

後続作業：group Aの完了後、group Bの修正単位について改めてHumanのrisk確定と承認を得る。

## blocker・Human判断待ち

- blocker：技術上のblockerはなし。group A修正単位はHumanのrisk確定と着手承認まで開始しない
- Human判断待ち：group A修正単位のrisk `high`確定と着手承認。単位内の修正方式などの細目は範囲固定後にHumanが確定する

## stale・deferred

- stale：blocking Finding 26件を全件未修正とする旧projectionは、修正順序の裁定とgroup E完了レビューにより置換済み。group E判定recordのblocking 7件は履歴として保持する。
- deferred：group A 2件・B 5件・C 5件・D 7件の計19件は未修正のまま各判定recordに保持する。#2 C／Dの扱い、#3既存保全データへの遡及適用、#4原子的filesystem競合防止、守り役後追いレビューの中51・低17、Work 7A第2項の後続slice、authority参照Digest検査器の実docsへの適用・修復、既存Issueのresolveも保留継続

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：group Eのegress対象107 passed、Session Log保全8 passed、関連回帰36 passed
- 直近の全Test：group E完了レビューで公式runner 1427 passed、failed 0、errors 0、skipped 0、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
