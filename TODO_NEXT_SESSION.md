# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続が完了。Work 7Aは4種root分離と第2項の前駆sliceまで完了。守り役後追い修正は重大Finding 26件中14件がverified、残り12件は未修正。ReviewCompass3所属Codex session 81件のprivate保存と現行rollout変換対応が完了。
- 現在作業：session保存はverified_with_live_boundaryとして完了し、現在のmainline作業はgroup C・Dの再着手時期に関するHuman判断待ちへ戻った。group Cは不成立REDをrevertし、裁定recordによりRED以降を白紙化済み。group Dは未着手でblocking 7件を保持する。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのまま、次：toolのverified後にHuman裁定を得て、実Issueのresolveを別作業単位で実施

## 最新のauthority／Evidence

- [ReviewCompass3 Codex session全件保存 Evidence v1](records/development/2026-08-10-all-reviewcompass3-codex-session-capture-evidence-v1.md) — SHA-256 `0a970c1511904bdd95b90dc49b03e5d343c67fb41a4ebf2123998c044d94a5da`
- [ReviewCompass3 Codex session全件保存 Human裁定 v1](records/development/2026-08-10-all-reviewcompass3-codex-session-capture-decision-v1.json) — SHA-256 `6d1367e121959197cd71a8e33a2e9aa45a95b20b18decc20688c708ef68ecbc6`
- [group C白紙化 Human裁定 v1](records/development/2026-08-10-group-c-reset-decision-v1.md) — SHA-256 `590b21ddafe0be72b5113d2c5deee275306391b33814f1575bccc27860a974eb`
- [group C再着手前 独立点検結果 v1](records/session-handoffs/2026-08-10-codex-review-result-group-c-readiness-v1.md) — SHA-256 `7f7b6d5d4f5f0dcdb82d7c31447bbbbeebe7befc842319938e1f953a4aa83643`
- [守り役後追い group D 判定 v1](records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-d-v1.md) — SHA-256 `c4ef93d511aa473948a7bc43c2a1f210a9f53869e6a4d150fa8e34eac0fd2086`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [V4 resolution永続化gap 改善候補](.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json) — SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`

## 次に行う一作業

Humanがgroup Cの再着手時期を決めた場合に限り、code・testへ触れず、白紙状態から範囲固定v4を新規作成してhighの独立範囲レビューへ回す。Humanの時期裁定まではgroup C・Dを開始しない。

開始条件：

- group C・Dの再着手時期についてHuman判断を得ること
- 白紙化裁定、group C元判定、再着手前点検、修正順序裁定を固定入力とし、revert済みREDと範囲固定v1〜v3を開始根拠にしないこと
- v4へ変更対象3 module、上流10反証、回帰10 test file、H3の実運用接続2経路、現在baseとDigest、訂正RED境界、規約Aの事前走査、固定入力の出自を一体で固定すること

完了条件：

- v4のhigh独立範囲レビューがverifiedとなること
- 上流10反証だけが狙った理由で失敗し正例が合格する訂正REDの受入条件をv4に固定すること
- 訂正REDのtest変更承認とGREEN再開承認を別々のHuman境界として明記し、未承認の実装へ進まないこと

後続作業：v4のverifiedとHumanの明示的な再開承認後にだけ、訂正REDを機械確認する。group C完了後にgroup D 7件を別単位で扱う。

## blocker・Human判断待ち

- blocker：group Cは訂正RED、現在状態に合うv4、回帰10 fileと実運用2経路の範囲、test変更・GREEN再開のHuman承認が欠けている。group Dはblocking 7件を未修正で保持する。
- Human判断待ち：group C・Dの再着手時期、group Cの訂正REDに必要なtest変更、v4のverified後のGREEN再開について明示判断が必要。

## stale・deferred

- stale：group Cを『blockerなし・着手可能』とする旧表示、revert済みREDを有効とする表示、範囲固定v1〜v3を再着手根拠とする表示はstale。
- deferred：group Dのblocking 7件、group C 5件、既知N-C1、既存保全データへの伏字化遡及適用、原子的filesystem競合防止、中51・低17、Work 7A第2項後続slice、authority参照Digest検査器の実docs適用・修復、既存Issueのresolveを保留する。現在進行中のCodex taskが保存後に追加するlive tailは次回の明示captureまでprivate archiveへ未反映となる。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Codex rollout parser 3 passed、parser／保存関連28 passed、session log全177 passed、いずれも終了コード0
- 直近の全Test：公式runnerを単独実行し1470 passed、failed 0、errors 0、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
