# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：『G02一件レビューの安全投影操作の追加』の契約候補v1はCodex独立確認で停止原因1件（§7.1の停止理由集合が8種の記載と9件の列挙で競合）の修正要となった。`stale_material`（organize経路専用）を外した8理由の閉じた列挙へ訂正した契約候補v2を作成し、Codexの限定再確認へ進む。投影・束縛・保護基準は問題なしと判定済み。実装は未開始で、開始可後に利用者の採用判断を求める。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-SAFE-PROJECTION-007 / v2 / limited_independent_rereview_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者の受入済み部品運用化目標](records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md) — SHA-256 `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- [停止理由集合を一意化したG02安全投影の契約候補v2](records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v2.md) — SHA-256 `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603`
- [契約候補v1を停止原因1件で修正要としたCodex独立確認](records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md) — SHA-256 `b211626ba83409e9a892c202c0903e1363b535dc93b6f390627d42361ba3d33f`
- [利用者による最小運用契約実行の製品受入判断](records/development/2026-08-16-minimal-operation-contract-execution-product-acceptance-decision-v1.md) — SHA-256 `8386ee089ff54b0fde80fca4592a58d8e660e71cd11cb9687e676ca3f824e808`
- [Codex独立完了再レビュー・verified判定](records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-rereview-v1.md) — SHA-256 `00825b1fbce7a3ea91177d1493c9098bbfea6a7a76868e24f8f050b1f59dc927`
- [blocking 3件の訂正Evidence](records/development/2026-08-16-minimal-operation-contract-execution-correction-evidence-v1.md) — SHA-256 `c2a386c87e542a7f626e77b931bb24672fd6bf392fda71e216a5c19923959c30`
- [実装成功Evidence（RED・契約欠陥発見・GREEN・全試験・E2E）](records/development/2026-08-16-minimal-operation-contract-execution-green-evidence-v1.md) — SHA-256 `145f4938b7358acf301195901dfcacdf633b712927e60539c2db8e956c088336`
- [採用中の最小運用契約実行の契約v4](records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md) — SHA-256 `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
- [条件付き事前承認の成立による契約v3採用judgment](records/development/2026-08-16-minimal-operation-contract-execution-adoption-decision-v1.md) — SHA-256 `5f8c9fab3e3512376359f4b58ca528b87adcb74d0d488e1e86af1af06f2b6614`
- [契約候補v3を開始可としたCodex限定再確認](records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md) — SHA-256 `daa414658c2d6fc8ef712ceb47ae9b188cd787c1214be1ab826209795e97689e`
- [利用者による一件の要求候補整合検査の製品受入判断](records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md) — SHA-256 `dd9edcfd5895c143f7c83c05dcc2df986d36d066030782a5577d534071866fd8`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

Codexが固定された契約候補v2を成果物変更なしで読み、v1の停止原因1件（停止理由集合の8種・9種競合）が
閉じた8理由の列挙で解消したかと、他境界の退行の有無だけを限定再確認し、判定record 1件を単独commitして停止する。
起動はClaudeがcodex execで行う。

開始条件：

- 契約候補v2、依頼record、本TODOが意味単位commitへ固定され、作業treeがcleanである
- Codexは依頼recordの鮮度検査に合格してから動く

完了条件：

- 判定recordが得られ、Claudeが鮮度・変更path 1件・判定内容を機械照合する

後続作業：開始可なら利用者へ縮小境界の採用と実装開始の判断を求める（新契約のため条件付き事前承認は引き継がない）。修正要ならClaudeが契約だけを次版へ訂正し限定再確認へ戻す。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：なし。契約候補v1の独立確認が開始可になった後に、採用と実装開始の判断を求める

## stale・deferred

- stale：候補3実行中の表示、次の一件の選択待ち表示はstale
- deferred：G24の要求作成責務、G02 organize・G25・安全保存との統合、既存G30基盤の正式化、候補5以降、外部送信、実利用者資料の使用は後続境界まで対象外。`.gitignore`食い違いは`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`として登録済み、Human仕分け待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象111件、G24既存関連59件、要求artifact関連21件、G08対象107件が各単独成功、終了コード0
- 直近の全Test：禁止認証環境6件を除く隔離条件で正規全試験2,238件成功、終了コード0。通常host環境の既存executor安全拒否12件は実装前cleanなHEADの一時worktreeで同一再現し退行なしと確認済み
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
