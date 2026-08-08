# TODO_NEXT_SESSION

更新日：2026-08-08

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討が完了。TODO検証単一入口の実装も完了した。
- 現在作業：TODO検証単一入口はRED commit ebadd12、実装commit 0bfcc4c、公式全1269 passedで完了。Humanはresolvedを承認したが、V4 Issueへ正規永続化するtoolが無いためstate変更を停止した。Human選択2によりtool不足をIC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001へ登録し、deferした。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（実装完了、formal resolution永続化はdefer）`、影響：正規resolve toolが無いためIssue record stateはregisteredのまま、次：将来のHuman判断までtool不足候補とともにdefer

## 最新のauthority／Evidence

- [V4 resolution永続化gap Human defer Decision](.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`
- [TODO検証単一入口 GREEN Evidence](records/development/2026-08-08-todo-handoff-unified-verification-green-evidence-v1.md) — SHA-256 `71442848c2b95a4b7f0212705ee24a99d8e008c8e459f219040b5308102730a9`
- [機密関連の実施順序 Decision](records/development/2026-08-07-confidentiality-work-order-decision-v1.md) — SHA-256 `ca5c4a89adb6ab2807887bb7834c4778f4e8658a697deb9f64617893dd67de09`
- [伏字化規則 GREEN Evidence](records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md) — SHA-256 `9dae5c2df9d39be08a63e22f47936fb27336d42c9032d8b5442bca8d7df68f85`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `08927e713a47517fd3bd0d5b7520a1eec0a9b1300c677e7590da3db847c65e74`

## 次に行う一作業

伏字化規則の設定登録と保全経路への接続。実装済み規則を設定へ登録し、保全経路で実際にマスクが適用されることをTDDで固定する。

開始条件：

- Humanの着手指示
- DEC-CONFIDENTIALITY-WORK-ORDER-001の実施順序2番目と既存redaction実装を固定入力にすること

完了条件：

- 設定登録GREENと、保全経路で伏字化が実際に適用されるEvidenceを固定すること

後続作業：幹線復帰としてWork 7A local_integrated deployment E2Eを推奨する。

## blocker・Human判断待ち

- blocker：なし。V4 resolve tool不足はdefer済みで、本線を阻害しない。
- Human判断待ち：次の一作業（伏字化規則の設定登録）の着手指示。行き先変更も可。

## stale・deferred

- stale：TODO検証単一入口Issueのresolution_verdict_pending projectionはHuman選択2によりstale。
- deferred：IC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001、参照Digest恒久検査器、守り役後追いレビュー、テストfixture重複、Work 7A以降。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Candidate V3 validator passed、Human Decision V4 repository validation passed、TODO単一入口48 passed
- 直近の全Test：venv公式runner 1269 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
