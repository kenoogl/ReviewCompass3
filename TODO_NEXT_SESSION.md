# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件の候補列挙を終え、一件ずつ削除せず、意味的な群を先に検査してから群ごとに整理する方針で進めている。
- 現在作業：401件の16意味群分類は独立確認済みとし、低危険度作業ごとのClaude手動確認を停止した。手動確認はまとめた実施計画と第3段完了前の最大2回に限定し、G04六件の役割分類へ進む。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 16意味群分類完了 / 手動確認上限採用 / G04役割分類の開始確認待ち`、影響：一件ずつの調査では手続きが増え、一括整理では異なる保証を混ぜるため、全体像を保ちながら意味群ごとに扱う必要がある、次：G04六件を読み取りだけで四つの役割へ分類し、意味的な実施単位の候補を示す

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [手動の他社モデル確認回数 利用者判断v1](records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md) — SHA-256 `9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`
- [試験整理候補の意味群分類 独立完了レビューv1](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-independent-completion-review-v1.md) — SHA-256 `fe740db405e7bba70feb8dc7fd47673fb679903a40c4682c973a5765fc2df547`
- [試験整理候補の意味群分類Evidence v1](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md) — SHA-256 `cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`
- [G04六試験の役割分類 軽量作業票v1](docs/development/2026-08-13-stage3-g04-role-classification-bootstrap-work-ticket-v1.md) — SHA-256 `51104e11ee44b18d74b89b3ff4cb709fae6a9c1c4ea43bccb29132e883a3046f`

## 次に行う一作業

G04六件について、現在の利用者、検出する欠陥、履歴資料、保証の重複、固定commitからの回復可能性を読み取り、現在の動作保証・履歴資料・両方・役割終了へ分類する。削除や統合は行わない。

開始条件：

- 対象六件が分類EvidenceのG04と一致する
- 作業票、手動確認回数Decision、最初の一件の再評価v3の内容識別値が固定済みである
- 読み取りと文書だけに限定し、試験、製品コード、設定、証跡、対応表を変更しない

完了条件：

- 六件すべてを四分類のいずれかへ根拠付きで分類する
- 現在保証、履歴資料、重複、固有性、回復可能性を区別する
- 同じ実施単位の候補と分離すべき候補を示し、削除・統合は行わない

後続作業：新規サブエージェント一者の独立確認後、他群の同種候補も検査し、複数群をまとめた実施計画を作る。その時点で第3段の一回目の手動Claude確認を行う。

## blocker・Human判断待ち

- blocker：なし。G04六件の読み取り調査を開始できる。
- Human判断待ち：G04六件の役割分類開始は承認済み。手動Claude確認はまとめた実施計画と第3段完了前の最大2回に限定する。

## stale・deferred

- stale：分類ごとのClaude手動確認、一件ずつ同じ深さで調査・削除する進め方、401件の一括精査・一括削除、ファイル単位の31群をそのまま実施単位とする見方は採用しない。
- deferred：G04分類後の削除・統合、他群の役割分類、複数群をまとめた実施計画、状態固定を宣言ファイルと共通検査へ置き換える作業、Work 8の変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G04六件の役割分類では試験を変更しない。承認済み一件の削除は複数群をまとめた実施計画まで実施しない。
- 直近の全Test：直近の独立レビューでは正規入口で1,739件成功、失敗・除外0、終了コード0。今回も読み取りと文書だけのため全試験は実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
