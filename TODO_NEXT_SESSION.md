# TODO_NEXT_SESSION

更新日：2026-08-10

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了。守り役後追い修正は重大Finding 26件中14件（group E 7件・A 2件・B 5件）が独立レビューでverified、残り12件（C 5件・D 7件）は未修正。
- 現在作業：group Cは不成立だったRED commit 431dd7bをrevert commit c24e3b4で完全に取り消し、裁定record commit 5e0320bによりRED以降を白紙化した。範囲固定v1〜v3は履歴として残るが再着手根拠ではない。group Dは未着手でblocking 7件を保持する。C・Dの再着手時期は未裁定である。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [group C白紙化 Human裁定 v1](records/development/2026-08-10-group-c-reset-decision-v1.md) — SHA-256 `590b21ddafe0be72b5113d2c5deee275306391b33814f1575bccc27860a974eb`
- [group C再着手前 独立点検結果 v1](records/session-handoffs/2026-08-10-codex-review-result-group-c-readiness-v1.md) — SHA-256 `7f7b6d5d4f5f0dcdb82d7c31447bbbbeebe7befc842319938e1f953a4aa83643`
- [守り役後追い group D 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-d-v1.md) — SHA-256 `c4ef93d511aa473948a7bc43c2a1f210a9f53869e6a4d150fa8e34eac0fd2086`
- [本日方針文書の廃棄 Human裁定 v1](records/development/2026-08-10-policy-document-retirement-decision-v1.md) — SHA-256 `29184da78c29b0ba27ab53d8ef3f43d28ed4b49f95115da54152bc9c24eefa41`
- [Stage Five設計正本](records/design/stage-five-design.json) — SHA-256 `29ed55927061c9991ec7bbad3f03c929214527b653979d3453c9bbd7eb499c4f`
- [守り役後追い優先度 Human裁定 v1](records/development/2026-08-10-guard-backfill-priority-decision-v1.md) — SHA-256 `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7`
- [守り役後追い修正順序 Human裁定 v1](records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md) — SHA-256 `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997`
- [レビュー材料モード Human裁定 v1](records/development/2026-08-10-review-material-mode-decision-v1.md) — SHA-256 `5b8e37f4ecfaceb068122abdfcc1e35299d7c4579637d6104f49658375243d80`
- [Pilot／Review連携方式 Human裁定 v1](records/development/2026-08-10-pilot-review-method-positioning-decision-v1.md) — SHA-256 `8d485c0bf1f81710e5d11afbc8319d66ab3e47e5ff3657cfabb762723b63e009`
- [group E修正 完了レビュー結果 v1](records/session-handoffs/2026-08-10-codex-review-result-egress-guard-fix-v1.md) — SHA-256 `82e95646ab23dae68f488ed04fe0c96204d97321803c7ff6dd4671b86b3d090b`
- [group A修正 完了レビュー結果 v2](records/session-handoffs/2026-08-10-codex-review-result-common-guard-fix-v2.md) — SHA-256 `26bc061381ae9afb72c134025307ca1591311fd1482c8ac3671c7c5be3989e05`
- [group B修正 完了レビュー結果 v2](records/session-handoffs/2026-08-10-codex-review-result-official-oracle-fix-v2.md) — SHA-256 `e6c402146110d1dc80a90924348c8a8c2e7fc87231f91d1c7b2f6f862c083d0b`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

Humanがgroup Cの再着手時期を決めた場合に限り、code・testへ触れず、白紙状態から範囲固定v4を新規作成してhighの独立範囲レビューへ回す。Humanの時期裁定まではgroup C・Dを開始しない。

開始条件：

- group C・Dの再着手時期についてHuman判断を得ること
- 白紙化裁定、group C元判定、再着手前点検、修正順序裁定を固定入力とし、revert済みRED 431dd7bと範囲固定v1〜v3を開始根拠にしないこと
- v4へ変更対象3 module、上流10反証、回帰10 test file、H3の実運用接続2経路、現在baseとDigest、訂正RED境界、規約Aの事前走査、固定入力の出自を一体で固定すること

完了条件：

- v4のhigh独立範囲レビューがverifiedとなること
- 上流10反証だけが狙った理由で失敗し正例が合格する訂正REDの受入条件をv4に固定すること
- 訂正REDのtest変更承認とGREEN再開承認を別々のHuman境界として明記し、未承認の実装へ進まないこと

後続作業：v4のverifiedとHumanの明示的な再開承認後にだけ、訂正REDを機械確認する。group C完了後にgroup D 7件を別単位で扱う。

## blocker・Human判断待ち

- blocker：group CはGC-READY-001〜004の4件が未解消。内容は、反証と正例が正しく機能する訂正REDの欠落、3 moduleと現在状態に合うv4の欠落、回帰10 fileと実運用2経路の範囲漏れ、test変更・GREEN再開のHuman承認欠落である。したがって『技術上のblockerなし・着手可能』ではない。
- Human判断待ち：group C・Dの再着手時期、group Cの訂正REDに必要なtest変更、v4のverified後のGREEN再開について明示判断が必要。先行の包括承認commit 271826aだけでは、後続の点検と白紙化裁定が置いた停止条件を上書きしない。

## stale・deferred

- stale：group Cを『blockerなし・着手可能』とする旧表示、RED 431dd7bを有効とする表示、範囲固定v1〜v3を再着手根拠とする表示はstale。本日作成の規約A/B/C文書、レビュー方法整理文書、骨太方針案と付随レビューrecordは廃棄裁定により今後の判断根拠から外す。引き続き有効なのはStage Five設計正本、廃棄裁定が生かした規約Aだけ、守り役の優先度・修正順序、材料モード、連携方式位置づけ、group C白紙化などのHuman裁定recordである。
- deferred：group Dのblocking 7件は未着手：F-D1 実行fileと対象repositoryの束縛、F-D2 候補recordの正準Digest再計算、F-D3 symlinkによるproject外台帳参照、F-D4 裁定連鎖の時刻・ID整合、F-D5 書込み直前のsymlink差替え、F-D6 Manifest自体のsymlink・解決先、F-D7 Layout Baseline固定方針値の検査。group C 5件、既知N-C1、#2 C／Dの扱い、#3既存保全データへの遡及適用、#4原子的filesystem競合防止、中51・低17、Work 7A第2項後続slice、authority参照Digest検査器の実docs適用・修復、既存Issueのresolveも保留継続。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：group CのRED追加2 fileは赤追加前と現HEADで差分0。現在の公式全Testに含まれる関連Testも合格
- 直近の全Test：本Closerが公式runnerを単独実行し1469 passed、failed 0、errors 0、skipped 0、Python 3.9.6、pytest 8.4.2、fallback false、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
