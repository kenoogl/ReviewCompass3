# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段と、最初の製品機能G25読取り専用入口は完了した。現在は立て直し後の二つ目の製品機能である安全保存の実装準備を進めている。
- 現在作業：安全保存の独立完了再レビューv2が残した2原因はREDを変えずGREENとなった。対象97件、関連30件、正規全1,862件が成功した。次は同じ独立担当による完了再々レビューを行う。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_rereview_v2_two_causes_remediated_final_verification_v3_passed_rereview_pending`

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
- [安全保存境界9のRED・GREEN Evidence](records/development/2026-08-15-session-artifact-safe-storage-boundary-9-tdd-evidence-v1.md) — SHA-256 `9f04021540534f327f7bbfeb80012d3ee3f54575222311111b15f10264adc47e`
- [安全保存の最終技術検証Evidence](records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v1.md) — SHA-256 `b43a1d7256985a7ab606219cf7cbbe19271edca4b1f2d657ce21e9429c59de14`
- [安全保存の独立完了レビュー修正要](records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v1.md) — SHA-256 `083ebadd2cc20e8006d2998c2cd71a812d52c59fea3f1838cb8d276980b4dc76`
- [安全保存の四原因修正後最終技術検証Evidence v2](records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v2.md) — SHA-256 `dc84ab5915b636f8d7595bc3652dcedbc288f9aba26f57b245ce9817e967fc4d`
- [安全保存の独立完了再レビューv2修正要](records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v2.md) — SHA-256 `d90364a873586b1be8ccf37196c2f49c5d879d87446379a54fc7194d85b77c88`
- [安全保存の二原因修正後最終技術検証Evidence v3](records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v3.md) — SHA-256 `fc2d86c305b4198b774b57e550205732b599c4f4c753f8db89c52b19175facbd`

## 次に行う一作業

独立完了再レビューv2と最終技術検証Evidence v3を固定入力にし、同じ独立担当が残る2指摘、条件1から21、変更範囲をread-onlyで再々反証する。

開始条件：

- 二修正commit、Evidence v3、TODOが意味単位commitへ固定され、worktreeがcleanである
- 採用契約v3、独立完了再レビューv2、Evidence v3を固定入力にする
- レビューはread-onlyで前回反例を同条件で再実行する
- 全Python commandに.venv/bin/python3を使う

完了条件：

- 前回2指摘の反例が期待する安全結果へ変わる
- 契約受入条件1から21の未接続が0件になる
- 新たな責務拡張、秘密出力、既存入口変更、外部能力追加がない
- 止める指摘0件の開始可、または残る修正要がpathと反例付きで固定される

後続作業：独立再々レビューが開始可なら、条件22として目的・根拠・合否基準・推奨・影響を利用者へ提示し、製品受入だけを依頼する。修正要なら受入を提示しない。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。内部の開始レビュー担当と完了レビュー担当を使う許可は取得済みで、製品受入判断だけを最終段階で利用者へ戻す

## stale・deferred

- stale：最終技術検証Evidence v1とv2の完了判断はstale。現在根拠は再レビューv2とEvidence v3で、独立再々レビュー前のため製品受入根拠にはまだしない
- deferred：独立再レビューではfileを変更しない。設計、契約、既存入口、中央一覧、push、外部送信、自動削除、実Session記録の使用は変更・開始しない

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：残る2原因の新規2反例を含む保存核と新入口97件、既存正式入口・pipeline・provenance・開発環境30件が終了コード0
- 直近の全Test：修正後の正規全試験は1,862件成功、失敗・error・skip 0、終了コード0。receipt SHA-256はe1005f53740a3d2f1f5176a322b70a14874a63df5748cf7df5ab972dea7e3ca9
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
