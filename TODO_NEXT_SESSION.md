# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は401件の候補列挙と最初の一件の予備調査まで進んだが、整理判断の範囲が狭かったため、意味的な全体単位での再評価へ戻る。
- 現在作業：最初の候補を意味的な成果物群として再評価した。実行時間を費用の中心にしたv2を利用者指摘で失効させ、v3では理解負担、過去資料との結合、変更時の調査範囲、部分保証の誤解、増殖の前例を基準に一件削除を推奨した。Codexの変更点確認はverifiedで、Claude確認待ちである。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 401件列挙完了 / 最初の候補群を再評価v3へ修正済み / Claude変更点確認待ち`、影響：試験一件だけの局所判断では、現在保証と履歴資料の役割、保持・削除・修正連鎖・将来調査の総費用を取り落とす、次：Claudeへv3の費用軸、保証の必要性、一件削除推奨、保存済みメモ注記の四変更点だけを手動で確認依頼する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [最初の試験整理候補 保守負債による再評価v3](records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v3.md) — SHA-256 `d7c51c08221825786cc443815f6c7c44cf11797b8a3bd47ef7114a6e92ef7476`
- [重要度に応じた確認方法の運用メモv1](docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md) — SHA-256 `a701fbf8bbd52b24829e80a0372e2e03d4f3013d1e86ef153522203ea3c35819`
- [最初の試験整理候補 v3 Codex変更点確認v1](records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-v3-delta-review-v1.md) — SHA-256 `62196d3b860e7b804af321dfb5a7efe30ce64fd9dc2b10d0aabb4134d0158098`
- [Claude向け最初の試験整理候補 v3変更点確認指示v1](records/session-handoffs/2026-08-13-claude-stage3-first-test-cleanup-lifecycle-v3-delta-review-prompt-v1.md) — SHA-256 `a33fffb13db5d871619c1db21da18b19f63f95d4d231a179fed8c08b1a775020`

## 次に行う一作業

利用者が固定指示をClaudeへ手動で渡し、v3で直した費用の軸、保証の必要性、一件削除推奨、保存済みメモ注記の四点だけを確認して、返答をこの会話へ戻す。試験、対応表、証跡、コード、設定は変更しない。

開始条件：

- 修正版v3、保存済みメモ、Codex変更点確認、Claude用指示の内容識別値が固定済みである
- Claudeにはv1・v2全体の再レビュー、新しい反証、全試験、別候補、追加機構を依頼しない
- 対象試験の削除または維持をClaudeへ裁定させず、利用者判断として残す

完了条件：

- 実行時間を費用の中心にせず、保守負債を中心にしたことが確認される
- 対象試験の部分保証が履歴全体と現在製品保証に不要で、一件削除を推奨できることが確認される
- 止める指摘と報告不一致が示され、file変更、試験削除、外部送信が未実施である

後続作業：二つの変更点確認が揃った後、利用者が推奨案Bの一試験削除を承認するか、維持して別候補へ移るかを判断する。

## blocker・Human判断待ち

- blocker：Claudeのv3変更点確認が未完了。対象試験の削除または維持は未承認である。
- Human判断待ち：Claude確認後に、保守負債を減らす推奨案Bとして対象試験一件を削除するか、維持して別候補へ移るかを判断する。

## stale・deferred

- stale：対象試験を役割終了としたv1の分類、実行時間の小ささを維持費用の中心にしたv2、履歴対応表の現在不一致だけを削除案の停止根拠にする裁定は採否に使わない。
- deferred：401件の残りの内容分類と試験削減、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象試験は三文言改変を検出するが、三文言以外の内容変更では三条件が真のままで、証跡全体を保証しない。Codexのv3変更点確認はverified、止める指摘0件、報告不一致0件。
- 直近の全Test：独立レビューが現在の正規入口で1,739件成功、失敗・除外0、終了コード0を確認した。リポジトリ内の試験は変更していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
