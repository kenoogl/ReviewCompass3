# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は401件の候補列挙と最初の一件の予備調査まで進んだが、整理判断の範囲が狭かったため、意味的な全体単位での再評価へ戻る。
- 現在作業：最初の候補を保守負債で再評価したv3について、Codexと利用者が手動で受け渡したClaudeの変更点確認がともにverifiedとなった。対象試験一件だけの削除を推奨でき、現在は利用者の採否判断待ちである。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 401件列挙完了 / 最初の候補群の再評価・二者確認完了 / Human採否判断待ち`、影響：試験一件だけの局所判断では、現在保証と履歴資料の役割、保持・削除・修正連鎖・将来調査の総費用を取り落とす、次：利用者が推奨案Bの一試験削除を承認するか、維持して別候補へ移るかを判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [最初の試験整理候補 保守負債による再評価v3](records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v3.md) — SHA-256 `d7c51c08221825786cc443815f6c7c44cf11797b8a3bd47ef7114a6e92ef7476`
- [重要度に応じた確認方法の運用メモv1](docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md) — SHA-256 `a701fbf8bbd52b24829e80a0372e2e03d4f3013d1e86ef153522203ea3c35819`
- [最初の試験整理候補 役割・保守負債レビュー完了記録v1](records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-review-completion-v1.md) — SHA-256 `cb0a119e4df2472d0da174ad83fb2faf77c2c5e385235d2304104b38b526e2b2`
- [Claude最初の試験整理候補 v3変更点確認結果v1](records/session-handoffs/2026-08-13-claude-stage3-first-test-cleanup-lifecycle-v3-delta-review-result-v1.md) — SHA-256 `047684783fdcef282d06043c826a88358a0da0f12256f6ee5e79a9a0f3ec541a`

## 次に行う一作業

利用者が、保守負債を減らす推奨案Bとして対象試験一件だけを削除するか、現状を維持して別候補へ移るかを判断する。判断前に試験、対応表、証跡、コード、設定は変更しない。

開始条件：

- 再評価v3、保存済みメモ、CodexとClaudeの変更点確認が固定済みである
- 両確認がverified、止める指摘0件、報告不一致0件である
- 削除対象を一試験だけとし、証跡、対応表、他の七試験、製品code、設定を変更しない境界が明示されている

完了条件：

- 利用者が案Bの採用または不採用を明示する
- 採用時は三文言の部分保証を廃止する意味判断と変更範囲をDecisionへ固定する
- 不採用時は対象試験を維持し、同じ調査を繰り返さず別候補へ移る

後続作業：案B採用なら一試験削除の軽量作業票と開始確認へ進み、不採用なら対象を維持して次の低危険度候補を選ぶ。

## blocker・Human判断待ち

- blocker：なし。実施前の利用者による意味判断待ちである。
- Human判断待ち：推奨案Bとして対象試験一件だけを削除するか、現状を維持して別候補へ移るかを判断する。

## stale・deferred

- stale：対象試験を役割終了としたv1の分類、実行時間の小ささを維持費用の中心にしたv2、履歴対応表の現在不一致だけを削除案の停止根拠にする裁定は採否に使わない。
- deferred：401件の残りの内容分類と試験削減、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象試験は三文言改変を検出するが証跡全体を保証しない。CodexとClaudeのv3変更点確認はともにverified、止める指摘0件、報告不一致0件。
- 直近の全Test：独立レビューが現在の正規入口で1,739件成功、失敗・除外0、終了コード0を確認した。リポジトリ内の試験は変更していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
