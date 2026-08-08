# TODO_NEXT_SESSION

更新日：2026-08-08

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討が完了。Humanの指示によりTODO検証単一入口の課題へ対応中。
- 現在作業：ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001のTDD実装と検証が完了。RED 2件をcommit ebadd12へ固定し、単一CLIへ三検証を集約した。compact TODOは3,871 bytesでCLI合格、関連48 passed、公式全1269 passed。GREEN Evidence固定済み。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / resolution_verdict_pending`、影響：実装と検証は完了し、Issue state変更だけがHuman判断待ち、次：HumanがResolution Verdictを判断する

## 最新のauthority／Evidence

- [TODO検証単一入口 GREEN Evidence](records/development/2026-08-08-todo-handoff-unified-verification-green-evidence-v1.md) — SHA-256 `71442848c2b95a4b7f0212705ee24a99d8e008c8e459f219040b5308102730a9`
- [TODO検証単一入口 公式Test receipt](records/development/2026-08-08-todo-handoff-unified-verification-green-test-receipt-v1.json) — SHA-256 `4dbcdb642ddeb35552748873e02f04056f7a84c6ae9ba31b26d45270b62626d4`
- [TODO検証単一入口 Issue](.reviewcompass/workflow/issues-v4/issue-todo-handoff-verification-gap-001--v1.json) — SHA-256 `475b0ea27b331b1d44e3883a30c575d21ebd14ab14b894725e8aa9121e51bba5`
- [TODO検証gap 観測](records/development/2026-08-07-todo-handoff-verification-gap-observation-v1.json) — SHA-256 `01f57093a875059d738f7045cfc9ca124dde3d838f6bed4f1a9c533382a43dcc`
- [TODO handoff共通手順](docs/development/prompts/todo-handoff-update.md) — SHA-256 `bb6b7b1364886b0c22591c4a48d5d2ed5b8aadc947152ce285cf70e19aba0591`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `08927e713a47517fd3bd0d5b7520a1eec0a9b1300c677e7590da3db847c65e74`

## 次に行う一作業

HumanがGREEN Evidenceを確認し、ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001のResolution Verdictを判断する。

開始条件：

- GREEN Evidence、公式Test receipt、単一CLIの実TODO合格を確認すること

完了条件：

- Humanがresolved、追加処置または差戻しを裁定すること

後続作業：resolved裁定後、伏字化規則の設定登録と保全経路への接続へ戻る。

## blocker・Human判断待ち

- blocker：実装blockerなし。Issue closureはHuman Resolution Verdict待ち。
- Human判断待ち：ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001のResolution Verdict。

## stale・deferred

- stale：超過した旧TODOのtodo_handoff単独合格結果。
- deferred：参照Digest恒久検査器、守り役後追いレビュー、テストfixture重複、Work 7A以降。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：TODO単一入口 targeted 10 passed、関連回帰48 passed、実TODO CLI passed
- 直近の全Test：venv公式runner 1269 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
