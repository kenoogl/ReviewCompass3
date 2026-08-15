# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理の製品受入が完了した。
- 現在作業：候補1の六境界実装、全確認、独立完了レビュー、合成一件、利用者の製品受入を完了した。次は候補2のG08設計・受入条件照合について、実装前の作業契約候補を一件に限定して定義する。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003 / completed / accepted_as_product`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約定義確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [一件レビュー材料作成・結果整理の製品受入判断](records/development/2026-08-15-one-item-review-product-acceptance-decision-v1.md) — SHA-256 `8401ff7bd145755af2d5893db2da1fd5d00ee62c224d1602c3080c380f454441`
- [合成一件の利用者向け受入表示Evidence](records/development/2026-08-15-one-item-review-synthetic-acceptance-evidence-v1.md) — SHA-256 `de5df0ccb9f7a41431721a59b001c2033af5421635db2c4781ea812ed5c592fe`
- [固定commitの独立完了レビュー・確認済み](records/development/2026-08-15-one-item-review-independent-completion-review-v1.md) — SHA-256 `8c2a112a095beb93e906b8f969f1f1fc66953643f0ffca9a6c76d67cba159969`
- [六境界・全試験・高危険度反例の最終検証](records/development/2026-08-15-one-item-review-final-verification-evidence-v1.md) — SHA-256 `3c11a18d68d50b54aba7465290534690b49cabe6c6295126f6a1c29ab1dd4aaa`
- [境界6の配置・結合・回帰確認成功](records/development/2026-08-15-one-item-review-boundary6-green-evidence-v1.md) — SHA-256 `a9ead3decf81c48e2465eb769929f59d8f2833fe0f3902cb1ef046761991075f`
- [境界6の別現在位置実行2件と期待失敗](records/development/2026-08-15-one-item-review-boundary6-red-evidence-v1.md) — SHA-256 `afd763b8560c85f75eb92cbb79a5c11b7dadb6b71cf7a3d0009adaec0caec3b4`
- [境界5の正式入口・安全表示156件成功](records/development/2026-08-15-one-item-review-boundary5-green-evidence-v1.md) — SHA-256 `2bf610c3dc0d45642a6e7824929e12d1bbf63bc0f780f70c832cb05cc31d7237`
- [境界5の正式入口・安全表示10件と期待失敗](records/development/2026-08-15-one-item-review-boundary5-red-evidence-v1.md) — SHA-256 `32670c7428a2f0ecc5fbbf76cdfa4d275db61dd8e8bd2041b14045d106820244`
- [境界4の分類・人の判断一覧146件成功](records/development/2026-08-15-one-item-review-boundary4-green-evidence-v1.md) — SHA-256 `f3d593576970cc65b3ca57687f564bae6cb01cac8f1056f27e6aab8cee4620fc`
- [境界4の分類・人の判断一覧4件と期待失敗](records/development/2026-08-15-one-item-review-boundary4-red-evidence-v1.md) — SHA-256 `0149e217f15cff256530d9138cc00341ed122906caad73a4dd7df354609dac7d`
- [境界3の結果集合検査・対象142件成功](records/development/2026-08-15-one-item-review-boundary3-green-evidence-v1.md) — SHA-256 `93b3baf8f3aa22730f327aa51b52c046e69ca1a522f529d7f73d0946a09c4b6c`
- [境界3の結果集合検査57件と期待失敗](records/development/2026-08-15-one-item-review-boundary3-red-evidence-v1.md) — SHA-256 `5d3c5dd8a99a959c653c41f479ac3d9ed7f86b221f5bc6f65776a0e28e96097b`
- [境界2の固定材料と安全停止・対象85件GREEN](records/development/2026-08-15-one-item-review-boundary2-green-evidence-v1.md) — SHA-256 `62559de8569b270fdfaac8e0332617cc915c1e7c8c7a4e96e26f93bed934ffc4`
- [境界2の対象56件と期待RED](records/development/2026-08-15-one-item-review-boundary2-red-evidence-v1.md) — SHA-256 `f2643dc006074b68b27e8639337c390d7b624cfc329096357c49a9a254bc3d59`
- [境界1の安全読取り核と対象29件GREEN](records/development/2026-08-15-one-item-review-boundary1-green-evidence-v1.md) — SHA-256 `50bcd7914a4ab35cc5b5501303540e7d542a9e77b4ad4bc303ab2703efb64146`
- [境界1の対象試験29件と期待RED](records/development/2026-08-15-one-item-review-boundary1-red-evidence-v1.md) — SHA-256 `145c29a0ad4d7149f06693275fc46c7b52cef73fcc7bfac0753a1a8f2bd7c33c`
- [作業票v2の独立変更点確認・開始可](records/development/2026-08-15-one-item-review-implementation-start-correction-review-v1.md) — SHA-256 `aec75a2636be23ca4d0458abcaa8123b8e34d6c32f8e97f6468f890fb80d2201`
- [結果集合の安全検査未接続を示した開始前レビュー](records/development/2026-08-15-one-item-review-implementation-start-review-v1.md) — SHA-256 `41e40a501942b4513300d28e4c24d4dd44e5c3626da49e5aa89b17dde9a441d4`
- [結果集合安全検査と条件対応表を追加した実装作業票v2](docs/development/2026-08-15-one-item-review-implementation-work-ticket-v2.md) — SHA-256 `831eed390b3de03bad4ce55a9082e01eb7c97d2ad43bd5db35f0cd2b5f2b8765`
- [作業契約v3の採用・案C実装開始判断](records/development/2026-08-15-one-item-review-contract-adoption-and-implementation-start-decision-v1.md) — SHA-256 `ceda14c8240794dca7c4d6ab8715ad87750eb41501b5f0223fd3a0fb32416d12`
- [六境界を固定した製品TDD実装作業票](docs/development/2026-08-15-one-item-review-implementation-work-ticket-v1.md) — SHA-256 `999ccb6b1830816e39f648341b0649205cde573d416b3d586a8c63b7bf06a784`
- [残る2原因を限定訂正した作業契約候補v3](records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v3.md) — SHA-256 `a52cd717f6709c5ca01a1e339385272abfe976a0b9ce176e857b427778cf07d6`
- [作業契約候補v3の変更点確認・開始可](records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v2.md) — SHA-256 `2e612712b194517097f0439398f61e505d0d9bb18fe8c50ae8c39f9c39e1b423`
- [作業契約候補v2の変更点確認・修正要](records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v1.md) — SHA-256 `8544484e25c7af07743002793c63a591aa3ad63c2dd09ce74f512fead4899a1f`
- [作業契約候補v1の独立定義挑戦・修正要](records/development/2026-08-15-one-item-review-task-contract-definition-challenge-v1.md) — SHA-256 `c1ec9fc3dc033c1dbf14c5201966497b1e2c8eae18cd38ededce5e8637ebd4b3`
- [安全保存受入後の次製品作業候補8件](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [安全保存の製品受入判断](records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md) — SHA-256 `7145f57a59efb965f64a5401f6e109685ba1920b5039fe65a4edd644af7573dc`
- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [製品コード候補と作業契約入力の目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

候補2のG08設計・受入条件照合について、既存2 pathと上位目的を読み、一件・通信なし・保存なしの作業契約候補を作る。

開始条件：

- 候補1の製品受入判断と本TODOがcommitへ固定され、作業場所に未記録差分がない
- 既存候補表のG08に対応する2 pathを機械的に特定し、現在の実測と上位目的を先に確認する
- 契約候補の作成だけを行い、採用、実装、既存試験変更を行わない

完了条件：

- 目的、入力、期待結果、対象外、許可操作、停止条件、確認方法が一件分に固定される
- 既存機能だけの最小案を含む3案と推奨理由が示される
- 独立した定義確認へ渡せる固定材料になる

後続作業：独立した定義確認で開始可になった後にだけ、利用者へ契約採用を求める。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。候補1の製品受入は利用者が明示済み。候補2は契約候補の定義までで実装を開始しない

## stale・deferred

- stale：候補1の製品受入待ち、独立完了レビュー待ち、実装作業票v1、開始前レビュー待ち、契約候補v1・v2、契約採用待ち、候補1選択待ちの表示はstale
- deferred：候補2の採用・実装、保存、外部送信、外部処理、実利用者資料、既存G02変更は次作業の対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象158件、G02関連142件、安全表示23件、高危険度反例40件が成功、各終了コード0。G02 14 fileは差分0
- 直近の全Test：正規全試験2,020件成功、失敗・error・skip 0、終了コード0。Python 3.13.14、pytest 8.4.2、runner版2、代替実行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
