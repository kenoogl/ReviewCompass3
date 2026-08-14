# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段、第2段、第3段は完了した。第4段は範囲作業票と独立開始前レビューまで完了し、分類開始のHuman承認待ちである。
- 現在作業：第4段の上流候補、コード候補152 path、試験関連192 path、二軸分類、最初の製品処理候補一群だけを深掘りする境界を固定した。独立レビューは開始可、止める指摘0件、報告不一致0件であり、分類と候補選定は未実施である。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：第4段の開始を妨げない。状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する、次：Issue状態を変更せず、第4段の固定範囲について利用者判断を得る

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第3段完了判断](records/development/2026-08-14-recovery-plan-v5-stage3-completion-decision-v1.md) — SHA-256 `88578d3160b046cb99c847aaaa6eb4d1ce7b6ee430d4708cfa23bc559edbe0f1`
- [第4段の正式製品コード識別の追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-formal-product-code-identification-amendment-decision-v1.md) — SHA-256 `1e21e6af4be4898e98436206b950efed4e6cca825397fbc85a9030455e5e94e3`
- [第4段の軽量整理と製品機能候補を分ける追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-lightweight-code-cleanup-boundary-amendment-decision-v1.md) — SHA-256 `d54a486c93a6d0f25411765f99a7fdb669edfb1db84c7a9298a2d9b5dfb8e70a`
- [第4段の範囲作業票](docs/development/2026-08-14-stage4-product-code-and-task-contract-input-bootstrap-work-ticket-v1.md) — SHA-256 `26c0b1d117067112881a289fc871a33c374d6693e6c157b2c96c10bb4d5557c8`
- [第4段の独立開始前レビュー](records/development/2026-08-14-stage4-product-code-and-task-contract-input-start-review-v1.md) — SHA-256 `d4eafd3048f5a4417228430ae4cdc8dfb88d3fd610674707fc8374b3e72d7206`

## 次に行う一作業

利用者が第4段の固定範囲を承認した後、152コード候補を意味群へ分けて二軸で軽く分類し、最初に詳しく確認する製品処理候補を一群だけ選ぶ。Human承認前には開始しない。

開始条件：

- 上流候補13件、コード候補152 path、試験関連192 pathを固定入力とすることを利用者が承認する
- 用途と今後の扱いを別軸で分類し、候補文書を正本へ自動昇格しないことを利用者が承認する
- 全152件は軽い分類に留め、最初の一群と到達範囲だけを詳しく確認することを利用者が承認する
- 既存のGit、rg、一時的な構文木解析だけを使い、新台帳・新検査器・新試験・新関門を作らないことを利用者が承認する

完了条件：

- 152 pathを重複・未分類なく意味群へ割り当て、用途区分と今後の扱いを別々に記録する
- 不明点を推測で埋めず、不明または保留として残す
- 最初の製品処理候補を一群だけ選び、利用者価値、現在入口、依存範囲、関連試験・文書を示す
- 外部送信、不可逆操作、権限変更、使用停止処理、未完成Task Contract機構を最初の候補から除外する
- 独立完了レビュー後に、候補採用の意味的判断を利用者へ戻す

後続作業：利用者が選定結果を承認した場合だけ、最初の製品処理候補の到達範囲を詳しく確認する。コード・試験・設定の変更は別の承認済み作業票で扱う。

## blocker・Human判断待ち

- blocker：なし。独立開始前レビューは開始可だが、分類開始にはHuman承認が必要である。
- Human判断待ち：第4段の固定入力、二軸分類、確認の深さ、既存read-only手段だけを使う方針の四点を承認するか。

## stale・deferred

- stale：第3段の17件候補・495参照、試験数削減、全試験の詳細人手確認は第4段の入力にしない。第4段の当初151件という途中集計は、拡張子なし実行コード1件を加えた152件へ訂正済みである。
- deferred：current 3文書の直接参照不一致3件は入力として保持し、本作業で修正・正式化しない。三種類の品質問題、Work 8、最初のTask Contract、REQ-WORKFLOW-009、外部送信、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：独立レビューでコード候補152 path・試験関連192 pathと4つの内容識別値を再現し、追跡shebang・実行属性・symlink・別拡張子・別配置Python・配布入口の漏れ0件。統合3文書の直接参照47件中、既知の3件だけ不一致。
- 直近の全Test：第3段の履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。第4段の範囲固定ではコード・試験・設定を変更していないため再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
