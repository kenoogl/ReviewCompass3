# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は試験数削減を目的とせず、観測commitの現役全試験から現行正本との矛盾候補だけを機械抽出し、候補だけを人が確認する方針で進める。
- 現在作業：全1,728件を人が詳しく調べないための軽量作業票v2が、一回限りの変更点レビューでverifiedとなった。直接参照から該当する利用者判断だけを完全一致で逆引きし、曖昧な場合は停止する範囲が確定した。候補抽出そのものは未実施である。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 中心問題は維持 / 将来手順を限定`、影響：状態固定試験が正当な変更を妨げた実害は残るが、全試験への一律の詳細確認、試験数削減、宣言file、共通検査、変異検査は行わない、次：作業票v2に従い、現役全試験から現行正本との矛盾候補だけを読み取りで機械抽出する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c150187e7e79ddd955942bba5c4a775dbda64537f31931bd048604ab5cb082ad`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc`
- [第3段試験整合方針の修正判断](records/development/2026-08-14-recovery-plan-v5-stage3-test-authority-consistency-amendment-decision-v1.md) — SHA-256 `83efdd438abbb3a34df1ebafd24c7891f8ae3d265634c8ef54bd817951c2d21c`
- [矛盾候補抽出の軽量作業票v2](docs/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-bootstrap-work-ticket-v2.md) — SHA-256 `79167fa82d194b9a85e5ae8762d8ef0fc394b271e52f95de2dc38f39ff8075b0`
- [作業票v2の一回限り変更点レビュー](records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-scope-one-time-review-v1.md) — SHA-256 `cdc8e46733eac0b9cd584bcaea46490f7a48a4566e5aab6552ada5d34958ba69`
- [試験増加状態固定Issue](.reviewcompass/workflow/issues-v4/issue-test-growth-state-pinning-001--v1.json) — SHA-256 `13f4c9a68d90105e66f3e3b5fb2df36b334f7921ee69430b82e85cf40b6f8194`

## 次に行う一作業

作業票v2に従い、観測commitの現役全試験から、現在有効な要求・採用済み設計判断・開発方針との矛盾候補だけを機械抽出し、Evidence一件へ固定する。全試験や全Decisionを人が総点検せず、試験の修正・削除・使用停止は行わない。

開始条件：

- 作業票v2が一回限りの変更点レビューでverifiedである
- 観測commitの正規入口から1,728件、重複0件、固定した内容識別値の試験集合を再現できる
- 各直接参照pathまたはIDから、完全一致するDecision記録だけを限定逆引きできる

完了条件：

- 再現方法、入力commit、全試験集合の件数・重複・内容識別値、抽出条件、候補一覧、限界をEvidence一件に固定している
- 候補だけを人の確認対象とし、候補でない試験の個別台帳、要求対応、役割分類を作っていない
- コード、試験、設定、Issue、既存Decision・Evidenceを変更せず、新しい恒久機構、検査器、試験、関門を作っていない

後続作業：独立完了レビュー後、抽出候補だけの意味確認結果を利用者判断へ渡す。矛盾が実証されない試験は現状維持とする。

## blocker・Human判断待ち

- blocker：なし。作業票v2は独立確認でverifiedとなり、候補抽出へ進める。逆引き結果や正本関係を一意に決められない場合は作業票の停止条件に従う。
- Human判断待ち：なし。次の意味判断は、機械抽出した候補の確認後に行う。

## stale・deferred

- stale：401件の残りを16意味群ごとに詳しく調べる将来手順と、試験数または短い実行時間の削減を第3段の目的にする見方は失効した。作業票v1の逆引き不足もv2で訂正済みである。
- deferred：ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001はregistered、issue_resolution_v4.pyは暫定・使用停止のまま維持する。Work 8の評価は第3段の全試験詳細確認とは分離し、必要時に別目的で判断する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：観測commitの正規収集で1,728件、node ID重複0件、内容識別値一致を確認した。独立レビューは先行反例の直接参照から後続Decision一件だけへ到達する限定逆引きを再現した。
- 直近の全Test：直近の正規全試験は1,728件成功である。本作業票とレビューは文書だけを変更したため、全試験は再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
