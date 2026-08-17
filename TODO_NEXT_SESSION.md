# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』の縦B契約010（Reviewer起動アダプタ）・縦A契約011（依頼組み立て器）・契約012（claude-subagent第2 backend）・**契約013（自由文類型）の六契約が製品受入まで完了**。レビュー起動はagy（Tier 1・既定）とclaude-subagent（Tier 3・起動ごとの明示受容つき）の2 backend体制が正式経路で、同一対象集合への2 oracle比較が初成立（両判定役一致）。依頼record作成はassemble→LLM記入→check合格が正式経路（3類型：契約レビュー・完了レビュー・自由文レビュー。類型推定は正準位置方式）。事前走査は6手順＋必読原則record。
- 現在作業：次の作業単位の順序選択待ち（利用者判断）。契約013は§9-8成立・完了（E2E 1往復で参照文書の陳腐化検出→所見採用まで実証。完了レビューcr-013-002＝`verified`・blocking 0）。候補＝(a) 縦C（合議・判定record比較の上位層。仕分け確定2件——機械gate実測・敵対fixture対応表のRED組み込み——を兼ねる）、(b) codex-cli第3 backend（疎通回復待ち。回復時は登録形深化を含めmodel照合範囲を再評価）、(c) 外部API pending解除・`review_plan`自動変換等の他候補。
- Task Contract：なし（契約013は§9-8成立・完了。受入判断record＝`2026-08-17-free-text-request-type-product-acceptance-decision-v1.md`。次契約は未定義）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者による契約013の製品受入判断（残余risk 5点受容・自由文類型の正式経路化。013系Evidenceの束縛表つき）](records/development/2026-08-17-free-text-request-type-product-acceptance-decision-v1.md) — SHA-256 `2e01fb5cab0ca5b5218bce77c6e4884ba9692f40f6f14054c65dd3439ffdc810`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力。§4は契約013反映済み）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6`
- [改善候補4件の仕分けrecord（採用2・保留2・実施時機の固定）](records/development/2026-08-17-improvement-candidates-triage-decision-v1.md) — SHA-256 `34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162`
- [利用者による契約012の製品受入判断（2 backend正式経路化。012系Evidenceの束縛表つき）](records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md) — SHA-256 `dad40e6c88a5c46dd4008806ab0e94c797d4c5f55aefd4f0d3d08891d343afb8`
- [利用者による契約011の製品受入判断（正式経路化。011系Evidenceの束縛表つき）](records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md) — SHA-256 `0a817d532e1da97bd817c12060f4b2d2b031e97fa76f2e932b77384d9e4c9792`
- [契約010の製品受入判断（headless起動の正式経路化）](records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md) — SHA-256 `78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が次の作業単位の順序を選択する。候補：

- **(a) 縦C（合議・判定record比較の上位層）の契約候補作成**——2 oracle比較の実データ（契約012の
  一致事例2組）が材料。事前走査（6手順）から着手し、仕分け確定事項2件（`IC-REUSE-SEARCH-GATE-CONNECTION-001`の
  運用実測・`IC-ADVERSARIAL-FIXTURE-CATALOG-001`のRED段組み込み）を兼ねる。
- (b) codex-cli第3 backend——トークン枯渇の疎通回復待ちのため着手不可（回復確認が先）。回復時は
  `IC-BACKEND-REGISTRY-DEEPENING-001`を同縦切りへ含め、`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`を再評価。
- (c) 外部API pending解除・`review_plan`出力の自動変換等の他候補。

開始条件：

- 本handoffを含むcommitが完了し、作業treeがcleanである

完了条件：

- 順序選択の文言がchatで得られる

後続作業：選択された作業単位の事前走査（6手順・必読原則record）または着手。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：次の作業単位の順序選択

## stale・deferred

- stale：契約008〜013の進行中表示（六契約とも受入完了）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。統合する場合はbackend合流でなく判定record規約への準拠——設計方針メモ§3）。後続候補＝`review_plan`出力の自動変換・縦C合議・codex-cli backend。改善候補の仕分けは確定済み（2026-08-17仕分けrecord）：`IC-BACKEND-REGISTRY-DEEPENING-001`＝採用・codex-cli追加と同時実施、`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`＝保留・同時機再評価、`IC-REUSE-SEARCH-GATE-CONNECTION-001`＝保留継続・縦C事前走査の実測後に再仕分け、`IC-ADVERSARIAL-FIXTURE-CATALOG-001`＝採用・縦C RED段要求へ組み込み。実装経路確認部品の`CLAUDE_VERSION`（2.1.220のまま）は次回その経路使用時に自経路の手続きで更新。Reviewer側digest実計算の特定command許可は将来の契約改定候補

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約013対象40件（`tests/test_request_builder.py`。既存32無変更＋新設8）、契約012対象67件、G30運用契約実行75件、layout 13件、bootstrap 41件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,482件成功・終了コード0（自由文類型実装後の実行）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
