# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25、一件用安全保存、一件レビュー材料、G08一件設計、G20の外部送信2契約（008・009）、『正式ツール化』縦Bの契約010（Reviewer起動アダプタ・headless正式経路）の**製品受入**まで完了。縦Aの契約011（依頼組み立て器・2類型）は採用・実装（RED30→全緑・導線配備・保護対象差分0）まで完了した。事前走査は6手順へ改定・手順書化し、正式再利用検索の導線を接続、対策4は改善候補`IC-REUSE-SEARCH-GATE-CONNECTION-001`として登録済み。
- 現在作業：契約011の最終段＝製品受入（§9-11）のHuman判断待ち。§9-8実運用E2Eと§9-10完了レビューは成立：e2e-011-001（縦A→縦B接続完走・blocking所見1件＝checkのfence内外非区別）→利用者採用の修正（RED2件先行・fence状態追跡・再発類型の前例RC2と同一原則）→e2e-011-002で**verified**（確認型info3件・blocking 0・unexamined空）。受入対象は§7.4残余risk 4点の最終受容。
- Task Contract：`TC-RC3-PRODUCT-REQUEST-BUILDER-011 / v3`＝`adopted_implementation_started`（E2E・完了レビューverified済み。製品受入待ち）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：契約011の受入作業を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

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

利用者が契約011の製品受入（§9-11）を判断する。受入対象：§7.4残余risk 4点——(1) 機械検査は形式の
守りで内容の質はLLM＋レビューの守りのまま、(2) 除外3形式定数の契約009側との将来乖離（同値性試験が
検出・停止）、(3) 雛形の実測2通基盤（類型登録形が追加を局所化）、(4) 除外と同形の実鍵の既知すり抜け
（契約009 §7.2と同一の受容・通過明示試験で可視化）。E2E 2往復と完了レビューverifiedのEvidenceは
固定済み。

開始条件：

- E2E Evidenceと本TODOが意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 製品受入（または保留・条件付き受入）の文言がchatで得られる

後続作業：受入後は後続順序の選択（claude-subagent第2 backend・縦C合議・自由文類型・API pending解除）
をHumanへ諮る。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行はagy headless正式経路が稼働中
- Human判断待ち：契約011の製品受入（§7.4残余risk 4点の最終受容）

## stale・deferred

- stale：契約008・009・010の進行中表示（受入完了）。e2e-011-001のblocking所見（fence修正442b05fとe2e-011-002 verifiedで解消）。契約011実装時の対象試験30件表示（fence敵対試験2件追加で32件）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象・条件は従前どおり。統合する場合はbackend合流でなく判定record規約への準拠——設計方針メモ§3）。契約011範囲外の後続＝自由文類型・`review_plan`出力の自動変換・縦C合議・claude-subagent／codex-cli backend。機械gate接続は`IC-REUSE-SEARCH-GATE-CONNECTION-001`（Human仕分け待ち）。Reviewer側digest実計算の特定command許可は将来の契約改定候補

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約011対象32件（`tests/test_request_builder.py`。fence敵対試験2件を含む）、契約010対象35件、G30運用契約実行75件、layout 13件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,442件成功・終了コード0（fence修正後の実行）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
