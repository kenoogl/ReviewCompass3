# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第4段を完了した。第5段では、G25の最初のTask Contractに基づく読取り専用製品入口を実装し、内部独立レビューの二指摘を限定修正した。
- 現在作業：新入口は完成候補である。対象12件、関連を含む67件、正規全試験1,740件が成功し、内部の限定修正レビューはverifiedとなった。外部の独立レビューとHuman受入は未完了である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / implementation_complete_pending_external_review_and_human_acceptance`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：G25製品入口の外部レビューとHuman受入を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [G25 Task Contract承認判断](records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md) — SHA-256 `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- [G25製品入口限定修正Evidence](records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-evidence-v1.md) — SHA-256 `2d297c90834d6c33c40cadcc4bcf3c53a29c57a939dea539f526913ba34126b5`
- [G25製品入口限定修正レビュー](records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-review-v1.md) — SHA-256 `43c18eee186a823376cf75a53dfd1fe9cfd799eebbe6c959ba91255a9d7177a5`
- [Claude向け修正後完了レビュー指示](records/session-handoffs/2026-08-14-claude-stage5-g25-session-artifact-entry-completion-review-prompt-v2.md) — SHA-256 `e8ce5978134bcfc44a372d81c91162a588836f44ae47d1ecced197df7f553003`

## 次に行う一作業

利用者がClaude向け修正後完了レビュー指示v2を他社モデルへ手動で渡し、読み取り専用の独立レビュー結果をこの作業へ戻す。結果がverifiedの場合だけ、実際の機能、用途、出力例、限界を確認して製品受入を判断する。

開始条件：

- Task Contract、承認判断、限定修正Evidence、限定修正レビュー、Claude指示v2の内容識別値が実fileと一致する
- 内部限定修正レビューがverified、止める指摘0件、報告不一致0件である
- 外部レビューは観測commit 44cc5eaだけを対象にし、repository fileを変更しない

完了条件：

- 外部レビューが契約適合、三path境界、安全出力、配布入口、禁止副作用、試験と状態の結び付きを判定する
- 止める指摘があればHuman受入へ進まず、不可欠な最小訂正だけを利用者へ戻す
- verifiedなら利用者が製品の機能、用途、限界を確認し、受入または不受入を裁定する

後続作業：Human受入の場合だけ成熟度表示の正式化と第5段の現在位置を別の意味単位で判断する。不受入なら入口を正式化せず、利用者が次のrouteを決める。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。外部独立レビューとHuman受入が未完了である。
- Human判断待ち：外部レビュー結果を踏まえ、G25読取り専用入口を最初の製品処理として受け入れるか。現時点では未判断である。

## stale・deferred

- stale：最初の実装Evidenceにある絶対path一般化と完了候補表示は先行レビューによりstaleである。限定修正Evidenceとverifiedレビューが修正後状態の根拠である。
- deferred：正式・安定表示への昇格、第5段完了、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：修正後の新入口12件とG25直接関連55件の合計67件が成功、終了コード0。限定REDは追加二例だけ失敗し、限定GREENは同じ試験で12件成功した。
- 直近の全Test：正規入口で1,740件成功、失敗・error・skip 0、終了コード0、Python 3.13.14、pytest 8.4.2、runner版2、代替実行なし。件数は現在集合の観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
