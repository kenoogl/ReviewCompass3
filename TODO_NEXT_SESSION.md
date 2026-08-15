# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存に必要な八つの働きについて、既存処理を条件付きで再利用する2項目、参考だけにする5項目、新規実装する1項目を利用者が承認した。次は、採用済み契約の22受入条件を、一回の失敗確認と最小実装で扱える製品TDD境界へ分ける事前確認である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_reuse_adjudicated_tdd_boundary_precheck_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：安全保存の実装境界確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`
- [立て直し完了後の現在位置訂正判断](records/development/2026-08-15-post-recovery-product-development-position-correction-decision-v1.md) — SHA-256 `5c753f8a155b018452d86ce29d5f37f4ef164e046feac3089f9936295436ef6a`
- [八つの働き正式検索Evidence](records/development/2026-08-15-safe-storage-capability-search-formal-execution-evidence-v1.md) — SHA-256 `d433fcdae6fea26f2fb8f3de703f54db9d7b2905dd4cbd6f2552739d5c645dbc`
- [再利用方法とHuman裁定負荷の承認判断](records/development/2026-08-15-safe-storage-capability-reuse-human-adjudication-decision-v1.md) — SHA-256 `68e9807328b8af3a8443534ab20b8da6d45afd42b03226a2b3964891ca9e1ceb`
- [Python仮想環境入口の不一致訂正Evidence](records/development/2026-08-15-python-venv-entry-correction-evidence-v1.md) — SHA-256 `17cc86a8ebde21a89cbf284b4f09dbbb18f7d261da9cf6b888bdb3f3398f9733`
- [製品TDD実装境界の事前確認方針](records/development/2026-08-15-tdd-implementation-boundary-precheck-policy-decision-v1.md) — SHA-256 `5c844a835b272283eb7ac485e2f5e4be792b7ded6dcf4d600054934a1007edfd`

## 次に行う一作業

採用済み契約の22受入条件と確定した再利用境界を入力に、安全保存機能を一回の失敗確認と最小実装で扱える意味的な製品TDD境界へ分け、実装作業票を作る前提が成立するか事前確認する。

開始条件：

- 契約v3、実装開始判断、八つの再利用方法の利用者承認が同じ対象契約へ結び付いている
- 条件付きで再利用するのは正式入口の安全な結果作成と内容識別値計算に限定し、参考だけの暫定処理を製品の実行時依存へ入れない
- 製品コード、製品試験、製品設定、配布入口を変更せず、まず境界だけを確認する
- 保存、削除、権限、状態遷移、復旧を高危険度として扱う

完了条件：

- 各実装単位に、利用者から見た入力・出力または状態変化と、一つの主要な失敗理由がある
- 各実装単位に、最小実装、先取りしない後続責務、安全上の不変条件、依存順、停止条件、戻せる完了地点がある
- 一つの試験が複数の未実装責務を理由に失敗する境界と、後続で先行試験を書き換える境界を残さない
- 変更候補file、先に失敗させる試験、製品入口へ公開する時点、独立開始前レビューへ渡す固定材料を特定する

後続作業：境界を安全に分けられる場合だけ、小さい実装作業票を固定し、独立開始前レビューで開始可となった後に失敗試験へ進む。分けられない場合は、試験を作る前に設計、Task Contract、実装順序のどれを見直すかを、目的と推奨案まで圧縮して利用者へ戻す。

## blocker・Human判断待ち

- blocker：機械的なblockerはない。次は文書上の製品TDD境界事前確認であり、製品実装は独立開始前レビューの開始可まで行わない
- Human判断待ち：現在はなし。境界を分けられない場合、契約意味または実装順序を変える必要がある場合だけ、目的、根拠、判断基準、推奨案、影響を先に示して最小判断を求める

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない
- deferred：製品TDD境界確認と独立開始前レビューが終わるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、自動commit、push、外部送信も開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：再利用裁定は文書と方針の変更であり製品試験は未実施。TODO更新後に単一入口validatorと参照Digestを確認する
- 直近の全Test：直近の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0。今回の変更では製品コード、試験、設定を変更していない
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
