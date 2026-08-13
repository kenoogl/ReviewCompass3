# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：最初の実施計画v1でG11の現役TRACEABILITY参照を見落としたため、G11を変更対象外へ戻したv2を独立確認済みとした。次はv2変更点だけをClaudeへ一回手動確認する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 16意味群分類完了 / 最初の整理計画v2独立確認済み / Claude変更点確認待ち`、影響：作業時点固定の試験を現役集合へ残すと負債が増える一方、現役対応表との接続を見落として削除すると現在保証を失う、次：固定済みプロンプトでv2変更点だけをClaudeが確認し、その結果を利用者が提示する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [手動の他社モデル確認回数 利用者判断v1](records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md) — SHA-256 `9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`
- [最初の試験整理 実施計画v2](docs/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2.md) — SHA-256 `c470da1e4ed3b19c548b64db0d817bdec2d1236b747d3388f50eeccf8c6d1147`
- [実施計画v2 一回限り修正後確認](records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-one-time-correction-review-v1.md) — SHA-256 `0afc66a36878dc431d7a3e9105b82b2e49c7c0886b8129211460d4c73cf09c45`
- [Claude向けv2変更点レビュー指示](records/session-handoffs/2026-08-13-claude-stage3-first-test-cleanup-implementation-plan-v2-delta-review-prompt-v1.md) — SHA-256 `953a92312e97181d90ff150650bc0b09d0a3daf2e974f7d1ebddf8a766957f42`

## 次に行う一作業

利用者が固定済みClaude向け指示をClaudeへ貼り付け、返答全文を本taskへ提示する。実装と削除はまだ行わない。

開始条件：

- v2計画と一回限り修正後確認のSHA-256が固定値と一致する
- Claudeへの指示がv1→v2の変更点だけに限定されている
- 外部送信は利用者が代行し、Codexは送信しない

完了条件：

- Claudeが判定、先行指摘、止める指摘、報告不一致、反証、利用者判断点を返す
- 本質から外れた新機構やG11の再設計を実施条件へ混入させない
- 結果を固定後、利用者がG04二試験と専用定数二件の整理実施を承認または不承認にする

後続作業：Claude結果がverified相当で利用者が明示承認した場合だけ、G04二試験と専用定数二件の削除を一作業単位で実施する。追加Claude確認は行わず、実装後は新規サブエージェントが独立完了レビューする。

## blocker・Human判断待ち

- blocker：外部送信経路をCodexから使用できないため、Claude確認の貼付けと返答回収は利用者の代行が必要。
- Human判断待ち：Claude結果を確認後、案B、未承認の一試験の保証廃止、対象file一件・二試験・専用定数二件という実施範囲を判断する。

## stale・deferred

- stale：v1のG11三試験を役割終了として削除する案、先行抽出Evidence v2のG11三試験に関する役割終了分類、分類ごとのClaude手動確認、一件ずつの削除は採用しない。
- deferred：G11三試験と専用補助処理、未使用の処理目録生成器、他の意味群、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：v2は文書限定のため試験未実行。機械照合では対象file八試験、削除候補二試験、残存予定六試験で一致。
- 直近の全Test：直近の独立レビューでは正規入口で1,739件成功、失敗・除外0、終了コード0。v2確認は文書と読み取りだけのため再実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
