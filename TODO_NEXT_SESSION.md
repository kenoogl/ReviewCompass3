# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の読取り専用入口を実装し、外部独立レビュー、利用者による製品受入、正式・安定表示への昇格まで完了した。
- 現在作業：G25読取り専用入口はReviewCompass3の最初の正式・安定した製品処理となった。独立レビューはverified、止める指摘0件、報告不一致0件である。第5段全体の完了確認と利用者判断は未実施である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / product_accepted_stable_pending_stage5_completion_review`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：第5段の全体完了確認を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [G25正式・安定表示への昇格判断](records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-decision-v1.md) — SHA-256 `b0529f44d202c4b9c49600624417a54a611ad8eb77581ee9515c941291f850d1`
- [G25正式・安定表示への昇格Evidence](records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-evidence-v1.md) — SHA-256 `51df5b3b84ce3ca846fc7206b0c1c9ad290db6021bb0dbe91f5f2dd4297bd6a4`
- [G25正式・安定表示への独立完了レビュー](records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-independent-completion-review-v1.md) — SHA-256 `3258ca6ea289852ef6a065bc5d103928fa654a15a4b56a455ee3e24741adfb92`

## 次に行う一作業

立て直し計画v5の第5段について、承認済みTask Contract、正式・安定した製品入口、証拠付きの正規実行、次作業の導出を全体確認し、第5段完了候補を利用者へ戻す。

開始条件：

- Task Contract、製品受入判断、昇格判断、昇格Evidence、独立完了レビューの内容識別値が実fileと一致する
- 古い状態識別値と限定GREEN commitの結び付き説明、およびそれに依存した内部レビュー判定を再利用しない
- 製品入口がstable、normative、promotion_required falseで、独立レビューがverifiedである

完了条件：

- 第5段の完了条件と実際の成果を一対一で対応付ける
- 完了候補について独立した全体レビューを行い、止める指摘と報告不一致を確認する
- 第5段を完了とするかを利用者が別に明示する

後続作業：第5段完了承認後にだけ、製品計画と次のTask Contractの関係から次の製品作業を選ぶ。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。第5段の全体完了レビューと利用者の段完了判断が未実施である。
- Human判断待ち：第5段全体を完了とするか。全体レビュー後に判断し、現時点では未判断である。

## stale・deferred

- stale：最初の実装Evidenceにある絶対path一般化と完了候補表示、限定修正Evidenceにある状態識別値4251a948...と限定GREEN commitの結び付き、同主張に依存した内部修正後レビュー判定、Claudeレビューの報告不一致0件表示はstaleである。製品動作の根拠は観測commit 44cc5eaでのClaude独立再実行へ置き換えた。
- deferred：第5段完了判断前に、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：正式・安定表示への独立レビューで、新入口12件とG25直接関連55件が成功し、昇格前後の同じ合成入力に対する出力がバイト単位で一致した。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を履歴付き複製で確認した。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
