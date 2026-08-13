# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件の候補列挙を終え、一件ずつ削除せず、意味的な群を先に検査してから群ごとに整理する方針へ進んだ。
- 現在作業：利用者は最初の一試験の削除判断を承認したうえで、実施は保留し、401件を先に意味的な群へ分類する順序を採用した。分類の軽量作業票を作成し、低危険度の開始確認へ進む。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 401件列挙完了 / 実施順序採用 / 意味群分類の開始確認待ち`、影響：一件ずつの調査では手続きが増え、一括整理では異なる保証を混ぜるため、全体像を保ちながら意味群ごとに扱う必要がある、次：分類作業票の低危険度開始確認後、401件を読み取りだけで意味群へ分類する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [試験増加候補の機械列挙Evidence v1](records/development/2026-08-13-test-growth-nodeid-enumeration-evidence-v1.md) — SHA-256 `dfa2ebb73a940daa527d3ceac8c502876bf13152bff940a24308411ab2a64f3f`
- [個別401件一覧](records/development/2026-08-13-test-growth-nodeid-candidates-v1.txt) — SHA-256 `11d383f82196e6d964340f83e085d4fd6c7f4e9b1fd3570de8830bafbffbecad`
- [試験整理の実施順序 利用者判断v1](records/development/2026-08-13-stage3-test-cleanup-execution-sequencing-decision-v1.md) — SHA-256 `8d05c2e57dbd03442ad4b2c8f910e4ba63d679631ebc0e98ee7d7d13556946e8`
- [試験整理候補の意味群分類 軽量作業票v1](docs/development/2026-08-13-stage3-test-cleanup-semantic-grouping-bootstrap-work-ticket-v1.md) — SHA-256 `f39e4450d627cb193f156e6f6cfa1d7e225c07ce0de8f36fbb7aeb4b7fff37c3`

## 次に行う一作業

低危険度の開始確認を行い、開始可なら既存一覧、Git履歴、参照検索だけを使って401件を意味的な群へ分類する。試験、製品コード、設定、証跡、対応表は変更しない。

開始条件：

- 作業票の目的、範囲、成果、停止条件が立て直し計画v5の第3段と一致する
- 401件一覧と列挙Evidenceの内容識別値が固定値と一致する
- 分類は読み取りと文書だけで、新しい台帳、検査器、試験を作らない

完了条件：

- 401件を重複なく一度ずつ含むことを機械確認する
- 意味群の境界、危険境界、役割判定に不足する材料を示す
- 最初に詳しく検査する一群だけを提案し、削除・統合は実施しない

後続作業：分類成果を新規サブエージェントと、利用者が手動でClaudeへ渡す変更点確認で独立確認し、その後に最初の実施群を利用者が判断する。

## blocker・Human判断待ち

- blocker：なし。分類作業票の低危険度開始確認前である。
- Human判断待ち：最初の一試験の削除判断と、先に401件を意味群へ分類してから群ごとに実施する順序は承認済み。分類後の最初の実施群は未判断。

## stale・deferred

- stale：一件ずつ同じ深さで調査・削除する進め方、401件を一括精査・一括削除する進め方、ファイル単位の31群をそのまま実施単位とする見方は採用しない。
- deferred：分類後の群ごとの削除・統合、状態固定を宣言ファイルと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象試験は三文言改変を検出するが証跡全体を保証しない。削除判断は承認済みだが、分類が終わるまで実施しない。
- 直近の全Test：直近の独立レビューでは正規入口で1,739件成功、失敗・除外0、終了コード0。今回の判断記録と作業票では試験を変更していない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
