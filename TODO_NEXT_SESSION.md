# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：G30最初の縦切り『最小運用契約実行』は、契約候補v2のCodex限定再確認で停止原因1件（hard link公開確定後の一時名削除失敗が未定義）の修正要となった。本線1-4自律実行指示に基づき、公開確定点と`partial_cleanup_failed`（終了コード6・最終名は正本として残存・回復境界）を一意化した契約候補v3を作成し、Codexの限定再確認へ進む。registry縮小（G08・G24の2操作）は開始可判定済み。実装は未開始である。
- Task Contract：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006 / v3 / limited_independent_rereview_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者の受入済み部品運用化目標](records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md) — SHA-256 `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- [公開確定点を一意化した最小運用契約実行の契約候補v3](records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v3.md) — SHA-256 `d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85`
- [契約候補v2を停止原因1件で修正要としたCodex限定再確認](records/development/2026-08-16-minimal-operation-contract-execution-v2-limited-rereview-v1.md) — SHA-256 `1926cfa2f4ebbb45d500813348e61cebc9f25018eae22194d28afaaa5aec005d`
- [利用者による一件の要求候補整合検査の製品受入判断](records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md) — SHA-256 `dd9edcfd5895c143f7c83c05dcc2df986d36d066030782a5577d534071866fd8`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

Codexが固定された契約候補v3を成果物変更なしで読み、v2の停止原因1件（公開確定後の一時名削除失敗の未定義）が
`partial_cleanup_failed`の一意な定義で閉じたかと、他境界の退行の有無だけを限定再確認し、判定record 1件を
単独commitして停止する。起動はClaudeがcodex execで行う（利用者の本線1-4自律実行指示による）。

開始条件：

- 契約候補v3、依頼record、本TODOが意味単位commitへ固定され、作業treeがcleanである
- Codexは依頼recordの鮮度検査に合格してから動く
- 製品コード、既存試験、既存G30基盤、受入済み部品を変更せず読取り専用で確認する

完了条件：

- 訂正1点の閉鎖と、v2で開始可とされた境界（registry縮小、目的縮小、機微検査、束縛照合位置、固定識別値）の退行有無を確認する
- 再利用4 file・保護10 path・機微規則の内容識別値一致を機械確認する
- 判定recordに開始可または修正要を根拠、未接続条件、最小修正とともに書き、単独commitして停止する
- Claudeが判定recordの鮮度・変更path 1件・判定内容を機械照合する

後続作業（Claudeが実施、自律実行指示の範囲）：開始可なら条件付き事前承認に基づき採用judgmentを記録して実装（失敗試験→最小実装→退行確認→独立完了レビュー）へ進み、修正要なら契約だけを次版へ訂正する。最終の製品受入だけは利用者判断として残す。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：なし。利用者の本線1-4自律実行指示の下で進行中。最終の製品受入だけを後で求める

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
