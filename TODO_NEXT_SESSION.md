# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段は完了した。第2段『最小信頼基盤を選び、既存資産を評価する』は、軽量作業票v1への利用者承認を得て開始可能になった。
- 現在作業：承認済み第2段軽量作業票v1の範囲で、四領域の採用表候補一件を作成する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：未レビューの守り役コードへ依存する入口を最小信頼基盤として選ぶと、誤合格の危険がある、次：選定候補から未修正の重大な欠陥への依存だけを機械確認し、依存する候補を採用候補にしない

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [第1段現在位置・利用経路表v1](records/development/2026-08-12-stage1-current-position-and-active-routes-v1.md) — SHA-256 `8b5668243831a0f4d87783fab1fc540a2c7cf6874826f0032f00df820a5e3efd`
- [第2段軽量作業票v1](docs/development/2026-08-12-stage2-minimum-trust-foundation-bootstrap-work-ticket-v1.md) — SHA-256 `6d9dfeab0fcf4394eef5a73c61171dce935133de7cce4757605eef2e295c621a`
- [第2段開始承認判断v1](records/development/2026-08-12-stage2-minimum-trust-foundation-start-decision-v1.md) — SHA-256 `0fd490a6d303a0a1b7dc49ac8d1e8fc54b4a8a043c9c19ee19965deabe0f121a`
- [未レビューコード課題の正本](.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json) — SHA-256 `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14`

## 次に行う一作業

承認済み作業票の固定範囲だけで、履歴保存、開発コード管理、テストコード管理、レビューの採用表候補一件を作成し、意味的に完結したコミットへ固定する。

開始条件：

- 開始承認判断が作業票v1とそのSHA-256へ結び付いていること
- 基準コミット、固定入力9件、四つの比較元、成果物未作成が一致していること
- コード、試験、設定、Python環境を変更せず、候補全体を16件以内に限定すること

完了条件：

- 四領域すべてに責務、候補、五条件の判定、提案状態、根拠、未確認範囲があること
- 各領域の選定候補について代表正常処理を一例だけ確認すること
- 重大な欠陥への依存とPython 3.13移行候補の位置付けを示すこと
- 対象外変更がなく、成果物一件が意味的に完結したコミットへ固定されること

後続作業：作業担当と異なる実行単位が、成果物を変更せず一回の独立完了レビューを行う。

## blocker・Human判断待ち

- blocker：なし。第2段の開始承認済み。
- Human判断待ち：現在作業の開始についてはなし。独立完了レビュー後に四領域の採否と第2段完了判断が必要。

## stale・deferred

- stale：第2段の開始確認待ちとする旧TODO表示は、開始承認判断v1により失効した。
- deferred：未完了の外部送信・認証・応答解析・配置更新は使用停止を維持する。重大な欠陥12件の一括修復、コードと試験の整理、正式な作業契約の導入、第3段以降は未開始。Python 3.13移行は位置付けだけを評価し、移行自体は別作業とする。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：`python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`を単独実行し、終了コード0、`passed`。
- 直近の全Test：開始判断と引継ぎ文書だけの変更のため実行しない。第2段本作業の代表正常処理として後続で公式全試験を一回実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
