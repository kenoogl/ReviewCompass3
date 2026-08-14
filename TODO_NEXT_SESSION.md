# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段の最初の作業として、承認済みG25の固定入力から最初のTask Contract案を作り、独立した定義挑戦を行う段階である。
- 現在作業：G25の10 pathを第5段で再利用する正式製品コード集合として採用した。他142 pathは一括廃止せず今回の集合から除外した。G25の読取り専用Session記録解析を最初のTask Contract候補とし、最小入力11項目を固定した。
- Task Contract：`none（G25の最初のTask Contract案を次作業で定義する）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：G25のTask Contract案作成を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第4段完了判断](records/development/2026-08-14-recovery-plan-v5-stage4-completion-decision-v1.md) — SHA-256 `147217192ea1d4d491005bd4cb7879f292f8739364e6b912a46d3dda8b8295b7`
- [第4段の製品コード候補とTask Contract入力Evidence](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [第4段の限定訂正レビュー](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-correction-review-v1.md) — SHA-256 `2c5abce8085642ff02d81fef3552e154917145f581b63b64f1df81a9f4f92137`
- [Task Contract中心構想候補](docs/concepts/2026-08-02-task-contract-centered-engineering.md) — SHA-256 `80f388b9308450f1758f623346e25fa6623c8d5d59cb32979436ee3831af1d91`

## 次に行う一作業

G25の固定入力11項目から、最初のTask Contract案を一件作り、実装前の独立した定義挑戦を行う。契約案の作成中はコード・試験・設定を変更しない。

開始条件：

- 第4段完了判断、訂正後Evidence、限定訂正レビューの内容識別値が実fileと一致する
- G25の10 pathとtree SHA-256を固定し、G26、G30、他142 pathを暗黙の実装前提へ加えない
- 上流候補9件は暫定入力、既知の不一致3件は競合候補として扱い、正本へ自動昇格しない
- 最初のTask Contract案と実装開始は、定義挑戦後の別のHuman判断対象とする

完了条件：

- 安定した契約ID、版、source requirement候補とG25固定コードを結び付ける
- 責務、境界、前提、必要材料、許可能力、成果、受入条件、来歴義務、Humanへ戻す条件、版付き依存を一件の契約案へ記す
- 独立した定義挑戦で、責務の過大化、隠れた依存、未承認上流の自動採用、書込み・送信等の範囲外能力を反証する
- 止める指摘を解消または明示した契約案を、実装開始判断とともに利用者へ戻す

後続作業：利用者が最初のTask Contractの意味と実装開始を承認した場合だけ、契約で確定した小さい範囲へTDDを適用し、正規入口から利用者向け処理を接続する。

## blocker・Human判断待ち

- blocker：なし。第4段は利用者承認により完了した。
- Human判断待ち：最初のTask Contract案と独立した定義挑戦の提示後に、契約の意味と実装開始を承認するか。現時点では未判断である。

## stale・deferred

- stale：第4段の採用・完了判断待ちという表示は、本Decisionにより解消した。訂正前Evidenceの環境参照記述と最初の独立レビューのreport_execution_mismatch判定も、限定訂正レビューverifiedにより解消済みである。
- deferred：G26のrepository_root省略反例の修正、他142 pathの個別採否、上流9文書の正式化と不一致3件の修正、G30、REQ-WORKFLOW-009、外部送信、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G25直接関連14 fileは55件成功、終了コード0。独立レビューでG25の10 path閉包、群外直接依存0、G26反例、上流47参照中3不一致を再現した。第4段完了判断は文書とTODOだけで、コード・試験・設定を変更していない。
- 直近の全Test：第3段の履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。第4段ではコード・試験・設定を変更していないため再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
