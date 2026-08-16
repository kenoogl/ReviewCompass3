# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：なし。外部APIレビューはpending（2026-08-16）。pending後の最初の区切り作業として`.gitignore`仕分け（`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`）を裁定(A)で完了した：正規tool（schema v2・intake v4検証合格）の決定record固定、除外1行の削除、参照済み歴史的依頼原文37件のcommit昇格、旧前提を固定していた既存試験1件の反転固定（利用者承認）。全試験2,375件全緑。次の一作業の選択待ちである。
- Task Contract：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009 / v2 / accepted`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [3 provider実環境確認Evidence（Gemini操縦のanthropic確認を含む）](records/development/2026-08-16-three-provider-live-check-evidence-v1.md) — SHA-256 `e04a2c95fbbe727a296dd27bbc9171dd378bfdc9409d77b788eabdd9a7b9f07d`
- [利用者による契約009の製品受入判断（残余risk最終受容・IC消費）](records/development/2026-08-16-external-send-scan-refinement-product-acceptance-decision-v1.md) — SHA-256 `a1ef5bebd6b3d918dff4080ed7faea532a3ad69b523ff206ed11eed77e916879`
- [識別子停止を維持へ訂正した契約009候補v2](records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v2.md) — SHA-256 `58e5f9165e2201892377744377a9758f79be7559fe26f82ed114ec246968e6da`
- [利用者によるG20一回送信の製品受入判断](records/development/2026-08-16-external-reviewer-single-send-product-acceptance-decision-v1.md) — SHA-256 `6f76c1c6198ccc9a0412e4a8e6751a29a89836d9d9ef5e76900772e6fa8ffa54`
- [採用中の置き場所矛盾を訂正した契約v5](records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md) — SHA-256 `6fc7b37b07f65519e78353df23fc7277c1c9265956320e46d5e6e35608e9d165`
- [暫定レビュー体制の決定（Gemini手動利用・Human中継）](records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md) — SHA-256 `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792`
- [利用者の受入済み部品運用化目標](records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md) — SHA-256 `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- [外部レビュー準備・実施の機械化目標](records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md) — SHA-256 `46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e`
- [利用者によるG02安全投影の製品受入判断](records/development/2026-08-16-one-item-review-safe-projection-product-acceptance-decision-v1.md) — SHA-256 `2cea891bb43fa83b15259310d97a459b6f446898bdedf79630cd2e945d8008cc`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者がpending外の作業から次の一作業を選ぶ。主な選択肢：(1)候補6以降（G26旧処理の残部整理・
G28継続回収・G27導入解除。候補一覧recordの推奨順）、(2)G24の要求作成責務やG02 organize・G25・
安全保存との統合など後続境界の再開判断、(3)その他利用者が指定する作業。選択後、Claudeが契約候補・
作業票の作成から着手する。

開始条件：

- 本TODO（pending反映）が意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 次の一作業の利用者選択がchatで得られる

後続作業：選択された作業の性質に応じて、仕分け材料の提示または契約候補作成→独立確認→採用判断→実装。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇により、codex exec起動によるレビューは停止（暫定Gemini体制で代替中）
- Human判断待ち：pending外からの次の一作業の選択

## stale・deferred

- stale：契約008・009の実装・レビュー・E2E各段階の進行中表示はすべてstale（両契約とも受入完了）
- deferred：**外部APIレビュー関連一式は利用者判断でpending**（2026-08-16。対象：機械化縦切り(a)依頼組み立て器・(b)prompt品質gate・(c)判定取り込み、応答解析・監査自動化・旧egress設計統合・複数送信、開発レビュー運搬のHuman中継から本経路への移行判断、5段手続きの手順書化、external_send_approved表示の観測登録。再開は利用者指示による。送信路自体は受入済みで利用可能なまま）。G24の要求作成責務、G02 organize・G25・安全保存との統合、既存G30基盤の正式化、候補6以降、実利用者資料の使用は後続境界まで対象外。`.gitignore`食い違い（`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`）は裁定(A)実行済み・解消

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：送信路対象61件（改名後`tests/test_external_review_send.py`。既存49＋精密化12）、egress関連107件、G02 158件、G08 107件、G24 111件、実行器75件、G30基盤e2e 38件、layout 13件（応答raw除外の維持試験1件追加後）——各単独終了コード0。保護path差分0（基準は契約009 v2 §6の固定commit）
- 直近の全Test：禁止認証隔離条件の正規全試験2,375件成功・終了コード0（契約009 GREEN・layout除外後）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
