# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』の縦B契約010（Reviewer起動アダプタ）・縦A契約011（依頼組み立て器）・契約012（claude-subagent第2 backend・Tier 2／3受容機構）の**五契約が製品受入まで完了**。レビュー起動はagy（Tier 1・既定）とclaude-subagent（Tier 3・起動ごとの明示受容つき）の2 backend体制が正式経路で、同一対象集合への2 oracle比較が初成立（両判定役一致）。依頼record作成はassemble→LLM記入→check合格が正式経路。事前走査は6手順＋必読原則record。
- 現在作業：**自由文類型（縦Aの第2縦切り・契約013）**。事前走査完走（`start_allowed: true`・範囲整理の利用者了解）→候補v1→自己レビュー（SR-C13-1〜3）→候補v2→独立確認cr-013-001＝`verified_with_findings`・blocking 0→所見反映の候補v3を**採用**→**実装完了**（RED8→全緑・既存2類型はgolden固定試験でbyte不変を機械証明・類型推定を正準位置＝「レビュー種別」行だけへ是正・自由記入節の非空／digest行拒否／fence敵対fixture・入口文書へ使い分け規律を追記）。残り＝(1) §9-5実運用E2E（自由文依頼1件。対象・依頼文は利用者と確認し起動は明示指示）、(2) §9-7完了レビュー（agy・Tier 1）、(3) §9-8製品受入。
- Task Contract：`TC-RC3-PRODUCT-FREE-TEXT-REQUEST-TYPE-013 / v3`＝`adopted_implementation_started`（実装済み。E2E・完了レビュー・製品受入待ち）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：契約013の受入作業を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用中の契約013候補v3（cr-013-001所見反映済み）](records/task-contract/2026-08-17-free-text-request-type-candidate-v3.md) — SHA-256 `73a287c137a73c617e25655c35377b88a7ffc033b89e4be68d63d3b0ce245ffc`
- [契約013採用と実装開始のHuman判断record](records/development/2026-08-17-free-text-request-type-contract-adoption-decision-v1.md) — SHA-256 `83894a4ea18fa23fa382ac0f90bc86e6d0bf01d0aedc6a99cb07becdcd237528`
- [契約013候補v2独立確認判定record（cr-013-001・verified_with_findings・blocking 0・機械転記）](records/session-handoffs/2026-08-17-free-text-request-type-contract-review-verdict-v1.md) — SHA-256 `dcfffbec261db38ba7c58dc8b92b9c5fa3b4d708940198abedaade29ae7112a6`
- [自由文類型 事前走査v1（6手順・start_allowed true・範囲整理の利用者了解）](records/development/2026-08-17-free-text-request-type-prescan-v1.md) — SHA-256 `aad68904a58f8ac79a8d99b1075636e1691684fde911fc83e15edc30437d9b55`
- [文字列理解の失敗類型と対策原則（参照record・事前走査の必読入力）](records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md) — SHA-256 `4c80a56c2f66ffb0baef0a10aae1680e3a04d5c2b883371c826a8f2237bfbcaf`
- [改善候補4件の仕分けrecord（採用2・保留2・実施時機の固定）](records/development/2026-08-17-improvement-candidates-triage-decision-v1.md) — SHA-256 `34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162`
- [利用者による契約012の製品受入判断（2 backend正式経路化。012系Evidenceの束縛表つき）](records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md) — SHA-256 `dad40e6c88a5c46dd4008806ab0e94c797d4c5f55aefd4f0d3d08891d343afb8`
- [利用者による契約011の製品受入判断（正式経路化。011系Evidenceの束縛表つき）](records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md) — SHA-256 `0a817d532e1da97bd817c12060f4b2d2b031e97fa76f2e932b77384d9e4c9792`
- [契約010の製品受入判断（headless起動の正式経路化）](records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md) — SHA-256 `78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

契約013 §9-5の実運用E2Eを行う。内容＝自由文依頼1件の対象（repository内commit済みfile）と依頼文を
利用者と確認→正式経路（`--type free_text`でassemble→LLM記入→check合格→commit）→**利用者の明示指示で
headless起動**（agy既定・Tier 1）→判定record取得・事後照合。不成立なら停止し、自動再試行をしない。

開始条件：

- 本handoffを含むcommitが完了し、作業treeがcleanである
- E2Eの対象・依頼文の利用者確認と起動の明示指示がchatで得られる

完了条件：

- §9-5のE2E判定record取得（または停止理由の確定）

後続作業：§9-7完了レビュー（agy・`completion_review`類型）→§9-8製品受入（残余risk 5点）→次の
順序選択（縦C・codex-cli等。仕分け確定事項はdeferred参照）。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：§9-5実運用E2Eの対象・依頼文の確認と起動指示

## stale・deferred

- stale：契約008〜012の進行中表示（五契約とも受入完了）
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
