# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G06案Bの整理と独立完了レビューがverifiedで完了した。G06は21件、関連84件、正規全試験は1,728件成功し、list再帰欠陥も置換入力一件が検出した。次は未評価群からG01を再評価するか利用者が判断する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / Work 5B・G06整理verified / 次群選択待ち`、影響：未評価群には現在の安全境界と重複候補が混在し、件数だけで削除可否を決められない、次：G01の19件を、現在利用者、異常例の重複、独自保証、変更・削除の総費用により再評価するかHumanが裁定する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `24e4383cc90962dad3bed8085569db6d342ef68e7cbdf8f837283e3154991b23`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G06整理Evidence](records/development/2026-08-14-stage3-g06-common-guards-cleanup-evidence-v1.md) — SHA-256 `0286819dfbd01aa4fe77d46cf9b74dee1e6fce3c3ebb83e8f19a49d4d3ef5acc`
- [G06整理 独立完了レビュー](records/development/2026-08-14-stage3-g06-common-guards-cleanup-independent-completion-review-v1.md) — SHA-256 `b7bcbdb2bb680e85c94b0d8168f9d06f49322d8351262abc1a73fe0e6ef36a59`
- [第3段 意味群分類Evidence](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md) — SHA-256 `cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`

## 次に行う一作業

利用者が承認した場合、G01「権威参照と内容識別値」19件だけの役割再評価を行う。削除・統合・製品変更は行わず、現在の利用者、同じ欠陥を検出する試験、各異常例の独自性、総費用を調べて三案を比較する。

開始条件：

- G06案Bの独立完了レビューがverifiedで、作業ツリーがcleanである
- 現在の収集でG01が19件であることを再確認する
- 利用者がG01再評価の開始を承認する

完了条件：

- G01の現役利用者と19件の保証対応を機械照合する
- 重要な中心判断へ少なくとも一つの反証を試し、現状維持を含む三案を総費用で比較する
- コード、試験、設定を変更せず、一回の独立完了レビューを行う

後続作業：G01の裁定後、必要なら意味的な実施計画を別作業とし、未評価群へ戻る。Claude手動確認は第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：なし。次群の意味的裁定前なので変更作業は開始しない。
- Human判断待ち：次群としてG01の19件を再評価するか。代替は、近年変更されたG08開発環境9件の再基準化、または高影響のG02不変結果保存11件の再評価。

## stale・deferred

- stale：G06の24件すべてが固有保証を持つという見方と、G06案B実施待ちという状態は解消済み。2026-08-13のG08一件という群件数は後続のPython 3.13移行後の現在集合にはそのまま適用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001、G11三試験と専用補助処理、外部送信を含む高危険度群、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G06 21件と関連84件が成功。list再帰欠陥では置換入力一件だけが失敗し、20件成功・1件失敗。
- 直近の全Test：G06整理後の正規全試験は1,728件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
