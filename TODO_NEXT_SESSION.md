# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は試験数削減を目的とせず、観測commitの現役全試験から現行正本との矛盾候補だけを機械抽出し、候補だけを人が確認する方針へ修正した。
- 現在作業：第3段の方針文書について、独立レビューが指摘した候補条件一件を限定修正中。過去の401件列挙、16意味群、独立確認済みの修正・削除は履歴として維持し、残る群ごとの詳細整理は今後の通常経路にしない。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 中心問題は維持 / 将来手順を限定`、影響：状態固定試験が正当な変更を妨げた実害は残るが、全試験への一律の詳細確認、宣言file、共通検査、変異検査は行わない、次：観測commit、現行正本、全試験集合、機械抽出規則を軽量作業票へ固定する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c150187e7e79ddd955942bba5c4a775dbda64537f31931bd048604ab5cb082ad`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc`
- [重要度別確認メモ](docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md) — SHA-256 `1090ea3083574c6dfb9cf0345505c070240cfd2e81b87929f6f7c2a50c0c2591`
- [第3段試験整合方針の修正判断](records/development/2026-08-14-recovery-plan-v5-stage3-test-authority-consistency-amendment-decision-v1.md) — SHA-256 `83efdd438abbb3a34df1ebafd24c7891f8ae3d265634c8ef54bd817951c2d21c`
- [Issue解決処理の使用停止と状態反映中止判断](records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-decision-v1.md) — SHA-256 `c20ee11c368145cab3103a802af2f5aa6f64649202b684976f535c6d97a640b1`
- [G01現役接続 独立完了レビュー](records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md) — SHA-256 `c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`

## 次に行う一作業

第3段の矛盾候補抽出について、観測commit、正規入口で収集する全試験集合、現行正本の範囲、固定した現行正本に含まれない資料を含む直接参照の機械抽出方法、停止条件を軽量作業票へ固定する。まだ候補抽出、試験の意味確認、修正、削除、使用停止は行わない。

開始条件：

- 第3段試験整合方針の修正が独立完了レビューでverifiedである
- 観測commitの正規入口から現役の全試験を重複なく収集できる
- 暫定資料と履歴資料を現在の合否基準から除外し、採用済みの要求、設計判断、開発方針を確認基準として列挙できる

完了条件：

- 観測commit、全試験集合、確認基準、現行正本に含まれない直接参照を含む機械抽出対象、候補判定、停止条件が作業票に固定されている
- 全試験を一件ずつ人が詳しく確認せず、抽出候補だけを人が確認する境界が明記されている
- 試験数、実行時間、来歴、重複して見えることを単独の整理理由にせず、コード、試験、設定を変更していない

後続作業：開始確認後、全試験から矛盾候補を機械抽出し、候補だけの意味確認結果を利用者判断へ渡す。

## blocker・Human判断待ち

- blocker：独立レビュー指摘一件の限定修正後確認が未完了である。旧TODOの群単位整理と段内全成果物整理には戻らない。
- Human判断待ち：なし。利用者は本方針と必要文書の修正を承認済みである。次の意味判断は矛盾候補の確認後に行う。

## stale・deferred

- stale：401件の残りを16意味群ごとに詳しく調べて整理する将来手順と、試験数または短い実行時間の削減を第3段の目的にする見方は、本方針判断で失効した。Issue解決処理の正式利用化と状態反映も中止済みである。
- deferred：ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001はregistered、issue_resolution_v4.pyは暫定・使用停止のまま維持する。Work 8の評価は第3段の全試験詳細確認とは分離し、必要時に別目的で判断する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書導線に関係する27件が成功した。現役方針参照8件、TODO参照6件、内容識別値、TODOの再生成一致を確認した。
- 直近の全Test：観測commitの正規収集は1,728件、重複による収集エラー0、終了コード0。直近の正規全試験は1,728件成功であり、本変更ではコード、試験、設定を変更しないため再実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
