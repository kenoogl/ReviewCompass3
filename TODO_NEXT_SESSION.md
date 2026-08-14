# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の読取り専用入口を実装し、外部独立レビューと利用者による製品受入まで完了した。
- 現在作業：G25読取り専用入口はReviewCompass3の最初の製品処理として受け入れられた。機能と安全上の限界は確定したが、成熟度表示は暫定のままであり、正式・安定表示への昇格と第5段完了は未判断である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / product_accepted_pending_maturity_promotion`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：G25製品入口の正式・安定表示への昇格判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [G25製品入口受入判断](records/development/2026-08-14-stage5-g25-session-artifact-product-entry-acceptance-decision-v1.md) — SHA-256 `57818c4390c02b866c55708b4292e965144d281a2349a5d12ad27bc4d31b7187`
- [G25製品入口Claude修正後完了レビュー結果](records/development/2026-08-14-stage5-g25-session-artifact-entry-claude-completion-review-result-v1.md) — SHA-256 `2eda7a0ac9f89d53df9a75298ad494d75a613b89606ecc20ca6f17bd251ee637`
- [G25受領記録の状態結び付き訂正裁定](records/development/2026-08-14-stage5-g25-session-artifact-entry-receipt-binding-adjudication-v1.md) — SHA-256 `0479601e87114a438afaf0536f0327d321c87dd6e534a042907d6869dec7ae2f`

## 次に行う一作業

受け入れ済みのG25読取り専用入口について、機能と安全上の限界を変えずに、成熟度表示を正式・安定へ昇格できるかを判断する。

開始条件：

- Task Contract、製品受入判断、Claudeレビュー結果、状態結び付き訂正裁定の内容識別値が実fileと一致する
- 古い状態識別値と限定GREEN commitの結び付き説明、およびそれに依存した内部レビュー判定を再利用しない
- 製品入口はprovisional、non-normative、promotion_required trueのままで、利用者の昇格判断を先取りしていない

完了条件：

- 正式・安定表示へ昇格する意味、変更範囲、維持する限界を平易に示す
- 昇格するか暫定表示を維持するかを利用者が明示する
- 昇格する場合も、全機微情報の検出保証がなく、外部送信は未承認である限界を変更しない

後続作業：成熟度表示の判断後に、第5段の残る完了条件を全体確認し、第5段完了を別に利用者へ戻す。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。成熟度表示を正式・安定へ昇格するかの判断が未完了である。
- Human判断待ち：受け入れ済みのG25読取り専用入口を正式・安定表示へ昇格するか。現時点では未判断である。

## stale・deferred

- stale：最初の実装Evidenceにある絶対path一般化と完了候補表示、限定修正Evidenceにある状態識別値4251a948...と限定GREEN commitの結び付き、同主張に依存した内部修正後レビュー判定、Claudeレビューの報告不一致0件表示はstaleである。製品動作の根拠は観測commit 44cc5eaでのClaude独立再実行へ置き換えた。
- deferred：第5段完了、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

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
