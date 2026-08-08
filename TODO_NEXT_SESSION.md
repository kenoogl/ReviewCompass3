# TODO_NEXT_SESSION

更新日：2026-08-09

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aの最初の縦切りとして4種root分離も独立レビュー済みで完了した。
- 現在作業：Work 7A第1項は元RED b006e60／GREEN 663ec50、symlink差替え修正RED 2239a02／GREEN 6f1c417、例外連鎖修正RED b77e044／GREEN 58e2533。Codex独立レビューでtargeted 33、関連46、公式全1315 passed、独立OSError反証も非漏洩・無副作用で合格し、verified / completed。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（実装完了、formal resolution永続化はdefer）`、影響：正規resolve toolが無いためIssue record stateはregisteredのまま、次：将来のHuman判断までtool不足候補とともにdefer

## 最新のauthority／Evidence

- [Work 7A 4種root分離 独立レビューEvidence](records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md) — SHA-256 `5418bc5839cd01cf8f6b99088c33108fb83fb366fa7a49ff773959e556fab1ec`
- [Work 7A 4種root分離 独立レビュー公式receipt](records/development/2026-08-09-work7a-four-root-separation-independent-review-test-receipt-v1.json) — SHA-256 `a88ee495c3d473cea2c6de60439e6a17c13d5070fa67f1c1d1984601dbc16f7f`
- [例外連鎖path修正 GREEN Evidence](records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md) — SHA-256 `f3896c8a2d4ec74003ce7633621bef65e41f18906b2e105c0e3d55eb77867239`
- [Layout Baseline v3承認Decision](records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json) — SHA-256 `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `496a028e22c5f07ce54b670cdc6a6425d4e45252e5f5841cfc1cb620f46c3a1c`
- [V4 resolution永続化gap Human defer Decision](.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

Work 7A第2項の最小E2E。別checkoutとproject移動後にProject Binding、Source Snapshot、Change Setを復元・照合できることをTDDで固定する。

開始条件：

- Humanの着手指示
- 4種root分離の独立レビューEvidenceと既存Binding・Snapshot・Change Set authorityを固定入力にし、Work 7A第2項だけへscopeを限定すること

完了条件：

- 別checkoutとproject移動後のidentity保持、Binding更新、Snapshot・Change Set復元を正例・負例・境界TestとGREEN Evidenceへ固定すること

後続作業：Work 7A第3項として、Control／Executionのstructured I/Oとstate owner確認へ進む。

## blocker・Human判断待ち

- blocker：なし。V4 resolve tool不足はdefer済みで、本線を阻害しない。
- Human判断待ち：Work 7A第2項への着手指示。行き先変更も可。

## stale・deferred

- stale：4種root分離の着手待ちprojectionと、初期化symlink差替え・例外連鎖漏洩を見逃した先行completed_claim。いずれも修復Evidenceと独立レビューにより置換済み。
- deferred：IC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001、C／Dの扱い、既存保全データへの遡及適用、原子的filesystem競合防止、参照Digest恒久検査器、守り役後追いレビュー、テストfixture重複。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 7A 4種root分離 targeted 33 passed、関連46 passed、独立OSError非漏洩・無副作用反証 passed
- 直近の全Test：venv公式runner 1315 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
