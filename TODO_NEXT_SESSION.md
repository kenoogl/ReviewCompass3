# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：Work 5B契約試験file一件・六試験を現役集合から外し、独立完了レビューはverifiedだった。全試験は1,731件成功し、契約v1・v2と過去資料は無変更である。次は承認済みG06案Bを実施する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / Work 5B整理verified / G06案B実施待ち`、影響：G06の現行24件にはlist内の不正値を見逃す入力と、固有保証のない衝突確認二件・不安定な実在記録走査一件が混在する、次：承認済みG06案Bとして既存入力一件を置換し、役割終了三件を試験file一件から整理する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [Work 5B試験整理Evidence](records/development/2026-08-14-work5b-contract-test-cleanup-evidence-v1.md) — SHA-256 `a1b5c61528ffe8aab9f3b2180bc28ba0a43cc11f1c4ddb41863f526e796a94ac`
- [Work 5B試験整理 独立完了レビュー](records/development/2026-08-14-work5b-contract-test-cleanup-independent-completion-review-v1.md) — SHA-256 `dd2d72331e9ffdc92fec9242d507d3451456f1d7df25d9d2451ba54c9a94d17d`
- [G06再評価 限定修正後確認](records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md) — SHA-256 `e0613030767c04d38014e9842388c2b302cc071f0a1c5b463bb3914bf6d7d36a`

## 次に行う一作業

G06案Bを実施する。tests/test_common_digests.pyの入れ子tuple入力一件をlist内tupleへ置換し、固有保証のない衝突確認二件と、名前順先頭200件だけを走査する実在記録試験一件を削除する。経路五件、閉じたJSON入力、Task Contract三境界は維持する。

開始条件：

- G06再評価の限定修正後確認がverifiedである
- 案B模擬でG06 21件・関連84件が成功し、list再帰欠陥で置換一件が失敗済みである
- 利用者が案Bを承認済みで、Work 5B整理がverifiedで完了している

完了条件：

- 変更範囲をtests/test_common_digests.py一件と実施Evidenceに限定する
- G06 21件、関連84件、list再帰の欠陥投入、正規全試験が成功する
- 新しい試験、検査器、台帳を追加せず、一回の独立完了レビューを行う

後続作業：G06案Bの独立完了レビュー後、第3段の次の意味群へ戻る。Claude手動確認は第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：なし。意味変更は利用者承認済みで、模擬と独立再評価も完了している。
- Human判断待ち：なし。案Bの実施は承認済み。新しい範囲変更または段完了が生じた場合だけ再度求める。

## stale・deferred

- stale：Work 5B契約試験六件を現役保証とする見方、G06の24件すべてが固有保証を持つという見方、先頭200件の走査を全記録整合の保証とする見方は採用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001、G11三試験と専用補助処理、他の未評価意味群、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 5B整理後の直接試験22件成功。G06案Bの事前模擬は21件・関連84件成功、list再帰欠陥で置換一件失敗。
- 直近の全Test：Work 5B整理後の正規全試験は1,731件成功、失敗・エラー・除外0。G06案B実施後は三件減の1,728件を期待する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
