# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段・第2段と第3段の実施作業は完了候補まで進んだ。第3段は、予定された最後の手動全体レビューとHuman段完了判断を残す。
- 現在作業：正しい現在状態の誤拒否確認と、第3段中127成果物のライフサイクル分類はそれぞれ独立レビューでverifiedとなった。第3段完了候補とClaude向け限定レビュープロンプトを固定した。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了候補・手動全体レビュー待ち`、影響：現行完了条件を満たす材料は揃ったが、利用者Decisionで残した他社モデル全体確認と段完了のHuman判断は未実施である、次：固定済みClaudeプロンプトを利用者が手動で渡し、返答をこのtaskへ戻す

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [正しい実装例による方法への修正判断](records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md) — SHA-256 `76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f`
- [既知の正しい現在状態による独立完了レビュー](records/development/2026-08-14-stage3-known-correct-state-witness-independent-completion-review-v1.md) — SHA-256 `623095ce50005400977749fa323e6bea00213db46b9487651ea42e01337afd97`
- [成果物ライフサイクル整理Evidence](records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-evidence-v1.md) — SHA-256 `ae20e42659624b76ec378b0f7a1123a29fd277d1f345f880e06bf1b38d14e5f1`
- [成果物ライフサイクル整理の独立完了レビュー](records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-independent-completion-review-v1.md) — SHA-256 `ea06bdb6566bc7e9f5653fa8a45e573b2966aed12e2e70fcd6de0a482a1544c8`
- [第3段完了候補](records/development/2026-08-14-stage3-completion-candidate-v1.md) — SHA-256 `ab9fe71622c435a8e01bf1385d682ae66814f77928edaf648fd3b3355eb6b1e4`
- [Claude向け第3段完了前全体レビュー指示](records/session-handoffs/2026-08-14-claude-stage3-completion-overall-review-prompt-v1.md) — SHA-256 `2a4f9b490007cbe5c853f5997c0754641da9441a62928c69c27f542b55581491`

## 次に行う一作業

利用者がClaude向け第3段完了前全体レビュー指示を手動で渡し、返答をこのtaskへ貼り付ける。操縦役は返答を固定材料と照合して記録する。外部送信は代行せず、第3段完了を先に承認しない。

開始条件：

- 第3段完了候補とClaude向け指示のSHA-256が実fileと一致する
- 正しい現在状態と成果物ライフサイクルの独立完了レビューがともにverifiedである
- レビュー対象を完了候補の中心判断に限定し、全1,728試験・127成果物の一律詳細確認へ広げない

完了条件：

- Claude返答の判定、止める指摘、報告不一致、反証、未実施事項を出どころどおり固定する
- 返答が固定材料と整合するかを機械照合し、本質から外れた提案を段完了条件へ混入させない
- 止める指摘0件かつ報告不一致0件なら、第3段完了可否を利用者へ明示的に戻す
- 外部送信、コード・試験・設定・Issue変更、第4段開始を行わない

後続作業：Claude結果がverifiedなら利用者が第3段完了を判断する。指摘があれば中心判断を崩す一原因だけを最小訂正候補として扱う。

## blocker・Human判断待ち

- blocker：技術的blockerはない。既存Decisionに基づく手動全体レビュー結果だけが段完了判断の前提として残る。
- Human判断待ち：利用者によるClaudeへの手動受渡しと、結果確認後の第3段完了可否。

## stale・deferred

- stale：参照文字列による17件候補・495参照、全試験の詳細人手確認、試験数削減、実行時間短縮は第3段の現役入力・完了条件にしない。
- deferred：誤った実装の受理、守れない保証表示、安全方針に反する副作用の見逃しは必要時のWork 8または通常開発へ分離する。ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001と暫定issue_resolution_v4.pyは使用停止のまま維持する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：正しい現在状態の独立確認は1,728件成功、失敗0。成果物分類はGit再生成127 path、19意味群、未分類0、重複0、役割終了0で独立レビューverified。
- 直近の全Test：観測commitの履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。以後のコード・試験・設定差分0をGit物体で確認済み。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
