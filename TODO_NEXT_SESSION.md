# TODO_NEXT_SESSION

更新日：2026-08-08

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口が完了。伏字化規則の設定登録とactual CLI保全経路への接続も独立レビュー済みで完了した。
- 現在作業：伏字化規則の設定登録はRED 89affb7／GREEN dc13ed1、actual CLI未接続の修正はRED 698a5aa／GREEN f9f92cf。Codex独立レビューでtargeted 13、関連34、公式全1282 passed、新作したactual CLIのhigh-entropy反証もfail-closedとなり、verified / completed。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（実装完了、formal resolution永続化はdefer）`、影響：正規resolve toolが無いためIssue record stateはregisteredのまま、次：将来のHuman判断までtool不足候補とともにdefer

## 最新のauthority／Evidence

- [伏字化・実保全入口 独立レビューEvidence](records/development/2026-08-08-redaction-production-entry-independent-review-evidence-v1.md) — SHA-256 `8b543e61ba9cb98b0d2ff65360ba5885c47cfa8f8cb5e60b74c3bdcff61af98b`
- [伏字化・実保全入口 独立レビュー公式receipt](records/development/2026-08-08-redaction-production-entry-independent-review-test-receipt-v1.json) — SHA-256 `ce26543e61df279103dfa57150f939fe4935fd08c989524dad2d56f29e4d1627`
- [actual CLI接続修正 GREEN Evidence](records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md) — SHA-256 `d9ec9d812c3cd8a3eb2efdc293eb934fe02dafe157aae9c3b24c996f2cb08f21`
- [機密関連の実施順序 Decision](records/development/2026-08-07-confidentiality-work-order-decision-v1.md) — SHA-256 `ca5c4a89adb6ab2807887bb7834c4778f4e8658a697deb9f64617893dd67de09`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `32c5fe8e6707a2f139a7486a5a6da9e484629f57b1cf6200dd5a96fca0611496`
- [V4 resolution永続化gap Human defer Decision](.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

Work 7A local_integrated deployment E2Eの最初の縦切り。install、project、runtime、sensitiveの各rootを分離し、既存Layout v3とdeployment境界をTDDで固定する。

開始条件：

- Humanの着手指示
- Layout Baseline v3とWork 7A checklistを固定入力にし、最初のroot分離だけへscopeを限定すること

完了条件：

- 4種rootのidentity、物理分離、禁止cross-writeを正例・負例・境界TestとGREEN Evidenceへ固定すること

後続作業：Work 7Aの次項目として、別checkoutとproject移動後のBinding、Snapshot、Change Set復元へ進む。

## blocker・Human判断待ち

- blocker：なし。V4 resolve tool不足はdefer済みで、本線を阻害しない。
- Human判断待ち：Work 7A最初の縦切りへの着手指示。行き先変更も可。

## stale・deferred

- stale：伏字化規則の着手待ちprojectionと、actual CLI未接続を完了扱いした先行completed_claim。いずれも修復Evidenceにより置換済み。
- deferred：IC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001、C／Dの扱い、既存保全データへの遡及適用、参照Digest恒久検査器、守り役後追いレビュー、テストfixture重複。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：伏字化設定・actual CLI targeted 13 passed、関連34 passed、独立actual CLI正例とhigh-entropy反証 passed
- 直近の全Test：venv公式runner 1282 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
