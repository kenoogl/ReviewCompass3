# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続、ReviewCompass3所属Codex session保存が完了。操縦者別連携の文書設計とHuman段完了承認を終え、最初の機械処理縦切りへ着手した。
- 現在作業：HumanがST-PC-005の第2縦切りへの完全移管を裁定し、v2の要求を26件へ限定するv3追補を作成した。v2とv3を合わせた実効指示の最終再確認待ちで、実装担当は未起動。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのままだが、本縦切りを妨げない、次：本縦切り完了後の別作業単位でHuman裁定を得て実Issueをresolveする

## 最新のauthority／Evidence

- [操縦者別連携 最小実装依頼 v2](records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v2.md) — SHA-256 `7310fa0c88e3becd4bf36e43c1363247d325d2ad013f809c8ffdbb78c96d6363`
- [操縦者別連携 指示文所見 Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-findings-human-decision-v1.md) — SHA-256 `de176de8ee6798de493010ef81e18e37c6ffb73bfeb95c54f23a865e1e5bbc57`
- [操縦者別連携 指示文品質再確認 v2](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-quality-rereview-v2.md) — SHA-256 `f78c23eb48452d85a0849fff1ce23556b52cdd6c4e4377d22bf527cec0efff86`
- [操縦者別連携 最小実装依頼 v3追補](records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v3.md) — SHA-256 `a3bbd01c73d0efe54513dc1f06a965e6ac4385c72d86aab5f84f167c03d2ccdd`
- [操縦者別連携 PA-PC-006 Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-pa-pc-006-human-decision-v1.md) — SHA-256 `f131eea737a8396e7d1284633ed96895e86d9b68176363e82cbdbb6c5d36c513`
- [操縦者別のClaude／Codex連携方法](docs/development/pilot-specific-claude-codex-collaboration.md) — SHA-256 `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [ReviewCompass3 開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c`

## 次に行う一作業

v2とv3を合わせた実効指示について、PA-PC-006の閉鎖、要求26件の整合、実装可能性を新しい監査・判定担当で最終確認する。

開始条件：

- v2、v3、PA-PC-006 Human裁定のSHA-256が固定されていること
- 監査担当と判定担当を別の新しい会話状態で起動すること
- 最終確認が合格するまで実装担当を起動しないこと

完了条件：

- 新規受入テストのRED確認後、固定したテストがGREENになること
- 既存bootstrap reviewテスト、故障注入、公式全テスト、差分検査が合格すること
- 反対側モデルの独立レビューがverifiedとなり、Human段完了承認を得ること

後続作業：品質関門を通過した後、実装担当が新規受入テストのRED確認から開始する。

## blocker・Human判断待ち

- blocker：Human裁定は完了したが、v2とv3を合わせた実効指示の最終品質確認が未了のため実装担当をまだ起動しない。
- Human判断待ち：最終確認で新規所見が出た場合は裁定が必要。実装後の段完了承認も別に必要。

## stale・deferred

- stale：group C・Dを直ちに次作業とする旧表示は、本作業を現在の一作業に選んだHuman判断により古い状態。group C・Dの裁定記録自体は有効なまま保持する。
- deferred：group C・D、外部送信、Claude／Codex CLI実起動、実装実行、実装後レビュー接続、Human所見裁定、再監査、既存保全データへの伏字化遡及適用、Work 7A後続、既存Issue resolveを保留する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：既存bootstrap review関連23 passed、終了コード0。PA-PC-006はHuman裁定により今回の要求から外して第2縦切りへ移管し、今回の要求集合は26件。新規受入テストは未着手。
- 直近の全Test：直近の公式全Testは1470 passed、failed 0、errors 0、終了コード0。実装後に再実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
