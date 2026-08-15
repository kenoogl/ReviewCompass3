# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存の製品受入が完了し、三つ目の製品処理候補へ進んだ。
- 現在作業：作業契約候補v3は変更点の独立確認で開始可となった。止める指摘は0件で、製品コードと試験は未変更。利用者の契約採用と案Cの実装開始判断を待つ。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003 / candidate_v3_ready_for_human_contract_and_implementation_decision`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約定義確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [残る2原因を限定訂正した作業契約候補v3](records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v3.md) — SHA-256 `a52cd717f6709c5ca01a1e339385272abfe976a0b9ce176e857b427778cf07d6`
- [作業契約候補v3の変更点確認・開始可](records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v2.md) — SHA-256 `2e612712b194517097f0439398f61e505d0d9bb18fe8c50ae8c39f9c39e1b423`
- [作業契約候補v2の変更点確認・修正要](records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v1.md) — SHA-256 `8544484e25c7af07743002793c63a591aa3ad63c2dd09ce74f512fead4899a1f`
- [作業契約候補v1の独立定義挑戦・修正要](records/development/2026-08-15-one-item-review-task-contract-definition-challenge-v1.md) — SHA-256 `c1ec9fc3dc033c1dbf14c5201966497b1e2c8eae18cd38ededce5e8637ebd4b3`
- [安全保存受入後の次製品作業候補8件](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [安全保存の製品受入判断](records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md) — SHA-256 `7145f57a59efb965f64a5401f6e109685ba1920b5039fe65a4edd644af7573dc`
- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [製品コード候補と作業契約入力の目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

利用者が、開始可となった作業契約候補v3の採用と、案Cの変更上限内での実装開始を判断する。推奨は両方を承認することである。

開始条件：

- 作業契約候補v3、開始可の変更点確認、本TODOが意味単位commitへ固定され、作業場所に未記録差分がない
- 契約採用と実装開始が別の判断であり、承認しても外部送信、外部処理、保存を許可しないことを利用者へ示す
- 変更上限が新しい製品核1、入口1、実行名1、対象試験1、短い証拠記録だけである

完了条件：

- 利用者が候補v3の契約採用可否を明示する
- 利用者が案Cの実装開始可否を明示する
- 不承認または条件付き承認なら、製品codeと試験を変更せず差分条件を固定する

後続作業：両方承認なら、実装境界の事前確認を作り、失敗試験を先に固定する。承認されない場合は実装へ進まない。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：候補v3を作業契約として採用するか、案Cの変更上限内で実装を開始するかの二点。推奨は両方承認

## stale・deferred

- stale：契約候補v1とv2は各修正要により実装開始根拠としてstale。候補1の選択待ち表示と安全保存の旧検証・旧レビューも引き続きstaleである
- deferred：利用者が契約採用と実装開始を承認するまでは、製品コード、試験、正式入口、実行名、既存G02、保存、外部送信、外部処理、実利用者資料を変更・実行しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書候補だけの変更で製品試験は未実施。固定参照とG02境界は一致。絶対pathの停止例6件と非停止例3件、配列順・指摘署名を独立確認し、終了コード0で開始可
- 直近の全Test：製品コードと試験を変更していないため再実行していない。直近の正規全試験は1,862件成功、失敗・error・skip 0、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
