# TODO_NEXT_SESSION

更新日：2026-08-12

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段は完了した。第2段は採用表候補を作成したが、公式全試験15件失敗によりテストコード管理が保留となり、段完了前で停止している。
- 現在作業：第2段の公式試験入口を正常化する軽量作業票v1を固定し、危険度highの独立開始前レビューへ渡す。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`：`registered`、影響：公式試験入口を変更する際、合否判定の安全境界を弱めると誤合格の危険がある、次：変更可能pathと既存試験変更の意味を軽量作業票へ固定し、異なる実行単位が開始前に確認する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [第2段採用表候補v1](records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md) — SHA-256 `f8749c543da4753b4e357375241b40b144cbd26edf831437048b2589fa873121`
- [第2段修正後確認v1](records/development/2026-08-12-stage2-minimum-trust-foundation-post-fix-review-v1.md) — SHA-256 `763e09d72dc7f2595b1042e05e204a5242d1392b966302c20f730f88d2213cdd`
- [公式試験入口正常化の軽量作業票v1](docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md) — SHA-256 `5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- [未レビューコード課題の正本](.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json) — SHA-256 `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14`

## 次に行う一作業

作業担当と異なる実行単位が、公式試験入口正常化の軽量作業票v1を変更せずに一回だけ開始前レビューする。

開始条件：

- 軽量作業票v1が基準コミット、固定入力、変更可能path、REDとGREEN、停止条件へ結び付いていること
- 危険度high、既存試験3件の意味変更、版付き設定への項目追加が明示されていること
- 作業票とTODOだけが未コミット差分であり、コード、試験、設定が未変更であること

完了条件：

- 開始前レビューが計画v5第6章の最小項目を持つ一件の記録へ固定されること
- 判定が開始可または修正要で、環境分離、期限付き試験、Python 3.13との分離を根拠付きで示すこと
- 利用者による実装開始判断とその対象が明示されること

後続作業：開始可の場合、利用者が既存試験3件の整理と版付き設定項目追加を含む実装開始を判断する。修正要の場合、作業票を直して一回だけ再確認する。

## blocker・Human判断待ち

- blocker：公式全試験は15件失敗しており、第2段のテストコード管理候補と段完了は保留中。開始前レビュー自体を妨げるものはない。
- Human判断待ち：独立開始前レビュー後に、既存試験3件の整理、設定版2と環境除外項目の追加、RED開始を承認するか判断する。

## stale・deferred

- stale：第2段の採用表候補作成中とする旧TODO表示は、採用表候補と修正後確認の各コミットにより失効した。
- deferred：Python 3.13移行は公式試験入口を現行3.9で正常化した後の別作業とする。重大な欠陥12件の修復、外部送信・認証・応答解析・配置、第3段以降は未開始。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：認証・接続用の6環境変数を当該処理だけから外したexecutor試験は28件成功、終了コード0。期限付き3件の隔離実行は3件失敗、終了コード1。
- 直近の全Test：公式入口は1,736件中1,721件成功、15件失敗、終了コード1。結果記録SHA-256は `cd482d418928f3956f8d70340cc039b3f2c7e4ea8e79d3ee0243ff884600d686`。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
