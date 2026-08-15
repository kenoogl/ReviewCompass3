# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存実装作業票v2の独立訂正確認ではv1の二指摘が解消したが、作成物と後続利用時の権限再確認に止める指摘1件があった。機能範囲と九境界を変えず、作成物の0700／0600相当、所有者、追加ACL、symlink非追跡open後検査を具体的なREDと最終検証へ固定する一点訂正v3を作った。次は同じ独立担当による一点確認である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_reuse_adjudicated_tdd_boundary_one_point_corrected_review_pending`

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
- [安全保存実装作業票v2の独立訂正レビュー](records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v2.md) — SHA-256 `9bcf716d88988e81304849583f42bce1d459f039c14f18154f19e7f59dccdada`
- [作成物の権限確認を一点訂正した安全保存実装作業票v3](docs/development/2026-08-15-session-artifact-safe-storage-implementation-work-ticket-v3.md) — SHA-256 `61deaecb4aec32bd0f16b595c75270d0dec1fbae555f3c99540b3a4455077938`

## 次に行う一作業

安全保存実装作業票v2と一点訂正v3を、同じ独立担当が累積作業票として読み取り専用で再確認し、作成物と後続利用時の権限検査が契約へ一致するか開始可または修正要を返す。

開始条件：

- 作業票v2、一点訂正v3、v2レビュー記録、固定入力のSHA-256がcommitへ固定され、worktreeがcleanである
- これまでを確認した同じ独立担当が、成果物を変更せず一点訂正と全体整合を再確認する
- 製品コード、製品試験、製品設定、配布入口が未変更である
- レビューは上位契約との矛盾、承認欠落、誤った合否、安全境界、範囲違反に限定する

完了条件：

- 作成した記録directoryとfileの0700／0600相当、所有者、種類、追加ACL、open後検査が境界3へ固定されている
- 保存再試行、復旧、再読込み、削除計画、削除が利用時点で同じ安全検査を行い、不合格時に変更しない
- 九境界、契約受入条件1から22、機能範囲、禁止事項に新たな矛盾がない
- 判定が開始可、止める指摘0件である

後続作業：開始可の場合だけ境界1の失敗試験へ進む。修正要が残る場合は製品コードへ進まず、目的、根拠、判断基準、推奨案、影響へ圧縮して利用者へ戻す。

## blocker・Human判断待ち

- blocker：なし。製品試験開始は独立一点確認の開始可まで保留する
- Human判断待ち：なし。内部の開始レビュー担当と完了レビュー担当を使う許可は取得済みで、製品受入判断だけを最終段階で利用者へ戻す

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない
- deferred：独立一点確認が開始可となるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、push、外部送信も開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：実装境界は文書作業であり製品試験は未実施。v2とv3の参照Digest、九境界、受入条件1から22、TODO単一入口を機械確認する
- 直近の全Test：直近の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0。今回の変更では製品コード、試験、設定を変更していない
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
