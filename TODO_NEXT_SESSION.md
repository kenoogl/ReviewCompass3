# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の最初のTask Contractに基づく読取り専用製品入口を実装し、修正後の外部独立レビューまで完了した。
- 現在作業：新入口はHuman受入候補である。Claudeは観測commit 44cc5eaの複製で対象12件、関連を含む67件、正規全試験1,740件の成功を独立確認した。古い受領記録とcommitの結び付き説明は不一致として無効化し、観測commitの直接再実行を根拠に置き換えた。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / implementation_complete_pending_human_acceptance`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：G25製品入口のHuman受入を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [G25 Task Contract承認判断](records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md) — SHA-256 `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- [G25製品入口Claude修正後完了レビュー結果](records/development/2026-08-14-stage5-g25-session-artifact-entry-claude-completion-review-result-v1.md) — SHA-256 `2eda7a0ac9f89d53df9a75298ad494d75a613b89606ecc20ca6f17bd251ee637`
- [G25受領記録の状態結び付き訂正裁定](records/development/2026-08-14-stage5-g25-session-artifact-entry-receipt-binding-adjudication-v1.md) — SHA-256 `0479601e87114a438afaf0536f0327d321c87dd6e534a042907d6869dec7ae2f`

## 次に行う一作業

利用者がG25読取り専用製品入口の機能、用途、出力、限界を確認し、最初の製品処理として正式に受け入れるかを判断する。

開始条件：

- Task Contract、承認判断、Claudeレビュー結果、状態結び付き訂正裁定の内容識別値が実fileと一致する
- 古い状態識別値と限定GREEN commitの結び付き説明、およびそれに依存した内部レビュー判定を再利用しない
- 製品入口はprovisional、non-normative、promotion_required trueのままで、正式化を先取りしていない

完了条件：

- 利用者が製品入口を受け入れるか受け入れないかを明示する
- 受入の場合も、全機微情報の検出保証がなく、外部送信は未承認である限界を維持する
- 不受入の場合は製品入口を正式化せず、利用者が後続routeを決める

後続作業：Human受入の場合だけ成熟度表示の正式化と第5段の現在位置を別の意味単位で判断する。第5段完了はこの受入判断だけでは自動決定しない。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。製品入口のHuman受入だけが未完了である。
- Human判断待ち：G25読取り専用入口を、最初の製品処理として正式に受け入れるか。現時点では未判断である。

## stale・deferred

- stale：最初の実装Evidenceにある絶対path一般化と完了候補表示、限定修正Evidenceにある状態識別値4251a948...と限定GREEN commitの結び付き、同主張に依存した内部修正後レビュー判定、Claudeレビューの報告不一致0件表示はstaleである。製品動作の根拠は観測commit 44cc5eaでのClaude独立再実行へ置き換えた。
- deferred：正式・安定表示への昇格、第5段完了、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Claudeが固定した観測状態の複製で、新入口12件とG25直接関連55件の合計67件の成功、終了コード0を独立確認した。
- 直近の全Test：Claudeが固定した観測状態の複製で正規全試験1,740件成功、失敗・error・skip 0、終了コード0、Python 3.13.14、pytest 8.4.2、runner版2、代替実行なしを独立確認した。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
