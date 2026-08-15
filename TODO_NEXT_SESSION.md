# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存の製品受入が完了し、三つ目の製品処理を契約v3で実装する段階へ進んだ。
- 現在作業：実装作業票v2は独立変更点確認で開始可、止める原因0件、受入条件1〜18の未接続0件となった。製品コードは未変更で、境界1の失敗試験を先に固定する段階にいる。
- Task Contract：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-003 / v3_adopted / option_c_implementation_start_approved / tdd_boundary_1_red_ready`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約定義確認を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

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

境界1だけの対象試験を新規作成し、正常な一件読取りが製品核不在という主要理由で失敗するREDを確認する。

開始条件：

- 開始可の訂正確認、本TODOが意味単位commitへ固定され、作業場所に未記録差分がない
- 変更pathはtests/test_one_item_review.pyだけとし、製品codeとpyproject.tomlをまだ変更しない
- 正常読取りと境界1の拒否例を記述するが、REDは実装不在という主要理由一つで確認する

完了条件：

- 対象試験の収集に成功する
- 正常な一件読取り試験が製品核不在の期待理由で失敗する
- 失敗がfixture、import typo、環境依存、別境界の期待によるものではない

後続作業：RED確認後、試験を変えずに境界1の安全な一件読取りだけを製品核へ最小実装し、GREENを確認する。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。契約v3採用と案C実装開始は承認済み。境界1は承認済み作業票v2に従うTDD実装である

## stale・deferred

- stale：実装作業票v1と開始前レビュー待ち表示はstale。契約候補v1・v2、契約採用待ち表示、候補1選択待ち表示もstale
- deferred：境界1のRED確認までは製品codeとpyproject.tomlを変更しない。境界2以降、既存G02、保存、外部送信、外部処理、実利用者資料は現在の一作業では対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：製品試験は未実施。作業票v2の独立確認は条件1〜18欠番・重複0、六境界必須欄欠落0、G02 14 file差分0、結果集合のpath・高乱雑性反証成功、終了コード0で開始可
- 直近の全Test：製品コードと試験を変更していないため再実行していない。直近の正規全試験は1,862件成功、失敗・error・skip 0、終了コード0
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
