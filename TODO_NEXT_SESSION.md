# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存の製品受入が完了し、三つ目の製品処理候補へ進んだ。
- 現在作業：一件のレビュー材料作成と外部送信なし結果整理の作業契約候補v1は独立定義挑戦で修正要となった。3原因だけを候補v2へ限定訂正し、製品コードと試験は未変更である。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003 / candidate_v2_pending_limited_independent_review_and_human_approval`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約定義確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [3原因を限定訂正した作業契約候補v2](records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v2.md) — SHA-256 `60b8703e5a361eb7f509ecdb7532c1b928450bf55aea5c2eb9814020046d3e37`
- [作業契約候補v1の独立定義挑戦・修正要](records/development/2026-08-15-one-item-review-task-contract-definition-challenge-v1.md) — SHA-256 `c1ec9fc3dc033c1dbf14c5201966497b1e2c8eae18cd38ededce5e8637ebd4b3`
- [安全保存受入後の次製品作業候補8件](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [安全保存の製品受入判断](records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md) — SHA-256 `7145f57a59efb965f64a5401f6e109685ba1920b5039fe65a4edd644af7573dc`
- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [製品コード候補と作業契約入力の目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

固定した作業契約候補v2へ、先行独立定義挑戦と同じ担当が変更点だけの独立確認を一回行う。3原因の解消と新しい矛盾の有無を調べる。

開始条件：

- 作業契約候補v2、先行独立定義挑戦、本TODOが意味単位commitへ固定され、作業場所に未記録差分がない
- レビュー担当はv1とv2のpath・SHA-256、先行3原因、対象commitを受け取り、成果を変更しない
- 製品コード、試験、実利用者資料、外部送信、外部処理を変更または実行しない

完了条件：

- 開始可または修正要の一方を、3原因ごとの解消判定と反証結果を伴って返す
- 識別子を含む全入力文字列、複製review、人の判断一覧、閉じた出力、固定絶対path規則を照合する
- 結果が修正要なら同じ原因の指摘をまとめ、実装へ進まない

後続作業：開始可なら利用者へ契約採用と実装開始を別々に求める。修正要なら実装へ進まず、残る原因をまとめる。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。独立定義挑戦の結果後に、契約採用と実装開始を別々に判断してもらう

## stale・deferred

- stale：契約候補v1は独立定義挑戦の修正要により実装開始根拠としてstale。候補1の選択待ち表示と安全保存の旧検証・旧レビューも引き続きstaleである
- deferred：候補v2の変更点確認と利用者承認までは、製品コード、試験、正式入口、実行名、既存G02、保存、外部送信、外部処理、実利用者資料を変更・実行しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書候補だけの変更で製品試験は未実施。独立定義挑戦は固定参照9件と検査codeのSHA-256一致、G02既存14 path差分0、集合SHA一致を確認。各commandは終了コード0
- 直近の全Test：製品コードと試験を変更していないため再実行していない。直近の正規全試験は1,862件成功、失敗・error・skip 0、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
