# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存の製品受入が完了し、三つ目の製品処理候補へ進んだ。
- 現在作業：利用者が候補1を選び、一件のレビュー材料作成と外部送信なし結果整理の作業契約候補v1を作成した。製品コードと試験は未変更で、次は固定候補への独立定義挑戦である。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003 / candidate_v1_pending_independent_definition_challenge_and_human_approval`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約定義確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [一件のレビュー材料作成と結果整理の作業契約候補v1](records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v1.md) — SHA-256 `574b94d6620b2bc57f36a6c84cc8a4ed17d041be096e3f9e41c9589aa9aa32b4`
- [安全保存受入後の次製品作業候補8件](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [安全保存の製品受入判断](records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md) — SHA-256 `7145f57a59efb965f64a5401f6e109685ba1920b5039fe65a4edd644af7573dc`
- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [製品コード候補と作業契約入力の目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

固定した作業契約候補v1へ、作業担当と異なる実行単位による独立定義挑戦を一回行う。責務、境界、必要材料、許可能力、禁止事項、受入条件、証拠、利用者判断点の欠落と矛盾を調べる。

開始条件：

- 作業契約候補v1と本TODOが意味単位commitへ固定され、作業場所に未記録差分がない
- レビュー担当は対象commit、契約path、SHA-256、固定根拠を受け取り、成果を変更しない
- 製品コード、試験、実利用者資料、外部送信、外部処理を変更または実行しない

完了条件：

- 開始可または修正要の一方を、止める原因と反証結果を伴って返す
- 固定参照の内容識別値、既存G02の保留境界、案Cの変更上限、利用者判断点を照合する
- 結果が修正要なら同じ原因の指摘をまとめ、実装へ進まない

後続作業：開始可なら利用者へ契約採用と実装開始を別々に求める。修正要なら原因だけを契約候補v2へ限定訂正し、変更点確認へ渡す。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。独立定義挑戦の結果後に、契約採用と実装開始を別々に判断してもらう

## stale・deferred

- stale：候補一覧にあった候補1の選択待ち表示は、利用者が候補1を選んだためstale。安全保存の旧技術検証v1・v2と旧完了レビューv1・v2も引き続きstaleである
- deferred：独立定義挑戦と利用者承認までは、製品コード、試験、正式入口、実行名、既存G02、保存、外部送信、外部処理、実利用者資料を変更・実行しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書候補だけの変更で製品試験は未実施。固定参照9件のSHA-256は全件一致、G02既存14 pathは観測commitから差分0、各確認commandは終了コード0
- 直近の全Test：製品コードと試験を変更していないため再実行していない。直近の正規全試験は1,862件成功、失敗・error・skip 0、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
