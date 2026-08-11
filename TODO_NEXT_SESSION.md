# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続、ReviewCompass3所属Codex session保存が完了。操縦者別連携の文書設計と第1機械処理縦切りがHuman段完了承認まで完了した。
- 現在作業：Humanは外部実行経路の最初の段階に無工具のClaude疎通確認を選択した。先行範囲レビューF1〜F4を反映した範囲固定v2を作成済み。test・実装・認証・実送信は未開始で、独立範囲レビュー前の状態。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのままだが、本縦切りを妨げない、次：本作業と分け、後続候補としてHuman裁定を得てresolveする

## 最新のauthority／Evidence

- [無工具Claude疎通経路 範囲固定 v2](records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v2.md) — SHA-256 `aefa05876b38a5b192d923f43dc17609678053ca33a4936b992e8a6646845c82`
- [無工具疎通確認 選択Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-no-tool-bootstrap-selection-human-decision-v1.md) — SHA-256 `3b29567232320f6751a2badd40d31b7f8ab321d731d7777f8fdd1b0f11afa0da`
- [外部実行経路 選択Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md) — SHA-256 `58d7809b547b339c3641f336cc23b2729aca6e09d7d50a109ed4c7f984de7983`
- [先行範囲レビュー v1](records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md) — SHA-256 `402b2f7af1b2b28c9dac497ec2624e6078e361cebf55730b12f8ee8784c1e1ff`
- [操縦者別のClaude／Codex連携方法](docs/development/pilot-specific-claude-codex-collaboration.md) — SHA-256 `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d`
- [委譲作業の共通レビュープロトコル](docs/development/work-review-protocol.md) — SHA-256 `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [ReviewCompass3 開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c`

## 次に行う一作業

反対側のCodexモデルを使うレビュー用サブエージェントが、範囲固定v2を実装変更なしで独立レビューする。

開始条件：

- 範囲固定v2、無工具段階選択Human裁定、TODOが同一の意味単位としてcommit済みであること
- 固定入力とレビュー材料のSHA-256が現在内容に一致すること
- 主担当とレビュー担当のモデル対応が操縦者別連携文書に一致すること

完了条件：

- 先行F1〜F4、上流authority、Human境界、受入条件、変更範囲、停止条件が独立に確認されること
- レビュー結果がcommitされ、blocking所見があればHuman裁定へ戻ること
- レビューがverifiedでもHumanのhigh risk・RED開始承認までtest・実装・認証・送信を開始しないこと

後続作業：範囲レビュー結果をHumanへ提示し、所見の採否、high risk、変更範囲、RED開始を一つの再開裁定として求める。実送信承認は実装完了レビュー後の別境界に残す。

## blocker・Human判断待ち

- blocker：Claude Codeは現在未認証。これは範囲レビューを妨げないが、認証操作と実送信を停止する。
- Human判断待ち：範囲レビュー後に、所見の採否とhigh riskのRED開始をHumanが判断する。現在の無工具段階選択は実装・認証・送信承認ではない。

## stale・deferred

- stale：接続段階のHuman選択待ちという旧表示は、無工具の疎通確認を選択した裁定により古い状態。先行範囲v1は実装根拠に使わない。
- deferred：実送信、認証操作、限定道具を許可する実装委譲、第2縦切り、group C・D、実装後レビュー接続、既存保全データへの伏字化遡及適用、Work 7A後続、既存Issue resolveを保留する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書・範囲固定段階のため新規testなし。直近の操縦者別連携受入89件は終了0。
- 直近の全Test：直近の公式全Testは1559 passed、failed 0、errors 0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
