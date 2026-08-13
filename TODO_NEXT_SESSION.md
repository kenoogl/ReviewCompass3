# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G04に残る処理目録生成器、基準資料、固定試験を再評価し、独立確認まで完了した。一式は混在単位のため今回は削除しない。一方、比較処理が禁止関数を許可関数名として誤表示する問題を確認し、扱う時期の利用者判断を待つ。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 16意味群分類完了 / 最初の整理単位完了 / 処理目録は維持候補 / 安全条件のroute判断待ち`、影響：処理目録の比較結果を現在の安全保証と誤認すると、禁止された処理起動を見逃す一方、正本判断なしの削除も現在の監査再現性を失う、次：利用者が安全条件の食い違いをいま扱うか、候補として後回しにするか、本線へ戻るだけかを判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [処理目録の役割再評価 作業票](docs/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-bootstrap-work-ticket-v1.md) — SHA-256 `34da7143927e8813251926eb38a3263f04c952dad31cdf69dc4bd1d02bb9b039`
- [処理目録の役割再評価Evidence](records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-evidence-v1.md) — SHA-256 `887b6f71390c899461838e8e9f9eaf6387103efc6bb383a5c6dd20a379c62f50`
- [処理目録の役割再評価 独立完了レビュー](records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-independent-completion-review-v1.md) — SHA-256 `34fc8dedbea2a1be5164977244a6d2799785e574e496ea6e42e5f958657a0934`
- [最初の試験整理 独立完了レビュー](records/development/2026-08-13-stage3-first-test-cleanup-independent-completion-review-v1.md) — SHA-256 `1ba8fef13216c5e6ee93dff431f336eda131ef23f6c9929efef3b2e83bd113c2`

## 次に行う一作業

利用者が、処理目録比較と現在の安全条件の食い違いについて、いま別作業で対処するか、外部送信入口の再利用前に必ず扱う候補として後回しにするか、追加routeを作らず第3段へ戻るかを判断する。コード、試験、正本はまだ変更しない。

開始条件：

- 再評価Evidenceと独立完了レビューが固定済みである
- 禁止関数を許可関数名として返す反例が機械再現されている
- 外部送信入口、コード、試験、正本を変更しない判断段階である

完了条件：

- 利用者が三つのrouteから一つを選ぶ
- 後回しを選ぶ場合、外部送信入口の再利用前に裁定する条件を維持する
- 本線へ戻る場合、次の意味群候補を一つだけ選び、今回の問題修正を混ぜない

後続作業：利用者のroute判断に従う。候補として後回しの場合は、処理目録一式を現状維持して第3段の次の意味群へ進む。Claude確認は追加せず、第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：技術的blockerはないが、安全条件の食い違いを埋もれさせないためroute判断まで次の整理を開始しない。
- Human判断待ち：いま対処、候補として後回し、本線へ戻るだけの三択。操縦役は候補として後回しを推奨する。

## stale・deferred

- stale：G04役割分類v2の処理目録一式を単純な未使用処理との結合削除候補とする見方、v1のG11三試験を役割終了として削除する案、分類ごとのClaude手動確認、一件ずつの削除は採用しない。
- deferred：処理目録比較と現行`AC-CB-012`の裁定、G11三試験と専用補助処理、他の意味群の実施、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：処理目録の基準再生成試験と、現在の汎用実行器到達禁止試験は独立確認で各一件成功、終了コード0。
- 直近の全Test：本作業は読み取りと記録だけのため再実行しない。直前の整理単位では正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
