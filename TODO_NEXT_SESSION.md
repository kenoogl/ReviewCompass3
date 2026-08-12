# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段『現在位置と現役経路の確定』は、成果物の独立完了レビュー合格と利用者の完了判断により完了した。第2段は未開始である。
- 現在作業：第1段の完了反映。次の一作業は、第2段の軽量作業票を一件作成して開始確認へ提示すること。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：未レビューの守り役コードへ依存する入口を最小信頼基盤として選ぶと、誤合格の危険がある、次：第2段で、選ぶ入口が未レビュー範囲へ依存するかを評価し、採用、使用停止または保留を判断できる形にする

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [第1段現在位置・利用経路表v1](records/development/2026-08-12-stage1-current-position-and-active-routes-v1.md) — SHA-256 `8b5668243831a0f4d87783fab1fc540a2c7cf6874826f0032f00df820a5e3efd`
- [第1段独立完了レビューv1](records/development/2026-08-12-stage1-current-position-bootstrap-completion-review-v1.md) — SHA-256 `f005a98c1da91f100e4f068ab89c24cf38f7f9b3637862df1c278b3a67265508`
- [第1段完了判断v1](records/development/2026-08-12-stage1-current-position-completion-decision-v1.md) — SHA-256 `724c4aa56fedb639e47a2f6b36b7bd1df471f5fc19f8d56d71ef7c6fba940903`
- [未レビューコード課題の正本](.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json) — SHA-256 `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14`

## 次に行う一作業

第2段『最小信頼基盤を選び、既存資産を評価する』の軽量作業票を一件作成し、開始確認へ提示する。Python 3.13への移行は、公式な開発・試験基盤への影響を評価する独立候補として作業票に位置付ける。

開始条件：

- 第1段完了判断が成果物と独立完了レビューの内容識別値へ結び付いていること
- 第1段成果物の四分類と未確認範囲を変更せず、第2段の入力として固定すること
- 第2段の作業、コード修正、試験整理、Python移行をまだ開始しないこと

完了条件：

- 四領域の責務、採用条件、非採用条件、評価上限、対象外を示すこと
- 目的、入力と根拠、範囲、成果、機械確認、レビュー事項、停止条件と完了条件の七項目を満たすこと
- 基準コミット、危険度案、作業担当、独立完了レビュー担当を固定すること
- 作業票を意味的に完結したコミットへ固定し、第2段の開始は利用者の確認待ちにすること

後続作業：利用者が第2段作業票の対象、採用条件、非採用条件、評価上限を確認し、開始可否を判断する。

## blocker・Human判断待ち

- blocker：なし。第1段は完了している。
- Human判断待ち：第2段の軽量作業票を提示した後に、作業開始の確認が必要。

## stale・deferred

- stale：第1段の現在位置・利用経路表が未作成で、完了判断待ちとする旧TODO表示は、成果物、独立完了レビュー、完了判断により失効した。
- deferred：未完了の外部送信・認証・応答解析・配置更新は引き続き使用停止。重大な欠陥12件の一括修復、コードと試験の整理、正式な作業契約の導入、第3段以降は未開始。Python 3.13移行は第2段で評価する独立候補であり、まだ実施しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書だけの変更。TODO引継ぎの単一検証入口を、最終追加前に単独実行する。
- 直近の全Test：文書だけの変更のため実行しない。第1段独立完了レビューの合格を段完了根拠とする。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
