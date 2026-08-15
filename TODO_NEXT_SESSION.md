# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存実装作業票v1の独立開始前レビューは修正要だった。機能範囲を変えず、安全な事前拒否、確定保存、同一入力・競合を分け、契約条件5、6、7、9と削除後監査期限を具体的なREDへ固定した九境界のv2へ限定訂正した。次は同じ独立担当による変更点確認である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_reuse_adjudicated_tdd_boundary_corrected_correction_review_pending`

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
- [安全保存実装作業票v1の独立開始前レビュー](records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v1.md) — SHA-256 `b639560e017cc87718e6d1cd9b398c969278d08652ab0ba44a996c1979e473ce`
- [限定訂正した安全保存の製品TDD実装作業票v2](docs/development/2026-08-15-session-artifact-safe-storage-implementation-work-ticket-v2.md) — SHA-256 `96cdfc57006557249143d29c2676f0361e90fec9beb9b3ecf3227b87bb0e0cc0`

## 次に行う一作業

限定訂正した安全保存実装作業票v2を、v1を確認した同じ独立担当が読み取り専用で再確認し、二つの止める指摘が解消し、契約22条件と九境界に新たな止める不整合がないか開始可または修正要を返す。

開始条件：

- 作業票v2、v1レビュー記録、固定入力のSHA-256がcommitへ固定され、worktreeがcleanである
- v1を確認した独立担当が、成果物を変更せず変更点と全体整合を再確認する
- 製品コード、製品試験、製品設定、配布入口が未変更である
- レビューは上位契約との矛盾、承認欠落、誤った合否、安全境界、範囲違反に限定する

完了条件：

- 安全な事前拒否、確定保存、同一入力・競合が別のRED理由と最小実装になっている
- 条件5、6、7、9と削除後監査期限が具体的なRED、観測対象、最小実装、不変条件へ接続されている
- 契約受入条件1から22の未接続0、九境界の必須欄欠落0である
- 判定が開始可、止める指摘0件である

後続作業：開始可の場合だけ境界1の失敗試験へ進む。修正要が残る場合は製品コードへ進まず、目的、根拠、判断基準、推奨案、影響へ圧縮して利用者へ戻す。

## blocker・Human判断待ち

- blocker：なし。製品試験開始は独立訂正確認の開始可まで保留する
- Human判断待ち：なし。内部の開始レビュー担当と完了レビュー担当を使う許可は取得済みで、製品受入判断だけを最終段階で利用者へ戻す

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない
- deferred：独立訂正確認が開始可となるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、push、外部送信も開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：実装境界は文書作業であり製品試験は未実施。九境界の必須欄、受入条件1から22の欠落0、参照Digest、TODO単一入口を機械確認する
- 直近の全Test：直近の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0。今回の変更では製品コード、試験、設定を変更していない
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
