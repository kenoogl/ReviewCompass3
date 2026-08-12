# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段は完了した。第2段『最小信頼基盤を選び、既存資産を評価する』の軽量作業票v1を作成し、開始確認待ちである。
- 現在作業：第2段軽量作業票v1の固定と開始確認。資産評価、正常処理の実行、Python移行は未開始。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：未レビューの守り役コードへ依存する入口を最小信頼基盤として選ぶと、誤合格の危険がある、次：第2段の固定範囲で、選定候補から未修正の重大な欠陥への依存だけを機械確認する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [第1段完了判断v1](records/development/2026-08-12-stage1-current-position-completion-decision-v1.md) — SHA-256 `724c4aa56fedb639e47a2f6b36b7bd1df471f5fc19f8d56d71ef7c6fba940903`
- [第2段軽量作業票v1](docs/development/2026-08-12-stage2-minimum-trust-foundation-bootstrap-work-ticket-v1.md) — SHA-256 `6d9dfeab0fcf4394eef5a73c61171dce935133de7cce4757605eef2e295c621a`
- [未レビューコード課題の正本](.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json) — SHA-256 `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14`

## 次に行う一作業

利用者が第2段軽量作業票v1の四つの前身、四領域の責務、五つの採用条件、評価上限、Python 3.13候補の扱いを確認し、第2段本作業の開始可否を判断する。

開始条件：

- 第2段軽量作業票v1が基準コミットと固定入力の内容識別値へ結び付いてコミット済みであること
- ReviewCompass、ReviewCompass2、LLMGP、現在までのReviewCompass3を四つの前身とする解釈を利用者が確認すること
- 一領域最大4件、全体最大16件の評価上限と、Python移行を別作業にする境界を利用者が確認すること

完了条件：

- 利用者の開始判断が作業票v1とそのSHA-256へ結び付いて記録されること
- 資産評価、コード・試験・設定変更、Python移行を開始判断の記録作業へ混ぜないこと
- 開始判断後の次作業を採用表候補一件の作成へ限定すること

後続作業：承認された作業票の範囲だけで、四領域の採用表候補一件を作成し、意味的に完結したコミットへ固定する。

## blocker・Human判断待ち

- blocker：技術的な妨げはない。第2段の開始には利用者の確認が必要。
- Human判断待ち：第2段軽量作業票v1に基づく本作業の開始可否。

## stale・deferred

- stale：第2段軽量作業票が未作成とする旧TODO表示は、本作業票v1の固定により失効する。
- deferred：未完了の外部送信・認証・応答解析・配置更新は使用停止を維持する。重大な欠陥12件の一括修復、コードと試験の整理、正式な作業契約の導入、第3段以降は未開始。Python 3.13移行は第2段で位置付けを評価するが、移行自体は別作業とする。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：`python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`を単独実行し、終了コード0、`passed`。
- 直近の全Test：文書だけの変更のため実行しない。作業票の構造、参照、内容識別値を機械確認する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
