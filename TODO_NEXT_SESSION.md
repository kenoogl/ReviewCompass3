# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5を採用し、第1段『現在位置と現役経路の確定』の軽量作業票v1をコミットした。利用者による第1段の開始承認も得た。
- 現在作業：第1段作業票は開始承認済み。現在位置・利用経路表の作成は未開始で、次の一作業として実施する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：未レビューの守り役codeを本線へ戻すと誤合格の危険がある、次：第1段の現在位置・利用経路表で現役、使用停止、未確認、履歴のみへ分類する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [立て直し計画v5採用判断](records/development/2026-08-12-project-stall-recovery-plan-v5-adoption-decision-v1.md) — SHA-256 `7f36d7ecbef722fa3c1a82b13c04f6486176de3204cf3a921db3a79643cdf23e`
- [第1段軽量作業票v1](docs/development/2026-08-12-stage1-current-position-bootstrap-work-ticket-v1.md) — SHA-256 `2428853615325add53155f108b608cb81b19ab4bc0bf51ebe9367670379531c0`
- [第1段開始承認判断v1](records/development/2026-08-12-stage1-current-position-bootstrap-start-decision-v1.md) — SHA-256 `55816e66e935f22b6532250a7e59b934fe1bed07f870547c84cde371d8fe0203`
- [未レビューcode backlog Issue正本](.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json) — SHA-256 `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14`

## 次に行う一作業

承認済みの第1段作業票と開始判断の範囲だけで、現在位置・利用経路表一件を作成し、意味的に完結したコミットへ固定する。

開始条件：

- 第1段開始判断が作業票v1とそのSHA-256へ結び付いていること
- 履歴確認の開始コミットと観測対象コミットが存在し、上位計画SHA-256が一致していること
- 作業開始時の作業ツリーがcleanで、予定成果物が未作成であること
- コード、試験、設定、計画、TODO、既存記録の修正、外部送信、第2段以降を対象に含めないこと

完了条件：

- 成果物一件が観測対象コミットと資料の母集合に結び付くこと
- 主要経路の各行が四分類の一つと根拠または未確認理由を持つこと
- 接続方法、入口導線、古い記述または競合、第2段へ渡す未確認範囲を示すこと
- 機械処理のコマンド、終了コード、件数、内容識別値を再確認できること
- 対象外変更がなく、成果物が意味的に完結したコミットへ固定されること

後続作業：作業担当とは異なる実行単位が、成果物を変更せず一回の独立完了レビューを行う。

## blocker・Human判断待ち

- blocker：技術的blockerなし。第1段の開始承認済み。
- Human判断待ち：現在の作業開始についてはなし。成果物の独立完了レビュー後に第1段完了判断を要する。

## stale・deferred

- stale：無工具Claude疎通の範囲固定v3、レビュー依頼v6、失敗する受入試験開始待ちを現在本線とする旧表示はstale。立て直し計画v5が現在の作業順を置き換えた。
- deferred：未完了のClaude実送信・認証・応答解析・配置更新は第1段で分類するまで使用停止。重大欠陥12件の修復、コード・テスト整理、Task Contract導入、第2段以降は未開始。旧ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001も本作業と分けて後回し。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書だけの変更のため新規testなし。開始判断文書の参照とSHA-256、TODOの構造・参照・Evidence Digestを機械照合済み。
- 直近の全Test：文書だけの変更のため実行していない。旧TODOの1559 passedは現在の完了根拠に使わない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
