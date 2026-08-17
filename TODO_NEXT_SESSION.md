# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』の契約010〜013、さらに本日の**セッションログ記録の導線整備（record-run wrapper・手順書・AGENTS導線）と契約014（前置record解釈）が製品受入まで完了**。レビュー起動はagy（Tier 1・既定）とclaude-subagent（Tier 3・明示受容つき）の2 backend、依頼record作成はassemble→LLM記入→check合格（3類型）が正式経路。事前走査は6手順＋必読原則record
- 現在作業：なし。レビュー基盤module（『正式ツール化』）は利用者判断で休止中（2026-08-17休止record）。セッションログ系の2作業単位——記録導線整備（`record-run`1コマンド化・現セッション既定除外）と契約014（前置record解釈。遡及77件・完了レビューcr-014-001＝`verified`・blocking 0）——は本日製品受入まで完了。記録の正式経路は`docs/development/prompts/session-log-record-run.md`
- Task Contract：`なし（契約014受入完了。次契約は未定義）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者による契約014の製品受入判断（014系Evidence 13点の束縛表つき）](records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md) — SHA-256 `759154984591f0479c505e4a2d01d6a86e2d9fd3a2c584b1187eb22f067e3a35`
- [契約014完了レビュー判定record cr-014-001（verified・blocking 0）](records/session-handoffs/2026-08-17-session-log-prefix-interpretation-completion-verdict-v1.md) — SHA-256 `de8b1051551cbffd3600dabc7b2649335a58ef47e418c1d592aac7d19179cb32`
- [契約014実装・遡及実測Evidence（受入条件6点の充足表）](records/development/2026-08-17-session-log-prefix-interpretation-implementation-evidence-v1.md) — SHA-256 `566c7b88fbd6a9bf6dac5ad93c28b876689977ab0f6393e314ad020632e55a9a`
- [セッションログ記録run手順書（正式経路の入口。AGENTS.md §1から接続）](docs/development/prompts/session-log-record-run.md) — SHA-256 `9c1808fdbb8c730d4d3f843a76dfce8f202260e2870e385f37eae557f48b834d`
- [レビュー基盤module開発の一時終了record（pending残件と再開の入口）](records/development/2026-08-17-review-tooling-module-pause-decision-v1.md) — SHA-256 `9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

なし（module休止中・次契約未定義）。再開時は利用者の指示で、休止record §3のpending残件——(a) 縦C（合議。仕分け確定2件を兼ねる）、(b) codex-cli第3 backend（疎通回復が合図）、(c) 外部API pending解除・`review_plan`自動変換等——または新規作業から選択し、事前走査（6手順・必読原則record）で着手する。

開始条件：

- 利用者の再開指示と順序選択がchatで得られる

完了条件：

- 選択された作業単位の事前走査record固定（または新規作業単位の範囲固定文書）

後続作業：休止record §4の再開の入口、および契約014受入判断§4の持ち越し（残存5件の扱い・新前置種別出現時の小改定）を参照。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：なし（module休止中。再開の時機・順序は利用者判断）

## stale・deferred

- stale：契約008〜014の進行中表示（七契約とも受入完了）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。統合する場合はbackend合流でなく判定record規約への準拠——設計方針メモ§3）。後続候補＝`review_plan`出力の自動変換・縦C合議・codex-cli backend。改善候補の仕分けは確定済み（2026-08-17仕分けrecord）：`IC-BACKEND-REGISTRY-DEEPENING-001`＝採用・codex-cli追加と同時実施、`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`＝保留・同時機再評価、`IC-REUSE-SEARCH-GATE-CONNECTION-001`＝保留継続・縦C事前走査の実測後に再仕分け、`IC-ADVERSARIAL-FIXTURE-CATALOG-001`＝採用・縦C RED段要求へ組み込み。実装経路確認部品の`CLAUDE_VERSION`（2.1.220のまま）は次回その経路使用時に更新。Reviewer側digest実計算の特定command許可は将来の契約改定候補。契約014の持ち越し：残存5件（本文なし前置のみfile）は正当な縮退として放置可・新しい前置種別の出現は`record-run`要約の非対応件数急変が合図（同型の小改定で対応）

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約014対象18件（`tests/test_session_log_prefix_interpretation.py`）、record-run 10件（`tests/test_session_log_record_run.py`）、session_logs系全域330件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（2026-08-16・契約013完了時点の実行。契約014はsession_logs系全域330件の単独緑で受入）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
