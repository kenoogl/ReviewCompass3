# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の読取り専用入口を実装し、外部独立レビュー、利用者による製品受入、正式・安定表示への昇格まで完了した。第5段全体の完了候補を作成し、内部の独立全体レビューはverifiedとなった。
- 現在作業：第5段完了候補は、内部の独立全体レビューとClaudeの読み取り専用全体レビューの双方でverified、止める指摘0件、報告不一致0件となった。第5段を完了とする利用者判断だけが未実施である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / product_accepted_stable_stage5_completion_candidate_external_verified_human_decision_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：第5段の完了判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第5段全体完了候補](records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-v1.md) — SHA-256 `5e9e2adebe65372e2e315bd5fbedc07302f11451854e8ad1a52313425ed9b04a`
- [第5段完了候補の内部独立全体レビュー](records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-independent-overall-review-v1.md) — SHA-256 `0ff20a88464ad6b7121842a21194c073034f5396bd59de7250e1b1f3b685eda4`
- [Claudeによる第5段完了候補の全体レビュー結果](records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-claude-overall-review-result-v1.md) — SHA-256 `4a2a8d91e978447f4356cc4da87261074d0c07237bf93aa2cf5aa7015d7bda9e`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`

## 次に行う一作業

内部とClaudeの全体レビュー結果を判断材料として、第5段を完了とするかを利用者が明示する。次のTask Contract定義挑戦の開始判断は分離する。

開始条件：

- 第5段完了候補、内部独立全体レビュー、Claude全体レビュー結果の内容識別値が実fileと一致する
- 二つの全体レビューがverified、止める指摘0件、報告不一致0件である
- 1,740件は観測値であり恒久合格値にせず、G26・G30・上流候補9件・要求候補は未正式のままとする

完了条件：

- 利用者が第5段を完了とするかを明示する
- 完了承認の場合は、残る限界を引き継いだ完了判断記録と現在位置だけを更新する
- 完了しない場合は、理由と最小の戻り先を利用者判断として固定する

後続作業：第5段完了承認後にだけ、一件のSession記録と伏字化結果を安全に保存して再読込みする二つ目のTask Contract候補について、定義挑戦を開始するかを利用者へ戻す。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。利用者の第5段完了判断だけが未実施である。
- Human判断待ち：第5段全体を完了とするか。完了承認と次のTask Contract定義挑戦の開始は分けて判断する。

## stale・deferred

- stale：最初の実装Evidenceにある絶対path一般化と完了候補表示、限定修正Evidenceにある状態識別値4251a948...と限定GREEN commitの結び付き、同主張に依存した内部修正後レビュー判定、先行Claudeレビューの報告不一致0件表示はstaleである。製品動作の根拠は観測commit 44cc5eaでのClaude独立再実行と正式表示への独立確認へ置き換えた。
- deferred：第5段完了判断前に、二つ目のTask Contract、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：正式・安定表示への独立レビューで、新入口12件とG25直接関連55件が成功し、昇格前後の同じ合成入力に対する出力がバイト単位で一致した。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を履歴付き複製で確認した。その後の製品コード・試験・設定・配布入口の差分0件を内部全体レビューで確認し、再実行せず結果を利用した。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
