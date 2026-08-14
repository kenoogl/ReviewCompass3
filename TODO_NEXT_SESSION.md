# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の最初のTask Contract version 1と三pathの実装開始が利用者に承認された。
- 現在作業：安全な項目選択、低乱雑性の絶対path残存時の停止、pyproject.tomlへの正規入口登録を含む案Cを、承認済みの三pathだけで試験駆動実装する段階である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / approved_for_implementation`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：G25のTask Contract判断と実装開始を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第4段完了判断](records/development/2026-08-14-recovery-plan-v5-stage4-completion-decision-v1.md) — SHA-256 `147217192ea1d4d491005bd4cb7879f292f8739364e6b912a46d3dda8b8295b7`
- [G25最初のTask Contract候補](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [G25 Task Contract定義挑戦](records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-challenge-v1.md) — SHA-256 `0d7277f98c09cfbf2c107e94a8179aa76b4f55c189c3ba024792a087ee671f52`
- [G25 Task Contract限定訂正レビュー](records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md) — SHA-256 `8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91`
- [G25 Task Contract承認判断](records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md) — SHA-256 `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`

## 次に行う一作業

承認済みの新しい読取り専用入口について、入口固有の試験を先に作り、未実装の失敗を確認する。その後、同じ試験を変えずに新入口とpyproject.tomlの実行名一件を実装する。

開始条件：

- 契約候補、限定訂正レビュー、承認判断の内容識別値が実fileと一致する
- 承認判断がapproved_for_implementationである
- G25既存10 path、G26、G30、他142 path、上流候補全体を実装範囲へ加えない

完了条件：

- 新入口がない状態で入口固有試験が未実装理由により失敗する
- 同じ試験を変更せず、新入口、pyproject.toml、対象試験の三pathだけで成功させる
- 対象試験、G25関連55件、通常の全試験、利用者向け合成例、独立完了レビューが契約条件を満たす

後続作業：独立完了レビューで止める指摘0件となった後、利用者へ実際の機能と出力例を提示し、最初の製品処理の完成を判断してもらう。

## blocker・Human判断待ち

- blocker：なし。契約と三pathの実装開始は利用者承認済みである。
- Human判断待ち：実装中に承認済みの責務、限界、三pathを変える必要が生じた場合だけ再判断する。実装完了と第5段完了は未判断である。

## stale・deferred

- stale：契約内容と実装開始のHuman判断待ちは、承認判断により解消した。訂正前候補のsetup.py登録と安全な出力境界不足も解消済みである。
- deferred：G26のrepository_root省略反例、他142 pathの個別採否、上流9文書の正式化と不一致3件、G30、外部送信、保存・探索、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：定義挑戦でG25直接関連14 fileは55件成功、終了コード0。変更点限定レビューは文書差分だけを確認し、コード・試験・設定は変更していない。
- 直近の全Test：第3段の履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。第4段完了後もコード・試験・設定は変更していないため再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
