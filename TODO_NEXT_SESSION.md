# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理し、第3段中に増えた成果物も段完了前の整理対象としている。
- 現在作業：G01の再評価、案Cの現役接続、独立完了レビューがverifiedで完了した。実文書2件・11参照を正規全試験へ接続し、重複2入力を不足2境界へ入れ替えた。対象19件と正規全試験1,728件は成功した。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / 実装と独立完了レビューverified / 状態反映判断待ち`、影響：検査コードは現役化済みだが、正式Issueの台帳状態がregisteredのままで実態と一致していない、次：利用者がresolvedへの反映を承認した場合、Human裁定記録を作成し、既存の正規Issue解決処理だけで状態と解決記録を更新する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `24e4383cc90962dad3bed8085569db6d342ef68e7cbdf8f837283e3154991b23`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G01現役接続Evidence](records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-evidence-v1.md) — SHA-256 `52022b04a72b1c5df458f949f80bde1383ef4238f8d6b6b024977eac6ad398cd`
- [G01現役接続 独立完了レビュー](records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md) — SHA-256 `c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`
- [第3段成果物整理の追補判断](records/development/2026-08-14-recovery-plan-v5-stage3-created-artifact-completion-condition-amendment-decision-v1.md) — SHA-256 `181c74b9b325df9544ce195e3344aee60d0090cce61ab4f136f5d8c1f9da00db`

## 次に行う一作業

利用者が承認した場合、ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001をresolvedへ反映する一作業を行う。Human裁定記録を固定し、既存の正規Issue解決処理でIssueのstateとcontent_digestだけを更新し、新規の解決記録を作る。コード、試験、設定は変更しない。

開始条件：

- G01現役接続の独立完了レビューがverifiedである
- 正式Issueがregisteredの版1であることを再確認する
- 利用者がresolvedへの状態反映を承認する

完了条件：

- Human裁定記録が対象Issue、resolved、利用者文言、Evidenceへ機械的に結び付く
- 正規Issue解決処理が台帳検証に合格し、stateとcontent_digest以外の既存Issue項目を変えない
- 解決記録、TODO、作業単位遷移を確認し、コード・試験・設定を変更しない

後続作業：Issue反映後、第3段の未評価意味群へ戻る。第3段完了前には、段開始から増えた成果物の全体列挙とClaude手動確認一回を行う。

## blocker・Human判断待ち

- blocker：なし。G01のコード作業は完了している。
- Human判断待ち：ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001をresolvedへ反映してよいか。

## stale・deferred

- stale：G01を未接続の暫定検査とする見方、G01再評価待ち、案C実施待ちという状態は解消済み。
- deferred：ISSUE-TEST-GROWTH-STATE-PINNING-001の残る意味群、IC-PROCESS-INVENTORY-SAFETY-CLAIM-001、G11三試験と専用補助処理、外部送信を含む高危険度群、Work 8の全体変異検査、第3段中に増えた全成果物の段完了前列挙。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G01は19件成功。実文書2件・11参照が一致。実文書ずれ、同居値拒否、空文書混在、NUL文字の4欠陥を既存試験が検出した。
- 直近の全Test：G01現役接続後の正規全試験は独立再実行でも1,728件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
