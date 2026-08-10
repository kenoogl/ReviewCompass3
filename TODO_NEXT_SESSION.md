# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続、ReviewCompass3所属Codex session保存が完了。操縦者別連携の文書設計とHuman段完了承認を終え、最初の機械処理縦切りへ着手した。
- 現在作業：操縦者別連携の最小実装依頼は、指示文監査6所見と判定担当の全件accept推奨を受け、所見ごとのHuman裁定待ち。実装担当は未起動で、group C・Dの保留も継続している。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのままだが、本縦切りを妨げない、次：本縦切り完了後の別作業単位でHuman裁定を得て実Issueをresolveする

## 最新のauthority／Evidence

- [操縦者別連携 最小実装依頼 v1](records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v1.md) — SHA-256 `2bc4f1b7953dfe4f615e97c41f10e869558a4868b8cd017b740c6148c105cdb4`
- [操縦者別連携 指示文品質確認 v1](records/session-handoffs/2026-08-11-pilot-collaboration-entry-prompt-quality-review-v1.md) — SHA-256 `456d6551515e1c09f493bd7fcbd4cd6c3b29a95df233558acb39e62deff1607a`
- [操縦者別のClaude／Codex連携方法](docs/development/pilot-specific-claude-codex-collaboration.md) — SHA-256 `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [ReviewCompass3 開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c`

## 次に行う一作業

HumanがPA-PC-001〜006を所見ごとに採用、不採用、保留のいずれかで裁定する。採用所見があれば指示書へ反映し、新しい監査・判定周回を行う。

開始条件：

- 指示文品質確認recordと対象指示書のSHA-256が一致していること
- HumanがPA-PC-001〜006を全件裁定すること
- 保留所見がある場合は実装担当を起動しないこと

完了条件：

- 新規受入テストのRED確認後、固定したテストがGREENになること
- 既存bootstrap reviewテスト、故障注入、公式全テスト、差分検査が合格すること
- 反対側モデルの独立レビューがverifiedとなり、Human段完了承認を得ること

後続作業：指示文品質関門を通過した後、実装担当が新規受入テストのRED確認から開始する。

## blocker・Human判断待ち

- blocker：PA-PC-001〜006のHuman裁定が未了のため、実装担当を起動できない。
- Human判断待ち：PA-PC-001〜006の採用、不採用、保留を所見ごとに決める必要がある。実装後の段完了承認も別に必要。

## stale・deferred

- stale：group C・Dを直ちに次作業とする旧表示は、本作業を現在の一作業に選んだHuman判断により古い状態。group C・Dの裁定記録自体は有効なまま保持する。
- deferred：group C・D、外部送信、Claude／Codex CLI実起動、実装実行、実装後レビュー接続、Human所見裁定、再監査、既存保全データへの伏字化遡及適用、Work 7A後続、既存Issue resolveを保留する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：既存bootstrap review関連23 passed、終了コード0。指示文監査6件、判定担当は6件全件accept推奨、新規所見0件。新規受入テストは未着手。
- 直近の全Test：直近の公式全Testは1470 passed、failed 0、errors 0、終了コード0。実装後に再実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
