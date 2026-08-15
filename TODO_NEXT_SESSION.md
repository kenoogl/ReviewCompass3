# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理の製品受入が完了した。残る7候補を順に実行中である。
- 現在作業：候補2の実装作業票v1・v2は独立限定再確認で開始可となった。止める原因0件、未接続条件0件、退行0件で、境界1の比較核について先行失敗試験を固定する。
- Task Contract：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004 / version_3_adopted / boundary_1_red_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の候補2実装を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [実装開始前限定再確認・開始可](records/development/2026-08-15-one-design-acceptance-implementation-start-correction-review-v1.md) — SHA-256 `b4a4c837eeb0e74867bff6a9ff5e6696cd7972b2bdb0c94edf30ea9ca1600b15`
- [条件12だけを限定訂正した実装作業票v2](docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md) — SHA-256 `a733a57203a0148c52d722713be4b3948134192da6f5bceef8ab5eb92e9a58ec`
- [実装開始前独立確認・条件12修正要](records/development/2026-08-15-one-design-acceptance-implementation-start-review-v1.md) — SHA-256 `886f599af67d2b80389b95d3b06b504ab5ae7f77f27723892c3a02b177269db1`
- [候補2の契約採用・案C実装開始判断](records/development/2026-08-15-one-design-acceptance-contract-adoption-and-implementation-start-decision-v1.md) — SHA-256 `0287184fd38a3b47bc8630ef447c6c491b4cfad2c614692b4cdab99af8abad0d`
- [独立確認済みの採用契約v3](records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md) — SHA-256 `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- [候補2の既存G08実測と契約定義Evidence](records/development/2026-08-15-one-design-acceptance-contract-definition-evidence-v1.md) — SHA-256 `9bad2d80fcddb6f97f9db71fa05a4811ce59404353aa07fb55c3070784d5f6b5`
- [直前製品の受入判断](records/development/2026-08-15-one-item-review-product-acceptance-decision-v1.md) — SHA-256 `8401ff7bd145755af2d5893db2da1fd5d00ee62c224d1602c3080c380f454441`
- [安全保存受入後の次製品作業候補8件](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [製品コード候補と作業契約入力の目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

境界1の比較核について、4比較、欠落、未参照、同名JSON項目、schema、正規化、内容識別値、人の判断一覧の失敗試験だけを追加し、実装不在による期待失敗を確認する。

開始条件：

- 開始可の限定再確認、本TODOがcommitへ固定され、作業場所に未記録差分がない
- 対象試験fileだけを追加し、製品核、入口、配布設定を作らない
- 契約条件1〜9の正常・負例と出力schemaを試験へ固定する

完了条件：

- 対象試験を単独実行し、実装不在だけを原因として期待失敗する
- 失敗件数と原因を境界1 RED Evidenceへ固定する
- 試験とEvidenceをcommitしてから最小実装へ進む

後続作業：境界1の試験を変えず、比較核だけを実装して全対象試験を成功させる。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。契約v3採用と案C実装開始は利用者が承認済み

## stale・deferred

- stale：候補2の開始前独立確認待ち・修正要、実装作業票v1単体、契約採用待ちの表示はstale
- deferred：候補2の製品受入、候補3以降の採用・実装、外部送信、実利用者設計は後続境界まで対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：候補2の既存G08関連31件が成功、終了コード0。既存G08 2実装fileと2試験fileは基準commitから差分0
- 直近の全Test：直近の正規全試験2,020件成功、失敗・error・skip 0、終了コード0。候補2実装後に再実行する
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
