# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理の製品受入が完了した。残る7候補を順に実行中である。
- 現在作業：候補2の境界2は、安全読込の追加試験24件が公開関数不在だけを原因として期待失敗し、境界1の43件は成功を維持した。試験とRED Evidenceを固定し、安全読込だけを実装する。
- Task Contract：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004 / version_3_adopted / boundary_2_red_verified / green_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の候補2実装を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [境界2の期待失敗24件と原因を固定したRED Evidence](records/development/2026-08-15-one-design-acceptance-boundary2-red-evidence-v1.md) — SHA-256 `7fa3eed3ee2170afdbfb8fef1351da1c0addeb43dab4645232dfcabc7e3ec658`
- [境界1の固定試験43件と既存関連31件を固定したGREEN Evidence](records/development/2026-08-15-one-design-acceptance-boundary1-green-evidence-v1.md) — SHA-256 `eacbcb1198916f00c2cbc6356f2ef5d3a8fab262959b6b3ebcbe033ab0042709`
- [境界1の期待失敗43件と原因を固定したRED Evidence](records/development/2026-08-15-one-design-acceptance-boundary1-red-evidence-v1.md) — SHA-256 `37790022390ee14875f7b9706604ac448df588a58b182db9245b56f0b911371e`
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

境界2の固定済み追加試験24件を変更せず、比較核moduleへ安全読込だけを実装する。

開始条件：

- 境界2試験、RED Evidence、本TODOが意味単位commitへ固定される
- 境界1と境界2の試験67件を変更しない
- CLI入口と配布設定には着手しない

完了条件：

- 対象試験67件を単独実行して全件成功し、終了コード0となる
- 既存G08保護対象4fileが基準commitから差分0である
- 安全読込とGREEN Evidenceをcommitしてから境界3へ進む

後続作業：境界3の正式命令入口と安全表示について先行失敗試験を固定する。

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
- 直近の関連Test：候補2の境界2追加試験24件は安全読込公開関数不在だけを原因として期待失敗、境界1固定43件は成功、対象全体は終了コード1。既存G08関連31件は直前成功、保護対象4fileは基準commitから差分0
- 直近の全Test：直近の正規全試験2,020件成功、失敗・error・skip 0、終了コード0。候補2実装後に再実行する
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
