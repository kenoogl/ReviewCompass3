# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』の縦B契約010（Reviewer起動アダプタ・headless正式経路）と**縦A契約011（依頼組み立て器・2類型）の製品受入**まで完了。依頼record作成はassemble→LLM記入→check合格が正式経路になった。事前走査は6手順へ改定・手順書化し、正式再利用検索の導線を接続、機械gate接続は改善候補`IC-REUSE-SEARCH-GATE-CONNECTION-001`として登録済み。
- 現在作業：契約012（claude-subagent第2 backend・Tier 2／3受容機構）の残り受入条件を進める。実装完了に加え、subagent許可modelの承認・定数固定（`claude-opus-5`）、§7.2契約訂正3件（`--verbose`列挙漏れ・通過変数の`USER`欠落＝実行器9変数と同値化・抑制注入変数9種の流用＝改善候補採用）まで完了し、**E2Eの前提は全て解消済み**（起動場所は操縦環境＝案B。認証成立・抑制つき起動を実測確認）。付随して本体自動更新（2.1.220→2.1.224）による`claude_bootstrap`のpin不一致24件を利用者承認のpin更新で復旧。残り＝(1) §9-8実E2E（`--accept-tier 3`＋受容根拠の明示。同一対象集合の別名依頼で初の2 oracle比較。**実施指示受領済み**）、(2) §9-10完了レビュー（agy・Tier 1）、(3) §9-11製品受入。
- Task Contract：`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012 / v2＋§7.2訂正record3件`＝`adopted_implementation_started`（実装・model承認・訂正済み。E2E・完了レビュー・製品受入待ち）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：契約012の受入作業を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

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

利用者の明示指示（Tier 3受容の明示を含む）を受けて§9-8実E2Eを行う。内容＝契約011の正式経路で
§9-10完了レビューと同一対象集合の別名依頼record（slug末尾`-subagent`）を組み立て→受容根拠record作成→
操縦環境から`--accept-tier 3`・run-id `e2e-012-001`で起動（親環境から`ANTHROPIC_BASE_URL`等の
禁止変数を外す運用。認証は保存済みsubscriptionログイン——通過変数訂正で成立を実測済み）→
転記・事後照合。不成立なら停止し、自動再試行をしない。

開始条件：

- 本handoffを含むcommitが完了し、作業treeがcleanである
- 利用者のE2E実施指示と`--accept-tier 3`受容の明示がchatで得られる

完了条件：

- E2E一往復の成立（判定record取得）、または停止理由の確定

後続作業：§9-10完了レビュー（agy・Tier 1）→§9-11製品受入→次縦切りの順序選択。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路が稼働中
- Human判断待ち：§9-8実E2Eの実施指示（`--accept-tier 3`受容の明示。その後に完了レビュー・製品受入）

## stale・deferred

- stale：契約008〜011の進行中表示（四契約とも受入完了）。「Tier 1以外は無条件停止」の表示（契約012実装により宣言＋明示受容の型へ一般化。既定挙動は不変）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象・条件は従前どおり。統合する場合はbackend合流でなく判定record規約への準拠——設計方針メモ§3）。契約011範囲外の後続＝自由文類型・`review_plan`出力の自動変換・縦C合議・codex-cli backend。機械gate接続は`IC-REUSE-SEARCH-GATE-CONNECTION-001`（Human仕分け待ち）。`IC-SUBAGENT-HARDENING-ENV-REUSE-001`は**採用・訂正実施済み**（2026-08-17の訂正record3件目）。実装経路確認部品の`CLAUDE_VERSION`（2.1.220のまま）は次回その経路使用時に自経路の手続きで更新。Reviewer側digest実計算の特定command許可は将来の契約改定候補

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約012対象57件（`tests/test_reviewer_launch.py`。通過変数・注入の訂正6件を含む）、契約011対象32件（無変更）、G30運用契約実行75件、layout 13件、bootstrap 41件（pin更新後）——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,464件成功・終了コード0（注入訂正後の実行）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
