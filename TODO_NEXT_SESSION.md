# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：最初の整理単位として、G04の履歴固定試験二件と専用定数二件を削除した。独立完了確認は問題なしで、正規全試験1,737件が成功した。次はG04に残る処理目録生成器と固定試験の現在利用を読み取りだけで再評価する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 16意味群分類完了 / 最初の整理単位完了 / 次候補再評価待ち`、影響：作業時点固定の試験を現役集合へ残すと負債が増える一方、現役の利用関係を見落として削除すると現在保証を失う、次：処理目録生成器と固定試験の利用者、役割、回復可能性を再評価する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G04六試験の役割分類Evidence v2](records/development/2026-08-13-stage3-g04-role-classification-evidence-v2.md) — SHA-256 `db16c07912ed13250f17faa017c71538bc277b79b133c3cf6874cd6ae789a834`
- [最初の試験整理 実施承認判断](records/development/2026-08-13-stage3-first-test-cleanup-implementation-approval-decision-v1.md) — SHA-256 `de6e39ebad70ae55dd0693251c57df153226e81cd2dfee7009e24a3c65be8ccd`
- [最初の試験整理 実施Evidence](records/development/2026-08-13-stage3-first-test-cleanup-implementation-evidence-v1.md) — SHA-256 `07a3dc91515fc27445e5180988e64a40bbcf705d86bfeb42c9175dceffebce14`
- [最初の試験整理 独立完了レビュー](records/development/2026-08-13-stage3-first-test-cleanup-independent-completion-review-v1.md) — SHA-256 `1ba8fef13216c5e6ee93dff431f336eda131ef23f6c9929efef3b2e83bd113c2`

## 次に行う一作業

`tools/development/process_call_inventory.py`、その基準資料、`test_process_inventory_baseline_matches_fixed_commit`について、現在の呼出し元、正規入口、履歴上の目的、現在保証、固定commitからの回復可能性を読み取りだけで再評価する。削除・統合は行わない。

開始条件：

- 最初の整理単位の実施Evidenceと独立完了レビューが固定済みである
- 対象を処理目録生成器、基準資料、固定試験と、その実際の利用者に限定する
- 読み取りと記録だけに限定し、コード、試験、設定、履歴資料を変更しない

完了条件：

- 現在の呼出し元と正規入口からの到達可能性を機械列挙する
- 現在保証、履歴資料、両方、役割終了のいずれかへ根拠付きで分類する
- 維持、試験だけ整理、コードと試験を同じ単位で整理という候補を比較し、実施はしない

後続作業：新規サブエージェントが再評価結果を独立確認し、その後に利用者へ維持または整理候補を提示する。低危険度の読み取り確認ではClaudeを追加せず、第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：なし。次候補の読み取り再評価を開始できる。
- Human判断待ち：最初の整理単位は承認・実施・独立確認済み。次候補の削除や製品コード変更は未承認である。

## stale・deferred

- stale：v1のG11三試験を役割終了として削除する案、先行抽出Evidence v2のG11三試験に関する役割終了分類、分類ごとのClaude手動確認、一件ずつの削除は採用しない。
- deferred：G11三試験と専用補助処理、他の意味群の実施、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：独立完了レビューで対象file六件成功、終了コード0。
- 直近の全Test：独立完了レビューで正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。観測commit全体の状態識別値とも一致。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
