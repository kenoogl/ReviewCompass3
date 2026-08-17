# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』の縦B契約010（Reviewer起動アダプタ・headless正式経路）と**縦A契約011（依頼組み立て器・2類型）の製品受入**まで完了。依頼record作成はassemble→LLM記入→check合格が正式経路になった。事前走査は6手順へ改定・手順書化し、正式再利用検索の導線を接続、機械gate接続は改善候補`IC-REUSE-SEARCH-GATE-CONNECTION-001`として登録済み。
- 現在作業：契約012（claude-subagent第2 backend・Tier 2／3受容機構）の受入は**§9-10まで全て成立**。§9-8実E2Eは2往復（`e2e-012-001`＝`rejected`・blocking F-1検出→利用者採用でF-1〜F-3修正→`e2e-012-002`＝`verified_with_findings`・blocking 0）、§9-10完了レビューはagy（Tier 1）が**`verified`・blocking 0・未検査空**。同一対象集合（digest表13行完全一致）への**初の2 oracle比較が成立し、両判定役が一致**。残り＝**§9-11製品受入のみ**（利用者が§7.4残余risk 4点を確認して受け入れる判断。Claudeが4点を提示済み）。
- Task Contract：`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012 / v2＋§7.2訂正record3件`＝`adopted_implementation_started`（実装・model承認・訂正・E2E・完了レビュー済み。製品受入待ち）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：契約012の受入作業を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [§9-10完了レビュー判定record（agy・Tier 1・verified・blocking 0・機械転記）](records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-verdict-v1.md) — SHA-256 `5f0ba930d3c478609b12dd573a87c6815350d159630440dcc971391cbe70441c`
- [契約012実運用E2E（§9-8）Evidence（2往復・F-1検出と修正・2 oracle実証）](records/development/2026-08-17-claude-subagent-e2e-evidence-v1.md) — SHA-256 `64a40fb7fdb67bb43de08f0a5b777f41aab80ff5f39778b58d30633da72c9407`
- [E2E 012-002判定record（verified_with_findings・blocking 0・機械転記）](records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-rereview-subagent-verdict-v1.md) — SHA-256 `8af6f9acc49afaecdb0034cc5fae31c8c308fabb5ea71b4720a672d0bd10fcb6`
- [E2E 012-001判定record（rejected・blocking F-1検出・機械転記）](records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-verdict-v1.md) — SHA-256 `9cde9965fbd120cc30a20c9af6cc45061b153e3d3172691974d5a2ac548c7bcc`
- [契約012 §7.2子環境の訂正record（抑制注入変数9種の流用・改善候補採用）](records/development/2026-08-17-claude-subagent-child-injection-correction-decision-v1.md) — SHA-256 `db84857854cda3bb8381535bd872653d5d82032d5f59d2a7799d023efad1d199`
- [claude本体2.1.224のpin更新record（自動更新起因24件失敗の復旧）](records/development/2026-08-17-claude-bootstrap-binary-pin-update-decision-v1.md) — SHA-256 `3e761b2b8bf31075ded1673c6592c9bb681d3ab6fadd49f25a91ee5daaee6c49`
- [契約012 §7.2子環境の訂正record（通過変数USER・実行器9変数と同値化）](records/development/2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md) — SHA-256 `d80b03d55ea1a75b742aa51f89f3428429eba51fd5bb55986037e808b42b3175`
- [契約012 §7.2固定引数の訂正record（--verbose・adopted）](records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md) — SHA-256 `3e96a358ea21c7c8a7e08a2436d3546d16dfb6e577706de29ddb1c96e6645375`
- [契約012 subagent許可model承認record（claude-opus-5・実測3回）](records/development/2026-08-17-subagent-allowed-models-approval-v1.md) — SHA-256 `d6f7420db1948f1755fd9db62453cc1f44e43427839d70408c30ee259b050703`
- [契約012実装Evidence（RED16→全緑・不変移設証明・保護差分0）](records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md) — SHA-256 `979b48868bdc69751c60fec4bb3f5e9abdf910b4c7d30b941b5cd7fe0922a7de`
- [契約012採用と実装開始のHuman判断record](records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md) — SHA-256 `5af17a1ede1f109d7f378af9457bc1d5f4e044107128c378599163167abc8959`
- [採用中の契約012候補v2](records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md) — SHA-256 `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d`
- [契約012候補v2独立確認判定record（機械転記・verified）](records/session-handoffs/2026-08-17-claude-subagent-backend-contract-review-verdict-v1.md) — SHA-256 `ae78da140e9b72576700437569f91aa67cdce2be237ae0a0cf48829b3d1676c3`
- [利用者による契約011の製品受入判断（残余risk 4点受容・正式経路化）](records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md) — SHA-256 `0a817d532e1da97bd817c12060f4b2d2b031e97fa76f2e932b77384d9e4c9792`
- [契約011実運用E2E・完了レビューEvidence（2往復・fence修正）](records/development/2026-08-17-request-builder-e2e-evidence-v1.md) — SHA-256 `fac5a19072ef241a24c248a9d09cb4efd92d11ccd5e8ba62434cc37492ceba09`
- [契約011完了レビュー判定record（機械転記・verified）](records/session-handoffs/2026-08-17-request-builder-implementation-completion-rereview-verdict-v1.md) — SHA-256 `16f8adecc4a6cafd9d4781695adf9db85a80d2fe95c65472a84b5c90cef6d2de`
- [契約011実装Evidence（RED→緑・導線・実演2件）](records/development/2026-08-17-request-builder-implementation-evidence-v1.md) — SHA-256 `939d54afb56d4a481b9ece80d926dfbc2cc83c19981b416c0580970f854fd6ba`
- [契約011採用と実装開始のHuman判断record](records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md) — SHA-256 `993e255cf3b15934ea22b76e2394840df34aacf81870c464c91fcebf7c938f74`
- [採用中の契約011候補v3（cr-011-001所見反映済み）](records/task-contract/2026-08-17-request-builder-candidate-v3.md) — SHA-256 `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1`
- [契約011候補v2独立確認判定record（機械転記・verified_with_findings）](records/session-handoffs/2026-08-17-request-builder-v2-review-verdict-v1.md) — SHA-256 `f8a719f74f880eac80b95582073a12aff2d481b097add45c38dbaf17b996e51a`
- [縦A事前走査v1（6手順の適用第1号）](records/development/2026-08-17-vertical-a-request-builder-prescan-v1.md) — SHA-256 `8aa156c82653b6d873bbcf1195064f14a1a1aba3913b996225af7b2dad17a03c`
- [正式再利用検索の証明書（start_allowed: true）](records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json) — SHA-256 `b081e9fa6243f46c653cd2870fc439c22f46cd903f7df21aa23f9f815e35c344`
- [契約010の製品受入判断（headless起動の正式経路化）](records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md) — SHA-256 `78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516`
- [レビュー経路の設計方針メモ（利用者裁定2件）](records/development/2026-08-17-review-path-design-principles-memo-v1.md) — SHA-256 `8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e`
- [レビュー実行体制の正式ツール化 統合検討v1（agy訂正済み）](records/development/2026-08-16-review-tooling-formalization-study-v1.md) — SHA-256 `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が§9-11の製品受入を判断する。Claudeが提示済みの契約012 §7.4残余risk 4点——(1) Tier 3の
独立性は限定的（緩和：唯一oracle禁止・機械反証併用・tier明記）、(2) claude CLI仕様変更への追随
（緩和：安全側停止・raw完全保存）、(3) subagent起動もanthropicへの内容送出を伴う（事実の明示：
操縦Claudeが同一provider下で常時repositoryを読んでおり新規の露出先は増えない。緩和：利用者指示
起点・起動record台帳）、(4) 2 oracle不一致時の裁定は手動（合議機械化は縦Cへ持ち越し）——を確認し、
受入（または保留）の文言をchatで与える。受入後は受入判断record作成→TODO更新→次縦切りの順序選択
（候補：codex-cli第3 backend（疎通回復待ち）・縦C合議・仕分け6件の処理）へ進む。

開始条件：

- 本handoffを含むcommitが完了し、作業treeがcleanである

完了条件：

- §9-11の受入（または保留）の文言がchatで得られる

後続作業：受入判断record→TODO更新→次縦切りの順序選択。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路とclaude-subagent（Tier 3・明示受容つき）の2経路が稼働
- Human判断待ち：**§9-11製品受入**（§7.4残余risk 4点の受容）。E2E判定の非blocking所見の仕分け——`F-4`〜`F-7`（e2e-012-001判定record）と`R-1`〜`R-2`（e2e-012-002判定record）

## stale・deferred

- stale：契約008〜011の進行中表示（四契約とも受入完了）。「Tier 1以外は無条件停止」の表示（契約012実装により宣言＋明示受容の型へ一般化。既定挙動は不変）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象・条件は従前どおり。統合する場合はbackend合流でなく判定record規約への準拠——設計方針メモ§3）。契約011範囲外の後続＝自由文類型・`review_plan`出力の自動変換・縦C合議・codex-cli backend。機械gate接続は`IC-REUSE-SEARCH-GATE-CONNECTION-001`（Human仕分け待ち）。`IC-SUBAGENT-HARDENING-ENV-REUSE-001`は**採用・訂正実施済み**（2026-08-17の訂正record3件目）。実装経路確認部品の`CLAUDE_VERSION`（2.1.220のまま）は次回その経路使用時に自経路の手続きで更新。Reviewer側digest実計算の特定command許可は将来の契約改定候補

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約012対象60件（`tests/test_reviewer_launch.py`。F-1固定試験・claude経路停止試験2件を含む）、契約011対象32件（無変更）、G30運用契約実行75件、layout 13件、bootstrap 41件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,467件成功・終了コード0（F-1〜F-3修正後の実行）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
