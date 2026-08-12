# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段は完了した。第2段は公式全試験15件失敗により停止しており、その原因を分離して公式試験入口を正常化する作業が開始承認済みである。
- 現在作業：承認済み軽量作業票v1に従い、試験3 fileだけで環境分離のREDを固定し、期限付き3件を恒久検査から分離する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：公式試験入口の合否判定を変更するため、試験を弱めると誤合格の危険がある、次：承認済みの試験3 fileだけで修正前後を区別するREDを固定し、GREEN中は変更しない

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [第2段採用表候補v1](records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md) — SHA-256 `f8749c543da4753b4e357375241b40b144cbd26edf831437048b2589fa873121`
- [公式試験入口正常化の軽量作業票v1](docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md) — SHA-256 `5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- [独立開始前レビューv1](records/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-start-review-v1.md) — SHA-256 `5dc23327f1072fd5438ca8ff2e2c22634f4257dd8970426471f69696be3a80ad`
- [開始判断v1](records/development/2026-08-12-stage2-official-test-entry-restoration-start-decision-v1.md) — SHA-256 `d1477c89f14cc05674ac9787fe887e544e638f4d9449431c1ffbe4a536c274c6`

## 次に行う一作業

試験3 fileだけを変更し、公式試験入口が認証・接続用の6変数を子処理へ渡す現行動作を新しい試験で失敗させ、期限付き3件を恒久検査から分離する。

開始条件：

- 開始判断v1が作業票、独立開始前レビュー、利用者承認へ結び付いていること
- 試験3 file以外に未コミット差分がなく、設定と実装が未変更であること
- 新しい試験が6名の除外、無害な環境の維持、親処理の不変を検査すること

完了条件：

- 新しい環境分離試験だけが修正前実装を理由に失敗し、同じfileの他試験が成功すること
- 期限付き3件の削除または縮小後も、固定基準再生成、egress 6 file、使い捨てGitの禁止path検出が残ること
- 試験3 fileだけが意味的に完結したRED commitへ固定されること

後続作業：RED commit後、版付き設定と公式試験入口を実装し、RED試験を変更せず関連試験と公式全試験を正常終了させる。

## blocker・Human判断待ち

- blocker：なし。独立開始前レビューは開始可で、利用者が固定範囲の実装開始を承認済み。
- Human判断待ち：現在作業の開始についてはなし。独立完了レビュー後に、テストコード管理候補の採用と第2段へ戻る判断が必要。

## stale・deferred

- stale：独立開始前レビュー待ちとする旧TODO表示は、開始前レビューと開始判断v1により失効した。
- deferred：Python 3.13移行、第2段採用表の更新、重大な欠陥12件の修復、外部送信・認証・応答解析・配置、第3段以降は未開始。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：6変数を当該処理だけから外したexecutor試験は28件成功。期限付き3件は同じ隔離状態でも3件失敗し、残す恒久検査3件は成功。
- 直近の全Test：公式入口は1,736件中1,721件成功、15件失敗、終了コード1。GREENで同じ正規入口を再実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
