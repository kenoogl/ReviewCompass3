# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了し、deferred #7、#5、#1に加えて、deferred #6は第1単位と第2単位（高19件の独立レビュー実施）まで完了した。
- 現在作業：deferred #6第2単位は、範囲固定commit bedf986、Human裁定commit 2c9e786、group A〜Eの判定record commits 17613d2・46f2465・f02c32c・e0e5d33・8a7da31により、高19件の独立レビュー実施を完了した。全groupの総合判定はreported_unverifiedで、blocking Finding 26件（A 2・B 5・C 5・D 7・E 7）は未修正のまま残る。修正は本単位scope外であり、次はHuman裁定待ち。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [deferred #6第2単位 範囲固定 v1](records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-high-reviews-scope-v1.md) — SHA-256 `6b587a7eedf77380aadf5b41ab90edd148bdcd6f69b850447dc684591737f8e9`
- [守り役後追いレビュー 優先度Human裁定 v1](records/development/2026-08-10-guard-backfill-priority-decision-v1.md) — SHA-256 `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7`
- [守り役後追い独立レビュー group A 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-a-v1.md) — SHA-256 `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139`
- [守り役後追い独立レビュー group B 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-b-v1.md) — SHA-256 `06c9722aed283224cff2347dc1e4d1c106f959103bfddee44d38e120e4628bd1`
- [守り役後追い独立レビュー group C 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-c-v1.md) — SHA-256 `d7b52bd131cbae3e559643c66e229c52084710586171cd3b4644e61bb5540b0d`
- [守り役後追い独立レビュー group D 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-d-v1.md) — SHA-256 `c4ef93d511aa473948a7bc43c2a1f210a9f53869e6a4d150fa8e34eac0fd2086`
- [守り役後追い独立レビュー group E 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-e-v1.md) — SHA-256 `a4bc656cdfe73188b1def7bc107a98a1027daf289dc3b6ab254b9808d3c86a33`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

deferred #6第2単位で未修正のblocking Finding 26件について、Humanが今後の扱いを裁定する。

開始条件：

- 範囲固定commit bedf986、Human裁定commit 2c9e786、group A〜E判定record commits 17613d2・46f2465・f02c32c・e0e5d33・8a7da31を固定入力として参照すること
- 裁定が固定されるまで、Findingの修正、code・test・判定record・一覧recordの変更を開始しないこと

完了条件：

- blocking Finding 26件を、別のhigh risk作業単位でいま修正するか、未修正のまま後回しにするかを決めること
- いま修正する場合は、26件をどの単位に分割し、どの順序で実施するかを決めること
- 修正着手は本裁定に含めず、作業単位ごとに範囲固定とHuman承認を得ること

後続作業：Humanが選んだ方針に従い、承認済みの別high risk作業単位へ進むか、26件を未修正のままdeferredとして本線へ戻る。

## blocker・Human判断待ち

- blocker：技術上のblockerはなし。blocking Finding 26件の修正はHuman裁定まで開始しない
- Human判断待ち：26件をいま修正するか後回しにするか。いま修正する場合は、別のhigh risk作業単位への分割方法と実施順序

## stale・deferred

- stale：後追い対象84件の優先度・実施対象・要Human判定6件を決める旧projectionは、Human裁定commit 2c9e786と高19件のレビュー判定5件により置換済み。
- deferred：#2 C／Dの扱い、#3既存保全データへの遡及適用、#4原子的filesystem競合防止は保留継続。守り役後追いレビューの中51・低17、Work 7A第2項の後続slice、authority参照Digest検査器の実docsへの適用・修復、既存IssueのresolveもHuman判断待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：group A〜Eの既存testは順に96・46・33・104・73 passed。既存fixture外の機械反証によりblocking Finding 26件を確認
- 直近の全Test：直近のgroup E隔離実行では公式runner 1381 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
