# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存案Cの実装前コード管理について、固定file一覧ではなく作業ごとの必要な働きから直接処理と全repositoryの共通内部部品を探す案Aを実装した。現在は関連試験GREENで、実装commit後の正式な八つの働き検索が未実施である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_capability_search_green_current_execution_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：コード管理入口と現在検索を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `3453626fd168ac014d5e929017dbfb654bea6425164cfa3aa02bbfdf4aaa1c56`
- [一操作による現在検索Evidence](records/development/2026-08-15-safe-storage-formal-code-reuse-search-one-operation-execution-evidence-v1.md) — SHA-256 `2b9dffc209a730609a8c3ee8c031c7695db5188245390122f4a21be8c82f55d0`
- [必要な働きによる検索の実装計画](records/development/2026-08-15-capability-derived-code-reuse-search-implementation-plan-v1.md) — SHA-256 `f9ec5f1546705ce38d6abebbe886723c947331370d27fcf67ebff4ed07dade0d`
- [必要な働きによる検索の実装Evidence](records/development/2026-08-15-capability-derived-code-reuse-search-implementation-evidence-v1.md) — SHA-256 `05dd4aec4d46547955dfb62370204171c7a599c78d068e3f8fac6926a6938e63`
- [安全保存の八つの働き検索計画](records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v2.json) — SHA-256 `f652448f72e306fcac57ab05bf88200fce352994afb48017db04a3c5e13f1421`

## 次に行う一作業

必要な働きによる検索実装を意味単位でcommitした後、変更なしの同commitから安全保存の八つの働きを一操作で正式検索し、候補と未対応を固定する。

開始条件：

- 検索実装、試験、schema 2計画、開発方針、source universe v7、freshness policy v10がcommitされ、作業場所に未commit変更がない
- 安全保存の八つの働きとnew-only証明書pathが計画内容識別値へ結び付き、出力先が未作成である
- 検索元を現在のGit管理コードから生成し、過去の20 pathまたは中央一覧へ制限しない
- ライフサイクルと再利用方法を自動裁定しない

完了条件：

- 八つの働きが同じcommit、source content ID、Profile、Discoveryへ結び付く
- 働きごとの候補、根拠、禁止副作用との衝突、sourceの成熟度表示、未対応がnew-only正本と証明書へ残る
- 候補の採用、不採用、修正利用とDecisionによる正式・使用停止の照合をHuman裁定待ちとして返す
- 製品コード、製品試験、製品設定、Task Contract、製品TDD境界を変更しない

後続作業：検索結果を固定した後、必要な候補だけをHumanが採否判断し、その後に別機能である製品TDD境界確認へ戻る。

## blocker・Human判断待ち

- blocker：検索実装にはblockerがない。正式検索はcleanな実装commitが必要なため、現在の未commit実装状態では実行しない。
- Human判断待ち：現時点で追加判断はない。正式検索後、実装依存へ採用する候補についてだけ採用、不採用、修正利用と正式・暫定・使用停止を利用者へ戻す。

## stale・deferred

- stale：固定20 pathによるv1検索と二つのv2証明書はcommit 0a02b51の履歴観測として保持するが、現在の実装開始根拠には八つの働きによる新検索を使う。
- deferred：八つの働きの検索と候補裁定が終わるまで、製品TDD境界、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、自動commit、push、外部送信も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：必要な働き検索、旧検索、鮮度、外部化、一操作入口の関連46件と、方針・権威参照29件が成功した。新しいコードによるstale、必要・禁止の副作用の同時指定拒否、実行時間と検索identityの分離を含む。
- 直近の全Test：実行時間の計測を含む正規全試験は1,758件成功、失敗・error・skip 0、終了コード0だった。Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
