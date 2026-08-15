# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存の境界8は、確認済みの一記録だけを順序削除し、四つの停止点から同じ確認値で再試行し、削除後監査を元の保持期限まで残すGREENとなった。専用55件、既存入口関連21件が成功した。次は境界9の四操作製品入口と配布用実行名を進める。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_reuse_adjudicated_tdd_boundaries_1_8_green_boundary_9_pending`

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
- [作成物の権限確認を一点訂正した安全保存実装作業票v3](docs/development/2026-08-15-session-artifact-safe-storage-implementation-work-ticket-v3.md) — SHA-256 `61deaecb4aec32bd0f16b595c75270d0dec1fbae555f3c99540b3a4455077938`
- [安全保存実装の独立開始前レビュー開始可](records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v3.md) — SHA-256 `f04b91fc28710cd8bc52b4a325febb14a087a1659484d510db12f01e2b4e60b7`
- [安全保存境界1のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-1-tdd-evidence-v1.md) — SHA-256 `2811b864c5e494800ce4364bac0d601cc4073e06ffffd6d096fef5b1f22e3051`
- [安全保存境界2のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-2-tdd-evidence-v1.md) — SHA-256 `aa6fabd0c0c7fe7856edfc317900e8f052cd648aa5f579b918d37b553c629189`
- [安全保存境界3のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-3-tdd-evidence-v1.md) — SHA-256 `58181132c2e905820d390b207155cc9a6b1d6dd89cc0f69c39470756bffa8b6b`
- [安全保存境界4のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-4-tdd-evidence-v1.md) — SHA-256 `c76bdd396126a87d7aa6495897436d1653bee56c46291df488ab6348a264317a`
- [安全保存境界5のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-5-tdd-evidence-v1.md) — SHA-256 `a45d24696a719318f6f96faf1b59ec4360a00fe8eb285824e0fe0a02022b717c`
- [安全保存境界6のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-6-tdd-evidence-v1.md) — SHA-256 `ff26865fcc29c87d93c3caf2e2f75e50eb7af6dccdfb0d4aff6d3fbf1d2dd37a`
- [安全保存境界7のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-7-tdd-evidence-v1.md) — SHA-256 `080989ebb3218d17bb96051e67b835972d85df4073a318ba78075940952f7ebc`
- [安全保存境界8のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-8-tdd-evidence-v1.md) — SHA-256 `ba01f116de413c5627a2965bb309a2dfc6286a9906ceeb59df672d0c4ddb8d0f`

## 次に行う一作業

境界9の試験として、store、load-derived、plan-delete、deleteの四操作を一つの製品入口から呼び、成功・停止を秘密とpathのないJSON一件と終了区分で返すことを要求する。

開始条件：

- 境界8のGREEN、Evidence、TODOが意味単位commitへ固定され、worktreeがcleanである
- 累積作業票v2＋v3の境界9と契約受入条件2、5から8、19、20を固定入力にする
- repository外の合成rootだけを用い、実Session記録と実保存rootを使わない
- 既存正式入口の出力bytesと終了区分を変更しない

完了条件：

- 製品入口と配布用実行名の不在を主要理由にREDになる
- 四操作が引数値だけを保存核へ渡し、一回だけJSONを出力する
- 全出力にraw本文、source_path、入力path、root、home、利用者名、host名、例外本文、秘密値がない
- 境界9のGREEN commit後に対象・関連・正規全試験と作業単位遷移が合格する

後続作業：境界9を意味単位commitで閉じた後、最終検証と独立完了レビューを行う。技術条件が合格した場合だけ製品受入候補を利用者へ提示する。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。内部の開始レビュー担当と完了レビュー担当を使う許可は取得済みで、製品受入判断だけを最終段階で利用者へ戻す

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない
- deferred：境界9では探索、複数処理、環境値解決、network、外部process、Git、自動削除を入口へ追加しない。中央一覧、push、外部送信も開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：境界8は新規8件、専用55件、既存入口関連21件が終了コード0。次は境界9の製品入口試験を追加する
- 直近の全Test：直近の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0。境界9後に正規全試験を再実行する
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
