# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段、第2段、第3段は完了した。第4段は固定範囲の分類、最初の製品処理候補の選定、最小Task Contract入力の整理、独立レビューまで完了し、採用と段完了のHuman判断待ちである。
- 現在作業：コード候補152 pathを30意味群へ重複・未分類なく割り当てた。G25の読取り専用Session記録解析10 pathを最初の正式製品コード候補とし、第5段へ渡す最小入力11項目を固定した。限定訂正後レビューはverified、止める指摘0件、報告不一致0件である。
- Task Contract：`none（第4段では入力候補だけを固定し、最初のTask Contractは未定義・未承認）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：第4段の完了判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第3段完了判断](records/development/2026-08-14-recovery-plan-v5-stage3-completion-decision-v1.md) — SHA-256 `88578d3160b046cb99c847aaaa6eb4d1ce7b6ee430d4708cfa23bc559edbe0f1`
- [第4段の正式製品コード識別の追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-formal-product-code-identification-amendment-decision-v1.md) — SHA-256 `1e21e6af4be4898e98436206b950efed4e6cca825397fbc85a9030455e5e94e3`
- [第4段の軽量整理と製品機能候補を分ける追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-lightweight-code-cleanup-boundary-amendment-decision-v1.md) — SHA-256 `d54a486c93a6d0f25411765f99a7fdb669edfb1db84c7a9298a2d9b5dfb8e70a`
- [第4段の範囲作業票](docs/development/2026-08-14-stage4-product-code-and-task-contract-input-bootstrap-work-ticket-v1.md) — SHA-256 `26c0b1d117067112881a289fc871a33c374d6693e6c157b2c96c10bb4d5557c8`
- [第4段の製品コード候補とTask Contract入力Evidence](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [第4段の独立完了レビュー](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-independent-completion-review-v1.md) — SHA-256 `7072027956c67534af613e7fa71aa661edb93d118cf1c01d052c742606ef03bd`
- [第4段の限定訂正レビュー](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-correction-review-v1.md) — SHA-256 `2c5abce8085642ff02d81fef3552e154917145f581b63b64f1df81a9f4f92137`

## 次に行う一作業

利用者が、第4段の選定結果、正式製品コード集合、最初のTask Contract候補、上流候補の扱い、第4段完了を一つの意味的判断として裁定する。判断前にコード・試験・設定・Task Contractを変更しない。

開始条件：

- 訂正後Evidenceと限定訂正レビューの内容識別値が実fileと一致する
- G25の10 path採用が現状資産の再利用可否だけを決め、将来の振る舞い・実行時成熟度・製品完成を承認しないと理解する
- 製品／保留61 path、開発支援71 path、共有10 pathを最初の正式製品コード集合へ含めない境界を維持する
- 上流候補9文書を暫定の入力候補として扱い、既知の直接参照不一致3件を自動修正・正式化しない

完了条件：

- G25の10 pathを第5段で再利用できる正式製品コード集合として採用または不採用にする
- G25の読取り専用Session記録解析を最初のTask Contract候補として採用または不採用にする
- 最小入力11項目と、上流候補9文書・既知の不一致3件の扱いを第5段への固定入力として裁定する
- 第4段完了と第5段への移行を承認または保留にし、Decision recordとTODOへ固定する

後続作業：第4段完了が承認された場合だけ、第5段の最初の小作業としてG25のTask Contract案を作り、独立した定義挑戦を行う。最初のTask Contract自体は別のHuman承認対象とする。

## blocker・Human判断待ち

- blocker：なし。限定訂正レビューはverifiedであり、残るのは意味的なHuman判断だけである。
- Human判断待ち：G25の10 pathを正式製品コード集合として採用するか、他142 pathを未採用のまま維持するか、G25を最初のTask Contract候補とするか、暫定上流候補と不一致3件を固定入力として受け入れるか、第4段を完了して第5段へ移るか。

## stale・deferred

- stale：訂正前Evidenceの環境参照記述と、独立完了レビューのreport_execution_mismatch判定は、Evidence限定訂正と訂正レビューverifiedにより解消した。第3段の17件候補・495参照、試験数削減、全試験の詳細人手確認は第4段以後の入力にしない。
- deferred：G26のrepository_root省略反例の修正、製品／保留61 pathの採否、上流9文書の正式化と不一致3件の修正、G30、コード・試験・設定の変更、外部送信、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：独立レビューで152／192集合、30群、一意割当、G25の10 path閉包、G26反例、上流47参照中3不一致を再現。G25直接関連14 fileは55件成功、終了コード0。限定訂正は文書一件だけで、既確認結果はstaleでない。
- 直近の全Test：第3段の履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。第4段ではコード・試験・設定を変更していないため再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
