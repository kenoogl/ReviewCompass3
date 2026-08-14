# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、群単位の整理と、第3段中に増えた成果物の段完了前整理を継続する。
- 現在作業：G01の実装と独立完了判断はverifiedのまま維持する。ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001の状態反映とissue_resolution_v4.pyの正式利用化は利用者判断により中止し、第3段の成果物整理方針へ戻った。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段整理を継続`、影響：第3段の残る意味群と、第3段中に追加・変更した成果物の全体整理が未完了である、次：第3段開始commitと、段内追加成果物を列挙する範囲を固定する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `5e0ab06b682939ab0c6e5804db02ee31952059a4404b8a21fe38ef07532514b3`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [第3段成果物整理の追補判断](records/development/2026-08-14-recovery-plan-v5-stage3-created-artifact-completion-condition-amendment-decision-v1.md) — SHA-256 `181c74b9b325df9544ce195e3344aee60d0090cce61ab4f136f5d8c1f9da00db`
- [Issue解決処理の使用停止と状態反映中止判断](records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-decision-v1.md) — SHA-256 `c20ee11c368145cab3103a802af2f5aa6f64649202b684976f535c6d97a640b1`
- [Issue解決処理の成熟度限定訂正レビュー](records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-correction-review-v1.md) — SHA-256 `7e69b63f1dc34b9920b92acb4a388f6610319670f08550e0aa6cc7870d854470`
- [G01現役接続 独立完了レビュー](records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md) — SHA-256 `c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`

## 次に行う一作業

第3段の方針修正へ戻り、第3段開始時点から段完了候補までに追加・変更したコード、試験、文書を全体列挙する作業の範囲を、軽量作業票へ固定する。まだ列挙結果の採否、削除、統合、コード・試験・設定の変更は行わない。

開始条件：

- Issue解決処理の使用停止と状態反映中止判断が固定され、対象Issueがregistered、対象処理が暫定のままである
- 立て直し計画v5と第3段成果物整理の追補判断の内容識別値が一致する
- 第3段開始commitを件数から推測せず、既存Decision、Evidence、Git履歴から確定する

完了条件：

- 第3段開始commit、観測commit、対象種別、除外範囲、列挙方法、四分類、停止条件を作業票へ固定する
- 新しい台帳、検査器、試験、関門を追加せず、重要度別に確認の深さを変える方針を維持する
- コード、試験、設定、Issue、第4段資料を変更せず、新規サブエージェントの独立開始前レビューを行う

後続作業：開始可の確認後、Git差分から成果物を機械列挙し、意味群ごとの整理候補を利用者判断へ渡す。

## blocker・Human判断待ち

- blocker：なし。Issue状態反映の枝は中止判断により閉じ、第3段の文書・読み取り作業へ戻れる。
- Human判断待ち：なし。次のHuman判断は、第3段成果物の意味群と整理候補を作成した後に行う。

## stale・deferred

- stale：Issue状態反映判断待ち、issue_resolution_v4.pyの正式利用化候補、修正案C実施待ちは利用者の中止判断により失効した。G01を未完了または暫定とする見方も失効したままである。
- deferred：ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001はregisteredのまま維持し、issue_resolution_v4.pyは暫定・使用停止とする。第3段の残る意味群、G11三試験と専用補助処理、外部送信を含む高危険度群、Work 8の全体変異検査は後続へ残す。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Issue解決処理の成熟度精査で対象24件と関連67件が成功したが、親フォルダ作成失敗時の片残り欠陥を独立再現した。G01の19件成功は変更していない。
- 直近の全Test：G01現役接続後の正規全試験は独立再実行で1,728件成功、失敗・エラー・除外0、終了コード0。本中止判断ではコード・試験・設定を変更しないため再実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
