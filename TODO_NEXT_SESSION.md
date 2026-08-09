# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了し、deferred #7のテストfixture重複共通化も独立レビュー済みで完了した。
- 現在作業：deferred #7は対象129件・公式全1338件とfixture同一性9項目の独立確認を経てverified / completed。Humanが着手承認した未実施の進行待ち行列は#5（参照Digest恒久検査器）→#1（IC-V4 resolve tool）→#6（守り役後追いレビュー）であり、現在はHumanの行き先指示待ち。Work 7A第2項checkbox全体は未完了。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（実装完了、formal resolution永続化は着手承認済み・未実施）`、影響：正規resolve toolが無いためIssue record stateはregisteredのまま、次：#1として進行待ち行列に保持し、Humanの行き先指示後に単一作業として着手

## 最新のauthority／Evidence

- [テストfixture重複共通化 独立review result v1](records/session-handoffs/2026-08-09-codex-review-result-test-fixture-dedup-v1.md) — SHA-256 `5fdb07e7c4f691f99d87db461509e41eb50e8fdaad577476f1d494a7e7cc544e`
- [テストfixture重複共通化 Evidence](records/development/2026-08-09-test-fixture-dedup-evidence-v1.md) — SHA-256 `fc8863c8b56ea0078af1834efe2d0913de02cb1dc18574c24ff7329c2b46b8b2`
- [テストfixture重複共通化 公式全Test receipt](records/development/2026-08-09-test-fixture-dedup-receipt-v1.json) — SHA-256 `cdd490b06c4f12d65c80e632d0674602554e53cf42eeffadc07d994cce55e4d7`
- [Deferred項目の仕分け裁定 v1](records/development/2026-08-09-deferred-items-triage-decision-v1.md) — SHA-256 `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91`
- [Work 7A checkout relocation 前駆slice Completion Evidence](records/development/2026-08-09-work7a-checkout-relocation-precursor-completion-evidence-v1.md) — SHA-256 `2a2e3752d5b91b672786549e1f7f93d40838bade06f56d4d1c170b63a240dcfd`
- [Work 7A checkout relocation 独立review result v3](records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v3.md) — SHA-256 `ec30754f1ff8d6e06b791b1be78c58dd558e1966b80c34716807b15c0d497a3c`
- [Work 7A第2項 前駆slice scope v2](records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md) — SHA-256 `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- [Layout Baseline v3承認Decision](records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json) — SHA-256 `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

Work 7A第2項の後続slice。Project Bindingを承認済みstorage shapeへ耐久保存し、project移動・別checkoutからidentityを照合して復元できることをTDDで固定する。

開始条件：

- Humanの着手指示
- 前駆slice Completion Evidence、独立review result v3、Layout v3のProject Binding authorityを固定入力にして新しいscopeを作ること
- 守り役codeとしてrisk highの範囲レビューを行い、Human再開承認までREDを開始しないこと

完了条件：

- state_root/projects/<project_id>/bindings/<binding_id>.jsonの承認済みshapeへBindingをDigest付きで保存し、project移動・別checkoutから安全に復元する正例・負例・境界Testを固定すること
- 耐久Bindingの改竄・identity不一致・欠落をfail-closedに拒否し、独立レビューでverifiedになること
- Verification Run復元とWork 7A第2項checkbox完了は後続へ残すこと

後続作業：Work 7A第2項のVerification Run復元sliceへ進む。

## blocker・Human判断待ち

- blocker：なし。#5・#1・#6は着手承認済みの進行待ちで、本線を阻害しない。
- Human判断待ち：Project Binding耐久保存・復元sliceへの着手指示。行き先変更も可。

## stale・deferred

- stale：Work 7A第2項を単一sliceで完了する旧projectionは、Human裁定「分割案1」と前駆sliceのverified Completion Evidenceにより置換済み。
- deferred：C／Dの扱い、既存保全データへの遡及適用、原子的filesystem競合防止。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：テストfixture重複共通化のfixture同一性9／9、対象129件、test関数105／105・assert 431／431・parametrize 11／11の不変をReviewerが独立確認
- 直近の全Test：venv公式runner 1338 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
