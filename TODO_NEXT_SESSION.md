# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件の候補列挙を終え、一件ずつ削除せず、意味的な群を先に検査してから群ごとに整理する方針で進めている。
- 現在作業：401件を16の意味群へ分類し、欠落0件・重複0件を確認した。新規サブエージェントの独立完了レビューはverified、止める指摘0件だった。現在は利用者が手動で受け渡すClaude確認待ちである。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 401件列挙完了 / 16意味群分類完了 / Codex独立確認済み / Claude確認待ち`、影響：一件ずつの調査では手続きが増え、一括整理では異なる保証を混ぜるため、全体像を保ちながら意味群ごとに扱う必要がある、次：利用者が固定指示をClaudeへ手動で渡し、分類の完全性とG04選定の確認結果をこの会話へ戻す

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [試験整理の実施順序 利用者判断v1](records/development/2026-08-13-stage3-test-cleanup-execution-sequencing-decision-v1.md) — SHA-256 `8d05c2e57dbd03442ad4b2c8f910e4ba63d679631ebc0e98ee7d7d13556946e8`
- [試験整理候補の意味群分類 独立完了レビューv1](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-independent-completion-review-v1.md) — SHA-256 `fe740db405e7bba70feb8dc7fd47673fb679903a40c4682c973a5765fc2df547`
- [試験整理候補の意味群分類Evidence v1](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md) — SHA-256 `cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`
- [Claude向け意味群分類完了レビュー指示v1](records/session-handoffs/2026-08-13-claude-stage3-test-cleanup-semantic-grouping-review-prompt-v1.md) — SHA-256 `a0f849949c2cc546d858d048b852e1ffc5ea6c8b07be783705b576c862aef7a2`

## 次に行う一作業

利用者が固定指示をClaudeへ手動で渡し、分類の完全性、群境界、G03とG04の分割、G04選定の確認結果をこの会話へ戻す。試験、製品コード、設定、証跡、対応表は変更しない。

開始条件：

- 新規サブエージェントの独立完了レビューがverified、止める指摘0件、報告不一致0件である
- レビューは分類の完全性、群境界、G03とG04の分割、G04選定だけを対象とする
- 401件の必要性判断、削除案、全試験、新しい仕組みへ範囲を広げない

完了条件：

- Claudeが401件の欠落・重複と16群の境界について独立した反証結果を示す
- G04六件の選定が現在の安全境界を誤って外していないか確認される
- Claudeの判定、止める指摘、報告不一致、未実施事項が揃う

後続作業：Claude確認も合格なら、分類作業を完了とし、G04六件の詳しい役割分類を次の一作業として利用者へ提示する。削除や統合はその後の別判断とする。

## blocker・Human判断待ち

- blocker：Claudeの確認は外部送信経路の問題により利用者の手動受け渡しが必要。新規サブエージェントの確認は完了済み。
- Human判断待ち：最初の一試験の削除判断と、先に意味群分類を行う順序は承認済み。G04六件の詳しい役割分類を始めるかはClaude確認後に判断する。

## stale・deferred

- stale：一件ずつ同じ深さで調査・削除する進め方、401件を一括精査・一括削除する進め方、ファイル単位の31群をそのまま実施単位とする見方は採用しない。
- deferred：G04を含む群ごとの役割分類と削除・統合、状態固定を宣言ファイルと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：401件を16群へ分類したが試験自体は変更していない。承認済み一件の削除は分類レビューが終わるまで実施しない。
- 直近の全Test：直近の独立レビューでは正規入口で1,739件成功、失敗・除外0、終了コード0。今回の分類は読み取りと文書だけのため全試験は再実行していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
