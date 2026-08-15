# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理の製品受入が完了した。残る7候補を順に実行中である。
- 現在作業：候補2の実装作業票v1は開始前独立確認で条件12の停止元2例が未接続と判明した。設計fileと受入条件fileに確定した読取不能だけを追加した作業票v2を固定し、限定再確認へ進む。
- Task Contract：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004 / version_3_adopted / corrected_implementation_start_rereview_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の候補2実装を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

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

固定commitの実装作業票v2について、条件12の設計・受入条件・特定不能の読取失敗が3つの停止元へ分かれ、他条件が退行していないか限定再確認する。

開始条件：

- 実装作業票v2、開始前独立確認、本TODOがcommitへ固定され、作業場所に未記録差分がない
- 確認担当は製品コード、試験、作業票、TODOを変更しない
- 常にsource noneへ変える欠陥と、他条件の退行だけを確認する

完了条件：

- 独立開始前確認が開始可または修正要を固定する
- 開始可なら止める指摘と未接続条件が0件である
- 修正要なら境界1へ進まず、指摘原因だけを限定訂正する

後続作業：開始可なら境界1の失敗試験を固定して期待失敗を確認する。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし。契約v3採用と案C実装開始は利用者が承認済み

## stale・deferred

- stale：候補2の実装作業票v1開始可、契約採用待ち、契約候補v1・v2、v3独立再確認待ちの表示はstale
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
