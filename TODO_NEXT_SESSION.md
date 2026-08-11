# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続、ReviewCompass3所属Codex session保存が完了。操縦者別連携の文書設計とHuman段完了承認を終え、最初の機械処理縦切りへ着手した。
- 現在作業：固定RED受入テスト73件が独立再レビューverifiedとなり、RT-PC-001〜004は全件closed。v6 §8に従い、テストを変更せずproduction実装へ進む。外部CLI実起動と外部送信は対象外。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのままだが、本縦切りを妨げない、次：本縦切り完了後の別作業単位でHuman裁定を得て実Issueをresolveする

## 最新のauthority／Evidence

- [操縦者別連携 単一実装依頼 v6](records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md) — SHA-256 `5ab9474b425162df9c192124c7558754b4b371402d2e4d67adfab448cbbb3b5d`
- [操縦者別連携 PA-PC-010 Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-pa-pc-010-human-decision-v1.md) — SHA-256 `669a55677dd47d4d2d87f24d901e55be3913c1df27ec9b351462bad9c75996c7`
- [操縦者別連携 単一v4指示文品質確認](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-quality-review-v4.md) — SHA-256 `d5550321827e0bc7e297569c9bbabc63259ef380f1d26f284f84028055679191`
- [操縦者別連携 単一v5指示文品質確認](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-quality-review-v5.md) — SHA-256 `20ba3fefa01ec2ff3db177713839af919d2d1789e99c3a169026e82e0c4df7e6`
- [操縦者別連携 単一v6限定指示文品質確認](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-quality-review-v6.md) — SHA-256 `d5fe00279566a6b37c51697c4c2ca7fdf1835c0943750ecdeca6cf5617b9cab3`
- [操縦者別連携 RED受入テスト 独立レビュー v1](records/session-handoffs/2026-08-11-pilot-collaboration-red-test-review-v1.md) — SHA-256 `6cf381e20fd4bc1f18d808d0b2237a94cf434a35ddfef8780e1374cc3b295607`
- [操縦者別連携 RED受入テスト所見 Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-red-test-findings-human-decision-v1.md) — SHA-256 `d350bb7d21b0a427b3306fb878c2044f75ccb9a7d0eb19438b8c68c965042e7a`
- [操縦者別連携 RED受入テスト 独立再レビュー v2](records/session-handoffs/2026-08-11-pilot-collaboration-red-test-rereview-v2.md) — SHA-256 `914c3d6a466fe439f50e000407fe3a2f0a5d70ace9616e86ed36ed18239553d2`
- [操縦者別連携 RT-PC-002 Human補足裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-rt-pc-002-human-clarification-v1.md) — SHA-256 `c0c985689e5e2878e1351a6267597499f02eeb8771adff599fed9d794f705add`
- [操縦者別連携 RED受入テスト 独立再レビュー v3](records/session-handoffs/2026-08-11-pilot-collaboration-red-test-rereview-v3.md) — SHA-256 `15325a1cc5762b7a0bf4c320d8dcd7ba1b1f128932ea45c8212c7a96239afb83`
- [操縦者別連携 RED受入テスト 独立再レビュー v4](records/session-handoffs/2026-08-11-pilot-collaboration-red-test-rereview-v4.md) — SHA-256 `da0c56616b101987158ceb624da25bfb2bf2cb012d56dbdbe755fe17ca30699c`
- [操縦者別のClaude／Codex連携方法](docs/development/pilot-specific-claude-codex-collaboration.md) — SHA-256 `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d`
- [委譲作業の共通レビュープロトコル](docs/development/work-review-protocol.md) — SHA-256 `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [ReviewCompass3 開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c`

## 次に行う一作業

固定したRED受入テスト73件を変更せず、v6の変更可能範囲内でproduction実装を行いGREENにする。

開始条件：

- 固定RED commit 6cb26e752d9e763d90a90f0b5ce8ed8591b2fff7が固定されていること
- 独立再レビューv4のpathとSHA-256が固定され、判定がverifiedであること
- 実装中に固定RED受入テストを変更しないこと

完了条件：

- 新規受入テストのRED確認後、固定したテストがGREENになること
- 既存bootstrap reviewテスト、故障注入、公式全テスト、差分検査が合格すること
- 反対側モデルの独立レビューがverifiedとなり、Human段完了承認を得ること

後続作業：実装後に対象test、既存bootstrap review test、故障注入、公式全test、差分検査を単独commandで実行し、反対側モデルで独立レビューする。

## blocker・Human判断待ち

- blocker：なし。固定RED受入テストはverified。production実装後の独立レビューとHuman段完了承認は未完了。
- Human判断待ち：RT-PC-002はv6どおり保存前停止とする。raw・launch・eventは作らずraw_digest_mismatchで停止し、先行裁定の『保存』はaudit_digest_mismatchだけに適用する。実装後の段完了承認は別に必要。

## stale・deferred

- stale：group C・Dを直ちに次作業とする旧表示は、本作業を現在の一作業に選んだHuman判断により古い状態。group C・Dの裁定記録自体は有効なまま保持する。
- deferred：group C・D、外部送信、Claude／Codex CLI実起動、実装後レビュー接続、既存保全データへの伏字化遡及適用、Work 7A後続、既存Issue resolveを保留する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：4 test fileは73件collect成功。単独REDは29 failed/19 passed、7 failed、10 failed/1 passed、3 failed/4 passedで全て終了1。既存1470件は終了0。再レビューv4はverified、RT-PC-001〜004全件closed。
- 直近の全Test：直近の公式全Testは1470 passed、failed 0、errors 0、終了コード0。実装後に再実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
