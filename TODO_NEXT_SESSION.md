# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存案Cの実装前コード管理について、現在のGit管理コード全体から八つの働きを正式検索し、直接確認対象、手掛かり、比較集団、成熟度を分けた証拠を固定した。候補の再利用方法に関するHuman裁定が未実施である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_capability_search_completed_reuse_adjudication_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：コード管理入口と現在検索を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `3453626fd168ac014d5e929017dbfb654bea6425164cfa3aa02bbfdf4aaa1c56`
- [比較候補生成との整合訂正判断](records/development/2026-08-15-capability-reuse-search-work4a-alignment-correction-decision-v1.md) — SHA-256 `1abe7a52c20e33d77f2f908f81dcf96c012bf5e07034b7431cbe9609f686aca6`
- [必要な働き検索の整合訂正実装Evidence](records/development/2026-08-15-capability-reuse-search-work4a-alignment-implementation-evidence-v1.md) — SHA-256 `addd9838d07f74628af3cce08afff93c3389305dae33695a118962348706504e`
- [安全保存の八つの働き検索計画v4](records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v4.json) — SHA-256 `1c9fef66370e3a067500ea0d6c1ecce9b77e0a9a107b51ad52c99519aab6ac45`
- [八つの働き正式検索Evidence](records/development/2026-08-15-safe-storage-capability-search-formal-execution-evidence-v1.md) — SHA-256 `d433fcdae6fea26f2fb8f3de703f54db9d7b2905dd4cbd6f2552739d5c645dbc`
- [八つの働き検索証明書](records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v3.json) — SHA-256 `de06acf8367b99b84ab0643652a05058065cd381798a2bc32d1990281f446322`

## 次に行う一作業

八つの働きごとに、正式検索で得た直接確認対象を「そのまま再利用」「条件を補って再利用」「参考だけ」「新規実装」のいずれにするか、利用者が裁定する。

開始条件：

- 正式検索Evidenceと証明書が同じcommit、source content ID、処理一覧、比較集団へ結び付き、既存検証処理でfreshと確認済みである
- 手掛かりと比較集団を再利用可能な処理の件数とみなさず、直接確認対象だけを採否の入口にする
- 暫定処理を自動的に正式化せず、再試行可能な削除は直接対応する既存処理なしという観測を維持する

完了条件：

- 八つの働きそれぞれに再利用方法と理由が一つずつ記録される
- 採用または修正利用する処理が関数単位、成熟度、安全条件へ結び付く
- 不採用と参考だけの処理を製品実装の依存として扱わない
- 製品コード、製品試験、製品設定、Task Contract、製品TDD境界を変更しない

後続作業：再利用方法の裁定後、別機能である製品TDDの実装境界事前確認を行い、小さい失敗確認と成功確認へ分けられる場合だけ実装計画へ進む。

## blocker・Human判断待ち

- blocker：機械検索にblockerはない。製品実装へ進む前に再利用方法のHuman裁定が必要である。
- Human判断待ち：検索Evidence §5の八つの提案を採用するか。特に、暫定処理は関数単位の修正利用または参考に限定し、再試行可能な削除は新規実装候補とするか。

## stale・deferred

- stale：固定20 pathによる旧検索、過大な平坦候補を作った能力検索v1からv3、および対応する旧証明書は履歴観測として保持するが、現在の実装開始根拠に使わない。
- deferred：再利用方法の裁定と製品TDD境界確認が終わるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。中央一覧、自動commit、push、外部送信も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：必要な働き検索と正式入口の対象16件、Work 4A等を含む関連181件が成功した。正式検索証明書と外部正本の再照合もfreshで合格した。
- 直近の全Test：検索実装の正規全試験は1,762件成功、失敗・error・skip 0、終了コード0だった。Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。以後の変更は検索計画とEvidenceだけで、コード・試験・設定に変更はない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
