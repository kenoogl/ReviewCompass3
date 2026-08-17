# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5第1〜5段・G25・一件用安全保存・G08一件設計・G20外部送信2契約・『正式ツール化』契約010〜013、セッションログ記録導線（record-run）と契約014（前置record解釈・遡及77件）が製品受入まで完了。**デプロイ方針を決定**（当面ローカル・配置同型性・next型起点・訂正版P3）。**全体見取り図を新設**し初期checklistを凍結。レビュー起動はagy（Tier 1既定）とclaude-subagent（Tier 3明示受容）の2 backend。全景は`docs/current/reviewcompass3-overview-current.md`
- 現在作業：なし。レビュー基盤moduleは休止中（2026-08-17休止record）。本日完了：セッションログ系2作業単位（record-run導線・契約014）、デプロイ方針決定（論点1〜4裁定）、checklist凍結＋全体見取り図新設。記録の正式経路は`docs/development/prompts/session-log-record-run.md`
- Task Contract：`なし（契約014受入完了。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [デプロイ方針Decision（論点1〜4の裁定・next型起点・訂正版P3）](records/development/2026-08-17-deployment-policy-decision-v1.md) — SHA-256 `ad3bbf84931f55d27c62e5243fede3fbfe2cc4c4d97cc87404ccab969e597671`
- [checklist凍結と全体見取り図新設のDecision（メモ【判断】5点対応表つき）](records/development/2026-08-17-checklist-freeze-and-overview-decision-v1.md) — SHA-256 `adff61b1061b31a1a9082f3a2e99cb59165f74d79e514540b4fb6aa72410d8f0`
- [全体見取り図（人向け全景。受入完了時にTODOと同時更新）](docs/current/reviewcompass3-overview-current.md) — SHA-256 `af59a803937bf52b7a459277d027223382b98731acbbf28ce093c3eb8a3545c4`
- [利用者による契約014の製品受入判断（014系Evidence 13点の束縛表つき）](records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md) — SHA-256 `759154984591f0479c505e4a2d01d6a86e2d9fd3a2c584b1187eb22f067e3a35`
- [レビュー基盤module開発の一時終了record（pending残件と再開の入口）](records/development/2026-08-17-review-tooling-module-pause-decision-v1.md) — SHA-256 `9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

なし（module休止中・次契約未定義）。再開の選択肢：(1) 休止record §3のpending残件（縦C合議／codex-cli第3 backend＝疎通回復が合図／外部API後続）、(2) デプロイ版の作成（合図＝**他アプリ開発の開始決定**。範囲＝デプロイ方針record §4）、(3) 新規作業。いずれも利用者の指示で選択し、事前走査（6手順・必読原則record）で着手する。

開始条件：

- 利用者の再開指示と順序選択がchatで得られる

完了条件：

- 選択された作業単位の事前走査record固定（または新規作業単位の範囲固定文書）

後続作業：休止record §4、デプロイ方針record §4〜5（デプロイ版の骨子・持ち越し）、契約014受入判断§4の持ち越しを参照。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：なし（module休止中。再開の時機・順序は利用者判断）

## stale・deferred

- stale：契約008〜014の進行中表示（七契約とも受入完了）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。統合時はbackend合流でなく判定record規約準拠）。後続候補＝`review_plan`自動変換・縦C合議・codex-cli backend。改善候補仕分け確定（2026-08-17）：`IC-BACKEND-REGISTRY-DEEPENING-001`採用・codex-cli追加と同時、`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`保留・同時機再評価、`IC-REUSE-SEARCH-GATE-CONNECTION-001`保留継続・縦C実測後、`IC-ADVERSARIAL-FIXTURE-CATALOG-001`採用・縦C RED組み込み。デプロイ関連：デプロイ版作成は他アプリ開発の開始決定が合図（方針record §4）・RC3版nextの返答語彙議論は後日・projection導出の本実装は運用実測後・REQ-PORTABLE系の権限束昇格は本格着手時。契約014持ち越し：残存5件（本文なし前置のみfile）は放置可・新前置種別は`record-run`非対応件数の急変が合図。`CLAUDE_VERSION`は次回経路使用時に更新

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約014対象18件（`tests/test_session_log_prefix_interpretation.py`）、record-run 10件（`tests/test_session_log_record_run.py`）、session_logs系全域330件——各単独終了コード0（本日後半は文書作業のみで試験対象変更なし）
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（2026-08-16・契約013完了時点の実行。契約014はsession_logs系全域330件の単独緑で受入）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
